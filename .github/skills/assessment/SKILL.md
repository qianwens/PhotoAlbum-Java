---
name: assessment
description: Run application assessment for a single repository
---

# Application Assessment

This skill performs application assessment for a single repository using AppCAT tools.

## When to Use This Skill

Use this skill when you need to:

• Assess a Java or .NET application for cloud readiness and migration issues
• Generate detailed assessment reports with issue analysis and recommendations
• Understand application dependencies, frameworks, and potential migration blockers

## What This Skill Does

This skill performs a simplified assessment workflow:

1. **Check Project Type and Prerequisites**:
   - **For Java projects**: Verify that MCP tools are available ('appmod-precheck-assessment' and 'appmod-run-assessment')
     - If these MCP tools are not configured, return immediately with setup instructions
   - **For .NET projects**: Check if .NET SDK is available
     - No MCP tools required for .NET assessment

2. **Run Assessment**:
   - **For Java projects**: Trigger AppCAT analysis via Assessment MCP server
     - Uses 'appmod-precheck-assessment' and 'appmod-run-assessment' MCP tools
     - Auto-detects project configuration
   - **For .NET projects**: Install and run AppCAT directly
     - Install: `dotnet tool update dotnet-appcat`
     - Run: `dotnet-appcat analyze --source {workspace-path} --target Any --serializer APPMODJSON --code --privacyMode Protected --non-interactive --report {workspace-path}\.github\modernize\report.json`
   - Analyzes code for cloud migration issues
   - Generates structured assessment data
   - Report is stored under `.github/modernize/` directory

3. **Consolidate Report** (Java projects only):
   - Search for `report.json` under `.github/modernize/` subdirectories
   - Common locations: `.github/modernize/appcat/result/report.json`
   - Copy the latest report to `.github/modernize/report.json`
   - For .NET projects, the report is already generated at `.github/modernize/report.json`
   - This consolidated report should be included in the pull request

## Input Parameters

- `workspace-path` (required): Path to the project to assess

## How to Use

### Prerequisites

**For Java projects**:
- MCP tools must be available: 'appmod-precheck-assessment' and 'appmod-run-assessment'
- If tools are not configured, the skill will return instructions for setup

**For .NET projects**:
- .NET SDK must be installed
- No MCP tools required - appcat will be installed and run directly via .NET CLI
- The assessment will automatically install `dotnet-appcat` tool if not already present

### Triggering Assessment

Simply express the intent to assess the application. Example prompts:

• "Assess the application"
• "Run AppCAT assessment for this project"
• "Analyze this application for Azure migration"

The assessment process automatically:
• Detects project language and framework
• **For Java**: Uses MCP tools to install and run AppCAT
• **For .NET**: Installs dotnet-appcat tool and runs analysis directly
• Executes comprehensive analysis
• Generates report at `.github/modernize/report.json` (or subdirectories for Java)

### Report Consolidation


**For Java projects**:
1. Search for `report.json` files under `.github/modernize/` subdirectories
2. If multiple reports exist, identify the most recently modified one
3. Copy the latest report to `.github/modernize/report.json`
4. Include this consolidated report in the pull request

**For .NET projects**:
1. Report is directly generated at `.github/modernize/report.json`
2. Include this `.g, location depends on project type:

**For Java projects** (via MCP server):
• Initially stored under `.github/modernize/` subdirectories
• Common locations: `.github/modernize/appcat/result/report.json`
• Consolidated to: `.github/modernize/report.json`

**For .NET projects** (direct execution):
• Directly generated at: `.github/modernize/report.json`

Final report location (include this in pull request):
• `.github/modernize/report.json`
• `.github/modernize/appcat/result/report.json`
• `.github/modernize/dotnet-appcat/result/report.json`
• `.github/modernize/repos/report-{timestamp}.json`

The consolidated report is copied to:
• `.github/modernize/report.json` (include this in pull request)

The **For Java**: MCP server is available (or clear instructions provided if not)
• ✅ **For .NET**: .NET SDK is available and dotnet-appcat tool is installed
• ✅ AppCAT analysis executes without errors
• ✅ Report generated at `.github/modernize/report.json`
• ✅ Rata**: Assessment tool version, timestamp, and configuration

## Success Criteria

Assessment is complete when:
• ✅ Assessment MCP server is available (or clear instructions provided if not)
• ✅ AppCAT analysis executes without errors via MCP server
• ✅ Latest report.json located under `.github/modernize/` subdirectories
• ✅ Report consolidated to `.github/modernize/report.json`
• ✅ Consolidated report included in pull request
Prerequisites Not Met**:
• **For Java**: Verify MCP tools are available ('appmod-precheck-assessment' and 'appmod-run-assessment')
  - Return immediately with setup instructions if tools are not available
  - Do not attempt to run assessment without MCP
• **For .NET**: Verify .NET SDK is installed
  - Check with `dotnet --version` command
  - Provide installation instructions if .NET SDK is missing

**Assessment Failures**:
• Unsupported project type (only Java and .NET supported)
• **For Java**: MCP server communication errors
• **For .NET**: 
  - dotnet-appcat tool installation failure
  - dotnet-appcat command execution errors
• Invalid project structure or build configuration

**Report Generation Issues**:
• **For Java**: No report.json found under `.github/modernize/` subdirectories after MCP execution
• **For .NET**: Report not generated at `.github/modernize/report.json`
• Report file is corrupted or invalid JSON

For any failure, provide clear error messages and troubleshooting step/` subdirectories
• Report file is corrupted or invalid JSON

For any failure, provide clear error messages.
