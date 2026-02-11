---
name: migration-spring-cache-backends-to-spring-cache-with-azure-cache-for-redis
description: Migrate from Spring Cache to Azure Cache for Redis for a scalable, managed solution that easily integrates with other Azure services.
---

# spring-cache-backends-to-spring-cache-with-azure-cache-for-redis

## Overview

Migrate from Spring Cache to Azure Cache for Redis for a scalable, managed solution that easily integrates with other Azure services.

## Knowledge Base Content

* KB ID: spring-cache-backends-to-spring-cache-with-azure-cache-for-redis
* Title: Migrate Spring Cache Backends to Spring Cache with Azure Cache for Redis
* Description: Provides specifications for migrating from Spring Cache to Azure Cache for Redis
* Content: # Migration Specification: Spring Cache to Azure Cache for Redis

## Overview

This migration involves transitioning from Spring's built-in caching abstraction to Azure Cache for Redis, a fully managed Redis service on Azure. This migration replaces local or simple caching mechanisms with a distributed, scalable Redis-based caching solution that provides better performance, persistence, and multi-instance support for cloud-native applications.

## Key Components to Replace

- **Local cache providers with Redis**: Replace in-memory cache managers like ConcurrentMapCacheManager with Redis-based implementations for distributed caching capabilities
- **Cache configuration with Redis configuration**: Migrate Spring cache configuration to Redis-specific settings including serialization, TTL, and connection pooling
- **Simple cache annotations with Redis-aware caching**: Maintain @Cacheable, @CacheEvict annotations while updating underlying cache manager to use Redis
- **Manual cache operations with Redis operations**: Replace direct CacheManager usage with RedisTemplate or ReactiveRedisTemplate for advanced Redis features

## Scope

### Included in Scope

- [x] Replace Spring Cache providers with Azure Redis Cache integration
- [x] Configure Redis connection with Azure Cache for Redis
- [x] Migrate cache configuration to Redis-specific settings
- [x] Update serialization strategies for Redis storage
- [x] Implement secure authentication using Azure Identity
- [x] Configure connection pooling and performance settings
- [x] **Spring Cache local provider removal and cleanup** - Complete elimination of local cache dependencies, configurations, and provider references

### Excluded from Scope

- [ ] Redis cluster configuration and advanced topology setup
- [ ] Custom Redis modules or extensions not supported by Azure Cache for Redis
- [ ] Data migration from existing cache stores to Redis
- [ ] Redis performance tuning beyond basic configuration
- [ ] Integration with non-Spring applications or frameworks

## Success Criteria

1. **Code compilation criterion** - All source code compiles successfully with Azure Cache for Redis dependencies
2. **Dependency resolution criterion** - All required Redis and Azure dependencies are correctly configured and resolved
3. **Configuration migration criterion** - All cache configuration files use Redis-specific settings and Azure connection details
4. **API compatibility criterion** - All cache annotations (@Cacheable, @CacheEvict, etc.) work with Redis backend
5. **Connection authentication criterion** - Azure Cache for Redis connection established using Managed Identity
6. **Serialization compatibility criterion** - Cache data serializes/deserializes correctly with Redis
7. **Performance criterion** - Cache operations perform within acceptable latency thresholds
8. **Distributed caching criterion** - Cache data is accessible across multiple application instances
9. **Spring Cache provider elimination criterion** - No local cache providers, simple cache managers, or in-memory cache references remain in the codebase

## Migration Steps

### 1. Dependency and Configuration Updates

1. **Add Azure Cache for Redis dependencies** - Use latest stable versions with Spring Cloud Azure BOM for consistency
2. **Configure passwordless authentication** - **Critical for Azure services: Use Microsoft Entra ID authentication instead of access keys/passwords**
3. **Update configuration files** - Migrate to Redis passwordless configuration format and remove Spring Cache local settings
4. **Remove Spring Cache local dependencies** - **Often missed: Ensure complete elimination of local cache providers to prevent conflicts**

### 2. Code Migration

