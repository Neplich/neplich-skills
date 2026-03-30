# Dependency Risk Auditor Instructions

## Overview

This skill audits project dependencies for security vulnerabilities, abandoned packages, and supply chain risks.

## Execution Steps

### Step 1: Identify Dependency Files

Search for dependency manifest files:
- `package.json` / `package-lock.json` (Node.js)
- `requirements.txt` / `Pipfile` (Python)
- `go.mod` / `go.sum` (Go)
- `Gemfile` / `Gemfile.lock` (Ruby)
- `pom.xml` / `build.gradle` (Java)
- `Cargo.toml` (Rust)

### Step 2: Run Security Audit Commands

Execute appropriate audit commands based on the ecosystem:

**Node.js:**
```bash
npm audit --json
```

**Python:**
```bash
pip-audit --format json
```

**Go:**
```bash
go list -json -m all | nancy sleuth
```

If audit tools are not available, proceed with manual analysis.

### Step 3: Analyze Dependencies

**A. Known Vulnerabilities:**
- Parse audit output for CVEs
- Classify by severity (Critical/High/Medium/Low)
- Check if vulnerability is exploitable in current usage

**B. Abandoned Packages:**
- Check last update date (>2 years = potential abandonment)
- Check GitHub repo status (archived, no recent commits)
- Check npm/PyPI deprecation notices

**C. Supply Chain Risks:**
- Check for packages with few maintainers
- Check for suspicious recent ownership changes
- Check for typosquatting risks

**D. Transitive Dependencies:**
- Identify high-risk transitive dependencies
- Check dependency tree depth

### Step 4: Generate Dependency Audit Report

Create `docs/security/{feature-name}/dependency-audit.md`:

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
   - Total dependencies count
   - Vulnerabilities found (by severity)
   - Abandoned packages count
   - Overall risk level

2. **Critical Vulnerabilities**
   - Package name and version
   - CVE ID
   - Vulnerability description
   - Exploitability assessment
   - Fix version / mitigation

3. **High/Medium/Low Vulnerabilities**
   - Same format as Critical

4. **Abandoned Packages**
   - Package name
   - Last update date
   - Replacement suggestions

5. **Upgrade Recommendations**
   - Priority order
   - Breaking change warnings
   - Testing requirements

## Output Format

```markdown
### [CRITICAL] Prototype Pollution in lodash

**Package:** lodash@4.17.15
**CVE:** CVE-2020-8203
**Severity:** Critical

**Description:**
Prototype pollution vulnerability allows attackers to modify object prototypes.

**Exploitability:** High - package is used in user input processing

**Fix:**
Upgrade to lodash@4.17.21 or higher
\`\`\`bash
npm install lodash@latest
\`\`\`

**Breaking Changes:** None
```
