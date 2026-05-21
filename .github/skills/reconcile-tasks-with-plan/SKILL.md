---
name: reconcile-tasks-with-plan
description: Update tasks.json to match the current plan.md content without modifying plan.md
---

# Reconcile tasks.json with plan.md

This skill synchronizes tasks.json with plan.md when the plan has been manually updated.
It reads the current plan.md and tasks.json, detects differences, and rewrites tasks.json
to reflect the plan. **Do NOT modify plan.md** — it is the source of truth for task intent.

## User Input

- modernization-work-folder (Mandatory): The folder containing plan.md and .metadata/tasks.json
- language (Mandatory): The programming language of the project (java or dotnet)

## Workflow

1. **Read current state**: Read the following files from `${modernization-work-folder}`:
   - `plan.md` — the authoritative modernization plan (source of truth for task intent)
   - `.metadata/tasks.json` — the current structured task list (source of truth for execution state)

2. **Detect inconsistencies**: Compare plan.md against the tasks defined in .metadata/tasks.json. Look for:
   - Tasks described in plan.md that are missing from tasks.json
   - Tasks in tasks.json that are no longer mentioned in plan.md
   - Changes in task descriptions, requirements, scope, or ordering between the two files

3. **Update tasks.json**: If inconsistencies are found, rewrite .metadata/tasks.json to match plan.md:
   - Refer to the json schema tasks-schema.json for the correct task structure
   - Add new tasks that appear in plan.md but are missing from tasks.json
   - Remove tasks that are no longer described in plan.md
   - Update descriptions, requirements, or ordering to match plan.md
   - **Preserve task IDs**: For tasks that clearly map to existing entries, keep the same task ID
   - **Preserve execution state**: Do NOT reset tasks that already have a `status` of "success", "failed", or "skipped". Keep their `status`, `taskSummary`, and `successCriteriaStatus` unchanged
   - **Preserve metadata**: Keep the `metadata` block unchanged (same `planName`, `createdAt`, etc.)
   - Follow the same task breakdown rules and schema conventions as `create-modernization-plan`
   - Consult `java-upgrade-guideline.md` or `dotnet-upgrade-guideline.md` as applicable for upgrade tasks

4. **Skip if consistent**: If no meaningful inconsistencies are found between plan.md and tasks.json, do not write any files. Simply respond that no changes were needed.

## Important Notes

- **Never modify plan.md** — it is the user's manually edited source of truth
- Only modify tasks that are genuinely affected by changes in plan.md
- Each task must remain independently testable
- Do not change task types unless the plan.md clearly indicates a different type
