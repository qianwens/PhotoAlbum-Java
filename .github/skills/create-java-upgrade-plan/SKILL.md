---
name: create-java-upgrade-plan
description: Create an upgrade plan to migrate a Java project to latest LTS versions
---

# Create Upgrade Plan

Creates `tasks.json` (in `.metadata/` subdirectory) and `plan.md` for upgrading Java projects to target versions.

> **Supported**: Java upgrades only. .NET and other languages are not supported.

## ⚠️ CRITICAL: Do NOT Read Files

**Do NOT read any workspace files** (pom.xml, build.gradle, source code, etc.).

This plan may apply to multiple repositories not yet cloned. Generate a **generic plan** based solely on the user's prompt—never detect or mention "current versions."

## User Input

upgrade-prompt (Mandatory): The user's upgrade request (e.g., "Java 17", "Spring Boot 3.2", or "Upgrade to the latest LTS versions")
modernization-work-folder (Mandatory): The folder to save the upgrade plan

## Validation

**Valid requests**: Java/framework version upgrades, LTS migrations, dependency bumps  
**Invalid requests**: Feature additions, bug fixes, refactoring, containerization, deployment, non-Java languages (.NET, Python, etc.)

If invalid, output exactly:
```
ERROR: The provided prompt is not a valid upgrade request. Please specify a target version (e.g., 'Java 17', 'Spring Boot 3.2').
```

If unsupported language, output exactly:
```
ERROR: Only Java upgrades are supported. The requested language is not supported.
```
Then STOP—do not create files or ask for clarification.

## Workflow

1. **Parse request** → Extract target versions (defaults: Java 25, Spring Boot 4.x)
2. **Generate tasks.json** → Follow `tasks-schema.json` and `upgrade-plan-template.md`, and save it to `.metadata/tasks.json`
3. **Generate plan.md** → Brief overview of the upgrade plan

## Task Rules

- **Java Upgrade Task Guidelines**: You must refer to the ./java-upgrade-guideline.md for specific rules and guidelines when creating Java upgrade tasks.
- Create **only** `upgrade` type tasks
- Specify **target versions only**—never "from version X"
- Use `builtin` skills (e.g., `java-version-upgrade`)
- `successCriteria` values must be **strings** (`"true"`, not `true`)
- Set `status` to `"pending"`

## Output

Save to `${modernization-work-folder}/`:
- `.metadata/tasks.json` — Upgrade tasks per schema
- `plan.md` — Plan overview
