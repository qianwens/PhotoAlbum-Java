---
name: security-assessment-merge
description: Merge CVE and CWE security assessment results into a unified security report and update report.json
---

# Security Assessment: Merge and Report

## Role

You are a **security assessment aggregator**. Your task is to read all CVE and CWE result files produced by earlier security skills, merge them into a unified security assessment report, and inject the findings into `report.json`.

> **Important:** You are a data aggregator, NOT an analyzer. Do NOT re-scan the codebase. Your sole responsibility is to read, normalize, merge, and write the security findings that were already produced by the CVE and CWE assessment skills.

## Working Directory

All security assessment input and output files are located under:

```
.github/modernize/assessment/engines/security/
```

All file paths in this skill are relative to this directory unless otherwise noted.

## Objective

1. Read all security assessment result files from the `.github/modernize/assessment/engines/security/` directory
2. Normalize CVE and CWE findings into a unified format
3. Generate `security-assessment.json` (machine-readable merged report) in the same directory
4. Generate `security-assessment.md` (human-readable markdown report) in the same directory
5. Inject a `"security"` array into the existing `report.json`

## Instructions

### Step 1: Read CVE Results

Read the CVE result file at `.github/modernize/assessment/engines/security/cve-assessment-result.json`.

This file is a **flat JSON array** where each element has:
```json
{
  "id": "CVE-2024-xxxx",
  "name": "Summary",
  "status": "FOUND",
  "category": "CVE",
  "severity": "critical|high|medium|low",
  "storyPoint": 1,
  "evidence": {
    "files": ["pom.xml:42"],
    "explanation": "Markdown description..."
  }
}
```

Only include entries where `status` is `"FOUND"`.

**Filter by minimum CVE severity:** The minimum severity threshold is provided in the assessment prompt instructions. Only include CVE findings whose severity meets or exceeds the specified threshold. The severity order from lowest to highest is: `low` < `medium` < `high` < `critical`. Exclude findings with unknown or missing severity. If no threshold was specified in the prompt, default to `high`.

If the file does not exist or is empty, treat CVE findings as an empty list.

### Step 2: Read CWE Results

Read all CWE result files matching `.github/modernize/assessment/engines/security/result-cwe-*.json`.

Each CWE file uses a **wrapper format**:
```json
{
  "input_name": "CWE - Category Name",
  "status": "success",
  "result": {
    "values": [
      {
        "id": "CWE-79",
        "name": "Cross-site Scripting",
        "status": "FOUND",
        "category": "Injection Attacks",
        "severity": "optional",
        "storyPoint": 8,
        "description": "The product does not neutralize or incorrectly neutralizes user-controllable input before it is placed in output that is used as a web page that is served to other users.",
        "evidence": {
          "files": ["src/Controller.java"],
          "explanation": "Description..."
        }
      }
    ]
  }
}
```

Navigate to `result.values` in each file and extract entries where `status` is `"FOUND"`.

If no CWE files exist, treat CWE findings as an empty list.

### Step 3: Build the Unified Security Findings Array

Transform all FOUND CVE and CWE items into the unified format:

```json
{
  "id": "CVE-2024-xxxx or CWE-79",
  "title": "Human-readable title",
  "category": "CVE or CWE category (e.g., Injection Attacks)",
  "severity": "mandatory|optional|potential",
  "description": "Detailed description",
  "evidence": {
    "files": ["path/to/file.java"],
    "explanation": "Why this was flagged"
  },
  "storyPoint": 1
}
```

For **CVE findings**: Map `name` → `title`, use `explanation` as both `description` and `evidence.explanation`. **Map the raw CVE severity to assessment severity levels:**
- `critical` or `high` → `mandatory`
- `medium` → `optional`
- `low` or unknown → `potential`

For **CWE findings**: Map `name` → `title`, map `severity` → `severity` (already in assessment format), map `storyPoint` → `storyPoint`, map `description` → `description`, use `explanation` as `evidence.explanation`.

### Step 4: Calculate Summary Statistics

Count:
- `totalFindings`: Total number of FOUND CVE + CWE items
- `cveCount`: Number of CVE findings
- `cweCount`: Number of CWE findings
- `bySeverity`: Count of findings grouped by severity (`mandatory`, `optional`, `potential`)
- `byCategory`: Count of findings grouped by category (`CVE`, `Injection Attacks`, etc.)
- `totalRulesAssessed`: Total number of CWE checklist items across all `.github/modernize/assessment/engines/security/result-cwe-*.json` files (both FOUND and NOT_FOUND)
- `rulesPassed`: `totalRulesAssessed - cweCount`

### Step 5: Write security-assessment.json

Write the full merged report to `.github/modernize/assessment/engines/security/security-assessment.json`:

```json
{
  "GeneratedAt": "2026-04-09T12:00:00.0000000Z",
  "ProjectPath": ".",
  "Summary": {
    "TotalFindings": 5,
    "CveCount": 2,
    "CweCount": 3,
    "BySeverity": { "mandatory": 3, "optional": 1, "potential": 1 },
    "ByCategory": { "CVE": 2, "Injection Attacks": 2, "Code Quality": 1 },
    "TotalRulesAssessed": 59,
    "RulesPassed": 56
  },
  "CveFindings": [
    {
      "Id": "CVE-2024-xxxx",
      "Name": "Vulnerability Title",
      "Category": "CVE",
      "Severity": "mandatory",
      "StoryPoint": 1,
      "Description": "...",
      "Files": ["pom.xml:42"],
      "Explanation": "..."
    }
  ],
  "CweFindings": [
    {
      "Id": "CWE-79",
      "Name": "Cross-site Scripting",
      "Category": "Injection Attacks",
      "Severity": "optional",
      "StoryPoint": 8,
      "Description": "...",
      "Files": ["src/Controller.java"],
      "Explanation": "..."
    }
  ]
}
```

