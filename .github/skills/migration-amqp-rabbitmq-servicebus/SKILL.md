---
name: migration-amqp-rabbitmq-servicebus
description: Migrate from RabbitMQ with AMQP to Azure Service Bus for messaging.
---

# amqp-rabbitmq-servicebus

## Overview

Migrate from RabbitMQ with AMQP to Azure Service Bus for messaging.

## Knowledge Base Content

* KB ID: microsoft://message-queue-tasks/rabbitmq-servicebus/amqp-rabbitmq-servicebus/rabbitmq-applicationConfig.formula
* Title: Migrate RabbitMQ properties
* Description: Migrate RabbitMQ properties to Azure Service Bus properties in Spring Messaging
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.{yml,yaml,properties}`
- Regex pattern to find code lines: `/rabbitmq/i`
> you could use tools to search code whatever if possible.
### Instruction

Your task is to migrate the RabbitMQ connection settings to Service Bus connection settings.

*DO NOT* optimize the code blocks not directly related to the migration changes, *KEEP* those commented out code, minimize the amount of code changes.

1. If the property name starts with 'spring.rabbitmq', with name in [host, port, addresses, username, password, virtual-host, ssl.enabled], do
  - Add Service Bus connection settings:
    - managed-identity-enabled
      property: spring.cloud.azure.credential.managed-identity-enabled
      value: true
    - client-id
      property: spring.cloud.azure.credential.client-id
      value: ${AZURE_CLIENT_ID}
    - entity-type
      property: spring.cloud.azure.servicebus.entity-type
      value: queue or topic. Check the dependency file first to analyze the topology of the RabbitMQ, if there are only Spring beans of Rabbit Queue object, then this is a Rabbit queue topology and should be migrated to Service Bus "queue" entity type. 
             If there are also Spring beans of Rabbit Exchange or Binding objects, then this is a Rabbit Exchange topology and should be migrated to Service Bus "topic" entity type.
    - namespace
      property: spring.cloud.azure.servicebus.namespace
      value: ${SERVICE_BUS_NAMESPACE}
  - Remove the RabbitMQ connection properties match 'spring.rabbitmq.{ host, port, addresses, username, password, virtual-host, ssl.enabled }' as well as other Spring Rabbit properties beginning with 'spring.rabbit.'.
    Don't replace these properties' prefix with 'spring.servicebus.'.

2. When adding the above properties in a yaml file, pay attention to the overall structural correctness.

3. Find the comment out line with keyword 'rabbitmq', and find the next comment out line or to the end of file, the properties between these two lines are regarded as RabbitMQ resource settings.
  The properties with keyword 'rabbitmq' in the names are RabbitMQ resource settings.
  - Replace the string 'rabbitmq' with 'Service Bus' in comment out lines.
  - If there are properties with string 'rabbitmq' in the name, replace string 'rabbitmq' with 'servicebus'.

4. If the file is a docker-compose file and there is a container start with rabbitmq images, remove the rabbitmq container and related usages.
* Tags: RabbitMQ, Azure Service Bus, Message Broker, Message Queue, Messaging, AMQP, Spring
