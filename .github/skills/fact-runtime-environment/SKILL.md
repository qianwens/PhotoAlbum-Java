---
name: fact-runtime-environment
description: Identify application runtime (Node.js, Python, Java, Go, .NET) in container
---

# Runtime Environment Analysis

## Purpose
Detect the application runtime/platform used in containerized applications (Node.js, Python, Java, Go, .NET, Ruby, PHP, etc.).

## Target Files/Locations
- **/Dockerfile, **/Containerfile (FROM base image)
- **/package.json, **/package-lock.json (Node.js)
- **/pom.xml, **/build.gradle (Java)
- **/*.csproj, **/*.sln (.NET)
- **/requirements.txt, **/Pipfile, **/pyproject.toml (Python)
- **/go.mod (Go)
- **/Gemfile (Ruby)
- **/composer.json (PHP)

## Example Patterns
- `FROM node:16`, `FROM python:3.9`, `FROM openjdk:11`, `FROM mcr.microsoft.com/dotnet/runtime:6.0`
- `RUN npm install`, `RUN pip install`, `RUN go build`, `RUN dotnet publish`

## Analysis Steps

### 1. Analyze Base Image
```
Use Grep: "FROM\\s+(node|python|openjdk|golang|mcr.microsoft.com/dotnet|ruby|php)"
Files: **/Dockerfile
Extract runtime from base image name
```

### 2. Check Build/Install Commands
```
Use Grep: "npm|pip|maven|gradle|dotnet|go build|bundle|composer"
Files: **/Dockerfile
Context: -B 1 -A 2
```

### 3. Identify Dependency Files
```
Use Glob to find:
- package.json, package-lock.json (Node.js)
- requirements.txt, Pipfile (Python)
- pom.xml, build.gradle (Java)
- *.csproj, *.sln (.NET)
- go.mod, go.sum (Go)
- Gemfile (Ruby)
- composer.json (PHP)
```

### 4. Check Version from Base Image
```
Parse FROM instruction:
- node:16-alpine → Node.js 16
- python:3.9-slim → Python 3.9
- openjdk:11-jre → Java 11
- mcr.microsoft.com/dotnet/runtime:6.0 → .NET 6
```

## Confidence Determination

### High Confidence
- ✅ Runtime base image clearly specified
- ✅ Build commands match runtime
- ✅ Dependency files present
- **Example**: "Node.js 16 runtime based on FROM node:16-alpine and package.json"

### Medium Confidence
- ⚠️ Generic base with runtime installed
- ⚠️ Multi-language project
- **Example**: "Java application, version unclear (uses maven but base is Ubuntu)"

### Low Confidence
- ⚠️ No clear runtime indicators
- **Example**: "Compiled binary, runtime unclear"

### Not Applicable
- ❌ No container
- **Example**: "No Dockerfile found"

## Output Format

```json
{
  "input_name": "Runtime Environment",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Runtime identified}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Base image}",
      "{Build commands}",
      "{Dependency files}"
    ],
    "values": [
      "{Runtime: Node.js, Python, Java, .NET, Go, etc.}",
      "{Version}",
      "{Variant: alpine, slim, etc.}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
