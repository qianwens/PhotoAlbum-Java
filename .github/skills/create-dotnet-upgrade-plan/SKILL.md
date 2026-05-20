---
name: create-dotnet-upgrade-plan
description: Creates a .NET upgrade plan (plan.md and tasks.json) for a repository. Analyzes the project to determine if a .NET version upgrade is needed and generates a structured upgrade task. Use when the user wants to create, generate, or prepare an upgrade/migration plan for a .NET project or solution.
---

# Create .NET Upgrade Plan

Generate an upgrade plan (`plan.md` and `.metadata/tasks.json`) for a .NET project or solution. This skill **only creates the plan** — it does not execute the upgrade. The upgrade execution is handled by the `modernize-dotnet-upgrade-engineer` agent during plan execution.

> **Supported**: .NET upgrades only. Other languages are not supported.

---

## CRITICAL: HEADLESS EXECUTION MODE

**This skill operates in fully autonomous headless mode. NO USER INTERACTION IS PERMITTED.**

### Non-Negotiable Rules

1. **NEVER stop, pause, or wait for user input** — not for confirmations, selections, reviews, or approvals
2. **NEVER ask "Would you like to proceed?"** — just proceed
3. **NEVER ask "Should I continue?"** — just continue
4. **ALWAYS complete the entire workflow** — from start to finish without interruption

---

## Input Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `upgrade-prompt` | Yes | The user's upgrade request (e.g., ".NET 10", "net10.0", "latest LTS") |
| `modernization-work-folder` | Yes | The folder to save the upgrade plan outputs |

---

## Input Validation

**Valid requests**: .NET version upgrades, LTS migrations, .NET Framework to modern .NET migrations

**Invalid requests**: Feature additions, bug fixes, refactoring, containerization, deployment, non-.NET languages

If invalid, output exactly and STOP:
```
ERROR: The provided prompt is not a valid upgrade request. Please specify a target version (e.g., '.NET 10', 'net10.0').
```

If unsupported language, output exactly and STOP:
```
ERROR: Only .NET upgrades are supported. The requested language is not supported.
```

---

## Guidelines

Refer to `dotnet-upgrade-guideline.md` for the rules on when to create an upgrade task, target version selection, and framework compatibility.

Key rules from the guideline:
- Only add an upgrade task if: the project is EOL, has Azure SDK incompatibility, or the user explicitly requests it
- Always upgrade to the **latest LTS** version unless the user specifies a different target
- Current latest LTS: **.NET 10** (`net10.0`)
- Create a **single** upgrade task that encompasses all necessary changes

---

## Workflow

### Step 1: Analyze the Project

Examine the project to determine:
1. **Current .NET version**: Read `.csproj` files to find `<TargetFramework>` or `<TargetFrameworks>`
2. **Project type**: Is it .NET Framework (requires SDK-style conversion), .NET Core, or modern .NET?
3. **Solution structure**: Is it a single project or a multi-project solution? List all projects.

### Step 2: Determine Upgrade Need

Apply the rules from `dotnet-upgrade-guideline.md`:
- If the project's .NET version is EOL → upgrade needed
- If the project targets .NET Framework < 4.6.2 (Azure SDK incompatibility) → upgrade needed
- If the user explicitly requests an upgrade → upgrade needed
- Otherwise → no upgrade needed, output: `ERROR: No upgrade is needed. The project is already on a supported .NET version.`

### Step 3: Generate plan.md

Create `plan.md` in `${modernization-work-folder}/` with:
- Source .NET version (detected from the project)
- Target .NET version (from user request or latest LTS)
- List of projects in the solution
- High-level description of what the upgrade entails (e.g., SDK-style conversion, TFM update, NuGet updates, API migration)

### Step 4: Generate tasks.json

Generate `tasks.json` in `${modernization-work-folder}/.metadata/` following `tasks-schema.json` and `upgrade-plan-template.md`.

Create a **single** upgrade task:

**Task Generation Rules:**

| Rule | Requirement |
|------|-------------|
| Task type | Use `upgrade` type |
| Task count | Exactly **one** upgrade task |
| Description | Include source and target .NET versions, project names |
| Reason | Include a **non-empty** `reason` field explaining why the upgrade is needed (for example: current .NET version is outdated or unsupported, target version standardization, required compatibility/security/support improvements) |
| Requirements | High-level summary of the upgrade scope (source version, target version, general areas affected). Do not include implementation details — the upgrade agent determines the specific steps. |
| Skills | Empty array `[]` — the upgrade agent handles execution internally |
| successCriteria values | Must be **strings** (`"true"`, not `true`) |
| status | Set to `"pending"` |
| id format | Use pattern `001-upgrade-dotnet-to-{target}` (e.g., `001-upgrade-dotnet-to-net10`) |

---

## Success Criteria

All of the following must be true:

- [ ] `plan.md` exists in `${modernization-work-folder}/`
- [ ] `tasks.json` exists in `${modernization-work-folder}/.metadata/`
- [ ] `plan.md` clearly states source and target .NET versions
- [ ] `tasks.json` follows schema with all required fields
- [ ] Exactly one upgrade task in tasks.json
- [ ] Workflow completed without user interaction

---

## Error Handling

| Problem | Solution |
|---------|----------|
| No .csproj found | Output `ERROR: No supported .NET project files (.csproj) found in the repository.` |
| Cannot determine current .NET version | Output `ERROR: Could not determine the current .NET version from project files.` |
| Project already on target version | Output `ERROR: The project is already on the target .NET version.` |

---

## Anti-Patterns (NEVER DO THESE)

| Don't | Do Instead |
|-------|------------|
| Stop to ask user for confirmation | Accept defaults and continue |
| Create multiple granular upgrade tasks | Create a single upgrade task |
| Wait for user review | Complete workflow, then show final results |
| Ask "Should I proceed?" | Just proceed |
