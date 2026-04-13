**Project context:**
- Directory: `/private/var/folders/4g/9m0612cn1811btk7081t7ych0000gn/T/idea-to-spec-eval-858uu6q3-workspace`
- Status: empty
- Tech stack: TBD
- Existing docs: none
- Suggested lane: greenfield-bootstrap
- Likely next step: stay in `idea-to-spec` to shape requirements and draft the PRD skeleton

当前工作区为空，没有现有代码或文档。你的目标是先梳理需求并落成 PRD 骨架，不直接初始化项目——这正好对应 greenfield-bootstrap 的文档先行阶段。

---

为了把"AI 对话助手，左侧会话列表，右侧聊天区"这个想法转化为可落地的 PRD，我们需要先对齐几个核心问题。我会一次聚焦一个决策点。

### 第一步：目标用户与核心场景

关于这个 AI 对话助手，我想确认以下几点（你可以选择确认、补充或修正）：

1. **目标用户是谁？**  
   - 默认假设：普通终端用户（C 端），用于日常问答、写作辅助、学习等通用场景。  
   - 还是特定人群，比如企业内部员工、开发者、某垂直领域用户？

2. **核心使用场景？**  
   - 默认假设：单用户与多个 AI 模型/角色进行多轮对话，需要历史会话管理和上下文连续性。  
   - 是否有团队协作、共享会话、或多人实时协作的需求？

3. **是否只支持单一 AI 模型，还是多模型？**  
   - 默认假设：MVP 阶段先对接一个后端（如 OpenAI/Claude API），但界面预留模型切换入口。

请确认或修正以上假设，我们就可以进入下一步（MVP 功能范围界定）。