---
name: fact-network-settings
description: Analyze container network configuration (bridge, host, custom networks)
---

# Network Settings Analysis

## Purpose
Identify container networking configuration including network modes, custom networks, and inter-service communication.

## Target Files/Locations
- **/docker-compose*.yml (networks section)
- **/k8s/**/*.yaml (Service, NetworkPolicy)
- **/Dockerfile (EXPOSE)

## Example Patterns
- `networks: - frontend - backend`
- `network_mode: bridge|host|none`
- `kind: NetworkPolicy`

## Analysis Steps

### 1. Check docker-compose Networks
```
Use Read: **/docker-compose*.yml
Look for:
- networks: top-level definitions
- service-level network assignments
- network_mode: bridge, host, none, container:name
```

### 2. Analyze Kubernetes Networking
```
Use Grep: "kind: Service|kind: NetworkPolicy|clusterIP|nodePort"
Files: **/k8s/**/*.yaml
Context: -B 1 -A 10
```

### 3. Check for Custom Network Drivers
```
In docker-compose:
- driver: bridge, overlay, macvlan
- ipam: configuration
- external: true/false
```

## Confidence Determination

### High Confidence
- ✅ Networks explicitly configured
- ✅ Network mode and drivers specified
- **Example**: "Custom bridge network 'app-network' with frontend and backend subnets"

### Medium Confidence
- ⚠️ Default networking, no custom config
- **Example**: "Uses default bridge network, no custom configuration"

### Low Confidence
- ⚠️ Networking inferred from service definitions
- **Example**: "Networking likely default, no explicit configuration"

### Not Applicable
- ❌ Non-networked application
- **Example**: "CLI tool, no network requirements"

## Output Format

```json
{
  "input_name": "Network Settings",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Networking summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{docker-compose networks}",
      "{K8s Services/Policies}",
      "{Network mode}"
    ],
    "values": [
      "{Network names}",
      "{Network mode: bridge, host, overlay}",
      "{Driver: bridge, overlay, etc.}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
