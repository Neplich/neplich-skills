# Dev Agent Skills for Codex

通过 Codex 的原生 skill 发现机制安装本仓库的 Agent skills。

## 快速安装

在 Codex 中输入：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/Neplich/dev-agent-skills/refs/heads/main/.codex/INSTALL.md
```

Codex 会先反问你两个问题，再执行安装：

1. 安装范围是 `personal` 还是 `project`
2. 安装 `all` agents，还是从多个 agents 中选择安装

## 可安装的 Agent

- `pm-agent`：产品规划、需求文档、路线图、发版说明
- `engineer-agent`：代码分析、项目搭建、功能实现、测试、调试、交付
- `qa-agent`：探索测试、规范测试、Bug 分析、回归验证
- `devops-agent`：部署规划、CI/CD、环境审计、故障处理
- `designer-agent`：UI/UX 设计、视觉系统、界面规范，仅产出设计文档不写代码
- `security-agent`：应用安全、权限审查、依赖风险、隐私映射

如果选择 `selected`，支持一次选择多个 Agent。

## 安装层级

### Personal

适合希望在所有项目里复用这些 Agent 的场景。

- 仓库 clone 到 `~/.codex/dev-agent-skills`
- skills 暴露到 `~/.agents/skills/dev-agent-skills/`

### Project

适合只想在当前项目里启用这些 Agent 的场景。

- 仓库 clone 到 `<project>/.codex/dev-agent-skills`
- skills 暴露到 `<project>/.agents/skills/dev-agent-skills/`

## 手动安装

### 前置条件

- 已安装 Codex
- 已安装 Git

### 1. 选择安装层级

`personal` 和 `project` 二选一。

Personal:

```bash
CLONE_ROOT="$HOME/.codex/dev-agent-skills"
SKILL_ROOT="$HOME/.agents/skills/dev-agent-skills"
```

Project:

```bash
PROJECT_ROOT="$PWD"
CLONE_ROOT="$PROJECT_ROOT/.codex/dev-agent-skills"
SKILL_ROOT="$PROJECT_ROOT/.agents/skills/dev-agent-skills"
```

### 2. clone 或更新仓库

如果目标目录已存在：

```bash
git -C "$CLONE_ROOT" pull --ff-only
```

否则：

```bash
mkdir -p "$(dirname "$CLONE_ROOT")"
git clone https://github.com/Neplich/dev-agent-skills.git "$CLONE_ROOT"
```

### 3. 选择安装全部或部分 Agent

安装时使用一个聚合目录，只暴露你选中的 Agent：

```bash
rm -rf "$SKILL_ROOT"
mkdir -p "$SKILL_ROOT"
```

Agent 到目录的映射如下：

- `pm-agent` -> `agents/product_manager`
- `engineer-agent` -> `agents/engineer`
- `qa-agent` -> `agents/qa`
- `devops-agent` -> `agents/devops`
- `designer-agent` -> `agents/designer`
- `security-agent` -> `agents/security`

例如只安装 `pm-agent`、`engineer-agent`、`qa-agent`：

```bash
ln -s "$CLONE_ROOT/agents/product_manager" "$SKILL_ROOT/product_manager"
ln -s "$CLONE_ROOT/agents/engineer" "$SKILL_ROOT/engineer"
ln -s "$CLONE_ROOT/agents/qa" "$SKILL_ROOT/qa"
```

如果要安装全部 Agent，就把六个目录都链接进去。

### 4. 重启 Codex

退出并重新打开 Codex，让它重新发现 skills。

## 这套安装方式是怎么工作的

Codex 会在启动时扫描 skill 目录。这里采用的是“聚合目录 + 按 Agent 暴露”的方式。

Personal 安装示意：

```text
~/.agents/skills/dev-agent-skills/
├── product_manager -> ~/.codex/dev-agent-skills/agents/product_manager
├── engineer -> ~/.codex/dev-agent-skills/agents/engineer
├── qa -> ~/.codex/dev-agent-skills/agents/qa
├── devops -> ~/.codex/dev-agent-skills/agents/devops
├── designer -> ~/.codex/dev-agent-skills/agents/designer
└── security -> ~/.codex/dev-agent-skills/agents/security
```

Project 安装时，路径换成当前项目下的 `.codex/` 和 `.agents/`。

虽然底层暴露的是 Agent 目录，但用户使用时仍然只需要使用 Agent 入口命令，例如 `/pm-agent`、`/engineer-agent`。

## 使用示例

安装完成后，可以在 Codex 中这样用：

```text
/pm-agent "我想做一个任务管理应用"
/engineer-agent "实现用户登录功能"
/qa-agent "测试登录功能"
/devops-agent "配置 CI/CD"
/designer-agent "设计用户登录界面"
/security-agent "进行安全审查"
```

## 更新

### Personal

```bash
git -C "$HOME/.codex/dev-agent-skills" pull --ff-only
```

### Project

```bash
git -C "$PWD/.codex/dev-agent-skills" pull --ff-only
```

更新后如果没有立即生效，重启 Codex。

## 卸载

### Personal

```bash
rm -rf "$HOME/.agents/skills/dev-agent-skills"
rm -rf "$HOME/.codex/dev-agent-skills"
```

### Project

```bash
rm -rf "$PWD/.agents/skills/dev-agent-skills"
rm -rf "$PWD/.codex/dev-agent-skills"
```

如果你只想减少已安装 Agent，不需要删 clone，只需要重建 `SKILL_ROOT` 并只保留需要的 Agent 链接。

## 排障

- 看不到命令时，先检查 `SKILL_ROOT` 下的符号链接是否正确，再重启 Codex。
- 使用 `project` 安装时，需要在同一个项目目录里打开 Codex。
- 如果你原先安装的是全部 Agent，后来改成部分安装，记得重建聚合目录，不要保留旧链接。
