
### Supported Task Patterns with Skill Definitions
These patterns have pre-defined skills to assist in their execution. When they are selected in a modernization plan, the corresponding skills should be used.
Each of the item is written in the following format: `- **skill-name**: skill-description`.

- **migration-AWS-secrets-manager-to-azure-key-vault**: Migrate from AWS Secrets Manager to Azure Key Vault to securely manage and access sensitive information in Azure.
- **migration-activemq-servicebus**: Migrate from ActiveMQ Artemis to Azure Service Bus for messaging.
- **migration-amqp-rabbitmq-servicebus**: Migrate from RabbitMQ with AMQP to Azure Service Bus for messaging.
- **migration-ant-project-to-maven-project**: Migrate current project from Ant project to Maven project
- **migration-apache-commons-jcs-to-azure-cache-for-redis**: Migrate from Apache Commons JCS in-process cache to Azure Cache for Redis.
- **migration-apache-ignite-to-azure-cache-redis**: Migrate from Apache Ignite distributed cache to Azure Cache for Redis.
- **migration-certificate-management-to-azure-key-vault**: Migrate from a local KeyStore to Azure Key Vault for secure storage and access to certificates and keys.
- **migration-containerization-copilot-agent**: The app does not have a Dockerfile and/or is not container-ready. Use Agent Mode with Copilot to create and execute a containerization plan.
- **migration-deprecated-api-upgrade**: Upgrade deprecated APIs to their recommended alternatives for improved security, performance, and compatibility.
- **migration-dynacache-to-azure-cache-for-redis**: Migrate from DynaCache to Azure Cache for Redis.
- **migration-eclipse-project-to-maven-project**: Migrate current project from eclipse project to maven project
- **migration-ehcache-to-azure-cache-for-redis**: Migrate from Ehcache in-process cache to Azure Cache for Redis.
- **migration-embedded-cache-to-azure-cache-for-redis**: Migrate from embedded cache to Azure Cache for Redis for a scalable, managed solution that easily integrates with other Azure services.
- **migration-hazelcast-to-azure-cache-for-redis**: Migrate from Hazelcast distributed cache to Azure Cache for Redis.
- **migration-infinispan-to-azure-cache-redis**: Migrate from Infinispan distributed cache to Azure Cache for Redis.
- **migration-jakarta-ee-upgrade**: Upgrade to the latest stable version of Jakarta EE for improved security, performance, and compatibility.
- **migration-java-ee-amqp-rabbitmq-servicebus**: Migrate from RabbitMQ with AMQP to Azure Service Bus for messaging in Java EE/Jakarta EE applications.
- **migration-java-version-upgrade**: Upgrade to the latest stable version of Java for improved security, performance, and compatibility.
- **migration-javax.email-send-to-azure-communication-service-email**: Migrate from Javax Email to Azure Communication Service for sending emails.
- **migration-jax-rpc-to-jax-ws**: Migrate from JAX-RPC to JAX-WS for web services. JAX-RPC is deprecated and JAX-WS is the recommended alternative.
- **migration-jboss-cache-to-azure-cache-for-redis**: Migrate from JBoss Cache to Azure Cache for Redis.
- **migration-jcache-to-azure-cache-for-redis**: Migrate from JCache (JSR-107) to Azure Cache for Redis for a scalable, managed solution that easily integrates with other Azure services.
- **migration-kafka-to-eventhubs**: Migrate from Kafka to Azure Event Hubs for Apache Kafka with managed identity for secure, credential-free authentication.
- **migration-local-files-to-mounted-azure-storage**: Migrate from local file system to Azure Storage Account File Share mounts for scalable and secure file storage.
- **migration-local-redis-to-azure-redis-cache**: Migrate from a local Redis instance to Azure Cache for Redis.
- **migration-local-session-to-azure-redis-cache**: Migrate from local session storage to Azure Cache for Redis for better scalability and distributed session management.
- **migration-log-to-console**: Migrate from file-based logging to console logging to support cloud-native apps and integration with Azure Monitor.
- **migration-memcached-to-azure-cache-for-redis**: Migrate from Memcached distributed cache to Azure Cache for Redis.
- **migration-mi-azuresql-azure-sdk-21v-china**: Migrate from SQL Database to Azure SQL Database with Azure SDK and managed identity in Mooncake for secure, credential-free authentication.
- **migration-mi-azuresql-azure-sdk-public-cloud**: Migrate from SQL Database to Azure SQL Database with Azure SDK and managed identity for secure, credential-free authentication.
- **migration-mi-cassandra-azure-sdk-public-cloud**: Migrate from Cassandra to Azure Cosmos DB for Cassandra for a fully managed, scalable database with Cassandra API support.
- **migration-mi-mariadb-azure-sdk-public-cloud**: Migrate from MariaDB to Azure Database for MariaDB with managed identity for secure, credential-free authentication.
- **migration-mi-mongodb-azure-sdk-public-cloud**: Migrate from MongoDB to Azure Cosmos DB for MongoDB with managed identity for a fully managed, scalable database service with MongoDB API support.
- **migration-mi-mysql-azure-sdk-21v-china**: Migrate from MySQL to Azure Database for MySQL with Azure SDK and managed identity in the Mooncake cloud for secure, credential-free authentication.
- **migration-mi-mysql-azure-sdk-public-cloud**: Migrate from MySQL to Azure Database for MySQL with Azure SDK and managed identity for secure, credential-free authentication.
- **migration-mi-postgresql-azure-sdk-21v-china**: Migrate from PostgreSQL to Azure Database for PostgreSQL with Azure SDK and managed identity in the Mooncake cloud for secure, credential-free authentication.
- **migration-mi-postgresql-azure-sdk-public-cloud**: Migrate from PostgreSQL to Azure Database for PostgreSQL with Azure SDK and managed identity for secure, credential-free authentication.
- **migration-on-premises-user-authentication-to-microsoft-entra-id**: Migrate the user authentication to Microsoft Entra ID authentication
- **migration-oracle-coherence-to-azure-cache-for-redis**: Migrate from Oracle Coherence distributed cache to Azure Cache for Redis.
- **migration-oracle-to-postgresql**: Migrate from Oracle DB to PostgreSQL
- **migration-oscache-to-azure-cache-for-redis**: Migrate from OSCache in-process cache to Azure Cache for Redis.
- **migration-plaintext-credential-to-azure-keyvault**: Migrate from plaintext credentials in the code to Azure Key Vault for storage and access to sensitive information.
- **migration-s3-to-azure-blob-storage**: Migrate from AWS S3 to Azure Blob Storage for scalable and secure object storage in Azure.
- **migration-shift-one-to-azure-cache-for-redis**: Migrate from ShiftOne in-process cache to Azure Cache for Redis.
- **migration-spring-boot-upgrade**: Upgrade to the latest stable version of Spring Boot for improved security, performance, and compatibility.
- **migration-spring-cache-backends-to-spring-cache-with-azure-cache-for-redis**: Migrate from Spring Cache to Azure Cache for Redis for a scalable, managed solution that easily integrates with other Azure services.
- **migration-spring-framework-upgrade**: Upgrade to the latest stable version of Spring Framework for improved security, performance, and compatibility.
- **migration-spring-jms-rabbitmq-servicebus**: Migrate from RabbitMQ with JMS to Azure Service Bus for a managed messaging service with JMS API support.
- **migration-sqs-to-servicebus**: Migrate from AWS Simple Queue Service to Azure Service Bus for a managed messaging service with advanced features.
- **migration-swarm-cache-to-azure-cache-for-redis**: Migrate from Swarm Cache to Azure Cache for Redis.


