---
name: validate-rulebook-compliance
description: Validate rulebook compliance by mapping rulebook rules to plan tasks
---

# Validate Rulebook Compliance

Map each rulebook rule to the tasks in the modernization plan and produce a compliance summary.

## User Input

- tasks-json-path (Mandatory): Path to the tasks.json file
- compliance-output-path (Mandatory): Path to write the compliance markdown summary

## Workflow

1. Read the tasks from ${tasks-json-path}
2. Read the rulebook files provided as attachments
3. For each rulebook rule, determine which task (if any) addresses it
4. Write a markdown summary to ${compliance-output-path} with the following format:

## Rulebook Compliance

| Rulebook | Rule | Status | Task |
|----------|------|--------|------|
| targets.md | brief rule summary | ✅ COVERED | 001 |
| policies.md | another rule | ❌ NOT COVERED | - |

**COVERED: X/Y  ·  NOT COVERED: Z/Y**

Include all rules from all rulebook files. Only write the markdown file, do not modify any other files.
