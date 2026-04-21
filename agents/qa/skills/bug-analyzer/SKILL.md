---
name: bug-analyzer
description: "Analyze failing scenarios with an evidence-first intake, classify defect confidence, and produce a durable bug artifact for QA handoff."
---

# Bug Analyzer

Turn a failing scenario into a defect artifact only when the evidence crosses a useful threshold. This skill is about judging defect quality, not filling a template.

## Shared QA Directory Contract

For feature-scoped QA artifacts, prefer `docs/qa/<feature-name>/` when it
exists:

- `test-cases/` stores reusable cases; every E2E case must be one Markdown file
  named `TC-NNN-<short-slug>.md`.
- `FILE_EXPLORATION.md` records file exploration used to derive or expand
  reusable coverage.
- `reports/` stores bug analysis artifacts when no stronger repo convention
  exists.

Bug analysis does not create broad test plans, but when a confirmed E2E
reproduction should become reusable regression coverage, write or update one
case file under `docs/qa/<feature-name>/test-cases/` and reference it from the
defect artifact.

## When to Use

- A test, manual check, or exploratory pass fails and needs triage
- A user reports broken behavior and the report needs validation
- QA needs a defect record that can survive handoff to engineering or release review

## Core Principle

Do not treat every failure as a confirmed bug. First collect evidence, then classify the report, then choose the output path that fits the repo context.

## Step 1 — Intake evidence

Collect the minimum evidence needed to judge the report:

- Failing scenario or symptom
- Source evidence from QA notes, user report, logs, screenshots, traces, console output, network output, or test output
- Environment and build context such as branch, commit, build number, release channel, feature flag state, browser or device, and runtime version

If evidence is missing, ask for it or record the gap explicitly. Do not guess.

## Step 2 — Classify the report

Classify the intake using evidence-confidence vocabulary:

- `confirmed and reproducible` - the failure is observed more than once or is deterministically replayable
- `confirmed but environment-sensitive` - the defect is real, but depends on environment, build, data, timing, permissions, feature flags, or state
- `suspected / needs more evidence` - the report is plausible but not yet strong enough to confirm

Keep the axes separate: evidence status describes reproducibility or sensitivity, while confidence describes how complete and strong the supporting proof is. A report can be `confirmed and reproducible` with medium confidence if the evidence is partial, or `suspected / needs more evidence` with low confidence if the proof is thin; do not collapse the two into one label.

Use the classification to decide whether the artifact should read like a defect report, a scoped investigation note, or an evidence request.

## Step 3 — Assess severity and confidence

Separate impact from certainty.

- Severity describes user or system impact
- Confidence describes how strongly the evidence supports the defect claim

Severity should include a rationale, not just a label. A low-confidence report can still be high severity if the potential impact is serious.

## Step 4 — Build the defect artifact

The defect artifact must include:

- Title
- Severity with rationale
- Reproduction steps
- Expected behavior
- Actual behavior
- Evidence attachments or references
- Confidence statement
- Implementation impact or release impact

Keep reproduction steps grounded in the observed evidence. If the failure is not fully reproducible, say what part is deterministic and what part is not.

## Step 5 — Choose the output path

Pick the durable output that matches the repo workflow and the user request.

- Use a local Markdown artifact when the work is being tracked in-repo, when the repo does not require GitHub workflow, or when the user asked for a file-based handoff
- Prefer `docs/qa/<feature-name>/reports/YYYY-MM-DD-bug-<short-slug>.md` when
  a feature QA directory is known
- Use a GitHub issue only when the repository workflow explicitly wants issue tracking or the user requested an issue

Do not assume GitHub issue creation is the primary output. Do not mutate code, commit changes, or invent a delivery workflow as part of this skill.

## Step 6 — Write the report

### Local Markdown artifact

Write the defect report to the repo's documented QA or bug-tracking location. If the repo already has a bug or QA report directory, use that convention. If not, use a clear Markdown file path agreed with the repo context.

Suggested content structure:

```markdown
# Defect: [short title]

## Classification
- Evidence status: confirmed and reproducible / confirmed but environment-sensitive / suspected / needs more evidence
- Severity: [severity] - [rationale]
- Confidence: [high / medium / low] with a short explanation

## Scenario
[failing scenario or symptom]

## Environment and Build Context
- Branch:
- Commit:
- Build / release:
- Platform:
- Browser / device / runtime:
- Flags / data / permissions:

## Reproduction Steps
1. ...
2. ...
3. ...

## Expected
[expected behavior]

## Actual
[actual behavior]

## Evidence
- [log / screenshot / trace / test output reference]
- [link or file path]

## Impact
[implementation or release impact]
```

If the report adds a reusable E2E regression case, include:

```markdown
## Reusable Test Case
- Test case file: docs/qa/<feature-name>/test-cases/TC-NNN-<short-slug>.md
- Purpose: [why this case should be rerun]
```

### GitHub issue

Create an issue only when the repo workflow or user request calls for issue tracking. The issue body should preserve the same defect contract as the Markdown artifact and should link back to supporting evidence where possible.

## Step 7 — Handle weak evidence

If the report is `suspected / needs more evidence`, keep the artifact honest:

- State what is missing
- Mark the current confidence level clearly
- List the next evidence needed to confirm or rule out the defect
- Avoid overstating reproducibility

## Step 8 — Final check

Before returning the artifact, verify that the report answers these questions:

- What failed?
- How strong is the evidence?
- How severe is the impact?
- What proof supports the claim?
- Where should the durable record live?

## Configuration

- Evidence first, template second
- Confidence language must be explicit
- Default output is a Markdown artifact unless the repository workflow or user request requires GitHub issue tracking

## Edge Cases

- **No reproducible failure yet**: classify as `suspected / needs more evidence`
- **Environment-specific failure**: keep the defect confirmed, but note the sensitivity in the classification and impact
- **Multiple symptoms from one root cause**: document the primary failure and list secondary symptoms as supporting evidence
- **Evidence conflicts**: prefer direct runtime evidence over summaries, and record the conflict rather than hiding it
