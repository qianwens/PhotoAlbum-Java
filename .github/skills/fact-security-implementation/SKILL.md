---
name: fact-security-implementation
description: Analyze security measures (HTTPS, Encryption, Token-based auth)
---

# Security Implementation Analysis

## Purpose
Identify security measures implemented in the application including HTTPS, authentication, authorization, encryption, and security headers.

## Target Files/Locations
- **/application.{properties,yml} (SSL, security configs)
- **/*.java, **/*.cs (security filters, auth)
- **/pom.xml, **/build.gradle, **/*.csproj (security dependencies)
- **/Dockerfile (SSL certificates)
- **/k8s/**/*.yaml (TLS secrets)

## Example Patterns
- **HTTPS/TLS**: server.ssl.*, SSLContext, TLS certificates
- **Authentication**: JWT, OAuth2, Basic Auth, API keys
- **Authorization**: @PreAuthorize, [Authorize], RBAC
- **Encryption**: AES, RSA, EncryptionService
- **Security Headers**: CORS, CSP, HSTS, X-Frame-Options

## Analysis Steps

### 1. Check for HTTPS/TLS Configuration
```
Use Grep: "server\\.ssl|https://|TLS|SSLContext|keystore"
Files: **/application.{properties,yml}, **/*.java, **/*.cs
Context: -B 2 -A 2

Check for:
- server.ssl.key-store
- SSLContext.getInstance("TLS")
- HTTPS redirect configurations
```

### 2. Check Authentication Mechanisms
```
Use Grep: "JWT|OAuth2|@EnableWebSecurity|JwtToken|Bearer|Basic Auth"
Files: **/*.{java,cs,js}
Context: -B 3 -A 3

Dependencies:
- spring-boot-starter-security
- Microsoft.AspNetCore.Authentication.JwtBearer
- passport (Node.js)

Look for:
- @EnableWebSecurity, @PreAuthorize (Spring)
- [Authorize], UseAuthentication() (.NET)
- JWT token generation/validation
```

### 3. Check for Authorization
```
Use Grep: "@PreAuthorize|@Secured|\\[Authorize\\]|hasRole|hasAuthority"
Files: **/*.{java,cs}

RBAC indicators:
- Role definitions
- Permission checks
- Access control lists
```

### 4. Check for Encryption
```
Use Grep: "AES|RSA|encrypt|decrypt|Cipher|CryptoService"
Files: **/*.{java,cs,py,js}

Look for:
- Data encryption at rest
- Encryption services
- Key management (KMS, KeyVault)
```

### 5. Check for Security Headers
```
Use Grep: "CORS|Content-Security-Policy|X-Frame-Options|HSTS|Strict-Transport-Security"
Files: **/*.{java,cs,js}, **/application.{properties,yml}

Spring: WebMvcConfigurer.addCorsMappings
.NET: app.UseCors(), app.UseHsts()
```

### 6. Check Dependency Scanning
```
Look for security scanning:
- Dependabot config
- Snyk, OWASP Dependency Check
- npm audit, dotnet list package --vulnerable
```

## Confidence Determination

### High Confidence
- ✅ Multiple security measures implemented
- ✅ HTTPS + authentication + authorization configured
- **Example**: "HTTPS with TLS 1.3, JWT authentication, role-based authorization, AES encryption for sensitive data"

### Medium Confidence
- ⚠️ Some security features but incomplete
- **Example**: "Basic authentication configured, HTTPS unclear"

### Low Confidence
- ⚠️ Security dependencies present but implementation unclear
- **Example**: "Security framework dependency but no explicit configuration found"

### Not Applicable
- ❌ Internal tool with no security requirements
- **Example**: "Development utility, no security implementation needed"

## Output Format

```json
{
  "input_name": "Security Implementation",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Security summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{HTTPS/TLS configuration}",
      "{Authentication mechanism}",
      "{Authorization approach}",
      "{Encryption usage}",
      "{Security headers}"
    ],
    "values": [
      "{Transport: HTTPS, TLS 1.2/1.3}",
      "{Auth: JWT, OAuth2, Basic}",
      "{Authorization: RBAC, attribute-based}",
      "{Encryption: AES-256, RSA}",
      "{Headers: CORS, CSP, HSTS}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
