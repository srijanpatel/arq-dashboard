import { chromium } from "playwright";
import { mkdirSync } from "fs";

const BASE = "http://localhost:5555";
const OUT = "screenshots";

mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({
  args: ["--no-sandbox", "--disable-gpu"],
});

async function capture(name, url, theme, opts = {}) {
  const ctx = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 2,
  });
  const page = await ctx.newPage();

  // Set theme before navigating
  await page.addInitScript((t) => {
    localStorage.setItem("arq-dash-theme", t);
  }, theme);

  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(1500); // let charts render

  if (opts.scroll) {
    await page.evaluate((y) => window.scrollTo(0, y), opts.scroll);
    await page.waitForTimeout(500);
  }

  await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: opts.fullPage || false });
  console.log(`  ✓ ${name}.png`);
  await ctx.close();
}

async function captureWithAction(name, url, theme, action) {
  const ctx = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 2,
  });
  const page = await ctx.newPage();
  await page.addInitScript((t) => {
    localStorage.setItem("arq-dash-theme", t);
  }, theme);
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(1500);
  if (action) await action(page);
  await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: false });
  console.log(`  ✓ ${name}.png`);
  await ctx.close();
}

console.log("Taking screenshots...");

// Stats page — light
await capture("stats-light", `${BASE}/#/`, "light", { fullPage: true });

// Stats page — dark
await capture("stats-dark", `${BASE}/#/`, "dark", { fullPage: true });

// Jobs page — light (wait for table to render)
await captureWithAction("jobs-light", `${BASE}/#/jobs/`, "light", async (page) => {
  await page.waitForTimeout(1000);
  await page.click("button:has-text('Search')");
  await page.waitForTimeout(2000);
});

// Jobs page — dark
await captureWithAction("jobs-dark", `${BASE}/#/jobs/`, "dark", async (page) => {
  await page.waitForTimeout(1000);
  await page.click("button:has-text('Search')");
  await page.waitForTimeout(2000);
});

// Job detail — light
await capture("job-detail-light", `${BASE}/#/jobs/a03b0021c0039d0009e0033`, "light");

// Job detail — dark
await capture("job-detail-dark", `${BASE}/#/jobs/a03b0021c0039d0009e0033`, "dark");

await browser.close();
console.log("Done!");
