# Platform Agent

负责环境管理、CI/CD 搭建和部署自动化的 Agent，将代码从开发环境推送到生产环境。

## Agent 定位

- **使用者**：个人使用（手动触发）
- **核心场景**：部署方案设计、CI/CD 流程搭建、环境配置管理、故障处理
- **输入来源**：Engineer Agent 的代码 + TRD 中的部署需求
- **输出形式**：`deploy/` 目录下的部署配置、CI/CD 配置文件、运维手册
- **部署范围**：本地开发、Docker 容器化、Kubernetes 集群

---

## Skill 清单

> 所有 skill 源文件统一在 `agents/platform/skills/` 下自管理，通过 `npx skills add ./agents/platform/skills/<name>` 安装到项目运行时。

| Skill | 目录 | 主要用途 | 阶段 |
|-------|------|---------|------|
| `deployment-planner` | `skills/deployment-planner/` | 生成三种部署方案配置（local/docker/helm） | 1. 规划 |
| `cicd-bootstrap` | `skills/cicd-bootstrap/` | 搭建 CI/CD 自动化流程（GitHub Actions/GitLab CI） | 2. 自动化 |
| `env-config-auditor` | `skills/env-config-auditor/` | 审计环境变量和配置完整性 | 3. 审计 |
| `incident-playbook-writer` | `skills/incident-playbook-writer/` | 生成故障处理和回滚手册 | 4. 运维 |

---

## 部署方案设计

Platform Agent 生成三种部署方案，存放在 `deploy/` 目录：

### 1. Local 方案 (`deploy/local/`)
- **用途**：本地开发调试
- **产出**：启动脚本、环境变量模板、数据库初始化脚本
- **特点**：快速启动，无需容器

### 2. Docker 方案 (`deploy/docker/`)
- **用途**：一键化群体部署
- **产出**：Dockerfile、docker-compose.yml、构建脚本
- **特点**：环境一致性，适合小团队

### 3. Helm 方案 (`deploy/helm/`)
- **用途**：K8s 大型部署
- **产出**：Helm charts、负载均衡配置、扩展策略
- **特点**：高可用、自动扩展

---

## 与其他 Agent 的协作接口

### 与 PM Agent 的接口

| PM 文档 | Platform 消费内容 |
|---------|------------------|
| TRD | 技术栈、部署需求、性能要求 |
| PRD | 用户规模、可用性要求 |

### 与 Engineer Agent 的协作流程

1. **Engineer 完成代码** → 提交 PR
2. **Platform 搭建 CI/CD** → 自动运行测试和构建
3. **PR 合并** → CI/CD 自动部署到 staging
4. **打 tag** → CI/CD 自动部署到 production

---

## 设计原则

1. **自动化优先** — 减少手动操作，一切通过 CI/CD 自动完成
2. **环境隔离** — staging 和 production 严格分离
3. **渐进式部署** — 从简单到复杂（local → docker → helm）
4. **安全第一** — secrets 管理、配置审计
5. **可回滚** — 每次部署都能快速回滚
6. **文档化** — 生成清晰的运维手册
