# idea-to-spec Eval Summary

本文件汇总 `idea-to-spec` 当前 4 个核心 eval case 的状态、主要发现和后续待补点。

## Case Overview

| Eval | Scenario | Status | Main Finding | Follow-up |
| --- | --- | --- | --- | --- |
| Eval 1 | Existing project feature | Reviewed + Auto-checked | Skill 协议有效；eval 已允许 `design.md` 作为阶段性产物 | 可继续增强 transcript 结构检查 |
| Eval 2 | Existing project update | Reviewed + Auto-checked | Skill update lane 有效；自动断言已覆盖 decision history 更新 | 可继续增强 blast-radius 细粒度检查 |
| Eval 3 | Greenfield discovery | Reviewed + Auto-checked | Skill discovery mode 有效；自动断言已覆盖确认 checkpoint | 可继续增强“延后文档化”的文本信号检查 |
| Eval 4 | Empty-workspace PM-first bootstrap routing | Defined | 覆盖空目录下的产品请求，防止直接掉到工程脚手架 | 需要补 with/without transcript 对照运行 |

## Key Conclusions

- 当前 `idea-to-spec` 协议在已有三类已运行场景上都明显优于无 skill 对照组
- 目前暴露的问题主要在 eval 定义精度，而不是主 prompt 方向
- Eval 1 / 2 / 3 当前都已有基础机器断言覆盖，不再只依赖文件存在性检查
- Eval 4 新增了空工作区 PM-first 守门场景，用于回归“不要直接初始化项目”
- `idea-to-spec` 的新协议已经形成可回归的最小基线：
  - context summary
  - 单决策点推进
  - `2-3` 个方案加 trade-off
  - section-based progression
  - `DECISIONS.md` 作为持久记忆
  - 增量落档与阶段收束

## Linked Artifacts

- 总体运行说明: [README.md](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/README.md)
- 人工对比模板: [COMPARISON_TEMPLATE.md](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/COMPARISON_TEMPLATE.md)
- Eval definitions: [evals.json](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/evals/evals.json)

### Eval 1

- Metadata: [eval_metadata.json](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/workspace/iteration-1/eval-1-existing-project-feature/eval_metadata.json)
- Auto report: [comparison.auto.md](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/workspace/iteration-1/eval-1-existing-project-feature/comparison.auto.md)
- Review: [comparison.md](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/workspace/iteration-1/eval-1-existing-project-feature/comparison.md)

### Eval 2

- Metadata: [eval_metadata.json](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/workspace/iteration-1/eval-2-existing-project-update/eval_metadata.json)
- Auto report: [comparison.auto.md](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/workspace/iteration-1/eval-2-existing-project-update/comparison.auto.md)
- Review: [comparison.md](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/workspace/iteration-1/eval-2-existing-project-update/comparison.md)

### Eval 3

- Metadata: [eval_metadata.json](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/workspace/iteration-1/eval-3-greenfield-discovery/eval_metadata.json)
- Auto report: [comparison.auto.md](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/workspace/iteration-1/eval-3-greenfield-discovery/comparison.auto.md)
- Review: [comparison.md](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/workspace/iteration-1/eval-3-greenfield-discovery/comparison.md)

### Eval 4

- Metadata: [eval_metadata.json](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/workspace/iteration-2/eval-4-greenfield-bootstrap-routing/eval_metadata.json)
- Fixture: [README.md](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/workspace/iteration-2/eval-4-greenfield-bootstrap-routing/README.md)

## Next Improvements

1. Run and review Eval 4 with and without skill to confirm the new PM-first guardrail holds in practice.
2. Add stronger automated checks for behavioral assertions instead of relying mostly on manual review.
3. Standardize transcript format so turn-by-turn confirmation discipline is easier to verify.
