---
name: migration-eclipse-project-to-maven-project
description: Migrate current project from eclipse project to maven project
---

# eclipse-project-to-maven-project

## Overview

Migrate current project from eclipse project to maven project

## Knowledge Base Content

* KB ID: eclipse-project-to-maven-project
* Title: Migrate eclipse project to maven project
* Description: This KB provides guidelines for migrating eclipse project to maven project
* Content: 
# Migration Considerations: Eclipse Project to Maven Project

## Overview

This document provides specific migration considerations when migrating from an Eclipse project structure to a Maven project structure. Use these considerations with the INITIAL_PROMPT_TEMPLATE.md to create a project-specific migration plan.

## Key Components to Replace

- Convert Eclipse project structure to Maven standard directory layout
- Replace Eclipse .project and .classpath files with Maven pom.xml
- Migrate library dependencies from .classpath to Maven dependencies
- Convert Eclipse build configuration to Maven build plugins
- Transform Eclipse source folders to Maven source directories
- Migrate Eclipse project settings to Maven properties and plugin configurations

## Common Patterns to Migrate

### 1. Project Structure Transformation

**Eclipse Project Structure (Common Patterns):**
```
project-root/
├── .project                    # Eclipse project configuration
├── .classpath                  # Eclipse classpath configuration
├── .settings/                  # Eclipse project settings
│   ├── org.eclipse.jdt.core.prefs
│   ├── org.eclipse.core.resources.prefs
│   └── org.eclipse.m2e.core.prefs
├── src/                        # Main source directory
│   └── com/example/...         # Package structure
├── test/                       # Test source directory (if exists)
├── resources/                  # Resources directory (if exists)
├── lib/                        # External JAR dependencies
├── WebContent/                 # Web application content (for web projects)
│   ├── WEB-INF/
│   │   ├── web.xml
│   │   └── lib/               # Web-specific libraries
│   ├── META-INF/
│   └── index.jsp
└── build/                      # Eclipse build output
```

**Maven Standard Structure (Target):**
```
project-root/
├── pom.xml                     # Maven project configuration
├── src/
│   ├── main/
│   │   ├── java/              # Java source files
│   │   ├── resources/         # Non-Java resources
│   │   └── webapp/            # Web application resources (for WAR)
│   │       ├── WEB-INF/
│   │       │   └── web.xml
│   │       ├── META-INF/
│   │       └── index.jsp
│   └── test/
│       ├── java/              # Test Java source files
│       └── resources/         # Test resources
└── target/                    # Maven build output
```

### 2. Eclipse Configuration File Analysis

#### .project File Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
    <name>ProjectName</name>
    <comment></comment>
    <projects>
    </projects>
    <buildSpec>
        <buildCommand>
            <name>org.eclipse.jdt.core.javabuilder</name>
            <arguments>
            </arguments>
        </buildCommand>
        <buildCommand>
            <name>org.eclipse.wst.common.project.facet.core.builder</name>
            <arguments>
            </arguments>
        </buildCommand>
    </buildSpec>
    <natures>
        <nature>org.eclipse.jdt.core.javanature</nature>
        <nature>org.eclipse.wst.common.project.facet.core.nature</nature>
        <nature>org.eclipse.wst.jsdt.core.jsNature</nature>
    </natures>
</projectDescription>
```

#### .classpath File Analysis
```xml
<?xml version="1.0" encoding="UTF-8"?>
<classpath>
    <classpathentry kind="src" path="src"/>
    <classpathentry kind="src" path="test"/>
    <classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-11"/>
    <classpathentry kind="lib" path="lib/commons-lang3-3.12.0.jar"/>
    <classpathentry kind="lib" path="lib/junit-4.13.2.jar"/>
    <classpathentry kind="lib" path="lib/servlet-api-2.5.jar"/>
    <classpathentry kind="con" path="org.eclipse.jdt.USER_LIBRARY/MyLibraries"/>
    <classpathentry kind="output" path="build"/>
