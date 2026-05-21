# Configuration & Externalized Settings Inventory

PhotoAlbum-Java uses three Spring Boot property files (default, docker, test profiles) as its sole configuration source, with secrets supplied via plain-text properties and Docker environment variable overrides — no external config server or secret store is employed.

## Configuration Sources

| Source | Type | Path / Location | Notes |
|--------|------|----------------|-------|
| `application.properties` | Spring Boot default profile | `src/main/resources/application.properties` | Active in local development; connects to Oracle at `oracle-db:1521/FREEPDB1` |
| `application-docker.properties` | Spring Boot `docker` profile | `src/main/resources/application-docker.properties` | Activated via `SPRING_PROFILES_ACTIVE=docker` in Docker Compose; overrides JDBC URL to `oracle-db:1521:XE` |
| `application-test.properties` | Spring Boot `test` profile | `src/test/resources/application-test.properties` | Active during `mvn test`; substitutes Oracle with H2 in-memory DB |
| `docker-compose.yml` | Docker Compose environment | `docker-compose.yml` (root) | Injects `SPRING_PROFILES_ACTIVE`, `SPRING_DATASOURCE_URL/USERNAME/PASSWORD` into the app container; sets Oracle init-db environment variables |
| `oracle-init/01-create-user.sql` | Oracle init script | `oracle-init/01-create-user.sql` | Executed automatically by the Oracle Free container on first start; creates `photoalbum` user with DBA privileges |
| `oracle-init/02-verify-user.sql` | Oracle init script | `oracle-init/02-verify-user.sql` | Post-creation verification query |
| `Dockerfile` | Container build config | `Dockerfile` (root) | Multi-stage build; sets default `JAVA_OPTS=-Xmx512m -Xms256m` |

No Spring Cloud Config server, Kubernetes ConfigMaps, HashiCorp Vault, Azure Key Vault, or AWS Secrets Manager references are present. No `bootstrap.properties` or `bootstrap.yml` files exist.

## Build Profiles

| Profile | Activation | Purpose | Key Dependencies / Plugins |
|---------|-----------|---------|---------------------------|
| (default) | Automatic — no `-P` flag required | Standard local build with all dependencies; runs tests against H2 | `spring-boot-maven-plugin` for executable JAR; `spring-boot-starter-test` + H2 in test scope |
| Docker multi-stage build | Triggered by `docker build` / `docker-compose up --build` | Compiles and packages in `maven:3.9.6-eclipse-temurin-8`; copies JAR to `eclipse-temurin:8-jre` runtime image | `mvn clean package -DskipTests` (skips tests inside Docker build); no additional Maven profiles declared in `pom.xml` |

No explicit Maven `<profiles>` blocks are declared in `pom.xml`. The only build variation is between a local Maven build (runs tests) and the Docker-contained build (skips tests).

## Runtime Profiles

| Profile | Activation Method | Config Files | Key Overrides vs Default |
|---------|-----------------|-------------|-------------------------|
| (default) | None — active when no profile is set | `application.properties` | Baseline — Oracle at `oracle-db:1521/FREEPDB1`, log level DEBUG for app code |
| `docker` | `SPRING_PROFILES_ACTIVE=docker` (set in `docker-compose.yml`) | `application.properties` + `application-docker.properties` | JDBC URL changed to `oracle-db:1521:XE`; app log level reduced to INFO; Hibernate SQL log to DEBUG |
| `test` | Applied automatically by `spring-boot-starter-test` via `application-test.properties` in test classpath | `application-test.properties` | Oracle replaced with `jdbc:h2:mem:testdb`; `ddl-auto=create-drop`; SQL logging disabled; upload path set to `target/test-uploads` |

Multiple active profiles are not combined in any declared configuration. The `docker` profile fully composes with the base `application.properties` (Spring Boot merges them).

## Properties Inventory

### photoalbum-java-app — Server & Encoding

| Property Key | Default | docker profile | test profile | Source |
|-------------|---------|---------------|-------------|--------|
| `server.port` | `8080` | `8080` | — | `application.properties` |
| `server.servlet.encoding.charset` | `UTF-8` | `UTF-8` | — | `application.properties` |
| `server.servlet.encoding.enabled` | `true` | `true` | — | `application.properties` |
| `server.servlet.encoding.force` | `true` | `true` | — | `application.properties` |

### photoalbum-java-app — DataSource

