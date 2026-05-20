---
name: validate-playbook-evidence
description: Analyze code changes and produce playbook compliance evidence from git diff
---

# Validate Playbook Evidence

Analyze the git diff and produce playbook compliance evidence showing which rules were implemented.

## User Input

- baseline-commit-sha (Mandatory): The baseline commit SHA to diff from
- playbook-file-list (Mandatory): Comma-separated list of playbook file names
- evidence-output-path (Mandatory): Path to write the evidence markdown summary

## Workflow

1. Analyze the git diff from baseline commit ${baseline-commit-sha} to HEAD
2. The playbook files are: ${playbook-file-list}
3. Write a markdown summary to ${evidence-output-path} with the following format:

## Playbook Code Evidence (from diff)

### [policies.md]
**Rule: brief rule summary**
```diff
+ filepath:line  added code
- filepath:line  removed code
```

Focus on the 2-5 most impactful rules. Each diff line starts with '+' or '-' and includes file:line prefix.
Only write the markdown file, do not modify any other files.
