---
name: migration-activemq-servicebus
description: Migrate from ActiveMQ Artemis to Azure Service Bus for messaging.
---

# activemq-servicebus

## Overview

Migrate from ActiveMQ Artemis to Azure Service Bus for messaging.

## Knowledge Base Content

* KB ID: microsoft://message-queue-tasks/activemq-servicebus/activemq-applicationConfig.formula
* Title: Migrate ActiveMQ properties
* Description: Migrate ActiveMQ properties to Azure Service Bus properties
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.{yml,yaml,properties}`
- Regex pattern to find code lines: `/activemq/i`
> you could use tools to search code whatever if possible.
### Instruction

Your task is to migrate the ActiveMQ connection settings to Service Bus connection settings. Please follow these guidelines:

- **DO NOT** optimize the code blocks that are not directly related to the migration changes.
- **KEEP** the commented-out code and minimize the amount of code changes.

1. **Add Service Bus Connection Settings:**
   - For properties starting with `spring.activemq` and named `broker-url`, `username`, or `password`:
     - Add the following Service Bus connection settings:
       - Managed Identity Enabled:
         - Property: `spring.cloud.azure.credential.managed-identity-enabled`
         - Value: `true`
       - Client ID:
         - Property: `spring.cloud.azure.credential.client-id`
         - Value: `${AZURE_CLIENT_ID}`
       - Namespace:
         - Property: `spring.jms.servicebus.namespace`
         - Value: `${SERVICE_BUS_NAMESPACE}`
       - Pricing Tier:
         - Property: `spring.jms.servicebus.pricing-tier`
         - Value: `${PRICING_TIER}`
       - Passwordless Enabled:
         - Property: `spring.jms.servicebus.passwordless-enabled`
         - Value: `true`
     - Remove the ActiveMQ connection properties that match `spring.activemq.{broker-url, username, password}`.

2. **Replace ActiveMQ Resource Settings:**
   - Find properties with the keyword `activemq` in their names and replace `activemq` with `servicebus`.

3. **Update Comments:**
   - Replace the string `activemq` with `Service Bus` in commented-out lines.

4. **Update Docker Compose Files:**
   - If the file is a docker-compose file and contains a container starting with ActiveMQ images, remove the ActiveMQ container and related usages.
* Tags: ActiveMQ, Azure Service Bus, Message Broker, Message Queue, Messaging, Spring, Spring JMS
