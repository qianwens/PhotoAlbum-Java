---
name: validate-playbook-compliance
description: Validate playbook compliance by mapping playbook rules to plan tasks
---

# Validate Playbook Compliance

Map each playbook rule to the tasks in the modernization plan and produce a compliance summary.

## User Input

- tasks-json-path (Mandatory): Path to the tasks.json file
- compliance-output-path (Mandatory): Path to write the compliance markdown summary

## Workflow

1. Read the tasks from ${tasks-json-path}
2. Read the playbook files provided as attachments
3. For each playbook rule, determine which task (if any) addresses it
4. Write a markdown summary to ${compliance-output-path} with the following format:

## Playbook Compliance

| Playbook | Rule | Status | Task |
|----------|------|--------|------|
| targets.md | brief rule summary | ✅ COVERED | 001 |
| policies.md | another rule | ❌ NOT COVERED | - |

**COVERED: X/Y  ·  NOT COVERED: Z/Y**

Include all rules from all playbook files. Only write the markdown file, do not modify any other files.
