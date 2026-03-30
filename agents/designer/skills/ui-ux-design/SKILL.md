---
name: ui-ux-design
description: Design UI/UX flows and specifications with optional reference website analysis. Outputs user journeys, page layouts, and ASCII prototypes.
---

# UI/UX Design

设计用户体验流程和界面规范，支持参考网站风格分析。

## 使用场景

- 需要设计新产品的用户界面
- 需要重新设计现有产品的交互流程
- 需要参考优秀网站的设计模式

## 输入

- PM 文档：PRD、BRD、TRD
- 可选：参考网站 URL

## 输出

生成 `docs/design/ui-ux-spec.md`，包含：
- 用户旅程图（Mermaid）
- 页面清单和布局
- ASCII 界面原型
- 交互行为说明

## 使用方式

```bash
# 基础使用
/ui-ux-design

# 指定参考网站
/ui-ux-design --reference https://example.com
```

---

详细实现指南请查看 `_internal/INSTRUCTIONS.md`
