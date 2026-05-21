---
name: repository-dependency-graph
description: Analyze the service topology of a multi-repository application. Given an application name and repository paths, identifies each independently deployable service, infers each service's role and language, detects inter-service dependencies, and produces a topology graph (Markdown).
---

# Repository Dependency Graph

<!-- ff:ai_analysis:start -->

Analyze the service topology of the application identified by the `name` parameter. For each
repository in `entries`, identify the independently deployable services it contains, infer their
roles and languages, and detect inter-service dependencies. Produce a topology graph in Markdown
format and save it to `{report-dir}/application-topology-graph.md`.

## Input Parameters

- `name` (required): The short, human-readable display name for the application. Used as the
  report heading and in the service table.
- `entries` (required, list): One or more repository entries belonging to this application. Each
  entry is an object with:
  - `repoName` (required): The canonical display name for the repository (e.g. `order-service`).
    Used in the topology graph, service table, and as the basis for slug generation. Takes
    precedence over the directory name for all naming and dependency-matching purposes.
  - `path` (required): The local filesystem path to the repository root.

  At least one entry must have an accessible `path`.
- `report-dir` (required): The directory where the output file is written. The directory is
  created and managed by the CLI runner; the skill must not modify its path or structure.

**Output filename**: `{report-dir}/application-topology-graph.md`

## Execution Steps

### Step 1: Validate Inputs

1. Verify `name` is non-empty. If empty, abort with:
   `> ERROR: The 'name' parameter is required and must not be empty.`
2. For each entry in `entries`, verify both `repoName` and `path` are present and non-empty. If
   either is missing, abort with:
   `> ERROR: Each entry in 'entries' must have both 'repoName' and 'path' fields.`
3. For each entry in `entries`, check whether `path` is accessible (exists and is readable).
   - Collect accessible entries into a working set.
   - Collect inaccessible entries into an `inaccessible` list for reporting.
4. If the working set is empty (all paths are inaccessible), abort with:
   `> ERROR: Topology analysis skipped for '{name}': none of the provided repository paths could be accessed.`
5. If `report-dir` does not exist or is not writable, abort with:
   `> ERROR: Output directory '{report-dir}' does not exist or is not writable.`

### Step 2: Per-Repository Service Identification

For each accessible entry in `entries`, identify independently deployable services using `entry.path`
as the filesystem root. Use `entry.repoName` as the canonical repository name — it replaces
directory-name inference for display labels, slug generation, and cross-repository dependency
matching.

**Build file detection** (determines language, framework, and service candidates):

| Build file | Language | Framework hints |
|------------|----------|-----------------|
| `pom.xml` | java | Check `<parent>` for `spring-boot-starter-parent` → Spring Boot; `quarkus-bom` → Quarkus; `micronaut-parent` → Micronaut |
| `build.gradle` / `build.gradle.kts` | java | Check `plugins {}` for `org.springframework.boot`, `io.quarkus`, `io.micronaut.application` |
| `*.csproj` | dotnet | Check `<TargetFramework>` and packages for `Microsoft.AspNetCore.*` → ASP.NET Core; `Microsoft.Azure.Functions.Worker` → Azure Functions |
| `*.sln` / `*.slnx` | dotnet | Multi-project solution; recurse into sub-projects |
| `package.json` (with `"start"` script or `"main"` field) | javascript/typescript | Check `"dependencies"` for `express`, `fastify`, `koa`, `@nestjs/core`, `next`, `react`, `vue`, `@angular/core` |
| `tsconfig.json` (without `package.json`) | typescript | Infer TypeScript library |

**Service identity** (one candidate per independently deployable unit):

- For single-service repos: use `entry.repoName` as the service name.
- For monorepos: use `entry.repoName` as the repository label; detect multiple deployable units by looking for:
  - Multiple `Dockerfile` files at different subdirectory levels (each names a service)
  - Multiple `*.csproj` files with `<OutputType>Exe</OutputType>` or `<OutputType>exe</OutputType>`
  - Multiple `pom.xml` files in subdirectories (each with its own `<artifactId>`)
  - Multiple `package.json` files with a `"start"` or `"main"` script at subdirectory level
  - Each detected unit becomes a separate Service entry; `subPath` is set to its relative path within the repo.

**ServiceRole inference rules** (apply in order; first match wins):

