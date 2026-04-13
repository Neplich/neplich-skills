---
name: idea-to-spec
description: "Use this when the user wants to turn a product idea, an empty-workspace app request, an existing-project feature request, or a spec change into structured PM or technical design output before implementation."
---

# Idea to Spec

Use this as the single public entry skill for the `idea-to-spec` skill group.

It owns:

- workspace and document context detection
- request lane selection
- design conversation control
- section-by-section requirement shaping
- handoff packet assembly
- progressive loading of internal instruction resources under
  `agents/product_manager/skills/idea-to-spec/_internal/`

Do not expose or recommend the full internal instruction tree up front. Keep
the user interacting with `idea-to-spec` until the narrowest useful next step
is clear.

## Non-Negotiable Protocol

For feature design and spec-change requests, follow these rules:

1. Read workspace and document context before proposing a formal design.
2. Advance one decision point per turn. Do not push multiple unresolved topics
   in parallel.
3. For meaningful design trade-offs, present `2-3` viable options, state the
   trade-off for each, and recommend one default.
4. Use section-based progression. Finish the current section before moving to
   the next one.
5. After the user confirms a decision, record it in the feature decision log.
6. After a section is stable, write or update the corresponding PM document
   instead of relying only on chat history.
7. After each major stage, consolidate the written docs into clean,
   declarative language. Do not leave "not X but Y" correction prose in the
   body text.
8. Do not recommend downstream generation until scope, users, constraints, and
   current-state understanding are either confirmed or explicitly captured as
   assumptions.
9. Do not regenerate existing documents by habit. Prefer delta-oriented
   iteration.
10. In empty or near-empty workspaces, do not jump to engineering bootstrap,
    framework selection, or scaffolding unless the user explicitly says to skip
    PM and start coding now.

## Operating Modes

Choose the conversation style first:

- **Explore mode** (default): Dialogue-driven, best for vague requests or
  unstable scope.
- **Fast mode**: Use when the user already gave goals, users, scope,
  constraints, and likely implementation boundaries.

If the user already supplied enough detail, switch to fast mode automatically.
Fast mode does not skip the non-negotiable protocol; it only compresses the
number of turns.

## Execution Lanes

Choose one lane during Phase 0. Lanes decide orchestration; modes decide how
you converse.

1. **Greenfield discovery**
   - Empty workspace, vague idea, or early concept validation
   - Stay in `idea-to-spec` until the request becomes spec-ready
2. **Greenfield bootstrap**
   - Empty workspace and the user wants durable docs now
   - Load `project-init`
3. **Existing-project feature**
   - Existing repo, adding a new feature, module, or integration
   - Anchor the work in current architecture, modules, permissions, and docs
4. **Existing-project update**
   - Existing repo, approved behavior or docs already exist, and the user wants
     to change them
   - Prefer impact analysis and targeted iteration over regeneration
5. **Pipeline**
   - User explicitly wants an end-to-end document workflow
   - Load `flow`
6. **Diff-only**
   - User only needs revision comparison
   - Load `version-differ`

## When to Use

- The user has an idea and wants a concrete plan or spec
- The workspace is empty or near-empty and the user is describing what the
  product should do before any stack has been settled
- The user needs a PRD, design doc, tech spec, or delivery plan
- The user wants to add a feature to an existing codebase and needs the plan
  anchored in current repo reality
- The user wants to update an existing feature and needs to know which docs or
  decisions must change
- The user wants the next best idea-to-spec step without manually choosing from
  generators, validators, or iteration skills

Do not use this for:

- pure code review or debugging
- implementation-only requests where the spec is already settled
- stack-only bootstrap requests where the user explicitly wants to skip PM
  discovery and scaffold code now
- trivial bug fixes that do not require product or architecture framing

## Internal Routing Contract

Before loading any internal instruction resource or building a handoff packet,
read:

`agents/product_manager/skills/idea-to-spec/_internal/_shared/skill-map.md`

Treat that file as the source of truth for:

- lane selection
- progressive disclosure
- handoff packet fields
- generator / validator / iteration routing
- documentation memory rules
- existing-project update policy
- fallback behavior

