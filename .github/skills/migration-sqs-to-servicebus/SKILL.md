---
name: migration-sqs-to-servicebus
description: Migrate from AWS Simple Queue Service to Azure Service Bus for a managed messaging service with advanced features.
---

# sqs-to-servicebus

## Overview

Migrate from AWS Simple Queue Service to Azure Service Bus for a managed messaging service with advanced features.

## Knowledge Base Content

* KB ID: microsoft://message-queue-tasks/sqs-to-servicebus/sqs-ApplicationConfiguration.formula
* Title: Migrate AWS Simple Queue Service Application Configuration
* Description: Migrate AWS Simple Queue Service (SQS) Application Configuration
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.{yml,yaml,properties}`
- Regex pattern to find code lines: `/sqs/i`
> you could use tools to search code whatever if possible.
### Instruction

Remove all AWS Simple Queue Service configuration properties as Azure Service Bus uses different configuration patterns.
Look for properties containing "aws.sqs" or "sqs" in their names and delete them.
