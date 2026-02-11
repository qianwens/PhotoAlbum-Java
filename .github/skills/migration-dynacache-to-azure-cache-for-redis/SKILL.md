---
name: migration-dynacache-to-azure-cache-for-redis
description: Migrate from DynaCache to Azure Cache for Redis.
---

# dynacache-to-azure-cache-for-redis

## Overview

Migrate from DynaCache to Azure Cache for Redis.

## Knowledge Base Content

* KB ID: dynacache-to-azure-cache-for-redis
* Title: Migrate Dynacache to Azure Cache for Redis
* Description: Provides specifications for migrating from Dynacache to Azure Cache for Redis
* Content: 
## Requirements:

### 1. Manage dependency versions with BOMs
- Use `azure-sdk-bom` to manage Azure SDK dependency versions
- Use `spring-cloud-azure-dependencies` to manage Spring Cloud Azure dependency versions
- Example configuration:
  ```xml
  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-sdk-bom</artifactId>
        <version>1.2.25</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
      <dependency>
        <groupId>com.azure.spring</groupId>
        <artifactId>spring-cloud-azure-dependencies</artifactId>
        <version>4.19.0</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>
  ```

### 2. Use compatible dependency versions
- **Spring Cloud Azure compatibility:**
  - Java < 17 → use Spring Boot 2.x
  - Spring Boot 2.x → use Spring Cloud Azure 4.x
- **Find the latest versions:** Search Maven Central for the most recent compatible versions of all dependencies.

### 3. Enable passwordless authentication

#### Case 1: Spring Boot applications
Use the Redis beans provided by Spring Cloud Azure:

1. **Add the correct dependency:**
   - Spring Cloud Azure 4.x: `spring-cloud-azure-starter-redis`
   - Other versions: `spring-cloud-azure-starter-data-redis-lettuce`

2. **Enable passwordless authentication:**
   - Spring Cloud Azure 4.x: set `spring.redis.azure.passwordless-enabled=true`
   - Other versions: set `spring.data.redis.azure.passwordless-enabled=true`

3. **Use dependency injection:** Spring Cloud Azure automatically creates Redis beans (`RedisConnectionFactory` and `RedisTemplate`) with passwordless authentication enabled. Inject these beans instead of creating Redis connections manually.

#### Case 2: Non-Spring Boot Java applications
Use `DefaultAzureCredential` to obtain authentication tokens:

1. **Add dependency:** `azure-identity`

2. **Create a Redis connection with automatic token refresh:** Use `DefaultAzureCredential`; refresh the AAD token early and issue `AUTH` again without rebuilding the connection. Always use SSL (port 6380).

   Key points:
   - Scope: `https://redis.azure.com/.default`
   - Refresh window: renew when fewer than 5 minutes remain (docs recommend at least 3 minutes early)
   - Reuse a single Jedis; just send `AUTH <new-token>`
   - Thread-safe via synchronized method (simple approach)

   Helper (lazy singleton + refresh-on-access + functional wrapper):
   ```java
   public final class AzureRedisClientManager {
     private static final String SCOPE = "https://redis.azure.com/.default";
     private static final DefaultAzureCredential CREDENTIAL = new DefaultAzureCredentialBuilder().build();
     private static final TokenRequestContext CONTEXT = new TokenRequestContext().addScopes(SCOPE);
     private static volatile AccessToken token;
     private static volatile Jedis jedis;

     private AzureRedisClientManager() {}

     // Internal: ensure a connected Jedis with a valid (not soon expiring) token
     private static synchronized Jedis getJedisWithUnexpiredToken() {
       if (jedis == null) {
         jedis = new Jedis(System.getenv("REDIS_HOSTNAME"), 6380, true); // SSL
       }
       if (token == null || OffsetDateTime.now().isAfter(token.getExpiresAt().minusMinutes(5))) {
         token = CREDENTIAL.getToken(CONTEXT).block();
         jedis.auth(token.getToken());
       }
       return jedis;
     }

     // Functional helper: ensure fresh token then execute the lambda
     public static <T> T withJedis(Function<Jedis, T> fn) {
       Jedis j = getJedisWithUnexpiredToken();
       return fn.apply(j);
     }

     // Void convenience
     public static void withJedis(Consumer<Jedis> c) {
       withJedis(j -> { c.accept(j); return null; });
     }
   }
   ```

   Usage:
   ```java
   AzureRedisClientManager.withJedis(j -> j.set("key", "value"));
   String value = AzureRedisClientManager.withJedis(j -> j.get("key"));
   ```
