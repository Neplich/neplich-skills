---
name: regression-suite
description: "Verify fixes with evidence reuse, adjacent-risk review, and clear pass/fail/blocked reporting for QA handoff."
---

# Regression Suite

Verify that a fix actually resolves the original failure and that nearby surfaces still behave correctly. This skill is about fix verification plus adjacent risk review, not replaying one bug in isolation.

## Shared QA Directory Contract

For feature-scoped regression work, prefer `docs/qa/<feature-name>/` as durable
QA memory:

- `TEST_SPEC.md` is the suite index and traceability summary.
- `test-cases/` stores reusable cases; every E2E case must be one Markdown file
  named `TC-NNN-<short-slug>.md`.
- `FILE_EXPLORATION.md` records file exploration used to derive or expand
  regression scope.
- `reports/` stores regression verification reports when no stronger repo
  convention exists.

Use these files to avoid rediscovering the full project on every regression
run.

## When to Use

- After a fix, patch, or hotfix is available for QA verification
- When a user asks to verify a defect closure or release readiness
- When a previous bug report needs to be rechecked against new code or a new build

## Core Principle

Reuse the original evidence instead of re-deriving the scope from scratch. The regression run should confirm the fix, test the nearby surfaces that could break, and report whether the scope is ready to release.

## Step 1 — Regression preflight

Read the evidence before executing anything:

- Existing QA test cases and prior file exploration:
  `docs/qa/<feature-name>/test-cases/*.md` and
  `docs/qa/<feature-name>/FILE_EXPLORATION.md`, when available
- Original bug report or failing test evidence
- Fix context such as changed files, PR notes, implementation notes, or release notes
- Related areas likely to regress because they share code, state, data, UI flow, API surface, permissions, or configuration

If the original evidence is missing or too thin, mark the run as `blocked` until the missing material is available.

If the user asks for standalone E2E regression and no PM-authored test cases are
available, first read `docs/qa/<feature-name>/test-cases/`. Then ask whether
there are new feature updates and whether QA should explore project files to
expand regression cases. If exploration is requested, update
`FILE_EXPLORATION.md` and create or update one E2E case file per reusable
scenario before execution.

## Step 2 — Define the verification scope

The regression scope must cover three questions:

- Does the original failure still reproduce?
- Does the expected fixed behavior now work?
- Do adjacent surfaces impacted by the fix still behave correctly?

Use the original evidence to keep the scope tight, but expand to nearby risk areas when the fix touches shared logic, state transitions, or user-visible flow.

## Step 3 — Prepare the environment

Use the repo's documented runtime and test instructions. Do not assume a fixed local port, fixed host, or a single app layout.

If the environment is not ready:

- Mark the verification as `blocked`
- Record what is missing
- Avoid fabricating a pass from incomplete setup

## Step 4 — Execute regression checks

Run checks that map to the scope:

- Reproduce the original failure path against the fixed build
- Verify the expected behavior now succeeds
- Exercise adjacent or nearby surfaces that could regress
- Execute existing or newly expanded E2E case files from
  `docs/qa/<feature-name>/test-cases/` when they map to the fix scope

Capture evidence from runtime output, screenshots, traces, logs, or test output as needed. Keep run status separate from evidence strength: `pass`, `fail`, and `blocked` are the regression run outcomes, while evidence confidence is a secondary note about how strong and complete the supporting proof is.

## Step 5 — Judge adjacent risk

For each nearby surface, answer whether it is still healthy. Include both direct and indirect risks, such as:

- Shared components or helpers
- Nearby flows that use the same data shape
- Permission or state-dependent branches
- Error handling and recovery paths
- Release-sensitive areas touched by the fix

## Step 6 — Produce the regression artifact

The regression artifact must include:

- Fix verification status: `pass`, `fail`, or `blocked`
- Original failure recheck result
- Expected fixed behavior result
- Adjacent regression checks
- New issues discovered, if any
- Release recommendation for this scope

The report should make it obvious whether the fix is safe to release, needs more work, or cannot yet be judged.

Suggested content structure:

```markdown
# Regression Verification: [short title]

## Scope
- Original defect:
- Fix context:
- Related risk areas:

## Fix Verification
- Status: pass / fail / blocked
- Original failure:
- Fixed behavior:
- Evidence confidence: [high / medium / low] with a short explanation

## Adjacent Regression Checks
- [surface] - pass / fail / blocked - note
- [surface] - pass / fail / blocked - note

## New Issues
- [issue or none]

## Release Recommendation
- [safe to release / hold release / needs more verification]
```

## Step 7 — Handle failures and gaps

If the original failure still reproduces, report `fail` and name the evidence. If the environment prevents a clean judgment, report `blocked`. If the fix works but evidence is thin, keep the report honest and call out what remains uncertain.

## Step 8 — Choose the output path

Use a durable output path that matches repo context.

- Use a local Markdown artifact when the repo tracks QA verification in files or when the user asked for a document
- Prefer `docs/qa/<feature-name>/reports/YYYY-MM-DD-regression-verification.md`
  when a feature QA directory is known
- Use a GitHub issue only when the repo workflow or user request explicitly wants issue tracking

Do not commit changes, do not mutate code, and do not assume a GitHub-first workflow.

## Configuration

- Evidence reuse is required
- Adjacent-risk review is required
- No hardcoded runtime host or port
- No self-mutating behavior
- Run status and evidence confidence must stay explicit and separate
- Run status is `pass`, `fail`, or `blocked`; confidence is separate

## Edge Cases

- **Original bug report missing**: `blocked` until evidence is provided
- **Fix not deployed to the verification environment**: `blocked`
- **Fix verified but a nearby surface fails**: `fail` with the adjacent regression called out
- **Original failure cannot be reproduced on baseline**: treat as an evidence problem and note the uncertainty, not as a false pass
