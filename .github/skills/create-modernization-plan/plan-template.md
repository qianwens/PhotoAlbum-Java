# Modernization Plan Template

Use this template to generate modernization plans for applications. Replace placeholders with actual values and customize content based on the specific modernization scenario.

**Planning Philosophy**:
- **Focus on GOALS, not implementation**: Describe WHAT needs to be achieved from the user's perspective
- **Skills define HOW**: All implementation details (frameworks, SDKs, libraries, code patterns, authentication methods) will be determined by the referenced skills
- **No assumptions**: Do not assume or specify any technical implementation approach in the plan - let skills handle all "how" decisions

---

# Modernization Plan: [Modernization Title]

**Project**: [Application Name]

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

**Purpose**: Describe the high-level modernization goals without technical details. Focus on business objectives and what will change.

**Template**:
> This migration [describe what is being migrated]. The application currently [describe current state]. The new architecture will:
>
> - [First key change and its business benefit]
> - [Second key change and its business benefit]
> - [Third key change and its business benefit]
>
> The migration follows [describe phased approach without technical specifics].

---

## Migration Impact Summary

**Purpose**: Create a simple table showing migration impact for each application and its affected services.
**Rule**: Each line should be limited to a maximum of 80 characters.
**Template**:
```
| Application | Original Service | New Azure Service | Authentication | Comments |
|-------------|------------------|-------------------|-------------|----------------|----------|
| [App Name]  | [Old Service]    | [Azure Service]   | [Auth method (Default is Managed Identity if user not specified)] | [User specified request for the migration] |
```

---

## Code

**Template**:
```markdown
### Task 1: [Task Name]

**Description**: [Brief description of what this task achieves from the user's perspective - focus on business/functional goals only]

**Requirements**:
  The original requirements from user input, leave it to empty if not specified from user input

**Environment Configration**:
  The environment Configration from user input (e.g. endpoint, access id), leave it to empty if not specified from user input

**App Scope**:
  The app folders that this task will operate
  If there are multiple apps to be migrate with the same skill, merge them in one task

**Skills**: 
  - Skill Name: [skill name must be used for the task, e.g., "migration-rabbitmq-to-servicebus"]
    - Skill Location: [Skill location: "project", "remote" and "builtin", "builtin" is renamed from "custom"]
  - Skill Name: [additional skill if needed]
    - Skill Location: [Skill location]

**Success Criteria**: Success Crtiera according to user input, if no input, user the default criteria
- [Pass Build: Yes (default) - Project must compile successfully after migration]
- [Generate New Unit Tests (Mock-based): No (default) - Create mock-based unit tests for newly added Azure integration code to ensure test coverage]
- [Generate New Integration Tests: No (default) - Create integration tests for Azure service interactions when requested:
  - If Azure resources are provided/accessible: Create tests that interact with actual Azure services
  - If no Azure resources are provided: Create integration tests with mocked Azure SDK clients using test containers or in-memory implementations where possible]
- [Pass Unit Tests: Yes (default) - All tests must pass; mock dependent Azure resources if not provided]
- [Pass New Integration Tests: No (default) - Integration tests must pass when generated:
  - With Azure resources: Tests validate actual Azure service connectivity and operations
  - Without Azure resources: Tests validate integration logic using mocked Azure clients, ensuring the integration layer works correctly]
- [Pass Security Compliance: No (default) - No known CVEs exist in project dependencies]


```

---

## Containerization

**Purpose**: Describe how to build the Docker container for deployment.

**IMPORTANT**: Only include Containerization section if the target deployment requires containerization (e.g., AKS, ACA) or if the user explicitly requested containerization. Skip this section for non-containerized deployments (e.g., App Service with code deployment). Only create Dockerfile for the application. Do not include Docker Compose for testing unless user requested.

**Template**:
```markdown
**Purpose**: [One sentence describing containerization goal]

**Dockerfile Location**: [path to Dockerfile, indicate if existing or to be created]
```

---

## Deployment

**Purpose**: Describe the target Azure service for deployment and the tooling to be used.

**IMPORTANT**: Only include deployment section if the user explicitly requested deployment.

**Template**:
```markdown
**Target Azure Service**: [Azure service name, e.g., Azure Container Apps, AKS, App Service]

**Resource Status**: [Specify if using existing resource or will create new service]

**Deployment Tool**: [az cli / bicep / terraform - default: bicep]

**Evaluation**: Run existing integration tests against the deployed endpoint to verify the deployment works correctly.
```

---

## Clarifications

**Purpose**: Document items that were not explicitly requested by the user but may be necessary or beneficial. Ask the user to confirm or provide input.

**Rule**: Only include this section if there are implicit dependencies, nice-to-have features, or ambiguities in the user's request.

**Template**:
```markdown
The following items were not explicitly requested but may be needed for a complete implementation:

1. **[Item Name]**: [Description of what needs clarification]
   - **Why needed**: [Explain the dependency or benefit]
   - **Options**: [List possible approaches or choices]
   - **Recommendation**: [Suggest a default if user doesn't respond]

```
