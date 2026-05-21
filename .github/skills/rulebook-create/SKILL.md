---
name: rulebook-create
description: Generate or update modernization rulebook from document sources. Use this skill when the user wants to create a rulebook, sync rulebook from a document or GitHub issue, extract migration policies from architecture docs, or update existing rulebook files with new decisions.
---

# Rulebook Create

Analyze source documents and generate a modernization rulebook — three markdown files that capture an organization's modernization strategy, approved migration targets, and enforceable policies (standards + guardrails).

## User Input

- **output-path** (Required): The folder to save the rulebook files.
- **source-file-path** (Optional): Path to the source file or directory containing the document content
- **use-defaults** (Optional): When `true`, read the built-in default rulebook files as reference to fill gaps in the generated rulebook. User source takes priority when there is a conflict. Default files: [charter-default](references/charter-default.md), [targets-default](references/targets-default.md), [policies-default](references/policies-default.md)

## Output Structure

```
${output-path}/
├── charter.md       # Scope, 6R modernization strategy, and principles
├── targets.md       # Approved target technologies, library mappings, and target artifacts
└── policies.md      # Standards + guardrails: naming, security, compliance, prohibited/required tech, validation gates
```

## Principles

- **Source Fidelity**: The rulebook is loaded and enforced by automated agents at runtime — a fabricated policy causes wrong migration decisions. Only include content explicitly present in the source document or user prompt. If a category isn't mentioned, omit that section entirely rather than adding placeholders.
- **Incremental Merge**: When output files already exist, merge at the **section level** — update sections with new or changed content, preserve unchanged sections verbatim. If the source explicitly removes or contradicts an existing entry, update that entry. Never drop existing content simply because the source is silent on it.
- **Direct Policy Output**: State policies as-is. Do not include rationale, explanations, or implementation guidance — those belong elsewhere (skills).

## Classification Principles

Each file serves a distinct purpose and is consumed at different stages of the modernization workflow:

- **charter.md** — Rulebook metadata (name, version), scope (covered applications, languages constraints), 6R modernization strategy (Rehost / Replatform / Refactor decision table with override conditions — Retire, Retain, Repurchase are outside app modernization scope), and guiding principles. Loaded during assessment and plan creation to determine what to modernize and what strategy to apply.
- **targets.md** — Approved framework versions, compute/data/integration services, source-to-target library mappings, and target artifacts (container base images). Loaded during assessment (to define target services to assess against) and plan creation (to determine what tasks to generate).
- **policies.md** — Naming & metadata standards, security requirements, compliance requirements, guardrails (prohibited technologies/patterns, required elements, region constraints), validation & quality gates, and coding style guidelines. Loaded during assessment, plan creation, and execution to enforce standards and guardrails.

## Workflow

### Step 1: Read and Analyze Source

1. If ${source-file-path} is provided, read the content (may be a GitHub issue export, markdown file, or a directory of files — if a directory, read all files recursively)
2. If ${use-defaults} is `true`, read the default rulebook files ([charter-default](references/charter-default.md), [targets-default](references/targets-default.md), [policies-default](references/policies-default.md)) as reference context. When the user source and a default conflict, the user source takes priority.
3. Check if output files already exist in ${output-path} — read them for merge comparison
4. Classify each decision from the source (and/or the user prompt) into one of the three output files using the Classification Guide above

If no source file is provided, work with the user prompt and any existing rulebook files only.

### Step 2: Generate Rulebook Files

For each file, use the corresponding template as the structural reference, then fill in content extracted from the source.
Only include sections/subsections that have meaningful, source-backed content. Do not emit empty headings, empty tables, or placeholder-only sections.

#### charter.md

Use the template [charter-template](charter-template.md) as a section catalog:
- Metadata, Scope, 6R Modernization Strategy (Rehost / Replatform / Refactor), Principles

#### targets.md

Use the template [targets-template](targets-template.md) as a section catalog:
- Target Frameworks, Target Compute Services, Target Data Services, Target Integration Services, Target Libraries, Target Artifacts

#### policies.md

Use the template [policies-template](policies-template.md) as a section catalog:
- Naming & Metadata Standards, Security Requirements, Compliance Requirements, Guardrails (Hard Boundaries), Validation & Quality Gates, Coding Style Guidelines

For each file: if it already exists, merge new content; if not, create it fresh.

### Step 3: Validate

Verify the output before finishing:
- [ ] All three files exist in ${output-path}
- [ ] Each file includes only sections with meaningful content from the source
- [ ] No empty headings, empty tables, or placeholder-only sections remain
- [ ] Every decision in the source document is reflected in at least one output file
- [ ] No content was invented beyond what the source provides

### Step 4: Present Summary

Report to the user:
- Number of target technologies defined
- Number of library migration mappings captured
- Number of prohibited technologies/patterns
- Number of required elements
- Number of validation/quality gates
- Sections omitted due to missing source content — flag these as gaps for architect review
