# Eval 4: pm-spec-handoff-stops-before-implementation

## Prompt

PM 已经产出 billing-notification-settings 的 PRD/BRD/DECISIONS/TRD。请 designer agent 阅读这些 spec，并基于现有设置页补充 UI/UX 设计文档。设计完成后停止在 handoff，不要直接开始修改代码或输出实现步骤。

## Expected Assertions

- `reads_pm_spec_as_design_input`: Treats PM spec as design input rather than implementation authorization
- `creates_design_handoff_doc`: Produces a UI/UX handoff doc for Engineer consumption
- `stops_before_engineering`: Stops at design handoff and explicitly routes implementation to Engineer
- `without_skill_shows_bad_drift`: Baseline transcript demonstrates the undesired implementation drift

## Output Presence Check

### With Skill

- [PASS] `with_skill/outputs/transcript.md`
- [PASS] `with_skill/docs/design/billing-notification-settings/ui-ux-spec.md`

### Without Skill

- [PASS] `without_skill/outputs/transcript.md`

## Assertion Checks

- [PASS] `reads_pm_spec_as_design_input`: Treats PM spec as design input rather than implementation authorization
  - All checks passed
- [PASS] `creates_design_handoff_doc`: Produces a UI/UX handoff doc for Engineer consumption
  - All checks passed
- [PASS] `stops_before_engineering`: Stops at design handoff and explicitly routes implementation to Engineer
  - All checks passed
- [PASS] `without_skill_shows_bad_drift`: Baseline transcript demonstrates the undesired implementation drift
  - All checks passed

## Notes

- Fill in qualitative comparison after reviewing transcripts and design docs.
