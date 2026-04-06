# 产品经理 Agent

基于本地仓库和 GitHub 项目资产的产品管理 Agent，负责收敛需求、维护 PM 文档，并在需要时把结果交接给 Designer 或 Engineer。

## Agent 定位

- **使用者**：个人使用（手动触发）
- **核心场景**：应用开发项目的需求分析、范围收敛、产品文档维护、路线图与版本信息管理
- **输入来源**：本地 `docs/`、代码库现状，以及 GitHub 的 Issues / PRs / Milestones / Releases
- **输出形式**：Markdown 文档，写入项目 `docs/` 目录
- **行业背景**：不限，依项目目标群体而定

---

## Skill 清单

> 所有 skill 源文件统一在 `agents/product_manager/skills/` 下自管理，通过 `npx skills add ./agents/product_manager/skills/<name>` 安装到项目运行时（`.agents/skills/`）。

### 核心 Skill

| Skill | 目录 | 主要用途 | 安全评级 |
|-------|------|---------|---------|
| `idea-to-spec` | `skills/idea-to-spec/` | feature 设计、spec 变更、PRD/BRD/TRD/ADR 流程 | ✅ 低风险 |
| `competitive-brief` | `skills/competitive-brief/` | 竞品简报、定位差距、Battlecard | ✅ 低风险 |
| `changelog-generator` | `skills/changelog-generator/` | 从 GitHub PR/Commits/Release Tags 生成版本日志 | ✅ 低风险 |
| `github-reader` | `skills/github-reader/` | 读取 GitHub 仓库状态（Issues/PRs/Milestones），为 PM 提供项目健康报告 | ✅ 低风险 |
| `roadmap-generator` | `skills/roadmap-generator` | 从 GitHub Milestones/Issues 生成或更新路线图 | ✅ 低风险 |
| `release-notes-generator` | `skills/release-notes-generator/` | 生成面向用户的发版说明，与 changelog-generator 互补 | ✅ 低风险 |

### 按需使用

| Skill | 目录 | 说明 |
|-------|------|------|
| `competitive-intelligence` | `skills/competitive-intelligence/` | 销售向竞品 Battlecard（HTML），有 ToB 销售场景时使用 |

### 已排除

| Skill | 原因 |
|-------|------|
| ~~`github-project-management`~~ | Gen 安全评级 Critical Risk，依赖 alpha 版 claude-flow MCP |

---

## 运行模型

PM Agent 是一个按需调用的 PM 闭环，不是固定流水线的第一个必经阶段。

它的典型闭环是：

1. 读取本地文档、仓库上下文和 GitHub 项目状态
2. 收敛需求、范围、优先级和产品决策
3. 写出可复用的 PM 文档
4. 在需要跨角色协作时，把文档交给 Designer 或 Engineer

常见 handoff 方式：

- `PM -> Designer`：需要专门的 UI/UX 或视觉设计阶段
- `PM -> Engineer`：已有足够产品信息，可以直接实施
- `PM` 独立完成：只做需求分析、路线图、版本信息或项目状态管理

---

## idea-to-spec 能力覆盖

`idea-to-spec` 已覆盖以下三类场景，无需额外安装对应 skill：

- `borghei/claude-skills@product-manager` → **由 idea-to-spec 覆盖**
- `davila7/claude-code-templates@agile-product-owner` → **由 idea-to-spec 覆盖**
- `smithery.ai@github-prd` → **由 idea-to-spec/prd-gen 覆盖**

内置子模块：`prd-gen` / `brd-gen` / `api-gen` / `trd-gen` / `adr-gen` / `mermaid-gen` / `weekly-report-gen`

---

## 管理的文档结构

### Feature 级 PM 文档

feature 级 PM 文档采用 feature-based 结构：

```text
docs/
└── pm/
    └── {feature-name}/
        ├── PRD.md
        ├── BRD.md
        ├── DECISIONS.md
        └── TRD.md
```

其中：

- `PRD.md`：功能需求、用户故事、验收标准
- `BRD.md`：业务目标、目标用户、商业背景
- `DECISIONS.md`：已确认决策、待确认问题、假设、被否决方案
- `TRD.md`：早期技术范围和约束，后续可由 Engineer 接手细化

### Repo 级 PM 产物

不是所有 PM 产物都属于某个单独 feature。跨 feature 或 repo 级 PM 产物仍可保留在更通用的位置，例如：

- `docs/roadmap.md`
- `docs/changelog.md`
- `docs/release-notes/`

---

## 与其他 Agent 的接口

### 向 Designer 交接

Designer 主要消费：

- `docs/pm/{feature}/PRD.md`
- `docs/pm/{feature}/BRD.md`
- `docs/pm/{feature}/DECISIONS.md`

### 向 Engineer 交接

Engineer 主要消费：

- `docs/pm/{feature}/PRD.md`
- `docs/pm/{feature}/DECISIONS.md`
- `docs/pm/{feature}/TRD.md`（如果存在）

---

## 当前状态

1. ~~自建 `changelog-generator` skill~~ ✅ 已完成
2. ~~自建 `github-reader` skill~~ ✅ 已完成
3. ~~自建 `roadmap-generator` skill~~ ✅ 已完成
4. ~~自建 `release-notes-generator` skill~~ ✅ 已完成
5. 逐步自动化触发（GitHub webhook → Agent）