1. **Replace cache manager configuration** - Update from local cache managers to Redis-based cache manager
2. **Configure Redis serialization** - **Migration-specific: Set up JSON or JDK serialization for Redis storage**
3. **Update cache configuration properties** - **Critical difference: Migrate TTL, eviction policies to Redis-specific settings**
4. **Configure passwordless authentication** - **Critical difference: Enable Microsoft Entra ID authentication through Spring Cloud Azure**

### 3. Validation and Cleanup

1. **Complete local cache provider removal** - **Commonly missed: Search and remove all local cache manager references, simple cache configurations**
2. **Verify Redis connectivity and functionality** - Ensure all cache operations work with Redis backend
3. **Validate configuration completeness** - **Migration-specific: Confirm no local cache configuration properties remain**

## Migration Patterns and Technical Specifications

### 0. Library Versions and Dependency Management

**Dependency Strategy:**
- **Use Spring Boot BOM**: Leverage Spring Boot dependency management for consistent Redis library versioning
- **Latest Stable Versions**: Use the latest stable version of Spring Data Redis and Azure Identity libraries
- **Version Consistency**: Ensure Redis client libraries use compatible versions with Spring Boot
- **Azure Security**: Include Azure Identity library for secure authentication to Azure Cache for Redis

**Required Dependencies:**
- **Spring Cloud Azure Redis Starter**: `com.azure.spring:spring-cloud-azure-starter-data-redis-lettuce` *(managed by Spring Cloud Azure BOM)*
- **Spring Data Redis**: `org.springframework.boot:spring-boot-starter-data-redis` *(managed by Spring Boot BOM)*
- **Remove local cache dependencies**: Completely eliminate simple cache providers and in-memory cache managers

**Version Management Approach:**
- **Primary Strategy**: Import Spring Boot BOM `org.springframework.boot:spring-boot-dependencies:3.4.1` *(use latest compatible version)* for automatic Redis dependency management
- **Azure Integration**: Include Spring Cloud Azure BOM `com.azure.spring:spring-cloud-azure-dependencies:5.23.0` *(use latest compatible version)* for consistent Azure library versions
- **Passwordless Authentication**: Spring Cloud Azure automatically handles Microsoft Entra ID authentication without additional Azure Identity dependencies

**Recommended Versions:** *(All versions shown are examples - use latest compatible versions from technology compatibility matrix)*
- **Spring Boot BOM**: `org.springframework.boot:spring-boot-dependencies:3.4.1`
- **Spring Cloud Azure BOM**: `com.azure.spring:spring-cloud-azure-dependencies:5.23.0`
- **Spring Cloud Azure Redis Starter**: Automatically managed by Spring Cloud Azure BOM

**Maven Dependencies Example:**
```xml
<dependencies>
    <dependency>
        <groupId>com.azure.spring</groupId>
        <artifactId>spring-cloud-azure-starter-data-redis-lettuce</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-redis</artifactId>
    </dependency>
</dependencies>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>3.4.1</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
        <dependency>
            <groupId>com.azure.spring</groupId>
            <artifactId>spring-cloud-azure-dependencies</artifactId>
            <version>5.23.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### 1. Cache Manager Configuration

**Technical Overview:**
- **Spring Cache**: Uses local cache managers like ConcurrentMapCacheManager or simple cache providers
- **Azure Cache for Redis**: Uses Redis-based cache manager with distributed caching capabilities
- **Migration Strategy**: Replace local cache manager configuration with Redis cache manager while maintaining Spring cache annotation compatibility

**Code Migration:**

*Spring Cache (Local):*
```java
@Configuration
@EnableCaching
public class CacheConfig {

    @Bean
    public CacheManager cacheManager() {
        // Simple in-memory cache manager
        SimpleCacheManager cacheManager = new SimpleCacheManager();
        cacheManager.setCaches(Arrays.asList(
            new ConcurrentMapCache("users"),
            new ConcurrentMapCache("products")
        ));
        return cacheManager;
    }
}
```

*Azure Cache for Redis:*
```java
@Configuration
@EnableCaching
public class RedisCacheConfig {

