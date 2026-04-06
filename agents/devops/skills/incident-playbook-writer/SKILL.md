---
name: incident-playbook-writer
description: "Use when a deployed system needs rollback guidance, incident response instructions, troubleshooting runbooks, or on-call preparation tied to the repository's actual deployment setup."
---

# Incident Playbook Writer

Create operational runbooks for common incidents and failure scenarios.

## When to Use

- Before first production deployment
- After experiencing an incident
- Setting up on-call procedures
- Need rollback documentation
- After adding a new service, worker, or deployment target
- When existing rollback or troubleshooting docs are outdated
- When operational procedures must be revised after topology or release-process changes

## Context Preflight

Before generating playbooks, inspect:

- which deployment methods are actually configured under `deploy/`
- current CI/CD and operational entrypoints if they affect rollback or incident response
- whether this is a repo-wide runbook or tied to a specific feature/release
- existing runbooks so you can extend rather than overwrite by habit

## Step 1 — Identify Deployment Method

Check which deployment methods are configured:
```bash
ls deploy/docker/ deploy/helm/ 2>/dev/null
```

Also inspect whether local-only deployment exists and whether rollback is even meaningful for the current setup.

## Step 2 — Create Rollback Playbook

### 2.1 Create `deploy/ROLLBACK.md`

For Docker deployment:
- How to rollback to previous image version
- Database migration rollback steps
- Cache clearing procedures

For Helm deployment:
- `helm rollback` command
- Check rollback status
- Verify application health

## Step 3 — Create Incident Response Guide

### 3.1 Create `deploy/INCIDENT_RESPONSE.md`

Common scenarios:
- **Application Down**: Health check, logs, restart procedure
- **Database Connection Failed**: Check credentials, network, restart
- **High CPU/Memory**: Identify cause, scale up, restart
- **Deployment Failed**: Rollback steps, log collection

## Step 4 — Create Troubleshooting Guide

### 4.1 Create `deploy/TROUBLESHOOTING.md`

Debug commands:
- View logs: `docker logs` / `kubectl logs`
- Check status: `docker ps` / `kubectl get pods`
- Access shell: `docker exec` / `kubectl exec`
- Check resources: CPU, memory, disk usage

## Step 5 — Create On-Call Guide

### 5.1 Create `deploy/ON_CALL.md`

Document:
- Escalation contacts
- Critical alerts and thresholds
- Response time expectations
- Communication channels

## Step 6 — Summary

Output:
```
## 运维手册生成完成

已创建以下文档：

- `deploy/ROLLBACK.md` - 回滚操作指南
- `deploy/INCIDENT_RESPONSE.md` - 故障响应流程
- `deploy/TROUBLESHOOTING.md` - 问题排查手册
- `deploy/ON_CALL.md` - 值班指南

### 建议
- 团队成员熟悉这些流程
- 定期演练回滚操作
```

## Edge Cases

- **No deploy/ directory**: Create it first
- **Custom deployment**: Ask for specific procedures
- **Multiple services**: Generate separate playbooks

## Output Rules

- Primary outputs belong in durable operational paths under `deploy/`
- Tie instructions to the repository's actual deployment methods and commands
- Do not generate generic on-call prose detached from the configured runtime
