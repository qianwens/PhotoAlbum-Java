---
name: fact-base-image
description: Identify container base image used in Dockerfile
---

# Base Image Analysis

## Purpose
Identify the base container image (e.g., alpine:3.15, ubuntu:20.04, node:16-alpine) used in Dockerfile/Containerfile to understand OS dependencies and image foundations.

## Target Files/Locations
- **/Dockerfile, **/Containerfile
- **/docker-compose*.yml
- **/k8s/**/*.yaml

## Example Patterns
- `FROM alpine:3.15`
- `FROM ubuntu:20.04`
- `FROM node:16-alpine AS builder`
- `FROM mcr.microsoft.com/dotnet/sdk:6.0`

## Analysis Steps

### 1. Find and Read Dockerfiles
```
Use Glob: **/Dockerfile, **/Containerfile
Use Read to examine each file
Look for FROM instructions
```

### 2. Extract Base Images
```
Use Grep: "^FROM\\s+"
Files: **/Dockerfile, **/Containerfile
Context: -A 1

Parse format: FROM <image>:<tag> [AS <stage>]
```

### 3. Check for Multi-stage Builds
```
Multiple FROM instructions indicate multi-stage build
Identify final stage base image
Note all intermediate base images
```

### 4. Verify Image Registry
```
Check for:
- Docker Hub (no prefix or docker.io/)
- MCR (mcr.microsoft.com/)
- GCR (gcr.io/)
- ECR (*.amazonaws.com/)
- Custom registry
```

## Confidence Determination

### High Confidence
- ✅ Dockerfile exists with explicit FROM instruction
- ✅ Image name and tag clearly specified
- **Example**: "Base image: alpine:3.15 from Dockerfile line 1"

### Medium Confidence
- ⚠️ Multiple stages with different base images
- ⚠️ FROM uses build argument (FROM ${BASE_IMAGE})
- **Example**: "Base image uses variable, likely node:16 based on docker-compose"

### Low Confidence
- ⚠️ No Dockerfile found
- ⚠️ Base image unclear from manifests
- **Example**: "Kubernetes deployment exists but base image not specified"

### Not Applicable
- ❌ No containerization
- **Example**: "No container files found"

## Output Format

```json
{
  "input_name": "Base Image",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Base image identified}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Dockerfile location}",
      "{FROM instruction(s)}",
      "{Multi-stage details if applicable}"
    ],
    "values": [
      "{Base image name:tag}",
      "{OS type (Alpine, Ubuntu, etc.)}",
      "{Registry source}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
