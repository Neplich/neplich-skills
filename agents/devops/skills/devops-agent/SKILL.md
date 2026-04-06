---
name: devops-agent
description: Use when the user needs deployment planning, CI/CD setup, environment configuration auditing, or incident readiness for an implemented system.
---

# DevOps Agent Dispatcher

`devops-agent` 是运维能力入口。它负责识别当前任务属于部署规划、CI/CD、配置审计还是故障手册，并把请求路由到正确的下游 DevOps skill。

## Role Boundary

`devops-agent` is responsible for:

- identifying the primary DevOps intent
- selecting the narrowest downstream DevOps skill
- sequencing multiple DevOps skills only when the user clearly wants a broader operational workflow
- asking route-level clarification only when the request is ambiguous

`devops-agent` is not responsible for:

- generating all deployment configs itself
- replacing `deployment-planner`, `cicd-bootstrap`, `env-config-auditor`, or `incident-playbook-writer`
- forcing every feature through a DevOps phase
- acting as a cross-repo orchestrator

## Available Skills

- `devops-agent:deployment-planner` - Generate deployment configs under `deploy/`
- `devops-agent:cicd-bootstrap` - Generate CI/CD automation config
- `devops-agent:env-config-auditor` - Audit env/config completeness and security
- `devops-agent:incident-playbook-writer` - Create rollback and incident playbooks

## Routing Protocol

1. Inspect the current operational context:
   - Is there implementation ready to deploy?
   - Is there a `deploy/` directory already?
   - Is CI/CD already configured?
   - Is this feature-scoped work or repo-wide operational work?
2. Read the narrowest useful upstream context:
   - relevant engineering docs when deployment or config depends on technical design
   - release-facing PM docs only when scale, availability, or rollout requirements matter
   - QA status only when deployment readiness depends on validation state
3. Choose the narrowest downstream skill.
4. If the user clearly wants a broader operational workflow, define the follow-up sequence.
5. If intent is ambiguous, ask one route-level clarification question.

## Default Routing Table

| User Intent | Skill to Execute |
|-------------|-----------------|
| 部署规划 / `deploy/` 新建或扩展 | `deployment-planner` |
| 配置 CI/CD | `cicd-bootstrap` |
| 环境变量 / 配置审计 | `env-config-auditor` |
| 回滚 / 故障手册 | `incident-playbook-writer` |

## Common Multi-Skill Chains

Use these only when the user wants the broader outcome:

- 首次部署准备 -> `deployment-planner` -> `cicd-bootstrap` -> `env-config-auditor`
- 发布前运维准备 -> `env-config-auditor` -> `incident-playbook-writer`
- 现有部署补自动化 -> `cicd-bootstrap` -> `env-config-auditor`

Do not expand into a full operational chain by default.

## Output Behavior

When routing is complete:

- state which DevOps skill should handle the request
- if relevant, state the follow-up DevOps chain
- make it clear whether the expected outputs are:
  - executable artifacts under `deploy/`
  - CI/CD config under repo-native paths such as `.github/workflows/`
  - durable operational docs under `docs/devops/` or `deploy/`
