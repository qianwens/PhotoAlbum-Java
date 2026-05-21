---
name: fact-system-packages
description: Identify system packages installed in container (nginx, curl, git, etc.)
---

# System Packages Analysis

## Purpose
Identify OS-level system packages installed in the container image through package manager commands.

## Target Files/Locations
- **/Dockerfile, **/Containerfile

## Example Patterns
- `RUN apt-get install nginx curl git`
- `RUN apk add --no-cache ca-certificates tzdata`
- `RUN yum install -y postgresql-client`

## Analysis Steps

### 1. Find Package Installation Commands
```
Use Grep: "apt-get install|apt install|apk add|yum install|dnf install"
Files: **/Dockerfile
Context: -A 5 (capture multi-line installs)
```

### 2. Extract Package Names
```
Parse package manager commands:
- apt: after "install" keyword
- apk: after "add" keyword
- yum/dnf: after "install" keyword

Handle flags: --no-cache, -y, --no-install-recommends
Handle line continuations with \
```

### 3. Categorize Packages
```
Group by purpose:
- Web servers: nginx, apache2
- SSL/Certificates: ca-certificates, openssl
- Development tools: git, curl, wget, vim
- Database clients: postgresql-client, mysql-client
- Build tools: gcc, make, build-essential
- Utilities: tzdata, bash, coreutils
```

### 4. Count Total Packages
```
Sum all packages across all RUN commands
Note if cleanup commands present (apt-get clean, rm -rf /var/lib/apt/lists/*)
```

## Confidence Determination

### High Confidence
- ✅ Package install commands clearly visible
- ✅ Package names explicitly listed
- **Example**: "15 system packages installed: nginx, curl, git, ca-certificates, tzdata, etc."

### Medium Confidence
- ⚠️ Some packages via install scripts
- **Example**: "Packages installed via apt but list partially in script files"

### Low Confidence
- ⚠️ Base image includes packages, additions unclear
- **Example**: "Base image may include packages, specific additions unclear"

### Not Applicable
- ❌ No container or minimal base (scratch, distroless)
- **Example**: "Uses scratch base image with no package manager"

## Output Format

```json
{
  "input_name": "System Packages",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Packages summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Package manager commands}",
      "{Package count}",
      "{Installation patterns}"
    ],
    "values": [
      "{Package names list}",
      "{Categories: web, ssl, dev tools, etc.}",
      "{Package manager: apt, apk, yum}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
