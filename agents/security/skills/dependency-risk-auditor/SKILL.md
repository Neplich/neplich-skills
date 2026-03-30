---
name: dependency-risk-auditor
description: Audit project dependencies for known vulnerabilities, abandoned packages, and supply chain risks.
---

# Dependency Risk Auditor

审计项目依赖的安全风险，识别漏洞和废弃包。

## 使用场景

- 项目使用了第三方依赖
- 需要进行供应链安全审查
- 准备发布前的依赖检查

## 输入

- 依赖清单文件（package.json, requirements.txt, go.mod 等）
- 代码库

## 输出

生成 `docs/security/{feature-name}/dependency-audit.md`，包含：
- 已知漏洞清单
- 废弃包识别
- 高风险依赖分析
- 升级建议和缓解措施

## 使用方式

```bash
/dependency-risk-auditor
```

---

详细实现指南请查看 `_internal/INSTRUCTIONS.md`
