const { chromium } = require('C:/users/arnas/git_repos/tandartsvanschiedam/node_modules/playwright');
const BREEDTES = [1920, 1600, 1440, 1280, 1100, 1000, 900, 768, 600, 480, 390, 360];
(async () => {
  const b = await chromium.launch({ channel: 'msedge', headless: true });
  const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
  await p.goto('http://127.0.0.1:8000/werkwijze/', { waitUntil: 'domcontentloaded' });
  for (const w of BREEDTES) {
    await p.setViewportSize({ width: w, height: 900 });
    await p.waitForTimeout(120);
    const r = await p.evaluate(() => {
      const h = document.querySelector('.b-lijstplaat__huis');
      return h ? Math.round(h.getBoundingClientRect().width) : null;
    });
    console.log(`${String(w).padStart(4)} px venster -> huisje ${r} px`);
  }
  await b.close();
})();
