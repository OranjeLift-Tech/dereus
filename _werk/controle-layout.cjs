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
            duplicateIds: [...document.querySelectorAll('[id]')].map(el => el.id).filter((id, i, ids) => ids.indexOf(id) !== i),
            brokenLabels: [...document.querySelectorAll('label[for]')].filter(el => !document.getElementById(el.htmlFor)).map(el => el.htmlFor),
            brokenAria: [...document.querySelectorAll('[aria-controls],[aria-labelledby],[aria-describedby]')].flatMap(el =>
              ['aria-controls', 'aria-labelledby', 'aria-describedby'].flatMap(attr => (el.getAttribute(attr) || '').split(/\s+/).filter(id => id && !document.getElementById(id)))),
            h1: document.querySelectorAll('h1').length
          };
        });
        assert.ok(layout.width <= layout.viewport + 1, `${width} ${route}: overflow ${layout.width}`);
        assert.ok(!layout.headerOverflow, `${width} ${route}: header overflow`);
        assert.equal(layout.h1, 1, route);
        assert.deepEqual(layout.broken, [], `${width} ${route}: broken images`);
        assert.deepEqual(layout.duplicateIds, [], `${width} ${route}: duplicate ids`);
        assert.deepEqual(layout.brokenLabels, [], `${width} ${route}: broken form labels`);
        assert.deepEqual(layout.brokenAria, [], `${width} ${route}: broken ARIA references`);
        const whatsapp = page.locator('.whatsapp');
        assert.equal(await whatsapp.count(), 1, `${width} ${route}: WhatsApp contact`);
        assert.equal(await whatsapp.getAttribute('aria-label'), 'Contact met Verhuisbedrijf De Reus via WhatsApp');
        assert.equal(await whatsapp.getAttribute('href'), 'https://wa.me/31850005647');
        assert.equal(await whatsapp.getAttribute('disabled'), null);
        assert.deepEqual(await page.evaluate(() => [...document.querySelectorAll('a[href="tel:+31850005647"]')].flatMap(tel => {
          const wa = tel.nextElementSibling;
          if (!wa || wa.href !== 'https://wa.me/31850005647' || !wa.hasAttribute('data-whatsapp-business')) return [tel.outerHTML];
          if (wa.nextElementSibling?.hasAttribute('data-whatsapp-business')) return ['Duplicate WhatsApp alternative'];
          if (wa.target === '_blank' && !wa.rel.includes('noopener')) return ['Unsafe new tab'];
          const visible = el => !!el.getClientRects().length && getComputedStyle(el).visibility !== 'hidden';
          return visible(tel) && !visible(wa) ? ['Visible phone without visible WhatsApp'] : [];
        })), [], `${width} ${route}: paired business phone contacts`);
        assert.deepEqual(await page.locator('.knop--cta').evaluateAll(items => items.filter(el => el.getClientRects().length).flatMap(el => {
          const style = getComputedStyle(el), box = el.getBoundingClientRect();
          return box.height < 44 || style.boxShadow.includes('inset') || parseFloat(style.borderTopWidth) > 1 ? [el.className] : [];
        })), [], `${width} ${route}: clean CTA styling and touch size`);
        assert.ok(await whatsapp.evaluate(el => {
          const box = el.getBoundingClientRect(), bar = document.querySelector('.mcta').getBoundingClientRect();
          return box.left >= 0 && box.right <= innerWidth && box.bottom <= innerHeight && (!bar.height || box.bottom <= bar.top - 10);
        }), `${width} ${route}: WhatsApp safe position`);
        assert.equal(await page.locator('#i-google > g').getAttribute('transform'), 'translate(2.64 2.64) scale(.78)');
        assert.ok(await page.evaluate(() => [...document.querySelectorAll('script[type="application/ld+json"]')].every(script => {
          const data = JSON.parse(script.textContent), graph = data['@graph'] || [data];
          return graph.filter(item => item['@type'] === 'MovingCompany').every(item =>
            item.logo.url.endsWith('/img/logo/dereus-logo.svg') && item.logo.width === 1000 && item.logo.height === 828);
        })), `${route}: approved JSON-LD logo`);
        if (route === '/diensten/') {
          assert.equal(await page.locator('.b-dienstenpanelen__index').count(), 0);
          assert.equal(await page.locator('.b-dienstenpanelen__paneel').count(), 8);
          assert.ok(await page.locator('.b-dienstenpanelen__panelen').evaluate(el => {
            const box = el.getBoundingClientRect(); return Math.abs((box.left + box.right) / 2 - innerWidth / 2) < 2;
          }), `${width}: service panels centered without an empty sidebar`);
        }
        if (route === '/contact/' && width > 960) {
          assert.ok(await page.evaluate(() => Math.abs(document.querySelector('.b-kaart__beeld').getBoundingClientRect().top
            - document.querySelector('#kaart-kop').getBoundingClientRect().top) < 2), `${width}: map top aligns address heading`);
        }
        const heading = route === '/' ? '.hero__tekst' : '.pk__tekst';
        if (await page.locator(heading).count()) {
          assert.ok(await page.locator(heading).evaluate(el => {
            const r = el.getBoundingClientRect();
            return Math.abs((r.left + r.right) / 2 - innerWidth / 2) < 2;
          }), `${width} ${route}: header not centered`);
        }
        if (route === '/') {
          assert.ok(await page.locator('.hero__team').evaluate(el => {
            const r = el.getBoundingClientRect();
            const text = document.querySelector('.hero__tekst').getBoundingClientRect();
            return Math.abs((r.left + r.right) / 2 - innerWidth / 2) < 2 && r.top >= text.bottom;
          }), `${width}: workers not centered below heading`);
        }
      }
      console.log(`${width}px: ${routes.length} pagina's gecontroleerd`);
    }

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(base, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(out, 'home-desktop.png') });
    await page.locator('.header__cta').focus();
    assert.ok(await page.locator('.header__cta').evaluate(el => {
      const style = getComputedStyle(el); return style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) >= 2;
    }), 'Keyboard focus remains visible on green buttons');
    /* Submenu Diensten: de rubriekslink draagt de chevron en de ARIA. Er is geen
       schakelknop meer; het paneel komt bij hover en bij focus, klikken navigeert. */
    const sublink = page.locator('.nav__link--sub');
    assert.equal(await sublink.getAttribute('aria-controls'), 'menu-diensten');
    await sublink.focus();
    await page.waitForFunction(() => getComputedStyle(document.querySelector('.mega')).visibility === 'visible');
    assert.equal(await sublink.getAttribute('aria-expanded'), 'true', 'submenu opens on keyboard focus');
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.closest('.mega') !== null), true, 'submenu is reachable by keyboard');
    await page.screenshot({ path: path.join(out, 'menu-desktop.png') });
    await page.keyboard.press('Escape');
    assert.equal(await sublink.getAttribute('aria-expanded'), 'false', 'Escape closes the submenu');
    assert.equal(await sublink.evaluate(el => el === document.activeElement), true, 'Escape returns focus to the link');
    await page.waitForFunction(() => getComputedStyle(document.querySelector('.mega')).visibility === 'hidden');
    /* Na Escape mag Tab niet in het uitfadende paneel landen, dan valt de focus naar de body. */
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement !== document.body && document.activeElement.closest('.mega') === null), true, 'focus moves past the dismissed submenu');
    /* Hover opent het paneel ook, Escape sluit het weer. */
    await page.locator('.nav__item--sub').hover();
    await page.waitForFunction(() => getComputedStyle(document.querySelector('.mega')).visibility === 'visible');
    assert.equal(await sublink.getAttribute('aria-expanded'), 'true', 'submenu opens on hover');
    await page.keyboard.press('Escape');
    await page.waitForFunction(() => getComputedStyle(document.querySelector('.mega')).visibility === 'hidden');
    await page.mouse.move(5, 500);
    await sublink.blur();
    /* De chevron zit in de link: erop klikken gaat naar de dienstenpagina, het schakelt niet. */
    await Promise.all([page.waitForNavigation({ waitUntil: 'networkidle' }), page.locator('.nav__link--sub .ic').click()]);
    assert.equal(new URL(page.url()).pathname, '/diensten/', 'clicking the chevron opens the services page');
    await page.goto(base, { waitUntil: 'networkidle' });
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
    await page.locator('.hero').screenshot({ path: path.join(out, 'home-laptop.png') });
    await page.locator('#header-of-van').fill('Den Haag');
    await page.locator('#header-of-naar').fill('Delft');
    await page.locator('#header-of-dienst').selectOption('particulier');
    await page.locator('.of-box--header .of-knop').click();
    await page.waitForURL('**/offerte/?**');
    assert.equal(await page.locator('#f-van').inputValue(), 'Den Haag');
    assert.equal(await page.locator('#f-naar').inputValue(), 'Delft');
    assert.equal(await page.locator('#f-dienst').inputValue(), 'particulier');

    await page.goto(base, { waitUntil: 'networkidle' });
    for (const [id, field] of [['aanvraag', 'aanvraag-van'], ['contact-formulier', 'bericht-naam']]) {
      const form = page.locator(`#${id} form`);
      await form.locator('button[type=submit]').click();
      assert.equal(await page.locator(`#${field}`).getAttribute('aria-invalid'), 'true');
      assert.equal(await page.locator(`#${id} .b-formulier__foutlijst`).isVisible(), true);
    }
    for (const id of ['diensten', 'waarom', 'cijfers', 'werkwijze', 'over-ons', 'aanvraag', 'contact']) {
      const section = page.locator(`#${id}`);
      assert.equal(await section.count(), 1, `Missing restored section: ${id}`);
      await section.scrollIntoViewIfNeeded();
      await section.screenshot({ path: path.join(out, `${id}-desktop.png`), style: '.header, .mcta, .skiplink { visibility: hidden !important; }' });
    }
    assert.deepEqual(await page.evaluate(() => [...document.querySelectorAll('.beeldaccent')].flatMap(art => {
      if (getComputedStyle(art).display === 'none') return [];
      const box = art.getBoundingClientRect(), parent = art.parentElement.getBoundingClientRect();
      const failures = [];
      if (box.left < parent.left || box.right > parent.right || box.top < parent.top || box.bottom > parent.bottom) failures.push('accent outside photo');
      if (getComputedStyle(art).pointerEvents !== 'none' || art.getAttribute('aria-hidden') !== 'true') failures.push('interactive accent');
      const walker = document.createTreeWalker(art.closest('section'), NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        if (!node.textContent.trim() || node.parentElement.closest('script,style,svg,.vh')) continue;
        const range = document.createRange(); range.selectNodeContents(node);
        if ([...range.getClientRects()].some(r => r.width && r.height && r.left < box.right && r.right > box.left && r.top < box.bottom && r.bottom > box.top)) failures.push('accent crosses text');
      }
      return failures;
    })), [], 'Photo accents remain inside images and clear of text');
    await page.route('https://cdn.jsdelivr.net/**', route => route.abort());
    await page.route('https://cdnjs.cloudflare.com/**', route => route.abort());
    await page.locator('[data-wereld-start]').click();
    await page.waitForFunction(() => !document.querySelector('[data-wereld-melding]').classList.contains('vh'));
    assert.equal(await page.locator('.wereld__terugval').isVisible(), true);
    assert.equal(await page.locator('[data-wereld-start]').isEnabled(), true);

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(base + '/diensten/', { waitUntil: 'networkidle' });
    await page.locator('.b-dienstenpanelen').scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(out, 'diensten-desktop.png') });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(base + '/diensten/', { waitUntil: 'networkidle' });
    await page.locator('.b-dienstenpanelen').scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(out, 'diensten-mobile.png') });
    assert.deepEqual(errors, [], 'Browser errors');
    console.log('Navigatie, focus, afbeeldingen en browserconsole: akkoord.');
    console.log(`Screenshots: ${out}`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
