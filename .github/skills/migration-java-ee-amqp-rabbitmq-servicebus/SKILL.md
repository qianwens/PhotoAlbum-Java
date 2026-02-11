---
name: migration-java-ee-amqp-rabbitmq-servicebus
description: Migrate from RabbitMQ with AMQP to Azure Service Bus for messaging in Java EE/Jakarta EE applications.
---

# java-ee-amqp-rabbitmq-servicebus

## Overview

Migrate from RabbitMQ with AMQP to Azure Service Bus for messaging in Java EE/Jakarta EE applications.

## Knowledge Base Content

* KB ID: microsoft://java-ee-amqp-rabbitmq-servicebus/java-ee-amqp-rabbitmq-servicebus.formula
* Title: Migrate Java EE/Jakarta EE project from RabbitMQ AMQP client to Azure Service Bus
* Description: Migrate Java EE/Jakarta EE project from RabbitMQ AMQP client to Azure Service Bus
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.{java,xml,properties}`
- Regex pattern to find code lines: `/rabbitmq|amqp-client|com\.rabbitmq|ConnectionFactory|Channel|Connection|DeliverCallback|Delivery|basicPublish|basicConsume|queueDeclare|exchangeDeclare/`
> you could use tools to search code whatever if possible.
### Instruction

Before starting the migration, analyze the project structure:
1. Identify all Maven/Gradle dependencies containing "rabbitmq" or "amqp-client"
2. Find Java files importing com.rabbitmq.client.* packages
3. Understand the messaging patterns:
   - Publisher pattern: Uses Channel.basicPublish()
   - Consumer pattern: Uses Channel.basicConsume() or DeliverCallback
   - Queue/Exchange declarations
4. Note connection parameters (host, port, credentials, virtual host)
5. Document message routing keys and queue/exchange names


### Instruction

Replace RabbitMQ dependencies with Azure Service Bus:
1. Remove RabbitMQ AMQP client dependency:
   - Maven: Remove com.rabbitmq:amqp-client
   - Gradle: Remove implementation 'com.rabbitmq:amqp-client'
2. Add Azure Service Bus dependency:
   - Maven: Add com.azure:azure-messaging-servicebus:7.17.14
   - Gradle: Add implementation 'com.azure:azure-messaging-servicebus:7.17.14'
3. Update dependency management sections if present
4. Remove any RabbitMQ version properties from pom.xml/build.gradle


### Instruction

For better organization, consider renaming RabbitMQ-specific packages:
1. Rename packages containing "rabbitmq" to "servicebus" or equivalent
2. Update all package declarations in affected Java files
3. Update all import statements referencing the old package names
4. Update Spring/CDI configuration files referencing old package names


### Instruction

Replace RabbitMQ publisher code with Azure Service Bus sender:
1. Replace RabbitMQ imports:
   - Remove: com.rabbitmq.client.{ConnectionFactory, Connection, Channel}
   - Add: com.azure.messaging.servicebus.{ServiceBusClientBuilder, ServiceBusSenderClient, ServiceBusMessage}
2. Replace connection setup:
   - Old: ConnectionFactory + host/port/credentials
   - New: ServiceBusClientBuilder with connection string
3. Replace publishing logic:
   - Old: channel.basicPublish(exchange, routingKey, props, messageBytes)
   - New: senderClient.sendMessage(new ServiceBusMessage(messageBody))
4. Handle message properties:
   - Old: Routing keys in basicPublish()
   - New: Message properties via ServiceBusMessage.getApplicationProperties()
5. Update constructor parameters to accept connection string instead of individual connection parameters
6. Add proper resource cleanup with sender.close()


### Instruction

Replace RabbitMQ consumer code with Azure Service Bus processor/receiver:
1. Replace RabbitMQ imports:
   - Remove: com.rabbitmq.client.{DeliverCallback, Delivery, Consumer}
   - Add: com.azure.messaging.servicebus.{ServiceBusProcessorClient, ServiceBusReceivedMessage, ServiceBusReceivedMessageContext}
2. Replace consumer setup:
   - Old: channel.basicConsume(queue, autoAck, deliverCallback, consumerTag -> {})
   - New: ServiceBusProcessorClient with processMessage and processError handlers
3. Replace message processing:
   - Old: DeliverCallback with delivery.getBody()
   - New: processMessage method with ServiceBusReceivedMessage.getBody()
4. Implement proper message acknowledgment:
   - Old: Auto-ack or manual channel.basicAck()
   - New: context.complete() for success, context.abandon() for retry
5. Add error handling with processError method
6. Update lifecycle methods (start/stop processor)


### Instruction

Replace RabbitMQ configuration with Azure Service Bus settings:
1. Spring XML configuration (beans.xml):
   - Update package names in bean class attributes
   - Replace RabbitMQ connection parameters (host, port, username, password, virtualHost, queueName)
   - With Azure Service Bus parameters (connectionString, topicName/queueName, subscriptionName if using topics)
2. Properties files:
   - Remove rabbitmq.* properties
   - Add azure.servicebus.* properties
   - Include connection string, topic/queue names, retry settings
3. Environment variables:
   - Replace RABBITMQ_* variables with AZURE_SERVICEBUS_CONNECTION_STRING
4. Application configuration classes:
   - Update @ConfigurationProperties annotations
   - Update field names and types for Azure Service Bus configuration


### Instruction

Apply proper architectural mapping:
1. Messaging Patterns:
   - RabbitMQ Exchange → Azure Service Bus Topic
   - RabbitMQ Queue → Azure Service Bus Queue or Subscription
   - RabbitMQ Routing Key → Azure Service Bus Message Properties
2. Connection Management:
   - RabbitMQ ConnectionFactory → ServiceBusClientBuilder
   - RabbitMQ Channel → ServiceBusSenderClient or ServiceBusProcessorClient
3. Message Handling:
   - RabbitMQ Delivery → ServiceBusReceivedMessage
   - RabbitMQ Properties → ServiceBusMessage application properties
4. Durability and Reliability:
   - RabbitMQ durable queues → Azure Service Bus queues (always durable)
   - RabbitMQ acknowledgments → Service Bus complete/abandon/defer


### Instruction

Refactor method calls to use new Azure Service Bus APIs:
1. Update method names to reflect new functionality:
   - publishToRabbitMQ() → sendToServiceBus()
   - consumeFromRabbitMQ() → receiveFromServiceBus()
   - createRabbitMQEntries() → createServiceBusEntries()
2. Update method signatures:
   - Remove RabbitMQ-specific parameters
   - Add Azure Service Bus connection string parameter
   - Update return types if needed
3. Update exception handling:
   - Remove RabbitMQ-specific exceptions
   - Add Azure Service Bus exception handling
4. Update logging messages to reference Service Bus instead of RabbitMQ


### Instruction

Provide configuration templates and documentation:
1. Create servicebus.properties with:
   - Connection string template
   - Topic/queue names
   - Retry policies
   - Timeout settings
2. Create migration documentation (AZURE_SERVICE_BUS_MIGRATION.md):
   - Architecture mapping table
   - Configuration instructions
   - Azure Service Bus setup steps
   - Benefits of the migration
   - Testing guidelines
3. Update README files with new setup instructions
4. Include environment variable examples


### Instruction

Ensure the migration is successful:
1. Run clean compile to verify all code compiles
2. Run full package build to ensure deployable artifacts are created
3. Check for any remaining RabbitMQ references:
   - Search for "rabbitmq", "amqp", "com.rabbitmq" in code
   - Verify only documentation and comments reference old system
4. Validate Azure Service Bus dependencies are included in final artifacts
5. Test connection string configuration
6. Verify message processing logic is preserved
7. Run integration tests if available


### Instruction

Maintain application functionality during migration:
1. Keep existing message format and parsing logic unchanged
2. Preserve message content structure and serialization
3. Maintain the same business logic for message processing
4. Keep existing error handling patterns for message processing failures
5. Preserve message ordering and delivery semantics where possible
6. Maintain existing logging and monitoring for message flows
7. Keep existing timeout and retry behavior equivalent
* Tags: RabbitMQ, Azure Service Bus, Message Broker, Message Queue, Messaging, AMQP, Java EE, Jakarta EE
