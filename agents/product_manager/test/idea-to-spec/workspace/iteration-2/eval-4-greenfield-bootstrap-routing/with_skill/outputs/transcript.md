好的，我们先来完成需求梳理和 PRD 骨架。

**Project context:**
- Directory: `/private/var/folders/4g/9m0612cn1811btk7081t7ych0000gn/T/idea-to-spec-eval-f7vnb5ay-workspace`
- Status: empty
- Tech stack: TBD
- Existing docs: none
- Suggested lane: greenfield-bootstrap
- Likely next step: 在 `idea-to-spec` 内完成需求澄清，逐步产出 PRD 骨架

---

下面进入 **Phase 1：澄清 What & Why**。为了把 PRD 写得扎实，我需要分几个决策点来确认。先从最核心的定位开始：

**Q1：产品定位与目标用户**
基于你的描述，我的初步理解是：

> 一个面向个人用户或小型团队的 Web 端 AI 对话助手，采用经典的"左列表、右聊天"布局。核心价值是提供简洁、低门槛的多轮对话体验。

为了校准方向，请帮我确认或补充以下几点：

1. **目标用户**：主要是个人日常使用（类似 ChatGPT 网页版），还是面向特定工作场景（如程序员辅助编程、文案创作、企业内部知识问答）？
2. **使用平台**：优先桌面 Web 端，还是需要兼顾移动端响应式？
3. **模型来源**：是只对接一个 AI 后端（比如仅 OpenAI / 仅 Claude），还是希望支持多模型切换（用户可自行配置 API Key）？
4. **数据持久化**：聊天记录是保存在浏览器本地（LocalStorage/IndexedDB），还是需要后端持久化+账号体系？

请先回答这几个问题，确认后我们再继续推进功能范围和非目标。