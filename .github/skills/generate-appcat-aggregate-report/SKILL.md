---
name: generate-appcat-aggregate-report
description: Generate an at-scale repository assessment markdown report from an aggregated AppCat JSON report, focusing on repository profiles and issue insights.
---

# Generate AppCat aggregate assessment report

This skill generates a human-readable, at-scale application
assessment report in Markdown from a single aggregated AppCat
JSON report.

The report structure and formatting rules are defined by the
`report-template.md` file.

You generate a **concise markdown summary** from an aggregated
AppCat JSON report. The markdown should provide two things:
- An **Application profile** that describes the main technical
  characteristics of each repository.
- An **Issue insights summary** that surfaces portfolio-level
  issue volume and readiness risks, and qualitatively describes
  how the repositories compare in terms of readiness.

Your responsibilities:

- Interpret the aggregated JSON (repositories, rules, domains).
- Compute the repository-level and portfolio-level metrics
  required by the template.
- Populate the markdown using the structure in `report-template.md`.
- Keep the output short, focused, and easy to read.

## Hard constraints (MUST follow)

These rules are **strict**. Do not violate them:

1. **Always aggregate by repository, never by project/application.**
  - A repository is identified **only** by `properties.repo`.
  - Projects (`projects` array items) are just raw input; you **must not**
    output one markdown block or table row per project.
2. **Each repository appears exactly once in the markdown.**
  - In **Application profile**: exactly one block per repository.
  - In **Issue insights summary**: exactly one table row per repository.
3. **Never loop over `projects` to write output directly.**
  - You may read `projects` to collect data, but you **must first group**
    by `properties.repo` and then drive all output from that grouped
    repository map.
4. **Repository-level numbers must match the HTML dashboard semantics.**
  - Issue counts are always **per repository**, based on distinct rules
    with incidents, not per project.

### Required repository aggregation algorithm (NO deviation)

Follow this high-level algorithm exactly when computing metrics:

1. Build a map `repoName -> repoState` where `repoName` is
  `project.properties.repo`.
2. For every project in `projects`:
  - Read `properties.repo`; if missing, infer a reasonable repo name
    (for example, folder name), but still treat this as **one repo**.
  - Merge languages/frameworks/tools into the same `repoState` entry.
3. For every project and its `incidents`:
  - For each incident, look up `rules[ruleId]` and update the
    per-repository rule map as described later in this file
    (distinct rules, domain labels, .NET behavior, etc.).
4. After processing **all** projects:
  - For each `repoName` in the map, compute:
    - Total issues (distinct rules for that repo).
    - Cloud readiness issues.
    - Upgrade readiness issues.
  - Use **this** repository map as the **only** source of truth for
    markdown output.

If at any point you are tempted to write something like
"for each project in projects, print…", **stop** and instead ensure you
are iterating over the **repository map** you built from `properties.repo`.

## Input JSON structure (conceptual)

You receive a single aggregated JSON file with this conceptual
shape (field names may vary slightly, but the semantics remain
the same):

- `projects`: array of assessed projects.
  - Each project has:
    - `properties.repo`: canonical repository name (preferred
      identifier).
    - `properties.languages`, `properties.frameworks`,
      `properties.tools`, and optionally a version field such as
      `properties.jdkVersion` or an equivalent runtime/version
      indicator.
    - `rules`: distinct rule definitions (each represents one
      **issue type**).
    - `incidents`: occurrences of rules in files/lines.
- `summary`: global statistics precomputed by the aggregator
  (you may use these when convenient, or recompute metrics if
  needed).

You do **not** need to list or describe the raw JSON fields;
only use them to compute the metrics required by the template.

## Core semantics

- A **repository** is identified by `properties.repo` on each
  project.
- A **rule** represents a distinct **issue type**.
- An **issue** for reporting is one distinct rule (`ruleId`)
  that has at least one occurrence in a given repository.

From this, derive:

- Per repository **total issue count** = number of distinct
  rules with at least one occurrence.
- Global **cloud readiness** and **upgrade readiness** counts
  = sums of the respective per-repository counts.

**Do not** use any precomputed counters from the JSON such as
`project.issues`, `project.storyPoints`, `summary.totalIssues`,
or `summary.totalIncidents` for these metrics. Always recompute
issue counts from `rules` + `incidents` as described below.

### Domain labels

Use rule `domain` to classify issues:

- `cloud-readiness` → cloud readiness issue.
- Any value ending with `-upgrade` (for example, `java-upgrade`,
  `dotnet-upgrade`) → upgrade readiness issue.

Per-repository counts:

- **Cloud readiness issues** = number of distinct rules with
  domain `cloud-readiness`.
- **Upgrade readiness issues** = number of distinct rules with
  domain ending in `-upgrade`.

Language-specific behavior:

- **Java projects**: only count issues when the rule has an
  explicit domain label.
- **.NET projects**: as of the current ruleset there are **no**
  `domain=` labels defined at all (and no `*-upgrade` domains),
  so you must treat **all .NET rules** as **cloud readiness**
  issues. For .NET repositories this means:
  - Every distinct rule that has incidents contributes to the
    cloud readiness issue count.
  - The upgrade readiness issue count will normally be `0`
    until .NET rules start using explicit `domain=*-upgrade`
    labels in future versions.

## What to compute

To fill the markdown template, compute at least:

