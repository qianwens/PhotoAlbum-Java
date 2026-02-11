---
name: migration-kafka-to-eventhubs
description: Migrate from Kafka to Azure Event Hubs for Apache Kafka with managed identity for secure, credential-free authentication.
---

# kafka-to-eventhubs

## Overview

Migrate from Kafka to Azure Event Hubs for Apache Kafka with managed identity for secure, credential-free authentication.

## Knowledge Base Content

* KB ID: microsoft://message-queue-tasks/kafka-to-eventhubs/dependency.formula
* Title: Add Spring Cloud Azure Starter for Kafka dependencies to use passwordless connections with Azure Event Hubs for Kafka
* Description: Add Spring Cloud Azure Starter dependency (pom.xml for maven dependency or build.gradle or build.gradle.kts for gradle dependency) for Azure Event Hubs for Kafka passwordless support
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/{pom.xml,build.gradle,build.gradle.kts}`
- Regex pattern to find code lines: `/spring-boot-starter-kafka|spring-kafka|spring-kafka-streams|spring-integration-kafka|spring-cloud-stream-binder-kafka|spring-cloud-starter-stream-kafka|spring-cloud-stream-binder-kafka-streams/`
> you could use tools to search code whatever if possible.
### Instruction

In pom.xml or build.gradle or build.gradle.kts: when there is any of the Spring dependencies for Kafka, then Add the Spring Cloud Azure Starter as well as the Spring Cloud Azure BOM. 
Only add the required dependencies, don't modify other lines and keep the changes minimized.

Add the Spring Cloud Azure dependencies:
1. Managed dependency:
  groupId: com.azure.spring
  artifactId: spring-cloud-azure-dependencies
  version: 5.22.0
  scope: import
  type: pom
  Note:
    - If the code is using Spring Boot 2.x, be sure to set the spring-cloud-azure-dependencies version to 4.19.0. If the code is using Spring Boot 3.x, Please check the latest version of the dependency, and update the version if possible.
    - Define a new property named spring-cloud-azure.version for spring-cloud-azure-dependencies.
    - This Bill of Material (BOM) should be configured in the <dependencyManagement> section for pom.xml
    - This Bill of Material (BOM) should be imported with the "platform" keyword for build.gradle or build.gradle.kts files. 
2. Dependencies:
  groupId: com.azure.spring
  artifactId: spring-cloud-azure-starter
