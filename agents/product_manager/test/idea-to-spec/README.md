# idea-to-spec Eval Running Guide

本目录用于评估 `idea-to-spec` 在功能设计对话中的行为质量，而不只是最终文档内容。

## 评估目标

`idea-to-spec` 的 eval 重点检查以下能力是否稳定触发：

- 先读取项目上下文并输出 context summary
- 单决策点推进，而不是并行追问多个未确认问题
- 在关键设计点上提供 `2-3` 个方案和 trade-off
- 按 section 逐段推进并等待确认
- 使用 `docs/pm/{feature-name}/DECISIONS.md` 作为持久记忆源
- 对已收敛 section 进行增量落档
- 在阶段结束后执行文档收束
- 在空工作区的新产品请求里保持 PM-first，而不是直接进入工程脚手架

## 目录结构

```text
agents/product_manager/test/idea-to-spec/
├─ COMPARISON_TEMPLATE.md
├─ README.md
├─ SUMMARY.md
├─ evals/
│  └─ evals.json
└─ workspace/
   ├─ iteration-1/
   │  ├─ eval-1-existing-project-feature/
   │  ├─ eval-2-existing-project-update/
   │  └─ eval-3-greenfield-discovery/
   └─ iteration-2/
      └─ eval-4-greenfield-bootstrap-routing/
```

每个 eval workspace 建议包含：

- 最小项目上下文文件，例如 `README.md`、`package.json`、`docs/...`
- `with_skill/outputs/` 目录
- `without_skill/outputs/` 目录
- `eval_metadata.json`

`eval_metadata.json` 中的输出项支持两种写法：

- 单一路径字符串：表示该产物必须存在
- 路径数组：表示这些路径中任意一个存在即可，用于 `design.md` / `PRD.md` 这类阶段性替代产物

断言项支持机器检查字段：

- `target`: 要检查的文件路径，默认 `with_skill/outputs/transcript.md`
- `all_of`: 必须全部出现的文本片段
- `any_of`: 至少出现一个的文本片段
- `none_of`: 不允许出现的文本片段
- `count_at_least`: 某段文本最少出现多少次

如果断言只有 `id`、`description` 而没有这些字段，runner 会把它标记为 `MANUAL`。

## 运行约定

### With Skill

在对应 workspace 根目录运行，显式启用 `idea-to-spec` skill。

期望结果：

- 输出遵循设计协议
- 若进入文档化阶段，产物优先写入 `docs/pm/{feature-name}/...`
- 对话或产物能体现 `DECISIONS.md`、section gate、增量落档

### Without Skill

在同一个 workspace 根目录运行，但不显式启用 `idea-to-spec` skill。

期望结果：

- 作为对照组，观察是否更容易直接给大段方案
- 是否缺少 context summary、方案比较、section 推进、文档记忆

## 评估步骤

1. 进入某个 eval workspace 根目录。
2. 读取该目录下的 `eval_metadata.json`。
3. 用 metadata 里的 `prompt` 运行一次 with-skill 版本。
4. 将输出写入 `with_skill/outputs/`。
5. 再运行一次 without-skill 版本。
6. 将输出写入 `without_skill/outputs/`。
7. 根据 `assertions` 做人工或脚本检查。
8. 如有需要，在该 eval 目录下补 `comparison.md` 记录对比结论。

建议区分两类报告：

- `comparison.auto.md`：由 helper 自动生成，记录输出存在性和断言清单
- `comparison.md`：人工补充的质量分析与结论

建议使用共享模板：

- [COMPARISON_TEMPLATE.md](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/COMPARISON_TEMPLATE.md)

建议在每轮主要评测后更新总览：

- [SUMMARY.md](/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/SUMMARY.md)

## 输出约定

对于 `idea-to-spec`，允许输出分为两类：

- 对话式输出记录
- 写入 workspace 内 feature 文档后的文件产物

建议至少保留以下一种：

- `with_skill/outputs/transcript.md`
- `without_skill/outputs/transcript.md`

如果产物写入了 workspace 内的 `docs/`，建议在 transcript 里记录：

- 写入了哪些路径
- 哪些 decision 被确认
- 当前停在哪个 section

如果某个 eval 允许阶段性产物，可以在 metadata 中把输出写成数组，例如：

- `["docs/pm/app-tags/design.md", "docs/pm/app-tags/PRD.md"]`

## 断言类型

`idea-to-spec` 的断言分为两类：

### 行为断言

- 是否先做上下文检测
- 是否单决策点推进
- 是否提供方案比较
- 是否按 section 推进
- 是否使用文档作为记忆源

### 产物断言

- 是否创建或更新了 `docs/pm/{feature-name}/DECISIONS.md`
- 是否把收敛后的 section 写入 PM 文档
- 是否在文档正文中使用稳定、表述性的语言

## 迭代方式

当 prompt 有重大更新时：

1. 新建 `workspace/iteration-N/`
2. 复制上一轮需要保留的 eval workspace
3. 重新运行 with/without skill
4. 对比上一轮结论是否退化

不要直接覆盖上一轮 workspace，避免失去回归基线。

## 建议补充物

后续如果要进一步自动化，建议补：

- 一个统一的 `comparison.md` 模板
- 一个简单的断言执行脚本
- transcript 命名约定和保存格式
