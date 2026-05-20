---
name: fact-servlet-container
description: Identify servlet container requirements and version
---

# Servlet Container Analysis

## Purpose
Identify the servlet container (application server) requirements for the application, including Servlet API version, container-specific features, and deployment model. This helps determine migration compatibility and modernization path.

## Target Files/Locations
- **Deployment descriptors**: **/WEB-INF/web.xml, **/META-INF/weblogic.xml, **/META-INF/jboss-web.xml
- **Build files**: **/pom.xml, **/build.gradle, **/build.gradle.kts
- **Configuration**: **/application.properties, **/application.yml
- **Server configs**: **/server.xml, **/context.xml (Tomcat), **/standalone.xml (JBoss/WildFly)
- **Java source**: **/*Servlet.java, **/*Filter.java, **/*Listener.java

## Example Patterns to Search
- **Servlet API**: `javax.servlet`, `jakarta.servlet`, `ServletContext`, `HttpServlet`
- **Servlet version**: `<web-app version="3.1"`, `version="4.0"`, `version="5.0"`
- **Container-specific**: `weblogic`, `jboss`, `wildfly`, `tomcat`, `websphere`, `glassfish`
- **Server dependencies**: `provided` scope for servlet-api, tomcat-embed, wildfly-swarm
- **Annotations**: `@WebServlet`, `@WebFilter`, `@WebListener`, `@MultipartConfig`

## Analysis Steps

### 1. Analyze web.xml Deployment Descriptor
```
Use Glob to find web.xml:
- **/WEB-INF/web.xml
- **/META-INF/web.xml

If found, use Read to examine:
- <web-app> version attribute (2.3, 2.4, 2.5, 3.0, 3.1, 4.0, 5.0, 6.0)
- XSD/DTD namespace for Servlet version
  - Java EE 5 (Servlet 2.5): java.sun.com/xml/ns/javaee
  - Java EE 6-7 (Servlet 3.0-3.1): xmlns.jcp.org/xml/ns/javaee
  - Jakarta EE 8+ (Servlet 4.0+): jakarta.ee/xml/ns/jakartaee
- Servlet definitions and mappings
- Filter configurations
- Container-specific elements
```

### 2. Check Build Dependencies for Servlet API
```
Use Glob to find build files:
- **/pom.xml
- **/build.gradle
- **/build.gradle.kts

Use Read or Grep to search for:
Maven (pom.xml):
- <artifactId>servlet-api</artifactId>
- <artifactId>javax.servlet-api</artifactId>
- <artifactId>jakarta.servlet-api</artifactId>
- <version>3.1.0</version>, <version>4.0.0</version>, <version>5.0.0</version>
- <scope>provided</scope> (indicates external container)

Gradle (build.gradle):
- providedCompile 'javax.servlet:javax.servlet-api:3.1.0'
- compileOnly 'jakarta.servlet:jakarta.servlet-api:5.0.0'

Check for embedded container dependencies:
- spring-boot-starter-web (embedded Tomcat)
- tomcat-embed-core
- jetty-server
- undertow-core
```

### 3. Search for Container-Specific Configuration
```
Use Glob to find container configs:
- **/META-INF/weblogic.xml (Oracle WebLogic)
- **/META-INF/jboss-web.xml (JBoss/WildFly)
- **/META-INF/glassfish-web.xml (GlassFish)
- **/META-INF/geronimo-web.xml (Apache Geronimo)
- **/WEB-INF/ibm-web-ext.xml (IBM WebSphere)

If found, this indicates container-specific features/requirements
```

### 4. Search for Servlet/Filter Implementations
```
Use Grep to find servlet code:
Pattern: "extends\\s+HttpServlet|implements\\s+Servlet|implements\\s+Filter"
Files: **/*.java
Context: -B 2 -A 5

Use Grep to find servlet annotations:
Pattern: "@WebServlet|@WebFilter|@WebListener|@MultipartConfig"
Files: **/*.java
Context: -B 1 -A 3

Analyze:
- Count of servlets/filters
- Use of Servlet 3.0+ annotations vs web.xml
- Async servlet support (@WebServlet(asyncSupported=true))
```

### 5. Check for Spring Boot Embedded Container
```
Use Grep in pom.xml or build.gradle:
Pattern: "spring-boot-starter-web|spring-boot-starter-tomcat|spring-boot-starter-jetty|spring-boot-starter-undertow"

If found:
- This is embedded container (not external)
- Check application.properties for server configuration
  - server.port
  - server.servlet.context-path
  - server.tomcat.* (if Tomcat)