| Role | Evidence |
|------|----------|
| `ApiGateway` | Name or directory contains `gateway`, `proxy`, `edge`, `ingress`; OR Spring Cloud Gateway / Netflix Zuul dependency detected |
| `Frontend` | Framework is React, Angular, Vue, Blazor, Next.js, Nuxt; OR name contains `ui`, `web`, `frontend`, `portal`, `dashboard` |
| `Worker` | No inbound HTTP port exposed in Dockerfile; OR name contains `worker`, `consumer`, `processor`, `job`, `scheduler`, `daemon`; OR Spring Batch / Azure WebJobs / Hangfire dependency detected |
| `DataService` | Name contains `db`, `data`, `repository`, `store`, `cache`; OR heavy ORM usage (Spring Data JPA, EF Core DbContext is >50% of dependencies) |
| `SharedLibrary` | No `Dockerfile` and no executable entry point; name contains `lib`, `shared`, `common`, `sdk`, `client` |
| `WebApi` | HTTP framework detected (Spring MVC, ASP.NET Core controllers, Express, NestJS, FastAPI) and none of the above matched |
| `Unknown` | None of the above rules matched |

**Service ID**: Lowercase slug of service name (replace spaces, dots, underscores with hyphens; remove non-alphanumeric except hyphens). Must be unique within the application.

### Step 3: Cross-Repository Dependency Detection

For each service, scan the following configuration and build files for references to other service names/identifiers discovered in Step 2:

