---
name: fact-data-classification
description: Identify data sensitivity classification (Public, Internal, Confidential, PII)
---

# Data Classification Analysis

## Purpose
Determine the sensitivity classification of data handled by the application to understand protection requirements.

## Target Files/Locations
- **/README.md, **/SECURITY.md, **/DATA_CLASSIFICATION.md
- **/docs/**/*.md (data classification)
- **/*.{java,cs,js,py} (data annotations, comments)
- **/schema.sql, **/migrations/*.sql (database schemas)
- **/*.proto, **/*.graphql (API schemas)

## Example Patterns
- **Public**: publicly accessible data, no protection needed
- **Internal**: company data, standard access controls
- **Confidential**: sensitive business data, strict access controls
- **PII**: personal identifiable information (names, emails, SSN)
- **PHI**: protected health information
- **PCI**: payment card data
- **Restricted**: highly sensitive, executive/legal only

## Analysis Steps

### 1. Check Documentation
```
Use Read: **/README.md, **/SECURITY.md, **/DATA_CLASSIFICATION.md
Use Grep: "data classification|sensitivity|PII|confidential|restricted"
Files: **/docs/**/*.md
Context: -B 2 -A 3

Look for:
- Data classification policy
- Sensitivity levels
- Data types handled
```

### 2. Analyze Database Schemas
```
Use Glob: **/schema.sql, **/migrations/*.sql, **/flyway/**/*.sql
Use Read to examine table definitions

Look for sensitive data indicators:
- email, phone, address (PII)
- ssn, tax_id, national_id (PII)
- credit_card, account_number (PCI)
- password, secret, token (Credentials)
- medical, diagnosis (PHI)
- salary, financial (Confidential)
```

### 3. Check Code for Data Annotations
```
Use Grep: "@PersonalData|@Confidential|@Restricted|@PII|@Sensitive"
Files: **/*.{java,cs}
Context: -B 1 -A 3

.NET: [PersonalData], [ProtectedPersonalData]
Java: Custom annotations or comments
```

### 4. Analyze API Schemas
```
Use Glob: **/*.proto, **/*.graphql, **/openapi.yaml
Read schema definitions

Identify sensitive fields:
- User personal information
- Authentication credentials
- Financial data
- Health information
```

### 5. Check Encryption Usage
```
Encryption usage indicates sensitive data:

Use Grep: "encrypt|cipher|AES|RSA|hash"
Files: **/*.{java,cs,js,py}
Context: -B 2 -A 2

What's encrypted:
- Passwords → Credentials (Confidential)
- Payment info → PCI Data
- Medical records → PHI
- Personal details → PII
```

### 6. Categorize Data Types
```
Based on findings, classify:
- Public: blog posts, product catalogs
- Internal: employee directory, internal docs
- Confidential: trade secrets, financial reports
- PII: customer names, emails, addresses
- PHI: medical records, diagnoses
- PCI: credit card numbers, CVV
```

## Confidence Determination

### High Confidence
- ✅ Data classification documented
- ✅ Sensitive data fields identified in schema
- ✅ Encryption applied to sensitive data
- **Example**: "Data classification: Confidential and PII - handles customer names, emails, addresses (PII) and financial transactions (Confidential)"

### Medium Confidence
- ⚠️ Data types identified but no formal classification
- **Example**: "Database contains email and address fields (likely PII) but no classification policy documented"

### Low Confidence
- ⚠️ Data types unclear from schema
- ⚠️ Generic field names
- **Example**: "Database schema generic, data sensitivity unclear"

### Not Applicable
- ❌ No data storage (stateless API proxy)
- **Example**: "Stateless authentication proxy, no data stored"

## Output Format

```json
{
  "input_name": "Data Classification",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Classification summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Documentation}",
      "{Database schema analysis}",
      "{Sensitive field identification}",
      "{Encryption usage}"
    ],
    "values": [
      "{Classification levels: Public, Internal, Confidential, PII, etc.}",
      "{Sensitive data types handled}",
      "{Protection measures per classification}",
      "{Data volume estimates if available}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
