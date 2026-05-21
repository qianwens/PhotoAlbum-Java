---
name: generate-report-md
description: Generate report.md from assessment report data by running the generate-report-md.py script
---

# Generate Report Markdown

Generate a `report.md` file from the assessment output by running the included Python script.

## Execution

Run the following command:

```bash
python .github/modernize/assessment/engines/generate-report-md.py .github/modernize/assessment/reports/report-{reportId}
```

If the script is not at that path, look for it in the skill's own directory or copy it from there. The script file is `generate-report-md.py` bundled alongside this skill.

Alternatively, if the script is available in the current working directory or skill resources:

```bash
python generate-report-md.py .github/modernize/assessment/reports/report-{reportId}
```

## What the script does

1. Reads `report.json` (Java/.NET) or `js-assessment-report.md` (JS/TS) from the report directory
2. Checks for available fact files in the `facts/` subdirectory
3. Generates `report.md` in the same directory

## Prerequisites

- Python 3 must be available in the environment
- The versioned report directory must already exist with `report.json` or the JS/TS report file
- Fact files should already be copied to the `facts/` subdirectory (if architecture analysis was enabled)

## Input

The script takes one argument: the path to the versioned report directory, e.g.:
`.github/modernize/assessment/reports/report-20240615143052`

## Output

`report.md` is written to the same directory as the input report.

## Fallback

If Python is not available or the script fails, you may generate report.md manually following the same structure as the local CLI renderer produces. The key requirements are:
- Summary table with Total Issues (count of unique rule groups, NOT file occurrences)
- Application Information table (without Story points row)
- Issue sections with anchor IDs derived from titles (not rule IDs)
- Codebase Insights section linking to available fact files
- No "Back to aggregate report" link
