# Product Manager Internal Routing Map

> Shared routing contract for `idea-to-spec` and the internal instruction
> resources under `agents/product_manager/skills/idea-to-spec/_internal/`.
> Load this file first whenever `idea-to-spec` needs to decide lane selection,
> handoff shape, lifecycle routing, or fallback behavior.

## 1. Public Surface and Internal Layout

- `idea-to-spec` is the only public, triggerable design-entry skill in this
  skill group.
- All other capabilities are internal instruction resources and live under:
  - `agents/product_manager/skills/idea-to-spec/_internal/analysis/`
  - `agents/product_manager/skills/idea-to-spec/_internal/gen/`
  - `agents/product_manager/skills/idea-to-spec/_internal/iteration/`
  - `agents/product_manager/skills/idea-to-spec/_internal/orchestration/`
  - `agents/product_manager/skills/idea-to-spec/_internal/validator/`
- Shared conventions and document schemas live under
  `agents/product_manager/skills/idea-to-spec/_internal/_shared/`.
- Default loading rule: keep only `idea-to-spec` in active context, then load
  exactly one internal `INSTRUCTIONS.md` plus the minimum shared references
  needed for the current step.

## 2. Entry Lane Selection

Pick one execution lane during Phase 0. Treat this as the first routing
decision, before deciding which internal instruction resource to load.

| Situation | Lane | Default next action |
| --- | --- | --- |
| Empty workspace, vague concept, early idea validation, or new-repo product request with unsettled scope | `greenfield-discovery` | Stay in `idea-to-spec` |
| Empty workspace and the user wants durable docs now | `greenfield-bootstrap` | Load `project-init` |
| Existing repo, adding a new feature or module | `existing-project-feature` | Stay in `idea-to-spec` until requirements or architecture stabilize |
| Existing repo, changing approved behavior / scope / rollout | `existing-project-update` | Load `change-impactor`, then route to iteration |
| User explicitly wants the full document chain | `pipeline` | Load `flow` |
| User only wants a document diff or comparison | `diff-only` | Load `version-differ` |

## 3. Conversation Protocol Rules

These rules apply before any internal routing:

- Advance one decision point per turn.
- For meaningful product or technical trade-offs, present `2-3` options with
  explicit trade-offs and recommend one default.
- Use section-based progression and do not move to the next section until the
  current one is confirmed or deliberately deferred.
- Record confirmed decisions, open questions, assumptions, and rejected options
  in `docs/pm/{feature-name}/DECISIONS.md` when the conversation is in
  documenting mode.
- Treat feature docs as durable memory for long-running design threads.
- After a major stage, consolidate process notes into stable declarative prose.

## 4. Progressive Disclosure Rules

- Default to one recommended next skill plus one optional alternative.
- Stay inside `idea-to-spec` while any of these remain unstable:
  - problem statement
  - target users
  - scope and non-goals
  - rollout constraints
  - architecture direction
- For existing-project requests, inspect repo structure and current docs before
  recommending generation or iteration.
- For empty or near-empty workspaces, keep product ideas on the PM path first
  even when the user's verbs sound like "build", "create", or "init".
- For change requests against approved docs, prefer impact analysis and direct
  iteration over regeneration.
- Show the full pipeline only when the user explicitly asks for end-to-end
  coverage or is clearly ready to operationalize multiple formal documents.
- If the user names a downstream capability explicitly, honor the intent but
  still use `idea-to-spec` to frame unresolved assumptions and assemble the
  handoff packet.

## 5. Internal Instruction Resource Registry

Use the narrowest internal instruction resource that matches the lane and
document state.

