---
name: fact-resource-limits
description: Identify CPU/Memory resource limits for containers
---

# Resource Limits Analysis

## Purpose
Identify CPU and memory resource constraints configured for containers through compose files or Kubernetes manifests.

## Target Files/Locations
- **/docker-compose*.yml (deploy.resources)
- **/k8s/**/*.yaml (resources.requests, resources.limits)
- **/Dockerfile (no resource limits, but checked for context)

## Example Patterns
- `memory: 2g`, `cpus: '1.5'`
- `limits: memory: "2Gi", cpu: "1000m"`
- `requests: memory: "512Mi", cpu: "250m"`

## Analysis Steps

### 1. Check docker-compose Resources
```
Use Read: **/docker-compose*.yml
Look for deploy.resources section:
  deploy:
    resources:
      limits:
        cpus: '2.0'
        memory: 2G
      reservations:
        cpus: '0.5'
        memory: 512M
```

### 2. Analyze Kubernetes Resources
```
Use Grep: "resources:|limits:|requests:|memory:|cpu:"
Files: **/k8s/**/*.yaml
Context: -B 3 -A 3

Parse format:
  resources:
    limits:
      memory: "2Gi"
      cpu: "1000m"
    requests:
      memory: "512Mi"
      cpu: "250m"
```

### 3. Check for Resource Quotas
```
Use Grep: "kind: ResourceQuota"
Files: **/k8s/**/*.yaml
Namespace-level resource constraints
```

## Confidence Determination

### High Confidence
- ✅ Resource limits explicitly configured
- ✅ Both limits and requests defined
- **Example**: "Container limits: 2Gi memory, 1000m CPU; requests: 512Mi memory, 250m CPU"

### Medium Confidence
- ⚠️ Only limits or only requests defined
- **Example**: "Memory limit 2GB configured, CPU unspecified"

### Low Confidence
- ⚠️ No explicit resource configuration
- **Example**: "No resource limits configured, uses node defaults"

### Not Applicable
- ❌ No container orchestration
- **Example**: "Direct Docker run, no resource management"

## Output Format

```json
{
  "input_name": "Resource Limits",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Resources summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{docker-compose deploy.resources}",
      "{K8s limits/requests}",
      "{ResourceQuota if present}"
    ],
    "values": [
      "{Memory limits and requests}",
      "{CPU limits and requests}",
      "{Units: Gi, Mi, millicores}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
