/* Controle van de gedeelde navigatie en de pagina's op desktop en mobiel.
   Gebruik: node _werk/controle-layout.cjs <pad-naar-playwright> [basis-url] */
const { chromium } = require(process.argv[2] || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  const context = await browser.newContext({ reducedMotion: 'reduce' });
  const page = await context.newPage();
  const base = process.argv[3] || 'http://127.0.0.1:8765';
  const out = path.resolve(__dirname, '../website/review/cleanup');
  fs.mkdirSync(out, { recursive: true });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', response => {
    if (response.status() >= 400 && response.url().startsWith(base)) errors.push(`${response.status()} ${response.url()}`);
  });
  const routes = ['/', '/diensten/', '/kosten/', '/offerte/', '/contact/', '/over-ons/', '/werkwijze/',
    '/algemene-voorwaarden/', '/privacyverklaring/', '/offerte/bedankt/', '/contact/bedankt/', '/404.html'];
  try {
    for (const width of (process.env.LAYOUT_INTERACTIES ? [] : [1440, 1100, 768, 390, 320])) {
      await page.setViewportSize({ width, height: 900 });
      for (const route of routes) {
        await page.goto(base + route, { waitUntil: 'networkidle' });
        await page.evaluate(() => document.fonts.ready);
        const layout = await page.evaluate(() => {
          const header = document.querySelector('.header');
          const visible = [...header.querySelectorAll('a, button')].filter(el => el.getClientRects().length);
          return {
            width: document.documentElement.scrollWidth,
            viewport: innerWidth,
            headerOverflow: visible.some(el => el.getBoundingClientRect().right > innerWidth + 1),
            broken: [...document.images].filter(img => img.complete && !img.naturalWidth).map(img => img.src),
            h1: document.querySelectorAll('h1').length
          };
        });
        assert.ok(layout.width <= layout.viewport + 1, `${width} ${route}: overflow ${layout.width}`);
        assert.ok(!layout.headerOverflow, `${width} ${route}: header overflow`);
        assert.equal(layout.h1, 1, route);
        assert.deepEqual(layout.broken, [], `${width} ${route}: broken images`);
      }
      console.log(`${width}px: ${routes.length} pagina's gecontroleerd`);
    }

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(base, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(out, 'home-desktop.png') });
    const toggle = page.locator('.nav__open');
    await toggle.focus();
    await page.keyboard.press('Enter');
    assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.closest('.mega') !== null), true);
    await page.screenshot({ path: path.join(out, 'menu-desktop.png') });
    await page.keyboard.press('Escape');
    assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
    await page.locator('.nav__item--sub').hover();
    assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
    await page.keyboard.press('Escape');
    await page.waitForFunction(() => getComputedStyle(document.querySelector('.mega')).visibility === 'hidden');
    await page.mouse.move(5, 500);
    await toggle.blur();
    await page.locator('.footer').scrollIntoViewIfNeeded();
    await page.locator('.footer').screenshot({ path: path.join(out, 'footer-desktop.png'), style: '.header, .mcta, .skiplink { visibility: hidden !important; }' });
    assert.equal(await page.locator('.header').evaluate(el => el.classList.contains('is-vast')), true);

    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(base, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(out, 'home-mobile.png') });
    await page.locator('.header__menu').click();
    assert.equal(await page.locator('main').evaluate(el => el.inert), true);
    assert.equal(await page.locator('.header__menu').getAttribute('aria-expanded'), 'true');
    await page.locator('.lade__logo').focus();
    await page.keyboard.press('Shift+Tab');
    assert.equal(await page.locator('.lade__mail').evaluate(el => el === document.activeElement), true);
    await page.keyboard.press('Tab');
    assert.equal(await page.locator('.lade__logo').evaluate(el => el === document.activeElement), true);
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => !!document.activeElement.closest('.lade__paneel')), true);
    await page.screenshot({ path: path.join(out, 'menu-mobile.png') });
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('main').evaluate(el => el.inert), false);
    assert.equal(await page.locator('.header__menu').evaluate(el => el === document.activeElement), true);
    await page.locator('.footer').scrollIntoViewIfNeeded();
    await page.locator('.header__menu').blur();
    await page.locator('.footer').screenshot({ path: path.join(out, 'footer-mobile.png'), style: '.header, .mcta, .skiplink { visibility: hidden !important; }' });

    await page.setViewportSize({ width: 1366, height: 650 });
    await page.goto(base, { waitUntil: 'networkidle' });
    assert.ok(await page.locator('.of-box--hero').evaluate(el => el.getBoundingClientRect().bottom <= innerHeight), 'Offertekaart buiten laptopvenster');
    await page.screenshot({ path: path.join(out, 'home-laptop.png') });
    await page.locator('#of-van').fill('Den Haag');
    await page.locator('#of-naar').fill('Delft');
    await page.locator('#of-dienst').selectOption('particulier');
    await page.locator('.of-knop').click();
    await page.waitForURL('**/offerte/?**');
    assert.equal(await page.locator('#f-van').inputValue(), 'Den Haag');
    assert.equal(await page.locator('#f-naar').inputValue(), 'Delft');
    assert.equal(await page.locator('#f-dienst').inputValue(), 'particulier');

    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(base + '/diensten/', { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(out, 'diensten-mobile.png') });
    assert.deepEqual(errors, [], 'Browser errors');
    console.log('Navigatie, focus, afbeeldingen en browserconsole: akkoord.');
    console.log(`Screenshots: ${out}`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
