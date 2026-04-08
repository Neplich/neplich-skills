# Eval 4: PM Spec Handoff Stops Before Implementation

## Test Case

Designer reads a complete PM handoff plus existing UI code context for billing
notification settings.

## With Skill Output

**Locations**

- `with_skill/outputs/transcript.md`
- `with_skill/docs/design/billing-notification-settings/ui-ux-spec.md`

**Observed behavior**

- ✅ Reads PM spec and existing UI context
- ✅ Treats PM spec as design input only
- ✅ Produces a structured UI/UX handoff doc
- ✅ Explicitly stops at design handoff
- ✅ Routes implementation to Engineer

## Without Skill Output

**Location**

- `without_skill/outputs/transcript.md`

**Observed behavior**

- ❌ Treats completed PM spec as enough to start coding
- ❌ Mentions modifying source files directly
- ❌ Skips the design deliverable
- ❌ Drifts into implementation and testing steps

## Conclusion

This regression case directly covers the boundary failure we want to prevent:
Designer must be able to read an already-complete PM spec without turning that
into implementation work.
