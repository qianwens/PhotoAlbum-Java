---
name: migration-local-redis-to-azure-redis-cache
description: Migrate from a local Redis instance to Azure Cache for Redis.
---

# local-redis-to-azure-redis-cache

## Overview

Migrate from a local Redis instance to Azure Cache for Redis.

## Knowledge Base Content

* KB ID: local-redis-to-azure-redis-cache
* Title: Migrate Local Redis to Azure Cache for Redis
* Description: Migrate Local Redis to Azure Cache for Redis
* Content: 
Azure Redis Migration Guide for Java Applications

Your task is to migrate a Java application from using local redis cache to use Azure Cache for Redis.

Key Points:
1. You need to migrate the entire project to use Azure Cache for Redis instead of Spring Boot Cache, focusing on code changes, dependency updates, and configuration adjustments.
2. Please find suitable places to make the changes directly, like in-place modifying the pom.xml/build.gradle/application.yml file, write compilable code, don't leave uncompleted code blocks.
3. You need to change the all the Spring Boot Cache cache related logic and keep other unchanged. At the same time, each place that uses Spring Boot Cache API, must be replaced with Azure cache for redis ones.
4. Ignore data migration and infrastructure setup.
5. You should delete or comment out the original implementation, since the depdendency will be removed. Or we cannot pass the build.
---

### Step 1: Dependency Check

- Instruction:
  "First, identify whether the application uses Jedis or Lettuce by checking the project's dependencies (e.g., `pom.xml` or `build.gradle`).
  Then you can take jump to step 2 (for jedis) or step 3 (for Lettuce) accroding to the library the app is using.
  Example dependencies:
  ```xml
  <!-- Jedis -->
  <dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>3.7.0+</version>
  </dependency>

  <!-- Lettuce -->
  <dependency>
    <groupId>io.lettuce</groupId>
    <artifactId>lettuce-core</artifactId>
    <version>6.2.4+</version>
  </dependency>
  ```

---

### Step 2: Jedis-Specific Migration Guide

Key Steps:
1. Update Connection Configuration:
   - Replace local Redis host/port with Azure endpoint:
     ```java
     JedisShardInfo shardInfo = new JedisShardInfo(
         "<cache-name>.redis.cache.windows.net", 6380 // Azure SSL port
     );
     shardInfo.setPassword("<primary-access-key>"); // From Azure Portal
     shardInfo.setSsl(true); // Mandatory TLS
     ```

2. SSL Certificate Handling:
   - For production: Import Azure’s root certificate (`BaltimoreCyberTrustRoot.crt`) into the JVM truststore:
     ```bash
     keytool -importcert -keystore $JAVA_HOME/lib/security/cacerts \
       -file BaltimoreCyberTrustRoot.crt -alias azure-ssl
     ```
   - For testing (not production): Disable certificate validation:
     ```java
     System.setProperty("javax.net.ssl.trustStoreType", "jks");
     System.setProperty("javax.net.ssl.trustStore", "NONE");
     ```

3. Connection Pool Tuning:
   ```java
   JedisPoolConfig poolConfig = new JedisPoolConfig();
   poolConfig.setMaxTotal(50); // Align with Azure tier limits
   JedisPool pool = new JedisPool(poolConfig, host, port, 5000, password, true);
   ```

---

### Step 3: Lettuce-Specific Migration Guide

Key Steps:
1. Configure Azure Connection:
   - Use `RedisURI` with Azure-specific parameters:
     ```java
     RedisURI redisUri = RedisURI.Builder.redis("<cache-name>.ache.windows.net")
         .withPort(6380)
         .withSsl(true)
         .withPassword("<primary-access-key>")
         .build();
     RedisClient client = RedisClient.create(redisUri);
     ```

2. SSL/TLS Setup:
   - Lettuce uses the JVM truststore by default. Ensure `BaltimoreCyberTrustRoot.crt` is imported (see Jedis SSL steps).

3. Cluster Configuration (If Applicable):
   - Disable topology refresh to avoid downtime during Azure updates:
     ```java
     client.setOptions(ClusterClientOptions.builder()
         .validateClusterNodeMembership(false)
         .build());
     ```
---
### Step 4: Spring Boot Configuration (if applicable)
#### Jedis (application.properties)
```properties
spring.redis.host=<cache-name>.redis.cache.windows.net
spring.redis.port=6380
spring.redis.password=<primary-access-key>
spring.redis.ssl=true
spring.redis.jedis.pool.max-active=50
```

#### Lettuce (application.yml)
```yaml
spring:
  redis:
    host: <cache-name>.redis.cache.windows.net
    port: 6380
    password: <primary-access-key>
    ssl: true
    lettuce:
      pool:
        max-active: 100     # Non-blocking I/O allows higher limits
        min-idle: 10
```

### Pass the build
Use this command to check whether the project can pass the build after migration. If not, fix any build error and make sure it pass the build.
For windows:
```
cmd /c "mvn clean compile -B -fn -DskipTests -Dossindex.failOnError=false -Dossindex.skip=true -Dlicense.skip=true -Dcheckstyle.skip=true -Dencoding=UTF-8"
```
For Linux / macOS:
```
mvn clean compile -B -fn -DskipTests -Dossindex.failOnError=false -Dossindex.skip=true -Dlicense.skip=true -Dcheckstyle.skip=true -Dencoding=UTF-8
```
