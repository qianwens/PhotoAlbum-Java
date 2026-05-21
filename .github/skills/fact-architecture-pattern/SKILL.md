---
name: fact-architecture-pattern
description: Identify the application architecture pattern
---

# Architecture Pattern Analysis

## Purpose
Determine the architectural pattern used in the application: Monolith, Microservices, Layered, Event-Driven, MVC, etc.

## Analysis Strategy

This SKILL performs a comprehensive analysis of project structure, dependencies, and code patterns to identify the architecture.

## Analysis Steps

### 1. Project Structure Analysis

**Check for Microservices Indicators:**
```bash
# Use Glob to search for service directories
**/services/**/
**/microservices/**/
**/apps/**/
```

**Check for Monolith Indicators:**
- Single deployable unit
- All code in one project/module

### 2. Configuration & Infrastructure Analysis

**Search for Service Discovery (Microservices):**
```bash
# Use Grep to find service discovery patterns
Pattern: "eureka|consul|etcd|kubernetes|k8s|service\.discovery"
Files: **/*.{yaml,yml,json,xml,properties,config}
```

**Search for API Gateway (Microservices):**
```bash
Pattern: "zuul|gateway|kong|ambassador|istio|envoy|traefik"
Files: **/*.{yaml,yml,json,xml,properties,pom.xml,build.gradle,package.json}
```

**Search for Message Brokers (Event-Driven):**
```bash
Pattern: "kafka|rabbitmq|activemq|azure\.servicebus|aws\.sqs|redis\.pub"
Files: **/*.{yaml,yml,json,xml,properties,config}
```

### 3. Code Pattern Analysis

**MVC Pattern Detection:**
```bash
# Search for controllers
Pattern: "@Controller|@RestController|ApiController|[Controller]|class.*Controller"
Files: **/*.{java,cs,py,js,ts}

# Search for models
Glob: **/models/**/*.*, **/entities/**/*.*, **/domain/**/*.*

# Search for views
Glob: **/views/**/*.*, **/templates/**/*.*
```

**Layered Architecture Detection:**
```bash
# Search for layer separation
Glob: **/controller*/**/*, **/service*/**/*, **/repository*/**/*, **/dao*/**/*.*

Pattern: "@Service|@Repository|@Component|[Service]|interface.*Repository"
Files: **/*.{java,cs}
```

**Event-Driven Pattern Detection:**
```bash
Pattern: "@EventHandler|@KafkaListener|@RabbitListener|EventEmitter|publish\(|subscribe\("
Files: **/*.{java,cs,js,ts,py}
```

### 4. Deployment Configuration Analysis

**Container Orchestration (Microservices):**
```bash
Glob: **/kubernetes/**/*.yaml, **/k8s/**/*.yaml, **/helm/**/*.*
Glob: docker-compose*.{yml,yaml}
```

**Check docker-compose for multiple services:**
```bash
Pattern: "services:\n(.*\n){3,}"
Files: docker-compose*.{yml,yaml}
```

## Analysis Decision Tree

1. **If multiple deployable services detected** → Microservices Architecture
   - Evidence: Multiple service directories, service discovery, API gateway

2. **If message brokers + event handlers detected** → Event-Driven Architecture
   - Evidence: Kafka/RabbitMQ configs, event listeners, pub/sub patterns

3. **If clear MVC structure detected** → MVC Architecture
   - Evidence: Controllers, Models, Views directories

4. **If layer separation detected (but single deployment)** → Layered Monolith
   - Evidence: Controller/Service/Repository layers in single project

5. **If single project with no clear separation** → Simple Monolith
   - Evidence: All code in one directory, minimal structure

## Confidence Levels

- **High**: Clear indicators from multiple sources (structure + config + code patterns)
- **Medium**: Some indicators present but mixed signals
- **Low**: Limited evidence, manual inspection recommended

## Output Format

After analysis, call the MCP tool:

```javascript
write_assessment_result({
  resultJson: JSON.stringify({
    input_name: "Architecture Pattern",
    analysis_method: "Hybrid",  // Code + LLM analysis
    status: "success",  // or "not_applicable" or "failed"
    result: {
      finding: "Microservices Architecture",
      confidence: "high",  // high, medium, or low
      evidence: [
        "Found 5 service directories: user-service, order-service, payment-service, notification-service, gateway-service",
        "docker-compose.yml defines 5 separate services",
        "Found Eureka service discovery configuration",
        "API Gateway detected: Zuul configuration in gateway-service/application.yml"
      ],
      values: ["Microservices", "Service Discovery", "API Gateway"],
      architecture_details: {
        pattern: "Microservices",
        service_count: 5,
        has_service_discovery: true,
        has_api_gateway: true,
        has_message_broker: false
      }
    },
    execution_time_seconds: 3.5,
    timestamp: new Date().toISOString()
  }),
  assessmentDir: variables.assessment_dir
});
```

## Example Patterns by Technology Stack

### Java/Spring Boot

**Microservices:**
- `@EnableEurekaClient`, `@EnableDiscoveryClient`
- `spring-cloud-starter-netflix-eureka`
- Multiple `@SpringBootApplication` classes

**Layered Monolith:**
- Single `@SpringBootApplication`
- Packages: `controller`, `service`, `repository`, `entity`

### .NET/ASP.NET Core

**Microservices:**
- Multiple `.csproj` files with `<OutputType>Exe</OutputType>`
- `Microsoft.Extensions.Http.Polly` (service-to-service calls)
- `Steeltoe.Discovery.Eureka`

**MVC:**
- Single `.csproj` with `Microsoft.AspNetCore.Mvc`
- Folders: `Controllers`, `Models`, `Views`

### Node.js/Express

**Microservices:**
- Multiple `package.json` files in subdirectories
- `express-gateway`, `consul` dependencies

**Layered:**
- Single `package.json`
- Folders: `routes`, `controllers`, `services`, `models`

### Python

**Microservices:**
- Multiple `app.py` or `main.py` files
- `nameko`, `flask-consul` dependencies

**Event-Driven:**
- `kafka-python`, `pika` (RabbitMQ), `celery`
- Event handler decorators

## Not Applicable Scenarios

Return `status: "not_applicable"` if:
- Project is not an application (library, CLI tool only)
- Insufficient code to determine architecture
- Non-standard structure that doesn't fit patterns

## Error Handling

Return `status: "failed"` if:
- Unable to access project files
- Critical analysis error occurred

Include error details in the result.

## Notes

- Architecture can be hybrid (e.g., Layered + Event-Driven)
- Include all applicable patterns in `values` array
- Prioritize most dominant pattern in `finding`
- If uncertain between patterns, use `confidence: "medium"` and explain in evidence
