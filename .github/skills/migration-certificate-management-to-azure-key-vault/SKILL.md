---
name: migration-certificate-management-to-azure-key-vault
description: Migrate from a local KeyStore to Azure Key Vault for secure storage and access to certificates and keys.
---

# certificate-management-to-azure-key-vault

## Overview

Migrate from a local KeyStore to Azure Key Vault for secure storage and access to certificates and keys.

## Knowledge Base Content

* KB ID: microsoft://security-tasks/certificate-management-to-azure-key-vault/java-code.formula
* Title: Migrate TLS/MTLS certificate from local to Azure Key Vault
* Description: Migrate TLS/MTLS certificate management from local storage to Azure Key Vault
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/KeyStore|Certificate|SSLContext/`
> you could use tools to search code whatever if possible.
### Instruction

Your task is to migrate a Java file from managing TLS/MTLS certificates locally (e.g., using KeyStore) to managing certificates in Azure Key Vault JCA while maintaining the same functionality. Below is a reference to the relevant Azure Key Vault APIs and migration examples for your convenience.
Please notes:
Replace `KeyStore` initialization with Azure Key Vault JCA equivalents.         
  - Example:
  ```java
  // Local KeyStore example
  KeyStore keyStore = KeyStore.getInstance("JKS");

  // Azure Key Vault JCA equivalent
  KeyVaultJcaProvider provider = new KeyVaultJcaProvider();
  Security.addProvider(provider);
  KeyStore keyStore = KeyVaultKeyStore.getKeyVaultKeyStoreBySystemProperty();
  ```
Should not remove KeyManagerFactory, need it to initialize SSLContext.
Make sure you add the following Descriptions as Comments if using KeyVaultKeyStore.getKeyVaultKeyStoreBySystemProperty()
  /**
   * Set the following configuration as system properties
   * - `azure.keyvault.uri`: The URI of your Azure Key Vault.
   * - `azure.keyvault.tenant-id`: The tenant ID of your Azure Active Directory.
   * - `azure.keyvault.client-id`: The client ID of your Azure Active Directory application.
   * - `azure.keyvault.client-secret`: The client secret of your Azure Active Directory application.
   */

Ensure the resulting code is clean, efficient, and preserves the original functionality. Keep all irrelevant code/comments unchanged.
