---
name: fact-xml-configs
description: Analyze XML configuration files usage in the application
---

# XML Configuration Files Analysis

## Purpose
Identify and catalog XML configuration files used by the application, including Spring context files, Hibernate configurations, web.xml, and other framework-specific XML files. This helps understand configuration management approach and migration requirements.

## Target Files/Locations
- **Spring Framework**: **/applicationContext*.xml, **/spring-*.xml, **/*-context.xml, **/beans.xml
- **Hibernate ORM**: **/hibernate.cfg.xml, **/*.hbm.xml
- **Java EE/Jakarta EE**: **/web.xml, **/ejb-jar.xml, **/persistence.xml
- **MyBatis**: **/mybatis-config.xml, **/*-mapper.xml
- **Log4j**: **/log4j.xml, **/log4j2.xml
- **Maven**: **/pom.xml
- **Build configs**: **/build.xml (Ant), **/ivy.xml
- **Application configs**: **/config/**/*.xml, **/conf/**/*.xml

## Example Patterns to Search
- Spring XML config with bean definitions
- Hibernate mapping files (.hbm.xml)
- MyBatis SQL mapper files
- web.xml servlet configurations
- persistence.xml JPA configurations
- log4j.xml or log4j2.xml logging configurations

## Analysis Steps

### 1. Search for Spring XML Configuration Files
```
Use Glob tool to find Spring config files:
- **/applicationContext*.xml
- **/spring-*.xml
- **/*-context.xml
- **/beans.xml
- **/META-INF/spring/**/*.xml

For each file found:
- Use Read tool to examine first 50 lines
- Check for <beans> root element
- Identify bean definitions, imports, property placeholders
- Note component-scan or annotation-config presence
```

### 2. Search for Hibernate Configuration Files
```
Use Glob tool to find Hibernate files:
- **/hibernate.cfg.xml
- **/*.hbm.xml

For each file:
- Read to identify database dialect
- Check for entity mappings
- Note session factory configuration
- Identify connection pool settings
```

### 3. Search for Java EE/Jakarta EE Deployment Descriptors
```
Use Glob tool to find Java EE files:
- **/WEB-INF/web.xml
- **/META-INF/ejb-jar.xml
- **/META-INF/persistence.xml
- **/META-INF/application.xml

Analyze each:
- Servlet/filter configurations (web.xml)
- JPA entity configurations (persistence.xml)
- EJB declarations (ejb-jar.xml)
```

### 4. Search for MyBatis Configuration Files
```
Use Glob tool:
- **/mybatis-config.xml
- **/*-mapper.xml
- **/sqlmap/**/*.xml

Check for:
- SQL mapper namespaces
- Select/insert/update/delete statements
- Result maps and parameter maps
```

### 5. Search for Logging XML Configurations
```
Use Glob tool:
- **/log4j.xml
- **/log4j2.xml
- **/logback.xml

Analyze:
- Appender configurations
- Logger level settings
- Output patterns
```

### 6. Count and Categorize All XML Files
```
Use Bash tool to count XML files:
find . -type f -name "*.xml" -not -path "*/target/*" -not -path "*/.git/*" | wc -l

Use Grep to identify XML configuration files (vs data files):
- Pattern: "<beans|<configuration|<hibernate-configuration|<web-app|<persistence"
- Files: **/*.xml
- Output mode: files_with_matches

Categorize by framework:
- Spring: beans, context namespaces
- Hibernate: hibernate-configuration, hibernate-mapping
- Java EE: web-app, ejb-jar, persistence-unit
- MyBatis: mapper namespace
- Logging: log4j:configuration, configuration (logback)
```

### 7. Analyze XML Complexity and Size
```
For each significant XML file:
- Use Read to get line count
- Check for external entity references
- Identify property placeholders (${...})
- Note XSD/DTD schema references
- Check for profiles or conditional configurations
```

## Confidence Determination

### High Confidence Criteria
Clear evidence of XML configuration usage with detailed findings:
- ✅ Multiple XML configuration files identified with specific purposes
- ✅ Framework-specific XML files present (Spring, Hibernate, etc.)
- ✅ Valid XML structure confirmed with proper root elements
- ✅ Bean/entity/mapper definitions clearly visible
- ✅ Relationship between files understood (imports, includes)

**Examples**:
- "Found 23 Spring XML config files with 450+ bean definitions across applicationContext.xml and imported files"
- "Hibernate configuration with 15 .hbm.xml entity mapping files and hibernate.cfg.xml"
- "Web application with web.xml (Servlet 3.1) and 8 Spring context XML files"

### Medium Confidence Criteria
Partial evidence or incomplete information:
- ⚠️ XML files found but unclear purpose or usage
- ⚠️ Config files present but may be legacy/unused
- ⚠️ XML files exist alongside annotation-based config (hybrid approach)
- ⚠️ Limited XML usage (only logging or build configs)
- ⚠️ XML files in resources but no clear loading mechanism

**Examples**:
- "Spring XML files found but @Configuration classes also present (hybrid setup)"
- "Hibernate .hbm.xml files exist but JPA annotations also used"
- "XML files present but timestamps suggest not recently modified"

### Low Confidence Criteria
Weak or ambiguous evidence:
- ⚠️ Only build tool XML files (pom.xml, build.xml)
- ⚠️ No framework-specific XML configurations
- ⚠️ XML files are data files, not configuration
- ⚠️ Test resources only, no production configs
- ⚠️ Commented-out or example XML files

