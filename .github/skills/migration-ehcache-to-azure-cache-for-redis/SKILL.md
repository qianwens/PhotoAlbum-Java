---
name: migration-ehcache-to-azure-cache-for-redis
description: Migrate from Ehcache in-process cache to Azure Cache for Redis.
---

# ehcache-to-azure-cache-for-redis

## Overview

Migrate from Ehcache in-process cache to Azure Cache for Redis.

## Knowledge Base Content

* KB ID: microsoft://cache-tasks/ehcache-to-azure-cache-for-redis/ehcache-cache-annotations.formula
* Title: Migrate Ehcache Spring Cache annotations to Azure Cache for Redis
* Description: Adapts Spring Cache annotations (@Cacheable, @CacheEvict, etc.) to work with Redis
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/@Cacheable|@CachePut|@CacheEvict|@CacheConfig|@Caching/`
> you could use tools to search code whatever if possible.
### Instruction

Your task is to examine Java code with Spring Cache annotations that were previously used with Ehcache and ensure they are properly configured to work with Azure Cache for Redis.

When migrating from Ehcache to Redis, most Spring Cache annotations (@Cacheable, @CachePut, @CacheEvict, etc.) can remain unchanged as they are cache-implementation agnostic. However, some custom key generators, condition expressions, or cache resolver logic may need adjustments.

Spring Cache annotation examples that generally remain unchanged:
```java
@Service
@CacheConfig(cacheNames = "users")
public class UserService {
  
  @Cacheable(key = "#id")
  public User getUserById(Long id) {
    // Method implementation
  }
  
  @CachePut(key = "#user.id")
  public User updateUser(User user) {
    // Method implementation
  }
  
  @CacheEvict(key = "#id")
  public void deleteUser(Long id) {
    // Method implementation
  }
  
  @Caching(evict = {
    @CacheEvict(value = "users", key = "#id"),
    @CacheEvict(value = "userProfiles", key = "#id")
  })
  public void deleteUserWithProfiles(Long id) {
    // Method implementation
  }
}
```

Areas that may need adjustment:

1. **Cache Key Generators**: If custom key generators were tuned for Ehcache, they may need adjustment:
```java
// Before (Ehcache-specific key generator)
@Bean
public KeyGenerator keyGenerator() {
  return new CustomEhcacheKeyGenerator();
}

// After (Redis-compatible key generator)
@Bean
public KeyGenerator keyGenerator() {
  return new RedisCompatibleKeyGenerator();
}
```

2. **TTL Expressions**: If using dynamic TTL settings with Ehcache's expiry policy:
```java
// Before (Ehcache-specific TTL)
@Cacheable(value = "users", key = "#id", 
           cacheManager = "ehCacheCacheManager")
public User getUserById(Long id) {
  // Method implementation
}

// After (Using Redis cache with TTL defined in the cache configuration)
@Cacheable(value = "users", key = "#id", 
           cacheManager = "redisCacheManager")
public User getUserById(Long id) {
  // Method implementation
}
```

3. **Custom Conditions**: If using Ehcache-specific conditions:
```java
// Before (Ehcache-specific condition)
@Cacheable(value = "users", condition = "#id > 100 && @ehCacheConditionEvaluator.shouldCache()")
public User getUserById(Long id) {
  // Method implementation
}

// After (Redis-compatible condition)
@Cacheable(value = "users", condition = "#id > 100 && @redisConditionEvaluator.shouldCache()")
public User getUserById(Long id) {
  // Method implementation
}
```

Implementation notes:
1. In most cases, Spring Cache annotations can remain unchanged
2. Update any cacheManager attributes to reference the Redis cache manager
3. Review and adjust any custom key generators to ensure they produce Redis-compatible keys
4. Remove any Ehcache-specific conditions or expressions
5. If using custom cache resolvers, update them to work with Redis
6. Check that serialization is properly configured for objects stored in Redis
7. For classes that use multiple caches, ensure all referenced caches are configured in Redis
8. Confirm that cache names used in annotations match those defined in your Redis cache configuration
