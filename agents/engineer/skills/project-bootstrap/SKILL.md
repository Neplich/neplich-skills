---
name: project-bootstrap
description: "Initialize a new project from settled specs only. If there is no TRD, PRD, or approved PM docs and the user did not explicitly say to skip PM, this skill must refuse to bootstrap and must redirect to `pm-agent:idea-to-spec` without asking about React, Vite, Next.js, package managers, or other stack choices."
---

# Project Bootstrap

Initialize a new project from scratch based on settled specs. Intelligently
chooses between official CLI tools and manual setup depending on the tech
stack.

## Non-Negotiable Gate

Before asking about frameworks, package managers, backend choices, or target
directories, run this gate:

1. Check whether a TRD or approved PM docs already exist.
2. Check whether the user explicitly said to skip PM and scaffold anyway.
3. If specs are missing and there is no explicit override, stop immediately and
   redirect to `pm-agent:idea-to-spec`.

In that stop branch, your response must do all of the following:

- state that there is no TRD, PRD, or other approved spec yet
- state that bootstrap should not start by default
- point the user to `pm-agent:idea-to-spec`
- mention that bootstrap can resume after PM docs are stable, or sooner only if
  the user explicitly says to skip PM

Do not ask stack questions in that branch. Do not suggest specific frameworks
in that branch. Do not begin scaffolding in that branch.

If the user invoked `project-bootstrap` directly but the gate fails, the direct
skill invocation does not override this rule.

## Required Stop-Branch Response

When specs are missing and the user did not explicitly say to skip PM, respond
with a short refusal/redirect in this shape:

```text
当前还没有 TRD、PRD 或其他已确认的 PM 文档，所以不能默认直接开始 bootstrap / scaffold。

这个请求应该先走 `pm-agent:idea-to-spec`，先把需求、范围和文档收敛下来。

等 PM 文档稳定后，我再根据 TRD 或已确认 spec 来初始化项目。
如果你明确要跳过 PM、直接搭一个 starter，也可以直接说明。
```

Keep it short. Do not append framework suggestions. Do not append stack
questions. Do not append an initialization plan.

## When to Use

- A TRD or approved PM docs describe a project that doesn't exist yet
- User explicitly asks to create/scaffold/bootstrap a new project and the
  required scope is already settled
- User explicitly says to skip PM discovery and just scaffold a starter

## Do Not Use

- Empty or near-empty workspace plus an idea-only product request
- Requests that are still converging on scope, flows, layout, roles, or PM docs
- Any case where the real next step is PRD / DECISIONS / TRD creation rather
  than code scaffolding

If those conditions apply, send the user to `pm-agent:idea-to-spec` first and
stop there.

## Step 1 — Read TRD or approved PM docs for tech stack requirements

Locate and read the strongest available spec:

```bash
find docs -maxdepth 4 \( -name 'TRD.md' -o -name 'trd.md' -o -name 'PRD.md' -o -name 'prd.md' -o -name 'DECISIONS.md' \) 2>/dev/null
```

Preferred input order:

1. engineer TRD
2. PM PRD plus DECISIONS
3. explicit user override to skip PM and scaffold anyway

If no TRD or approved PM docs exist:

- If the user explicitly said to skip PM and just scaffold, ask only for the
  minimum stack choices you need to initialize the repo.
- Otherwise stop and tell the user to run `pm-agent:idea-to-spec` first. Do not
  ask about frameworks, package managers, backend shape, or target directories.
  Do not start framework selection or scaffolding yet.

Extract from the available docs:
- **Language + framework** (e.g., TypeScript + Next.js)
- **Database** (if any)
- **Architecture pattern** (monorepo, serverless, etc.)
- **Key integrations** (auth provider, external APIs, etc.)

## Step 2 — Choose initialization method

Apply this decision tree:

```
Has official CLI scaffolder?
├── Yes → Use it (e.g., create-next-app, cargo init)
│   └── Does TRD specify options? → Pass them as CLI flags
└── No → Manual setup
    └── Create directory structure + manifest + minimal config
```

### Official CLI mapping