</classpath>
```

### 3. Migration Mapping Patterns

#### Basic pom.xml Template
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>project-name</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>jar</packaging> <!-- or war for web projects -->

    <name>Project Name</name>
    <description>Migrated from Eclipse project</description>

    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <failOnMissingWebXml>false</failOnMissingWebXml>
    </properties>

    <dependencies>
        <!-- Dependencies migrated from .classpath -->
    </dependencies>

    <build>
        <plugins>
            <!-- Build plugins for compilation and packaging -->
        </plugins>
    </build>
</project>
```

#### Source Directory Mapping

**Eclipse .classpath entries:**
```xml
<classpathentry kind="src" path="src"/>
<classpathentry kind="src" path="test"/>
<classpathentry kind="src" path="resources"/>
```

**Maven pom.xml configuration:**
```xml
<build>
    <sourceDirectory>src/main/java</sourceDirectory>
    <testSourceDirectory>src/test/java</testSourceDirectory>
    <resources>
        <resource>
            <directory>src/main/resources</directory>
        </resource>
    </resources>
    <testResources>
        <testResource>
            <directory>src/test/resources</directory>
        </testResource>
    </testResources>
</build>
```

#### Dependency Migration

**Eclipse .classpath library entries:**
```xml
<classpathentry kind="lib" path="lib/commons-lang3-3.12.0.jar"/>
<classpathentry kind="lib" path="lib/junit-4.13.2.jar"/>
<classpathentry kind="lib" path="lib/servlet-api-2.5.jar"/>
```

**Maven pom.xml dependencies:**
```xml
<dependencies>
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
        <version>3.12.0</version>
    </dependency>
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.13.2</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>servlet-api</artifactId>
        <version>2.5</version>
        <scope>provided</scope>
    </dependency>
</dependencies>
```

#### JRE/JDK Version Mapping

**Eclipse .classpath JRE entry:**
```xml
<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-11"/>
```

**Maven pom.xml compiler configuration:**
```xml
<properties>
    <maven.compiler.source>11</maven.compiler.source>
    <maven.compiler.target>11</maven.compiler.target>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <source>11</source>
                <target>11</target>
                <encoding>UTF-8</encoding>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### 4. Web Project Migration

#### Eclipse Dynamic Web Project

**Eclipse .project with web nature:**
```xml
<natures>
    <nature>org.eclipse.jdt.core.javanature</nature>
    <nature>org.eclipse.wst.common.project.facet.core.nature</nature>
    <nature>org.eclipse.wst.jsdt.core.jsNature</nature>
</natures>
```

**Maven WAR packaging:**
```xml
<packaging>war</packaging>

<properties>
    <failOnMissingWebXml>false</failOnMissingWebXml>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-war-plugin</artifactId>
            <version>3.3.2</version>
            <configuration>
                <webXml>src/main/webapp/WEB-INF/web.xml</webXml>
            </configuration>
        </plugin>
    </plugins>
</build>
```

#### Web Content Directory Migration

**Eclipse WebContent structure:**
```
WebContent/
├── WEB-INF/
│   ├── web.xml
│   └── lib/
├── META-INF/
├── css/
├── js/
└── index.jsp
```

**Maven webapp structure:**
```
src/main/webapp/
├── WEB-INF/
│   └── web.xml
├── META-INF/
├── css/
├── js/
└── index.jsp
```

### 5. Special Eclipse Features Migration

#### User Libraries

**Eclipse .classpath user library:**
```xml
<classpathentry kind="con" path="org.eclipse.jdt.USER_LIBRARY/MyLibraries"/>
```

**Maven dependency management:**
```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>my-bom</artifactId>
            <version>1.0.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

#### Eclipse Variable References

**Eclipse .classpath variable:**
```xml
<classpathentry kind="var" path="M2_REPO/org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar"/>
```

