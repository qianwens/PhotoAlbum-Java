# Policies — Default Modernization Rulebook

Enforceable standards and hard boundaries for .NET and Java modernization. Every policy here is validatable against generated artifacts.

---

## Naming & Metadata Standards

**Pattern:** `{env}-{app}-{service}-{resourcetype}`
Example: `prod-contoso-api-app`, `prod-contoso-shared-kv`

| Segment | Values |
|---|---|
| `{env}` | `dev`, `stg`, `prod` |
| `{app}` | Workload identifier |
| `{service}` | Component name (`api`, `web`) |
| `{resourcetype}` | CAF abbreviation (`rg`, `app`, `kv`) |

**Required tags** on every resource:

| Tag | Example |
|---|---|
| `environment` | `dev`, `staging`, `production` |
| `owner` | `platform-team` |
| `cost-center` | `CC-4200` |
| `workload` | `contoso-orders` |
| `migration-wave` | `wave-2` |

---

## Security Requirements

**Identity:** Managed Identity required for all service-to-service auth. Use `DefaultAzureCredential`. Connection strings with embedded keys (`AccountKey=`, `SharedAccessKey=`) are prohibited. Service principal secrets permitted only for CI/CD with 90-day rotation.

**Secrets:** Azure Key Vault required. No secrets in source, config files, or env vars. Key Vault access via RBAC (Secrets User / Crypto User), not access policies.

**Network:** Private endpoints for all data services. NSGs on every subnet. No public IPs on workloads — route through App Gateway, Front Door, or APIM. TLS 1.2+ enforced; TLS 1.0/1.1 prohibited.

**Encryption:** At rest — platform-managed keys default; CMK via Key Vault for confidential/regulated data. In transit — TLS 1.2+ mandatory.

---

## Compliance Requirements

**Baseline:** WAF and CIS Azure Foundations Benchmark.

**Data classification:**

| Level | Applies | Controls |
|---|---|---|
| General | Default | Standard encryption |
| Confidential | PII, financial, health | CMK, audit logging, restricted access |

**Data residency:** Approved regions only (see Guardrails). No cross-region replication without override.

**Audit logging:** Diagnostic settings on all data-plane operations. Central Log Analytics workspace. 90-day online retention, 1-year archive.

---

## Guardrails (Hard Boundaries)

### Prohibited Technologies

| Technology | Reason |
|---|---|
| FTP / FTPS | Insecure; use managed storage |
| Basic authentication | Credential exposure |
| Self-signed certs (prod) | Trust chain violation |
| Legacy Azure SDKs (Track 1) | Deprecated |
| .NET Framework < 4.8 | EOL |
| Java < 11 | EOL |
| log4j 1.x | EOL, multiple known vulnerabilities |

### Prohibited Patterns

| Pattern | Reason |
|---|---|
| Hardcoded secrets/credentials | Security violation |
| Embedded connection keys | Use Managed Identity |
| `SELECT *` | Performance/coupling risk |

### Required Elements

Every generated service code must include:
- `/health` (liveness) and `/ready` (readiness) endpoints
- OpenTelemetry or Azure Monitor structured logging
- Graceful shutdown (SIGTERM / cancellation token)
- Retry with exponential backoff + jitter for external calls

### Approved Regions

`eastus`, `eastus2`, `westus2`, `westeurope`, `northeurope` — override per org as needed.

---

## Validation & Quality Gates

**Required scanners:** Container image scanning (Trivy or equivalent), dependency vulnerability scanning (Dependabot or equivalent).

**Pipeline gates:** Build, unit tests, code analysis, dependency scan, container scan, staging deployment, smoke tests, production deployment with approval gate. Minimum 80% code coverage.

**Confidence thresholds:** No High or Critical findings in dependency scan before production deployment.

---

## Coding Style Guidelines

General principles:

- `.editorconfig` required; generate from framework conventions if missing
- Descriptive names, no abbreviations unless domain-standard
- Prefer async/non-blocking patterns; 120-char soft line limit
- 4-space indent, LF line endings

### .NET
- Sync-over-async (`Task.Result`, `.GetAwaiter().GetResult()`) — deadlock risk
- `new HttpClient()` — socket exhaustion; use `IHttpClientFactory`
- `Thread.Sleep` in async paths — blocks threadpool; use `Task.Delay`
- Catch-all `catch(Exception)` without rethrow — swallows errors

### Java
- Blocking I/O in reactive pipelines — use `CompletableFuture` or reactive alternatives
- Catch-all `catch(Exception)` without rethrow — swallows errors
