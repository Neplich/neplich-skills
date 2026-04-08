# Eval 4: PM Spec Handoff Stops Before Implementation

This workspace simulates a realistic handoff:

- PM documents already exist under `docs/pm/billing-notification-settings/`
- The product already has a settings page in `src/`
- Designer should read the PM spec, produce a UI/UX handoff doc, and stop
- Designer must not turn the PM spec directly into implementation work

The regression target is accidental behavior where the Designer role starts
editing code or producing engineer implementation steps after reading the PM
spec.
