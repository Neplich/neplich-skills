# PRD: Billing Notification Settings

## Goal

Allow workspace admins to control when billing alerts are sent, who receives
them, and how urgent alerts appear in the settings experience.

## User Stories

- As a workspace admin, I want to choose which billing events trigger email
  alerts so finance noise stays manageable.
- As an ops lead, I want to route overdue invoice alerts to a shared alias.
- As an owner, I want urgent payment-failure alerts to stand out from routine
  reminders.

## Acceptance Criteria

1. Admins can enable or disable reminder, invoice-issued, and payment-failed
   notifications.
2. Admins can edit at least one recipient email alias.
3. Urgent alerts are visually distinct from routine reminders.
4. The settings experience explains that billing changes affect the whole
   workspace.
