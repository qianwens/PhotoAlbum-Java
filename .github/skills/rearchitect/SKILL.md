---
name: rearchitect
description: Scan project for Apache Struts and WinForms usage, report findings with modern alternatives
---

# Rearchitect — Legacy Framework Detection

Scan the current project to detect outdated or unmaintained frameworks/technology stacks, report findings, and suggest modern alternatives. Save results via the `write_assessment_result` tool.

## Input Parameters

- `workspace-path` (optional): Path to the project to analyze (defaults to current directory)

## Execution Steps

### Step 1: Determine Project Type

Identify the project's technology stack by looking for marker files:

| Marker File | Project Type |
|-------------|-------------|
| `pom.xml`, `build.gradle`, `build.gradle.kts` | Java/JVM |
| `*.csproj`, `*.sln`, `*.slnx` | .NET |
| `web.xml` | Java Web (Servlet) |

### Step 2: Run Detection

**Only** check the two targets listed below. Do **not** scan for or report any other frameworks, libraries, or dependencies beyond these two targets.

---

#### Required Targets

##### 1. Apache Struts

**Configuration file detection:**
- `pom.xml` / `build.gradle` / `build.gradle.kts`: search for `org.apache.struts`, `struts2-core`, `struts-core`, `struts-taglib`
- `web.xml`: search for `org.apache.struts`, `StrutsPrepareAndExecuteFilter`, `ActionServlet`

**Source code detection:**
- Java files: search for `import org.apache.struts`, `import com.opensymphony.xwork2`
- JSP files: search for `<%@ taglib.*struts`, `<s:` (Struts 2 tags)

**Alternatives:** Spring Boot + Spring MVC, or Quarkus / Micronaut

**Fixed explanation (use verbatim when detected):**
> Apache Struts has reached end-of-life and no longer receives security patches or bug fixes. It has a history of critical remote code execution vulnerabilities (e.g., CVE-2017-5638, CVE-2023-50164) that made it one of the most exploited frameworks in the Java ecosystem. Continued use exposes the application to known, unpatched attack vectors. Migration to a modern, actively maintained framework such as Spring Boot is strongly recommended to ensure ongoing security support and access to current Java platform features.

##### 2. WinForms (Windows Forms)

**Configuration file detection:**
- `.csproj`: search for `<UseWindowsForms>true</UseWindowsForms>`, `System.Windows.Forms`, `<OutputType>WinExe</OutputType>` (combined with WindowsForms references)

**Source code detection:**
- C# files: search for `using System.Windows.Forms`, `: Form`, `: UserControl` (in System.Windows.Forms context)
- Presence of `.Designer.cs` files

**Alternatives:** WPF, MAUI, Avalonia UI, or Blazor Desktop

**Fixed explanation (use verbatim when detected):**
> Windows Forms (WinForms) is a legacy UI framework tied exclusively to Windows and .NET Framework. While it still receives minimal maintenance in .NET 8+, it lacks modern UI capabilities such as responsive layouts, high-DPI scaling, hardware-accelerated rendering, and cross-platform support. Its designer-centric, event-driven programming model makes it difficult to adopt modern patterns like MVVM or data binding. Migrating to WPF is recommended for richer user experiences, better maintainability, and modern UI patterns.

---

### Step 3: Save Output

Call the `write_assessment_result` tool with the following parameters:
- `resultJson`: the detection results as a JSON string
- `assessmentDir`: the value of the `assessment_dir` variable

The JSON must strictly follow this format:

```json
{
  "outdatedFrameworks": [
    {
      "name": "Apache Struts 2",
      "old": "struts2",
      "new": "spring-boot",
      "status": "end-of-life",
      "detectedVersion": "2.5.30",
      "migrationComplexity": "high",
      "detectedIn": {
        "configFiles": ["path/to/pom.xml"],
        "sourceFiles": ["path/to/Action.java", "path/to/Login.jsp"]
      },
      "alternatives": [
        "Spring Boot + Spring MVC",
        "Quarkus",
        "Micronaut"
      ],
      "explanation": "Apache Struts has reached end-of-life and no longer receives security patches or bug fixes. It has a history of critical remote code execution vulnerabilities (e.g., CVE-2017-5638, CVE-2023-50164) that made it one of the most exploited frameworks in the Java ecosystem. Continued use exposes the application to known, unpatched attack vectors. Migration to a modern, actively maintained framework such as Spring Boot is strongly recommended to ensure ongoing security support and access to current Java platform features."
    }
  ]
}
```

**JSON field descriptions:**
- `name`: Full framework name (with version distinction, e.g. "Apache Struts 1" vs "Apache Struts 2")
- `old`: Short identifier of the legacy framework (e.g. `struts2`, `winforms`)
- `new`: Short identifier of the recommended primary alternative (e.g. `spring-boot`, `maui`, `blazor`)
- `status`: `"end-of-life"` | `"deprecated"` | `"unmaintained"` | `"security-vulnerability"` | `"critical-bug"` | `"runtime-incompatible"`
- `detectedVersion`: Version string detected from config files, or `null` if not determinable
- `migrationComplexity`: `"high"` | `"medium"` | `"low"`
- `detectedIn.configFiles`: List of config file paths where references were detected
- `detectedIn.sourceFiles`: List of source file paths where references were detected
- `alternatives`: List of all recommended alternative frameworks
- `explanation`: Fixed explanation text for why this framework needs to be upgraded — use the exact text specified in each target's "Fixed explanation" section above

If no outdated frameworks are detected, pass `{"outdatedFrameworks": []}` to the tool.

**The JSON passed to the tool must contain ONLY the JSON object described above. No other text or formatting.**

## Error Handling

- **Unsupported project type**: Output a single line: `> ERROR: Unsupported project type. This skill supports Java, .NET, JavaScript, and TypeScript projects only.`
- **No build files found**: Output: `> ERROR: No recognized build files found at {workspace-path}. Verify the path is correct.`
- **Insufficient info**: Generate a best-effort report from available data. Set `detectedVersion` to `null` for dependencies where the version cannot be determined.

## Success Criteria

- All detection targets are checked against both configuration files and source code
- No frameworks or dependencies beyond Apache Struts and WinForms are reported
- JSON is valid and follows the specified schema exactly
- Only high-confidence findings are reported — no guesses or uncertain cases
- Result saved via `write_assessment_result` tool
