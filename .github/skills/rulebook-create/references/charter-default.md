# Charter — Default Modernization Rulebook

## Metadata

- **Name:** `azure-app-modernization-default`
- **Description:** Default rulebook for modernizing .NET and Java applications to Azure App Service, Container Apps, or AKS

---

## Scope

**Included:** Java (8+), .NET Framework / .NET 6+ — web apps, REST/gRPC APIs, background workers, event-driven microservices. Custom libraries used by in-scope apps are in-scope.

**Excluded:** Mainframe/COBOL, desktop apps (WinForms/WPF/Electron), embedded/IoT, standalone database migrations, standalone data pipelines/ETL, Node.js and Python applications.

**Constraints:**

| Constraint | Rule |
|---|---|
| Traffic | Production apps require zero-downtime migration (blue-green, canary) |
| Timelines | Target 90-day execution cycles per wave |
| Compliance | Regulated apps (PCI-DSS, HIPAA, FedRAMP) must preserve compliance posture |

---

## Modernization Strategy (6R Guidelines)

Of the 6R strategies, this rulebook covers **Rehost**, **Replatform**, and **Refactor** — the three that involve app modernization. Retire, Retain, and Repurchase are outside the scope of app modernization.

Supported strategies: **Rehost** (lift-and-shift, no code changes), **Replatform** (minimal code changes — containerize, adopt managed services), **Refactor** (modify code/architecture — decompose, upgrade).

| App Type | Strategy | Target | Override |
|---|---|---|---|
| Stateless web apps / APIs (containerized) | Replatform | Container Apps | Complex orchestration → AKS |
| Stateless web apps / APIs (non-containerized) | Replatform | App Service | — |
| Apps with OS-level dependencies (COM, registry, custom installers) | Rehost | App Service Managed Instance | Can containerize → Container Apps or AKS |
| Stateful monoliths | Refactor | Container Apps + backing services | Cannot decompose in timeline → App Service |
| Legacy (EOL framework) | Refactor | Container Apps on supported runtime | OS dependencies → App Service MI |
| Background workers / jobs | Replatform | Container Apps | Complex orchestration → AKS |
| Event-driven / messaging | Replatform | Container Apps + Service Bus | Complex orchestration → AKS |

**Decision sequence:** Match app to table row → apply default unless override met → escalate to architecture review if no match.

---

## Principles

| # | Principle | Rule |
|---|---|---|
| 1 | Cloud-first | Target Azure PaaS by default; IaaS only when required |
| 2 | Zero data loss | Validated data migration and rollback plan before cutover |
| 3 | Reversibility | Prefer reversible steps; no one-way doors without sign-off |
| 4 | Least privilege | Azure RBAC + managed identities; no shared credentials |
| 5 | Infrastructure as code | All infra in Bicep or Terraform; no portal-only resources |
| 6 | Observability | Structured logs, metrics, distributed traces via Azure Monitor |
| 7 | Managed services | Managed databases, caches, brokers over self-hosted |
| 8 | Minimize blast radius | Small independent waves; resource group isolation |
| 9 | Cost awareness | Right-size resources; consumption SKUs; tag for cost attribution |
| 10 | Security by design | Defender for Cloud, TLS 1.2+, Entra ID authentication |