**Examples**:
- "Only pom.xml found, no application XML configs"
- "XML files in test resources only, production uses properties/YAML"
- "Sample XML files in documentation directory, not active configs"

### Not Applicable Criteria
When XML configuration analysis doesn't apply:
- ❌ Pure annotation-based configuration (Spring Boot @Configuration)
- ❌ Configuration via properties/YAML files only
- ❌ Non-Java application (.NET, Node.js, Python)
- ❌ Library project with no configuration requirements
- ❌ Modern application using Java Config exclusively

**Examples**:
- "Spring Boot application using only @Configuration classes and application.yml"
- ".NET Core application, XML config analysis not applicable"
- "Node.js application with JSON configuration only"

## Output Format

**CRITICAL**: Use the `write_assessment_result` tool (not just output JSON text).

```json
{
  "input_name": "XML Configs",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Clear 1-2 sentence summary of XML configuration usage}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Number and types of XML files found}",
      "{Specific file paths for major configs}",
      "{Framework identifications from XML content}",
      "{Configuration patterns observed}"
    ],
    "values": [
      "{Framework: Spring, Hibernate, MyBatis, etc.}",
      "{File count by type}",
      "{Key configuration file names}",
      "{Schema versions or namespaces}"
    ]
  },
  "execution_time_seconds": {elapsed_time},
  "timestamp": "{ISO 8601 timestamp}"
}
```

**Finding Examples**:
- ✅ Good: "Application uses Spring XML configuration with 18 context files defining 250+ beans, including applicationContext.xml as root config"
- ✅ Good: "Hibernate-based persistence with hibernate.cfg.xml and 12 .hbm.xml entity mapping files for database layer"
- ✅ Good: "Web application with web.xml (Servlet 3.0), 5 Spring XML contexts, and MyBatis mapper files for SQL"
- ✅ Good: "No XML configuration detected - application uses Spring Boot with annotation-based @Configuration classes"
- ❌ Bad: "XML files found"
- ❌ Bad: "Configuration exists"

**Evidence Examples**:
- ✅ Good: "applicationContext.xml at src/main/resources/ with 45 bean definitions and 3 imported context files"
- ✅ Good: "15 Hibernate mapping files (*.hbm.xml) in src/main/resources/mappings/ for entity persistence"
- ✅ Good: "web.xml at WEB-INF/ defines 8 servlets and 12 filters with Spring DispatcherServlet"
- ✅ Good: "23 MyBatis mapper XML files in resources/mappers/ with SQL definitions"
- ❌ Bad: "Found XML files in project"
- ❌ Bad: "Spring configuration present"

## Error Handling

### 1. No XML Configuration Found
- Report finding as "No XML configuration files detected"
- Set confidence to high if thorough search confirmed absence
- Note alternative config approaches if detected (annotations, properties, YAML)

### 2. Mixed Configuration Approaches
- Report both XML and alternative approaches found
- Set confidence to medium
- List what's configured via XML vs annotations/properties
- Example: "Hybrid approach: Spring XML for legacy beans, @Configuration for new services"

### 3. Too Many XML Files
- If >100 XML files found, categorize and sample
- Provide statistics by category
- Focus detailed analysis on framework config files
- Note if many are data files vs configuration files

### 4. Tool Failures
- If Glob returns too many results, refine with more specific patterns
- If Read fails on corrupted XML, note the file but continue
- After 3 retries on critical operations, report partial results with caveats

### 5. Invalid/Malformed XML
- Note files that appear to be XML but fail parsing
- Don't let malformed files block analysis
- Report count of valid vs invalid XML files found

## Example Complete Analysis

**Scenario**: Java Spring MVC application with XML-based configuration

**Steps Executed**:
1. Glob for Spring XML: Found 18 files (applicationContext.xml + 17 imported)
2. Read applicationContext.xml: Confirmed Spring 4.3 with bean definitions
3. Glob for Hibernate: Found hibernate.cfg.xml and 12 .hbm.xml files
4. Glob for Java EE: Found web.xml in WEB-INF/
5. Count total XML: 45 XML files in project (excluding target/)
6. Categorized: 18 Spring, 13 Hibernate, 1 Java EE, 8 MyBatis, 2 logging, 3 Maven

**Result**:
```json
{
  "input_name": "XML Configs",
  "analysis_method": "LLM",
  "status": "success",
  "result": {
    "finding": "Application heavily uses XML configuration with 18 Spring context files, 13 Hibernate mappings, and Java EE web.xml for a traditional XML-based architecture",
    "confidence": "high",
    "evidence": [
      "applicationContext.xml at src/main/resources/ with <beans> root and 45 bean definitions",
      "18 Spring XML files with imports: data-context.xml, security-context.xml, service-context.xml, etc.",
      "hibernate.cfg.xml and 12 entity mapping files (*.hbm.xml) in resources/mappings/",
      "web.xml at WEB-INF/web.xml defines DispatcherServlet and 8 filters (Servlet API 3.0)",
      "8 MyBatis mapper XML files in resources/mappers/ with SQL queries",
      "log4j.xml configuration for logging with 5 appenders"
    ],
    "values": [
      "Spring Framework (XML-based config, Spring 4.3 schema)",
      "Hibernate ORM (12 .hbm.xml entity mappings)",
      "Java EE Servlet 3.0 (web.xml)",
      "MyBatis (8 mapper files)",
      "45 total XML configuration files",
      "Log4j XML configuration"
    ]
  },
  "execution_time_seconds": 32.8,
  "timestamp": "2026-02-28T10:18:15Z"
}
```
