---
name: appsec-checklist
description: Scan codebase for common security vulnerabilities and generate security checklist report before release.
---

# AppSec Checklist

扫描代码库中的常见安全漏洞，生成应用安全检查清单。

## 使用场景

- 功能开发完成，准备发布前
- 需要进行安全自查
- 需要生成安全审查报告

## 输入

- 代码库（自动扫描）
- PM 文档：PRD、TRD（了解功能和架构）

## 输出

生成 `docs/security/{feature-name}/appsec-checklist.md`，包含：
- 安全漏洞清单（按风险等级分类）
- 不安全配置检查
- 输入验证问题
- 认证/会话管理问题
- 修复建议

## 使用方式

```bash
/appsec-checklist
```

---

详细实现指南请查看 `_internal/INSTRUCTIONS.md`
