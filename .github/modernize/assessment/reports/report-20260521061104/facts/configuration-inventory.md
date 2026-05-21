# Configuration & Externalized Settings Inventory

The application uses a small set of local configuration sources: Spring property files, Docker Compose service definitions, Docker image settings, and Oracle initialization scripts. Configuration is straightforward, but secrets are stored inline in repository-managed files rather than external secret stores.

## Configuration Sources

| Source | Type | Path/Location | Notes |
|---|---|---|---|
| Spring application properties | Runtime config | `src/main/resources/application.properties` | Default server, datasource, JPA, upload, and logging settings |
| Spring profile properties | Runtime config | `src/main/resources/application-docker.properties` | Docker-specific Oracle connection and logging overrides |
| Docker Compose | Container orchestration config | `docker-compose.yml` | Defines web and Oracle services, environment variables, networking, and startup order |
| Dockerfile | Image/runtime config | `Dockerfile` | Defines build image, runtime image, JVM options, and exposed port |
| Maven build file | Build config | `pom.xml` | Declares framework versions and dependencies |
| Oracle init SQL | Database bootstrap config | `oracle-init/*.sql` | Creates database user, verifies privileges, and supports health checks |
| Test annotation config | Test runtime signal | `src/test/java/com/photoalbum/PhotoAlbumApplicationTests.java` | Activates the `test` Spring profile during context-load testing |

## Build Profiles

| Profile | Activation | Purpose | Key Dependencies/Plugins |
|---|---|---|---|
| Default Maven build | Automatic | Standard packaging of the Spring Boot jar | `spring-boot-maven-plugin`; no explicit Maven `<profiles>` detected |

## Runtime Profiles

| Profile | Activation Method | Config Files | Key Overrides |
|---|---|---|---|
| `default` | Automatic when no profile is set | `application.properties` | Oracle `FREEPDB1` JDBC URL, debug logging for app and Spring Web, upload limits |
| `docker` | `SPRING_PROFILES_ACTIVE=docker` in Docker Compose | `application.properties`, `application-docker.properties` | Oracle XE JDBC URL, lower web logging verbosity, container-oriented datasource host |
| `test` | `@ActiveProfiles("test")` on test class | Base properties plus Spring Boot test defaults | Uses test-scoped H2 dependency; no dedicated `application-test.properties` file detected |

## Properties Inventory

### photoalbum-java-app

| Property Key | Default | Profiles | Source |
|---|---|---|---|
| `server.port` | `8080` | default, docker | Spring properties files |
| `server.servlet.encoding.charset` | `UTF-8` | default, docker | Spring properties files |
| `server.servlet.encoding.enabled` | `true` | default, docker | Spring properties files |
| `server.servlet.encoding.force` | `true` | default, docker | Spring properties files |
| `spring.datasource.url` | Oracle JDBC URL | default, docker | Spring properties files |
| `spring.datasource.username` | `photoalbum` | default, docker | Spring properties files |
| `spring.datasource.password` | `[MASKED]` | default, docker | Spring properties files |
| `spring.datasource.driver-class-name` | `oracle.jdbc.OracleDriver` | default, docker | Spring properties files |
| `spring.jpa.database-platform` | `org.hibernate.dialect.OracleDialect` | default, docker | Spring properties files |
| `spring.jpa.hibernate.ddl-auto` | `create` | default, docker | Spring properties files |
| `spring.jpa.show-sql` | `true` | default, docker | Spring properties files |
| `spring.jpa.properties.hibernate.format_sql` | `true` | default, docker | Spring properties files |
| `spring.servlet.multipart.max-file-size` | `10MB` | default, docker | Spring properties files |
| `spring.servlet.multipart.max-request-size` | `50MB` | default, docker | Spring properties files |
| `app.file-upload.max-file-size-bytes` | `10485760` | default, docker | Spring properties files |
| `app.file-upload.allowed-mime-types` | `image/jpeg,image/png,image/gif,image/webp` | default, docker | Spring properties files |
| `app.file-upload.max-files-per-upload` | `10` | default, docker | Spring properties files |
| `logging.level.com.photoalbum` | `DEBUG` or `INFO` | default, docker | Spring properties files |
| `logging.level.org.springframework.web` | `DEBUG` or `WARN` | default, docker | Spring properties files |
| `logging.level.org.hibernate.SQL` | `DEBUG` | docker only | `application-docker.properties` |

