---
name: fact-version-information
description: Extract application version from build files and configuration
---

# Version Information Analysis

## Purpose
Identify the application version number from build descriptors, manifests, and configuration files.

## Target Files/Locations
- **/pom.xml (<version>)
- **/*.csproj (<Version>)
- **/package.json (version field)
- **/build.gradle (version property)
- **/application.{properties,yml} (info.app.version)
- **/AssemblyInfo.cs ([assembly: AssemblyVersion])

## Example Patterns
- `<version>1.2.3</version>` (Maven)
- `"version": "2.0.0-beta"` (Node.js)
- `<Version>1.5.0</Version>` (.NET)
- `version = "3.1.4"` (Gradle)

## Analysis Steps

### 1. Check Build File Versions
```
Maven (pom.xml):
Use Grep: "<version>"
Extract first non-parent version

Gradle (build.gradle):
Use Grep: "^version\\s*="
Extract: version = '1.2.3'

Node.js (package.json):
Use Read and parse: { "version": "1.2.3" }

.NET (*.csproj):
Use Grep: "<Version>"
Extract: <Version>1.2.3</Version>
```

### 2. Check Assembly Info
```
.NET:
Use Grep: "AssemblyVersion|AssemblyFileVersion"
Files: **/AssemblyInfo.cs
Extract: [assembly: AssemblyVersion("1.2.3.4")]
```

### 3. Check Application Configuration
```
Use Grep: "version:|app\\.version|info\\.app\\.version"
Files: **/application.{properties,yml}, **/appsettings.json
```

### 4. Check Git Tags
```
Use Bash: git describe --tags --abbrev=0
Latest tag often represents version
```

## Confidence Determination

### High Confidence
- ✅ Version explicitly in build file
- ✅ Semantic versioning format (X.Y.Z)
- **Example**: "Application version: 1.2.3 from pom.xml and package.json"

### Medium Confidence
- ⚠️ Version found but format unusual
- ⚠️ Snapshot/development version
- **Example**: "Version: 2.0.0-SNAPSHOT (development version)"

### Low Confidence
- ⚠️ No version in files, inferred from git
- **Example**: "Version unclear, git tag suggests 1.0.0"

### Not Applicable
- ❌ Versioning not used
- **Example**: "No version information found in project"

## Output Format

```json
{
  "input_name": "Version Information",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Version summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Source file and location}",
      "{Version format}",
      "{Git tag if applicable}"
    ],
    "values": [
      "{Version number: X.Y.Z}",
      "{Version type: release, snapshot, beta}",
      "{Build/patch number if applicable}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
