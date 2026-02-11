---
name: migration-mi-postgresql-azure-sdk-21v-china
description: Migrate from PostgreSQL to Azure Database for PostgreSQL with Azure SDK and managed identity in the Mooncake cloud for secure, credential-free authentication.
---

# mi-postgresql-azure-sdk-21v-china

## Overview

Migrate from PostgreSQL to Azure Database for PostgreSQL with Azure SDK and managed identity in the Mooncake cloud for secure, credential-free authentication.

## Knowledge Base Content

* KB ID: mi-postgresql-azure-sdk-21v-china
* Title: Via Azure SDK for Mooncake
* Description: Azure Database for PostgreSQL Managed Identity via Azure SDK for 21V China
* Content: 
Your task is to migrate a Java project to use managed identity for authentication in Azure PostgreSQL instead of a password.

1. Get PostgreSQL JDBC URL by searching "jdbc:postgresql" in the project. If there is no match, skip all the rest of the steps.

2. Update the PostgreSQL JDBC URL. To use managed identity for authentication in Azure PostgreSQL, the PostgreSQL JDBC URL should be updated. Follow these steps:
  2.1. Add these parameters to the PostgreSQL JDBC URL:
    - user=${MANAGED_IDENTITY_NAME}
    - sslmode=require&authenticationPluginClassName=com.azure.identity.extensions.jdbc.postgresql.AzurePostgresqlAuthenticationPlugin
    - azure.authorityHost=https://login.partner.microsoftonline.cn
    - azure.scopes=https://ossrdbms-aad.database.chinacloudapi.cn/.default
    - azure.managedIdentityEnabled=true
    - azure.clientId=${MANAGED_IDENTITY_CLIENT_ID}
  2.2. Use environment variable for database host/port/database name if the original value is not Azure PostgreSQL.
  2.3. Add comments about environment variables in the PostgreSQL JDBC URL.
  2.4. Comment out all "username" and "password" related content which are ONLY corresponding to the PostgreSQL JDBC URL. This includes but is not limited to java files (xxx.java), properties files (xxx.yaml / xxx.properties).
  2.5. Example:
     - Example: Property file difference fragment
        ```diff
        - url:  jdbc:postgresql://localhost:5432/testdb
        - username: testuser
        - password: testpass
        + # Remember to set the value for the environment variables in the url value below
        + url: jdbc:postgresql://${PGHOST}:${PGPORT}/${PGDATABASE}?user=${MANAGED_IDENTITY_NAME}&sslmode=require&authenticationPluginClassName=com.azure.identity.extensions.jdbc.postgresql.AzurePostgresqlAuthenticationPlugin&azure.authorityHost=https://login.partner.microsoftonline.cn&azure.scopes=https://ossrdbms-aad.database.chinacloudapi.cn/.default&azure.managedIdentityEnabled=true&azure.clientId=${MANAGED_IDENTITY_CLIENT_ID}
        + # Comment out all content about "username" and "password" because now PostgreSQL will authenticate using managed identity.
        + # username: testuser
        + # password: testpass
        ```
    - Example: Java code difference fragment 1
        ```diff
        - @Value("${spring.shardingsphere.dataSource1.username}")
        - private String username;
        - @Value("${spring.shardingsphere.dataSource1.password}")
        - private String password;
        + // Comment out all content about "username" and "password" because now PostgreSQL will authenticate using managed identity.
        + // @Value("${spring.shardingsphere.dataSource1.username}")
        + // private String username;
        + // @Value("${spring.shardingsphere.dataSource1.password}")
        + // private String password;
        ```
    - Example: Java code difference fragment 2
        ```diff
        - hikariDataSource.setUsername(dataSource1Config.getUsername());
        - hikariDataSource.setPassword(dataSource1Config.getPassword());
        + // Comment out all content about "username" and "password" because now PostgreSQL will authenticate using managed identity.
        + // hikariDataSource.setUsername(dataSource1Config.getUsername());
        + // hikariDataSource.setPassword(dataSource1Config.getPassword());
        ```

3. Add dependency. To use the AzurePostgresqlAuthenticationPlugin in the PostgreSQL JDBC URL, it's necessary to add dependencies.
  3.1. Example: pom file difference
      ```diff
      + <dependency>
      +     <groupId>com.azure</groupId>
      +     <artifactId>azure-identity-extensions</artifactId>
      +     <version>1.2.2</version>
      + </dependency>
      ```
  3.2. Note: Please check the latest compatible version of the dependency, and upgrade the version if possible.
