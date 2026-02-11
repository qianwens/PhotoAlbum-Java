---
name: migration-log-to-console
description: Migrate from file-based logging to console logging to support cloud-native apps and integration with Azure Monitor.
---

# log-to-console

## Overview

Migrate from file-based logging to console logging to support cloud-native apps and integration with Azure Monitor.

## Knowledge Base Content

* KB ID: microsoft://storage-tasks/log-to-console/java.formula
* Title: Update Java code to log to console
* Description: Update the Java code to ensure logs are output only to the console
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/FileAppender|FileWriter|FileHandler|SocketHandler/`
> you could use tools to search code whatever if possible.
### Instruction

Your goal is ensure the logger in java code has these features:
1. If there is no log related content in the java file, then do nothing.
2. If there is log related content in the java file, then make sure:
  2.1. Log not output to file
  2.2. Ensure log output to console
* Tags: logging, log to console, console output, logback, log4j2, log4j
