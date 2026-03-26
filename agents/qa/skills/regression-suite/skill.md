---
name: regression-suite
description: "Manage regression test suites. Re-run tests after bug fixes to verify fixes and ensure no new regressions. Use when Engineer completes a bug fix and you need to validate the fix works correctly."
---

# Regression Suite

Manage and execute regression tests after bug fixes. Verify that fixes work correctly and no new issues were introduced.

## When to Use

- After Engineer fixes a bug and submits code
- When user asks to "回归测试", "验证修复", or "regression test"
- Before releasing a hotfix
- To re-validate previously discovered issues

## Step 1 — Identify regression scope

Determine which bugs need regression testing:

```bash
# Check for bug reports
ls docs/bugs/bug-*.md 2>/dev/null

# Or check GitHub issues with bug label
gh issue list --label "bug" --state open 2>/dev/null
```

If a specific Bug ID or PR is provided, focus on that bug's test cases.

## Step 2 — Read bug report

Read the original bug report to understand:
- Reproduction steps
- Expected vs actual behavior
- Environment information
- Related test scenarios

```bash
# Read specific bug report
cat docs/bugs/bug-NNN.md

# Or read GitHub issue
gh issue view NNN 2>/dev/null
```

## Step 3 — Detect environment

Check if the application is already running:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
```

If response is not 200, proceed to start the application.

## Step 4 — Start application

Try to start the application using these methods in order:

1. Check `deploy/local.md` for startup commands
2. Try common commands:
   - `npm run dev`
   - `npm start`
   - `yarn dev`
   - `pnpm dev`
   - `docker-compose up -d`

Wait for health check (max 60 seconds, check every 2 seconds):

```bash
for i in {1..30}; do
  if curl -s http://localhost:3000 > /dev/null; then
    echo "App ready"
    break
  fi
  sleep 2
done
```

## Step 5 — Install dependencies

Install Playwright if not already installed:

```bash
npm install -D playwright
npx playwright install chromium
```

## Step 6 — Execute regression tests

Reproduce the original bug's steps to verify the fix:

```javascript
const { chromium } = require('playwright');

const regressionResults = {
  bugId: 'NNN',
  total: 0,
  passed: 0,
  failed: 0,
  tests: []
};

async function runRegressionTest(name, testFn) {
  regressionResults.total++;
  const result = { name, status: 'passed', error: null };
  try {
    await testFn();
    regressionResults.passed++;
    console.log(`✓ [Regression] ${name}`);
  } catch (error) {
    regressionResults.failed++;
    result.status = 'failed';
    result.error = error.message;
    console.log(`✗ [Regression] ${name}: ${error.message}`);
  }
  regressionResults.tests.push(result);
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto('http://localhost:3000');

  // Test 1: Verify the original bug is fixed
  await runRegressionTest('Original bug fix verification', async () => {
    // Follow reproduction steps from bug report
    // Assert expected behavior now works
  });

  // Test 2: Verify related functionality still works
  await runRegressionTest('Related feature regression check', async () => {
    // Test nearby features that might be affected
  });

  await browser.close();

  console.log(JSON.stringify(regressionResults, null, 2));
})();
```

## Step 7 — Check for new regressions

Run broader tests around the fixed area:

- Related UI flows
- Adjacent features
- Edge cases of the fixed functionality

Monitor for:
- Console errors
- Network failures
- Visual regressions
- Performance degradation

## Step 8 — Generate regression report

Create regression report at `docs/qa-reports/YYYY-MM-DD-regression-report.md`:

```markdown
# 回归测试报告 - YYYY-MM-DD

**执行时间**: YYYY-MM-DD HH:MM - HH:MM
**测试类型**: 回归测试
**关联 Bug**: Bug #NNN / PR #NNN

## 修复验证
- Bug #NNN: ✓ 已修复 / ✗ 未修复

## 回归检查
- 总用例数: N
- 通过: N
- 失败: N
- 新问题: N

## 新发现的问题
1. [Bug #NNN](../bugs/bug-NNN.md) - [描述]

## 结论
- ✓ 修复有效，无新回归问题
- ✗ 修复无效 / 发现新回归问题
```

## Step 9 — Update bug status

If the fix is verified:

```bash
# For local bugs
# Add "已验证" status to bug report header

# For GitHub issues
gh issue comment NNN --body "回归测试通过，修复已验证。详见 docs/qa-reports/YYYY-MM-DD-regression-report.md"
```

If the fix failed:

```bash
# For GitHub issues
gh issue comment NNN --body "回归测试失败，Bug 仍可复现。详见 docs/qa-reports/YYYY-MM-DD-regression-report.md"
```

## Step 10 — Cleanup

Close browser and stop application if it was started by this skill.

## Step 11 — Commit results

Commit the regression report:

```bash
git add docs/qa-reports/
git commit -m "Add regression test report - $(date +%Y-%m-%d)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

## Configuration

Default settings (can be overridden by user):

- Target URL: http://localhost:3000
- Browser: Chrome (headless)
- Test timeout: 30 seconds per test

## Edge Cases

- **Bug report not found**: Ask user for Bug ID or reproduction steps
- **App won't start**: Report error and ask user to start manually
- **Fix not deployed**: Ask user to deploy the fix first
- **Multiple bugs to verify**: Run regression for each bug sequentially
- **Original bug cannot be reproduced on old code**: Note in report, may be environment-specific