| Framework | Command | Common Options |
|-----------|---------|---------------|
| Next.js | `npx create-next-app@latest <name>` | `--typescript --tailwind --eslint --app --src-dir` |
| Vite (React) | `npm create vite@latest <name> -- --template react-ts` | |
| Vite (Vue) | `npm create vite@latest <name> -- --template vue-ts` | |
| Express | Manual (no official CLI) | |
| NestJS | `npx @nestjs/cli new <name>` | `--strict --package-manager <pm>` |
| FastAPI | Manual | |
| Django | `django-admin startproject <name>` | |
| Go module | `go mod init <module-path>` | |
| Rust | `cargo init <name>` | `--lib` or `--bin` |
| Tauri | `npm create tauri-app@latest` | |

If unsure, tell the user which CLI you plan to use and confirm before running.

## Step 3 — Run initialization

Execute the chosen method. For CLI tools, use non-interactive flags where possible to avoid prompts.

After initialization, verify the project structure:

```bash
ls -la
```

## Step 3.5 — Create standardized directory structure

Create the following standard directories with README files:

```bash
mkdir -p frontend backend docs deploy tmp
```

Create README.md for each directory:

- **frontend/README.md**: Frontend application code and assets
- **backend/README.md**: Backend services and APIs
- **docs/README.md**: Project documentation and planning materials
- **deploy/README.md**: Deployment scripts and configurations
- **tmp/README.md**: Temporary files and test outputs (add to .gitignore)

### Directory usage rules

- **frontend/**: All frontend code (web, mobile, desktop UI)
- **backend/**: All backend services, APIs, databases
- **docs/**: PRD, TRD, ADR, API specs, planning documents
- **deploy/**: Docker files, k8s configs, deployment scripts
- **tmp/**: Test outputs, build artifacts, temporary files (gitignored)

### Subdirectory README requirement

Every subdirectory created under these top-level directories MUST have its own README.md explaining:
- Purpose of the subdirectory
- Key files and their roles
- How to work with code in this directory

Update `.gitignore` to exclude tmp/:

```bash
echo "tmp/" >> .gitignore
```

## Step 4 — Configure project infrastructure

Based on TRD requirements and detected tech stack, set up:

### Linting & Formatting
- **TypeScript/JS**: ESLint + Prettier (or Biome)
- **Python**: Ruff
- **Go**: Built-in (`go fmt`, `go vet`) + golangci-lint
- **Rust**: rustfmt + clippy

### Git configuration
- `.gitignore` (use the framework's default, extend if needed)
- `.editorconfig` if the TRD mentions team-wide formatting

### CI (if TRD specifies)
Create `.github/workflows/ci.yml` with:
- Lint step
- Test step
- Build step

Use the simplest working CI config. Don't over-engineer.

## Step 5 — Install core dependencies

Based on TRD, install:
- Database ORM/driver
- Auth libraries
- Testing framework (if not included by the scaffolder)
- Any other TRD-specified dependencies

Use the detected package manager's install command.

## Step 6 — Verify the project works

Run these checks in order:

1. **Build**: `npm run build` / `cargo build` / `go build ./...` / etc.
2. **Lint**: `npm run lint` / `ruff check .` / `golangci-lint run` / etc.
3. **Test**: `npm test` / `pytest` / `go test ./...` / `cargo test` / etc. (expect 0 tests but no errors)

If any step fails, fix it before proceeding.

## Step 7 — Generate Project Profile

Run `codebase-analyzer` logic on the newly created project to produce a Project Profile. This becomes the handoff packet for subsequent skills.

## Step 8 — Summary

Output a summary:

```
## 项目初始化完成

- **项目名**: <name>
- **技术栈**: <language + framework>
- **包管理器**: <pm>
- **目录结构**: <brief description>
- **已配置**: lint ✅ / format ✅ / CI ✅ / test framework ✅
- **验证**: build ✅ / lint ✅ / test ✅

### 建议下一步
- 使用 `feature-implementor` 开始实现功能
```

## Edge Cases

- **TRD specifies unfamiliar framework**: Search for the framework's official getting-started guide and follow it. Don't guess.
- **Monorepo**: Use workspace tools (pnpm workspaces, Turborepo, Nx) as specified in TRD. Initialize root workspace first, then individual packages.
- **No TRD or approved PM docs available**: Redirect to `pm-agent:idea-to-spec` unless the user explicitly asked to skip PM and scaffold anyway.
- **Explicit skip-PM bootstrap**: Ask only the minimum stack questions
  (language, framework, project type) and generate a minimal viable setup.
- **CLI tool not installed**: Check with `which <tool>` or `npx` fallback. Install globally only if the user agrees.
- **Conflicting TRD requirements**: Flag the conflict to the user and ask for a decision before proceeding.
