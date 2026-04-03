---
name: qa-agent
description: QA Agent intelligent dispatcher - analyzes testing needs and executes appropriate QA skills.
---

# QA Agent Dispatcher

QA Agent 智能入口，根据测试需求自动选择执行合适的测试 skills。

## Available Skills

- `qa-agent:exploratory-tester` - Exploratory testing
- `qa-agent:spec-based-tester` - Spec-based testing
- `qa-agent:bug-analyzer` - Bug analysis and reporting
- `qa-agent:regression-suite` - Regression test management

## Step 1: Analyze Context

Identify:
- Is there a spec/PRD to test against?
- Is this a bug report or general testing request?
- Is this a regression check or new feature test?

## Step 2: Select Skill

| User Intent | Skill to Execute |
|-------------|-----------------|
| 探索性测试 | exploratory-tester |
| 规范测试 | spec-based-tester |
| 分析 bug | bug-analyzer |
| 回归测试 | regression-suite |
| 完整测试 | spec-based-tester → exploratory-tester → regression-suite |

If intent is ambiguous, ask the user to clarify before proceeding.

## Step 3: Execute

Invoke the selected skill(s) using the Skill tool.

## Step 4: Present Results

Summarize test results and output report locations.
