---
name: fact-application-type
description: Determine the type of application (Web App, API, Service, etc.)
---

# Application Type Analysis

## Purpose
Identify the type of application based on code structure and dependencies.

## Target Files/Locations
- **/pom.xml, **/build.gradle, **/build.gradle.kts (Java)
- **/*.csproj (C#/.NET)
- **/package.json (Node.js)
- **/requirements.txt, **/Pipfile, **/pyproject.toml (Python)
- **/*.java, **/*.cs, **/*.js, **/*.ts, **/*.py (source code)

## Analysis Steps

### 1. Check Java Web Frameworks
```
Use Grep: "spring-boot-starter-web|@RestController|@RequestMapping|spring-boot-starter-webflux"
Files: **/pom.xml, **/build.gradle, **/*.java

Map findings:
- spring-boot-starter-web / @RestController → REST API
- spring-boot-starter-webflux → REST API (Reactive)
```

### 2. Check Java gRPC
```
Use Grep: "grpc|io\\.grpc"
Files: **/pom.xml, **/build.gradle, **/*.proto

If found → gRPC Service
```

### 3. Check .NET Project Type
```
Use Grep: "Microsoft\\.AspNetCore|Microsoft\\.NET\\.Sdk\\.Web"
Files: **/*.csproj

Map findings:
- Microsoft.NET.Sdk.Web / Microsoft.AspNetCore → Web App / REST API
```

### 4. Check .NET gRPC
```
Use Grep: "Grpc\\.AspNetCore"
Files: **/*.csproj

If found → gRPC Service
```

### 5. Check .NET Background Service
```
Use Grep: "BackgroundService|Microsoft\\.Extensions\\.Hosting"
Files: **/*.csproj, **/*.cs

If found (and no web SDK) → Background Service
```

### 6. Check Node.js Frameworks
```
Use Grep: "express|fastify|koa|@nestjs|@grpc/grpc-js"
Files: **/package.json

Map findings:
- express / fastify / koa / @nestjs → REST API / Web App
- @grpc/grpc-js → gRPC Service
```

### 7. Check Python Frameworks
```
Use Grep: "flask|django|fastapi|tornado|grpcio"
Files: **/requirements.txt, **/Pipfile, **/pyproject.toml

Map findings:
- flask / django / fastapi / tornado → REST API / Web App
- grpcio → gRPC Service
```

### 8. Check for Batch/Job Indicators
```
Use Glob: **/cron*, **/*job*, **/*batch*, **/*scheduler*
Use Grep: "@Scheduled|CronJob|BackgroundJob"
Files: **/*.{java,cs,py}

If no web framework found but batch patterns detected → Batch Job
```

## Confidence Determination

### High Confidence
- ✅ Web framework dependency clearly identified
- ✅ REST/gRPC annotations in source code
- **Example**: "REST API: Spring Boot with @RestController annotations"

### Medium Confidence
- ⚠️ Framework found but type ambiguous
- **Example**: "ASP.NET Core project, could be Web App or API"

### Low Confidence
- ⚠️ No clear framework indicators
- **Example**: "Unable to determine application type from available files"

### Not Applicable
- ❌ Library project with no entry point
- **Example**: "Library/SDK project, no application type"

## Output Format

```json
{
  "input_name": "Application Type",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Application type}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Framework dependencies}",
      "{Annotations/decorators found}",
      "{Project structure indicators}"
    ],
    "values": [
      "{Type: REST API, Web App, gRPC Service, Background Service, Batch Job, etc.}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