### Supported Task Patterns without Skill Definitions
These patterns do not have pre-defined skills. When they are selected in a modernization plan, prepare a prompt based on the description to guide the AI in performing the required tasks.

- Migrate from Amazon Kinesis to Azure Event Hubs for scalable and secure event streaming in Azure.
- Migrate from Amazon SNS to Azure Service Bus for scalable and secure messaging in Azure.
- Migrate from Apache Pulsar to Azure Event Hubs for scalable and secure event streaming in Azure.
- Migrate from AWS Lambda to Azure Functions for scalable and secure serverless compute in Azure.
- Migrate from Firebird to Azure PostgreSQL for scalable and secure database management in Azure.
- Migrate from Google Cloud Bigtable to Azure Cosmos DB for scalable and secure NoSQL database management in Azure.
- Migrate from Google Cloud Functions to Azure Functions for scalable and secure serverless compute in Azure.
- Migrate from Google Pub/Sub to Azure Service Bus for reliable and secure messaging in Azure.
- Migrate from Google Cloud Spanner to Azure PostgreSQL for scalable and secure database management in Azure.
- Migrate from Google Cloud Storage to Azure Blob Storage for scalable and secure object storage in Azure.
- Migrate from Google Firestore to Azure Cosmos DB for scalable and secure NoSQL database management in Azure.
- Migrate from IBM DB2 to Azure PostgreSQL for scalable and secure database management in Azure.
- Migrate from IBM JMS to Azure Service Bus for messaging.
- Migrate from Quartz Scheduler to Azure Functions for serverless, event-driven task scheduling in Azure.
- Migrate from Solace PubSub+ to Azure Service Bus for scalable and secure messaging in Azure.
- Migrate from Spring Batch to Azure Durable Functions for scalable and secure serverless compute in Azure.
- Migrate from Spring Cloud Config to Azure App Configuration for scalable and secure configuration management in Azure.
- Migrate from SQLite to Azure PostgreSQL for scalable and secure database management in Azure.
- Migrate from Sybase ASE to Azure PostgreSQL for scalable and secure database management in Azure.
- Migrate from TIBCO EMS JMS to Azure Service Bus for scalable and secure messaging in Azure.

