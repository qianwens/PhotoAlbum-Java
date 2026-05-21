---
name: generate-report-html
description: Generate report.html from assessment report data by running the generate-report-html.py script
---

# Generate Report HTML

Generate a self-contained `report.html` file from the assessment output by running the included Python script.

## Execution

Run the following command:

```bash
python .github/modernize/assessment/engines/generate-report-html.py .github/modernize/assessment/reports/report-{reportId}
```

If the script is not at that path, look for it in the skill's own directory or copy it from there. The script file is `generate-report-html.py` bundled alongside this skill.

Alternatively, if the script is available in the current working directory or skill resources:

```bash
python generate-report-html.py .github/modernize/assessment/reports/report-{reportId}
```

## What the script does

1. Reads `report.json` (Java/.NET) or `js-assessment-report.md` (JS/TS) from the report directory
2. Reads fact files from the `facts/` subdirectory (if present)
3. Generates `report.html` in the same directory

## Prerequisites

- Python 3 must be available in the environment
- The versioned report directory must already exist with `report.json` or the JS/TS report file
- Fact files should already be copied to the `facts/` subdirectory (if architecture analysis was enabled)

## Input

The script takes one argument: the path to the versioned report directory, e.g.:
`.github/modernize/assessment/reports/report-20240615143052`

## Output

`report.html` is written to the same directory as the input report.

## Fallback

If Python is not available or the script fails, you may generate report.html manually following the same structure as the local CLI renderer produces. The key requirements are:
- Self-contained HTML with embedded CSS and JavaScript
- SVG donut charts for issue summary
- Interactive expandable issue rows with file locations
- Fact tabs with Mermaid diagram support
- No "Back to aggregate dashboard" link
