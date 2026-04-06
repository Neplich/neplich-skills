---
name: env-config-auditor
description: "Use when checking deployment readiness, tracing missing environment variables, or reviewing environment configuration coverage across local, CI/CD, and runtime environments."
---

# Environment Config Auditor

Validate environment configuration completeness and security across all deployment environments.

## When to Use

- Before first deployment
- After adding new features that need env vars
- Troubleshooting deployment issues
- Security audit of configuration

## Context Preflight

Before auditing, inspect the narrowest relevant context:

- code paths that read environment variables
- `deploy/` config that defines local, Docker, or Helm runtime settings
- CI/CD config such as `.github/workflows/` or `.gitlab-ci.yml`
- relevant engineering or PM docs only if they clarify environment-specific constraints

If the repo has no durable deployment/config context yet, suggest running `deployment-planner` first.

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

### 2.4 Check repo-native CI/CD config
Check `.github/workflows/` or `.gitlab-ci.yml` for secret names and deploy-time config references

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

## Step 5 — Generate Durable Audit Report

Write the report to a durable project path:

- prefer `docs/devops/{feature-name}/ENV_AUDIT.md` for feature or release scoped audits
- otherwise use `deploy/ENV_AUDIT.md` for repo-wide deployment audits

Use this structure:

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

Output:

- the audit report path
- the highest-risk missing or unsafe config items
- whether the next likely step is:
  - `deployment-planner`
  - `cicd-bootstrap`
  - direct Engineer follow-up for missing runtime config

## Edge Cases

- **No deploy/ directory**: Suggest running `deployment-planner` first
- **No env vars found**: Verify search patterns for the tech stack
- **Encrypted secrets**: Skip validation, note in report
- **Unknown feature scope**: Use `deploy/ENV_AUDIT.md` instead of inventing a feature folder
