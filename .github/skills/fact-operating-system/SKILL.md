---
name: fact-operating-system
description: Identify target/current operating system for deployment
---

# Operating System Analysis

## Purpose
Determine the target or current operating system the application runs on, especially for containerized or cloud-native applications.

## Target Files/Locations
- **/Dockerfile (FROM base image OS)
- **/README.md, **/docs/**/*.md (system requirements)
- **/k8s/**/*.yaml (nodeSelector, node affinity)
- **/pom.xml, **/*.csproj (target runtime identifiers)

## Example Patterns
- **Container base**: FROM alpine:3.15, FROM ubuntu:20.04, FROM mcr.microsoft.com/windows/servercore:ltsc2019
- **.NET RID**: linux-x64, win-x64, osx-x64
- **Node selector**: kubernetes.io/os: linux

## Analysis Steps

### 1. Check Container Base Image OS
```
Use Grep: "^FROM\\s+"
Files: **/Dockerfile
Extract base image name

Map to OS:
- alpine → Alpine Linux
- ubuntu → Ubuntu Linux
- debian → Debian Linux
- centos/rocky → CentOS/Rocky Linux
- windows/servercore → Windows Server
- mcr.microsoft.com/windows → Windows
```

### 2. Check .NET Runtime Identifiers
```
Use Grep: "RuntimeIdentifier|<RuntimeIdentifiers>"
Files: **/*.csproj

RIDs:
- linux-x64 → Linux 64-bit
- linux-arm64 → Linux ARM 64-bit
- win-x64 → Windows 64-bit
- win-arm64 → Windows ARM 64-bit
- osx-x64 → macOS Intel
- osx-arm64 → macOS Apple Silicon
```

### 3. Check Kubernetes Node Selectors
```
Use Grep: "nodeSelector:|kubernetes\\.io/os:"
Files: **/k8s/**/*.yaml
Context: -A 3

Values:
- linux → Linux nodes
- windows → Windows nodes
```

### 4. Check Documentation
```
Use Read: **/README.md (first 100 lines)
Look for:
- System Requirements section
- OS mentions (Linux, Windows, macOS)
- Installation instructions per OS
```

### 5. Check Platform-Specific Scripts
```
Use Glob:
- **/*.sh → Linux/macOS
- **/*.ps1, **/*.bat → Windows

Presence indicates OS support
```

## Confidence Determination

### High Confidence
- ✅ OS explicitly defined in container base or RID
- ✅ Documentation confirms OS
- **Example**: "Target OS: Alpine Linux 3.15 from Dockerfile base image"

### Medium Confidence
- ⚠️ OS inferred from framework or scripts
- **Example**: "Likely Linux (shell scripts present, typical Java deployment)"

### Low Confidence
- ⚠️ OS unclear, multiple possibilities
- **Example**: "Cross-platform framework, specific OS deployment unclear"

### Not Applicable
- ❌ Pure Java/JVM with no OS-specific features
- **Example**: "Platform-independent Java library"

## Output Format

```json
{
  "input_name": "Operating System",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{OS summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Container base image}",
      "{Runtime identifier}",
      "{Documentation}",
      "{Scripts}"
    ],
    "values": [
      "{OS: Alpine Linux, Ubuntu, Windows Server, etc.}",
      "{Version: 3.15, 20.04, 2019, etc.}",
      "{Architecture: x64, arm64}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
