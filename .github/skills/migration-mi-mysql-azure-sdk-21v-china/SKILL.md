---
name: migration-mi-mysql-azure-sdk-21v-china
description: Migrate from MySQL to Azure Database for MySQL with Azure SDK and managed identity in the Mooncake cloud for secure, credential-free authentication.
---

# mi-mysql-azure-sdk-21v-china

## Overview

Migrate from MySQL to Azure Database for MySQL with Azure SDK and managed identity in the Mooncake cloud for secure, credential-free authentication.

## Knowledge Base Content

* KB ID: microsoft://security-tasks/secure-azure-mysql-with-managed-identity/mi-mysql-azure-sdk-21v-china/db-connection.formula
* Title: Upgrade code to use Managed Identity in Azure MySQL (China Cloud)
* Description: Migrate Azure MySQL authentication to managed identity approach using AzureMysqlAuthenticationPlugin.
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/DriverManager/`
> you could use tools to search code whatever if possible.
### Instruction

Your task is to migrate a java file from using a connection string to using passwordless managed identity for authentication in Azure MySQL (China Cloud).
Ensure the resulting code is clean, efficient, and preserves the original functionality.
Please ensure to follow the guidance below to complete this task:
1. Remove password Usage: Eliminate the hardcoded password in the connection string.
2. Replace the value of user name with managed identity for the database connection: Please use the name of managed identity to replace the value of the user name for PostgreSQL database connection.
3. Add Authentication Plugin Config: Please add a new string variable for authenticationPluginClassNameConfig. The value should be exactly this string "&authenticationPlugins=com.azure.identity.extensions.jdbc.mysql.AzureMysqlAuthenticationPlugin"
4. Append the mentioned authenticationPluginClassNameConfig to the connection string url.
5. Use the updated connection string url to get Connection.

Below are the APIs provided for your reference:

Class: DriverManager
  Description: The basic service for managing a set of JDBC drivers.
  Package: java.sql
  Methods:
    getConnection(String url): Attempts to establish a connection to the given database URL.
    getConnection(String url, Properties info): Attempts to establish a connection to the given database URL.
