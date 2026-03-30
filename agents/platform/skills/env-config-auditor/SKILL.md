---
name: env-config-auditor
description: "Audit environment variables and configuration completeness across local, staging, and production environments. Use when checking deployment readiness, validating configs, or troubleshooting missing environment variables. Trigger on phrases like 'check config', 'audit environment', 'missing env vars', 'config validation'."
---

# Environment Config Auditor

Validate environment configuration completeness and security across all deployment environments.

## When to Use

- Before first deployment
- After adding new features that need env vars
- Troubleshooting deployment issues
- Security audit of configuration

## Step 1 — Scan for Required Environment Variables

Search codebase for env var usage:
```bash
grep -r "process.env\." --include="*.js" --include="*.ts" || \
grep -r "os.getenv" --include="*.py" || \
grep -r "os.Getenv" --include="*.go"
```

Extract all unique environment variable names.

## Step 2 — Check Configuration Files

Compare env vars across environments:

### 2.1 Check `deploy/local/.env.example`
List all variables defined

### 2.2 Check `deploy/docker/.env.example`
List all variables defined

### 2.3 Check CI/CD secrets documentation
Check `deploy/SECRETS.md` if exists

## Step 3 — Identify Missing Variables

Create a comparison table:

| Variable | Code Usage | Local | Docker | Helm | CI/CD |
|----------|-----------|-------|--------|------|-------|
| DATABASE_URL | ✅ | ✅ | ✅ | ❌ | ✅ |
| API_KEY | ✅ | ❌ | ❌ | ❌ | ❌ |

## Step 4 — Check for Security Issues

Scan for common security problems:

### 4.1 Hardcoded secrets
```bash
grep -r "password\s*=\s*['\"]" --include="*.js" --include="*.py" --include="*.go"
```

### 4.2 Unsafe defaults
Check for:
- `DEBUG=true` in production configs
- Default passwords
- Exposed ports

### 4.3 Missing required secrets
Verify sensitive vars are not in `.env.example` with real values

## Step 5 — Generate Audit Report

Create `tmp/config-audit-report.md`:

```markdown
# Environment Configuration Audit Report

## Missing Variables
- API_KEY: Missing in all environments
- DATABASE_URL: Missing in Helm config

## Security Issues
- ⚠️ Hardcoded password found in backend/config.js:42
- ⚠️ DEBUG=true in docker/.env.example

## Recommendations
1. Add API_KEY to all .env.example files
2. Remove hardcoded credentials
3. Set DEBUG=false for production
```

## Step 6 — Summary

Output findings and action items to user.

## Edge Cases

- **No deploy/ directory**: Suggest running `deployment-planner` first
- **No env vars found**: Verify search patterns for the tech stack
- **Encrypted secrets**: Skip validation, note in report
