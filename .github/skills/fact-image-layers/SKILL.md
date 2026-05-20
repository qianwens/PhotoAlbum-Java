---
name: fact-image-layers
description: Analyze container image layer count and structure
---

# Image Layers Analysis

## Purpose
Analyze Dockerfile instructions to understand image layer structure, count of layers, and optimization opportunities.

## Target Files/Locations
- **/Dockerfile, **/Containerfile

## Example Patterns
Layer-creating instructions: RUN, COPY, ADD, FROM
Non-layer instructions: ENV, ARG, LABEL, EXPOSE, CMD, ENTRYPOINT, WORKDIR

## Analysis Steps

### 1. Count Layer-Creating Instructions
```
Use Grep to count RUN/COPY/ADD:
- Pattern: "^(RUN|COPY|ADD)\\s+"
- Files: **/Dockerfile, **/Containerfile
- Mode: count

Each match creates a layer (except multi-stage FROM)
```

### 2. Analyze RUN Instruction Complexity
```
Use Read Dockerfile and analyze:
- Single-command RUN vs multi-command (&&)
- Layer optimization (combined commands)
- Example: RUN apt-get update && apt-get install (1 layer)
  vs: RUN apt-get update \n RUN apt-get install (2 layers)
```

### 3. Check for Multi-stage Build
```
Count FROM instructions:
Each stage adds base layers
Final image only includes layers from last stage + COPY --from
```

### 4. Identify Layer Size Contributors
```
Look for large operations:
- Package installations (apt-get, yum, apk)
- File copies (COPY large directories)
- Downloads (wget, curl in RUN)
```

## Confidence Determination

### High Confidence
- ✅ Dockerfile analyzed completely
- ✅ Clear count of layer instructions
- ✅ Multi-stage structure understood
- **Example**: "Image has 8 layers: 3 from base (alpine), 3 RUN, 2 COPY"

### Medium Confidence
- ⚠️ Some build-time variables affect layers
- ⚠️ External build process unclear
- **Example**: "Approximately 6-8 layers based on Dockerfile instructions"

### Low Confidence
- ⚠️ Dockerfile uses complex ARGs affecting structure
- ⚠️ BuildKit features that modify layering
- **Example**: "Layer count unclear due to conditional build steps"

### Not Applicable
- ❌ No Dockerfile
- **Example**: "No container image definition found"

## Output Format

```json
{
  "input_name": "Image Layers",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Layer analysis summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{RUN instruction count}",
      "{COPY/ADD instruction count}",
      "{Multi-stage stages}",
      "{Optimization patterns observed}"
    ],
    "values": [
      "{Estimated layer count}",
      "{FROM instructions: N}",
      "{RUN instructions: N}",
      "{COPY/ADD instructions: N}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
