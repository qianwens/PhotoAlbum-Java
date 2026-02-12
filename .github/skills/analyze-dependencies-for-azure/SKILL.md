---
name: analyze-dependencies-for-azure
description: Analyze application dependency files to identify dependencies that should be migrated to Azure services, and recommend framework upgrade paths.
---

# Analyze dependencies for Azure service recommendations and upgrade paths

This skill analyzes application dependency files (such as `pom.xml`,
`build.gradle`, `build.gradle.kts`, `*.csproj`) across multiple
repositories. It produces two outputs:

1. **Azure service recommendations** — dependencies that should map
   to Azure services when migrating to Azure.
2. **Framework upgrade paths** — detected framework/runtime versions
   and their recommended upgrade targets.

You receive:

- **Dependency file contents** stored as a JSON file at
  `dependency-files-json-path`. Read this file first. It is a JSON
  object whose keys are `"{repoName}::{filePath}"` and values are
  the file contents (text).

## Your task

1. **Read** the JSON file at `dependency-files-json-path`.

2. **Identify Azure-relevant dependencies** — libraries, packages, or
   modules that represent backing services, middleware, or
   infrastructure (databases, messaging, caching, storage, auth,
   secrets, email, logging, scheduling, etc.) and recommend the best
   Azure service for each.

3. **Detect framework / runtime versions** from the dependency files
   and recommend upgrade paths. Report only these framework types:
   - Java X (e.g. "Java 8", "Java 11", "Java 17")
   - Spring Boot X / Spring X (e.g. "Spring Boot 2.7")
   - .NET Framework X (e.g. ".NET Framework 4.8")
   - .NET X (e.g. ".NET 6", ".NET 8")
   - Java EE / Jakarta EE (e.g. "Java EE 8")

   Each Java app must appear in at least a JDK entry. Each .NET app
   must appear in at least a .NET Framework or .NET entry. Add
   Spring Boot / Java EE entries only when detected.

4. **Produce a JSON output file** at the path specified by
   `output-json-path`.

## Output format

Write a JSON file with this exact structure:

```json
{
  "recommendations": [
    {
      "dependency": "<human-readable name, e.g. 'Apache Kafka'>",
      "category": "<database | messaging | caching | storage | auth | secrets | email | logging | scheduling | other>",
      "detectedIn": ["<repoName1>", "<repoName2>"],
      "detectedArtifacts": ["<artifact-id or package-name>"],
      "options": ["<Azure Service Option 1>", "<Azure Service Option 2>"],
      "recommendation": "<ONE recommended Azure service>",
      "rationale": "<1-2 sentences>"
    }
  ],
  "upgradePaths": [
    {
      "framework": "<framework with version, e.g. 'Java 11', '.NET Framework 4.8'>",
      "detectedIn": ["<repoName1>", "<repoName2>"],
      "apps": "<number of apps using this framework version>",
      "recommendation": "<latest LTS stable version to upgrade to>",
      "rationale": "<short rationale>"
    }
  ]
}
```

## Rules

1. **Aggregate across repos.** Same dependency in multiple repos →
   single entry with all repos in `detectedIn`.
2. **Be specific with Azure names.** Use full names like
   "Azure Cache for Redis", "Azure Service Bus".
3. **One entry per logical dependency.** Group related artifacts
   (e.g. `spring-kafka` + `kafka-clients` → one Kafka entry).
4. **Skip irrelevant dependencies.** No test frameworks, build
   plugins, or standard utilities (JUnit, Mockito, Lombok, xUnit, etc.).
5. **Group upgrade paths by framework + version.** Multiple apps
   on the same version → single entry with total app count and
   all repo names in `detectedIn`.
6. **Always produce valid JSON.** No trailing commas, no comments.
7. **Both arrays are required.** If nothing found, use empty arrays.

## Completion criteria

1. A valid JSON file exists at `output-json-path`.
2. Both `recommendations` and `upgradePaths` arrays are present.
3. Each entry has a non-empty `recommendation` and `rationale`.
4. Each `upgradePaths` entry has a `detectedIn` array listing repos.

If dependency files are empty or cannot be parsed, output
`{"recommendations": [], "upgradePaths": []}`.