**Maven repository management:**
```xml
<repositories>
    <repository>
        <id>central</id>
        <url>https://repo1.maven.org/maven2</url>
    </repository>
</repositories>
```

#### Eclipse Project References

**Eclipse .project dependencies:**
```xml
<projects>
    <project>shared-library</project>
    <project>common-utils</project>
</projects>
```

**Maven multi-module structure:**
```xml
<!-- Parent pom.xml -->
<modules>
    <module>shared-library</module>
    <module>common-utils</module>
    <module>main-project</module>
</modules>

<!-- In main-project/pom.xml -->
<dependencies>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>shared-library</artifactId>
        <version>${project.version}</version>
    </dependency>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>common-utils</artifactId>
        <version>${project.version}</version>
    </dependency>
</dependencies>
```

### 6. Build and Deployment Configuration

#### Eclipse Build Path and Output

**Eclipse build output:**
```xml
<classpathentry kind="output" path="build"/>
```

**Maven build configuration:**
```xml
<build>
    <directory>target</directory>
    <outputDirectory>target/classes</outputDirectory>
    <testOutputDirectory>target/test-classes</testOutputDirectory>

    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-clean-plugin</artifactId>
            <version>3.3.1</version>
        </plugin>
    </plugins>
</build>
```

#### Eclipse Annotation Processing

**Eclipse .settings/org.eclipse.jdt.core.prefs:**
```properties
org.eclipse.jdt.core.compiler.processAnnotations=enabled
org.eclipse.jdt.core.compiler.generated.annotation.enabled=true
```

**Maven annotation processing:**
```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <annotationProcessorPaths>
                    <path>
                        <groupId>org.mapstruct</groupId>
                        <artifactId>mapstruct-processor</artifactId>
                        <version>1.5.5.Final</version>
                    </path>
                </annotationProcessorPaths>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### 7. Eclipse-specific Files to Handle

#### Files to Remove After Migration
- `.project` - Eclipse project descriptor
- `.classpath` - Eclipse classpath configuration
- `.settings/` directory - Eclipse IDE settings
- `build/` directory - Eclipse build output
- `lib/` directory - Manual JAR dependencies (after converting to Maven dependencies)

#### Files to Keep and Possibly Modify
- `src/` directory contents - Source code (may need to move to Maven structure)
- `WebContent/` or `web/` - Web content (move to `src/main/webapp`)
- `resources/` - Resource files (move to `src/main/resources`)
- Documentation files - README, LICENSE, etc.

### 8. Common Migration Challenges

#### Challenge 1: Non-Standard Source Directories

**Eclipse custom source folders:**
```xml
<classpathentry kind="src" path="generated-sources"/>
<classpathentry kind="src" path="custom-src"/>
```

**Maven configuration:**
```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>build-helper-maven-plugin</artifactId>
            <version>3.4.0</version>
            <executions>
                <execution>
                    <id>add-source</id>
                    <phase>generate-sources</phase>
                    <goals>
                        <goal>add-source</goal>
                    </goals>
                    <configuration>
                        <sources>
                            <source>generated-sources</source>
                            <source>custom-src</source>
                        </sources>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

#### Challenge 2: Unknown Library Dependencies

For JAR files in the `lib/` directory where Maven coordinates are unknown:

1. **Identify the library:**
   ```bash
   # Check MANIFEST.MF inside the JAR
   unzip -q -c library.jar META-INF/MANIFEST.MF

   # Search Maven Central
   # Use online tools like: https://search.maven.org/
   ```

2. **If not available in public repositories:**
   ```xml
   <!-- Install to local repository -->
   <!-- mvn install:install-file -Dfile=lib/library.jar -DgroupId=com.unknown -DartifactId=unknown-lib -Dversion=1.0 -Dpackaging=jar -->

   <dependency>
       <groupId>com.unknown</groupId>
       <artifactId>unknown-lib</artifactId>
       <version>1.0</version>
   </dependency>
   ```

