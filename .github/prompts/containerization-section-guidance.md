# Guidance: Generating Containerization Section for Migration Plans

## Purpose
The Containerization section provides essential information for packaging the application into a Docker container for deployment. It should focus only on building the application container, not testing infrastructure.

## Structure

### Section Header
```markdown
## Containerization
```

### Content Elements

1. **Purpose Statement**
   - One-sentence description of why containerization is needed
   - Example: "Package the application into a Docker container image for deployment to Azure."

2. **Build Instructions**
   - Base image and runtime requirements
   - Build stage configuration (if multi-stage build)
   - Key dependencies to include
   - Exposed ports
   - Build command
   - Verification steps

3. **Dockerfile Location**
   - Path to the Dockerfile in the repository
   - Indicate if existing or to be created

## Template

```markdown
## Containerization

**Purpose**: [One sentence describing the containerization goal]

**Build Instructions**:
- Base image: [runtime image, e.g., eclipse-temurin:8-jre]
- Build stage: [build image if multi-stage, e.g., maven:3.9.6-eclipse-temurin-8]
- Include [key dependencies] in classpath
- Expose port: [application port]
- Build command: `docker build -t [image-name]:[tag] .`
- Verify build: [verification steps]

**Dockerfile Location**: [path to Dockerfile]
```

## Example

```markdown
## Containerization

**Purpose**: Package the application into a Docker container image for deployment to Azure.

**Build Instructions**:
- Base image: `eclipse-temurin:8-jre` (Java 8 runtime)
- Build stage: `maven:3.9.6-eclipse-temurin-8` (compile application)
- Include PostgreSQL JDBC driver in classpath
- Expose port: `8080`
- Build command: `docker build -t photoalbum-java:latest .`
- Verify build: Run container locally and test dual-database connectivity

**Dockerfile Location**: `./Dockerfile` (existing)
```

## What NOT to Include

❌ **Do NOT include:**
- Docker Compose files for testing
- Database containers for local development
- Testing orchestration
- Development environment setup
- Multi-container configurations

✅ **DO include:**
- Application container build information only
- Production-relevant configuration
- Deployment-focused instructions

## Guidelines

1. **Keep it concise**: Focus on essential build information
2. **Be specific**: Include exact image names, versions, and commands
3. **Production-focused**: Information should be relevant for deployment, not development
4. **Verification**: Include simple verification steps to ensure the build works
5. **Reference existing files**: Point to Dockerfile location rather than including full content

## Variations by Project Type

### Java Spring Boot
```markdown
- Base image: `eclipse-temurin:[version]-jre`
- Build stage: `maven:[version]-eclipse-temurin-[version]`
- Include JDBC drivers for databases
- Expose port: `8080` (default Spring Boot port)
```

### Python Application
```markdown
- Base image: `python:[version]-slim`
- Install dependencies from `requirements.txt`
- Expose port: `8000` (or application-specific port)
```

### Node.js Application
```markdown
- Base image: `node:[version]-alpine`
- Build stage: `node:[version]` (for npm install)
- Expose port: `3000` (or application-specific port)
```

### .NET Application
```markdown
- Base image: `mcr.microsoft.com/dotnet/aspnet:[version]`
- Build stage: `mcr.microsoft.com/dotnet/sdk:[version]`
- Expose port: `80` or `443`
```

## Integration with Migration Plan

The Containerization section should appear:
- **After**: Code Migration section (features completed)
- **Before**: Deployment section (container is built before deployment)

Sequence:
1. Code Migration → Application code ready
2. Containerization → Application packaged
3. Deployment → Container deployed to cloud

## Example Workflow

```
Developer completes code migration
    ↓
Reads Containerization section
    ↓
Builds Docker image locally
    ↓
Verifies image runs correctly
    ↓
Proceeds to Deployment section
    ↓
Pushes image to container registry
    ↓
Deploys to cloud platform
```

---

**Document Version**: 1.0  
**Last Updated**: December 5, 2025  
**Purpose**: Guide for creating consistent, focused Containerization sections in migration plans
