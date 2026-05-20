---
name: fact-testing-framework
description: Analyze testing tools and frameworks used in the project
---

# Testing Framework Analysis

## Purpose
Detect testing frameworks and tools used in the codebase.

## Target Files/Locations
- **/pom.xml, **/build.gradle, **/build.gradle.kts (Java)
- **/*.csproj (C#/.NET)
- **/package.json (Node.js)
- **/requirements.txt, **/requirements-dev.txt, **/setup.py, **/pyproject.toml (Python)
- **/go.mod (Go)
- **/test/**/*.{java,cs,py,js,ts}, **/*Test.{java,cs}, **/*Tests.cs, **/*.test.{js,ts}, **/*.spec.{js,ts}, **/test_*.py, **/*_test.go

## Analysis Steps

### 1. Check Java Testing Frameworks (Maven/Gradle)
```
Use Grep: "junit-jupiter|<artifactId>junit</artifactId>|testng|mockito"
Files: **/pom.xml, **/build.gradle, **/build.gradle.kts

Map findings:
- junit-jupiter → JUnit 5
- <artifactId>junit</artifactId> → JUnit 4
- testng → TestNG
- mockito → Mockito
```

### 2. Check .NET Testing Frameworks
```
Use Grep: "xunit|nunit|MSTest"
Files: **/*.csproj

Map findings:
- xunit → xUnit
- nunit → NUnit
- MSTest → MSTest
```

### 3. Check Node.js Testing Frameworks
```
Use Grep: "\"jest\"|\"@types/jest\"|\"mocha\"|\"@types/mocha\"|\"chai\"|\"jasmine\"|\"vitest\"|\"@vitest\""
Files: **/package.json

Map findings:
- jest / @types/jest → Jest
- mocha / @types/mocha → Mocha
- chai / @types/chai → Chai
- jasmine / @types/jasmine → Jasmine
- vitest / @vitest → Vitest
```

### 4. Check Python Testing Frameworks
```
Use Grep: "pytest|unittest|nose"
Files: **/requirements.txt, **/requirements-dev.txt, **/setup.py, **/pyproject.toml

Map findings:
- pytest → pytest
- unittest → unittest
- nose → nose
```

### 5. Check Go Testing Frameworks
```
Use Grep: "testify|ginkgo"
Files: **/go.mod

Map findings:
- testify → testify
- ginkgo → Ginkgo
```

### 6. Count Test Files
```
Use Glob to find test files:
- **/*Test.java, **/*Test.cs, **/*Tests.cs
- **/*.test.js, **/*.test.ts, **/*.spec.js, **/*.spec.ts
- **/test_*.py, **/*_test.go

Count matching files for evidence
```

### 7. Analyze Test Patterns in Source
```
Use Grep: "@Test|@TestMethod|\\[Fact\\]|\\[Theory\\]|describe\\(|it\\(|test\\("
Files: **/*.{java,cs,js,ts,py}
Context: -B 1 -A 2

Check for common test annotations/decorators
```

## Confidence Determination

### High Confidence
- ✅ Testing framework dependencies found in build files
- ✅ Test files present with matching annotations
- **Example**: "JUnit 5, Mockito detected in pom.xml; Found 23 test files"

### Medium Confidence
- ⚠️ Test files found but no explicit framework dependency
- **Example**: "Test files found, framework inferred from annotations"

### Low Confidence
- ⚠️ Few test files, no framework dependencies
- **Example**: "2 test-like files found, no framework detected"

### Not Applicable
- ❌ No test files or testing dependencies
- **Example**: "No testing frameworks detected"

## Output Format

```json
{
  "input_name": "Testing Framework",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Frameworks summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Build file framework references}",
      "{Test file counts}",
      "{Test annotation patterns}"
    ],
    "values": [
      "{Detected frameworks: JUnit 5, Mockito, xUnit, Jest, etc.}",
      "{Test file count}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
