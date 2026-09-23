// Schermafdruk van de footer op twee maten, om te zien hoe de nieuwe wagen tegen het Diepblauw staat.
// Gebruik: node footer-shot.cjs
const path = require('node:path');
const { chromium } = require('C:/users/arnas/git_repos/tandartsvanschiedam/node_modules/playwright');

const UIT = __dirname;
const MATEN = [
  { naam: '1440x900', width: 1440, height: 900 },
  { naam: '390x844', width: 390, height: 844, isMobile: true, deviceScaleFactor: 2 },
];

(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  for (const maat of MATEN) {
    const ctx = await browser.newContext({
      viewport: { width: maat.width, height: maat.height },
      deviceScaleFactor: maat.deviceScaleFactor || 1,
      isMobile: !!maat.isMobile,
      hasTouch: !!maat.isMobile,
    });
    const page = await ctx.newPage();
    await page.goto('http://127.0.0.1:8000/', { waitUntil: 'networkidle' });
    // alles laten laden: de footerfoto is lazy
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(1200);
    await page.evaluate(() => document.querySelectorAll('img').forEach(i => { i.loading = 'eager'; }));
    await page.waitForTimeout(800);
    const el = await page.$('.footer__intro') || await page.$('footer');
    await el.screenshot({ path: path.join(UIT, `footer-${maat.naam}.png`) });
    console.log('geschreven: footer-' + maat.naam + '.png');
    await ctx.close();
  }
  await browser.close();
})();
