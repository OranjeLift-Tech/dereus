/* Controle van de gekozen accordion: toetsenbord, onderbroken animaties, mobiel en zonder JS. */
const { chromium } = require(process.argv[2] || 'playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const base = process.argv[3] || 'http://127.0.0.1:8765';

(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  try {
    for (const reducedMotion of ['no-preference', 'reduce']) for (const width of [1440, 390, 320]) {
      const page = await browser.newPage({ viewport: { width, height: 900 }, reducedMotion });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.goto(base, { waitUntil: 'networkidle' });
      const section = page.locator('[data-werkwijze]');
      await section.scrollIntoViewIfNeeded();
      const buttons = section.locator('summary');
      assert.equal(await buttons.count(), 5);
      assert.deepEqual(await section.locator('.werkwijze__stappen > li').evaluateAll(items => items.map(el => el.id)),
        ['stap-1', 'stap-2', 'stap-3', 'stap-4', 'stap-5']);
      assert.equal(await buttons.first().getAttribute('aria-expanded'), 'true');
      if (width > 800) {
        const list = await section.locator('.werkwijze__stappen').boundingBox();
        const image = await section.locator('.werkwijze__beeld').boundingBox();
        assert.ok(image.x > list.x + list.width, 'step text left, prominent image right');
      } else assert.equal(await section.locator('.werkwijze__beeld').isVisible(), false);
      await buttons.first().focus(); await page.keyboard.press('ArrowDown');
      assert.equal(await buttons.nth(1).evaluate(el => el === document.activeElement), true);
      await page.keyboard.press('Enter');
      await page.waitForFunction(() => document.querySelector('.werkwijze').getAnimations({ subtree: true }).length === 0);
      assert.equal(await buttons.nth(1).getAttribute('aria-expanded'), 'true');
      assert.equal(await section.locator('details[open]').count(), 1);
      if (width <= 800) assert.equal(await section.locator('details[open] .werkwijze__mobielbeeld').isVisible(), true);
      // Interrupt several in-flight transitions; only the final requested step may remain open.
      await buttons.evaluateAll(items => { items[3].click(); items[0].click(); items[4].click(); });
      if (reducedMotion === 'reduce') assert.equal(await section.evaluate(el => el.getAnimations({ subtree: true }).length), 0);
      await page.waitForFunction(() => document.querySelector('.werkwijze').getAnimations({ subtree: true }).length === 0);
      assert.equal(await section.locator('details[open]').count(), 1);
      assert.equal(await buttons.nth(4).getAttribute('aria-expanded'), 'true');
      await page.waitForFunction(() => document.querySelector('[data-stap-beeld="4"]').classList.contains('is-actief'));
      for (const button of await buttons.all()) {
        const id = await button.getAttribute('aria-controls');
        assert.equal(await page.locator(`[id="${id}"]`).count(), 1);
      }
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
      if ((width === 1440 && reducedMotion === 'no-preference') || (width === 390 && reducedMotion === 'reduce')) {
        await page.locator('#werkwijze').screenshot({ path: path.join(__dirname, `../website/review/cleanup/werkwijze-selected5-${width}.png`),
          style: '.header, .mcta, .whatsapp { visibility: hidden !important; }' });
      }
      await page.evaluate(() => { location.hash = 'stap-3'; });
      await page.waitForFunction(() => document.querySelector('#stap-3 details').open);
      assert.equal(await section.locator('details[open]').count(), 1);
      assert.deepEqual(errors, []);
      console.log(`${width}px, motion=${reducedMotion}: akkoord`);
      await page.close();
    }
    const page = await browser.newPage({ javaScriptEnabled: false, viewport: { width: 390, height: 900 } });
    await page.goto(base, { waitUntil: 'networkidle' });
    await page.locator('#stap-4 summary').click();
    assert.equal(await page.locator('#stap-4 .werkwijze__antwoord').isVisible(), true, 'native accordion works without JS');
    console.log('Zonder JavaScript: akkoord');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
