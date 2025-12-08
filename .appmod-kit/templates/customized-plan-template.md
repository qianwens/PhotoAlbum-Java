# Migration Plan Template

Use this template to generate migration plans for applications. Replace placeholders with actual values and customize content based on the specific migration scenario.

---

# Migration Plan: [Migration Title]

**Project**: [Application Name]  
**Migration Strategy**: [e.g., code + local verify + azure verify]  
**Date**: [Date]  
**Branch**: [Git branch name]

---

## Technical Framework

**Purpose**: Document the application's current technology stack to provide context for the migration.

**Template**:
```markdown
- **Language**: [Programming language and version, e.g., Java 11, Python 3.9, .NET 6]
- **Framework**: [Application framework and version, e.g., Spring Boot 2.7.18, Django 4.2, ASP.NET Core 6.0]
- **Build Tool**: [Build system, e.g., Maven 3.9, Gradle 8.0, npm]
- **Database**: [Current database, e.g., Oracle 19c, PostgreSQL 14, SQL Server 2019]
- **Key Dependencies**: [Major libraries/frameworks, e.g., Spring Data JPA, Hibernate, Entity Framework]
```

---

## Overview

**Purpose**: Describe the high-level migration goals without technical details. Focus on business objectives and what will change.

**Template**:
> This migration [describe what is being migrated]. The application currently [describe current state]. The new architecture will:
> 
> - [First key change and its business benefit]
> - [Second key change and its business benefit]
> - [Third key change and its business benefit]
> 
> The migration follows [describe phased approach without technical specifics].

---

## Services

**Purpose**: List Azure services and resources required for the migration with their resource identifiers.

**Template**:
```markdown
### [Service Name 1]
- **Resource ID**: [Azure resource ID or indicate "to be provisioned"]
- **Server Name**: [FQDN if applicable]
- **Database/Container/etc**: [specific resource details]
- **Authentication**: [auth method]
- **Purpose**: [what this service will be used for]

### [Service Name 2]
- **Resource ID**: [Azure resource ID or indicate "to be provisioned"]
- **Purpose**: [what this service will be used for]
```

---

## Architecture Design

**Purpose**: Draft a Mermaid diagram showing the new architecture with impacted components only.

**Template**:
```mermaid
graph TB
    subgraph "[Component Name] - [Modified/New/Existing]"
        [Define components and their relationships]
    end
    
    [Add styling to distinguish new, modified, and unchanged components]
    
    style [new-components] fill:#90EE90,stroke:#333,stroke-width:3px
    style [modified-components] fill:#FFD700,stroke:#333,stroke-width:3px
    style [azure-services] fill:#4da6ff,stroke:#333,stroke-width:2px
```

**Legend Template**:
- 🟢 **Green**: New components to be created
- 🟡 **Yellow**: Existing components to be modified
- **Gray**: Unchanged components

---

## Code Migration

**Purpose**: Break down migration work into testable features without modifying unimpacted code.

**Breakdown Rules**:
- Create features ONLY based on what the user explicitly requested - do not infer or add implicit features
- One feature per user-requested capability (configuration + implementation)
- Each feature can be evaluated with integration tests
- Do not add tests for unimpacted code or existing functionality unless user requested
- Steps describe brief changes, unit test goals, and integration test goals without specific file names

**Template**:
```markdown
### Feature: [Feature Name]

**Description**: [Brief description of what this feature migrates]

**Steps**:
1. **Code**: [Brief summary of code changes without file names]
2. **Unit Test**: [What the unit tests will verify, create mock test if no azure resource provided]
3. **Integration Test**: [What the integration tests will validate]
```

---

## Containerization

**Purpose**: Describe how to build the Docker container for deployment.

**Rule**: Only create Dockerfile for the application. Do not include Docker Compose for testing unless user requested.

**Template**:
```markdown
**Purpose**: [One sentence describing containerization goal]

**Dockerfile Location**: [path to Dockerfile, indicate if existing or to be created]
```

---

## Deployment

**Purpose**: Describe the deployment script and what it does, provision only if resources not provided, and specify integration tests to run.

**Template**:
```markdown
**Deployment Script**: [script name] (update or create)

**Script Actions**:
- [Action 1: build application]
- [Action 2: build and tag Docker image]
- [Action 3: push to container registry]
- Provision [Azure resources] (only if not provided by user)
- [Action 4: configure environment variables]
- [Action 5: deploy to Azure service]

**Integration Test**: [Describe which integration tests to run against deployed endpoint]
```

