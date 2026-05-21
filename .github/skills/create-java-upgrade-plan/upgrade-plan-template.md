# Upgrade Plan Template

> **Important**: Specify only TARGET versions—never "current" or "from" versions. Do NOT read project files.

## Schema Rules

- Use `upgradeTask` type from `tasks-schema.json`
- `successCriteria` values: **strings** (`"true"`, `"false"`)
- `skills.location`: `"builtin"` | `"project"` | `"remote"`
- `status`: `"pending"`

## Example: tasks.json
{
  "description": "Upgrade plan to migrate project to latest LTS versions",
  "tasks": [
    {
      "type": "upgrade",
      "id": "001-upgrade-java-spring-boot",
      "description": "Upgrade to Java 25 and Spring Boot 4.x",
      "requirements": "Upgrade JDK to 25, Spring Boot to 4.x, Spring Framework to 7.x, and migrate javax.* to jakarta.* if needed",
      "environmentConfiguration": null,
      "skills": [{ "name": "java-version-upgrade", "location": "builtin" }],
      "successCriteria": {
        "passBuild": "true",
        "generateNewUnitTests": "false",
        "passUnitTests": "true"
      },
      "status": "pending"
    }
  ],
  "metadata": {
    "planName": "upgrade-to-lts",
    "projectName": "application",
    "language": "java",
    "createdAt": "2026-02-06T00:00:00.000Z",
    "version": "1.0"
  }
}
```

## Example: plan.md

```markdown
# Upgrade Plan

## Overview
Upgrade to latest LTS versions.

## Tasks
See the .metadata/tasks.json for detailed task breakdown.
```
