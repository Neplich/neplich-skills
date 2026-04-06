# DevOps Agent

负责环境管理、CI/CD 搭建和部署自动化的 Agent。它是按需调用的运维闭环，不是每个功能都必须经过的固定阶段。

## Agent 定位

- **使用者**：个人使用（手动触发）
- **核心场景**：部署方案设计、CI/CD 流程搭建、环境配置管理、故障处理
- **输入来源**：Engineer Agent 的代码与工程文档，必要时结合 PM 的 PRD/TRD 和 QA 状态
- **输出形式**：以可执行配置为主，包括 `deploy/` 目录、CI/CD 配置文件，以及必要的运维说明文档
- **部署范围**：本地开发、Docker 容器化、Kubernetes 集群

---

## Skill 清单

> 所有 skill 源文件统一在 `agents/devops/skills/` 下自管理，通过 `npx skills add ./agents/devops/skills/<name>` 安装到项目运行时。

| Skill | 目录 | 主要用途 | 阶段 |
|-------|------|---------|------|
| `deployment-planner` | `skills/deployment-planner/` | 生成三种部署方案配置（local/docker/helm） | 1. 规划 |
| `cicd-bootstrap` | `skills/cicd-bootstrap/` | 搭建 CI/CD 自动化流程（GitHub Actions/GitLab CI） | 2. 自动化 |
| `env-config-auditor` | `skills/env-config-auditor/` | 审计环境变量和配置完整性 | 3. 审计 |
| `incident-playbook-writer` | `skills/incident-playbook-writer/` | 生成故障处理和回滚手册 | 4. 运维 |

---

## 部署方案设计

DevOps Agent 的主产物优先落在可执行路径，而不是只写说明文档。

### 主要产物类型

- `deploy/` 下的部署配置与运维文档
- `.github/workflows/` 或 `.gitlab-ci.yml` 下的 CI/CD 配置
- 在需要补充说明时，写入 `docs/devops/{feature-name}/`

其中，部署方案默认存放在 `deploy/` 目录：

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

| PM 文档 | DevOps 消费内容 |
|---------|------------------|
| TRD | 技术栈、部署需求、性能要求 |
| PRD | 用户规模、可用性要求 |

### 与 Engineer Agent 的协作流程

1. **Engineer 产出代码与必要工程文档** → 进入可部署状态
2. **DevOps 按需介入** → 生成或更新 `deploy/` 配置、CI/CD、环境审计结果、故障手册
3. **如有缺口** → 用户再决定是回到 `engineer-agent`、`pm-agent` 还是继续 DevOps 工作

DevOps 不是每个项目都必须调用。只有在部署、交付自动化、环境治理或运维准备成为当前任务时，才需要进入这条闭环。

### 典型调用方式

- **首次部署准备**：`deployment-planner -> cicd-bootstrap -> env-config-auditor`
- **已有部署补自动化**：`cicd-bootstrap -> env-config-auditor`
- **发布前运维准备**：`env-config-auditor -> incident-playbook-writer`

---

## 设计原则

1. **自动化优先** — 减少手动操作，一切通过 CI/CD 自动完成
2. **环境隔离** — staging 和 production 严格分离
3. **渐进式部署** — 从简单到复杂（local → docker → helm）
4. **安全第一** — secrets 管理、配置审计
5. **可回滚** — 每次部署都能快速回滚
6. **配置优先** — 优先生成可执行部署配置，再补充说明文档
7. **按需调用** — 不把 DevOps 强行塞进每条功能链路