Load only the narrowest internal `INSTRUCTIONS.md` needed for the next step.

## Core Principles

- **Entry first**: `idea-to-spec` is the front door for design work, not just a
  greenfield brainstormer.
- **Context before output**: Read repo and doc context before proposing formal
  artifacts.
- **Protocol before prose**: Manage design conversations through explicit
  decision points, not open-ended brainstorming.
- **Delta-oriented on existing projects**: Describe what changes relative to the
  current system, not just the target end state.
- **Progressive disclosure**: Offer one recommended next step plus one optional
  alternative by default.
- **PM before bootstrap**: Empty-workspace product requests stay in PM lanes
  first, even if the user's wording sounds implementation-oriented.
- **Reuse settled context**: Downstream internal instruction resources should
  inherit confirmed facts instead of re-asking the basics.
- **Document as memory**: Use feature docs as durable working memory for large
  designs.
- **Do not regenerate by habit**: Prefer targeted iteration when the artifact
  already exists and is good enough to update in place.
- **Never fabricate**: Mark uncertain business rules, metrics, or technical
  constraints as `Assumption - needs confirmation`.

## Feature Document Memory

For ongoing feature design, use the short-path document layout:

- `docs/pm/{feature-name}/DECISIONS.md`
- `docs/pm/{feature-name}/PRD.md`
- `docs/pm/{feature-name}/BRD.md`
- `docs/pm/{feature-name}/design.md` as a temporary PM working draft when the
  design has not yet split into formal docs

Treat `DECISIONS.md` as the source of truth for:

- confirmed decisions
- open questions
- assumptions
- rejected options

When the design spans many turns, re-read the feature docs before continuing.

## Phase 0: Workspace and Doc Detection

Always run this before the main conversation.

### Inspect the workspace

Check for:

- repo markers: `.git`, `README`, `docs/`
- stack markers: `package.json`, `pnpm-lock.yaml`, `go.mod`, `Cargo.toml`,
  `pyproject.toml`, `pom.xml`
- architecture markers: `src/`, `apps/`, `packages/`, `services/`, `infra/`
- documentation markers: BRD / PRD / TRD / ADR / API / TEST_SPEC /
  DECISIONS files, validation reports, doc indexes

### Classify the current state

Determine:

- workspace status: `empty`, `prototype`, `existing-project`
- doc maturity:
  - `no-docs`
  - `draft-docs`
  - `approved-core-docs`
  - `partial-doc-set`
- request shape:
  - idea validation
  - new feature on existing project
  - change to existing feature or decision
  - full workflow request
  - diff-only request

### Output a compact context summary

Use this structure:

```text
Project context:
- Directory: [path]
- Status: [empty / prototype / existing project]
- Tech stack: [detected or TBD]
- Existing docs: [none / partial / approved core docs]
- Suggested lane: [greenfield-discovery / greenfield-bootstrap / existing-project-feature / existing-project-update / pipeline / diff-only]
- Likely next step: [stay in idea-to-spec / project-init / prd-gen / change-impactor / flow / ...]
```

## Phase 0.5: Lane Selection Rules

Apply these rules immediately after the context summary:

- If the workspace is empty and the user wants persistent docs, choose
  `greenfield-bootstrap` and load `project-init`.
- If the workspace is empty and the user only wants concept validation, stay in
  `greenfield-discovery`.
- If the workspace is empty or near-empty and the user is describing product
  behavior, layout, roles, or scope, keep the work in `greenfield-discovery` or
  `greenfield-bootstrap`. Do not suggest engineering bootstrap from Phase 0.
- If an existing repo is present and the user is adding a feature or module,
  choose `existing-project-feature`.
- If the repo and formal docs already exist and the user is changing approved
  behavior, constraints, or rollout, choose `existing-project-update`.
- If the user explicitly wants the whole document pipeline, choose `pipeline`.
- If the user only wants a comparison between two revisions, choose `diff-only`.

When uncertain between `existing-project-feature` and `existing-project-update`,
ask one clarifying question:

- "Are we defining a net-new capability, or revising behavior that is already
  covered by current docs or implementation?"

## Existing-Project Playbooks

