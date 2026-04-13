---
name: codebase-analyzer
description: "Scan and understand an existing codebase before starting work. Use this skill whenever the engineer needs to understand a project's structure, tech stack, coding conventions, dependencies, or architecture patterns before implementing features. Trigger on phrases like '分析代码库', '了解项目结构', '项目用了什么技术栈', '代码规范是什么', or any request to understand an existing codebase before coding."
---

# Codebase Analyzer

Scan an existing codebase and produce a structured Project Profile. This profile serves as context for all downstream engineer skills (feature-implementor, test-writer, etc.) so they can follow existing conventions.

## When to Use

- Before starting any work on an existing project
- When another skill needs project context but no Project Profile exists yet
- When the user asks about project structure, tech stack, or conventions

## Step 1 — Verify project root

Confirm you are in a valid project directory:

```bash
ls -la
```

Look for project markers: `.git`, `README.md`, `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `pom.xml`, `Makefile`, etc.

If no project markers found, tell the user this doesn't appear to be a project directory and ask for clarification.

## Step 2 — Scan project structure

```bash
find . -maxdepth 3 -type f \
  ! -path '*/node_modules/*' \
  ! -path '*/.git/*' \
  ! -path '*/vendor/*' \
  ! -path '*/dist/*' \
  ! -path '*/__pycache__/*' \
  ! -path '*/target/*' \
  | head -100
```

Identify:
- Source code directories (`src/`, `lib/`, `app/`, `pkg/`, `internal/`, `cmd/`)
- Test directories (`tests/`, `test/`, `__tests__/`, `spec/`)
- Config files (lint, format, build, CI)
- Documentation (`docs/`, `README`)

## Step 3 — Identify tech stack

Read the primary manifest file to determine:

| Marker File | Stack | Package Manager |
|-------------|-------|-----------------|
| `package.json` | Node.js / TypeScript | npm / yarn / pnpm / bun |
| `go.mod` | Go | go modules |
| `Cargo.toml` | Rust | cargo |
| `pyproject.toml` / `requirements.txt` | Python | pip / poetry / uv |
| `pom.xml` / `build.gradle` | Java / Kotlin | maven / gradle |
| `Gemfile` | Ruby | bundler |
| `composer.json` | PHP | composer |

Detect the framework from dependencies:
- **Node.js**: next, express, fastify, nestjs, react, vue, angular, svelte
- **Python**: django, flask, fastapi, streamlit
- **Go**: gin, echo, fiber, chi
- **Rust**: actix-web, axum, rocket

Also check for TypeScript (`tsconfig.json`) and monorepo indicators (`pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`).

## Step 4 — Extract coding conventions

Check for these config files and summarize what they enforce:

| Tool | Config Files |
|------|-------------|
| ESLint | `.eslintrc*`, `eslint.config.*` |
| Prettier | `.prettierrc*`, `prettier.config.*` |
| Biome | `biome.json` |
| Ruff | `ruff.toml`, `pyproject.toml [tool.ruff]` |
| Black | `pyproject.toml [tool.black]` |
| golangci-lint | `.golangci.yml` |
| rustfmt | `rustfmt.toml` |
| EditorConfig | `.editorconfig` |

Also sample 2-3 existing source files to detect:
- Naming style (camelCase / snake_case / PascalCase)
- Import ordering convention
- Comment style and density
- Error handling patterns

## Step 5 — Analyze dependencies

Read the manifest file and categorize:
- **Core framework** (e.g., Next.js 14, FastAPI 0.100)
- **Database** (prisma, drizzle, sqlalchemy, gorm, diesel)
- **Auth** (next-auth, passport, jwt libraries)
- **Testing** (jest, vitest, pytest, go test, cargo test)
- **Build tools** (webpack, vite, turbopack, esbuild)
- **Key libraries** (anything domain-specific)

## Step 6 — Identify architecture patterns

Based on directory structure and code samples, classify:

| Pattern | Indicators |
|---------|-----------|
| MVC | `controllers/`, `models/`, `views/` directories |
| Layered | `services/`, `repositories/`, `handlers/` directories |
| Feature-based | Directories named after features with co-located files |
| Monorepo | `packages/`, `apps/` with workspace config |
| Serverless | `functions/`, `api/` routes, serverless config |
| Microservices | Multiple `services/` with independent configs |

## Step 7 — Check CI/CD configuration

Look for:
- `.github/workflows/*.yml` (GitHub Actions)
- `.gitlab-ci.yml` (GitLab CI)
- `Jenkinsfile`
- `.circleci/config.yml`
- `Dockerfile`, `docker-compose.yml`

Summarize what CI does: lint, test, build, deploy.

## Step 8 — Produce Project Profile

Output the profile in this structure:

```yaml
project_profile:
  path: <project root>
  name: <from manifest or directory name>
  description: <from README or manifest>

  tech_stack:
    language: <primary language>
    framework: <primary framework + version>
    runtime: <node/deno/bun/python/go/etc + version if detectable>
    package_manager: <npm/yarn/pnpm/pip/cargo/etc>
    typescript: <true/false>
    monorepo: <true/false>

  architecture:
    pattern: <MVC/layered/feature-based/etc>
    source_dirs: [list of source directories]
    test_dirs: [list of test directories]
    key_modules: [list of main modules/features]

  conventions:
    naming: <camelCase/snake_case/PascalCase>
    linter: <tool + config summary>
    formatter: <tool + config summary>
    import_style: <description>
    error_handling: <description>

  dependencies:
    core: [framework, key libs with versions]
    database: <ORM/driver if any>
    auth: <auth solution if any>
    testing: <test framework>
    build: <build tool>

  ci_cd:
    platform: <GitHub Actions/GitLab CI/etc>
    steps: [lint, test, build, deploy]
    config_path: <path to CI config>

  docs:
    has_pm_docs: <true/false>
    pm_doc_inventory: [list of docs found in docs/]
    has_readme: <true/false>
    has_api_docs: <true/false>
```

## Edge Cases

- **Empty project**: If the directory only has `.git` and maybe a README, report `status: empty`. Recommend `pm-agent:idea-to-spec` when the user is still defining the product, and recommend `project-bootstrap` only when a TRD or approved PM docs already exist.
- **Monorepo**: Profile the root workspace config plus each package/app that seems relevant to the user's task. Ask which sub-project to focus on if unclear.
- **Multiple languages**: List all detected languages; identify the primary one by code volume. Note secondary languages (e.g., "Python backend + TypeScript frontend").
- **No CI**: Note the absence and flag as a gap.
- **No linter/formatter**: Note the absence. Sample code to infer implicit conventions.
