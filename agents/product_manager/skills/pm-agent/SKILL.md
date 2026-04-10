---
name: pm-agent
description: Route PM work to the right downstream skill. Use when the user needs product discovery, idea shaping, requirement clarification, scope definition, spec creation or updates, competitor research, release communication, roadmap planning, changelog generation, or GitHub project status. Trigger on phrases like "做个 PRD", "梳理需求", "定义范围", "已有 spec 要改", "竞品分析", "battlecard", "生成 changelog", "写发版说明", "做路线图", "项目状态", "milestone 进度", "有哪些 PR 卡住了", or any PM-level request that should be routed before execution."
---

# PM Agent Dispatcher

`pm-agent` is the PM capability entry point. It classifies the user's PM goal,
routes to the narrowest downstream PM skill, and defines follow-up chains only
when the broader outcome clearly spans multiple PM capabilities.

## Role Boundary

`pm-agent` is responsible for:

- identifying the primary PM outcome the user wants
- selecting the narrowest PM skill that owns that outcome
- sequencing multiple PM skills when the request clearly spans discovery,
  status, planning, and release communication
- asking at most one route-level clarification question when the target outcome
  is truly ambiguous

`pm-agent` is not responsible for:

- running the full design or document-writing protocol itself
- duplicating the domain logic of `idea-to-spec`, `competitive-brief`,
  `competitive-intelligence`, `changelog-generator`,
  `release-notes-generator`, `roadmap-generator`, or `github-reader`
- continuing into design implementation, engineering execution, QA, DevOps, or
  security work

## Available Skills

- `pm-agent:idea-to-spec` - Product discovery, scope shaping, spec creation, spec updates
- `pm-agent:competitive-brief` - Competitive analysis, positioning, market comparison
- `pm-agent:competitive-intelligence` - Sales-facing battlecards and deal support
- `pm-agent:changelog-generator` - Developer-facing changelog generation from GitHub
- `pm-agent:release-notes-generator` - User-facing release notes and announcements
- `pm-agent:roadmap-generator` - Roadmap creation or sync from GitHub planning signals
- `pm-agent:github-reader` - GitHub status, milestones, backlog, PR queue, blockers

## Routing Signals

Route by the user's intended PM outcome, not by literal wording.

- Product discovery, feature framing, scope convergence, requirement shaping,
  spec creation, spec updates, "把想法变成文档", "收敛需求", "定义边界"
  -> `idea-to-spec`
- Competitor research, positioning comparison, market scan, messaging gaps,
  "竞品分析", "我们和 X 怎么比"
  -> `competitive-brief`
- Sales battlecard, objection handling, deal support, field enablement,
  "battlecard", "销售怎么讲我们和 X 的差异"
  -> `competitive-intelligence`
- Changelog, what changed, unreleased changes, version history, "这个版本改了什么"
  -> `changelog-generator`
- Release notes, release announcement, customer-facing release summary,
  "发版说明", "what's new", "用户版本说明"
  -> `release-notes-generator`
- Roadmap, future planning, upcoming work, milestone-driven planning,
  "路线图", "接下来做什么", "版本规划"
  -> `roadmap-generator`
- Repo health, milestone progress, issue backlog, review queue, release blockers,
  "项目状态", "有哪些 PR 卡住", "release ready 吗"
  -> `github-reader`

## Default Routes

| PM Outcome | Primary Skill |
| --- | --- |
| 新想法、新功能、范围收敛、已有 spec 更新 | `idea-to-spec` |
| 竞品分析、定位比较、市场情报 | `competitive-brief` |
| 销售 battlecard、deal support | `competitive-intelligence` |
| changelog、版本差异、未发布改动 | `changelog-generator` |
| 发版说明、发布公告、面向用户的版本总结 | `release-notes-generator` |
| 路线图、里程碑规划、后续优先级 | `roadmap-generator` |
| 项目状态、milestone 进度、backlog、PR 队列、阻塞项 | `github-reader` |

If the request is PM-shaped but underspecified, use these defaults:

- if it is about feature direction, scope, requirements, or docs -> `idea-to-spec`
- if it is about current repo/project state -> `github-reader`
- if it is about communicating shipped work -> choose
  `changelog-generator` for developer-facing output and
  `release-notes-generator` for user-facing output

## Common Multi-Skill Chains

Use these only when the user clearly wants the broader PM workflow:

- 完整产品规划 -> `idea-to-spec` -> `competitive-brief` -> `roadmap-generator`
- 先看项目状态再做规划 -> `github-reader` -> `roadmap-generator`
- 先整理变更再写对外版本说明 -> `changelog-generator` -> `release-notes-generator`
- 先做产品收敛再准备发布沟通 -> `idea-to-spec` -> `release-notes-generator`

Do not expand into a multi-skill PM chain unless the broader follow-up is
explicitly requested or strongly implied by the user's end goal.

## Escalation Rules

- Ask one route-level clarification question only when two routes are equally
  plausible and the output type materially changes.
- If fresh GitHub data is needed for roadmap or release communication, route to
  the PM skill that owns the final output; it may pull GitHub context itself.
- If the user is actually asking for UI/UX deliverables, stop PM routing at the
  PM handoff and point the next step to `designer-agent`.
- If the user is asking to build or modify software, finish the PM routing and
  point the next step to `engineer-agent`.

## Output Behavior

When routing is complete:

- state which PM skill should handle the request
- if relevant, state the follow-up PM chain
- preserve settled PM context so the downstream skill does not need to reopen
  route decisions
