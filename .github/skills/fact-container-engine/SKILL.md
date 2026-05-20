---
name: fact-container-engine
description: Identify container runtime being used (Docker, Podman, containerd)
---

# Container Engine Analysis

## Purpose
Determine which container engine the application uses (Docker, Podman, containerd, etc.) through analysis of configuration files, build scripts, and deployment manifests.

## Target Files/Locations
- **/Dockerfile, **/Containerfile
- **/docker-compose*.yml
- **/.dockerignore
- **/Makefile, **/*.sh (build scripts)
- **/k8s/**/*.yaml, **/*.yaml (Kubernetes manifests)
- **/README.md, **/docs/**/*.md (documentation)
- **/.github/workflows/*.yml, **/.gitlab-ci.yml (CI/CD)

## Example Patterns to Search
- **Docker**: `docker build`, `docker-compose`, `FROM`, `ENTRYPOINT`, `.dockerignore`
- **Podman**: `podman build`, `podman-compose`, `podman run`
- **containerd**: `ctr`, `nerdctl`
- **Build tools**: `docker buildx`, `buildah`, `kaniko`

## Analysis Steps

### 1. Check for Dockerfile/Containerfile
```
Use Glob: **/Dockerfile, **/Containerfile
- Dockerfile indicates Docker usage
- Containerfile indicates Podman/Buildah compatibility
```

### 2. Search for Docker Compose Files
```
Use Glob: **/docker-compose*.yml
Indicates Docker Compose usage
```

### 3. Analyze Build Scripts
```
Use Grep: "docker|podman|buildah|nerdctl"
Files: **/*.sh, **/Makefile, **/*.bash
Context: -B 2 -A 2
```

### 4. Check CI/CD Pipelines
```
Use Grep in CI files:
- Pattern: "docker|podman|container"
- Files: **/.github/workflows/*.yml, **/.gitlab-ci.yml
```

### 5. Review Documentation
```
Use Grep in docs:
- Pattern: "docker|podman|container engine"
- Files: **/README.md, **/docs/**/*.md
```

## Confidence Determination

### High Confidence
- ✅ Dockerfile + docker-compose.yml present
- ✅ Build scripts explicitly use docker commands
- ✅ CI/CD uses specific container engine
- **Example**: "Docker engine with Compose v2 based on docker-compose.yml and Dockerfile"

### Medium Confidence
- ⚠️ Generic Containerfile (Docker/Podman compatible)
- ⚠️ Build scripts don't specify engine
- **Example**: "Containerfile present, compatible with Docker or Podman"

### Low Confidence
- ⚠️ No explicit engine indicators
- ⚠️ Only Kubernetes manifests (engine unclear)
- **Example**: "Container usage implied but engine unclear"

### Not Applicable
- ❌ No containerization
- **Example**: "No container files found - traditional deployment"

## Output Format

```json
{
  "input_name": "Container Engine",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Container engine identified}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Files found}",
      "{Commands in scripts}",
      "{CI/CD configuration}"
    ],
    "values": [
      "{Engine name: Docker, Podman, etc.}",
      "{Compose version if applicable}",
      "{Build tools used}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
