/* Alle 27 headers: unieke achtergronden, toegankelijke invoer en native GET-overdracht. */
const { chromium } = require(process.argv[2] || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.argv[3] || 'http://127.0.0.1:8765';
const liveRoutes = ['/', '/diensten/', '/kosten/', '/offerte/', '/contact/', '/over-ons/', '/werkwijze/',
  '/algemene-voorwaarden/', '/privacyverklaring/', '/offerte/bedankt/', '/contact/bedankt/', '/404.html'];
const manifest = require('../img/headers/manifest.json');
const routes = Object.keys(manifest);
const address = route => base + (liveRoutes.includes(route) ? '' : '/_voorbeeld') + route;
const out = path.resolve(__dirname, '../website/review/cleanup/headers-final');

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  const page = await browser.newPage({ reducedMotion: 'reduce' });
  const errors = [], measurements = [];
  page.on('pageerror', error => errors.push(error.message));
  try {
    assert.equal(routes.length, 27);
    for (const [width, height] of [[1440, 900], [1366, 768], [768, 1024], [390, 667], [320, 568]]) {
      const backgrounds = new Set();
      await page.setViewportSize({ width, height });
      for (const route of routes) {
        await page.goto(address(route), { waitUntil: 'networkidle' });
        await page.evaluate(() => document.fonts.ready);
        const info = await page.evaluate(() => {
          const card = document.querySelector('.of-box--header'), form = card?.querySelector('form');
          const photo = document.querySelector('.hero__foto img, .pk__foto');
          const select = form?.querySelector('select'), styles = select && getComputedStyle(select);
          const canvas = document.createElement('canvas').getContext('2d');
          if (styles) canvas.font = `${styles.fontWeight} ${styles.fontSize} ${styles.fontFamily}`;
          const rect = card?.getBoundingClientRect(), header = document.querySelector('.header').getBoundingClientRect();
          const ids = [...document.querySelectorAll('[id]')].map(el => el.id);
          const title = document.querySelector('.hero__h1,.pk__h1').getBoundingClientRect();
          const text = document.querySelector('.hero__tekst,.pk__tekst').getBoundingClientRect();
          const region = document.querySelector('.hero,.pk').getBoundingClientRect();
          const content = document.querySelector('main').cloneNode(true);
          content.querySelectorAll('.hero,.pk,.hero-pil,.pk-pil,.pk__ankers,script').forEach(el => el.remove());
          return { count: document.querySelectorAll('.of-box--header').length,
            top: rect?.top, bottom: rect?.bottom, headerBottom: header.bottom,
            overflow: document.documentElement.scrollWidth > innerWidth + 1,
            photo: photo?.getAttribute('src'), imageReady: !!photo?.complete && !!photo?.naturalWidth,
            fieldIds: form ? [...form.querySelectorAll('input,select')].map(el => el.id) : [],
            duplicates: ids.filter((id, index) => ids.indexOf(id) !== index),
            placeholder: select?.options[0]?.textContent,
            textWidth: select ? canvas.measureText(select.options[0].textContent).width : Infinity,
            available: select ? select.clientWidth - parseFloat(styles.paddingLeft) - parseFloat(styles.paddingRight) : 0,
            labelOverflow: form ? [...form.querySelectorAll('.of-veld > span')].some(el => el.scrollWidth > el.clientWidth + 1) : true,
            labels: form ? [...form.querySelectorAll('input,select')].every(el => el.labels?.length && el.labels[0].textContent.trim()) : false,
            method: form?.method, action: form?.getAttribute('action'),
            centered: Math.abs((text.left + text.right) / 2 - innerWidth / 2) < 2,
            headingClipped: title.top < header.bottom - 1 || title.left < 0 || title.right > innerWidth + 1 || text.bottom > region.bottom + 1,
            contentLength: content.textContent.replace(/\s+/g, ' ').trim().length
          };
        });
        measurements.push({ route, width, height, ...info });
        assert.equal(info.count, 1, `${width} ${route}: one header form`);
        assert.deepEqual(info.fieldIds, ['header-of-van', 'header-of-naar', 'header-of-datum', 'header-of-dienst']);
        assert.deepEqual(info.duplicates, [], `${width} ${route}: unique IDs`);
        assert.equal(info.overflow, false, `${width} ${route}: overflow`);
        assert.equal(info.imageReady, true, `${width} ${route}: background loaded`);
        assert.equal(info.photo, manifest[route].src, `${route}: matches route-specific manifest`);
        assert.equal(info.labels, true, `${route}: accessible field labels`);
        assert.equal(info.method, 'get', `${route}: native GET method`);
        assert.equal(info.action, '/offerte/', `${route}: native quote destination`);
        assert.equal(info.centered, true, `${width} ${route}: centered heading`);
        assert.equal(info.headingClipped, false, `${width} ${route}: heading content clipped`);
        assert.ok(info.contentLength > (route.includes('/bedankt/') || route === '/404.html' ? 40 : 80), `${route}: non-header page content remains`);
        assert.equal(info.placeholder, 'Kies een type');
        assert.ok(info.textWidth <= info.available + 1, `${width} ${route}: placeholder clipped (${info.textWidth}/${info.available})`);
        assert.equal(info.labelOverflow, false, `${width} ${route}: field label clipped`);
        if (width >= 1366) {
          assert.ok(info.top >= info.headerBottom, `${width} ${route}: header navigation obscures form`);
          assert.ok(info.bottom <= height, `${width} ${route}: quote below fold (${info.bottom}/${height})`);
        }
        backgrounds.add(info.photo);
        if ([1440, 390, 320].includes(width) && ['/', '/diensten/', '/offerte/', '/over-ons/', '/404.html', '/werkgebied/delft/', '/diensten/internationale-verhuizingen/'].includes(route)) {
          const name = route === '/' ? 'home' : route.replaceAll('/', '').replace('.html', '');
          await page.screenshot({ path: path.join(out, `${name}-${width}.png`) });
        }
        if (route === '/' && width === 1440) {
          for (const id of ['diensten', 'waarom', 'cijfers', 'werkwijze', 'reviews', 'over-ons', 'werkgebied', 'vragen', 'aanvraag', 'contact']) {
            assert.equal(await page.locator(`#${id}`).count(), 1, `Preserved homepage section ${id}`);
          }
          assert.equal(await page.locator('.werkwijze__stap').count(), 5, 'Five preserved moving-process steps');
          const process = await page.locator('#werkwijze').textContent();
          for (const phrase of ['U laat uw gegevens en uw verhuisdatum achter.', 'Binnen 24 uur belt uw verhuisadviseur u.', 'Duidelijk, vrijblijvend en op maat.', 'Na uw akkoord zetten wij de datum vast.', 'Wij doen het zware werk, u wijst aan waar alles moet komen.']) {
            assert.ok(process.includes(phrase), `Preserved process copy: ${phrase}`);
          }
        }
      }
      assert.equal(backgrounds.size, routes.length, `${width}: every page has a different background`);
      await page.goto(base, { waitUntil: 'networkidle' });
      const form = page.locator('.of-box--header form');
      await form.locator('[name=van]').focus();
      await page.keyboard.press('Tab');
      assert.equal(await page.locator('[name=naar]').first().evaluate(el => el === document.activeElement), true, 'Tab moves from origin to destination');
      const select = form.locator('[name=dienst]');
      await select.selectOption('');
      await select.focus();
      await page.keyboard.press('ArrowDown');
      await page.keyboard.press('Enter');
      assert.notEqual(await select.inputValue(), '', 'Native select changes with keyboard');
      assert.ok(await select.evaluate(el => getComputedStyle(el.closest('label')).boxShadow !== 'none'), 'Visible field focus treatment');
      await page.keyboard.press('Tab');
      assert.equal(await form.locator('button[type=submit]').evaluate(el => el === document.activeElement), true, 'Tab reaches submit');
      await form.locator('[name=van]').fill('Den Haag');
      await form.locator('[name=naar]').fill('Delft');
      await form.locator('[name=datum]').fill('2027-05-20');
      await form.locator('[name=dienst]').selectOption('particulier');
      await form.locator('button[type=submit]').click();
      await page.waitForURL('**/offerte/?**');
      assert.equal(await page.locator('#f-van').inputValue(), 'Den Haag');
      assert.equal(await page.locator('#f-naar').inputValue(), 'Delft');
      assert.equal(await page.locator('#f-datum').inputValue(), '2027-05-20');
      assert.equal(await page.locator('#f-dienst').inputValue(), 'particulier');
      console.log(`${width}x${height}: 27 headers, toetsenbord en offerte-overdracht akkoord`);
    }
    // Native GET must also work without JavaScript, including on concept pages.
    const noJs = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 1366, height: 768 } });
    const native = await noJs.newPage();
    for (const route of routes) {
      await native.goto(address(route), { waitUntil: 'domcontentloaded' });
      const form = native.locator('.of-box--header form');
      await form.locator('[name=van]').fill('Den Haag');
      await form.locator('[name=naar]').fill('Delft');
      await form.locator('[name=datum]').fill('2027-05-20');
      await form.locator('[name=dienst]').selectOption('particulier');
      await form.locator('button[type=submit]').click();
      await native.waitForURL('**/offerte/?**');
      const url = new URL(native.url());
      assert.equal(url.pathname, '/offerte/');
      for (const [key, value] of Object.entries({ van: 'Den Haag', naar: 'Delft', datum: '2027-05-20', dienst: 'particulier' })) assert.equal(url.searchParams.get(key), value, `${route}: native ${key}`);
    }
    await noJs.close();
    console.log('27 native GET-formulieren zonder JavaScript akkoord.');
    assert.deepEqual(errors, [], 'No browser errors');
  } finally {
    fs.writeFileSync(path.join(out, 'measurements.json'), JSON.stringify(measurements, null, 2));
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
