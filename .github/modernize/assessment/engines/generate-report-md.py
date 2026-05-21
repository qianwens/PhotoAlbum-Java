#!/usr/bin/env python3
"""
Generates report.md from report.json (Java/.NET) or js-assessment-report.md (JS/TS).

Usage:
    python generate_report_md.py /path/to/.github/modernize/assessment/reports/report-{id}
"""

import json
import os
import re
import sys


def make_anchor_id(title: str) -> str:
    """Convert title to anchor ID: replace non-alnum/non-dash with _, collapse, trim trailing."""
    if not title:
        return "issue"
    result = []
    last_was_underscore = False
    for ch in title:
        if ch.isalnum() or ch == '-':
            result.append(ch)
            last_was_underscore = False
        else:
            if not last_was_underscore and result:
                result.append('_')
                last_was_underscore = True
    if result and result[-1] == '_':
        result.pop()
    return ''.join(result)


def escape_table_cell(value: str) -> str:
    if not value:
        return ""
    return value.replace("|", "\\|").replace("\r", "").replace("\n", " ")


def escape_html(value: str) -> str:
    if not value:
        return ""
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def get_array_as_string(node) -> str:
    """Convert a JSON node (array or string) to comma-separated string."""
    if node is None:
        return ""
    if isinstance(node, list):
        values = [v for v in node if v and str(v).strip()]
        return ", ".join(str(v) for v in values) if values else ""
    if isinstance(node, str):
        return node if node.strip() else ""
    return str(node)


def get_severity_rank(severity: str) -> int:
    s = (severity or "").strip().lower()
    return {"mandatory": 0, "potential": 1, "optional": 2, "information": 3}.get(s, 999)


def is_dotnet_component(language: str) -> bool:
    if not language or language.strip().lower() == "n/a":
        return True
    lang_lower = language.lower()
    return ".net" in lang_lower or "c#" in lang_lower


