# Rujeet Prajapati — JavaScript system tests

These Playwright Test cases automate three OpenCart Abstracta functions.

| Test case ID | Function | Three scenarios |
|---|---|---|
| TC-RP-LOGIN | Customer login | Valid credentials, incorrect password, unregistered email |
| TC-RP-SEARCH | Product search | Exact name, partial keyword, unknown product |
| TC-RP-CART | Shopping cart | Add product, update quantity and total, remove product |

## Setup and execution

Install Node.js 18 or newer, then run:

```bash
cd rujeet-js-tests
npm install
npx playwright install chromium
npm test
```

To watch the tests execute:

```bash
npm run test:headed
```

Open the HTML evidence report with:

```bash
npm run report
```

Every scenario runs in a clean browser context. Playwright stores screenshots in `test-results/` and the interactive execution report in `playwright-report/`.
