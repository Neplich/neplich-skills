---
name: privacy-surface-mapper
description: Map personal data collection points and privacy compliance requirements for GDPR/CCPA.
---

# Privacy Surface Mapper

映射个人数据收集点，识别隐私合规要求。

## 使用场景

- 应用收集用户个人信息
- 需要进行 GDPR/CCPA 合规检查
- 需要生成隐私影响评估

## 输入

- 代码库（数据收集和存储代码）
- PM 文档：PRD（功能和数据需求）

## 输出

生成 `docs/security/{feature-name}/privacy-map.md`，包含：
- 个人数据收集清单
- 数据存储和传输分析
- 用户权利实现状态（访问、删除、导出）
- 合规风险和建议

## 使用方式

```bash
/privacy-surface-mapper
```

---

详细实现指南请查看 `_internal/INSTRUCTIONS.md`
