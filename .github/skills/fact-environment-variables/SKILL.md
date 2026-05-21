---
name: fact-environment-variables
description: Identify container environment variables and configuration
---

# Environment Variables Analysis

## Purpose
Catalog environment variables used in containerized applications for configuration, secrets, and runtime behavior.

## Target Files/Locations
- **/Dockerfile (ENV instruction)
- **/docker-compose*.yml (environment section)
- **/k8s/**/*.yaml (env, envFrom)
- **/.env, **/.env.example

## Example Patterns
- `ENV DATABASE_URL=...`
- `environment: - NODE_ENV=production`
- `env: - name: API_KEY`
- `envFrom: - configMapRef`

## Analysis Steps

### 1. Check Dockerfile ENV
```
Use Grep: "^ENV\\s+"
Files: **/Dockerfile
Extract variable names and default values
```

### 2. Analyze docker-compose Environment
```
Use Read: **/docker-compose*.yml
Look for environment: section
Format: KEY=VALUE or array of strings
```

### 3. Check Kubernetes ConfigMaps/Secrets
```
Use Grep: "env:|envFrom:|configMapRef|secretRef"
Files: **/k8s/**/*.yaml
Context: -B 2 -A 5
```

### 4. Check .env Files
```
Use Glob: **/.env, **/.env.example, **/.env.template
Use Read to list variable names (mask values)
```

### 5. Categorize Variables
```
Group by type:
- Database: DATABASE_URL, DB_HOST, DB_PASSWORD
- API Keys: API_KEY, SECRET_KEY
- Feature Flags: ENABLE_FEATURE_X
- Runtime: NODE_ENV, LOG_LEVEL, DEBUG
```

## Confidence Determination

### High Confidence
- ✅ Variables explicitly defined in multiple files
- ✅ .env.example provides template
- **Example**: "12 environment variables configured including DATABASE_URL, API_KEY, NODE_ENV"

### Medium Confidence
- ⚠️ Some variables in code but not all documented
- **Example**: "Environment variables used but no .env.example template"

### Low Confidence
- ⚠️ Variables referenced but not listed
- **Example**: "Application likely uses env vars but none explicitly configured"

### Not Applicable
- ❌ No container or hardcoded config
- **Example**: "No environment variable usage detected"

## Output Format

```json
{
  "input_name": "Environment Variables",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Variables summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Dockerfile ENV count}",
      "{docker-compose environment}",
      "{K8s ConfigMap/Secret refs}",
      "{.env file presence}"
    ],
    "values": [
      "{Variable names (masked values)}",
      "{Categories: database, api, runtime, etc.}",
      "{Count: N variables}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
