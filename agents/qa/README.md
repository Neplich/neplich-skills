# QA Agent

面向验证与证据输出的 QA dispatcher 型 Agent。它负责识别请求是规范验收、探索测试、缺陷分析还是修复后的回归验证，并把请求路由到最合适的 QA skill。

## Agent 定位

- **使用者**：个人使用（手动触发）
- **核心场景**：规范验收、UI 交互测试、边界测试、探索测试、Bug 复现与分析、回归验证、发布前测试把关
- **输入来源**：PM Agent 的 Test Spec + PRD + TRD
- **输出形式**：测试报告（简洁版）+ Bug 报告（详细版，Markdown 或 GitHub Issue）
- **测试范围**：UI 交互测试 + 边界测试（补充 Engineer 未覆盖的场景）

---

## Skill 清单

> 所有 skill 源文件统一在 `agents/qa/skills/` 下自管理，通过 `npx skills add ./agents/qa/skills/<name>` 安装到项目运行时。

| Skill | 目录 | 主要用途 | 阶段 |
|-------|------|---------|------|
| `exploratory-tester` | `skills/exploratory-tester/` | 自动探索 UI，发现文档未覆盖的问题 | 1. 探索 |
| `spec-based-tester` | `skills/spec-based-tester/` | 基于 Test Spec 执行标准测试用例（UI 交互 + 边界测试） | 2. 规范测试 |
| `bug-analyzer` | `skills/bug-analyzer/` | 分析测试失败，生成详细 Bug 报告（Markdown 或 GitHub Issue） | 3. Bug 分析 |
| `regression-suite` | `skills/regression-suite/` | 管理回归测试套件，验证 Bug 修复效果 | 4. 回归验证 |

---

## 与其他 Agent 的协作接口

### 与 PM Agent 的接口

| PM 文档 | QA 消费内容 |
|---------|------------|
| Test Spec | 测试场景、测试数据、覆盖要求 |
| PRD | 功能需求、用户故事、验收标准 |
| TRD | 技术实现细节、架构约束 |

### 与 Engineer Agent 的协作流程

1. **Engineer 实现完成** → 提交代码
2. **QA 手动触发测试** → 执行 `spec-based-tester` + `exploratory-tester`
3. **发现 Bug** → 使用 `bug-analyzer` 生成报告
4. **Engineer 修复** → 提交修复代码
5. **QA 回归验证** → 使用 `regression-suite` 验证修复

## 入口路由策略

QA Agent 按验证目标来路由：

- 基于 PRD / TRD / Test Spec 的规范验证、验收测试 -> `spec-based-tester`
- 冒烟测试、探索性测试、UI 边界探索 -> `exploratory-tester`
- bug 复现、失败归因、详细缺陷报告 -> `bug-analyzer`
- 修复后的复测、回归集验证、发布前已知问题复核 -> `regression-suite`

默认兜底规则：

- 有明确 spec 或验收目标时优先 `spec-based-tester`
- 没有稳定 spec 但用户要“走一遍看看”时优先 `exploratory-tester`
- 从失败现象或缺陷单开始时优先 `bug-analyzer`
- 从“这个修复好了没有”开始时优先 `regression-suite`

---

## 设计原则

1. **探索优先** — 不局限于 Test Spec，主动发现潜在问题
2. **环境自适应** — 自动检测和启动测试环境
3. **详细可追溯** — Bug 报告包含完整复现信息
4. **补充而非重复** — 关注 Engineer 覆盖不到的场景（UI 交互、边界条件）
5. **Chrome 优先** — 先保证主流浏览器支持
6. **手动触发** — 不做自动化监听，保持简单
