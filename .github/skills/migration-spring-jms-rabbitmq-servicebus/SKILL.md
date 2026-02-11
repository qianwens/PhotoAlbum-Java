---
name: migration-spring-jms-rabbitmq-servicebus
description: Migrate from RabbitMQ with JMS to Azure Service Bus for a managed messaging service with JMS API support.
---

# spring-jms-rabbitmq-servicebus

## Overview

Migrate from RabbitMQ with JMS to Azure Service Bus for a managed messaging service with JMS API support.

## Knowledge Base Content

* KB ID: microsoft://message-queue-tasks/rabbitmq-servicebus/spring-jms-rabbitmq-servicebus/rabbitmq-ConnectionFactory.formula
* Title: Migrate RabbitMQ ConnectionFactory
* Description: Remove RabbitMQ ConnectionFactory
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/RMQConnectionFactory/`
> you could use tools to search code whatever if possible.
### Instruction

Your task is to migrate a Java file using the RabbitMQ RMQConnectionFactory methods while maintaining the same functionality.
Spring JMS RabbitMQ has to define a RMQConnectionFactory bean to init connection to the rabbitmq server. In Service Bus, it automatically
provides a bean of ConnectionFactory to connect to Azure Service Bus Instance.
So you need to remove the ConnectionFactory code, reference and all the class variables used by ConnectionFactory from RabbitMQ.
The variables used by ConnectionFactory can include [host, port, username, password, virtual-host, ssl.enabled]

Below are the APIs provided for your reference:
Class: RMQConnectionFactory
  Package: com.rabbitmq.jms.admin

Important guidelines:

1. Remove RMQConnectionFactory Bean:
    - Completely remove any beans, reference, configurations and variables related to RabbitMQ RMQConnectionFactory
    - DO NOT create any Service Bus ConnectionFactory beans as replacements
    - Example of code to remove ConnectionFactory bean entirely:
      ```java
      import com.rabbitmq.jms.admin.RMQConnectionFactory;
      // ignore other imports irrelevant with jms

      @Bean
      public ConnectionFactory connectionFactory() {
          RMQConnectionFactory factory = new RMQConnectionFactory();
          factory.setHost(properties.getHost());
          factory.setPort(properties.getPort());
          factory.setUsername(properties.getUsername());
          factory.setPassword(properties.getPassword());
          factory.setVirtualHost(properties.getVirtualHost());
          factory.setSsl(properties.isSslEnabled());
          return factory;
      }
      ```
    - When other beans depend on the ConnectionFactory bean creation method, modify their method signatures to add ConnectionFactory as a parameter instead of calling the factory method directly:
      ```java
      // before
      @Bean
      public ConnectionFactory connectionFactory(){
        RMQConnectionFactory connectionFactory = new RMQConnectionFactory();
        connectionFactory.setUsername(rabbitProps.getUsername());
        connectionFactory.setPassword(rabbitProps.getPassword());
        connectionFactory.setHost(rabbitProps.getHost());
        connectionFactory.setPort(5672);
        return connectionFactory;
      }

      @Bean
      public JmsTemplate jmsTemplate() {
        return new JmsTemplate(connectionFactory());
      }

      //after
      @Bean
      public JmsTemplate jmsTemplate(ConnectionFactory connectionFactory) {
        return new JmsTemplate(connectionFactory);
      }
      ```

2. Import Cleanup:
   - All imports from packages starting with 'com.rabbitmq.jms'
   - Any other unused imports that were related to RabbitMQ
* Tags: RabbitMQ, Azure Service Bus, Message Broker, Message Queue, Messaging, Spring JMS, Spring
