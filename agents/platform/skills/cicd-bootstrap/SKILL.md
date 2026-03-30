---
name: cicd-bootstrap
description: "Set up CI/CD automation pipelines for GitHub Actions or GitLab CI. Use when the user wants to automate testing, building, and deployment. Trigger on phrases like 'setup CI/CD', 'automate deployment', 'GitHub Actions', 'GitLab CI', or when deployment configs exist but CI/CD is missing."
---

# CI/CD Bootstrap

Generate CI/CD pipeline configurations that automate testing, building, and deployment based on the deployment strategy (local/docker/helm).

## When to Use

- Deployment configs exist in `deploy/` directory
- User wants to automate the deployment process
- Need to set up GitHub Actions or GitLab CI
- Project is ready for continuous deployment

## Input Requirements

Detect or ask:
- **Git platform**: GitHub or GitLab
- **Deployment target**: Which deployment method to use (docker/helm)
- **Environments**: staging and/or production
- **Deployment triggers**: On PR merge, on tag, manual

## Step 1 — Detect Git Platform and Deployment Method

Check which platform:
```bash
ls .github/ 2>/dev/null && echo "GitHub" || ls .gitlab-ci.yml 2>/dev/null && echo "GitLab"
```

Check available deployment methods:
```bash
ls deploy/docker/ deploy/helm/ 2>/dev/null
```

## Step 2 — Create GitHub Actions Workflow (if GitHub)

### 2.1 Create `.github/workflows/ci.yml`

CI workflow for pull requests:
- Checkout code
- Setup runtime (Node.js/Python/Go)
- Install dependencies
- Run linter
- Run tests
- Build application

### 2.2 Create `.github/workflows/deploy-staging.yml`

Auto-deploy to staging on main branch merge:
- Run CI checks
- Build Docker image (if using docker)
- Push to container registry
- Deploy to staging environment

### 2.3 Create `.github/workflows/deploy-production.yml`

Deploy to production on tag creation:
- Trigger on: `v*.*.*` tags
- Run full CI checks
- Build production image
- Deploy to production
- Create GitHub release

## Step 3 — Create GitLab CI Config (if GitLab)

### 3.1 Create `.gitlab-ci.yml`

Define stages and jobs:
- **test stage**: lint, test, build
- **deploy-staging stage**: auto-deploy on main
- **deploy-production stage**: manual trigger or on tag

## Step 4 — Configure Secrets

Document required secrets in `deploy/SECRETS.md`:

For GitHub Actions:
- `DOCKER_USERNAME` / `DOCKER_PASSWORD` (if using Docker Hub)
- `KUBECONFIG` (if using K8s)
- `STAGING_SERVER` / `PRODUCTION_SERVER` (if using SSH)

For GitLab CI:
- Add secrets in Settings → CI/CD → Variables

## Step 5 — Test CI/CD Pipeline

Create a test commit to verify:
```bash
git checkout -b test-cicd
echo "# CI/CD Test" >> README.md
git add README.md
git commit -m "test: verify CI/CD pipeline"
git push origin test-cicd
```

Check pipeline status in GitHub Actions or GitLab CI

## Step 6 — Summary

Output:
```
## CI/CD 配置完成

已创建自动化部署流程：

### CI Pipeline
- 位置: `.github/workflows/ci.yml` 或 `.gitlab-ci.yml`
- 触发: 每次 PR 提交
- 步骤: lint → test → build

### Staging 部署
- 触发: main 分支合并
- 自动部署到 staging 环境

### Production 部署
- 触发: 创建 v*.*.* tag
- 部署到 production 环境

### 需要配置的 Secrets
见 `deploy/SECRETS.md`

### 下一步建议
- 使用 `env-config-auditor` 检查环境变量
- 创建第一个 PR 测试 CI 流程
```

## Edge Cases

- **No deploy/ directory**: Run `deployment-planner` first
- **Existing CI config**: Ask before overwriting
- **Multiple deployment targets**: Generate separate workflows
- **Custom build steps**: Ask user for specific commands
