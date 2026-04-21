---
name: exploratory-tester
description: "Discovery-driven exploratory QA that uses an exploration charter to examine changed product surfaces, environmental risks, and nearby failure modes with flexible tooling."
---

# Exploratory Tester

Use this skill to discover defects through guided exploration, not to generate random UI actions. The exploration strategy is chosen only after reading the product context, implementation changes, and environment instructions. The output is an exploratory QA report plus, when warranted, a defect-ready escalation path.

## Shared QA Directory Contract

For feature-scoped QA, use `docs/qa/<feature-name>/` as durable QA memory:

- `TEST_SPEC.md` is the suite index and coverage summary.
- `test-cases/` stores reusable test cases.
- Every E2E test case produced or expanded by exploration must be written as
  one Markdown file: `test-cases/TC-NNN-<short-slug>.md`.
- `FILE_EXPLORATION.md` records source files, config files, routes, test
  harnesses, fixtures, and environment notes inspected to derive coverage.
- `reports/` stores exploratory reports when no stronger repo convention
  exists.

Exploration should supplement this directory instead of re-reading the entire
project on every standalone QA run.

## When to Use

- After implementation changes when you need discovery beyond scripted coverage
- When the team wants exploratory QA against a changed surface or risky workflow
- When prior QA reports, known bugs, or environment notes suggest adjacent risk
- When the user asks for exploratory testing, discovery testing, or broad defect hunting

## Role Boundary

- This skill performs exploratory discovery, not spec validation
- This skill does not write bug tickets itself
- This skill does not dump generic browser-script output without interpretation

## Exploration Preflight

Before any testing action, gather the context needed to choose an exploration charter:

1. Read existing QA memory first when available:
   `docs/qa/<feature-name>/TEST_SPEC.md`,
   `docs/qa/<feature-name>/test-cases/*.md`,
   `docs/qa/<feature-name>/FILE_EXPLORATION.md`, and relevant reports.
2. Read the PM or release context for the feature, scope, and intended user
   value.
3. Read implementation notes, changed files, or the equivalent change summary
   to identify the exact surface that moved.
4. Read known bugs, risk notes, and prior QA reports so exploration can target
   realistic failure modes.
5. Read environment instructions that affect how the app should be exercised,
   including setup, auth, feature flags, test accounts, or required services.

If any of the above is missing, note the gap and make the smallest safe assumption needed to continue.

For standalone exploratory or E2E requests with no PM-authored test cases, ask
the user whether there are new feature updates and whether project-file
exploration should be used to expand test cases. If they decline exploration,
use existing QA memory and execute only the scoped charter.

## Exploration Charter

Define a short charter before interacting with the app. The charter must include:

- Surface to explore: the specific screen, flow, API-backed interaction, or change area
- Timebox: chosen from the context, not a fixed skill default
- Heuristics: what kinds of failures matter most for this pass
- Escalation signals: what observations are strong enough to become a bug report candidate

Charter heuristics should be specific to the change and typically include:

- Changed-path smoke coverage
- Navigation and routing edges
- Validation and form-handling edges
- Empty states and data absence
- Permissions and access boundaries
- Interruptions, retries, cancellations, refreshes, and partial completion
- Nearby risk surfaces that are plausibly coupled to the changed area

## Exploration Strategy

Choose the exploration path after preflight and chartering, in this order:

1. Smoke the changed surface end to end to confirm the basic path still works.
2. Probe edge cases around navigation, validation, empty states, permissions, and interruptions.
3. Expand into nearby risk areas only if the first two steps reveal coupling, instability, or suspicious signals.

Randomized action generation is optional and should only be used as a supplement when it helps coverage. It is not the default contract and should never replace chartered exploration.

## Execution Methods

Use whichever tools best fit the charter and environment:

- Browser automation for repeatable UI traversal
- Manual walkthroughs when judgment, visual inspection, or auth handling matters
- Console and network inspection when client or backend signals need confirmation
- Existing QA scripts when they already target the relevant path
- Targeted randomized inputs or action variations only when they support a specific heuristic

Prefer the least brittle method that still produces clear evidence.

## Exploration Procedure

1. Record the charter and the context used to derive it.
2. Execute the smoke path over the changed surface.
3. Probe the prioritized edge cases from the charter.
4. Branch into nearby risk exploration only when the observed behavior justifies it.
5. If exploration reads source or config files to derive coverage, write or
   update `docs/qa/<feature-name>/FILE_EXPLORATION.md` with the files read,
   why they were read, and coverage implications.
6. If exploration identifies reusable E2E scenarios, write or update one case
   file per scenario under `docs/qa/<feature-name>/test-cases/`.
7. Track what was covered, what was intentionally skipped, and what still needs
   follow-up.

During exploration, capture:

- Exact steps or script paths used
- Visible UI behavior
- Console errors and warnings relevant to the issue
- Network failures, abnormal responses, or suspicious timing
- Reproduction consistency
- Any conditions that make the result ambiguous or environment-dependent

## Bug Escalation Rules

Escalate to bug-analyzer only when the exploration finds a reproducible failure with enough evidence for a defect report.

Escalation-quality evidence usually includes:

- Clear reproduction steps
- The affected surface and scenario
- Observable wrong behavior
- Supporting console, network, or log evidence when available
- Notes on frequency and any environment dependencies

Keep unconfirmed anomalies in the exploratory report. Do not promote them as defects unless reproduction or evidence quality crosses the threshold above.

## Evidence Output

Write the exploratory report to
`docs/qa/<feature-name>/reports/YYYY-MM-DD-exploratory-report.md` when the
feature QA directory is known. Otherwise use the fallback path
`docs/qa-reports/YYYY-MM-DD-<feature>-exploratory-report.md`.

The report must be concise, handoff-ready, and clearly separate these sections:

- Observed issues: confirmed failures and reproducible defects
- Suspicious but unconfirmed signals: anomalies worth watching, but not yet defect-ready
- Exploration path covered: what was actually tested
- Gaps not explored: what remains untested and why
- Recommended next actions: follow-up QA, engineering checks, or escalation candidates

The report should also record the charter, timebox, and the evidence used to reach conclusions.

When new E2E case files are created or changed, list those paths in the report
so a later spec-based run can execute from them without repeating the same file
exploration.

## Out of Scope

- Random UI clicking without a charter
- Pure spec conformance checking
- Writing bug tickets as the primary artifact
- Hardcoded environment assumptions such as a fixed local URL
- Self-mutating workflow instructions such as committing results from the skill contract
