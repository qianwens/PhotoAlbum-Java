---
name: fact-embedded-language-usage
description: Identifies whether the Java app executes or embeds code in another language or interpreter at runtime
---

# Embedded Language Usage Analysis

## Purpose
Detect if the application executes external processes, embeds scripting engines, or dynamically evaluates code in other languages at runtime. This includes shell command execution, JavaScript engines, Python interpreters, Groovy shells, and embedded SQL/native code execution.

## Target Files/Locations
- **Java source files**: **/*.java
- **Script files**: **/*.sh, **/*.bat, **/*.ps1
- **Configuration files**: **/application.{properties,yml}, **/pom.xml, **/build.gradle
- **Resources**: **/resources/**/*.js, **/resources/**/*.py, **/resources/**/*.groovy

## Example Patterns to Search
- **Process Execution**: `Runtime.getRuntime().exec()`, `ProcessBuilder`, `ProcessBuilder.command()`
- **Script Engines**: `ScriptEngineManager`, `ScriptEngine.eval()`, `Nashorn`, `GraalVM.Polyglot`
- **Embedded Interpreters**: `GroovyShell`, `PythonInterpreter`, `JRuby`, `Jython`
- **Dynamic Evaluation**: `eval()`, `compile()`, `interpret()`
- **Native Code**: `System.loadLibrary()`, `JNI`, `JNA`, `native` keyword
- **SQL Execution**: `Statement.execute()`, `PreparedStatement`, dynamic SQL construction

## Analysis Steps

### 1. Search for Process Execution
```
Use Grep tool to search for external process execution:
- Pattern: "Runtime\\.getRuntime\\(\\)\\.exec|ProcessBuilder|exec\\(|startProcess"
- Files: **/*.java
- Context: -B 2 -A 2 (2 lines before/after for context)

Look for:
- Shell command execution
- External program invocation
- Dynamic command construction
```

### 2. Search for ScriptEngine APIs
```
Use Grep tool to find scripting engine usage:
- Pattern: "ScriptEngineManager|ScriptEngine|Nashorn|GraalVM|Polyglot"
- Files: **/*.java
- Context: -B 3 -A 3

Check for:
- ScriptEngineManager instantiation
- JavaScript, Python, Groovy engine loading
- eval() or compile() calls
```

### 3. Search for Embedded Language Interpreters
```
Use Grep tool to detect interpreter embedding:
- Pattern: "GroovyShell|PythonInterpreter|JRuby|Jython|LuaJ|BeanShell"
- Files: **/*.java
- Context: -B 3 -A 3

Identify:
- Groovy script execution
- Python code embedding
- Ruby/Lua interpreters
```

### 4. Check for Native Library Loading
```
Use Grep tool to find native code usage:
- Pattern: "System\\.loadLibrary|System\\.load|native\\s+\\w+|JNI|JNA"
- Files: **/*.java
- Context: -B 2 -A 2

Look for:
- JNI native method declarations
- Dynamic library loading
- JNA interface definitions
```

### 5. Analyze Dependencies
```
Use Glob to find build files:
- **/pom.xml
- **/build.gradle
- **/build.gradle.kts

Use Read to check for dependencies:
- groovy-all, groovy-core
- jython, jruby
- nashorn-core, graalvm-js
- jna, jna-platform
- rhino (Mozilla JavaScript engine)
```

### 6. Check for Dynamic SQL Execution
```
Use Grep tool to find dynamic SQL:
- Pattern: "Statement\\.execute|executeUpdate|executeQuery|createStatement"
- Files: **/*.java
- Context: -B 3 -A 3

Analyze for:
- Dynamic SQL string construction
- Concatenated SQL queries
- PreparedStatement vs Statement usage
```

### 7. Scan for Script Files in Resources
```
Use Glob to find embedded scripts:
- **/resources/**/*.js
- **/resources/**/*.py
- **/resources/**/*.groovy
- **/resources/**/*.lua

If found, these may be loaded and executed at runtime
```

## Confidence Determination

### High Confidence Criteria
Evidence of actual embedded language execution with clear implementation:
- ✅ ScriptEngineManager or ProcessBuilder instantiated with specific parameters
- ✅ Code shows eval() or execute() calls with script content
- ✅ Dependencies include scripting engines (groovy, jython, nashorn)
- ✅ Script files found in resources directory
- ✅ Multiple instances of embedded language usage across codebase

**Examples**:
- "ScriptEngineManager found in MainController.java:45 with engine.eval(jsCode)"
- "GroovyShell.evaluate() called in RuleEngine.java with 15 .groovy files in resources/"
- "ProcessBuilder executing bash scripts found in 8 locations"

### Medium Confidence Criteria
Partial evidence or indirect indicators:
- ⚠️ Dependencies include scripting engines but no direct usage found
- ⚠️ Process execution found but limited to standard system commands
- ⚠️ Native library loading present but unclear purpose
- ⚠️ SQL execution detected but mostly using PreparedStatement
- ⚠️ Comments reference scripting but no implementation found

