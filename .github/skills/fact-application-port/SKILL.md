---
name: fact-application-port
description: Identify exposed application ports from container configuration
---

# Application Port Analysis

## Purpose
Identify which ports the containerized application exposes for HTTP, HTTPS, and other services.

## Target Files/Locations
- **/Dockerfile (EXPOSE instruction)
- **/docker-compose*.yml (ports section)
- **/k8s/**/*.yaml (containerPort, servicePort)
- **/application.{properties,yml} (server.port)

## Example Patterns
- `EXPOSE 8080 443`
- `ports: - "3000:3000"`
- `containerPort: 8080`
- `server.port=8080`

## Analysis Steps

### 1. Check Dockerfile EXPOSE
```
Use Grep: "^EXPOSE\\s+"
Files: **/Dockerfile, **/Containerfile
Extract port numbers
```

### 2. Analyze docker-compose Ports
```
Use Read: **/docker-compose*.yml
Look for ports: section
Format: "HOST:CONTAINER" or just "PORT"
```

### 3. Check Kubernetes Manifests
```
Use Grep: "containerPort|servicePort|targetPort"
Files: **/k8s/**/*.yaml, **/*.yaml
Context: -B 2 -A 2
```

### 4. Check Application Configuration
```
Use Grep: "server\\.port|PORT|HTTP_PORT"
Files: **/application.{properties,yml}, **/.env
```

## Confidence Determination

### High Confidence
- ✅ EXPOSE in Dockerfile + ports in compose/k8s
- ✅ Application config matches container config
- **Example**: "Application exposes port 8080 (HTTP) and 443 (HTTPS) based on Dockerfile EXPOSE and docker-compose ports"

### Medium Confidence
- ⚠️ Ports in config but not all files consistent
- **Example**: "Port 8080 in Dockerfile EXPOSE, but docker-compose uses 3000:8080"

### Low Confidence
- ⚠️ No explicit port configuration
- **Example**: "No EXPOSE instruction, likely uses default runtime port"

### Not Applicable
- ❌ No container or non-networked app
- **Example**: "CLI application, no network ports"

## Output Format

```json
{
  "input_name": "Application Port",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Ports summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Dockerfile EXPOSE}",
      "{docker-compose ports}",
      "{K8s port config}",
      "{Application config}"
    ],
    "values": [
      "{Port numbers: 8080, 443, etc.}",
      "{Protocol: HTTP, HTTPS, TCP}",
      "{Port mapping if applicable}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