    // Spring Cloud Azure automatically configures Redis connection
    // with passwordless authentication - no manual connection factory needed

    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);

        // JSON serialization for better Redis storage
        Jackson2JsonRedisSerializer<Object> jackson2JsonRedisSerializer =
            new Jackson2JsonRedisSerializer<>(Object.class);
        ObjectMapper om = new ObjectMapper();
        om.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
        om.enableDefaultTyping(ObjectMapper.DefaultTyping.NON_FINAL);
        jackson2JsonRedisSerializer.setObjectMapper(om);

        template.setValueSerializer(jackson2JsonRedisSerializer);
        template.setKeySerializer(new StringRedisSerializer());
        template.setHashKeySerializer(new StringRedisSerializer());
        template.setHashValueSerializer(jackson2JsonRedisSerializer);

        template.afterPropertiesSet();
        return template;
    }

    @Bean
    public CacheManager cacheManager(RedisConnectionFactory connectionFactory) {
        RedisCacheConfiguration config = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofHours(1)) // Default TTL of 1 hour
            .serializeKeysWith(RedisSerializationContext.SerializationPair.fromSerializer(new StringRedisSerializer()))
            .serializeValuesWith(RedisSerializationContext.SerializationPair.fromSerializer(new Jackson2JsonRedisSerializer<>(Object.class)))
            .disableCachingNullValues();

        return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(config)
            .transactionAware()
            .build();
    }
}
```

### 1.1. Azure Security and Authentication

**Technical Overview:**
- **Security Priority**: **When migrating to Azure Cache for Redis, use Microsoft Entra ID passwordless authentication to eliminate credential management and enhance security**
- **Spring Cloud Azure Integration**: Use Spring Cloud Azure Redis starter that automatically handles Microsoft Entra ID authentication
- **Configuration Strategy**: Implement passwordless authentication that works seamlessly across development, staging, and production environments

**Authentication Migration Pattern:**

*Traditional Authentication (Connection Strings/Keys - AVOID):*
```java
// AVOID: Any form of hardcoded credentials
String connectionString = "your-cache-name.redis.cache.windows.net:6380,password=your-access-key,ssl=True,abortConnect=False";
String accessKey = "your-access-key";
```

*Microsoft Entra ID Passwordless Authentication (Recommended):*
```java
// RECOMMENDED: Passwordless authentication with Spring Cloud Azure
@Configuration
@EnableCaching
public class RedisCacheConfig {

    // No explicit authentication configuration needed
    // Spring Cloud Azure handles Microsoft Entra ID authentication automatically
    @Bean
    public CacheManager cacheManager() {
        // Spring Cloud Azure Redis starter automatically configures
        // the connection with Microsoft Entra ID authentication
        return RedisCacheManager.builder()
            .cacheDefaults(RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofHours(1)))
            .transactionAware()
            .build();
    }
}
```

**Required Dependencies for Azure Authentication:** *(Use latest compatible versions from compatibility matrix)*
- **Spring Cloud Azure Redis Starter**: `com.azure.spring:spring-cloud-azure-starter-data-redis-lettuce` *(use latest compatible version for passwordless authentication)*
- **Spring Cloud Azure BOM**: `com.azure.spring:spring-cloud-azure-dependencies:5.23.0` *(use latest compatible version for consistent Azure library versions)*
- **Spring Data Redis**: `org.springframework.boot:spring-boot-starter-data-redis` *(managed by Spring Boot BOM)*
- **Remove credential-based dependencies**: Eliminate any authentication libraries that use access keys, passwords, or connection strings

**Environment-Specific Configuration:**
```yaml
# application.yml - Passwordless configuration with no sensitive data
spring:
  data:
    redis:
      host: <your-redis-name>.redis.cache.windows.net
      port: 6380
      username: <your-redis-username>  # Get from Azure Cache for Redis Entra ID configuration
      ssl:
        enabled: true
      azure:
        passwordless-enabled: true  # Enable Microsoft Entra ID authentication
```

### 2. Cache Annotation Compatibility

**Technical Overview:**
- **Spring Cache**: Standard cache annotations work with any cache provider
- **Azure Cache for Redis**: Same annotations work with Redis backend with enhanced distributed capabilities
- **Migration Strategy**: Maintain existing cache annotations while benefiting from Redis persistence and distribution

**Feature Gap Analysis:**
- **Annotation Support**: Full compatibility maintained for @Cacheable, @CacheEvict, @CachePut, @Caching
- **Enhanced Features**: Redis provides persistence, distribution, and advanced eviction policies
- **Performance**: Network latency considerations for Redis calls vs local cache

**Code Migration:**

*Spring Cache Annotations (No Changes Required):*
```java
@Service
public class UserService {

