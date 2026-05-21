---
name: validate-assessment-rulebook-compliance
description: Validate that assessment findings cover rulebook source technologies and patterns
---

# Validate Assessment Rulebook Compliance

Check whether the assessment detected the source technologies and patterns defined in the rulebook.

## User Input

- assessment-findings-path (Mandatory): Path to the pre-processed assessment findings JSON file
- compliance-output-path (Mandatory): Path to write the compliance markdown summary

## Workflow

1. Read the assessment findings from ${assessment-findings-path}. This is a JSON array of objects with `ruleId`, `title`, and `description` fields representing issues detected during assessment.
2. Read the rulebook files provided as attachments (targets.md, policies.md).
3. Extract each source technology, pattern, or constraint mentioned in the rulebook files.
4. For each rulebook item, determine whether the assessment findings contain a rule that detects or covers it. Use semantic matching — the rule description does not need to be an exact match, but must clearly relate to the same technology or pattern.
5. Write a markdown summary to ${compliance-output-path} with the following format:

## Assessment Rulebook Coverage

| Rulebook | Source Technology/Pattern | Status | Evidence (Rule ID) |
|----------|--------------------------|--------|-------------------|
| targets.md | brief technology/pattern summary | ✅ DETECTED | matching-rule-id |
| policies.md | another pattern | ❌ NOT DETECTED | - |

**DETECTED: X/Y · NOT DETECTED: Z/Y**

## Rules

- Only include source technologies and patterns from the rulebook — do not include target recommendations.
- A rulebook item is DETECTED if at least one assessment rule clearly relates to detecting that technology or pattern.
- If multiple rules match, list the most specific one.
- Only write the markdown file, do not modify any other files.
