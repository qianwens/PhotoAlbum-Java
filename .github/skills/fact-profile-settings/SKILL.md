---
name: fact-profile-settings
description: Analyze environment-specific profiles and configuration
---

# Profile Settings Analysis

## Purpose
Identify how the application manages environment-specific configurations (Development, Test, Staging, Production) through profiles, property files, or environment-based settings. This helps understand configuration management complexity and deployment requirements.

## Target Files/Locations
- **Spring profiles**: **/application-{profile}.{properties,yml}, **/application.{properties,yml}
- **Maven profiles**: **/pom.xml (`<profiles>` section)
- **Gradle profiles**: **/build.gradle, **/build.gradle.kts (buildTypes, productFlavors)
- **Environment configs**: **/config/**, **/environments/**, **/profiles/
- **Java properties**: **/{env}/*.properties, **/*-{env}.properties
- **.NET configs**: **/appsettings.{Environment}.json, **/web.{config}.config
- **Docker/K8s**: **/docker-compose.{env}.yml, **/k8s/**/*-{env}.yaml
- **CI/CD**: **/.github/workflows/, **/.gitlab-ci.yml, **/Jenkinsfile

## Example Patterns to Search
- **Spring profiles**: `spring.profiles.active`, `@Profile("dev")`, `application-dev.properties`
- **Maven profiles**: `<profile><id>development</id>`, `<activeByDefault>`, `<activation>`
- **Environment variables**: `${ENV:prod}`, `#{environment}`, `process.env.NODE_ENV`
- **Profile-specific beans**: `@Profile("production")`, `@ConditionalOnProfile`
- **Config file names**: dev, test, staging, uat, prod, production, development

## Analysis Steps

### 1. Search for Spring Profile Configuration Files
```
Use Glob to find Spring profile-specific configs:
- **/application-dev.{properties,yml,yaml}
- **/application-test.{properties,yml,yaml}
- **/application-staging.{properties,yml,yaml}
- **/application-prod.{properties,yml,yaml}
- **/application-production.{properties,yml,yaml}
- **/application-uat.{properties,yml,yaml}
- **/application-local.{properties,yml,yaml}

Use Read to examine application.properties/yml:
- Check for spring.profiles.active setting
- Look for profile-specific property groups (--- separator in YAML)
- Identify default profile configuration

Count and categorize profiles found
```

### 2. Search for @Profile Annotations in Java Code
```
Use Grep to find profile usage in code:
Pattern: "@Profile\\(|@ConditionalOnProfile|spring\\.profiles\\."
Files: **/*.java
Context: -B 1 -A 2

Analyze:
- Which beans/components are profile-specific
- Profile names used in annotations
- Conditional logic based on profiles
```

### 3. Analyze Maven Profile Configuration
```
Use Glob to find Maven build file:
- **/pom.xml

Use Read or Grep to search for:
- <profiles> section
- <profile><id> elements (dev, test, prod, etc.)
- <activeByDefault> settings
- <activation> conditions (property, JDK, OS)
- Profile-specific properties, dependencies, plugins

Example patterns to search:
<profile>
  <id>development</id>
  <activation>
    <activeByDefault>true</activeByDefault>
  </activation>
</profile>
```

### 4. Check Gradle Build Profiles
```
Use Glob to find Gradle files:
- **/build.gradle
- **/build.gradle.kts

Use Read to check for:
- buildTypes { debug, release }
- productFlavors { dev, staging, prod }
- Environment-specific configurations
- ext { profile = project.hasProperty('env') ? env : 'dev' }
```

### 5. Search for .NET Environment Configurations
```
Use Glob to find .NET configs:
- **/appsettings.Development.json
- **/appsettings.Staging.json
- **/appsettings.Production.json
- **/web.Development.config
- **/web.Release.config

Use Grep in .csproj files:
Pattern: "<Environments>|ASPNETCORE_ENVIRONMENT|IHostEnvironment"
```

### 6. Check for Environment-Specific Directories
```
Use Glob to find environment directories:
- **/config/dev/**
- **/config/prod/**
- **/environments/development/**
- **/profiles/**

Use Bash to list directory structure:
find . -type d -name "dev" -o -name "test" -o -name "prod" -o -name "staging" | head -20
```

