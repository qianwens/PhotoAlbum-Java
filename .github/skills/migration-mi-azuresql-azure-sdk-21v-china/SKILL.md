---
name: migration-mi-azuresql-azure-sdk-21v-china
description: Migrate from SQL Database to Azure SQL Database with Azure SDK and managed identity in Mooncake for secure, credential-free authentication.
---

# mi-azuresql-azure-sdk-21v-china

## Overview

Migrate from SQL Database to Azure SQL Database with Azure SDK and managed identity in Mooncake for secure, credential-free authentication.

## Knowledge Base Content

* KB ID: microsoft://security-tasks/secure-azure-sql-with-managed-identity/mi-azuresql-azure-sdk-21v-china/db-connection.formula
* Title: Upgrade code to use Managed Identity in Azure SQL (China Cloud)
* Description: Migrate SQL Server authentication to use Azure Managed Identity with ActiveDirectoryMSI in China Cloud.
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/SQLServerDataSource/`
> you could use tools to search code whatever if possible.
### Instruction

Your task is to migrate a java file from using a connection string to using passwordless managed identity for authentication in Azure SQL (China Cloud).
Ensure the resulting code is clean, efficient, and preserves the original functionality.
Please ensure to follow the guidance below to complete this task:
1. Remove user and password usage: Eliminate the hardcoded user and password in the connection string.
2. Please add a variable for the Azure client ID of Azure managed identity.
3. Please append msiClientId to the connection string url: ";msiClientId=" + <azure managed identity client id>
4. Please append this exact string of authentication to the connection string url: ";authentication=ActiveDirectoryMSI"
5. Use the updated connection string url for SQLServerDataSource when set url.

Below are the APIs provided for your reference:

Class: SQLServerDataSource
  Description: Represents a list of properties specific to connecting to a SQL Server database by using a SQLServerConnection object.
  Package: com.microsoft.sqlserver.jdbc
  Implements: ISQLServerDataSource, DataSource, java.io.Serializable, javax.naming.Referenceable
  Contructor:
    SQLServerDataSource(): Initializes a new instance of the SQLServerDataSource class.
  Methods:
    setUrl(String url): Sets the URL that is used to connect to the data source.
    getURL(): Returns the URL used to connect to the data source.
    getConnection(): 	Tries to establish a connection with the data source that this SQLServerDataSource object represents.
