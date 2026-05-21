# Targets — Default Modernization Rulebook

Approved target technologies for .NET and Java modernization. Defines *what is approved* — not implementation steps (those belong in skills).

---

## Target Frameworks

| Language | Target Version | EOL Versions (must upgrade) |
|---|---|---|
| Java | 21+ LTS, Spring Boot 3.x | Java 8 EOL; 11/17 supported but 21+ preferred |
| .NET | 8+ LTS | .NET Framework 4.x, .NET Core 3.1, .NET 6 end-of-support |

---

## Target Compute Services

| Workload Type | Target | Selection Rule |
|---|---|---|
| Containerized stateless apps / APIs | **Azure Container Apps** | Scale-to-zero, managed ingress, Dapr/KEDA; no full K8s control plane needed |
| Complex orchestration, multi-container | **Azure Kubernetes Service (AKS)** | Full K8s control plane, custom networking, service mesh, DaemonSets |
| Non-containerized web apps | **Azure App Service** | Platform-managed TLS, deployment slots, integrated auth; lowest migration friction |
| Apps with OS-level dependencies | **Azure App Service Managed Instance** | COM, registry, custom installers, RDP access via Bastion; lift-and-improve with OS control |

**Selection:** Evaluate workload characteristics against table → select matching target. No single universal default; target is determined by app profile.

---

## Target Data Services

Backing services for modernized applications — not standalone migration targets.

| Source | Target | When |
|---|---|---|
| SQL Server | **Azure SQL Database** | Default; Managed Instance only if instance-scoped features needed |
| PostgreSQL | **Azure Database for PostgreSQL Flexible Server** | Default for PostgreSQL |
| MySQL | **Azure Database for MySQL Flexible Server** | Default for MySQL |
| Oracle, other RDBMS | Evaluate case-by-case | Prefer Azure SQL or PostgreSQL |
| MongoDB, DynamoDB, document stores | **Azure Cosmos DB** | Multi-model NoSQL; select appropriate API |
| Memcached, self-hosted Redis, in-process caches | **Azure Cache for Redis** | Distributed caching and session state |
| File shares, NFS, local disk | **Azure Blob Storage** | Unstructured data; Hot/Cool/Archive tiers |
| SMB file shares | **Azure Files** | When SMB/NFS mount semantics required |

---

## Target Integration Services

Backing services — selected when the application's messaging/eventing/API layer migrates alongside the app.

| Source | Target | When |
|---|---|---|
| RabbitMQ, MSMQ, ActiveMQ, IBM MQ | **Azure Service Bus** | Reliable enterprise messaging (queues, topics, sessions, dead-letter) |
| Custom webhooks, polling | **Azure Event Grid** | Reactive event-driven, push delivery |
| Kafka, high-throughput streaming | **Azure Event Hubs** | High-throughput ingestion; Kafka protocol compatible |
| Custom reverse proxies, legacy gateways | **Azure API Management** | API facade, rate limiting, auth, developer portal |

---

## Target Libraries

Source → target mappings for .NET and Java task generation.

| Category | Source | Target |
|---|---|---|
| Azure SDK (.NET) | `Microsoft.Azure.*` (Track 1) | `Azure.*` (Track 2) |
| Azure SDK (Java) | `com.microsoft.azure:*` | `com.azure:*` |
| Logging (.NET) | log4net, NLog | OpenTelemetry + Azure Monitor |
| Logging (Java) | log4j 1.x, SLF4J + Logback | OpenTelemetry + Azure Monitor |
| Auth | Connection strings, hardcoded keys | `DefaultAzureCredential` (Managed Identity) |
| Config (.NET) | `web.config`, `app.config`, hardcoded | Azure App Configuration + Key Vault |
| Config (Java) | `application.properties`, hardcoded | Azure App Configuration + Key Vault |
| DI (.NET) | Autofac, Unity, Ninject | Built-in `Microsoft.Extensions.DependencyInjection` |
| HTTP (.NET) | Raw `HttpClient`, `WebClient`, `RestSharp` | `IHttpClientFactory` with resilience policies |
