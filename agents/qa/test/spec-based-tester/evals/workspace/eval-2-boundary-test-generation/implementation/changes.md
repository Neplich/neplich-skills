# Implementation Changes

Validation moved from the form component into `auth/validators.ts`. Locked
account handling now shares the same error boundary as invalid credentials.
