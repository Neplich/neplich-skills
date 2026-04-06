# DevOps Skill Evals

最小 DevOps eval 基线目录。

当前先覆盖 `env-config-auditor`，用于验证：

- skill 是否把环境审计结果写到 durable artifact，而不是 `tmp/`
- 报告是否能同时检查 `deploy/` 和 CI/CD 配置
- 断言是否与当前 DevOps canonical model 一致

运行方式：

```bash
python3 agents/devops/test/run_eval.py \
  agents/devops/test/env-config-auditor/workspace/iteration-1/eval-1-missing-variables/eval_metadata.json
```

自动报告会生成到对应 eval 目录下的 `comparison.auto.md`。
