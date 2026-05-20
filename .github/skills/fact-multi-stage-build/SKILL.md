---
name: fact-multi-stage-build
description: Check if Dockerfile uses multi-stage build pattern
---

# Multi-stage Build Analysis

## Purpose
Determine if the project uses Docker multi-stage builds for image optimization.

## Target Files/Locations
- **/Dockerfile, **/Dockerfile.*, **/*.Dockerfile, **/Containerfile

## Analysis Steps

### 1. Find Dockerfile(s)
```
Use Glob: **/Dockerfile, **/Dockerfile.*, **/*.Dockerfile, **/Containerfile
List all matching files
```

### 2. Count FROM Instructions
```
Use Grep: "^FROM\\s+"
Files: (all Dockerfiles found in step 1)

Count the number of FROM instructions per file:
- 1 FROM = single-stage build
- 2+ FROM = multi-stage build
```

### 3. Extract Named Stages
```
Use Grep: "^FROM\\s+.*\\s+[Aa][Ss]\\s+"
Files: (all Dockerfiles found in step 1)
Context: full line

Extract stage names from "FROM ... AS stage_name" patterns
```

### 4. Verify Stage Usage
```
Use Grep: "--from="
Files: (all Dockerfiles found in step 1)

Check COPY --from=stage_name instructions to verify multi-stage usage
```

## Confidence Determination

### High Confidence
- ✅ Multiple FROM instructions with named stages
- ✅ COPY --from= instructions present
- **Example**: "Multi-stage build detected in Dockerfile with 3 stages (builder, tester, runtime)"

### Medium Confidence
- ⚠️ Multiple FROM instructions but no named stages
- **Example**: "Multi-stage build with 2 unnamed stages"

### Low Confidence
- ⚠️ Single FROM instruction
- **Example**: "Single-stage build, no optimization"

### Not Applicable
- ❌ No Dockerfile found
- **Example**: "No Dockerfile or Containerfile found in project"

## Output Format

```json
{
  "input_name": "Multi-stage Build",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Multi-stage build summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Dockerfile locations}",
      "{FROM instruction count}",
      "{Named stages}"
    ],
    "values": [
      "{Build type: Multi-stage or Single-stage}",
      "{Stage count}",
      "{Stage names if available}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