| Property Key | Default | docker profile | test profile | Source |
|-------------|---------|---------------|-------------|--------|
| `spring.datasource.url` | `jdbc:oracle:thin:@oracle-db:1521/FREEPDB1` | `jdbc:oracle:thin:@oracle-db:1521:XE` | `jdbc:h2:mem:testdb` | Profile files |
| `spring.datasource.username` | `photoalbum` | `photoalbum` | `sa` | Profile files |
| `spring.datasource.password` | `photoalbum` [SENSITIVE] | `photoalbum` [SENSITIVE] | _(empty)_ | Profile files |
| `spring.datasource.driver-class-name` | `oracle.jdbc.OracleDriver` | `oracle.jdbc.OracleDriver` | `org.h2.Driver` | Profile files |

### photoalbum-java-app — JPA / Hibernate

| Property Key | Default | docker profile | test profile | Source |
|-------------|---------|---------------|-------------|--------|
| `spring.jpa.database-platform` | `org.hibernate.dialect.OracleDialect` | `org.hibernate.dialect.OracleDialect` | `org.hibernate.dialect.H2Dialect` | Profile files |
| `spring.jpa.hibernate.ddl-auto` | `create` | `create` | `create-drop` | Profile files |
| `spring.jpa.show-sql` | `true` | `true` | `false` | Profile files |
| `spring.jpa.properties.hibernate.format_sql` | `true` | `true` | — | Profile files |

### photoalbum-java-app — File Upload

| Property Key | Default | docker profile | test profile | Source |
|-------------|---------|---------------|-------------|--------|
| `spring.servlet.multipart.max-file-size` | `10MB` | `10MB` | — | `application.properties` |
| `spring.servlet.multipart.max-request-size` | `50MB` | `50MB` | — | `application.properties` |
| `app.file-upload.max-file-size-bytes` | `10485760` | `10485760` | `10485760` | Profile files |
| `app.file-upload.allowed-mime-types` | `image/jpeg,image/png,image/gif,image/webp` | same | same | Profile files |
| `app.file-upload.max-files-per-upload` | `10` | `10` | `10` | Profile files |
| `app.file-upload.upload-path` | — | — | `target/test-uploads` | `application-test.properties` |

### photoalbum-java-app — Logging

| Property Key | Default | docker profile | test profile | Source |
|-------------|---------|---------------|-------------|--------|
| `logging.level.com.photoalbum` | `DEBUG` | `INFO` | `DEBUG` | Profile files |
| `logging.level.org.springframework.web` | `DEBUG` | `WARN` | — | Profile files |
| `logging.level.org.hibernate.SQL` | — | `DEBUG` | — | `application-docker.properties` |

## Startup Parameters & Resource Requirements

| Service | JVM / Runtime Options | Memory | CPU | Instance Count |
|---------|----------------------|--------|-----|---------------|
| photoalbum-java-app (Docker) | `JAVA_OPTS=-Xmx512m -Xms256m` (set in Dockerfile `ENV`) | No `mem_limit` set in Compose | Not specified | 1 (no scaling config) |
| photoalbum-java-app (local Maven) | JVM default (no explicit heap flags) | Host JVM defaults | Not specified | 1 |
| oracle-db | Oracle Free container defaults | No `mem_limit` set in Compose | Not specified | 1 |

The `JAVA_OPTS` environment variable is read by the `ENTRYPOINT` script (`sh -c "java $JAVA_OPTS -jar app.jar"`). It can be overridden at `docker run` time or via `docker-compose.yml` `environment` section. No `-Dspring.profiles.active` JVM system property is used; profile activation is exclusively via `SPRING_PROFILES_ACTIVE` environment variable.

## Startup Dependency Chain

```
oracle-db  →  (Docker healthcheck: healthcheck.sh, interval 30s, timeout 10s, retries 15, start_period 180s)
           ↓
photoalbum-java-app  →  depends_on: oracle-db (condition: service_healthy)
                        restart policy: on-failure
```

1. **`oracle-db`** starts first. The Docker Compose health check runs `healthcheck.sh` inside the Oracle container every 30 seconds with a 180-second start period and up to 15 retries (~7.5 minutes total patience).
2. **`photoalbum-java-app`** only starts after `oracle-db` reports healthy. No application-level readiness probe (Spring Boot Actuator is not on the classpath). If Oracle is unavailable after the container starts, the Spring application context will fail to initialize (Hibernate `ddl-auto=create` requires a live connection at startup) and Docker Compose will restart the container per `restart: on-failure`.

