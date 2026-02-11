---
name: migration-plaintext-credential-to-azure-keyvault
description: Migrate from plaintext credentials in the code to Azure Key Vault for storage and access to sensitive information.
---

# plaintext-credential-to-azure-keyvault

## Overview

Migrate from plaintext credentials in the code to Azure Key Vault for storage and access to sensitive information.

## Knowledge Base Content

* KB ID: microsoft://security-tasks/plaintext-credential-to-azure-keyvault/plaintext-credential-in-code.formula
* Title: Migrate plaintext credentials in Java to use Azure Key Vault
* Description: Migrate plaintext credentials in Java files to Azure Key Vault for secure storage and retrieval.
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/(password|secret|key|connectionString|credential|token|apiKey)[\s]*=[\s]*[\"\'"][^\"\';]*[\"\']|(private|public|protected|static|final)*[\s]+(String|char\[\])[\s]+(password|secret|key|connectionString|credential|token|apiKey)[\s]*=[\s]*[\"\'"][^\"\';]*[\"\']|[\.]put[\s]*\([\s]*[\"\'](password|secret|key|connectionString|credential|token|apiKey)[\"\']([\s]*,[^;\)]*)*[\s]*[\"\'"][^\"\';]*[\"\']/`
> you could use tools to search code whatever if possible.
### Instruction

Applicable condition: Don't take the test file into consideration.
Your task is to migrate any java file from using the plaintext credential to leverage Azure Key Vault to managed the credentials.
Here are the steps:
  1. You have to make sure this is really a plaintext sensitive credential in java file before editing it. It must be in a string formula with password you can directly read.
    Ignore all other cases like a pass-in parameter, a variable read from environment variable or other config service.
    - ONLY modify sensitive credentials that are hardcoded directly in the source code
      * Example of sensitive credentials to modify: passwords, API keys, tokens, encryption keys, connection strings containing passwords
      * For example: `private final String dbPassword = "password123";` should be modified
    - DO NOT modify the following cases and leave them unchanged:
      * Regular configuration that isn't sensitive (URLs, hostnames, port numbers, usernames, database names)
        For example: `private final String dbUrl = "jdbc:mysql://localhost:3306/mydb";` should NOT be modified
      * Test cases and test files should be excluded from editing.
      * Code that calls a bean/service/method to retrieve a secret, including getter & setter functions
      * Code that reads credentials from environment variables, property files, or configuration systems
      * Code that directly or indirectly retrieves credentials from method parameters or dynamic context
        - For example:
          ```
          public boolean login(String email, String password) {
              PreparedStatement st = conn.prepareStatement("SELECT * FROM user WHERE email = ? AND password = ?");
              st.setString(1, email);
              st.setString(2, password); // This should NOT be replaced with Azure Key Vault logic
          }
          ```
          ```
          String password = request.getParameter("password").trim();
          ```
          This should NOT be replaced with Azure Key Vault logic.
      * Any code that already uses a credential management system
    - We only want to modify the actual implementation where plaintext sensitive credentials are directly defined
  2. Base on the following API provided, leverage Azure Key Vault to manage the credential.

Here are the APIs for your reference:

If you want to read a secret from the Azure Key Vault, keep in mind always use `new DefaultAzureCredentialBuilder().build()` as your best choice. Here is a sample code:
Don't forget to import the package for the `SecretClient` & `SecretClientBuilder` & `KeyVaultSecret`
```
// Please replace with your own Key Vault URI and <secret-name>
SecretClient secretClient = new SecretClientBuilder()
  .vaultUrl("<your-key-vault-url>")
  .credential(new DefaultAzureCredentialBuilder().build())
  .buildClient();

KeyVaultSecret secret = secretClient.getSecret("<secret-name>");
```
