---
name: fact-service-definition
description: Analyze service definition files (docker-compose.yml, K8s manifests)
---

# Service Definition Analysis

## Purpose
Catalog and analyze service definition files that describe how the application is deployed and orchestrated.

## Target Files/Locations
- **/docker-compose*.yml, **/docker-compose.*.yml
- **/k8s/**/*.yaml, **/manifests/**/*.yaml
- **/helm/**/templates/*.yaml

## Example Patterns
- Docker Compose services with image, ports, volumes, environment
- Kubernetes Deployments, Services, ConfigMaps, Secrets
- Helm charts with templated manifests

## Analysis Steps

### 1. Catalog Docker Compose Files
```
Use Glob: **/docker-compose*.yml
For each file:
- Count services defined
- Check for extends or depends_on
- Note environment variants (dev, prod)
```

### 2. Catalog Kubernetes Manifests
```
Use Glob: **/k8s/**/*.yaml, **/manifests/**/*.yaml
Use Grep: "kind: Deployment|kind: Service|kind: ConfigMap|kind: Secret"
Files: **/*.yaml
Count by kind

Group by resource type:
- Workloads: Deployment, StatefulSet, DaemonSet, Job
- Services: Service, Ingress
- Config: ConfigMap, Secret
- Storage: PersistentVolumeClaim
```

### 3. Check for Helm Charts
```
Use Glob: **/Chart.yaml, **/values.yaml
If found: Helm is used
Count template files
```

### 4. Analyze Service Complexity
```
For Compose:
- Single service vs multi-service
- Service dependencies (depends_on)

For K8s:
- Microservices count
- Service mesh indicators
- Namespace organization
```

## Confidence Determination

### High Confidence
- ✅ Service files present and parseable
- ✅ Clear service structure
- **Example**: "3-service docker-compose with web, api, database services fully configured"

### Medium Confidence
- ⚠️ Some service files found but structure unclear
- **Example**: "K8s manifests present but relationships between services unclear"

### Low Confidence
- ⚠️ Service definitions incomplete
- **Example**: "Partial service definitions, missing critical resources"

### Not Applicable
- ❌ No service definitions
- **Example**: "Single container, no orchestration files"

## Output Format

```json
{
  "input_name": "Service Definition",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Service definitions summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{File types and counts}",
      "{Service/resource counts}",
      "{Orchestration approach}"
    ],
    "values": [
      "{Tool: Compose, K8s, Helm}",
      "{Service count}",
      "{Resource types and counts}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
