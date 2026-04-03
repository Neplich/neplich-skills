---
name: devops-agent
description: DevOps Agent intelligent dispatcher - analyzes deployment needs and executes appropriate DevOps skills.
---

# DevOps Agent Dispatcher

DevOps Agent 智能入口，根据部署需求自动选择执行合适的运维 skills。

## Available Skills

- `devops-agent:deployment-planner` - Plan deployment strategy
- `devops-agent:cicd-bootstrap` - Setup CI/CD pipeline
- `devops-agent:env-config-auditor` - Audit environment configuration
- `devops-agent:incident-playbook-writer` - Create incident playbooks

## Step 1: Analyze Context

Identify:
- Is there a TRD with deployment requirements?
- Is this a new deployment setup or an existing one?
- What environment (local, staging, production)?

## Step 2: Select Skill

| User Intent | Skill to Execute |
|-------------|-----------------|
| 部署规划 | deployment-planner |
| 配置 CI/CD | cicd-bootstrap |
| 环境审计 | env-config-auditor |
| 故障手册 | incident-playbook-writer |
| 完整部署流程 | deployment-planner → cicd-bootstrap → env-config-auditor |

If intent is ambiguous, ask the user to clarify before proceeding.

## Step 3: Execute

Invoke the selected skill(s) using the Skill tool.

## Step 4: Present Results

Summarize what was configured and where output files are located.
