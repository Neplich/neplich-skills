---
name: qa-agent
description: Route QA work to the right downstream skill. Use when the user needs documented acceptance, exploratory discovery, failure reproduction, or fix verification. Trigger on phrases like "测一下这个功能", "按 spec 验证", "做冒烟测试", "探索一下 UI", "帮我复现这个问题", "分析 bug", "复测这个修复", "回归测试", or any QA-oriented request that should be routed before execution.
---

# QA Agent Dispatcher

`qa-agent` is the QA capability entry point. It routes the request based on the
evidence outcome the user wants, the repository context available, and whether
the work is documented acceptance, exploratory discovery, failure reproduction,
or fix verification.

## Role Boundary

`qa-agent` is responsible for:

- identifying whether the request is about documented acceptance, exploratory
  discovery, failure reproduction, or fix verification
- selecting the narrowest QA skill that owns the expected testing output
- carrying PM and implementation context into the selected QA skill
- stating the expected evidence artifact for the chosen route
- asking at most one route-level clarification question when the testing target
  is truly ambiguous

`qa-agent` is not responsible for:

- implementing product changes or directly fixing bugs
- replacing engineering debugging when code changes are required
- prescribing fixed port, framework, or browser assumptions before repo context
- expanding requested verification into broad discovery by default
- forcing every QA request through a full test battery

## Shared QA Document Contract

When QA work is feature-scoped, use `docs/qa/<feature-name>/` as the durable
QA directory before falling back to ad hoc report paths.

- `TEST_SPEC.md` is the suite index, coverage summary, and traceability record.
- `test-cases/` stores reusable executable or manual test cases.
- Each E2E test case must live in its own Markdown file:
  `test-cases/TC-NNN-<short-slug>.md`.
- `FILE_EXPLORATION.md` records project file exploration used to derive or
  expand test cases.
- `reports/` may store execution reports for validation, exploratory, bug, or
  regression runs.

For standalone QA or E2E requests where PM has not supplied PRD / TRD / Test
Spec cases, route the downstream skill with this required sequence:

1. Read `docs/qa/<feature-name>/TEST_SPEC.md` and
   `docs/qa/<feature-name>/test-cases/*.md` first.
2. Ask the user whether there are new feature changes and whether QA should
   explore the project files to expand test cases.
3. If the user requests exploration, keep file discovery targeted, write or
   update `FILE_EXPLORATION.md`, and add any new E2E coverage as one file per
   test case under `test-cases/`.
4. Execute from the existing and newly added test case files, rather than
   rediscovering the full project on every run.

## Available Skills

- `qa-agent:exploratory-tester` - Exploratory, smoke, and edge-case UI testing
- `qa-agent:spec-based-tester` - Structured validation against specs, PRD, TRD, or test docs
- `qa-agent:bug-analyzer` - Failure triage, reproduction notes, and detailed bug reports
- `qa-agent:regression-suite` - Regression verification after fixes or before release

## Routing Signals

Route by the evidence outcome the user wants.

- 文档化验收、规范验证、"按需求验收", "按 spec 测", "这个实现符合 PRD 吗"
  -> `spec-based-tester`
- 探索式发现、冒烟、边界发现、"探索一下", "随便走一遍", "找潜在问题"
  -> `exploratory-tester`
- 失败复现、缺陷写作、归因整理、"帮我复现", "分析这个 bug", "写 bug 报告"
  -> `bug-analyzer`
- 修复验证、回归扫测、已知问题复核、"复测", "回归验证", "确认修复没反弹"
  -> `regression-suite`

## Default Routes

| QA Outcome | Primary Skill |
| --- | --- |
| 文档化验收、规范验证 | `spec-based-tester` |
| 探索式发现、冒烟、边界发现 | `exploratory-tester` |
| 失败复现、缺陷写作、归因整理 | `bug-analyzer` |
| 修复验证、回归扫测、已知问题复核 | `regression-suite` |

If the request is QA-shaped but underspecified, use these defaults:

- if there is a clear documented acceptance target -> `spec-based-tester`
- if the user wants exploratory discovery -> `exploratory-tester`
- if the user starts from a failure symptom or defect report -> `bug-analyzer`
- if the user starts from a known fix or bug ID -> `regression-suite`

## Escalation Rules

- Ask one route-level clarification question only when the evidence target truly
  changes and the repo context does not already answer it.
- If the environment or docs are incomplete, still choose the narrowest QA
  route first rather than bouncing the user back immediately.
- If code changes are clearly required, keep the QA route focused on evidence
  and hand the fix back to `engineer-agent`.

## Output Behavior

When routing is complete:

- state which QA skill should handle the request
- state the expected evidence artifact for the route