def render_appcat_report(report_dir: str, report_json_path: str) -> str:
    """Render report.md from report.json for Java/.NET."""
    with open(report_json_path, 'r', encoding='utf-8') as f:
        root = json.load(f)

    rules = root.get("rules", {})
    projects = root.get("projects", [])
    security_findings = root.get("security", [])
    rearchitect_findings = root.get("rearchitect", [])

    if not projects:
        return ""

    # Parse first component
    project = projects[0]
    properties = project.get("properties", {}) or {}

    component_name = properties.get("repo") or properties.get("appName") or "Others"
    language = get_array_as_string(properties.get("languages")) or "N/A"
    frameworks = get_array_as_string(properties.get("frameworks")) or "N/A"
    build_tools = get_array_as_string(properties.get("tools")) or "N/A"

    # Merge all projects for same component
    all_incidents = []
    for proj in projects:
        incidents_array = proj.get("incidents", [])
        for inc in incidents_array:
            all_incidents.append(inc)

    # Group incidents by ruleId, track unique rules
    rule_groups = {}  # ruleId -> list of incidents
    for inc in all_incidents:
        rule_id = inc.get("ruleId", "")
        if not rule_id or rule_id not in rules:
            continue
        rule_groups.setdefault(rule_id, []).append(inc)

    # Compute severity counts (unique rules)
    mandatory_rules = set()
    potential_rules = set()
    optional_rules = set()
    for rule_id in rule_groups:
        rule_obj = rules.get(rule_id, {})
        severity = (rule_obj.get("severity") or "").strip().lower()
        if severity == "mandatory":
            mandatory_rules.add(rule_id)
        elif severity == "potential":
            potential_rules.add(rule_id)
        elif severity == "optional":
            optional_rules.add(rule_id)

    # Security finding counts
    sec_mandatory = sum(1 for f in security_findings if (f.get("severity") or "").strip().lower() == "mandatory")
    sec_potential = sum(1 for f in security_findings if (f.get("severity") or "").strip().lower() == "potential")

    total_issues = len(rule_groups) + len(security_findings)
    mandatory_blockers = len(mandatory_rules) + sec_mandatory
    potential_issues = len(potential_rules) + sec_potential

    # Classify rules into cloud/upgrade
    is_dotnet = is_dotnet_component(language)
    cloud_rules = []
    upgrade_rules = []

    for rule_id, incidents in rule_groups.items():
        rule_obj = rules.get(rule_id, {})
        labels = rule_obj.get("labels", []) or []
        labels = [l for l in labels if l and str(l).strip()]

        has_domain_label = any(str(l).lower().startswith("domain=") for l in labels)
        is_cloud = any(str(l).lower() == "domain=cloud-readiness" for l in labels)
        is_upgrade = any(str(l).lower().endswith("-upgrade") for l in labels)

        if not has_domain_label and is_dotnet:
            is_cloud = True

        if is_cloud:
            cloud_rules.append(rule_id)
        if is_upgrade:
            upgrade_rules.append(rule_id)

    # Get AKS effort for each rule (first incident's target or rule-level)
    def get_aks_effort(rule_id: str) -> float:
        incidents = rule_groups.get(rule_id, [])
        for inc in incidents:
            targets = inc.get("targets", {}) or {}
            for target_id, target_data in targets.items():
                if isinstance(target_data, dict) and "aks" in target_id.lower():
                    effort = target_data.get("effort", 0)
                    if effort:
                        return float(effort)
            break
        # Fallback to rule-level
        rule_obj = rules.get(rule_id, {})
        return float(rule_obj.get("effort", 0) or 0)

    def sort_key(rule_id):
        rule_obj = rules.get(rule_id, {})
        severity = (rule_obj.get("severity") or "").strip().lower()
        rank = get_severity_rank(severity)
        count = len(rule_groups.get(rule_id, []))
        return (rank, -count)

    cloud_rules.sort(key=sort_key)
    upgrade_rules.sort(key=sort_key)

    # Build markdown
    lines = []
    lines.append(f"# {component_name}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Total Issues | {total_issues} |")
    lines.append(f"| Mandatory Blockers | {mandatory_blockers} |")
    lines.append(f"| Potential Issues | {potential_issues} |")
    lines.append("")
    lines.append("## Application Information")
    lines.append("")
    lines.append("| Property | Value |")
    lines.append("|----------|-------|")
    lines.append(f"| Language | {escape_table_cell(language)} |")
    lines.append(f"| Frameworks | {escape_table_cell(frameworks)} |")
    lines.append(f"| Build tools | {escape_table_cell(build_tools)} |")

    # Conditional rows
    jdk_version = properties.get("jdkVersion", "")
    if jdk_version and str(jdk_version).strip():
        lines.append(f"| JDK version | {escape_table_cell(str(jdk_version))} |")

    description = properties.get("description", "")
    if description and str(description).strip():
        lines.append(f"| Description | {escape_table_cell(str(description))} |")

    app_type = properties.get("applicationType", "")
    if app_type and str(app_type).strip():
        lines.append(f"| Application type | {escape_table_cell(str(app_type))} |")

    tags = get_array_as_string(properties.get("tags"))
    if tags:
        lines.append(f"| Tags | {escape_table_cell(tags)} |")

    loc = properties.get("linesOfCode", "")
    if loc and str(loc).strip():
        lines.append(f"| Lines of code | {escape_table_cell(str(loc))} |")

    # Do NOT include Story points
    lines.append("")

    def render_issue_section(section_title: str, rule_ids: list):
        if not rule_ids:
            return
        lines.append(f"## {section_title}")
        lines.append("")
        lines.append("| Issue Name | Criticality | Story Points | Occurrences |")
        lines.append("|------------|-------------|--------------|-------------|")

        for rule_id in rule_ids:
            rule_obj = rules.get(rule_id, {})
            title = rule_obj.get("title") or rule_id
            severity = (rule_obj.get("severity") or "").strip().lower()
            crit_label = {"mandatory": "Mandatory", "potential": "Potential"}.get(severity, "Optional")
            effort = get_aks_effort(rule_id)
            # Format effort: integer if whole, else float
            effort_str = str(int(effort)) if effort == int(effort) else f"{effort:g}"
            count = len(rule_groups.get(rule_id, []))
            anchor_id = make_anchor_id(title)

            # Check if any incident has a file path
            has_locations = any(
                (inc.get("location") or "").strip()
                for inc in rule_groups.get(rule_id, [])
            )
            occurrences_cell = f"[{count}](#{anchor_id})" if has_locations else str(count)
            lines.append(f"| {escape_table_cell(title)} | {crit_label} | {effort_str} | {occurrences_cell} |")

        lines.append("")
        lines.append("### Issue Details")
        lines.append("")

        for rule_id in rule_ids:
            rule_obj = rules.get(rule_id, {})
            title = rule_obj.get("title") or rule_id
            incidents = rule_groups.get(rule_id, [])

            locations = []
            for inc in incidents:
                file_path = (inc.get("location") or "").strip()
                if not file_path:
                    continue
                line_num = inc.get("line")
                if line_num is not None:
                    try:
                        line_num = int(line_num)
                        locations.append(f"{file_path} (line {line_num})")
                    except (ValueError, TypeError):
                        locations.append(file_path)
                else:
                    locations.append(file_path)

            if not locations:
                continue

            anchor_id = make_anchor_id(title)
            lines.append(f'<details id="{anchor_id}">')
            lines.append(f"<summary><b>{escape_html(title)}</b> — affected files</summary>")
            lines.append("")
            for loc in locations:
                lines.append(f"- `{loc}`")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    render_issue_section("Cloud Readiness Issues", cloud_rules)
    render_issue_section("Upgrade Issues", upgrade_rules)

    # Rearchitect findings
    if rearchitect_findings:
        lines.append("## Rearchitect Findings")
        lines.append("")
        lines.append("> **Note:** These findings were generated by AI and may contain inaccuracies or incomplete information. Please review carefully.")
        lines.append("")
        lines.append("| Finding | Old | New | Story Points | Files |")
        lines.append("|---------|-----|-----|--------------|-------|")

        for finding in rearchitect_findings:
            name = finding.get("name", "")
            old = finding.get("old", "")
            new = finding.get("new", "")
            story_points = finding.get("storyPoints", 5)
            detected_in = finding.get("detectedIn", {}) or {}
            config_files = detected_in.get("configFiles", []) or []
            source_files = detected_in.get("sourceFiles", []) or []
            all_files = config_files + source_files
            anchor_id = make_anchor_id(name)
            files_cell = f"[{len(all_files)}](#{anchor_id})" if all_files else "0"
            lines.append(f"| {escape_table_cell(name)} | {escape_table_cell(old)} | {escape_table_cell(new)} | {story_points} | {files_cell} |")

        lines.append("")
        lines.append("### Rearchitect Finding Details")
        lines.append("")

        for finding in rearchitect_findings:
            name = finding.get("name", "")
            detected_in = finding.get("detectedIn", {}) or {}
            config_files = detected_in.get("configFiles", []) or []
            source_files = detected_in.get("sourceFiles", []) or []
            all_files = config_files + source_files
            if not all_files:
                continue
            anchor_id = make_anchor_id(name)
            lines.append(f'<details id="{anchor_id}">')
            lines.append(f"<summary><b>{escape_html(name)}</b> — affected files</summary>")
            lines.append("")
            for file in all_files:
                lines.append(f"- `{file}`")
            lines.append("")
            explanation = finding.get("explanation", "")
            if explanation and explanation.strip():
                lines.append(f"**Explanation:** {explanation}")
                lines.append("")
            lines.append("</details>")
            lines.append("")

    # Security Issues
    if security_findings:
        lines.append("## Security Issues")
        lines.append("")
        lines.append("> **Note:** These issues were generated by AI and may contain inaccuracies or incomplete information. Please review carefully.")
        lines.append("")
        lines.append("| Issue Name | Criticality | Story Points | Files |")
        lines.append("|------------|-------------|--------------|-------|")

        ordered_findings = sorted(
            security_findings,
            key=lambda f: (get_severity_rank((f.get("severity") or "").strip().lower()), -(f.get("storyPoint", 0) or 0))
        )

        for finding in ordered_findings:
            severity = (finding.get("severity") or "").strip().lower()
            crit_label = {"mandatory": "Mandatory", "potential": "Potential"}.get(severity, "Optional")
            finding_id = finding.get("id", "")
            title = finding.get("title", "")
            display_name = f"{finding_id}: {title}" if title and title.strip() else finding_id
            story_point = finding.get("storyPoint", 0) or 0
            evidence = finding.get("evidence", {}) or {}
            files = evidence.get("files", []) or []
            anchor_id = make_anchor_id(display_name)
            files_cell = f"[{len(files)}](#{anchor_id})" if files else "0"
            lines.append(f"| {escape_table_cell(display_name)} | {crit_label} | {story_point} | {files_cell} |")

        lines.append("")
        lines.append("### Security Issue Details")
        lines.append("")

        for finding in ordered_findings:
            evidence = finding.get("evidence", {}) or {}
            files = evidence.get("files", []) or []
            if not files:
                continue
            finding_id = finding.get("id", "")
            title = finding.get("title", "")
            display_name = f"{finding_id}: {title}" if title and title.strip() else finding_id
            anchor_id = make_anchor_id(display_name)
            lines.append(f'<details id="{anchor_id}">')
            lines.append(f"<summary><b>{escape_html(display_name)}</b> — affected files</summary>")
            lines.append("")
            for file in files:
                lines.append(f"- `{file}`")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    lines.append("---")
    lines.append("")

    # Codebase Insights
    append_codebase_insights(lines, report_dir)

    lines.append("[Share feedback](https://aka.ms/ghcp-appmod/feedback)")

    return '\n'.join(lines) + '\n'


