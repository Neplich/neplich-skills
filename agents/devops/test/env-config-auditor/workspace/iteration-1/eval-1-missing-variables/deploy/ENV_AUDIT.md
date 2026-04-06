# Environment Configuration Audit Report

## Missing Variables

- `API_KEY`: used in code, present in `deploy/local/.env.example`, missing in `deploy/docker/.env.example`, not referenced in CI/CD
- `REDIS_URL`: used in code, present in `deploy/local/.env.example`, missing in `deploy/docker/.env.example`, not referenced in CI/CD
- `STRIPE_SECRET_KEY`: used in code, missing in `deploy/local/.env.example`, missing in `deploy/docker/.env.example`, present in CI/CD only

## Coverage Snapshot

| Variable | Code Usage | Local | Docker | Helm | CI/CD |
|----------|-----------|-------|--------|------|-------|
| DATABASE_URL | ✅ | ✅ | ✅ | ❌ | ✅ |
| REDIS_URL | ✅ | ✅ | ❌ | ❌ | ❌ |
| API_KEY | ✅ | ✅ | ❌ | ❌ | ❌ |
| STRIPE_SECRET_KEY | ✅ | ❌ | ❌ | ❌ | ✅ |

## Security Issues

- No evidence of hardcoded secrets in the sample workspace
- Sensitive variables should not be committed with real values in `.env.example`

## Recommendations

1. Add `API_KEY` and `REDIS_URL` coverage to the Docker deployment path if Docker is a supported runtime.
2. Decide whether `STRIPE_SECRET_KEY` belongs in runtime env files, CI/CD secrets, or both, and document that path explicitly.
3. Add Helm or another production runtime config before claiming production readiness.
4. Keep CI/CD secret references aligned with the variables actually required by the application.
