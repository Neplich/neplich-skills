Project context:
- Directory: `/Users/neplich/dev/neplich-skills/agents/product_manager/test/idea-to-spec/workspace/iteration-2/eval-4-greenfield-bootstrap-routing`
- Status: `empty`
- Tech stack: `TBD`
- Existing docs: `no-docs`
- Suggested lane: `greenfield-bootstrap`
- Likely next step: `project-init` (after we stabilize requirements)
- Request shape: greenfield idea, user wants durable PM docs before any engineering bootstrap

明白了，我们先不碰代码脚手架，把需求先聊清楚，再落成 PRD 骨架。

为了把“AI 对话助手”的 PRD 写准确，我需要先确认几个根本性的产品决策。先从最核心的用户与场景开始：

**决策点 1：目标用户与核心场景**

我整理了 3 个最典型的高频方向，请选一个（或告诉我你的变体）：

| 选项 | 目标用户 | 核心场景 | 关键差异 |
|---|---|---|---|
| A. 个人效率助手 | 普通用户 / 知识工作者 | 日常问答、写作辅助、头脑风暴 | 强调轻量、快速、多设备同步 |
| B. 开发者/专业工具 | 程序员、设计师、分析师 | 代码调试、Prompt 迭代、多模型对比 | 强调多模型切换、Markdown/代码渲染、API Key 自定义 |
| C. 企业/团队内部助手 | 企业员工、客服 | 对接内部知识库、权限隔离、审计 | 强调权限管理、数据安全、审计日志 |

**我的默认推荐：B（开发者/专业工具）**，因为“左侧会话列表 + 右侧聊天区”是最接近 ChatGPT/Claude 这类专业对话产品的形态， MVP 上下文最清晰，也最容易定义可验收的功能边界。

请确认：
1. 你倾向哪个方向？（A / B / C / 其它）
2. 你打算先做 **Web 应用**、**桌面端（Electron/Tauri）**，还是 **移动端优先**？
