// Schermafdruk van de sectie "Wat u vooraf kunt regelen" op /werkwijze/, op twee maten.
// Gebruik: node lijstplaat-shot.cjs
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
    await page.goto('http://127.0.0.1:8000/werkwijze/', { waitUntil: 'networkidle' });
    await page.evaluate(() => {
      document.querySelectorAll('img').forEach(i => { i.loading = 'eager'; });
      const el = document.querySelector('#voorbereiding');
      if (el) el.scrollIntoView({ block: 'center' });
    });
    await page.waitForTimeout(1500);
    const el = await page.$('#voorbereiding');
    if (!el) throw new Error('#voorbereiding niet gevonden');
    await el.screenshot({ path: path.join(UIT, `lijstplaat-${maat.naam}.png`) });
    // ook even nakijken wat de foto werkelijk is en hoe groot het huisje staat
    const info = await page.evaluate(() => {
      const img = document.querySelector('.b-lijstplaat__foto');
      const huis = document.querySelector('.b-lijstplaat__huis');
      if (!img || !huis) return null;
      const r = huis.getBoundingClientRect();
      return { src: img.getAttribute('src'), natuurlijk: img.naturalWidth + 'x' + img.naturalHeight,
               huis: Math.round(r.width) + 'x' + Math.round(r.height) };
    });
    console.log(maat.naam, JSON.stringify(info));
    await ctx.close();
  }
  await browser.close();
})();