    @Cacheable(value = "users", key = "#userId")
    public User getUserById(Long userId) {
        // Method implementation remains unchanged
        return userRepository.findById(userId);
    }

    @CacheEvict(value = "users", key = "#userId")
    public void updateUser(Long userId, User user) {
        // Method implementation remains unchanged
        userRepository.save(user);
    }

    @CacheEvict(value = "users", allEntries = true)
    public void clearUserCache() {
        // This now clears Redis cache instead of local cache
    }
}
```

*Enhanced Redis Cache Configuration:*
```java
@Configuration
public class CacheConfiguration {

    @Bean
    public CacheManager cacheManager(LettuceConnectionFactory connectionFactory) {
        Map<String, RedisCacheConfiguration> cacheConfigurations = new HashMap<>();

        // Different TTL for different cache types
        cacheConfigurations.put("users",
            RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofHours(2)));

        cacheConfigurations.put("products",
            RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(30)));

        return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofHours(1)))
            .withInitialCacheConfigurations(cacheConfigurations)
            .transactionAware()
            .build();
    }
}
```

### 3. Advanced Redis Operations

**Technical Overview:**
- **Spring Cache**: Limited to basic cache operations through CacheManager
- **Azure Cache for Redis**: Full Redis capabilities through RedisTemplate and Redis commands
- **Migration Strategy**: Enhance existing cache operations with Redis-specific features when needed

**Code Migration:**

*Spring Cache Direct Operations:*
```java
@Service
public class CacheService {

    @Autowired
    private CacheManager cacheManager;

    public void manualCacheOperation() {
        Cache cache = cacheManager.getCache("users");
        cache.put("key", "value");
        String value = cache.get("key", String.class);
        cache.evict("key");
    }
}
```

*Redis Enhanced Operations:*
```java
@Service
public class RedisCacheService {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Autowired
    private CacheManager cacheManager;

    // Maintain compatibility with Spring Cache
    public void manualCacheOperation() {
        Cache cache = cacheManager.getCache("users");
        cache.put("key", "value");
        String value = cache.get("key", String.class);
        cache.evict("key");
    }

    *Redis Enhanced Operations:*
```java
@Service
public class RedisCacheService {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Autowired
    private CacheManager cacheManager;

    // Maintain compatibility with Spring Cache
    public void manualCacheOperation() {
        Cache cache = cacheManager.getCache("users");
        cache.put("key", "value");
        String value = cache.get("key", String.class);
        cache.evict("key");
    }

    // Enhanced Redis operations using RedisTemplate
    // RedisTemplate is automatically configured by Spring Cloud Azure
    public void advancedRedisOperations() {
        // Set with custom TTL
        redisTemplate.opsForValue().set("user:123", "John Doe", Duration.ofMinutes(30));

        // Hash operations
        redisTemplate.opsForHash().put("user:123:profile", "name", "John Doe");
        redisTemplate.opsForHash().put("user:123:profile", "email", "john@example.com");

        // Set operations
        redisTemplate.opsForSet().add("user:123:permissions", "READ", "WRITE");

        // List operations
        redisTemplate.opsForList().rightPush("user:notifications", "New message");

        // Check existence
        Boolean exists = redisTemplate.hasKey("user:123");

        // Set expiration
        redisTemplate.expire("user:123", Duration.ofHours(2));
    }
}
```
    public void advancedRedisOperations() {
        // Set with custom TTL
        redisTemplate.opsForValue().set("session:123", "sessionData", Duration.ofMinutes(30));

        // Atomic operations
        redisTemplate.opsForValue().increment("counter:views");

        // Hash operations
        redisTemplate.opsForHash().put("user:123", "name", "John Doe");
        redisTemplate.opsForHash().put("user:123", "email", "john@example.com");

        // List operations for caching collections
        redisTemplate.opsForList().rightPush("recent:products", "product123");

        // Set operations for unique collections
        redisTemplate.opsForSet().add("user:123:permissions", "READ", "WRITE");
    }

