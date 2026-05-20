---
name: fact-external-dependencies
description: Identify external system dependencies (SQL Server, Redis, LDAP, File shares)
---

# External Dependencies Analysis

## Purpose
Catalog external systems and services the application depends on including databases, caches, authentication services, and storage.

## Target Files/Locations
- **/application.{properties,yml} (connection strings)
- **/docker-compose*.yml (external services)
- **/*.env.example (dependency URLs)
- **/README.md (setup instructions)
- **/*.{java,cs,js,py} (connection code)

## Example Patterns
- **Databases**: SQL Server, PostgreSQL, MySQL, Oracle, MongoDB
- **Caches**: Redis, Memcached, Elasticsearch
- **Auth**: LDAP, Active Directory, OAuth providers
- **Storage**: S3, Azure Blob, NFS, SMB
- **Queues**: RabbitMQ, Kafka, SQS, Azure Service Bus

## Analysis Steps

### 1. Check Application Configuration
```
Use Grep: "datasource|database|jdbc:|connectionString|redis|ldap|s3|blob"
Files: **/application.{properties,yml}, **/appsettings*.json
Context: -B 1 -A 2

Extract:
- spring.datasource.url=jdbc:sqlserver://...
- ConnectionStrings:DefaultConnection
- redis.host
- ldap.url
```

### 2. Check docker-compose Services
```
Use Read: **/docker-compose*.yml
Identify services:
- postgres, mysql, sqlserver
- redis, memcached
- rabbitmq, kafka
- elasticsearch

Note: external vs internal dependencies
```

### 3. Check Environment Variables
```
Use Read: **/.env.example
Look for:
- DATABASE_URL
- REDIS_URL
- LDAP_SERVER
- S3_BUCKET
- API endpoint URLs
```

### 4. Check Documentation
```
Use Read: **/README.md
Look for:
- Prerequisites section
- External services setup
- Configuration instructions
```

### 5. Search Code for Connections
```
Use Grep: "SqlConnection|MongoClient|RedisClient|LdapContext|S3Client"
Files: **/*.{java,cs,js,py}
Context: -B 2 -A 3
```

## Confidence Determination

### High Confidence
- ✅ Dependencies in config + docker-compose + docs
- ✅ Connection strings present
- **Example**: "External dependencies: SQL Server 2019, Redis 6, LDAP (Active Directory), Azure Blob Storage from config and docs"

### Medium Confidence
- ⚠️ Dependencies referenced but details incomplete
- **Example**: "Database required (connection string present) but type/version unclear"

### Low Confidence
- ⚠️ Possible dependencies inferred from code
- **Example**: "May use Redis based on client library dependency"

### Not Applicable
- ❌ Fully self-contained application
- **Example**: "Standalone application with embedded database, no external dependencies"

## Output Format

```json
{
  "input_name": "External Dependencies",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Dependencies summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Configuration entries}",
      "{docker-compose services}",
      "{Documentation}",
      "{Connection code}"
    ],
    "values": [
      "{Dependency: SQL Server, Redis, etc.}",
      "{Versions if known}",
      "{Purpose: database, cache, auth, storage}",
      "{Count: N external systems}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