| Capability | Skill | Internal path | Use when |
| --- | --- | --- | --- |
| Change impact analysis | `change-impactor` | `agents/product_manager/skills/idea-to-spec/_internal/analysis/change-impactor/INSTRUCTIONS.md` | A change request may affect one or more existing docs |
| Traceability review | `trace-check` | `agents/product_manager/skills/idea-to-spec/_internal/analysis/trace-check/INSTRUCTIONS.md` | Need coverage or mapping review after generation / iteration |
| Version diff | `version-differ` | `agents/product_manager/skills/idea-to-spec/_internal/analysis/version-differ/INSTRUCTIONS.md` | Need comparison only, not editing |
| BRD generation | `brd-gen` | `agents/product_manager/skills/idea-to-spec/_internal/gen/brd-gen/INSTRUCTIONS.md` | Business case or stakeholder alignment is stable |
| PRD generation | `prd-gen` | `agents/product_manager/skills/idea-to-spec/_internal/gen/prd-gen/INSTRUCTIONS.md` | Requirements and flows are stable |
| TRD generation | `trd-gen` | `agents/product_manager/skills/idea-to-spec/_internal/gen/trd-gen/INSTRUCTIONS.md` | Technical approach is stable |
| ADR generation | `adr-gen` | `agents/product_manager/skills/idea-to-spec/_internal/gen/adr-gen/INSTRUCTIONS.md` | A decision needs durable rationale |
| API generation | `api-gen` | `agents/product_manager/skills/idea-to-spec/_internal/gen/api-gen/INSTRUCTIONS.md` | Interface contracts are stable |
| Test spec generation | `tspecs-gen` | `agents/product_manager/skills/idea-to-spec/_internal/gen/tspecs-gen/INSTRUCTIONS.md` | QA assets should be derived from approved requirements or design |
| Workflow execution | `flow` | `agents/product_manager/skills/idea-to-spec/_internal/orchestration/flow/INSTRUCTIONS.md` | User wants an end-to-end pipeline |
| Project bootstrap | `project-init` | `agents/product_manager/skills/idea-to-spec/_internal/orchestration/project-init/INSTRUCTIONS.md` | Empty workspace needs durable doc scaffolding |
| Multi-doc update | `iteration-coordinator` | `agents/product_manager/skills/idea-to-spec/_internal/orchestration/iteration-coordinator/INSTRUCTIONS.md` | Multiple docs must change together |
| Direct doc update | Matching `*-iteration` | `agents/product_manager/skills/idea-to-spec/_internal/iteration/.../INSTRUCTIONS.md` | One approved doc needs revision |
| Quality review | Matching `*-validator` | `agents/product_manager/skills/idea-to-spec/_internal/validator/.../INSTRUCTIONS.md` | A generated or updated doc needs a score / gap report |

## 6. Handoff Packet Contract

When `idea-to-spec` hands work to any internal instruction resource, pass a
compact packet that preserves settled context and avoids re-asking basics.

- `project_context`: repo path, workspace status, tech stack, key modules
- `docs_context`: doc inventory, maturity, missing artifacts, active feature doc
  paths
- `request_lane`: one of the lane values above
- `problem_and_goal`: problem, target users, success metrics
- `scope`: MVP, non-goals, priorities, rollout constraints
- `current_state`: integrations, permissions, data flows, dependencies
- `change_request`: delta summary for existing-project updates
- `decisions_locked`: agreed decisions that should not be reopened lightly
- `decision_log_path`: path to `docs/pm/{feature-name}/DECISIONS.md` when it
  exists
- `drafted_sections`: sections already produced in this session or in the
  working docs
- `assumptions_and_open_questions`: unresolved items that need confirmation
- `recommended_next_skill`: selected internal capability and reason

Example packet:

