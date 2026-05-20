---
name: fact-orchestration-tool
description: Identify container orchestration platform (Docker Compose, Kubernetes, Docker Swarm)
---

# Orchestration Tool Analysis

## Purpose
Determine which container orchestration tool manages the application deployment.

## Target Files/Locations
- **/docker-compose*.yml (Docker Compose)
- **/k8s/**/*.yaml, **/*.yaml (Kubernetes)
- **/swarm/ (Docker Swarm)
- **/.github/workflows/, **/.gitlab-ci.yml (CI/CD hints)

## Example Patterns
- Docker Compose: `docker-compose.yml`, `version: '3.8'`
- Kubernetes: `kind: Deployment`, `apiVersion: apps/v1`
- Docker Swarm: `deploy: mode: replicated`

## Analysis Steps

### 1. Check for Docker Compose
```
Use Glob: **/docker-compose*.yml
If found: Docker Compose is used
Check version: '2.x' or '3.x'
```

### 2. Check for Kubernetes Manifests
```
Use Glob: **/k8s/**/*.yaml, **/manifests/**/*.yaml
Use Grep: "apiVersion:.*apps/v1|kind: Deployment|kind: Service"
Files: **/*.yaml
If Kubernetes resources found: K8s is used
```

### 3. Check for Docker Swarm Config
```
Use Grep: "deploy:|mode: replicated|placement:"
Files: **/docker-compose*.yml
Swarm uses Compose format with deploy: section
```

### 4. Check CI/CD for Deployment Hints
```
Use Grep: "kubectl|helm|docker-compose|docker stack"
Files: **/.github/workflows/*.yml, **/.gitlab-ci.yml
Context: -B 2 -A 2
```

## Confidence Determination

### High Confidence
- ✅ Clear orchestration files present
- ✅ CI/CD deploys using specific tool
- **Example**: "Kubernetes orchestration with 15 manifests in k8s/ directory and kubectl in CI/CD"

### Medium Confidence
- ⚠️ Files present but usage unclear
- **Example**: "docker-compose.yml for local dev, K8s for production (multiple tools)"

### Low Confidence
- ⚠️ No clear orchestration indicators
- **Example**: "Single Dockerfile, orchestration unclear"

### Not Applicable
- ❌ No container orchestration
- **Example**: "Direct Docker run, no orchestration"

## Output Format

```json
{
  "input_name": "Orchestration Tool",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Orchestration summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{docker-compose.yml presence}",
      "{K8s manifest count and location}",
      "{CI/CD deployment commands}"
    ],
    "values": [
      "{Tool: Docker Compose, Kubernetes, Docker Swarm}",
      "{Version: Compose 3.8, K8s 1.25, etc.}",
      "{Manifest count}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