#### Challenge 3: Eclipse-specific Build Steps

**Eclipse builders in .project:**
```xml
<buildSpec>
    <buildCommand>
        <name>org.eclipse.wst.validation.validationbuilder</name>
    </buildCommand>
    <buildCommand>
        <name>org.eclipse.jdt.core.javabuilder</name>
    </buildCommand>
</buildSpec>
```

**Maven equivalent plugins:**
```xml
<build>
    <plugins>
        <!-- Validation -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-checkstyle-plugin</artifactId>
            <version>3.3.0</version>
        </plugin>

        <!-- Compilation -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
        </plugin>
    </plugins>
</build>
```

### 9. Update .gitignore File

**⚠️ IMPORTANT: This is a critical step that must be included in your migration plan**

**Migration planning checklist**:
- ✅ Locate existing .gitignore file or create a new one
- ✅ Add maven related entries in .gitignore file

**Maven related .gitignore entries**:
   ```
   # Maven specific
   target/
   .mvn/wrapper/maven-wrapper.jar
   !**/src/main/**/target/
   !**/src/test/**/target/
   ```

### 10. Migration Steps Summary

1. **Analyze Eclipse Project Structure**
   - Review .project and .classpath files
   - Identify source directories, dependencies, and build configuration
   - Document any custom Eclipse settings

2. **Create Maven Directory Structure**
   - Create standard Maven directory layout
   - Move source files to appropriate Maven directories
   - Move resources to Maven resource directories

3. **Create pom.xml**
   - Set basic project information (groupId, artifactId, version)
   - Configure Java version and encoding
   - Add dependencies based on .classpath analysis

4. **Migrate Dependencies**
   - Identify Maven coordinates for JAR dependencies
   - Add dependencies to pom.xml with appropriate scopes
   - Handle any libraries not available in public repositories

5. **Configure Build Plugins**
   - Add Maven compiler plugin with appropriate Java version
   - Add packaging plugins (war plugin for web projects)
   - Configure any special build requirements

6. **Test the Migration**
   - Run `mvn clean compile` to verify compilation
   - Run `mvn test` to verify tests work
   - Run `mvn package` to verify packaging
   - Verify the application runs correctly

7. **Clean Up**
   - Remove Eclipse-specific files (.project, .classpath, .settings)
   - Remove lib directory after confirming all dependencies are in Maven
   - Update `.gitignore` file
   - Update documentation and build instructions

### 11. Verification Checklist

- [ ] Project compiles successfully with `mvn clean compile`
- [ ] Tests run successfully with `mvn test`
- [ ] Project packages successfully with `mvn package`
- [ ] All external dependencies are resolved from Maven repositories
- [ ] No Eclipse-specific files remain in the project
- [ ] Application functionality is preserved
- [ ] Build output matches expected artifacts
- [ ] IDE integration works (can import as Maven project)
- [ ] Source directory structure follows Maven conventions
- [ ] All resources are properly included in the build

This migration transforms an Eclipse project into a standard Maven project that can be built from the command line and imported into any IDE that supports Maven projects.

## File and Directory Movement Best Practices

When restructuring projects during Eclipse to Maven migration, follow these practices to ensure successful migration:

1. **⚠️ Important** Always use move operations instead of copy operations
   - **Use**: `mv`
   - **Avoid**: `cp`, `robocopy`, `xcopy`
   - **Reason**: Move operations ensure original files are automatically removed, preventing forgotten cleanup that can cause build conflicts and duplicate files

2. **⚠️ Important** Avoid moving parent folder to child folder
   - **Problem**: Moving a parent directory directly into its own subdirectory can cause infinite loops or file system errors
   - **Solution**: Rename the original folder first, then make sure maven related directories exist, then move file and direcory
   - **Example**: Instead of `mv src/* src/main/java/`, use `mv src src_temp && mkdir -p src/main/java && mv src_temp/* src/main/java/`