There is no config-server, discovery-server, or API gateway in the startup chain.

## Secrets & Sensitive Configuration

| Secret Reference | Type | Profile | Storage |
|----------------|------|---------|---------|
| `spring.datasource.password` | Oracle DB password | default, docker | Plain-text in `application.properties` / `application-docker.properties` — value: [MASKED] |
| `SPRING_DATASOURCE_PASSWORD` | Oracle DB password (env var override) | docker (Compose) | Plain-text in `docker-compose.yml` — value: [MASKED] |
| `ORACLE_PASSWORD` | Oracle root/sys password | docker (Compose, oracle-db service) | Plain-text in `docker-compose.yml` — value: [MASKED] |
| `APP_USER_PASSWORD` | Oracle app-user password | docker (Compose, oracle-db service) | Plain-text in `docker-compose.yml` — value: [MASKED] |

### Secrets Provisioning Workflow

All secrets are stored as plain-text values in source-controlled configuration files (`application.properties`, `docker-compose.yml`). There is no secrets management system in use:

- **No external secret store**: No HashiCorp Vault, Azure Key Vault, AWS Secrets Manager, or Kubernetes Secrets are referenced.
- **No encryption**: No Jasypt, DPAPI, or sealed-secret encryption of property values.
- **Credential flow**: Oracle credentials are hard-coded in `application.properties` (default profile) and additionally injected as `SPRING_DATASOURCE_*` environment variables in `docker-compose.yml`. The values in both locations are identical plain-text strings.
- **Risk**: Committing database passwords to source control is a critical security issue. Any developer or CI system with repository read access can obtain the database credentials.

**Recommended remediation**: Externalize secrets to a vault (e.g., Azure Key Vault with managed identity, or GitHub Actions secrets injected at deploy time) and remove credential values from all checked-in files.

## Feature Flags

No feature flag framework is present. No `@ConditionalOnProperty`, `@ConditionalOnExpression`, LaunchDarkly, Unleash, or custom toggle mechanism is used. The only conditional behaviour is the standard Spring Boot profile activation that selects the appropriate `application-{profile}.properties` file.

| Flag Name | Default | Controlled By |
|-----------|---------|--------------|
| None detected | — | — |

## Framework & Runtime Versions

| Component | Version | Source |
|-----------|---------|--------|
| Java (compile target) | 8 (1.8) | `pom.xml` — `maven.compiler.source/target` |
| Java (Docker build) | 8 (`eclipse-temurin:8`) | `Dockerfile` — `FROM maven:3.9.6-eclipse-temurin-8` / `FROM eclipse-temurin:8-jre` |
| Spring Boot | 2.7.18 | `pom.xml` — parent BOM |
| Spring MVC | 5.3.x (managed by Spring Boot 2.7.18 BOM) | Transitive via `spring-boot-starter-web` |
| Hibernate | 5.6.x (managed by Spring Boot 2.7.18 BOM) | Transitive via `spring-boot-starter-data-jpa` |
| Thymeleaf | 3.0.x (managed by Spring Boot 2.7.18 BOM) | Transitive via `spring-boot-starter-thymeleaf` |
| Hibernate Validator | 6.x (managed by Spring Boot 2.7.18 BOM) | Transitive via `spring-boot-starter-validation` |
| Jackson | 2.14.x (managed by Spring Boot 2.7.18 BOM) | Transitive via `spring-boot-starter-json` |
| Oracle JDBC (ojdbc8) | Managed by Spring Boot BOM (Oracle 21c driver) | `pom.xml` — `com.oracle.database.jdbc:ojdbc8` |
| Commons IO | 2.11.0 | `pom.xml` — explicit version |
| H2 Database | 2.x (managed by Spring Boot 2.7.18 BOM) | `pom.xml` — test scope |
| Maven | 3.9.6 (Docker build stage) | `Dockerfile` — `FROM maven:3.9.6-eclipse-temurin-8` |
| Maven (local) | ≥ 3.x (not pinned) | System-installed; used for `mvn test` |
| Docker base image (build) | `maven:3.9.6-eclipse-temurin-8` | `Dockerfile` |
| Docker base image (runtime) | `eclipse-temurin:8-jre` | `Dockerfile` |
| Oracle Database | Free 23ai (`gvenzl/oracle-free:latest`) | `docker-compose.yml` |
