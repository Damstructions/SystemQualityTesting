const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 60_000,
  fullyParallel: false,
  retries: 0,
  workers: 1,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }]
  ],
  use: {
    baseURL: 'https://opencart.abstracta.us/',
    ...devices['Desktop Chrome'],
    locale: 'en-AU',
    screenshot: 'on',
    trace: 'retain-on-failure',
    video: 'retain-on-failure'
  },
  outputDir: 'test-results'
});
