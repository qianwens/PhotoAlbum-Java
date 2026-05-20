---
name: fact-volume-mounts
description: Identify persistent volume configurations for data storage
---

# Volume Mounts Analysis

## Purpose
Identify persistent storage volumes configured for data persistence, configuration, and logs.

## Target Files/Locations
- **/Dockerfile** (VOLUME instruction)
- **/docker-compose*.yml** (volumes section)
- **/k8s/**/*.yaml** (volumeMounts, volumes, PersistentVolumeClaim)

## Example Patterns
- `VOLUME /data /logs`
- `volumes: - ./data:/app/data`
- `mountPath: /var/lib/postgresql/data`

## Analysis Steps

### 1. Check Dockerfile VOLUME
```
Use Grep: "^VOLUME\\s+"
Files: **/Dockerfile
Extract volume paths
```

### 2. Analyze docker-compose Volumes
```
Use Read: **/docker-compose*.yml
Look for volumes: section (both top-level and per-service)
Types: bind mounts, named volumes, tmpfs
```

### 3. Check Kubernetes Volumes
```
Use Grep: "volumeMounts:|volumes:|persistentVolumeClaim"
Files: **/k8s/**/*.yaml
Context: -B 1 -A 5
```

### 4. Categorize Volume Purposes
```
Group by type:
- Data: /data, /var/lib/postgresql, /var/lib/mysql
- Logs: /logs, /var/log
- Config: /etc/config, /app/config
- Temp: /tmp, /var/tmp
```

## Confidence Determination

### High Confidence
- ✅ Volumes explicitly configured
- ✅ Mount paths and purposes clear
- **Example**: "3 volumes: /data for database, /logs for application logs, /config for runtime config"

### Medium Confidence
- ⚠️ VOLUME declared but mount points unclear
- **Example**: "Dockerfile declares VOLUME /data but docker-compose doesn't mount it"

### Low Confidence
- ⚠️ No explicit volumes but app may use storage
- **Example**: "No volumes configured, data likely ephemeral"

### Not Applicable
- ❌ Stateless application
- **Example**: "Stateless API with no persistent storage"

## Output Format

```json
{
  "input_name": "Volume Mounts",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Volumes summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Dockerfile VOLUME}",
      "{docker-compose volumes}",
      "{K8s PVC/volumes}"
    ],
    "values": [
      "{Volume paths}",
      "{Purposes: data, logs, config}",
      "{Volume types: bind, named, PVC}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
