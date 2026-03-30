# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库工作时提供指导。

## 仓库架构

这是一个**多 Agent 技能市场**，发布 6 个基于角色的 Agent（PM、Engineer、QA、DevOps、Designer、Security）作为可安装插件。每个 Agent 包含多个遵循标准化结构的 skills。

### 核心概念

**Agent 结构：**
- 每个 agent 位于 `agents/{agent-name}/`
- 包含：`README.md`、`skills/`、`test/`
- Agent 基于角色（PM、Engineer、QA、DevOps、Designer、Security），而非工具

**Skill 结构：**
- `SKILL.md` - 公开文档（名称、描述、用法）
- `_internal/INSTRUCTIONS.md` - AI agent 的详细实现指南
- `_internal/modules/` - 可选的辅助模块
- Skills 使用 YAML frontmatter 存储元数据

**文档组织：**
- `docs/` 目录被 gitignore（仅工作文档）
- 生产文档使用基于功能的结构：`docs/{agent}/{feature-name}/`
- 文档 frontmatter 包含：`feature`、`version`、`date`、`last_updated`
- 版本历史通过 git 跟踪，不创建多个文件

**Marketplace 注册：**
- `.claude-plugin/marketplace.json` - 定义所有 agents 及其 skills
- `skills-lock.json` - 记录已安装 skills 的元数据

### Agent 协作流程

```
PM Agent → Designer Agent → Engineer Agent → QA Agent → DevOps Agent → Security Agent
   ↓           ↓               ↓              ↓           ↓              ↓
  PRD      UI/UX 规范       代码实现        测试报告    部署配置      安全审查
  BRD      视觉系统                                    CI/CD
  TRD
```

**文档依赖关系：**
- Engineer 读取：`docs/pm/{feature}/`、`docs/design/{feature}/`
- QA 读取：`docs/pm/{feature}/`、代码实现
- DevOps 读取：`docs/pm/{feature}/TRD.md`
- Designer 读取：`docs/pm/{feature}/PRD.md`、`docs/pm/{feature}/BRD.md`
- Security 读取：`docs/pm/{feature}/`、代码库

## 开发工作流

### 添加新 Agent

1. 创建目录结构：
   ```bash
   mkdir -p agents/{agent-name}/{skills,test}
   ```

2. 创建 `agents/{agent-name}/README.md`，参考现有 agent 模式

3. 为每个 skill 创建：
   - `skills/{skill-name}/SKILL.md`
   - `skills/{skill-name}/_internal/INSTRUCTIONS.md`
   - `test/{skill-name}/evals/evals.json`

4. 在 `.claude-plugin/marketplace.json` 中注册：
   ```json
   {
     "name": "{agent-name}-agent",
     "description": "...",
     "skills": ["./agents/{agent-name}/skills/{skill-name}"]
   }
   ```

5. 更新 `skills-lock.json` 添加 skill 元数据

6. 创建评估测试并运行对比（使用/不使用 skill）

### Skill 设计原则

- **文档驱动**：Skills 消费和产出 markdown 文档
- **技术栈无关**：不假设特定框架
- **最小化和聚焦**：每个 skill 有一个明确职责
- **独立触发**：Skills 可独立工作，不仅限于链式调用
- **非技术友好**：优先为业务用户编写

### 测试 Skills

每个 skill 应包含：
- `test/{skill-name}/evals/evals.json` - 测试用例定义
- `test/{skill-name}/evals/workspace/eval-{id}/` - 测试工作区
- 对比测试：使用 skill vs 不使用 skill

### 文档版本管理

**应该做：**
- 使用基于功能的目录：`docs/{agent}/{feature-name}/`
- 添加 frontmatter 包含版本信息
- 依赖 git 历史进行版本跟踪
- 修改时更新 `last_updated` 字段

**不应该做：**
- 创建基于日期的子目录
- 创建多个版本文件（PRD-v1.md、PRD-v2.md）
- 将 docs/ 提交到 git（已被 gitignore）

## 当前状态

**已实现的 Agents (6):**
- `pm-agent` - 7 个 skills
- `engineer-agent` - 6 个 skills
- `qa-agent` - 4 个 skills
- `devops-agent` - 4 个 skills
- `designer-agent` - 2 个 skills
- `security-agent` - 4 个 skills

**总计 Skills:** 27

**计划中的 Agents:**
- `growth_ops` (P1) - 分析、漏斗分析、反馈综合
- `orchestrator` (P2) - 请求路由、项目状态总结

参见 `docs/superpowers/plans/2026-03-27-team-agent-expansion.md` 了解扩展路线图。

## 重要文件

- `.claude-plugin/marketplace.json` - Agent 和 skill 注册表
- `skills-lock.json` - 已安装 skills 的元数据
- `agents/{agent}/README.md` - Agent 文档
- `docs/superpowers/plans/` - 实现计划（gitignored 但重要）
- `docs/superpowers/specs/` - 设计规范（gitignored 但重要）