    // Batch operations for better performance
    public void batchOperations() {
        redisTemplate.executePipelined((RedisCallback<Object>) connection -> {
            connection.set("key1".getBytes(), "value1".getBytes());
            connection.set("key2".getBytes(), "value2".getBytes());
            connection.set("key3".getBytes(), "value3".getBytes());
            return null;
        });
    }
}
```

### 4. Performance and Connection Management

**Technical Overview:**
- **Spring Cache**: No connection management concerns with local caches
- **Azure Cache for Redis**: Requires connection pooling, timeout configuration, and performance tuning
- **Migration Strategy**: Use Spring Cloud Azure automatic configuration with customizable performance settings

**Code Migration:**

*Passwordless Redis Performance Configuration:*
```java
@Configuration
public class RedisPerformanceConfig {

    // Spring Cloud Azure automatically handles connection factory creation
    // You can customize connection pool settings through application properties

    @Bean
    @Primary
    public CacheManager performantCacheManager(RedisConnectionFactory connectionFactory) {
        // Configure different cache settings for optimal performance
        Map<String, RedisCacheConfiguration> cacheConfigurations = new HashMap<>();

        // Fast cache for frequently accessed data
        cacheConfigurations.put("fast-cache",
            RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(5))
                .disableCachingNullValues());

        // Long-lived cache for stable data
        cacheConfigurations.put("stable-cache",
            RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofHours(4))
                .disableCachingNullValues());

        return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofHours(1)))
            .withInitialCacheConfigurations(cacheConfigurations)
            .transactionAware()
            .build();
    }
}
```

*Application Properties for Performance Tuning:*
```yaml
# application.yml - Performance optimization with passwordless authentication
spring:
  data:
    redis:
      host: <your-redis-name>.redis.cache.windows.net
      port: 6380
      username: <your-redis-username>
      ssl:
        enabled: true
      azure:
        passwordless-enabled: true
      timeout: 500ms
      lettuce:
        pool:
          max-active: 20
          max-idle: 10
          min-idle: 5
          max-wait: 1000ms
          time-between-eviction-runs: 60s
        shutdown-timeout: 100ms
```

**Performance Configuration:**
```yaml
# application.yml - Production Redis configuration
spring:
  data:
    redis:
      host: ${AZURE_REDIS_HOSTNAME}
      port: 6380
      password: ${AZURE_REDIS_ACCESS_KEY}
      ssl:
        enabled: true
      timeout: 2000ms
      lettuce:
        pool:
          max-active: 20
          max-idle: 10
          min-idle: 5
          max-wait: 1000ms
        shutdown-timeout: 100ms
      connect-timeout: 2000ms

  cache:
    redis:
      time-to-live: 3600000 # 1 hour default TTL
      cache-null-values: false
      key-prefix: "app:cache:"
      use-key-prefix: true
```

### 99. Spring Cache Local Provider Removal and Cleanup Patterns

**Technical Overview:**
- **Complete Elimination Strategy**: Ensure all traces of local Spring Cache providers are removed to prevent conflicts and ensure Redis is the sole cache backend
- **Cleanup Verification**: Implement systematic checks to verify complete removal of local cache components
- **Migration Completeness**: Validate that the application uses only Redis for caching without fallback to local cache

**Dependency Removal Checklist:**

*Maven Build File Changes:*
```diff
 <dependencies>
-    <!-- Remove local cache dependencies if explicitly added -->
-    <dependency>
-        <groupId>org.springframework</groupId>
-        <artifactId>spring-context-support</artifactId>
-    </dependency>
+    <!-- Add Spring Cloud Azure Redis dependencies -->
+    <dependency>
+        <groupId>org.springframework.boot</groupId>
+        <artifactId>spring-boot-starter-data-redis</artifactId>
+    </dependency>
+    <dependency>
+        <groupId>com.azure.spring</groupId>
+        <artifactId>spring-cloud-azure-starter-data-redis-lettuce</artifactId>
+    </dependency>
 </dependencies>
