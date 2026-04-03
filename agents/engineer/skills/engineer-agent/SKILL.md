---
name: engineer-agent
description: Engineer Agent intelligent dispatcher - analyzes context and automatically selects appropriate engineering skills.
---

# Engineer Agent Dispatcher

Engineer Agent 智能入口，根据项目状态和用户需求自动选择执行合适的工程 skills。

## Available Skills

- `engineer-agent:codebase-analyzer` - Analyze project structure and tech stack
- `engineer-agent:project-bootstrap` - Initialize new project based on TRD
- `engineer-agent:feature-implementor` - Implement features based on PM docs
- `engineer-agent:test-writer` - Write tests based on Test Spec
- `engineer-agent:debugger` - Debug and fix issues
- `engineer-agent:delivery` - Git workflow, commits, PRs

## Step 1: Analyze Context

Check project state:
- Is this a new project or existing codebase?
- Are there PM documents available in `docs/`?
- Is there existing code to analyze?
- What is the current git status?

## Step 2: Select Skill

| User Intent | Skill to Execute |
|-------------|-----------------|
| 分析项目 | codebase-analyzer |
| 初始化项目 | project-bootstrap |
| 实现功能 | feature-implementor |
| 编写测试 | test-writer |
| 修复 bug | debugger |
| 创建 PR/交付 | delivery |
| 完整开发流程 | codebase-analyzer → feature-implementor → test-writer → delivery |

If intent is ambiguous, ask the user to clarify before proceeding.

## Step 3: Execute

Invoke the selected skill(s) using the Skill tool. For multi-step flows, pass context between skills.

## Step 4: Present Results

Summarize execution results and output locations.