Use Glob for Spring Boot config:
- **/application.properties
- **/application.yml
```

### 6. Identify Container Version from Dependencies
```
Parse Maven/Gradle files for exact versions:
- javax.servlet-api: 2.5, 3.0, 3.1 (Java EE)
- jakarta.servlet-api: 4.0 (Jakarta EE 8), 5.0 (Jakarta EE 9), 6.0 (Jakarta EE 10)

Match to Servlet API specifications:
- Servlet 2.5 = Java EE 5 (Tomcat 6, JBoss 5)
- Servlet 3.0 = Java EE 6 (Tomcat 7, JBoss 7, GlassFish 3)
- Servlet 3.1 = Java EE 7 (Tomcat 8, WildFly 8-10, WebLogic 12c)
- Servlet 4.0 = Java EE 8 / Jakarta EE 8 (Tomcat 9, WildFly 14+)
- Servlet 5.0 = Jakarta EE 9 (Tomcat 10, WildFly 22+)
- Servlet 6.0 = Jakarta EE 10 (Tomcat 10.1+, WildFly 27+)
```

### 7. Check for Container-Specific Features
```
Use Grep to search for container-specific APIs:
- WebLogic: "weblogic\\..*|WorkManager|JMS"
- JBoss/WildFly: "org\\.jboss|org\\.wildfly|EJB"
- WebSphere: "com\\.ibm\\.websphere"
- Tomcat: "org\\.apache\\.catalina|org\\.apache\\.tomcat"

