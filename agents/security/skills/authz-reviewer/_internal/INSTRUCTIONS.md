# Authorization Reviewer Instructions

## Overview

This skill reviews authentication and authorization implementation to ensure proper access control and secure session management.

## Execution Steps

### Step 1: Understand User Roles and Permissions

1. **Read PM documents** from `docs/pm/{feature-name}/`:
   - PRD: identify user roles, permissions, access levels
   - Extract role definitions (e.g., admin, user, guest)

2. **Create role matrix** - document expected permissions for each role

### Step 2: Analyze Authentication Flow

**A. Find authentication code:**
- Search for login/signup endpoints
- Search for password handling
- Search for token generation (JWT, session)

**B. Check authentication security:**
- Password hashing algorithm (bcrypt, argon2)
- Password strength requirements
- Rate limiting on login attempts
- Account lockout mechanism
- Multi-factor authentication (if applicable)

### Step 3: Analyze Authorization Logic

**A. Find authorization checks:**
- Search for permission checks in routes/controllers
- Search for role-based access control (RBAC)
- Search for middleware/decorators handling authorization

**B. Check authorization coverage:**
- All protected endpoints have authorization checks
- Authorization happens server-side (not just client-side)
- Proper role hierarchy enforcement
- Tenant isolation (for multi-tenant apps)

### Step 4: Review Session Management

**A. Session configuration:**
- Session timeout settings
- Secure cookie flags (httpOnly, secure, sameSite)
- Session regeneration after login
- Proper logout implementation

**B. Token security (if using JWT/tokens):**
- Token expiration
- Token refresh mechanism
- Token storage (not in localStorage for sensitive apps)
- Token revocation capability

### Step 5: Generate Authorization Review Report

Create `docs/security/{feature-name}/authz-review.md`:

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

1. **Role Permission Matrix**
   - Table showing roles and their permissions
   - Expected vs actual implementation

2. **Authentication Flow Analysis**
   - Login flow diagram
   - Password security assessment
   - Session/token generation review

3. **Authorization Coverage**
   - Protected endpoints list
   - Authorization check status for each
   - Missing authorization checks (if any)

4. **Session Management Review**
   - Session configuration assessment
   - Security flags status
   - Session lifecycle handling

5. **Security Issues Found**
   - Critical/High/Medium/Low issues
   - Specific locations and fix recommendations

6. **Recommendations**
   - Priority fixes
   - Best practices to implement

## Output Format

Use tables and diagrams for clarity:

```markdown
## Role Permission Matrix

| Role | View Users | Edit Users | Delete Users | Admin Panel |
|------|-----------|-----------|--------------|-------------|
| Admin | ✅ | ✅ | ✅ | ✅ |
| User | ✅ | ❌ | ❌ | ❌ |
| Guest | ❌ | ❌ | ❌ | ❌ |

## Authorization Issues

### [HIGH] Missing Authorization Check on Delete Endpoint

**Location:** `src/api/users.js:78`

**Issue:** DELETE /api/users/:id has no authorization check

**Risk:** Any authenticated user can delete other users

**Fix:**
\`\`\`javascript
app.delete('/api/users/:id', requireRole('admin'), async (req, res) => {
  // delete logic
});
\`\`\`
```
