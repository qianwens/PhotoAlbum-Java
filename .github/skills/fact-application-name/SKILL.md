---
name: fact-application-name
description: Identify application name/identifier from configuration files
---

# Application Name Analysis

## Purpose
Extract the application name or identifier from project files, configuration, and build descriptors.

## Target Files/Locations
- **/pom.xml (<name>, <artifactId>)
- **/*.csproj (<AssemblyName>, <RootNamespace>)
- **/package.json (name field)
- **/build.gradle (rootProject.name)
- **/application.{properties,yml} (spring.application.name)
- **/README.md (title or project name)

## Example Patterns
- `<name>CustomerPortal</name>` (Maven)
- `"name": "order-processor"` (Node.js)
- `spring.application.name=payment-service`
- `<AssemblyName>InventoryAPI</AssemblyName>` (.NET)

## Analysis Steps

### 1. Check Build File Names
```
Maven (pom.xml):
Use Grep: "<name>|<artifactId>"
Extract: <name>ProjectName</name>

Gradle (build.gradle):
Use Grep: "rootProject\\.name"
Extract: rootProject.name = 'project-name'

Node.js (package.json):
Use Read and parse JSON: { "name": "app-name" }

.NET (*.csproj):
Use Grep: "<AssemblyName>|<RootNamespace>"
```

### 2. Check Application Configuration
```
Use Grep: "spring\\.application\\.name|app\\.name|application\\.name"
Files: **/application.{properties,yml}, **/appsettings.json
Context: -B 1 -A 1
```

### 3. Check README
```
Use Read: **/README.md (first 50 lines)
Look for:
- # Title
- Project name in first paragraph
- Badge labels
```

### 4. Check Container Names
```
Use Grep: "container_name:"
Files: **/docker-compose*.yml
Application name often in container name
```

## Confidence Determination

### High Confidence
- ✅ Name consistently appears across multiple files
- ✅ Clear identifier in build/config files
- **Example**: "Application name: CustomerPortal from pom.xml, spring.application.name, and README"

### Medium Confidence
- ⚠️ Name in build file but not elsewhere
- ⚠️ Generic name (app, service, api)
- **Example**: "Project name: my-app (generic name from package.json only)"

### Low Confidence
- ⚠️ No clear application name
- ⚠️ Names inconsistent across files
- **Example**: "Multiple names found, primary name unclear"

### Not Applicable
- ❌ Multi-module project with multiple applications
- **Example**: "Monorepo with 10 microservices, no single application name"

## Output Format

```json
{
  "input_name": "Application Name",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Application name}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Source file and field}",
      "{Consistency across files}",
      "{Alternative names found}"
    ],
    "values": [
      "{Primary name}",
      "{Alternative names/identifiers}",
      "{Artifact IDs or namespaces}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