### Step 6: Write security-assessment.md

Write a human-readable markdown report to `.github/modernize/assessment/engines/security/security-assessment.md`:

```markdown
# Security Assessment Report

**Generated:** <timestamp>

## Summary

| Metric | Count |
|--------|-------|
| Total Findings | N |
| CVE Vulnerabilities | N |
| CWE Vulnerabilities | N |
| Total Rules Assessed | N |
| Rules Passed | N |

### By Severity

| Severity | Count |
|----------|-------|
| mandatory | N |
| optional | N |
| potential | N |

## CVE Findings (Dependency Vulnerabilities)

### CVE-2024-xxxx: Title
- **Severity:** mandatory
- **Story Points:** 1
- **Files:** pom.xml:42

<explanation>

## CWE Findings (Code-Level Vulnerabilities)

### CWE-79: Cross-site Scripting
- **Category:** Injection Attacks
- **Severity:** optional
- **Story Points:** 8
- **Files:** src/Controller.java

<explanation>
```

If there are no findings at all, write:
```markdown
## No security vulnerabilities found.

The assessment did not detect any CVE or CWE vulnerabilities in the codebase.
```

### Step 7: Merge into report.json

The `report.json` file lives in a versioned report directory:

```
.github/modernize/assessment/reports/report-{reportId}/report.json
```

where `{reportId}` is a `yyyyMMddHHmmss` timestamp (e.g., `20260410120000`). This directory is created by the main assessment skill.

**Step 7a: Locate report.json**

Find the latest versioned report directory by listing directories matching the `report-*` pattern and sorting in descending order (newest first):

```bash
REPORTS_DIR=".github/modernize/assessment/reports"
REPORT_DIR=$(ls -d "$REPORTS_DIR"/report-* 2>/dev/null | sort -r | head -n 1)

if [ -n "$REPORT_DIR" ] && [ -f "$REPORT_DIR/report.json" ]; then
  echo "Found report.json at: $REPORT_DIR/report.json"
else
  echo "Warning: No versioned report directory found under $REPORTS_DIR"
fi
```

**Step 7b: Merge security findings into report.json**

**Use `jq` for safe JSON manipulation** — do NOT manually rewrite report.json.

Write the unified findings array to a temporary file, then merge:

```bash
SECURITY_DIR=".github/modernize/assessment/engines/security"

# Write the unified findings array
cat > "$SECURITY_DIR/unified-findings.json" << 'SECURITY_EOF'
[
  ... unified findings array from Step 3 ...
]
SECURITY_EOF

# Merge into report.json using jq
if [ -n "$REPORT_DIR" ] && [ -f "$REPORT_DIR/report.json" ] && command -v jq &> /dev/null; then
  jq --argjson sec "$(cat "$SECURITY_DIR/unified-findings.json")" '. + {"security": $sec}' "$REPORT_DIR/report.json" > "$REPORT_DIR/report.json.tmp" && mv "$REPORT_DIR/report.json.tmp" "$REPORT_DIR/report.json"
elif [ -n "$REPORT_DIR" ] && [ -f "$REPORT_DIR/report.json" ]; then
  # Fallback without jq: use python
  python3 -c "
import json
report_path = '$REPORT_DIR/report.json'
with open(report_path, 'r') as f: report = json.load(f)
with open('$SECURITY_DIR/unified-findings.json', 'r') as f: security = json.load(f)
report['security'] = security
with open(report_path, 'w') as f: json.dump(report, f, indent=2)
" 2>/dev/null || echo "Warning: Could not merge security into report.json (jq and python3 unavailable)"
else
  echo "Warning: report.json not found — skipping merge. The standalone security-assessment.json is still valid."
fi

# Clean up temp file
rm -f "$SECURITY_DIR/unified-findings.json"
```

**Step 7c: Handle missing report.json**

If no `report-*` directory or `report.json` exists (e.g., AppCAT was not run or failed), create a minimal stub in a new versioned directory:

```bash
if [ -z "$REPORT_DIR" ] || [ ! -f "$REPORT_DIR/report.json" ]; then
  REPORT_ID=$(date -u +"%Y%m%d%H%M%S")
  REPORT_DIR="$REPORTS_DIR/report-$REPORT_ID"
  mkdir -p "$REPORT_DIR"
  cat > "$REPORT_DIR/report.json" << STUB_EOF
{
  "metadata": {
    "id": "$REPORT_ID",
    "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%S.0000000Z")",
    "note": "Security-only report (AppCAT was not run or failed)"
  },
  "security": $(cat "$SECURITY_DIR/unified-findings.json" 2>/dev/null || echo "[]")
}
STUB_EOF
  echo "Created stub report at: $REPORT_DIR/report.json"
fi
```

## Error Handling

- If no security result files exist at all, write empty reports (`security-assessment.json` with zero findings, `security-assessment.md` with "No vulnerabilities found")
- If a CWE result file is malformed, skip it and continue with the rest
- If the `report.json` merge fails, log a warning but do NOT fail the overall task — the standalone `security-assessment.json` is still valid
- Always produce all three output files (`security-assessment.json`, `security-assessment.md`, and the merged `report.json`)
