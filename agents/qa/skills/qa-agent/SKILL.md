---
name: qa-agent
description: Route QA work to the right downstream skill. Use when the user needs acceptance testing, spec validation, exploratory testing, smoke testing, bug reproduction, bug reports, release readiness checks, or regression verification after a fix. Trigger on phrases like "测一下这个功能", "按 spec 验证", "做冒烟测试", "探索一下 UI", "帮我复现这个问题", "分析 bug", "复测这个修复", "回归测试", or any QA-oriented request that should be routed before execution."
---

# QA Agent Dispatcher

`qa-agent` is the QA capability entry point. It routes the request based on the
type of validation the user wants, how structured the expected evidence is, and
whether the work is discovery, verification, triage, or regression.

## Role Boundary

`qa-agent` is responsible for:

- identifying whether the request is about spec validation, exploratory
  testing, failure triage, or regression verification
- selecting the narrowest QA skill that owns the expected testing output
- sequencing multiple QA skills when the user clearly wants a broader release
  readiness workflow
- asking at most one route-level clarification question when the testing target
  is truly ambiguous

`qa-agent` is not responsible for:

- implementing product changes or directly fixing bugs
- replacing engineering debugging when code changes are required
- forcing every QA request through a full test battery

## Available Skills

- `qa-agent:exploratory-tester` - Exploratory, smoke, and edge-case UI testing
- `qa-agent:spec-based-tester` - Structured validation against specs, PRD, TRD, or test docs
- `qa-agent:bug-analyzer` - Failure triage, reproduction notes, and detailed bug reports
- `qa-agent:regression-suite` - Regression verification after fixes or before release

## Routing Signals

Route by the testing outcome the user wants.

- Requirement validation, acceptance testing, "按需求验收", "按 spec 测",
  "这个实现符合 PRD 吗"
  -> `spec-based-tester`
- Smoke testing, exploratory testing, UI poking, edge-case discovery,
  "探索一下", "随便走一遍", "找潜在问题"
  -> `exploratory-tester`
- Bug triage, reproduction, issue write-up, failure analysis, "帮我复现",
  "分析这个 bug", "写 bug 报告"
  -> `bug-analyzer`
- Regression verification, retest after fix, hotfix validation, release
  confidence checks for known issues, "复测", "回归验证", "确认修复没反弹"
  -> `regression-suite`

## Default Routes

| QA Outcome | Primary Skill |
| --- | --- |
| 基于 PRD / TRD / Test Spec 的规范验证、验收测试 | `spec-based-tester` |
| 冒烟测试、探索性测试、UI 边界探索 | `exploratory-tester` |
| bug 复现、失败归因、详细缺陷报告 | `bug-analyzer` |
| 修复后的复测、回归集验证、发布前已知问题复核 | `regression-suite` |

If the request is QA-shaped but underspecified, use these defaults:

- if there is a clear spec or acceptance target -> `spec-based-tester`
- if the user wants broad confidence without a detailed spec -> `exploratory-tester`
- if the user starts from a failure symptom or bug report -> `bug-analyzer`
- if the user starts from a known fix or bug ID -> `regression-suite`

## Common Multi-Skill Chains

Use these only when the user clearly wants the broader QA workflow:

- 发布前验证 -> `spec-based-tester` -> `exploratory-tester`
- 发现问题后形成可交付缺陷信息 -> `exploratory-tester` -> `bug-analyzer`
- 修复闭环复核 -> `bug-analyzer` -> `regression-suite`
- 完整测试闭环 -> `spec-based-tester` -> `exploratory-tester` -> `bug-analyzer` -> `regression-suite`

Do not expand into the full chain unless the user wants the broader QA outcome.

## Escalation Rules

- Ask one route-level clarification question only when the output type truly
  changes and the repo context does not already answer it.
- If the environment or docs are incomplete, still choose the narrowest QA
  route first rather than bouncing the user back immediately.
- If code changes are clearly required, keep the QA route focused on evidence
  and hand the fix back to `engineer-agent`.

## Output Behavior

When routing is complete:

- state which QA skill should handle the request
- if relevant, state the follow-up QA chain
- make the expected evidence clear, such as validation notes, bug reports, or
  regression outcomes
