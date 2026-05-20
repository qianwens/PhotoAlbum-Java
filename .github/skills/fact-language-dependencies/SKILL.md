---
name: fact-language-dependencies
description: Identify language-specific dependencies in container (package.json, requirements.txt, pom.xml)
---

# Language Dependencies Analysis

## Purpose
Identify application-level dependencies through package manifests copied into the container image.

## Target Files/Locations
- **/package.json, **/package-lock.json (Node.js)
- **/requirements.txt, **/Pipfile (Python)
- **/pom.xml, **/build.gradle (Java)
- **/*.csproj, **/packages.config (.NET)
- **/go.mod, **/go.sum (Go)
- **/Gemfile, **/Gemfile.lock (Ruby)
- **/composer.json (PHP)

## Example Patterns
- `COPY package*.json ./`
- `RUN pip install -r requirements.txt`
- `RUN npm install --production`
- `RUN mvn clean install`

## Analysis Steps

### 1. Identify Copied Dependency Files
```
Use Grep: "COPY.*(package\\.json|requirements\\.txt|pom\\.xml|.*\\.csproj|go\\.mod|Gemfile|composer\\.json)"
Files: **/Dockerfile
Context: -B 1 -A 1
```

### 2. Read Dependency Files
```
Use Glob to find dependency files in project:
- **/package.json (read dependencies section)
- **/requirements.txt (read package list)
- **/pom.xml (read <dependencies>)
- **/*.csproj (read <PackageReference>)
```

### 3. Count and Categorize Dependencies
```
For each runtime:
- Node.js: dependencies vs devDependencies
- Python: required packages
- Java: compile, runtime, test scope
- .NET: PackageReference items
- Go: direct vs indirect
```

### 4. Check Install Commands
```
Use Grep: "npm install|pip install|mvn|gradle|dotnet restore|go mod download"
Files: **/Dockerfile
Verify dependencies are installed in image
```

## Confidence Determination

### High Confidence
- ✅ Dependency files copied and installed in Dockerfile
- ✅ Files readable and parseable
- **Example**: "45 Node.js dependencies from package.json installed via npm install"

### Medium Confidence
- ⚠️ Dependency files exist but install command unclear
- **Example**: "package.json present, installation method not explicit"

### Low Confidence
- ⚠️ Can't access dependency files
- **Example**: "Dependency files referenced but not readable"

### Not Applicable
- ❌ No language dependencies (native binary)
- **Example**: "Compiled Go binary with no external dependencies"

## Output Format

```json
{
  "input_name": "Language Dependencies",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Dependencies summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Dependency files found}",
      "{COPY/install commands}",
      "{Dependency count}"
    ],
    "values": [
      "{Dependency file: package.json, requirements.txt, etc.}",
      "{Dependency count}",
      "{Key dependencies list}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
