# Repository Guidance

This file provides repository-level guidance for AI coding agents working in this project.

## Repository Architecture

This repository is a multi-agent skill marketplace. It publishes 6 role-based agents for product, engineering, QA, DevOps, design, and security workflows. Each agent contains multiple skills that follow a standardized structure.

### Core Concepts

**Agent structure**

- Each agent lives under `agents/{agent-name}/`
- Each agent contains `README.md`, `skills/`, and `test/`
- Agents are organized by role rather than by tool

**Skill structure**

- `SKILL.md` is the public skill document
- `_internal/INSTRUCTIONS.md` contains detailed implementation guidance for the agent
- `_internal/modules/` may contain optional support modules
- Skills use YAML frontmatter for metadata

**Documentation organization**

- `docs/superpowers/` is gitignored and reserved for working docs
- Public project documentation should follow `docs/{agent}/{feature-name}/`
- Document frontmatter should include `feature`, `version`, `date`, and `last_updated`
- Version history should be tracked in git rather than separate versioned files

**Marketplace registration**

- `.claude-plugin/marketplace.json` defines all agents and their skills
- `skills-lock.json` stores installed skill metadata

### Agent Collaboration Flow

```text
PM Agent → Designer Agent → Engineer Agent → QA Agent → DevOps Agent → Security Agent
   ↓           ↓               ↓              ↓           ↓              ↓
  PRD      UI/UX Spec      Code Changes    Test Report  Deploy Config  Security Review
  BRD      Visual System                                  CI/CD
  TRD
```

**Document dependencies**

- Engineer reads `docs/pm/{feature}/` and `docs/design/{feature}/`
- QA reads `docs/pm/{feature}/` and the implementation
- DevOps reads `docs/pm/{feature}/TRD.md`
- Designer reads `docs/pm/{feature}/PRD.md` and `docs/pm/{feature}/BRD.md`
- Security reads `docs/pm/{feature}/` and the codebase

**Role boundaries**

- Designer Agent stops at design deliverables under `docs/design/{feature}/` and must not implement code
- Engineer Agent is the role that turns PM and Designer documents into code, tests, and delivery artifacts
- Reading a PM spec or design spec does not authorize Designer Agent to continue into implementation

## Development Workflow

> [!IMPORTANT]
> Every time `CLAUDE.md` is updated, `AGENTS.md` must be updated as well. Every time `AGENTS.md` is updated, `CLAUDE.md` must be updated as well. The two files must stay identical.

### Adding a New Agent

1. Create the directory structure:
   ```bash
   mkdir -p agents/{agent-name}/{skills,test}
   ```

2. Create `agents/{agent-name}/README.md` following the existing agent pattern

3. For each skill, create:
   - `skills/{skill-name}/SKILL.md`
   - `skills/{skill-name}/_internal/INSTRUCTIONS.md`
   - `test/{skill-name}/evals/evals.json`

4. Register the agent in `.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "{agent-name}-agent",
     "description": "...",
     "skills": ["./agents/{agent-name}/skills/{skill-name}"]
   }
   ```

5. Update `skills-lock.json` with the new skill metadata

6. Add evaluation tests and run comparisons with and without the skill

### Skill Design Principles

- **Document-driven**: skills consume and produce Markdown documents
- **Tech-stack agnostic**: do not assume a specific framework unless the project requires it
- **Minimal and focused**: each skill should have a single clear responsibility
- **Independently triggerable**: skills should work on their own, not only as part of a chain
- **Business-friendly**: prioritize clarity for non-technical users when possible

### Testing Skills

Each skill should include:

- `test/{skill-name}/evals/evals.json` for evaluation case definitions
- `test/{skill-name}/evals/workspace/eval-{id}/` for evaluation workspaces
- comparison results for using the skill vs. not using the skill

Skill evals are availability tests for the agent skill. They must verify that the skill can be triggered, that its protocol is executable, and that it produces the expected structured artifact for the role. Eval assertions should check skill-specific behavior such as context reading, execution-path selection, evidence handling, blocked assumptions, and handoff boundaries instead of only checking generic model answer quality.

**Eval runner constraints**

- Final eval validation must be performed directly by a fresh Codex subagent in the current session. The subagent should read the skill document, relevant agent README, eval fixture workspace, and `evals.json`, then judge whether the skill behavior satisfies the eval assertions.
- Do not treat background CLI transcript generation as the source of truth for eval pass/fail. CLI-generated transcripts may be kept as diagnostic artifacts only, while the final availability judgment must come from subagent validation.
- Baseline outputs remain required. Do not weaken evals by making `without_skill` optional just to hide transcript-generation failures.
- When legacy transcript generation is needed for comparison artifacts, prefer structured output and extract the final result field, rather than relying on plain text stdout.
- Generate transcripts in an isolated temporary workspace, not directly in the committed eval fixture. Historical outputs or generated PM docs can contaminate empty-workspace routing and other context-sensitive cases.
- Use `execution_cleanup` in `eval_metadata.json` for paths that must be removed from the temporary workspace before each run, such as stale `PRD.md`, `docs/pm/`, or prior output folders.
- Persist run diagnostics such as command, cwd, timeout, return code, and stdout length so infra failures can be separated from assertion failures.
- Prefer semantic assertions over brittle exact-string checks when behavior can legitimately vary in language or formatting. For example, treat localized or equivalent PM-first lane labels as acceptable if they preserve the intended routing behavior.

### Documentation Versioning

**Do**

- Use feature-based directories such as `docs/{agent}/{feature-name}/`
- Add frontmatter with version metadata
- Rely on git history for version tracking
- Update `last_updated` when modifying a document

**Do not**

- Create date-based subdirectories
- Create multiple versioned files such as `PRD-v1.md` and `PRD-v2.md`
- Commit working docs from `docs/superpowers/` to git

## Current Status

**Implemented agents (6)**

- `pm-agent` - 7 specialist skills
- `engineer-agent` - 6 specialist skills
- `qa-agent` - 4 specialist skills
- `devops-agent` - 4 specialist skills
- `designer-agent` - 2 specialist skills
- `security-agent` - 4 specialist skills

**Total specialist skills:** 27

**Planned agents**

- `growth_ops` (P1) - analytics, funnel analysis, feedback synthesis
- `orchestrator` (P2) - request routing, project status summarization

See `docs/superpowers/plans/2026-03-27-team-agent-expansion.md` for the expansion roadmap.

## Important Files

- `.claude-plugin/marketplace.json` - agent and skill registry
- `skills-lock.json` - installed skill metadata
- `CLAUDE.md` - repository guidance for Claude Code, must be kept in sync with `AGENTS.md`
- `AGENTS.md` - shared repository guidance, must be kept in sync with `CLAUDE.md`
- `agents/{agent}/README.md` - agent-level documentation
- `docs/superpowers/plans/` - implementation plans, gitignored but important
- `docs/superpowers/specs/` - design specs, gitignored but important
