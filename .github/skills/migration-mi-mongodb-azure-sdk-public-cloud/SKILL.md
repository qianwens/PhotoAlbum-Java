---
name: migration-mi-mongodb-azure-sdk-public-cloud
description: Migrate from MongoDB to Azure Cosmos DB for MongoDB with managed identity for a fully managed, scalable database service with MongoDB API support.
---

# mi-mongodb-azure-sdk-public-cloud

## Overview

Migrate from MongoDB to Azure Cosmos DB for MongoDB with managed identity for a fully managed, scalable database service with MongoDB API support.

## Knowledge Base Content

* KB ID: microsoft://security-tasks/mi-mongodb-azure-sdk-public-cloud/db-connection.formula
* Title: Update Java code to connect to Azure Cosmos DB for MongoDB via Service Connector in Azure public cloud
* Description: Update Java code to make Java application or Spring Boot application connect to Azure Cosmos DB for MongoDB via Service Connector in Azure public cloud
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/MongoClient/`
> you could use tools to search code whatever if possible.
### Instruction

Your task is to update Java code to connect to Azure Cosmos DB for MongoDB via Service Connector in Azure public cloud.

1. For applications that have the dependency "spring-boot-starter-data-mongodb" and do not create their own MongoClient:
  Do nothing, because properties with prefix "spring.data.mongodb" will be injected as environment variables.

2. For other Java applications that create their own MongoClient, create a MongoClient with a password retrieved by an Azure AD token.
  2.1. Only update files that create MongoClient, not files that just use it as a parameter.
  2.2. Merge the following template code fragment into existing code:
    ```java
    import java.net.URI;
    import java.net.http.HttpClient;
    import java.net.http.HttpRequest;
    import java.net.http.HttpResponse;
    import java.util.List;
    import java.util.Map;
    import com.azure.core.credential.AccessToken;
    import com.azure.core.credential.TokenRequestContext;
    import com.azure.identity.DefaultAzureCredential;
    import com.azure.identity.DefaultAzureCredentialBuilder;
    import com.mongodb.MongoClient;
    import com.mongodb.MongoClientURI;
    import org.json.simple.JSONObject;
    import org.json.simple.parser.JSONParser;

        try {
            String listConnectionStringUrl = System.getenv("AZURE_COSMOS_LISTCONNECTIONSTRINGURL");
            String scope = System.getenv("AZURE_COSMOS_SCOPE");

            // If possible, inject DefaultAzureCredential as a bean instead of creating it directly here
            DefaultAzureCredential defaultCredential = new DefaultAzureCredentialBuilder().build();

            // Get the access token.
            AccessToken accessToken = defaultCredential.getToken(new TokenRequestContext().addScopes(new String[]{ scope })).block();
            String token = accessToken.getToken();

            // Get the password.
            HttpClient client = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1) // Without this line, will cause a runtime error such as: HTTP Error 411. The request must be chunked or have a content length
                .build();
            HttpRequest request = HttpRequest.newBuilder()
                .uri(new URI(listConnectionStringUrl))
                .header("Authorization", "Bearer " + token)
                .POST(HttpRequest.BodyPublishers.noBody())
                .build();
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            JSONParser parser = new JSONParser();
            JSONObject responseBody = parser.parse(response.body());
            List<Map<String, String>> connectionStrings = responseBody.get("connectionStrings");
            String connectionString = connectionStrings.get(0).get("connectionString");

            // Connect to Azure Cosmos DB for MongoDB
            MongoClientURI uri = new MongoClientURI(connectionString);
            MongoClient mongoClient = new MongoClient(uri);
        } catch (Exception e) {
            throw new RuntimeException("Failed to create MongoClient", e);
        }
      ```
  2.3. Remove all comments from the template code.
  2.4. When both the environment variable name from new added code and original code can be used, use the new added one.
  2.5. Keep other MongoClient configuration related code in existing code.
  2.6. For Spring beans, don't create DefaultAzureCredential as a local variable, inject it as a bean instead.
    2.6.1. Prefer this way in Spring bean definition methods: Define DefaultAzureCredential as a bean, and inject DefaultAzureCredential as a beane.
      ```java
      import com.azure.core.credential.TokenCredential;
      import com.azure.identity.DefaultAzureCredentialBuilder;
      import com.mongodb.MongoClient;
      import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
      import org.springframework.context.annotation.Bean;

      // Important: Add bean definition in case it's not defined in other places.
      @Bean
      @ConditionalOnMissingBean // Add this in case it's defined in other places.
      public TokenCredential credential() { // Caution: the return type is TokenCredential
        return new DefaultAzureCredentialBuilder().build(); // Import DefaultAzureCredentialBuilder and use its simple name rather than using fully qualified name.
      }
      // Inject TokenCredential as bean
      @Bean
      public MongoClient mongoClient(TokenCredential credential) {
        // Use credential here.
        return ...
      }
      ```
    2.6.2. Avoid this way in Spring bean definition methods: Create DefaultAzureCredential as a local variable
      ```java
      import com.azure.identity.DefaultAzureCredential;
      import com.azure.identity.DefaultAzureCredentialBuilder;
      import com.mongodb.MongoClient;
      import org.springframework.context.annotation.Bean;

      @Bean
      public MongoClient mongoClient() {
        // Create DefaultAzureCredential as a local variable
        DefaultAzureCredential defaultCredential = new DefaultAzureCredentialBuilder().build();
        // Use credential here.
        return ...
      }
      ```
  2.7. For environment variables and properties, only use the names that exist in existing code or these names that provided by Service Connector:
      - AZURE_COSMOS_LISTCONNECTIONSTRINGURL
      - AZURE_COSMOS_SCOPE
      - AZURE_COSMOS_RESOURCEENDPOINT
      - AZURE_COSMOS_CLIENTID
  2.8. If it is supported to use "@Value" in current file, then use it to replace "System.getenv()". And use property instead of environment variable in "@Value".
    2.8.1. Example:
      ```java
      @Value("${azure.cosmos.listkeyurl}")
      private String listKeyUrl;
      ```
    2.8.2. Use property (azure.cosmos.listkeyurl) instead of environment variable (AZURE_COSMOS_LISTKEYURL).
    2.8.3. Use lowercase for all characters in property name.
    2.8.4. When both the property name from new added code (example: "azure.cosmos.listkeyurl") and original code (example: "app.cosmos.listkeyurl") can be used, use the new added one.
  2.9. Remove unused code and comments. For example: If some private field and private method will never be used after your modification, then delete them all.
  2.10. Organize imports:
      - Prefer importing classes and using their simple names rather than using fully qualified names.
      - Remove unused imports.
      - Add missing imports.
      - Keep existing import order.