**Examples**:
- "Groovy dependency in pom.xml but no GroovyShell usage detected"
- "Runtime.exec() called once in utility class for system info"
- "Native library loaded but JNI methods not clearly identified"

### Low Confidence Criteria
Weak or ambiguous evidence:
- ⚠️ Only standard JDBC operations (no dynamic SQL)
- ⚠️ No scripting dependencies detected
- ⚠️ Process execution in test code only
- ⚠️ Commented-out embedded language code
- ⚠️ Assumptions based on project type

**Examples**:
- "Standard PreparedStatement usage only, no dynamic SQL"
- "No scripting engine references found"
- "Process execution only in unit tests for test setup"

### Not Applicable Criteria
When embedded language analysis doesn't apply:
- ❌ Pure Java application with no external language integration
- ❌ Library project with no executable code
- ❌ Static website or documentation-only repository
- ❌ Different platform (e.g., .NET project being analyzed for Java patterns)

**Examples**:
- "Pure Java Spring Boot REST API with no scripting requirements"
- "Maven plugin project with no runtime execution"
- "Documentation repository with no code"

## Output Format

**CRITICAL**: Use the `write_assessment_result` tool (not just output JSON text).

```json
{
  "input_name": "Embedded Language Usage",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Clear 1-2 sentence summary of embedded language usage}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Specific file path + line number where usage detected}",
      "{Type of embedded language (Groovy, JavaScript, shell, etc.)}",
      "{Dependencies or script files found}",
      "{Context of usage (business rules, data processing, etc.)}"
    ],
    "values": [
      "{Scripting engine name and version}",
      "{Number of usage instances}",
      "{Types of scripts found}",
      "{Native libraries loaded}"
    ]
  },
  "execution_time_seconds": {elapsed_time},
  "timestamp": "{ISO 8601 timestamp}"
}
```

**Finding Examples**:
- ✅ Good: "Application uses GroovyShell to execute business rules with 23 .groovy scripts in resources/rules/ directory"
- ✅ Good: "ScriptEngineManager loads Nashorn JavaScript engine to process data transformations in DataProcessor.java"
- ✅ Good: "ProcessBuilder executes shell scripts for deployment automation in 8 service classes"
- ✅ Good: "No embedded language usage detected - pure Java implementation with standard JDBC"
- ❌ Bad: "Scripting is used"
- ❌ Bad: "Found some code execution"

**Evidence Examples**:
- ✅ Good: "GroovyShell.evaluate() at src/main/java/com/example/rules/RuleEngine.java:67"
- ✅ Good: "groovy-all-2.5.14 dependency in pom.xml with 23 .groovy files in resources/rules/"
- ✅ Good: "ScriptEngineManager initialized in MainController.java:45 with JavaScript engine type"
- ❌ Bad: "Found scripting code"
- ❌ Bad: "Process execution detected"

## Error Handling

### 1. No Evidence Found
- Don't fail - report finding as "No embedded language usage detected"
- Set confidence to high if thorough search performed
- Provide reasoning: "Searched for process execution, script engines, and embedded interpreters - none found"

### 2. Ambiguous Results
- Report what was found with context
- Set confidence to medium
- Explain uncertainty: "Groovy dependency present but no explicit usage found in code"

### 3. Tool Failures
- If Grep fails, retry with simpler pattern
- If Grep still fails, try Bash with find/grep combination
- If Read fails on large files, try reading with offset/limit
- After 3 retry attempts, return error status with details

### 4. Large Codebases
- If initial search returns too many results (>500 matches), refine pattern
- Focus on main source directories (exclude test code initially)
- Prioritize by file path (src/main > src/test)
- Sample representative files for detailed analysis

## Example Complete Analysis

**Scenario**: Java Spring Boot application with Groovy rule engine

**Steps Executed**:
1. Grep for ScriptEngine: Found 3 matches in RuleEngine.java
2. Grep for GroovyShell: Found 15 matches across 5 files
3. Glob for .groovy files: Found 23 files in resources/rules/
4. Read RuleEngine.java: Confirmed GroovyShell usage with dynamic script loading
5. Read pom.xml: Found groovy-all-2.5.14 dependency

**Result**:
```json
{
  "input_name": "Embedded Language Usage",
  "analysis_method": "LLM",
  "status": "success",
  "result": {
    "finding": "Application uses Groovy as embedded scripting engine for business rules execution with 23 rule scripts loaded dynamically at runtime",
    "confidence": "high",
    "evidence": [
      "GroovyShell.evaluate() at src/main/java/com/example/rules/RuleEngine.java:67-89",
      "groovy-all-2.5.14 dependency in pom.xml line 45",
      "23 .groovy script files in src/main/resources/rules/ directory",
      "RuleLoader.java:34 loads scripts from classpath using ResourceLoader",
      "15 GroovyShell usage instances across 5 files in rules package"
    ],
    "values": [
      "Groovy 2.5.14 (groovy-all)",
      "GroovyShell with CompilerConfiguration",
      "23 business rule scripts (.groovy)",
      "Dynamic rule evaluation at runtime"
    ]
  },
  "execution_time_seconds": 38.5,
  "timestamp": "2026-02-28T10:15:42Z"
}
```