### 7. Analyze Docker/K8s Environment Configurations
```
Use Glob to find container configs:
- **/docker-compose.dev.yml
- **/docker-compose.prod.yml
- **/k8s/dev/**/*.yaml
- **/k8s/production/**/*.yaml
- **/Dockerfile.dev, **/Dockerfile.prod

Use Grep to find environment variables:
Pattern: "ENV|ENVIRONMENT|PROFILE"
Files: **/Dockerfile, **/docker-compose*.yml
```

### 8. Search for CI/CD Environment Configurations
```
Use Glob to find CI/CD files:
- **/.github/workflows/**/*.yml
- **/.gitlab-ci.yml
- **/Jenkinsfile
- **/azure-pipelines.yml

Use Read to check for:
- Environment-based job definitions
- Deployment stages (dev, test, prod)
- Environment-specific variables
```

### 9. Count and Categorize Profiles
```
Aggregate all findings:
- List all profile names found
- Count config files per profile
- Identify primary profiles (dev, test, prod)
- Note any custom or unusual profile names
- Check for profile activation logic
```

## Confidence Determination

### High Confidence Criteria
Clear and comprehensive profile configuration:
- ✅ Multiple profile-specific config files found (dev, test, prod)
- ✅ Profile activation mechanism clearly defined
- ✅ Profile-specific beans or components in code
- ✅ Build tool profiles configured (Maven/Gradle)
- ✅ Consistent naming across different config types
- ✅ Environment-specific properties well documented

**Examples**:
- "Application uses 4 Spring profiles (dev, test, staging, prod) with separate application-{profile}.yml files and @Profile annotations in 12 configuration classes"
- "Maven build configured with 3 profiles (development, testing, production) using different database connections and feature flags per environment"
- ".NET application with appsettings.{Environment}.json for Development, Staging, and Production with ASPNETCORE_ENVIRONMENT detection"

### Medium Confidence Criteria
Partial profile configuration or unclear structure:
- ⚠️ Some profile files found but incomplete coverage
- ⚠️ Profiles defined but no clear activation mechanism
- ⚠️ Mixed approaches (some Spring, some environment variables)
- ⚠️ Profile names inconsistent across config types
- ⚠️ Only build profiles without runtime profiles (or vice versa)

**Examples**:
- "Spring profiles for dev and prod found, but test/staging configs missing"
- "Maven profiles defined but no corresponding Spring profile configs"
- "Environment-based configuration exists but profile names vary (dev vs development, prod vs production)"

### Low Confidence Criteria
Weak or minimal profile evidence:
- ⚠️ Only default configuration, no environment variants
- ⚠️ Profile files exist but appear unused or outdated
- ⚠️ Single-environment application (dev only)
- ⚠️ Hardcoded values instead of profile-based configs
- ⚠️ Profile references in comments but no implementation

**Examples**:
- "Only application.properties found, no profile-specific configs"
- "Profile files exist but timestamps suggest not used in 2+ years"
- "Comments mention dev/prod configs but actual implementation uses hardcoded values"

### Not Applicable Criteria
When profile analysis doesn't apply:
- ❌ Simple utility/library with no environment differences
- ❌ Single-purpose tool with no configuration needs
- ❌ Prototype or demo application
- ❌ Different platform with different config approach
- ❌ Configuration managed entirely external (ConfigMap, external config server)

**Examples**:
- "Command-line utility with no environment-specific behavior"
- "Demo application with hardcoded sample data"
- "Library project with no deployment configuration"

## Output Format

**CRITICAL**: Use the `write_assessment_result` tool (not just output JSON text).

```json
{
  "input_name": "Profile Settings",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Clear 1-2 sentence summary of profile configuration}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Number and names of profiles identified}",
      "{Profile activation mechanism}",
      "{Config files per profile}",
      "{Code using profile-specific logic}",
      "{Build tool profile configuration}"
    ],
    "values": [
      "{Profile names: dev, test, staging, prod, etc.}",
      "{Config file types: properties, yml, json}",
      "{Activation method: spring.profiles.active, Maven, env vars}",
      "{Number of profile-specific files}",
      "{Profile-annotated components count}"
    ]
  },
  "execution_time_seconds": {elapsed_time},
  "timestamp": "{ISO 8601 timestamp}"
}
```

