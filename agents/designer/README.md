# Designer Agent

负责将 PM 文档转化为可实现的界面与视觉设计文档，作为 PM 和 Engineer 之间的可选设计 handoff。

## Agent 定位

- **使用者**：个人使用（手动触发）
- **核心场景**：UI/UX 设计、视觉风格定义、界面原型
- **输入来源**：PM Agent 的 PRD/BRD/DECISIONS/TRD 文档
- **输出形式**：`docs/design/{feature-name}/` 目录下的设计文档（Markdown + Mermaid + ASCII 原型）
- **技术栈无关**：不生成代码，只提供设计规范

---

## Skill 清单

> 所有 skill 源文件统一在 `agents/designer/skills/` 下自管理，通过 `npx skills add ./agents/designer/skills/<name>` 安装到项目运行时。

| Skill | 目录 | 主要用途 | 阶段 |
|-------|------|---------|------|
| `ui-ux-design` | `skills/ui-ux-design/` | 设计 UX 流程和 UI 规范，支持参考网站风格分析 | 1. 交互设计 |
| `visual-design` | `skills/visual-design/` | 定义设计系统（颜色、字体、组件）和文案指南 | 2. 视觉设计 |

---

## 运行模型

Designer Agent 是按需调用的设计闭环，不是每个功能开发都必须经过的固定阶段。

它的典型闭环是：

1. 读取 PM 文档
2. 收敛交互设计和视觉系统
3. 写出 Engineer 可消费的设计文档

常见 handoff 是：

- `PM -> Designer`
- `Designer -> Engineer`

如果某个功能不需要单独设计阶段，可以直接走 `PM -> Engineer`。

---

## 设计流程

```text
PM 文档 (PRD/BRD/DECISIONS/TRD)
     │
     ▼
┌──────────────┐
│ui-ux-design  │ ← 询问参考网站 → 分析风格 → UX 流程 + UI 规范
└──────┬───────┘
       │
┌──────▼───────┐
│visual-design │ ← 设计系统 + 文案指南
└──────────────┘
       │
       ▼
  Engineer 实现
```

---

## 与其他 Agent 的协作接口

### 与 PM Agent 的接口

| PM 文档 | Designer 消费内容 |
|---------|------------------|
| `docs/pm/{feature}/PRD.md` | 功能需求、用户故事、使用场景 |
| `docs/pm/{feature}/BRD.md` | 目标用户、业务目标、品牌调性 |
| `docs/pm/{feature}/DECISIONS.md` | 已确认决策、待确认问题、设计约束 |
| `docs/pm/{feature}/TRD.md` | 技术约束、性能要求、平台限制 |

### 与 Engineer Agent 的协作流程

1. **PM 完成文档** → PRD/BRD/DECISIONS/TRD
2. **Designer 设计界面** → UX 流程 + UI 规范 + 设计系统
3. **Engineer 实现代码** → 根据设计文档选择技术栈实现

---

## 输出目录结构

Designer Agent 的输出统一放在 feature-based 目录：

```text
docs/
└── design/
    └── {feature-name}/
        ├── UI_UX_SPEC.md
        └── VISUAL_SYSTEM.md
```

---

## 设计原则

1. **文档优先** — 输出清晰的设计文档，而非直接生成代码
2. **技术栈无关** — 不依赖特定前端框架，Engineer 可自由选择实现方式
3. **轻量实用** — 小团队适用的轻量设计系统，避免过度设计
4. **可视化优先** — 使用 Mermaid 图表和 ASCII 布局图辅助说明
5. **风格参考** — 支持分析参考网站，提取可复用的设计模式
6. **无障碍意识** — 设计系统包含基础无障碍要求
