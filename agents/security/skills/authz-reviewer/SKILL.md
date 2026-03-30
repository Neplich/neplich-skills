---
name: authz-reviewer
description: Review authentication and authorization logic, check permission models and access control implementation.
---

# Authorization Reviewer

审查认证授权逻辑，检查权限模型和访问控制实现。

## 使用场景

- 实现了用户认证/授权功能
- 需要审查权限模型是否正确
- 多角色/多租户系统的权限检查

## 输入

- 代码库（认证/授权相关代码）
- PM 文档：PRD（用户角色定义）

## 输出

生成 `docs/security/{feature-name}/authz-review.md`，包含：
- 角色权限矩阵
- 认证流程分析
- 授权检查覆盖情况
- 会话管理审查
- 安全问题和修复建议

## 使用方式

```bash
/authz-reviewer
```

---

详细实现指南请查看 `_internal/INSTRUCTIONS.md`
