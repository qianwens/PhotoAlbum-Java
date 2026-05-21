---
name: fact-startup-instrumentation
description: Analyze startup instrumentation (logging, telemetry, AOP)
---

# Startup Instrumentation Analysis

## Purpose
Detect and analyze logging frameworks, telemetry/APM tools, and aspect-oriented programming (AOP) components initialized at application startup.

## Analysis Strategy

This SKILL searches for configuration files, startup code, and dependency declarations to identify instrumentation frameworks.

## Analysis Steps

### 1. Logging Framework Detection

**Search for Logging Configuration Files:**
```bash
# Use Glob to find config files
Glob patterns:
- **/logback.xml, **/logback-spring.xml
- **/log4j2.xml, **/log4j2.yml, **/log4j.properties
- **/appsettings*.json (for Serilog/NLog in .NET)
- **/logging.conf, **/logging.yaml (Python)
- **/winston.config.js (Node.js)
```

**Search for Logging Dependencies:**
```bash
# Use Grep to find logging libraries
Pattern: "logback|log4j2|slf4j|serilog|nlog|ilogger|winston|bunyan|pino|logging\.getLogger"
Files: **/pom.xml, **/build.gradle, **/*.csproj, **/package.json, **/requirements.txt, **/Gemfile
```

**Search for Logger Initialization in Code:**
```bash
Pattern: "LoggerFactory|ILogger|getLogger|Logger\.getLogger|createLogger|logging\.basicConfig"
Files: **/Program.cs, **/Startup.cs, **/Main.java, **/*Application.java, **/app.py, **/main.py, **/server.js, **/app.js
```

### 2. Telemetry & APM Detection

**Application Insights (.NET/Java):**
```bash
Pattern: "applicationinsights|Microsoft\.ApplicationInsights|TelemetryClient"
Files: **/*.csproj, **/pom.xml, **/appsettings.json, **/ApplicationInsights.config
```

**OpenTelemetry (Cross-platform):**
```bash
Pattern: "opentelemetry|otel|TracerProvider|MeterProvider"
Files: **/pom.xml, **/build.gradle, **/*.csproj, **/package.json, **/requirements.txt
```

**New Relic:**
```bash
Pattern: "newrelic|New Relic"
Files: **/newrelic.yml, **/newrelic.config, **/newrelic.js
```

**Datadog:**
```bash
Pattern: "datadog|dd-trace|ddtrace"
Files: **/pom.xml, **/package.json, **/requirements.txt, **/Gemfile
```

**Dynatrace:**
```bash
Pattern: "dynatrace|oneagent"
Files: **/*.config, **/dockerfile, **/deployment.yaml
```

**Elastic APM:**
```bash
Pattern: "elastic-apm|ElasticApm"
Files: **/pom.xml, **/*.csproj, **/package.json, **/requirements.txt
```

### 3. Aspect-Oriented Programming (AOP) Detection

**Spring AOP (Java):**
```bash
Pattern: "@Aspect|@Before|@After|@Around|spring-aop|aspectjweaver"
Files: **/*.java, **/pom.xml, **/build.gradle
```

**PostSharp (.NET):**
```bash
Pattern: "PostSharp|[MethodInterception]|[OnMethodBoundary]"
Files: **/*.cs, **/*.csproj
```

**AspectJ:**
```bash
Pattern: "aspectj|@Pointcut|@Aspect"
Files: **/*.java, **/aop.xml, **/pom.xml
```

### 4. Startup Code Analysis

**Check Main Entry Points:**
```bash
# Use Glob to find entry points
Patterns:
- **/Program.cs (ASP.NET Core)
- **/Startup.cs (ASP.NET Core)
- **/Main.java, **/*Application.java (Spring Boot)
- **/app.py, **/main.py, **/__init__.py (Python)
- **/server.js, **/app.js, **/index.js (Node.js)
```

**Analyze Startup Configuration:**
```bash
# Read entry point files and check for:
- Logger configuration: builder.Logging.Add*, LogManager.Setup()
- Telemetry setup: services.AddApplicationInsightsTelemetry()
- AOP configuration: services.EnableAspectOrientedProgramming()
```

## Framework-Specific Patterns

### Java/Spring Boot

**Logback:**
```xml
<!-- logback-spring.xml -->
<configuration>
  <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
  ...
```
```java
// Code pattern
private static final Logger logger = LoggerFactory.getLogger(Application.class);
```

**Log4j2:**
```xml
<!-- log4j2.xml -->
<Configuration status="WARN">
  <Appenders>
```
```java
private static final Logger logger = LogManager.getLogger(Application.class);
```

### .NET/ASP.NET Core

**Serilog:**
```csharp
// Program.cs
Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .WriteTo.File("logs/log.txt")
    .CreateLogger();
```
```json
// appsettings.json
"Serilog": {
  "Using": ["Serilog.Sinks.Console", "Serilog.Sinks.File"]
}
```

**NLog:**
```csharp
// Program.cs
builder.Logging.ClearProviders();
builder.Host.UseNLog();
```
```xml
<!-- nlog.config -->
<nlog xmlns="http://www.nlog-project.org/schemas/NLog.xsd">
```

