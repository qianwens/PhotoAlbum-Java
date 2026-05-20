---
name: fact-health-checks
description: Identify health check configurations (HTTP checks, command checks)
---

# Health Checks Analysis

## Purpose
Identify health check and readiness probe configurations for monitoring application health.

## Target Files/Locations
- **/Dockerfile (HEALTHCHECK instruction)
- **/docker-compose*.yml (healthcheck section)
- **/k8s/**/*.yaml (livenessProbe, readinessProbe, startupProbe)
- **/*.{java,cs,js,py,go} (health endpoints)

## Example Patterns
- `HEALTHCHECK CMD curl -f http://localhost/ || exit 1`
- `healthcheck: test: ["CMD", "curl", "-f", "http://localhost"]`
- `livenessProbe: httpGet: path: /health`

## Analysis Steps

### 1. Check Dockerfile HEALTHCHECK
```
Use Grep: "^HEALTHCHECK"
Files: **/Dockerfile
Parse: CMD, interval, timeout, retries
```

### 2. Analyze docker-compose Healthchecks
```
Use Read: **/docker-compose*.yml
Look for healthcheck: section per service
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost/health"]
    interval: 30s
    timeout: 10s
    retries: 3
```

### 3. Check Kubernetes Probes
```
Use Grep: "livenessProbe:|readinessProbe:|startupProbe:"
Files: **/k8s/**/*.yaml
Context: -A 10

Parse probe types:
- httpGet: path + port
- exec: command
- tcpSocket: port
```

### 4. Search for Health Endpoints in Code
```
Use Grep: "/health|/healthz|/ready|/live|HealthCheck"
Files: **/*.{java,cs,js,py,go}
Context: -B 2 -A 5

Common frameworks:
- Spring Boot: /actuator/health
- ASP.NET Core: /health
- Express.js: /health
```

## Confidence Determination

### High Confidence
- ✅ Health checks configured in orchestration files
- ✅ Health endpoint exists in code
- **Example**: "Health checks: HTTP GET /health endpoint with 30s interval, 3 retries"

### Medium Confidence
- ⚠️ Health check configured but endpoint unclear
- **Example**: "HEALTHCHECK defined using curl but endpoint not verified"

### Low Confidence
- ⚠️ No explicit health checks configured
- **Example**: "No health checks configured, relies on container exit codes"

### Not Applicable
- ❌ Simple app with no health monitoring needs
- **Example**: "Batch job, health checks not applicable"

## Output Format

```json
{
  "input_name": "Health Checks",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Health checks summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Dockerfile HEALTHCHECK}",
      "{docker-compose healthcheck}",
      "{K8s probes}",
      "{Health endpoint in code}"
    ],
    "values": [
      "{Check type: HTTP, exec, TCP}",
      "{Endpoint: /health, /ready, etc.}",
      "{Timing: interval, timeout, retries}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
