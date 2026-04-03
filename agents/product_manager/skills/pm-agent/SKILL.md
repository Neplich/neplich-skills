---
name: pm-agent
description: PM Agent intelligent dispatcher - analyzes user intent and automatically selects and executes appropriate PM skills.
---

# PM Agent Dispatcher

PM Agent 智能入口，自动分析用户意图并选择执行合适的 PM skills。

## Available Skills

- `pm-agent:idea-to-spec` - Generate PRD, BRD, TRD, ADR from ideas
- `pm-agent:competitive-brief` - Competitive analysis and positioning
- `pm-agent:competitive-intelligence` - Sales-focused battlecard
- `pm-agent:changelog-generator` - Generate changelog from GitHub
- `pm-agent:release-notes-generator` - Generate user-facing release notes
- `pm-agent:roadmap-generator` - Generate roadmap from GitHub milestones
- `pm-agent:github-reader` - Read GitHub project status

## Step 1: Analyze User Intent

Parse the user's request to identify:
- Primary goal (new product, analysis, documentation, status check)
- Specific artifacts needed (PRD, roadmap, changelog, etc.)
- Context (existing project vs new idea)

## Step 2: Select Skill

| User Intent | Skill to Execute |
|-------------|-----------------|
| 新产品/新功能想法 | idea-to-spec |
| 竞品分析 | competitive-brief |
| 销售 battlecard | competitive-intelligence |
| 生成 changelog | changelog-generator |
| 发版说明 | release-notes-generator |
| 路线图规划 | roadmap-generator |
| 项目状态 | github-reader |
| 完整产品规划 | idea-to-spec → competitive-brief → roadmap-generator |

If intent is ambiguous, ask the user to clarify before proceeding.

## Step 3: Execute

Invoke the selected skill(s) using the Skill tool. For multiple skills, execute in sequence and pass context between them.

## Step 4: Present Results

Summarize what was done and where outputs are located.
