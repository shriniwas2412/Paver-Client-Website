// Serves the built site from the repo root and runs the checks in e2e/.
// Run: cd tests && npm install && npx playwright install chromium && npm test
const { defineConfig, devices } = require("@playwright/test");
const PORT = 8765;
module.exports = defineConfig({
  testDir: "e2e",
  timeout: 60_000,
  fullyParallel: true,
  reporter: [["list"]],
  use: { baseURL: `http://localhost:${PORT}/`, trace: "retain-on-failure" },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"] }, testIgnore: /mobile\.spec\.js/ },
    { name: "mobile", use: { ...devices["Pixel 7"] }, testMatch: /mobile\.spec\.js/ },
  ],
  webServer: { command: `python3 -m http.server ${PORT}`, cwd: "..", port: PORT, reuseExistingServer: true },
});