These indicate tight coupling to specific containers
```

## Confidence Determination

### High Confidence Criteria
Clear and definitive evidence of servlet container requirements:
- ✅ web.xml present with explicit version attribute
- ✅ Servlet API dependency with specific version in build file
- ✅ Container-specific configuration files found
- ✅ Servlet/Filter implementations found in code
- ✅ Clear deployment model (embedded vs external container)

**Examples**:
- "Web application requires Servlet 3.1 API (Java EE 7) based on web.xml version='3.1' and javax.servlet-api:3.1.0 dependency"
- "Spring Boot application with embedded Tomcat 9.0.65 (Servlet 4.0) from spring-boot-starter-web:2.7.3"
- "WebLogic-specific deployment with weblogic.xml and WorkManager configuration - requires Oracle WebLogic 12c+"

### Medium Confidence Criteria
Partial evidence or inferred information:
- ⚠️ Servlet API dependency present but no web.xml (annotation-based config)
- ⚠️ Container type inferred from Spring Boot starter but version unclear
- ⚠️ Servlet code found but no explicit version indicators
- ⚠️ Legacy web.xml without version attribute
- ⚠️ Mixed signals (multiple container dependencies)

**Examples**:
- "Servlet 3.0+ usage inferred from @WebServlet annotations, but no explicit version in dependencies"
- "Spring Boot with default embedded container (likely Tomcat) but version not specified"
- "Servlet implementations found but build file doesn't declare servlet-api dependency explicitly"

### Low Confidence Criteria
Weak or ambiguous evidence:
- ⚠️ No web.xml or servlet annotations found
- ⚠️ Servlet API in transitive dependencies only
- ⚠️ Container type unclear or multiple possibilities
- ⚠️ Test code has servlet dependencies but main code doesn't
- ⚠️ Comments reference servlets but no actual implementation

**Examples**:
- "Servlet API appears in dependency tree but no servlet code found"
- "No clear servlet container indicators - may be non-web application"
- "Test dependencies include servlet-api but unclear if production code uses it"

### Not Applicable Criteria
When servlet container analysis doesn't apply:
- ❌ Non-web application (standalone, batch, CLI tool)
- ❌ REST API using JAX-RS without servlets (Jersey, RESTEasy standalone)
- ❌ Pure reactive application (Spring WebFlux on Netty)
- ❌ Different platform (.NET, Node.js, Python)
- ❌ Library/framework project (no executable component)

**Examples**:
- "Spring Boot application using WebFlux and Netty - no servlet container required"
- "Standalone Java application with no web components"
- "Node.js Express application - servlet analysis not applicable"

## Output Format

**CRITICAL**: Use the `write_assessment_result` tool (not just output JSON text).

```json
{
  "input_name": "Servlet Container",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Clear 1-2 sentence summary of servlet container requirements}",
    "confidence": "high|medium|low",
    "evidence": [
      "{web.xml version or absence}",
      "{Servlet API dependency with version}",
      "{Container-specific files or features}",
      "{Deployment model (embedded/external)}",
      "{Container type identified}"
    ],
    "values": [
      "{Servlet API version (e.g., 3.1, 4.0, 5.0)}",
      "{Java EE / Jakarta EE version}",
      "{Container type and version (if known)}",
      "{Number of servlets/filters}",
      "{Container-specific features used}"
    ]
  },
  "execution_time_seconds": {elapsed_time},
  "timestamp": "{ISO 8601 timestamp}"
}
```

**Finding Examples**:
- ✅ Good: "Application requires Servlet 3.1 container (Java EE 7) deployed to external WebLogic 12c server with WebLogic-specific WorkManager configuration"
- ✅ Good: "Spring Boot application with embedded Tomcat 9.0.65 (Servlet 4.0 / Jakarta EE 8) managed by spring-boot-starter-web"
- ✅ Good: "Modern Jakarta EE 9 application requiring Servlet 5.0 container (WildFly 22+, Tomcat 10+) with 8 servlets and 5 filters"
- ✅ Good: "Non-web application - no servlet container required (standalone Spring Boot with WebFlux)"
- ❌ Bad: "Uses servlets"
- ❌ Bad: "Container required"

**Evidence Examples**:
- ✅ Good: "web.xml at WEB-INF/web.xml declares version='3.1' with Java EE 7 namespace"
- ✅ Good: "javax.servlet-api:3.1.0 with <scope>provided</scope> in pom.xml"
- ✅ Good: "weblogic.xml found with WorkManager 'default' configuration"
- ✅ Good: "spring-boot-starter-web:2.7.3 includes tomcat-embed-core:9.0.65"
- ✅ Good: "5 servlets using @WebServlet annotations (Servlet 3.0+ feature)"
- ❌ Bad: "web.xml exists"
- ❌ Bad: "Container dependency found"

## Error Handling

### 1. No Servlet Evidence Found
- Check if this is a web application at all
- Search for alternative web frameworks (JAX-RS, Spring WebFlux)
- Report as "not_applicable" if truly not a web app
- If web app with no servlet evidence: low confidence "Unable to determine container requirements"

### 2. Mixed Servlet API Versions
- Report all versions found with locations
- Set confidence to medium
- Note potential migration status: "Project in transition from javax.servlet to jakarta.servlet"

### 3. Embedded vs External Container Confusion
- Check for spring-boot packaging (jar vs war)
- Spring Boot jar = embedded, war = external
- Report both possibilities if unclear

### 4. Tool Failures
- If Grep fails on large pom.xml, use Read with offset/limit
- If XML parsing issues, try grep for version patterns
- After 3 retries, report with caveats

## Example Complete Analysis

**Scenario**: Traditional Java EE web application on WebLogic

**Steps Executed**:
1. Glob for web.xml: Found WEB-INF/web.xml
2. Read web.xml: version="3.1", Java EE 7 namespace
3. Read pom.xml: javax.servlet-api:3.1.0 with provided scope
4. Glob for container configs: Found META-INF/weblogic.xml
5. Grep for servlets: Found 8 servlet classes, 5 filters
6. Grep for container features: Found WorkManager references

**Result**:
```json
{
  "input_name": "Servlet Container",
  "analysis_method": "LLM",
  "status": "success",
  "result": {
    "finding": "Application requires Servlet 3.1 (Java EE 7) container, specifically Oracle WebLogic 12c, with WebLogic-specific features including WorkManager and JMS integration",
    "confidence": "high",
    "evidence": [
      "web.xml at WEB-INF/web.xml with version='3.1' and Java EE 7 namespace (xmlns.jcp.org/xml/ns/javaee)",
      "javax.servlet-api:3.1.0 dependency with <scope>provided</scope> in pom.xml",
      "weblogic.xml at META-INF/weblogic.xml with WorkManager configuration",
      "8 servlet implementations: AuthServlet, MainServlet, UploadServlet, etc.",
      "5 filter implementations including CharacterEncodingFilter and AuthenticationFilter",
      "WebLogic-specific API usage: weblogic.jms.* and weblogic.servlet.*"
    ],
    "values": [
      "Servlet API 3.1",
      "Java EE 7",
      "Oracle WebLogic 12c (minimum)",
      "8 servlets, 5 filters",
      "WebLogic WorkManager 'default-workmanager'",
      "WAR packaging for external deployment"
    ]
  },
  "execution_time_seconds": 28.4,
  "timestamp": "2026-02-28T10:22:38Z"
}
```