This skill must handle existing projects explicitly. Use the following playbook
instead of treating every request as a blank-sheet idea.

### Lane: `existing-project-feature`

Use when the codebase exists but the requested capability is new.

1. Identify the current system boundary:
   - touched modules
   - existing user roles and permissions
   - current APIs and events
   - data ownership and storage
   - rollout constraints, backwards compatibility, and observability
2. Produce a **delta brief** before formal docs:
   - current state
   - target change
   - impacted modules and integrations
   - constraints inherited from the current system
   - open risks and dependencies
3. Continue through the normal clarify / shape / architect phases, but always
   anchor requirements and design to the detected current state.
4. Once requirements are stable, hand off to the narrowest generator:
   - `prd-gen` for requirements formalization
   - `trd-gen` for technical design
   - `api-gen` or `adr-gen` only when those artifacts are already clearly
     justified

### Lane: `existing-project-update`

Use when the request changes something that already exists in docs or
implementation.

1. Summarize the requested delta:
   - what changes
   - why it changes now
   - which current behaviors, contracts, or rollout plans are affected
2. If the blast radius is unclear, load `change-impactor`.
3. Route based on impact:
   - one primary doc affected -> matching `*-iteration`
   - multiple primary docs affected -> `iteration-coordinator`
   - comparison only -> `version-differ`
4. After updates, recommend the matching validator, and prefer `trace-check`
   after multi-doc changes.
5. Do not default to full regeneration unless the current artifact is missing,
   unusable, or the user explicitly asks for regeneration.

## Phase 1: Clarify the What and Why

Goal: determine what to build or change, why it matters now, and where the
scope should stop.

In **explore mode**, advance one decision point at a time.

Always resolve:

- problem statement
- target users or operators
- success metrics
- MVP scope and non-goals
- hard constraints: timeline, team, compliance, platform

For existing projects, also resolve:

- current state and integration points
- affected modules, APIs, or permissions
- what must stay backward-compatible
- whether the request adds capability or revises existing behavior

In **fast mode**, extract these items directly and fill sensible defaults for
missing details, but still mark assumptions explicitly.

### Phase 1 Output

Confirm at least:

```text
Here's my understanding:

- Problem: [one sentence]
- Target users: [who, when, where]
- Goal: [success metrics]
- Scope: [MVP must-haves vs nice-to-haves]
- Non-goals: [explicitly excluded]
- Constraints: [timeline, tech, compliance, team]
- Current state: [existing modules / flows / permissions / docs]
- Change type: [new capability / behavior update / policy update / doc gap]
- Top risks: [top 3]
```

Then ask for confirmation or correction. Once confirmed, update the feature
decision log.

## Phase 2: Validate the Bet (Optional)

Run this only when the user wants to validate whether something is worth
building or shipping.

Output:

| Assumption | Why risky | Validation method | Success bar | Owner | Due |
| --- | --- | --- | --- | --- | --- |

If the user has already committed to implementation, skip this phase.

## Phase 3: Shape the Product Requirements

Goal: make requirements testable and scoped.

Use section-based progression. For PM design work, the default section order is:

1. Scope and goals
2. Core objects and data model
3. Interfaces and query/write semantics
4. Frontend interaction shape
5. Error and edge-case handling
6. Phasing and test coverage

For each section:

- resolve one decision point at a time
- present options when the section contains a real trade-off
- wait for confirmation before moving on
- update the feature docs once the section is stable

Use a requirements table when requirements stabilize:

| ID | User Story | Requirement | Acceptance Criteria | Priority | Notes |
| --- | --- | --- | --- | --- | --- |

Every P0 item must have testable acceptance criteria.

For existing projects, explicitly capture:

- impacted existing flows
- compatibility and migration constraints
- feature flags or phased rollout assumptions

## Phase 4: Shape the Technical Design

Goal: surface trade-offs and make implementation planning real.

For major technical decisions, present `2-3` viable options with trade-offs and
recommend one default.

Recommended order:

1. architecture options and recommendation
2. data model and state ownership
3. API, event, or interface contracts
4. non-functional requirements
5. error handling, migration, rollout, and rollback