### docker-compose service environment overrides

| Property Key | Default | Profiles | Source |
|---|---|---|---|
| `SPRING_PROFILES_ACTIVE` | `docker` | docker | `docker-compose.yml` |
| `SPRING_DATASOURCE_URL` | Oracle JDBC URL | docker | `docker-compose.yml` |
| `SPRING_DATASOURCE_USERNAME` | `photoalbum` | docker | `docker-compose.yml` |
| `SPRING_DATASOURCE_PASSWORD` | `[MASKED]` | docker | `docker-compose.yml` |
| `ORACLE_PASSWORD` | `[MASKED]` | docker | `docker-compose.yml` |
| `APP_USER` | `photoalbum` | docker | `docker-compose.yml` |
| `APP_USER_PASSWORD` | `[MASKED]` | docker | `docker-compose.yml` |

## Startup Parameters & Resource Requirements

| Service | JVM/Runtime Options | Memory | Instance Count |
|---|---|---|---:|
| `photoalbum-java-app` | `JAVA_OPTS="-Xmx512m -Xms256m"`; exposes port 8080 | 256 MB initial heap, 512 MB max heap | 1 container in Compose |
| `oracle-db` | No JVM options; Oracle container health check script | No explicit memory limit configured | 1 container in Compose |

## Startup Dependency Chain

1. `oracle-db` starts first and initializes the database user via scripts mounted from `oracle-init/`.
2. Docker Compose waits for the Oracle container health check (`healthcheck.sh`) to report healthy.
3. `photoalbum-java-app` starts only after `oracle-db` is healthy because of `depends_on.condition: service_healthy`.
4. The Spring Boot application then connects to Oracle using the active datasource settings and creates the schema on startup.

## Secrets & Sensitive Configuration

| Secret Reference | Type | Storage (masked) |
|---|---|---|
| `spring.datasource.password` | Database password | Inline Spring properties value masked in report |
| `SPRING_DATASOURCE_PASSWORD` | Database password | Docker Compose environment variable masked in report |
| `ORACLE_PASSWORD` | Oracle system/admin password | Docker Compose environment variable masked in report |
| `APP_USER_PASSWORD` | Oracle application user password | Docker Compose environment variable masked in report |

### Secrets Provisioning Workflow

Secrets are provisioned locally and statically. Source values are checked into repository-managed Spring properties and Docker Compose environment variables, then injected directly into the application container and Oracle container at startup. No managed identity, external vault, RBAC-governed secret store, or deployment-time secret binding workflow was detected.

## Feature Flags

| Flag Name | Default | Controlled By |
|---|---|---|
| None detected | N/A | No `@ConditionalOnProperty`, feature flag framework, or toggle file detected |

## Framework & Runtime Versions

| Component | Version | Source |
|---|---|---|
| Spring Boot | `2.7.18` | `pom.xml` parent POM |
| Java target | `1.8` | `pom.xml` properties |
| Maven build image | `3.9.6-eclipse-temurin-8` | `Dockerfile` |
| Java runtime image | `eclipse-temurin:8-jre` | `Dockerfile` |
| Bootstrap | `5.3.0` | CDN reference in Thymeleaf templates |
| Oracle JDBC | `ojdbc8` (managed) | `pom.xml` dependency |
| Oracle database container | `gvenzl/oracle-free:latest` | `docker-compose.yml` |
| Spring Data JPA / Hibernate | Spring Boot managed | `pom.xml` dependency set |