**Files to scan**:
- `application.properties`, `application.yml`, `application.yaml` (Spring Boot)
- `appsettings.json`, `appsettings.*.json` (ASP.NET Core)
- `*.env`, `.env`, `.env.*`
- `docker-compose.yml`, `docker-compose.yaml`, `docker-compose.*.yml`
- Helm chart `values.yaml`, `values.*.yaml`
- Kubernetes manifests (`*.yaml` in `k8s/`, `kubernetes/`, `deploy/`, `manifests/` directories)
- `pom.xml` (Maven dependencies — detect another service's `artifactId` as a dependency)
- `*.csproj` (NuGet `<PackageReference>` — detect another service's project/package name)
- `package.json` (`dependencies` / `devDependencies` — detect another service's package name)

**What to look for**:

| DependencyType | Evidence |
|----------------|----------|
| `HttpCall` | Property value matching a pattern like `http(s)://{service-name}`, `{service-name}.default.svc`, `{service-name}:PORT`, or an environment variable named `{SERVICE_NAME}_URL` / `{SERVICE_NAME}_HOST` / `{SERVICE_NAME}_BASE_URL` |
| `MessageQueue` | Property key or value containing a topic/queue name that also appears in another service's config (e.g., `spring.kafka.topic`, `rabbitmq.queue`, `azure.servicebus.topic`) |
| `SharedLibrary` | Build file dependency whose artifact/package name matches another service's slug or name (common for `SharedLibrary`-role services) |
| `DirectReference` | `depends_on:` in docker-compose; Kubernetes service reference; direct project reference in `.sln` / `*.csproj` |

For each detected dependency, record:
- `targetServiceId` (the other service's slug)
- `dependencyType` (from the table above)
- `evidence` (the config file path and key/value that triggered the match, e.g., `appsettings.json: ServiceUrls:OrderService = http://order-service`)

Only record dependencies where **both** the source service and the target service are within the analyzed set. Do not record dependencies on external services (databases, cloud services, etc.) — those are covered by the `dependency-map` skill.

### Step 4: Cycle Detection

Perform a depth-first search (DFS) on the directed dependency graph.

- Maintain a visited set and a recursion stack.
- When a back edge is detected (a node already in the recursion stack is encountered again), record the cycle as a warning string:
  `"Circular dependency detected: {ServiceA} → {ServiceB} → ... → {ServiceA}"`
- Continue DFS after recording the cycle (do not abort).
- Collect all cycle warning strings into `cycleWarnings`.

### Step 5: Duplicate Service Detection

For each pair of services, check:
1. Are their slugified names identical? (e.g., `order-service` and `order-service`)
2. Do their names differ only by separator or case after normalization? (e.g., `orderservice` == `order_service` == `OrderService`)
3. Do their primary entry-point artifact names match? (e.g., same Maven `<artifactId>`, same .NET assembly name)

If any condition is true, add to that service's `warnings` list:
`"WARNING: Potential duplicate of '{other-service-name}' (from {other-repo-name} at {other-repo-path}). Verify these are not the same service."`

### Step 6: Generate Mermaid Diagram

Build a `flowchart TD` diagram.

**Node format**: `{ServiceId}["{ServiceName}\n({Role})"]`
- Example: `orderSvc["order-service\n(WebApi)"]`

**Edge format** (normal dependency):
`{SourceId} -->|"{DependencyType}"| {TargetId}`
- Example: `apiGateway -->|"HttpCall"| orderSvc`

**Cycle edge format**:
`{SourceId} -.->|"⚠ cycle"| {TargetId}`

**Node label rules**:
- Use plain text only; avoid `@`, `#`, `$`, `%`, `&`, `<`, `>`, `"` inside node labels
- Replace double quotes in names with single quotes before embedding in labels
- All node IDs must be unique across the diagram

**Scale limit (40-node rule)**:
- If total service count ≤ 40: show all services individually.
- If total service count > 40: collapse per-repository into aggregate nodes:
  - `{repoSlug}Grp["{repoName}\n({N} services)"]` where `{repoSlug}` is the slug of `entry.repoName`
  - Show only cross-repository edges between aggregate nodes.
  - Add a note at the top of the diagram section: `> Note: {N} services exceed the 40-node display limit. Services are grouped by repository.`

### Step 7: Render Output

Produce the final output content:

**Markdown format** :

```
# Topology Graph: {name}

Analyzed {N} service(s) across {M} repositor(y/ies) for application "{name}" on {YYYY-MM-DD HH:MM UTC}.

## Services

```mermaid
{mermaid diagram content}
```

## Service Details

| Service | Role | Language | Source Repository | Warnings |
|---------|------|----------|------------------|----------|
| {service-name} | {Role} | {language} | {repoName} | {warnings or —} |
...

## Warnings

- {cycle warning 1}
- {cycle warning 2}
- {duplicate warning}
- Inaccessible repository: {repoName} ({path}) (skipped)
```
(Omit `## Warnings` section entirely when no warnings exist.)

### Step 8: Save Output

1. Compute the output filename:
   - Full path: `{report-dir}/application-topology-graph.md`
2. Write the rendered content to the output file (create or overwrite).
3. Log: `Topology graph for '{name}' saved to {output-path}`

## Scaling Rules

- Maximum 40 Mermaid nodes for GitHub rendering compatibility and diagram legibility.
- When service count > 40: collapse to per-repository aggregate nodes (Step 6 scale limit rule).
- Performance expectation: analysis of 3–10 repositories should complete in under 5 minutes on a
  standard developer workstation.
- For very large monorepos (>20 sub-projects), limit per-repo service detection to a maximum of
  10 services; add a note in the Warnings section: `Note: Repository '{repo}' contains more than
  10 detected services; only the first 10 are shown.`

## Mermaid Syntax Rules

- Use `flowchart TD` (top-down layout).
- Avoid special characters in node labels: `@`, `#`, `$`, `%`, `&`, `<`, `>`.
- Always quote arrow labels with double quotes: `-->|"label"|`.
- Use `-.->` (dotted arrow) for cycle edges with label `"⚠ cycle"`.
- All node IDs must be unique across the entire diagram.
- Do not use `subgraph` — flat node layout only (services are already grouped logically by role
  via node labels).

## Error Handling

| Condition | Behavior |
|-----------|----------|
| All `entries` inaccessible | Abort with error message (Step 1). No output file written. |
| Subset of paths inaccessible | Continue with accessible subset. Add each inaccessible entry as `Inaccessible repository: {repoName} ({path}) (skipped)` in Warnings section. |
| Missing `repoName` or `path` field | Abort with error message (Step 1). No output file written. |
| No build files found in any repository | Best-effort: list each repo as a service with `role: Unknown` and `language: unknown`. Add note in Warnings: `Note: No recognized build files were found. Service roles could not be inferred.` |
| Unsupported project type | Set `language: unknown` and `role: Unknown` for that service. Do not fail. |
| Service name collision (duplicate IDs after slugification) | Append the `repoName` as a suffix: `{slug}-{repo-name-slug}`. |
| Output file write error | Log error: `Failed to write topology graph for '{name}' to {report-dir}/application-topology-graph.md: {error}`. Do not abort the parent process. |

## Success Criteria

- Output file `{report-dir}/application-topology-graph.md` is created and non-empty.
- File contains at least one service node in the Mermaid diagram.
- All inaccessible repository paths are listed in the Warnings section (none silently ignored).
- The Mermaid diagram contains no syntax errors (valid `flowchart TD` syntax).
- The Service Details table has one row per detected service.
- The Warnings section is present only when at least one warning exists.
- No unhandled exceptions propagate to the assessment pipeline.

<!-- ff:ai_analysis:end -->
