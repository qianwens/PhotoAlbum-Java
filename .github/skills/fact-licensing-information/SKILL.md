---
name: fact-licensing-information
description: Identify software licensing details from LICENSE files and dependency analysis
---

# Licensing Information Analysis

## Purpose
Extract licensing information for the application and its dependencies to understand compliance requirements.

## Target Files/Locations
- **/LICENSE, **/LICENSE.txt, **/LICENSE.md
- **/pom.xml (<licenses>)
- **/package.json (license field)
- **/*.csproj (<PackageLicenseExpression>)
- **/NOTICE, **/COPYING, **/COPYRIGHT

## Example Patterns
- MIT License
- Apache License 2.0
- GPL v3, LGPL
- BSD 3-Clause
- Commercial/Proprietary

## Analysis Steps

### 1. Check License Files
```
Use Glob: **/LICENSE*, **/COPYING, **/COPYRIGHT
Use Read to examine content

Identify license type:
- MIT: "Permission is hereby granted, free of charge"
- Apache 2.0: "Apache License, Version 2.0"
- GPL: "GNU General Public License"
- BSD: "Redistribution and use in source and binary forms"
```

### 2. Check Build File Licenses
```
Maven (pom.xml):
Use Grep: "<licenses>|<license>"
Extract: <name>Apache License 2.0</name>

Node.js (package.json):
Use Read and parse: { "license": "MIT" }

.NET (*.csproj):
Use Grep: "<PackageLicenseExpression>"
Extract: <PackageLicenseExpression>MIT</PackageLicenseExpression>
```

### 3. Check Dependency Licenses
```
Look for license reports:
- **/license-report.html
- **/licenses/ directory
- THIRD-PARTY-NOTICES

Tools that generate these:
- maven-license-plugin
- license-checker (npm)
- dotnet list package --include-transitive
```

### 4. Scan for Commercial Licenses
```
Use Grep: "commercial|proprietary|all rights reserved|confidential"
Files: **/LICENSE*, **/README.md
Context: -B 2 -A 2
```

## Confidence Determination

### High Confidence
- ✅ LICENSE file present with clear text
- ✅ License in build file matches LICENSE file
- **Example**: "MIT License confirmed in LICENSE file and package.json"

### Medium Confidence
- ⚠️ License file present but type unclear
- ⚠️ Multiple licenses mentioned
- **Example**: "LICENSE file present, appears to be MIT but not standard format"

### Low Confidence
- ⚠️ No LICENSE file, inferred from comments
- **Example**: "No LICENSE file, copyright header suggests proprietary"

### Not Applicable
- ❌ Internal tool with no license requirement
- **Example**: "Internal company tool, no formal licensing"

## Output Format

```json
{
  "input_name": "Licensing Information",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{License summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{LICENSE file presence and content}",
      "{Build file license declaration}",
      "{Dependency licenses if available}",
      "{Copyright notices}"
    ],
    "values": [
      "{Primary license: MIT, Apache 2.0, etc.}",
      "{Dependency licenses if scanned}",
      "{Copyright holder}",
      "{License compatibility notes}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
