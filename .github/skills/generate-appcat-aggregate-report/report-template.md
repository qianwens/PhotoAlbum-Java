# Application Assessment Overview Template

Use this template to generate a concise markdown summary of a
multi-repository assessment.

All example data below (repo1, repo2, issue1, etc.) are placeholders.
Replace them with actual repository names, issue titles, and values
calculated from the aggregated JSON report.

The report MUST follow this structure:

---

## Application profile

Start with 1–2 sentences explaining that this section summarizes
the main technical characteristics of each repository.

Then, for each repository, add a short profile block using
simple key/value lines instead of a table, for example:

Repository: customers-service
Primary language and version: Java 17
Build tool: Maven
Primary frameworks: Spring Boot, Spring Cloud

Guidance:

- Keep the same set of keys and ordering for every repository.
- **Repository**: the canonical repository name.
- **Primary language and version**: the main language and, when
  available, its runtime version (for example, `Java 17`,
  `.NET 8`, `Node.js 20`). If version information is unclear,
  you may omit the version and use just the language.
- **Build tool**: the primary build tool (for example, Maven,
  Gradle, MSBuild).
- **Primary frameworks**: 1–2 key application frameworks
  (for example, Spring Boot, ASP.NET Core).

Separate repository blocks with a blank line. Avoid listing too
many minor frameworks or tools; keep each profile compact.

---

## Issue insights summary

Start with a short paragraph that summarizes overall readiness
risks and **main blocker themes**, for example:

> This portfolio includes several repositories with varying
> levels of cloud and upgrade readiness. A few repositories
> concentrate most of the blockers, while others are closer
> to cloud-ready.

Do **not** include explicit numeric counts here (no totals for
repositories, issues, or cloud/upgrade readiness). Keep the
language qualitative (for example, "several", "a few",
"most", "some").

After the introductory paragraph (and optional bullets), provide
1–2 short sentences that **summarize the situation across the
repositories**, for example:

- Which repositories appear to have the heaviest concentration of
  issues.
- Which ones look relatively lighter and closer to cloud-ready.
- Any obvious common blocker themes (for example, secrets in
  configuration, outdated runtimes, insecure protocols).

Keep this section **purely qualitative and concise**. Focus on
describing the relative readiness of repositories and the main
blocker patterns, and avoid all explicit numeric details.

## Formatting rules

- Focus on repository-level information; do **not** generate
  long per-file or per-incident sections.
- Use only qualitative wording in Issue insights summary:
  do **not** output any explicit numeric values (no counts,
  totals, or percentages) and do not include per-repository
  numeric tables.
- Keep the report **concise** and easy to scan.
- **Do not** include code snippets, Dockerfiles, or manifests.
- **Do not** include header metadata at the top of the report.
- Use normal sentence case for section titles, not uppercase.
