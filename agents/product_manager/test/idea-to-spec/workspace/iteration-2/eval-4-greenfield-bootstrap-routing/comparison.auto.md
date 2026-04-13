# Eval 4: greenfield-bootstrap-routing

## Prompt

这是一个空目录。我想做一个 AI 对话助手，左侧是会话列表，右侧是聊天区。先不要直接初始化项目，先帮我梳理需求并落成 PRD 骨架。

## Expected Assertions

- `empty_workspace_context_summary`: Starts with an empty-workspace context summary instead of immediate scaffolding
- `bootstrap_lane_selected`: Routes the request to PM bootstrap rather than engineering bootstrap
- `pm_docs_named`: Names PM document artifacts as the immediate next step

## Output Presence Check

### With Skill

- [PASS] `with_skill/outputs/transcript.md`

### Without Skill

- [FAIL] `without_skill/outputs/transcript.md`

## Assertion Checks

- [PASS] `empty_workspace_context_summary`: Starts with an empty-workspace context summary instead of immediate scaffolding
  - All checks passed
- [PASS] `bootstrap_lane_selected`: Routes the request to PM bootstrap rather than engineering bootstrap
  - All checks passed
- [PASS] `pm_docs_named`: Names PM document artifacts as the immediate next step
  - All checks passed

## Notes

- Fill in qualitative comparison after reviewing transcripts and docs.