def append_codebase_insights(lines: list, report_dir: str):
    """Append Codebase Insights section with links to available fact files."""
    fact_docs = [
        ("architecture-diagram.md", "Architecture Diagram", "Understand the big picture: system layers and component relationships"),
        ("dependency-map.md", "Dependency Map", "Know what the project depends on and where the risks are"),
        ("api-service-contracts.md", "API & Service Contracts", "See how services communicate and what contracts they expose"),
        ("data-architecture.md", "Data Architecture", "Explore data models, storage, and data flow patterns"),
        ("configuration-inventory.md", "Configuration Inventory", "Review how the application is configured across environments"),
        ("business-workflows.md", "Business Workflows", "Trace end-to-end business processes and domain logic"),
    ]

    facts_dir = os.path.join(report_dir, "facts")

    lines.append("## Codebase Insights")
    lines.append("")
    lines.append("> **Note:** These documents are generated by AI and may contain inaccuracies or incomplete information. Please review carefully.")
    lines.append("")

    existing = []
    if os.path.isdir(facts_dir):
        for filename, title, desc in fact_docs:
            if os.path.isfile(os.path.join(facts_dir, filename)):
                existing.append((filename, title, desc))

    if not existing:
        lines.append("> **Codebase Insights aren't available yet.**")
        lines.append(">")
        lines.append("> These documents are generated when assessment runs with **Full analysis** coverage. Re-run the assessment and set `analysisCoverage: full` to enable them.")
        lines.append("")
        return

    for i, (filename, title, desc) in enumerate(existing, 1):
        lines.append(f"{i}. **[{title}](facts/{filename})** — {desc}")

    lines.append("")