For existing projects, always anchor the design in:

- current modules and extension points
- data model reuse vs schema change
- auth and permission boundaries
- operational impact on current monitoring or alerting

## Phase 5: Delivery and Update Planning

When the user needs execution planning, produce:

- milestones
- work breakdown
- test plan
- release, canary, and rollback plan

For existing-project updates, also include:

- migration steps if needed
- compatibility strategy
- rollback trigger conditions
- post-release verification against current production behavior

## Deliverable Shapes

Default to feature-scoped docs under `docs/pm/{feature-name}/`.

- `DECISIONS.md` for the decision ledger
- `PRD.md` for product requirements
- `BRD.md` for business framing when needed
- `design.md` for an intermediate PM draft before the final split

Downstream docs should use the short-path agent structure:

- `docs/design/{feature-name}/...`
- `docs/engineer/{feature-name}/...`
- `docs/qa/{feature-name}/...`
- `docs/devops/{feature-name}/...`
- `docs/security/{feature-name}/...`

## Handoff Behavior

After each phase or whenever the request becomes stable enough, recommend the
next best step using the shared skill map.

Default output:

```text
## Recommended Next Step

- Best next skill: <skill-name>
- Why this is next: <one sentence>
- Input to pass forward: <sections or handoff packet>
- Output you will get: <document or report>

Optional alternative:
- <skill-name> - <when to choose this instead>
```

Rules:

- Always recommend a next step, even if the user did not ask.
- Prefer the narrowest useful internal skill.
- Recommend a direct `*-iteration` skill before `flow` for existing-doc updates.
- Recommend `flow` only when the user explicitly wants end-to-end execution.

## Quality Checklist

Before delivery, validate against:

- `agents/product_manager/skills/idea-to-spec/_internal/_shared/quality-rules.md`

Additionally confirm:

1. Every P0 requirement is testable.
2. Critical flows include empty, failure, and permission states.
3. Contracts specify auth, idempotency, errors, and retry strategy where
   relevant.
4. NFRs contain concrete numbers, assumptions, or a validation plan.
5. Existing-project changes describe compatibility, migration, and rollback.
6. All assumptions and unknowns are captured explicitly.
7. Confirmed decisions are reflected in `DECISIONS.md`.
8. Section docs have been consolidated into stable prose, not chat-like
   corrections.

## Failure Handling

- **Insufficient information**: propose a default, mark it as an assumption,
  and ask for confirmation.
- **Unclear existing-project lane**: ask whether the request is net-new
  capability or a change to existing behavior.
- **Too many possible downstream skills**: stay in `idea-to-spec` and narrow
  the request before loading anything else.
- **Conflicting requirements**: state the conflict plainly, explain trade-offs,
  and ask the user to choose.
- **Artifact already exists but is low quality**: prefer targeted iteration;
  regenerate only if in-place revision would be misleading or unsafe.

## Safety Boundaries

- Only perform local, read-only inspection during Phase 0 unless the user
  explicitly asks for file output or the conversation is already in document
  authoring mode.
- Do not access external URLs or APIs.
- Do not fabricate business constraints or technical facts.
- Do not silently reopen confirmed decisions.

## Examples

### Example 1: Greenfield idea

**User**: "I have an idea for a notification system."

**Skill**:

- detects repo and doc context
- stays in `greenfield-discovery`
- shapes the idea through controlled decision points
- recommends `prd-gen` once requirements stabilize

### Example 2: Existing project, new feature

**User**: "Add in-app notifications to this existing Next.js app. Reuse the
current comments module if possible."

**Skill**:

- detects an existing repo and current modules
- chooses `existing-project-feature`
- writes a delta brief anchored in current architecture
- progresses section by section and records confirmed decisions
- recommends `prd-gen`, then `trd-gen`

### Example 3: Existing docs need revision

**User**: "We are changing auth from session-based to JWT. Update the current
docs and tell me what changes."

**Skill**:

- chooses `existing-project-update`
- loads `change-impactor`
- routes to `iteration-coordinator` if several docs are affected
- records updated decisions and consolidates the revised docs
- recommends validators and `trace-check` after the updates
