# AppSec Checklist Instructions

## Overview

This skill scans the codebase for common security vulnerabilities and generates a comprehensive security checklist report. It focuses on OWASP Top 10 and common security misconfigurations.

## Execution Steps

### Step 1: Understand the Feature Context

1. **Read PM documents** from `docs/pm/{feature-name}/`:
   - PRD: understand feature functionality and data flow
   - TRD: understand architecture, third-party services, data storage

2. **Identify security-critical areas**:
   - Authentication/authorization logic
   - User input handling
   - Data storage and transmission
   - API endpoints
   - File uploads
   - Admin interfaces

### Step 2: Scan for Common Vulnerabilities

Use Grep and Read tools to search for security issues:

**A. Input Validation Issues**
- Search for user input handling without validation
- Check for SQL injection risks (raw SQL queries)
- Check for XSS risks (unescaped output in templates)
- Check for command injection (shell execution with user input)

**B. Authentication & Session Management**
- Search for password handling (plain text storage, weak hashing)
- Check session configuration (secure flags, httpOnly, sameSite)
- Check for hardcoded credentials
- Review JWT/token implementation

**C. Access Control**
- Check authorization logic
- Look for missing permission checks
- Review role-based access control implementation

**D. Sensitive Data Exposure**
- Search for API keys, secrets in code
- Check for sensitive data in logs
- Review encryption usage for sensitive data

**E. Security Misconfiguration**
- Check for debug mode in production
- Review CORS configuration
- Check for exposed admin endpoints
- Review error handling (information disclosure)

**F. Insecure Dependencies**
- Check for known vulnerable packages (if package.json/requirements.txt exists)

### Step 3: Generate Security Report

Create `docs/security/{feature-name}/appsec-checklist.md` with:

**Frontmatter:**
```yaml
---
feature: {feature-name}
version: v1
date: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

**Report Structure:**

1. **Executive Summary**
   - Total issues found
   - Risk level distribution (Critical/High/Medium/Low)
   - Overall security posture

2. **Critical Issues** (if any)
   - Issue description
   - Location (file:line)
   - Risk explanation
   - Fix recommendation

3. **High Priority Issues**
   - Same format as Critical

4. **Medium Priority Issues**
   - Same format

5. **Low Priority Issues**
   - Same format

6. **Security Best Practices Checklist**
   - [ ] Input validation on all user inputs
   - [ ] Parameterized queries (no SQL injection)
   - [ ] Output encoding (no XSS)
   - [ ] Secure session management
   - [ ] Proper authentication
   - [ ] Authorization checks on all protected resources
   - [ ] Secrets not in code
   - [ ] HTTPS enforced
   - [ ] Security headers configured
   - [ ] Error messages don't leak info

7. **Recommendations**
   - Priority order for fixes
   - Additional security measures to consider

### Step 4: Risk Classification

**Critical:**
- SQL injection vulnerabilities
- Authentication bypass
- Hardcoded secrets/credentials
- Remote code execution risks

**High:**
- XSS vulnerabilities
- Missing authorization checks
- Insecure session management
- Sensitive data exposure

**Medium:**
- Missing input validation
- Weak password policies
- Information disclosure in errors
- Missing security headers

**Low:**
- Debug mode enabled
- Verbose error messages
- Missing rate limiting
- Outdated dependencies (no known exploits)

## Output Format

Use clear, actionable language. For each issue:

```markdown
### [CRITICAL] SQL Injection in User Search

**Location:** `src/api/users.js:45`

**Issue:**
User input is directly concatenated into SQL query without sanitization.

**Code:**
\`\`\`javascript
const query = `SELECT * FROM users WHERE name = '${req.query.name}'`;
\`\`\`

**Risk:**
Attacker can execute arbitrary SQL commands, potentially accessing or deleting all database data.

**Fix:**
Use parameterized queries:
\`\`\`javascript
const query = 'SELECT * FROM users WHERE name = ?';
db.query(query, [req.query.name]);
\`\`\`
```

## Notes

- Focus on actionable findings, not theoretical risks
- Provide specific file locations and line numbers
- Include code examples for both vulnerable and fixed versions
- Prioritize issues that are actually exploitable in the current context
