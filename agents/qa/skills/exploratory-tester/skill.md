---
name: exploratory-tester
description: "Automatically explore UI to discover undocumented issues. Simulates random user actions (clicks, inputs, scrolling) to find crashes, errors, and performance problems. Use when you need to test beyond documented specs or discover edge cases."
---

# Exploratory Tester

Automatically explore a web application UI to discover issues not covered by documentation. This skill simulates random user behavior to find crashes, errors, and unexpected behaviors.

## When to Use

- After implementing new features to discover edge cases
- When Test Spec coverage is incomplete
- To find UI issues before formal testing
- When user asks to "探索测试", "自动测试UI", or "发现潜在问题"

## Step 1 — Detect environment

Check if the application is already running:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
```

If response is not 200, proceed to start the application.

## Step 2 — Start application

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

## Step 3 — Install dependencies

Install Playwright if not already installed:

```bash
npm install -D playwright
npx playwright install chromium
```

## Step 4 — Initialize Playwright

Create a minimal test script to initialize Playwright:

```javascript
// exploratory-test.js
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto('http://localhost:3000');
  await explore(page);
  await browser.close();
})();
```

## Step 5 — Random exploration

Implement exploration logic (default 10 minutes):

```javascript
const issues = [];
const visited = new Set();

function generateRandomInput() {
  const types = [
    () => Math.random().toString(36).substring(7),
    () => Math.floor(Math.random() * 10000).toString(),
    () => new Date().toISOString().split('T')[0],
    () => 'test@example.com'
  ];
  return types[Math.floor(Math.random() * types.length)]();
}

async function explore(page, duration = 600000) {
  const startTime = Date.now();

  while (Date.now() - startTime < duration) {
    try {
      // Random action selection
      const action = Math.random();

      if (action < 0.4) {
        // Click random clickable element
        const elements = await page.$$('button, a, [role="button"]');
        if (elements.length > 0) {
          const el = elements[Math.floor(Math.random() * elements.length)];
          await el.click();
        }
      } else if (action < 0.7) {
        // Input random text
        const inputs = await page.$$('input, textarea');
        if (inputs.length > 0) {
          const input = inputs[Math.floor(Math.random() * inputs.length)];
          await input.fill(generateRandomInput());
        }
      } else {
        // Scroll
        await page.evaluate(() => window.scrollBy(0, Math.random() * 500 - 250));
      }

      await page.waitForTimeout(1000);

    } catch (error) {
      // Record exception
      issues.push({
        type: 'error',
        message: error.message,
        url: page.url(),
        timestamp: new Date().toISOString()
      });
    }
  }
}
```

## Step 6 — Record exceptions

Monitor for these issue types:

- Console errors (error level)
- Network failures (4xx, 5xx)
- Unhandled promise rejections
- Page crashes
- Slow responses (> 3 seconds)

```javascript
page.on('console', msg => {
  if (msg.type() === 'error') {
    issues.push({
      type: 'console_error',
      message: msg.text(),
      url: page.url(),
      timestamp: new Date().toISOString()
    });
  }
});

page.on('response', response => {
  if (response.status() >= 400) {
    issues.push({
      type: 'network_error',
      status: response.status(),
      url: response.url(),
      timestamp: new Date().toISOString()
    });
  }
});
```

## Step 7 — Generate report

Create exploration report at `docs/qa-reports/YYYY-MM-DD-exploratory-report.md`:

```markdown
# 探索测试报告 - YYYY-MM-DD

**执行时间**: YYYY-MM-DD HH:MM - HH:MM
**探索时长**: 10 分钟
**访问页面数**: N

## 发现的问题

### 严重问题 (N)
1. [描述] - 复现路径
2. ...

### 一般问题 (N)
1. [描述] - 复现路径
2. ...

## 探索路径
- 页面 A → 页面 B → 页面 C
- ...

## 建议
- [改进建议]
```

## Step 8 — Cleanup

Close browser and stop application if it was started by this skill:

```javascript
await browser.close();
```

If application was started by this skill:

```bash
# Kill the process started in Step 2
kill $APP_PID
```

## Step 9 — Commit results

Commit the exploration report:

```bash
git add docs/qa-reports/
git commit -m "Add exploratory test report - $(date +%Y-%m-%d)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

## Configuration

Default settings (can be overridden by user):

- Exploration duration: 10 minutes
- Target URL: http://localhost:3000
- Browser: Chrome (headless)
- Action delay: 1 second between actions

## Edge Cases

- **App won't start**: Report error and ask user to start manually
- **No clickable elements**: Focus on navigation and scrolling
- **Authentication required**: Ask user for login credentials or test URL
- **No issues found**: Report successful exploration with no issues