+
+<dependencyManagement>
+    <dependencies>
+        <dependency>
+            <groupId>com.azure.spring</groupId>
+            <artifactId>spring-cloud-azure-dependencies</artifactId>
+            <version>5.23.0</version>
+            <type>pom</type>
+            <scope>import</scope>
+        </dependency>
+    </dependencies>
+</dependencyManagement>
```

**Code Cleanup Patterns:**

*Configuration Class Changes:*
```diff
-// Remove local cache manager configurations
-@Bean
-public CacheManager cacheManager() {
-    SimpleCacheManager cacheManager = new SimpleCacheManager();
-    cacheManager.setCaches(Arrays.asList(
-        new ConcurrentMapCache("users"),
-        new ConcurrentMapCache("products")
-    ));
-    return cacheManager;
-}
+// Redis cache manager configuration with Spring Cloud Azure
+@Bean
+public CacheManager cacheManager(RedisConnectionFactory connectionFactory) {
+    return RedisCacheManager.builder(connectionFactory)
+        .cacheDefaults(RedisCacheConfiguration.defaultCacheConfig()
+            .entryTtl(Duration.ofHours(1)))
+        .build();
+}
```

*Configuration File Changes:*
```diff
-# Remove local cache configuration
-spring:
-  cache:
-    type: simple
-    cache-names: users,products
+# Add Redis passwordless cache configuration
+spring:
+  cache:
+    type: redis
+  data:
+    redis:
+      host: <your-redis-name>.redis.cache.windows.net
+      port: 6380
+      username: <your-redis-username>
+      ssl:
+        enabled: true
+      azure:
+        passwordless-enabled: true
```

**Cleanup Verification Commands:**
```bash
# Search for remaining local cache references
grep -r "SimpleCacheManager" src/ --exclude-dir=target
grep -r "ConcurrentMapCache" src/ --exclude-dir=target
grep -r "spring.cache.type=simple" src/ --exclude-dir=target

# Verify Spring Cloud Azure Redis dependencies are present
grep "spring-cloud-azure-starter-data-redis-lettuce" pom.xml build.gradle

# Check for resolved dependencies
# Maven
mvn dependency:tree | grep redis

# Gradle
gradle dependencies | grep redis
```

**Common Cleanup Oversights:**
- **Cache Manager Configuration**: Remove SimpleCacheManager, ConcurrentMapCacheManager beans
- **Configuration Properties**: Clean up spring.cache.type=simple, spring.cache.cache-names
- **Test Configurations**: Update test cache configurations to use embedded Redis or Redis testcontainers
- **Documentation**: Update cache-related documentation to reflect Redis usage
- **Monitoring Configuration**: Remove local cache-specific monitoring and add Redis monitoring

## Reference Resources

1. [Spring Data Redis Official Documentation](https://docs.spring.io/spring-data/redis/docs/current/reference/html/)
2. [Azure Cache for Redis Documentation](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/)
3. [Spring Boot Redis Integration Guide](https://docs.spring.io/spring-boot/docs/current/reference/html/data.html#data.nosql.redis)
4. [Redis Performance Best Practices](https://redis.io/docs/manual/performance/)
5. [Azure Cache for Redis Security Configuration](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-best-practices-security)
6. [Spring Cache Abstraction Documentation](https://docs.spring.io/spring-framework/docs/current/reference/html/integration.html#cache)
7. [Azure Identity and Authentication Best Practices](https://docs.microsoft.com/en-us/azure/developer/java/sdk/identity)
8. [Azure SDK for Java BOM and Dependency Management](https://docs.microsoft.com/en-us/azure/developer/java/sdk/dependency-management)
9. [Lettuce Redis Client Documentation](https://lettuce.io/core/release/reference/)
10. [Redis Data Types and Commands Guide](https://redis.io/docs/data-types/)
11. [Spring Boot Redis Testing Guide](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing.testcontainers)
12. [Azure Cache for Redis Monitoring and Troubleshooting](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-monitoring)
13. [Redis Serialization Strategies](https://docs.spring.io/spring-data/redis/docs/current/reference/html/#redis.serializers)
