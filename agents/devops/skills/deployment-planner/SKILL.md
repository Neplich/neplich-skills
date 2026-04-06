---
name: deployment-planner
description: "Use when a project needs new or updated deployment configuration, when an existing system adds services or deployment targets, or when `deploy/` assets must be created or extended for local, Docker, or Kubernetes environments."
---

# Deployment Planner

Generate three deployment configurations based on project requirements: local development, Docker containerization, and Kubernetes (Helm) orchestration.

## When to Use

- TRD or engineering docs specify deployment requirements
- User asks to set up or update deployment infrastructure
- Project is ready for production deployment
- Need to create deployment configurations from scratch
- Existing deployment config must be extended for a new service, worker, or microservice
- Existing deployment targets must be expanded or revised, such as adding Docker, Helm, staging, or production variants

## Context Preflight

Before generating anything, inspect:

- the current codebase shape and runtime stack
- relevant engineering docs and PM deployment requirements when they exist
- whether `deploy/` already exists
- whether the work is repo-wide or feature-scoped

If `deploy/` already exists, prefer extension or targeted iteration over blind regeneration.

## Input Requirements

Read from engineering docs, PM docs, or ask the user:
- **Tech stack**: Language, framework, database
- **Scale**: Expected users, traffic volume
- **Environment needs**: staging/production split
- **Dependencies**: External services, databases

## Step 1 — Analyze Project Requirements

Read TRD to extract:
- Application type (web app, API, full-stack)
- Runtime requirements (Node.js, Python, Go, etc.)
- Database needs (PostgreSQL, MySQL, Redis, etc.)
- External dependencies (S3, email service, etc.)

If no durable deployment requirements exist, ask the user:
1. What type of application is this?
2. What runtime/language does it use?
3. Does it need a database? Which one?
4. Any external services required?

## Step 2 — Create Local Development Setup (`deploy/local/`)

Generate files for local development:

### 2.1 Create `deploy/local/README.md`

Document:
- Prerequisites (Node.js version, Python version, etc.)
- Quick start commands
- Environment variables needed
- Database setup instructions

### 2.2 Create `deploy/local/.env.example`

Template with all required environment variables:
```
DATABASE_URL=postgresql://localhost:5432/myapp_dev
REDIS_URL=redis://localhost:6379
API_KEY=your_api_key_here
```

### 2.3 Create `deploy/local/start.sh`

Startup script that:
- Checks prerequisites
- Starts database (if needed)
- Runs migrations
- Starts the application

## Step 3 — Create Docker Setup (`deploy/docker/`)

Generate Docker containerization files:

### 3.1 Create `deploy/docker/README.md`

Document:
- Docker and docker-compose installation
- Build and run commands
- Port mappings
- Volume mounts

### 3.2 Create `deploy/docker/Dockerfile`

Multi-stage build optimized for production:
- Use official base images
- Install dependencies
- Copy application code
- Set up non-root user
- Expose ports

### 3.3 Create `deploy/docker/docker-compose.yml`

Define services:
- Application container
- Database container (if needed)
- Redis/cache (if needed)
- Network configuration
- Volume persistence

### 3.4 Create `deploy/docker/.env.example`

Docker-specific environment variables

## Step 4 — Create Kubernetes/Helm Setup (`deploy/helm/`)

Generate Helm charts for K8s deployment:

### 4.1 Create `deploy/helm/README.md`

Document:
- Helm installation
- Chart installation commands
- Configuration options
- Scaling instructions

### 4.2 Create `deploy/helm/Chart.yaml`

Helm chart metadata

### 4.3 Create `deploy/helm/values.yaml`

Default configuration:
- Replica count
- Image repository and tag
- Resource limits (CPU, memory)
- Service type and ports
- Ingress configuration
- Environment variables

### 4.4 Create `deploy/helm/templates/`

K8s resource templates:
- `deployment.yaml` - Application deployment
- `service.yaml` - Service definition
- `ingress.yaml` - Ingress rules (if needed)
- `configmap.yaml` - Configuration
- `secret.yaml` - Secrets template
- `hpa.yaml` - Horizontal Pod Autoscaler (if needed)

## Step 5 — Verify Directory Structure

Ensure all files are created:

```bash
tree deploy/
```

Expected structure:
```
deploy/
├── local/
│   ├── README.md
│   ├── .env.example
│   └── start.sh
├── docker/
│   ├── README.md
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
└── helm/
    ├── README.md
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── deployment.yaml
        ├── service.yaml
        ├── ingress.yaml
        ├── configmap.yaml
        ├── secret.yaml
        └── hpa.yaml
```

## Step 6 — Summary

Output:
```
## 部署配置生成完成

已创建三种部署方案：

### Local 开发环境
- 位置: `deploy/local/`
- 启动: `cd deploy/local && ./start.sh`
- 用途: 本地开发调试

### Docker 容器化
- 位置: `deploy/docker/`
- 启动: `cd deploy/docker && docker-compose up`
- 用途: 一键部署，环境一致性

### Kubernetes (Helm)
- 位置: `deploy/helm/`
- 安装: `helm install myapp ./deploy/helm`
- 用途: 生产环境，高可用，自动扩展

### 下一步建议
- 使用 `cicd-bootstrap` skill 搭建自动化部署流程
- 使用 `env-config-auditor` skill 检查配置完整性
```

## Edge Cases

- **No database**: Skip database-related configurations
- **Monorepo**: Generate separate configs for each service
- **Existing deploy/ directory**: Ask user before overwriting
- **Unsupported tech stack**: Search for official deployment guides

## Output Rules

- Primary outputs belong under `deploy/`
- Prefer executable config over prose-only explanation
- Add `README.md` files only where they help someone use the generated deployment assets
- Do not automatically create CI/CD config here; hand off to `cicd-bootstrap` when needed
