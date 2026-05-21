---
name: dotnet-upgrade-assessment
description: Runs .NET upgrade assessment only. Does not create plans, execute upgrades, or modify source code.
---

# .NET Upgrade Assessment Skill

This skill runs a .NET upgrade assessment using the MCP server. It performs ONLY assessment — no plans, no code changes, no upgrades.

## Input Parameters

- `workspace-path` (optional): Path to the project root containing the `.sln` or `.slnx` file. Defaults to `.` (current directory). For a repository with multiple solutions, pass the solution folder path.
- `target-framework` (optional): Target .NET framework version for upgrade (e.g., `net8`, `net9`, `net10`).

## Prerequisites — MCP Tool Availability Check

Before doing anything else, verify that ALL of the following MCP tools are available:
- `get_state`
- `get_scenarios`
- `initialize_scenario`
- `generate_dotnet_upgrade_assessment`

**If ANY of these tools are NOT available, STOP immediately.** Do NOT attempt to perform the assessment manually, do NOT analyze code yourself, and do NOT use alternative approaches. Simply report that the required MCP tools are unavailable and exit.

## Prerequisites — Locate the Report Directory

Before calling any MCP tools, find the versioned report directory that was created by the core assessment skill. The directory is at:

```
{workspace-path}/.github/modernize/assessment/reports/report-{reportId}/
```

Where `reportId` is a 14-digit timestamp in `yyyyMMddHHmmss` format (e.g., `20250514065424`). Find the latest one:

```bash
REPORT_DIR=$(ls -d {workspace-path}/.github/modernize/assessment/reports/report-[0-9]* 2>/dev/null | sort | tail -1)
```

If `REPORT_DIR` is empty (no `report-*` directory exists), report an error and STOP — the core assessment must run first.

## Prerequisites — ua-settings.json Setup

Create the settings file pointing to the discovered report directory:

```bash
mkdir -p {workspace-path}/.github/modernize
cat > {workspace-path}/.github/modernize/ua-settings.json << 'EOF'
{
  "outputPath": "{REPORT_DIR}"
}
EOF
export UA_SETTINGS_FILE_PATH="$(realpath {workspace-path}/.github/modernize/ua-settings.json)"
```

Replace `{workspace-path}` with the actual parameter value and `{REPORT_DIR}` with the discovered report directory path from the previous step.

## Execution Steps

Execute these steps IN ORDER. Do NOT skip any step. Do NOT deviate from this sequence.

### Step 1: Call `get_state()`

Call the MCP tool `get_state()` to initialize the workflow state.

### Step 2: Call `get_scenarios()`

Call the MCP tool `get_scenarios()`. From the response, identify the scenario for ".NET version upgrade" and note its `scenarioId`.

### Step 3: Call `initialize_scenario`

Call the MCP tool `initialize_scenario` with:
- `scenarioId`: the ID found in Step 2
- `description`: "Upgrade assessment for {solution file name}"

### Step 4: Find the solution file or folder

Look for `.sln` or `.slnx` files in `{workspace-path}`. Use the first one found.
If no solution file exists, use projects mode with `{workspace-path}` directly.

### Step 5: Call `generate_dotnet_upgrade_assessment`

Call `generate_dotnet_upgrade_assessment` on the selected solution, project, folder, or project list. Scope the assessment to the user's selected projects when the request is not solution-wide.
If `target-framework` was provided as an input parameter, pass it as `targetFramework` in the request as well.

For a solution-wide assessment:

```json
{
  "inputMode": "solution",
  "paths": "{absolute-path-to-solution}",
  "targetFramework": "net10.0"
}
```

For scoped project assessments, pass one or more absolute project paths as a semicolon-delimited string:

```json
{
  "inputMode": "projects",
  "paths": "{absolute-path-to-project-1};{absolute-path-to-project-2}",
  "targetFramework": "net10.0"
}
```

For folder assessments, pass the absolute folder path:

```json
{
  "inputMode": "folder",
  "paths": "{absolute-path-to-folder}",
  "targetFramework": "net10.0"
}
```



### Step 6: Verify scenario output files

Confirm that the MCP server wrote assessment files under `{REPORT_DIR}/scenarios/dotnet-version-upgrade/`. Expected files include:
- `assessment.json`
- `assessment.csv`
- `assessment.md`
- `scenario.json`
- `dependencies-health.json`

If the directory or files are missing, report what was generated and note the discrepancy.

### Step 7: Return the result

Report the assessment output file path (`{REPORT_DIR}/scenarios/dotnet-version-upgrade/`). STOP.

## Cleanup

After the assessment completes (whether successful or failed), remove the settings file:

```bash
rm -f {workspace-path}/.github/modernize/ua-settings.json
```

## Rules

- **ALL work MUST go through MCP tool calls.** Do NOT analyze code yourself.
- **Do NOT create plans or modify source files.** This is assessment only.
- **Do NOT ask for user input.** Run all steps in one session without pausing.
- **If a tool call fails, report the exact error.** Do NOT work around it or retry with different parameters.
- **Do NOT load additional skills or instructions.** Follow only the steps above.
- **Do NOT call `get_instructions`, `start_task`, `complete_task`, `break_down_task`, or any task/workflow management tools.** Those are for upgrade execution, not assessment.
- **Do NOT create git branches, commits, or source control operations.**
- **Do NOT read or analyze source code files.** The MCP tools handle all analysis internally.
