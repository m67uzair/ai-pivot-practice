// Captures real screenshots of the live/public project pages for the demo.
const {chromium} = require('playwright');
const fs = require('fs');

const SHOTS = [
  // [url, filename, fullPage]
  ['https://github.com/m67uzair/pr-review-bot-test/pull/1', 'pr_conversation.png', true],
  ['https://github.com/m67uzair/pr-review-bot-test/pull/1/files', 'pr_diff.png', true],
  ['https://pr-review-bot-production-36f2.up.railway.app/docs', 'live_docs.png', false],
];

(async () => {
  fs.mkdirSync('public/shots', {recursive: true});
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: {width: 1440, height: 900},
    deviceScaleFactor: 2,
  });
  for (const [url, file, full] of SHOTS) {
    try {
      await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 45000});
      await page.waitForTimeout(3500);
      await page.screenshot({path: 'public/shots/' + file, fullPage: full});
      console.log('OK   ', file);
    } catch (e) {
      console.log('FAIL ', file, String(e).slice(0, 140));
    }
  }
  await browser.close();
})();
