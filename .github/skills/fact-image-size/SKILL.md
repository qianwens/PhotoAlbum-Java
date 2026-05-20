---
name: fact-image-size
description: Analyze and estimate container image size
---

# Image Size Analysis

## Purpose
Estimate container image size based on base image, installed packages, and copied files. Identify size optimization opportunities.

## Target Files/Locations
- **/Dockerfile, **/Containerfile
- Application artifacts to be copied

## Example Patterns
- Base image (alpine: ~5MB, ubuntu: ~70MB, node:16: ~900MB)
- Package installations (apt, yum, apk)
- Application files (JAR, WAR, binaries)

## Analysis Steps

### 1. Identify Base Image Size
```
Read Dockerfile for FROM instruction
Estimate base sizes:
- scratch: 0MB
- alpine:3.15: ~5MB
- distroless: ~20MB
- ubuntu:20.04: ~70MB
- debian:11: ~120MB
- node:16: ~900MB
- openjdk:11: ~600MB
- mcr.microsoft.com/dotnet/runtime:6.0: ~180MB
```

### 2. Analyze Package Installations
```
Use Grep: "apt-get install|apk add|yum install"
Files: **/Dockerfile
Context: -A 3

Estimate:
- Few utilities (curl, wget): +5-10MB
- Build tools (gcc, make): +100-200MB
- Large packages (nginx, postgresql): +50-100MB each
```

### 3. Check Application Files Size
```
For COPY/ADD instructions:
- Look for source paths
- Use Bash to check size: du -sh {source_path}
- Common sizes:
  - JAR files: 30-150MB
  - Node modules: 100-500MB
  - .NET publish: 50-100MB
```

### 4. Consider Multi-stage Build Efficiency
```
If multi-stage:
- Build stage size doesn't matter
- Only final stage COPY --from adds to size
- Final image = base + runtime files only
```

### 5. Calculate Estimate
```
Total = Base + Packages + Application Files + Layer Overhead
Layer overhead: ~10-20% for metadata
```

## Confidence Determination

### High Confidence
- ✅ Base image size known
- ✅ Application files sized via filesystem
- ✅ Package installations enumerated
- **Example**: "Estimated 250MB: alpine (5MB) + Java runtime (150MB) + app JAR (85MB) + dependencies (10MB)"

### Medium Confidence
- ⚠️ Base image known but packages unclear
- ⚠️ Application size estimated without measurement
- **Example**: "Approximately 200-300MB based on Node.js base and typical app size"

### Low Confidence
- ⚠️ Complex build process with many layers
- ⚠️ Cannot access application files for sizing
- **Example**: "Likely 100MB-1GB range, difficult to estimate without build"

### Not Applicable
- ❌ No containerization
- **Example**: "No Dockerfile found"

## Output Format

```json
{
  "input_name": "Image Size",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Image size estimate with breakdown}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Base image and size}",
      "{Package installations}",
      "{Application files size}",
      "{Calculation method}"
    ],
    "values": [
      "{Estimated total size: XMB or X.XGB}",
      "{Base image size}",
      "{Application layer size}",
      "{Dependencies size}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