**Finding Examples**:
- ✅ Good: "Application uses comprehensive Spring profile system with 4 environments (dev, test, staging, prod) managed through application-{profile}.yml files and 15 @Profile-annotated configuration classes"
- ✅ Good: ".NET Core application with environment-based configuration using appsettings.{Environment}.json for Development, Staging, and Production environments activated via ASPNETCORE_ENVIRONMENT"
- ✅ Good: "Maven multi-profile build with 3 profiles (development, testing, production) controlling database connections, logging levels, and feature toggles"
- ✅ Good: "No environment profiles detected - single configuration approach suitable for utility application"
- ❌ Bad: "Profiles exist"
- ❌ Bad: "Environment configuration found"

**Evidence Examples**:
- ✅ Good: "application-dev.yml, application-test.yml, application-staging.yml, application-prod.yml in src/main/resources/"
- ✅ Good: "15 configuration classes with @Profile annotations: @Profile('dev') in DevDatabaseConfig.java, @Profile('prod') in ProdSecurityConfig.java"
- ✅ Good: "Maven pom.xml defines 3 profiles with <id>development</id>, <id>testing</id>, <id>production</id> at lines 120-185"
- ✅ Good: "spring.profiles.active=dev in application.properties, overridable via SPRING_PROFILES_ACTIVE environment variable"
- ❌ Bad: "Configuration files found"
- ❌ Bad: "Profiles detected in code"

## Error Handling

### 1. No Profiles Found
- Verify it's not a single-environment application by design
- Check for alternative configuration mechanisms (external config, env vars only)
- Report finding: "No profile-based configuration detected - single configuration model"
- Set confidence to high if thorough search confirms absence

### 2. Inconsistent Profile Names
- Report all variations found (dev vs development, prod vs production)
- Note potential misconfiguration risks
- Set confidence to medium
- Recommend standardization in evidence notes

### 3. Partial Profile Implementation
- List which profiles are complete vs incomplete
- Note missing files (e.g., dev and prod exist but no test)
- Set confidence to medium with caveats

### 4. Mixed Configuration Approaches
- Document each approach found (Spring profiles, Maven profiles, Docker configs)
- Clarify how they interact or if they're independent
- This is common and valid - report comprehensively

### 5. Tool Failures
- If Glob returns too many results, refine patterns
- If Read fails on large files, use Grep for specific patterns
- After 3 retries, report partial results with notes

## Example Complete Analysis

**Scenario**: Spring Boot microservice with comprehensive profile setup

**Steps Executed**:
1. Glob for Spring configs: Found application-{dev,test,staging,prod}.yml (4 files)
2. Read application.yml: Found spring.profiles.active: dev
3. Grep for @Profile: Found 18 matches in 15 configuration classes
4. Read pom.xml: No Maven profiles (uses Spring profiles only)
5. Checked Docker: Found docker-compose.dev.yml and docker-compose.prod.yml
6. Glob for K8s: Found k8s/dev/ and k8s/prod/ directories with manifests

**Result**:
```json
{
  "input_name": "Profile Settings",
  "analysis_method": "LLM",
  "status": "success",
  "result": {
    "finding": "Application implements comprehensive 4-environment profile system (dev, test, staging, prod) using Spring profiles with separate YAML configs, 15 profile-annotated configuration classes, and environment-specific Docker/Kubernetes manifests",
    "confidence": "high",
    "evidence": [
      "4 Spring profile configs: application-dev.yml, application-test.yml, application-staging.yml, application-prod.yml in src/main/resources/",
      "application.yml sets spring.profiles.active: dev as default, overridable via SPRING_PROFILES_ACTIVE env var",
      "15 configuration classes use @Profile annotations: DevDatabaseConfig, ProdSecurityConfig, TestEmailConfig, etc.",
      "docker-compose.dev.yml and docker-compose.prod.yml set different SPRING_PROFILES_ACTIVE values",
      "Kubernetes manifests in k8s/dev/ and k8s/prod/ directories with environment-specific ConfigMaps",
      "Profile-specific settings: database URLs, Redis hosts, feature flags, logging levels"
    ],
    "values": [
      "4 environments: dev, test, staging, prod",
      "Spring profile activation via application.yml and environment variables",
      "15 @Profile-annotated configuration classes",
      "4 profile-specific YAML files (150-200 lines each)",
      "Docker Compose configs for dev and prod",
      "Kubernetes ConfigMaps per environment"
    ]
  },
  "execution_time_seconds": 35.2,
  "timestamp": "2026-02-28T10:26:14Z"
}
```