def render_jsts_report(report_dir: str, ncu_path: str) -> str:
    """Render report.md from js-assessment-report.md for JS/TS."""
    with open(ncu_path, 'r', encoding='utf-8') as f:
        ncu_output = f.read()

    # Parse ncu output
    dependencies = []
    patch_count = 0
    minor_count = 0
    major_count = 0
    zero_major_count = 0
    package_manager = "npm"
    current_category = ""
    current_category_display = ""

    for line in ncu_output.split('\n'):
        trimmed = line.strip()
        if trimmed.startswith("Using "):
            package_manager = trimmed[len("Using "):].strip()
        elif trimmed.startswith("Patch"):
            current_category = "patch"
            current_category_display = "Patch"
        elif trimmed.startswith("Minor"):
            current_category = "minor"
            current_category_display = "Minor"
        elif trimmed.startswith("Major   Potentially breaking"):
            current_category = "major"
            current_category_display = "Major"
        elif trimmed.startswith("Major version zero"):
            current_category = "zero-major"
            current_category_display = "Major (0.x)"
        elif trimmed and '→' in trimmed:
            arrow_idx = trimmed.index('→')
            before_arrow = trimmed[:arrow_idx].strip()
            after_arrow = trimmed[arrow_idx + 1:].strip()

            parts = before_arrow.split()
            name = ' '.join(parts[:-1]) if len(parts) >= 2 else before_arrow
            current_version = parts[-1] if len(parts) >= 2 else ""

            dependencies.append((name, current_version, after_arrow, current_category_display))

            if current_category == "patch":
                patch_count += 1
            elif current_category == "minor":
                minor_count += 1
            elif current_category == "major":
                major_count += 1
            elif current_category == "zero-major":
                zero_major_count += 1

    total_count = patch_count + minor_count + major_count + zero_major_count

    # Derive repo name from directory name
    repo_name = os.path.basename(report_dir)

    lines = []
    lines.append(f"# {repo_name}")
    lines.append("")
    lines.append("JavaScript/TypeScript Dependency Assessment")
    lines.append("")
    lines.append("## Application Information")
    lines.append("")
    lines.append("| Property | Value |")
    lines.append("|----------|-------|")
    lines.append("| Language | JavaScript/TypeScript |")
    lines.append(f"| Build tools | {escape_table_cell(package_manager)} |")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Update Type | Count |")
    lines.append("|-------------|-------|")
    lines.append(f"| **Total Updates** | **{total_count}** |")
    lines.append(f"| Patch | {patch_count} |")
    lines.append(f"| Minor | {minor_count} |")
    lines.append(f"| Major | {major_count} |")
    if zero_major_count > 0:
        lines.append(f"| Major (0.x) | {zero_major_count} |")
    lines.append("")

    if dependencies:
        lines.append("## Dependency Updates")
        lines.append("")
        lines.append("| Package | Current | Target | Type |")
        lines.append("|---------|---------|--------|------|")
        for name, current, target, category in dependencies:
            lines.append(f"| {escape_table_cell(name)} | {escape_table_cell(current)} | {escape_table_cell(target)} | {category} |")
        lines.append("")

    lines.append("## Recommendations")
    lines.append("")
    lines.append("| Update Type | Guidance |")
    lines.append("|-------------|---------|")
    lines.append("| Patch & Minor | Generally safe to apply. Consider updating these first. |")
    lines.append("| Major | Review breaking changes in package release notes before updating. |")
    lines.append("| Major (0.x) | Exercise caution — these packages follow unstable version semantics. |")
    lines.append("")
    lines.append("---")
    lines.append("")

    append_codebase_insights(lines, report_dir)

    lines.append("[Share feedback](https://aka.ms/ghcp-appmod/feedback)")

    return '\n'.join(lines) + '\n'


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_report_md.py <report-directory>", file=sys.stderr)
        sys.exit(1)

    report_dir = sys.argv[1]

    if not os.path.isdir(report_dir):
        print(f"Error: Directory not found: {report_dir}", file=sys.stderr)
        sys.exit(1)

    report_json_path = os.path.join(report_dir, "report.json")

    if os.path.isfile(report_json_path):
        # Java/.NET mode
        markdown = render_appcat_report(report_dir, report_json_path)
    else:
        # JS/TS mode - look for js-assessment-report.md
        ncu_path = os.path.join(report_dir, "js-assessment-report.md")
        if not os.path.isfile(ncu_path):
            # Check parent directory
            parent = os.path.dirname(report_dir)
            ncu_path = os.path.join(parent, "js-assessment-report.md")
        if not os.path.isfile(ncu_path):
            print("Error: Neither report.json nor js-assessment-report.md found.", file=sys.stderr)
            sys.exit(1)
        markdown = render_jsts_report(report_dir, ncu_path)

    if not markdown:
        print("Error: Failed to generate report.", file=sys.stderr)
        sys.exit(1)

    output_path = os.path.join(report_dir, "report.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
