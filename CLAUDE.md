# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Architecture

This is a **multi-agent skills marketplace** that publishes 5 role-based agents (PM, Engineer, QA, DevOps, Designer) as installable plugins. Each agent contains multiple skills that follow a standardized structure.

### Key Concepts

**Agent Structure:**
- Each agent lives in `agents/{agent-name}/`
- Contains: `README.md`, `skills/`, `test/`
- Agents are role-based (PM, Engineer, QA, DevOps, Designer), not tool-based

**Skill Structure:**
- `SKILL.md` - Public documentation (name, description, usage)
- `_internal/INSTRUCTIONS.md` - Detailed implementation guide for AI agents
- `_internal/modules/` - Optional helper modules
- Skills use YAML frontmatter for metadata

**Document Organization:**
- `docs/` directory is gitignored (working documents only)
- Production documents use feature-based structure: `docs/{agent}/{feature-name}/`
- Document frontmatter includes: `feature`, `version`, `date`, `last_updated`
- Version history tracked via git, not multiple files

**Marketplace Registration:**
- `.claude-plugin/marketplace.json` - Defines all agents and their skills
- `skills-lock.json` - Records installed skills metadata

### Agent Collaboration Flow

```
PM Agent → Designer Agent → Engineer Agent → QA Agent → DevOps Agent
   ↓           ↓               ↓              ↓           ↓
  PRD      UI/UX Spec      Implementation   Testing   Deployment
  BRD      Visual System      Code          Reports   CI/CD
  TRD
```

**Document Dependencies:**
- Engineer reads: `docs/pm/{feature}/`, `docs/design/{feature}/`
- QA reads: `docs/pm/{feature}/`, code implementation
- DevOps reads: `docs/pm/{feature}/TRD.md`
- Designer reads: `docs/pm/{feature}/PRD.md`, `docs/pm/{feature}/BRD.md`

## Development Workflow

### Adding a New Agent

1. Create directory structure:
   ```bash
   mkdir -p agents/{agent-name}/{skills,test}
   ```

2. Create `agents/{agent-name}/README.md` following existing agent patterns

3. For each skill, create:
   - `skills/{skill-name}/SKILL.md`
   - `skills/{skill-name}/_internal/INSTRUCTIONS.md`
   - `test/{skill-name}/evals/evals.json`

4. Register in `.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "{agent-name}-agent",
     "description": "...",
     "skills": ["./agents/{agent-name}/skills/{skill-name}"]
   }
   ```

5. Update `skills-lock.json` with skill metadata

6. Create evaluation tests and run comparisons (with/without skill)

### Skill Design Principles

- **Document-driven**: Skills consume and produce markdown documents
- **Tech-stack agnostic**: Don't assume specific frameworks
- **Minimal and focused**: Each skill has one clear responsibility
- **Independently triggerable**: Skills work standalone, not just in chains
- **Non-technical friendly**: Write for business users first

### Testing Skills

Each skill should have:
- `test/{skill-name}/evals/evals.json` - Test case definitions
- `test/{skill-name}/evals/workspace/eval-{id}/` - Test workspaces
- Comparison tests: with skill vs without skill

### Document Versioning

**DO:**
- Use feature-based directories: `docs/{agent}/{feature-name}/`
- Add frontmatter with version info
- Rely on git history for version tracking
- Update `last_updated` field when modifying

**DON'T:**
- Create date-based subdirectories
- Create multiple version files (PRD-v1.md, PRD-v2.md)
- Commit docs/ to git (it's gitignored)

## Current State

**Implemented Agents (5):**
- `pm-agent` - 7 skills
- `engineer-agent` - 6 skills
- `qa-agent` - 4 skills
- `devops-agent` - 4 skills
- `designer-agent` - 2 skills

**Total Skills:** 23

**Planned Agents:**
- `security` (P1) - Security review, auth/authz, dependency auditing
- `growth_ops` (P1) - Analytics, funnel analysis, feedback synthesis
- `orchestrator` (P2) - Request routing, project state summarization

See `docs/superpowers/plans/2026-03-27-team-agent-expansion.md` for expansion roadmap.

## Important Files

- `.claude-plugin/marketplace.json` - Agent and skill registry
- `skills-lock.json` - Installed skills metadata
- `agents/{agent}/README.md` - Agent documentation
- `docs/superpowers/plans/` - Implementation plans (gitignored but important)
- `docs/superpowers/specs/` - Design specifications (gitignored but important)
