<div align="center">

# Neplich Agent Skills

面向产品、工程和测试协作的 Agent Skills Marketplace。

通过一个仓库统一发布 3 个可安装 Agent：
`pm-agent`、`engineer-agent`、`qa-agent`。

[概览](#概览) • [包含的-agent](#包含的-agent) • [使用方式](#使用方式) • [仓库结构](#仓库结构) • [开发说明](#开发说明)

</div>

这个仓库用于集中管理一组面向软件交付流程的 Agent Skills。当前包含 Product Manager、Engineer、QA 三类 Agent，共 17 个 skills，可按角色独立安装，也可以按团队流程组合使用。

> [!NOTE]
> 该仓库本身是 marketplace 源。用户安装时，先添加 marketplace，再按需安装某个 Agent。

## 概览

仓库中的三个 Agent 分别覆盖产品文档、工程实现和质量验证三个环节：

- `pm-agent`：负责需求梳理、规格生成、路线图、版本说明和 GitHub 状态读取
- `engineer-agent`：负责代码库理解、项目初始化、功能实现、测试、调试和交付
- `qa-agent`：负责探索测试、规范测试、Bug 分析和回归验证

这种拆分方式适合文档驱动的协作流程：

1. PM 先产出 PRD、TRD、ADR、Test Spec 等文档
2. Engineer 基于文档实现代码并完成交付
3. QA 基于文档和产物执行测试、分析问题、做回归验证

## 包含的 Agent

| Agent | 作用 | Skills |
| --- | --- | --- |
| [`pm-agent`](./agents/product_manager/README.md) | 产品文档、竞品分析、路线图、版本日志、发版说明、GitHub 项目读取 | 7 |
| [`engineer-agent`](./agents/engineer/README.md) | 代码分析、项目搭建、功能实现、测试编写、调试修复、交付管理 | 6 |
| [`qa-agent`](./agents/qa/README.md) | 探索测试、规范测试、Bug 分析、回归验证 | 4 |

## 使用方式

```bash
# 1. 添加 marketplace
/plugin marketplace add neplich/neplich-skills

# 2. 安装 QA Agent（一次性获得全部 4 个 skills）
/plugin install qa-agent@neplich-agent-skills
```

同理安装其他 Agent：

```bash
/plugin install pm-agent@neplich-agent-skills
/plugin install engineer-agent@neplich-agent-skills
```

## 仓库结构

```text
.
├── .claude-plugin/
│   └── marketplace.json
├── agents/
│   ├── engineer/
│   ├── product_manager/
│   └── qa/
├── docs/
└── skills-lock.json
```

关键目录说明：

- `.claude-plugin/marketplace.json`：定义 marketplace 名称、插件列表和每个 Agent 暴露的 skills
- `agents/product_manager/`：PM Agent 的 README、skills 和测试样例
- `agents/engineer/`：Engineer Agent 的 README、skills 和测试样例
- `agents/qa/`：QA Agent 的 README、skills 和测试样例
- `skills-lock.json`：记录已收录 skills 的锁定信息

## 开发说明

如果你要继续维护这个仓库，通常只需要关注这几类修改：

- 新增或调整某个 Agent 的能力：修改对应 `agents/<agent>/skills/`
- 更新 Agent 说明文档：修改对应 `agents/<agent>/README.md`
- 调整 marketplace 暴露出的插件或 skills：修改 `.claude-plugin/marketplace.json`

建议把根 README 保持在“入口文档”的层级，只说明仓库定位、安装方式和 Agent 分工；更细的 skill 设计和使用细节，放到各 Agent 自己的 README 中维护。