1. **Global overview (for internal reasoning only)**
   - Total number of repositories.
   - Aggregate cloud readiness and upgrade readiness issue
     counts.

   These values are **only** for internal reasoning. In the
   markdown Issue insights summary you must **not** output any
   explicit numeric totals (no "Total X" lines, no exact
   counts); instead, use qualitative phrases such as "several
   repositories", "most issues are cloud-readiness", or
   "only a few upgrade readiness issues".

2. **Application profile metrics**
   - For each repository, determine:
     - Primary language (from `properties.languages`, or inferred
       from frameworks/tools if necessary).
     - Language/runtime version when available (for example,
       from `properties.jdkVersion` or target framework info),
       to populate the "Primary language and version" line.
     - Aggregated frameworks (from `properties.frameworks`).
     - Aggregated build tools (from `properties.tools`).

3. **Repository-level issue metrics (for reasoning)**
   - For each repository, determine **only from the aggregated
     AppCat JSON**, using the `rules` map and `incidents`:
     - Total issue count = number of **distinct `ruleId` values**
       that have at least one incident in that repository.
     - Cloud readiness issue count = number of **distinct rules**
       whose domain label is `domain=cloud-readiness`.
     - Upgrade readiness issue count = number of **distinct rules**
       whose domain label ends with `-upgrade` (for example,
       `domain=java-upgrade`, `domain=dotnet-upgrade`).
     - Domain labels are read from `rules[ruleId].labels` entries
       that start with `domain=`.
     - For **.NET repositories** (language contains `.NET` or
       `C#`), if a rule has **no** `domain=` label at all, then
       treat that rule as **cloud readiness**.
     - 1–2 **top blockers** (issue titles) per repository chosen
       by, in order:
       - Higher severity from the rule object
         (`mandatory` > `potential` > `optional` > `information`
           > others).
       - Higher number of incidents for that rule within the
         same repository.
       - Stable tie-breaking by `ruleId` or title when needed,
         so that multiple high-impact rules can appear (for
         example, two security rules with similar weight).

     A simple way to compute these metrics without mistakes is:

     1. For each repository, build a map `ruleId -> { isCloud,
        isUpgrade }`, initially empty.
     2. Walk all `incidents` for that repository. For each
        incident:
        - Look up the corresponding rule in `rules[ruleId]`.
        - Derive `isCloud` / `isUpgrade` from the rule's
          `labels` and language rules above (including the
          .NET behavior).
        - Update the map entry for that `ruleId` so that
          `isCloud` / `isUpgrade` become `true` if they were
          ever `true` for any incident.
     3. After processing all incidents for that repository:
        - `Total issue count` = number of distinct keys in the
          map.
        - `Cloud readiness issues` = number of entries where
          `isCloud` is `true`.
        - `Upgrade readiness issues` = number of entries where
          `isUpgrade` is `true`.

     > **Critical rule:** Never use the raw number of incidents
     > (occurrences of a rule) as the issue count. If a single
     > upgrade rule fires 6 times in different files, that still
     > counts as **1 upgrade readiness issue** for that
     > repository. All prose like "this repository has X upgrade
     > readiness issues" must use the **distinct rule** counts
     > from this map, not incident counts.

## Reporting and formatting rules

- **Use the template in `report-template.md` exactly** for
  section structure and overall flow, but **do not** add a
  detailed numeric table. The output should remain narrative
  and high level.
- Only emit the two sections defined in the template:
  **Application profile** and **Issue insights summary**.
  Do **not** add extra sections such as "Executive Summary",
  "Project Details", "Recommendations", or "Next Steps".
- **Do not** generate per-project deep-dive content. Avoid
  listing individual issues with their locations, snippets,
  or long descriptions. Do not include per-file, per-class,
  or per-line details.
- **Do not** use the word "incident" in the markdown output.
  You can reason about incidents internally but only surface
  **issues** to the user.
- Use terms: **repository**, **issue**, **cloud readiness**,
  **upgrade readiness**.
- Avoid terms like: incident, bug, vulnerability, ticket.
- You may compute detailed per-repository metrics internally,
  but in the markdown, keep the Issue insights summary focused
  on **qualitative comparisons** between repositories (for
  example, which ones are most/least ready, and common blocker
  themes). Do **not** output any explicit numeric values in
  Issue insights summary: no global totals, no per-repository
  counts, and no percentages. Prefer wording like "most issues
  are cloud-readiness" or "a small number of upgrade readiness
  issues appear in the portfolio".
- Keep the text short, neutral, and focused on clarity. Prefer
  1–3 sentences per narrative paragraph.

This skill is **only** responsible for generating the markdown
summary based on the aggregated JSON input. The HTML dashboard
is generated separately; your job is to provide a complementary
text summary that reflects the same data.

The skill is complete when:

1. A Markdown file exists at `output-markdown-path`.
2. The file follows the structure and formatting rules from `prompt-guide-path`,
  producing exactly the **Application profile** and **Issue insights summary**
  sections (and no others).
3. All numeric data (counts, percentages, readiness scores) is derived from the
  current `aggregate-report-json-path` content, not from any example.
4. Each repository in the aggregated JSON appears exactly once in the
  Application profile block list and once in the Issue insights summary table,
  without additional per-repository sections.

If any required input file is missing or unreadable, clearly explain the
problem in your reasoning and fail fast instead of hallucinating data.
