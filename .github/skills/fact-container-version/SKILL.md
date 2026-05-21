---
name: fact-container-version
description: Identify container runtime version (Docker, Podman version)
---

# Container Version Analysis

## Purpose
Determine the version of the container runtime being used through CI/CD configurations, documentation, or system requirements.

## Target Files/Locations
- **/.github/workflows/*.yml, **/.gitlab-ci.yml
- **/README.md, **/docs/**/*.md
- **/Makefile, **/*.sh
- **/docker-compose.yml (version field)

## Example Patterns
- `docker-compose version: '3.8'`
- Docker version: 20.10.17
- Podman version: 4.1.0

## Analysis Steps

### 1. Check docker-compose Version
```
Use Glob: **/docker-compose*.yml
Use Read to find: version: '3.x' or version: '2.x'
This indicates required Docker Compose version
```

### 2. Search CI/CD for Version Specs
```
Use Grep: "docker.*version|container.*version"
Files: **/.github/workflows/*.yml, **/.gitlab-ci.yml
Context: -B 2 -A 2
```

### 3. Check Documentation
```
Use Grep: "docker.*[0-9]+\\.[0-9]+|podman.*[0-9]+\\.[0-9]+"
Files: **/README.md, **/docs/**/*.md
Context: -B 1 -A 1
```

### 4. Look for Version Requirements
```
Search for:
- "requires Docker 20.10+"
- "tested with Podman 4.x"
- Minimum version specifications
```

## Confidence Determination

### High Confidence
- ✅ docker-compose version explicitly set
- ✅ CI/CD specifies container version
- ✅ Documentation states version requirements
- **Example**: "Docker 20.10.17 specified in CI/CD, docker-compose v3.8"

### Medium Confidence
- ⚠️ docker-compose version found but engine version unclear
- ⚠️ Version mentioned in docs but not enforced
- **Example**: "docker-compose v3.8 indicates Docker 19.03+ requirement"

### Low Confidence
- ⚠️ No explicit version information
- ⚠️ Version inferred from features used
- **Example**: "Features used suggest Docker 20.10+ but not specified"

### Not Applicable
- ❌ No containerization
- **Example**: "No container configuration found"

## Output Format

```json
{
  "input_name": "Container Version",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Container version information}",
    "confidence": "high|medium|low",
    "evidence": [
      "{docker-compose version}",
      "{CI/CD specifications}",
      "{Documentation references}"
    ],
    "values": [
      "{Engine: Docker/Podman}",
      "{Version number or requirement}",
      "{Compose version if applicable}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