```yaml
project_context:
  path: /repo
  status: existing-project
  tech_stack: [nextjs, postgres]
  key_modules: [comments-service, auth-service, notification-center]
docs_context:
  inventory:
    - docs/pm/notifications/PRD.md
    - docs/engineer/notifications/TRD.md
  maturity: approved-core-docs
  missing_artifacts: [docs/pm/notifications/DECISIONS.md]
  active_feature_docs:
    - docs/pm/notifications/PRD.md
request_lane: existing-project-feature
problem_and_goal:
  problem: Users miss comment mentions.
  target_users: [workspace members]
  success_metrics: ["notification read rate > 70%"]
scope:
  mvp: [in-app notifications, unread badge]
  non_goals: [email digests]
current_state:
  integrations: [comments service, auth service]
  permissions: [workspace member, admin]
change_request:
  summary: Add in-app notifications for mentions and assignments.
decisions_locked:
  - Start with polling, not websockets
decision_log_path: docs/pm/notifications/DECISIONS.md
drafted_sections:
  - current state
  - user flows
  - acceptance criteria
assumptions_and_open_questions:
  - Notification retention window still unconfirmed
recommended_next_skill:
  name: prd-gen
  reason: Requirements are stable and ready for formalization
```

## 7. Phase and Situation Routing

| Phase / Situation | Primary internal skill | Alternative / follow-up |
| --- | --- | --- |
| Empty workspace, durable docs needed | `project-init` | Stay in `idea-to-spec` for lightweight validation only |
| Business case, ROI, or stakeholder alignment needed | `brd-gen` | Stay in `idea-to-spec` for a brief validation memo |
| Existing repo, new feature requirements stable | `prd-gen` | `prd-validator` after generation |
| Existing repo, technical design stable | `trd-gen` | `adr-gen`, `api-gen`, then matching validators |
| Existing repo, one approved doc needs revision | Matching `*-iteration` | Matching validator |
| Existing repo, multiple docs need coordinated revision | `change-impactor` -> `iteration-coordinator` | `trace-check` and `version-differ` after updates |
| QA assets or regression mapping needed | `tspecs-gen` | `tspecs-validator` or `trace-check` |
| Full end-to-end pipeline requested | `flow` | Narrower gen / validator steps if the user backs off |
| Diff only | `version-differ` | `trace-check` if the issue is coverage rather than versioning |

## 8. Existing-Project Update Rules

- Run `change-impactor` first when the user asks to update an existing feature,
  requirement, rollout policy, or integration and the blast radius is unclear.
- If exactly one core doc is affected, use the matching `*-iteration` skill
  directly instead of `iteration-coordinator`.
- If multiple docs are affected, use this order by default:
  - BRD -> PRD -> TRD -> API -> TEST_SPEC
  - ADRs run in parallel when a decision record is affected
- After multi-doc updates, prefer `trace-check` before closing the loop.
- Regenerate from scratch only when:
  - the target artifact is missing
  - the current artifact is too incomplete to safely iterate
  - the user explicitly prefers regeneration

## 9. Lifecycle Coverage Matrix

| Document Type | Generator | Validator | Iteration |
| --- | --- | --- | --- |
| BRD | `brd-gen` | `brd-validator` | `brd-iteration` |
| PRD | `prd-gen` | `prd-validator` | `prd-iteration` |
| TRD | `trd-gen` | `trd-validator` | `trd-iteration` |
| API | `api-gen` | `api-validator` | `api-iteration` |
| ADR | `adr-gen` | `adr-validator` | `adr-iteration` |
| TEST_SPEC | `tspecs-gen` | `tspecs-validator` | `tspecs-iteration` |

## 10. Shared References

- Schema source root:
  `agents/product_manager/skills/idea-to-spec/_internal/_shared/doc-schemas/`
- Generator conventions:
  `agents/product_manager/skills/idea-to-spec/_internal/_shared/gen-conventions.md`
- Validator conventions:
  `agents/product_manager/skills/idea-to-spec/_internal/_shared/validator-conventions.md`
- Quality scoring:
  `agents/product_manager/skills/idea-to-spec/_internal/_shared/quality-rules.md`
- Versioning and output rules:
  `agents/product_manager/skills/idea-to-spec/_internal/_shared/output-conventions.md`