**ILogger (Built-in):**
```csharp
builder.Logging.AddConsole();
builder.Logging.AddDebug();
builder.Logging.AddApplicationInsights();
```

### Python

**Logging Module:**
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

**Loguru:**
```python
from loguru import logger
logger.add("file.log", rotation="500 MB")
```

### Node.js

**Winston:**
```javascript
const winston = require('winston');
const logger = winston.createLogger({
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

**Pino:**
```javascript
const pino = require('pino');
const logger = pino();
```

## Analysis Decision Logic

1. **Check for configuration files** → High confidence if config exists
2. **Check for dependencies** → Medium confidence
3. **Check for code usage** → Confirms framework is actively used
4. **Check for multiple frameworks** → List all detected

## Confidence Levels

- **High**: Configuration file + dependency + code usage detected
- **Medium**: Dependency + code usage (no explicit config)
- **Low**: Only dependency found (may not be actively used)

## Output Format

After analysis, call the MCP tool:

```javascript
write_assessment_result({
  resultJson: JSON.stringify({
    input_name: "Startup Instrumentation",
    analysis_method: "Hybrid",  // Code + LLM analysis
    status: "success",  // or "not_applicable" or "failed"
    result: {
      finding: "Serilog with Application Insights and custom AOP interceptors",
      confidence: "high",  // high, medium, or low
      evidence: [
        "Found appsettings.json with Serilog configuration (Console, File, Application Insights sinks)",
        "Program.cs configures Serilog at line 12: Log.Logger = new LoggerConfiguration()...",
        "ApplicationInsights.config found with instrumentation key",
        "Custom AOP: Found 3 MethodInterceptionAspect classes for logging, caching, and validation"
      ],
      values: [
        "Serilog 3.1.1",
        "Application Insights",
        "Custom AOP (MethodInterception)"
      ],
      instrumentation_details: {
        logging_framework: "Serilog",
        logging_version: "3.1.1",
        log_sinks: ["Console", "File", "ApplicationInsights"],
        telemetry_provider: "Application Insights",
        aop_framework: "Custom (MethodInterception)",
        startup_file: "Program.cs"
      }
    },
    execution_time_seconds: 2.8,
    timestamp: new Date().toISOString()
  }),
  assessmentDir: variables.assessment_dir
});
```

## Multiple Framework Examples

### Example 1: Spring Boot with Logback + Elastic APM + Spring AOP
```json
{
  "finding": "Logback with Elastic APM and Spring AOP",
  "confidence": "high",
  "evidence": [
    "logback-spring.xml found with RollingFileAppender",
    "pom.xml includes elastic-apm-agent 1.39.0",
    "Found 8 @Aspect classes for cross-cutting concerns",
    "Application.java initializes APM agent at startup"
  ],
  "values": ["Logback", "Elastic APM 1.39.0", "Spring AOP", "AspectJ"]
}
```

### Example 2: Python with Loguru + OpenTelemetry
```json
{
  "finding": "Loguru with OpenTelemetry",
  "confidence": "medium",
  "evidence": [
    "requirements.txt includes loguru==0.7.0",
    "app.py configures loguru with rotation and retention",
    "Found opentelemetry-api in requirements.txt",
    "No explicit OpenTelemetry initialization code found"
  ],
  "values": ["Loguru 0.7.0", "OpenTelemetry (partial)"]
}
```

### Example 3: Node.js with Winston + Datadog
```json
{
  "finding": "Winston with Datadog APM",
  "confidence": "high",
  "evidence": [
    "winston.config.js configures Console, File, and HTTP transports",
    "package.json includes winston@3.11.0 and dd-trace@4.23.0",
    "server.js imports and initializes dd-trace at line 1",
    "Found custom Winston format for JSON structured logging"
  ],
  "values": ["Winston 3.11.0", "Datadog APM 4.23.0"]
}
```

## Not Applicable Scenarios

Return `status: "not_applicable"` if:
- No logging framework detected (using only print/console.log)
- Project is a library without startup entry point
- CLI tool with minimal logging requirements

Example:
```json
{
  "input_name": "Startup Instrumentation",
  "analysis_method": "Code",
  "status": "not_applicable",
  "result": {
    "finding": "No structured logging framework detected",
    "confidence": "high",
    "evidence": [
      "No logging configuration files found",
      "No logging dependencies in package.json",
      "Only console.log statements found in code"
    ],
    "values": []
  },
  "execution_time_seconds": 1.2,
  "timestamp": "2026-03-01T01:00:00Z"
}
```

## Error Handling

Return `status: "failed"` if:
- Unable to access project files
- Critical analysis error occurred
- Timeout during file search

Include error details:
```json
{
  "status": "failed",
  "result": {
    "finding": "Analysis failed",
    "confidence": "low",
    "evidence": ["Error: Permission denied reading configuration files"],
    "values": []
  }
}
```

## Notes

- Applications often use multiple logging/telemetry tools (e.g., Serilog + Application Insights)
- List all detected frameworks in `values` array
- Prioritize most prominent framework in `finding`
- AOP frameworks are often used for logging interception - include in analysis
- Check both code and configuration for complete picture
