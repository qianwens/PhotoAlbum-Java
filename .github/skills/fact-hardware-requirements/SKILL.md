---
name: fact-hardware-requirements
description: Identify minimum hardware requirements (RAM, CPU, disk)
---

# Hardware Requirements Analysis

## Purpose
Extract minimum hardware requirements from documentation, resource configurations, and deployment files.

## Target Files/Locations
- **/README.md, **/INSTALL.md, **/REQUIREMENTS.md (system requirements)
- **/docs/**/*.md (hardware mentions)
- **/docker-compose*.yml (resource limits)
- **/k8s/**/*.yaml (resource requests/limits)

## Example Patterns
- "4GB RAM minimum"
- "2 CPU cores recommended"
- "10GB disk space required"
- `limits: memory: "4Gi", cpu: "2"`

## Analysis Steps

### 1. Check Documentation
```
Use Read: **/README.md, **/INSTALL.md, **/REQUIREMENTS.md
Search for:
- "System Requirements" section
- "Hardware Requirements" section
- RAM/memory mentions (GB, GiB)
- CPU mentions (cores, GHz)
- Disk mentions (GB storage)

Use Grep: "[0-9]+\\s*(GB|GiB|MB|MiB)|[0-9]+\\s*(cores?|CPU)|disk|storage"
Context: -B 2 -A 2
```

### 2. Check Container Resource Limits
```
Use Read: **/docker-compose*.yml
Look for deploy.resources.limits/reservations

Use Grep: "memory:|cpu:"
Files: **/k8s/**/*.yaml
Context: -B 3 -A 1

Extract resource specifications:
- Memory: 2Gi, 4Gi, 512Mi
- CPU: 1000m, 2, 500m
```

### 3. Analyze Resource Patterns
```
From K8s/Compose:
- limits = maximum resources
- requests/reservations = minimum required

Calculate totals for multi-container apps
```

### 4. Check Database Requirements
```
If database used, estimate:
- PostgreSQL: ~1GB RAM minimum
- MySQL: ~512MB RAM minimum
- MongoDB: ~1GB RAM minimum
- Plus storage for data
```

## Confidence Determination

### High Confidence
- ✅ Requirements explicitly documented
- ✅ Resource limits configured match docs
- **Example**: "4GB RAM, 2 CPU cores, 10GB disk from README and matching K8s resource requests"

### Medium Confidence
- ⚠️ Requirements in one source only
- **Example**: "4GB memory limit in docker-compose, no documentation"

### Low Confidence
- ⚠️ Requirements estimated from resources used
- **Example**: "Estimated 2GB RAM based on container limits, not documented"

### Not Applicable
- ❌ Serverless or managed platform
- **Example**: "AWS Lambda deployment, hardware not directly specified"

## Output Format

```json
{
  "input_name": "Hardware Requirements",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Hardware summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Documentation sections}",
      "{Container resource limits}",
      "{Calculations}"
    ],
    "values": [
      "{RAM: minimum and recommended}",
      "{CPU: cores or millicores}",
      "{Disk: storage requirements}",
      "{Network: if specified}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
