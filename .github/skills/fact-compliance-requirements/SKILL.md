---
name: fact-compliance-requirements
description: Identify regulatory compliance needs (GDPR, HIPAA, PCI-DSS, SOX)
---

# Compliance Requirements Analysis

## Purpose
Identify regulatory compliance requirements the application must meet based on data handling, industry, and security measures.

## Target Files/Locations
- **/README.md, **/COMPLIANCE.md, **/SECURITY.md, **/privacy-policy.md
- **/docs/**/*.md
- **/*.{java,cs,js,py,ts} (data handling, encryption)
- **/application.{properties,yml} (audit logging)

## Example Patterns
- GDPR: data protection, right to erasure, consent
- HIPAA: PHI, encryption, audit logs
- PCI-DSS: payment data, encryption at rest/transit
- SOX: financial data, audit trails, access controls

## Analysis Steps

### 1. Check Documentation
```
Use Read: **/README.md, **/COMPLIANCE.md, **/SECURITY.md
Use Grep: "GDPR|HIPAA|PCI-DSS|PCI|SOX|Sarbanes-Oxley|ISO 27001|SOC 2"
Files: **/docs/**/*.md
Context: -B 2 -A 3

Look for:
- Compliance statements
- Regulatory requirements
- Data handling policies
```

### 2. Check for Data Protection Code
```
Use Grep: "PersonalData|PII|PHI|PaymentData|encrypt|anonymize|pseudonymize"
Files: **/*.{java,cs,js,py}
Context: -B 2 -A 2

Indicators:
- Data encryption implementations
- Anonymization functions
- Consent management
- Data retention policies
```

### 3. Check for Audit Logging
```
Use Grep: "AuditLog|audit|trail|compliance.*log"
Files: **/*.{java,cs}, **/application.{properties,yml}

Look for:
- Audit event logging
- User action tracking
- Data access logs
```

### 4. Check for Data Privacy Features
```
Search for:
- Data export (GDPR right to portability)
- Data deletion (right to erasure)
- Consent management
- Cookie policies

Use Grep: "exportData|deleteUser|consent|privacy|GDPR"
```

### 5. Check Security Measures
```
Compliance often requires:
- Encryption at rest and in transit
- Access controls (RBAC)
- Multi-factor authentication
- Regular security audits

Cross-reference with security-implementation analysis
```

## Confidence Determination

### High Confidence
- ✅ Explicit compliance documentation
- ✅ Compliance-specific code features
- ✅ Regulatory requirements mentioned
- **Example**: "GDPR compliant: data encryption, consent management, right-to-erasure API implemented"

### Medium Confidence
- ⚠️ Some compliance features but not comprehensive
- **Example**: "Encryption and audit logging present, suggests PCI-DSS consideration but not documented"

### Low Confidence
- ⚠️ No explicit compliance requirements
- ⚠️ Features that could support compliance
- **Example**: "Standard security features, no specific compliance mentioned"

### Not Applicable
- ❌ Internal tool with no regulatory requirements
- **Example**: "Development utility, no compliance requirements"

## Output Format

```json
{
  "input_name": "Compliance Requirements",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Compliance summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{Documentation mentions}",
      "{Compliance-specific code}",
      "{Security features}",
      "{Audit logging}"
    ],
    "values": [
      "{Regulations: GDPR, HIPAA, PCI-DSS, SOX, etc.}",
      "{Features: encryption, audit logs, consent}",
      "{Data types: PII, PHI, payment data}",
      "{Certifications if mentioned}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
