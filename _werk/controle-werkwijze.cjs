/* Controle van "Zo werkt het" op de home (#werkwijze, blok stapkaarten): de vijf stappen als kaarten, de
   lagen van het patroon steps-four-green (paneel, figuur op de paneelrand die boven de kaart uitkomt, het
   witte deel van de kaart onder de snijlijn, het klei-icoon dat de tekst vrijlaat, "Stap n" op het wit en niet
   meer over de figuur), de rijen per breedte, de knoppen na de kaarten, het
   hoverrecept, een ankerlink naar een stap en de pagina zonder JS.
   Sinds 28-09-2026 ("Home "Zo werkt het", routeband or option A (28-09-2026): A on Koningsblauw"); daarvoor
   stond hier de routeband (intro-route-band), en nog eerder de uitklapbare werkwijze. Beide blokken staan nog
   in _werk/blokken/, maar geen pagina gebruikt ze meer.

   node _werk/controle-werkwijze.cjs [pad-naar-playwright] [basis-url] [--snel]
   Beide argumenten mogen weg: dan zoekt controle-kit.cjs Playwright zelf en start het een
   eigen server. Onder _werk/controle.cjs draait dit als module, op de gedeelde browser. */
const path = require('node:path');
const kit = require('./controle-kit.cjs');

const UIT = path.resolve(__dirname, '../website/review/cleanup');

async function draai({ browser, basis, snel = false } = {}) {
  const { assert, omhul, meld, rapport } = kit.zacht('werkwijze');
  const breedtes = snel ? [1440, 390] : [1920, 1440, 1101, 1100, 1024, 900, 768, 701, 700, 390, 320];

  for (const width of breedtes) {
    const page = kit.temmen(await browser.newPage({ viewport: { width, height: 900 }, reducedMotion: 'reduce' }));
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await omhul(`${width}px`, async () => {
      await page.goto(basis, { waitUntil: 'load' });
      const section = page.locator('#werkwijze');
      assert.equal(await section.count(), 1);
      assert.deepEqual(await section.evaluate(el => ['b-stapkaarten', 'sectie--blauw'].map(k => el.classList.contains(k))), [true, true],
        'Zo werkt het is het blok stapkaarten op de Koningsblauwe band');
      assert.equal(await page.locator('.b-routeband').count(), 0, 'de routeband staat er niet meer');
      await section.scrollIntoViewIfNeeded();
      // de kaarten onder de vouw zijn lui: laad ze nu, en wacht hoogstens 5 s op een beeld dat nooit laadt
      await section.evaluate(el => { for (const i of el.querySelectorAll('img')) i.loading = 'eager';
        return Promise.race([new Promise(r => setTimeout(r, 5000)),
          Promise.all([...el.querySelectorAll('img')].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))]); });
      assert.deepEqual(await section.locator('.b-stapkaarten__stap').evaluateAll(items => items.map(el => el.id)),
        ['stap-1', 'stap-2', 'stap-3', 'stap-4', 'stap-5']);
      const m = await section.evaluate(el => {
        const r = e => e.getBoundingClientRect();
        // eerst alles meten, dan pas scrollen: tops tegen de lijst, want beelden boven de sectie laden onder het scrollen
        const lijst0 = r(el.querySelector('.b-stapkaarten__lijst'));
        const kaarten = [...el.querySelectorAll('.b-stapkaarten__stap')].map(li => {
          const kaart = r(li.querySelector('.b-stapkaarten__kaart')), paneel = r(li.querySelector('.b-stapkaarten__paneel'));
          const fig = r(li.querySelector('.b-stapkaarten__fig')), titel = r(li.querySelector('.b-stapkaarten__titel'));
          const foto = li.querySelector('.b-stapkaarten__foto'), klei = li.querySelector('.b-stapkaarten__klei');
          const kr = klei ? r(klei) : null, nr = r(li.querySelector('.b-stapkaarten__nr'));
          const over = (a, b) => a && b && Math.min(a.right, b.right) > Math.max(a.left, b.left) && Math.min(a.bottom, b.bottom) > Math.max(a.top, b.top);
          return { id: li.id, top: Math.round(kaart.top - lijst0.top), boven: kaart.top - fig.top, snede: fig.bottom - paneel.bottom,
            binnen: fig.left >= kaart.left - 1 && fig.right <= kaart.right + 1, titelVrij: titel.top >= paneel.bottom,
            geladen: foto.complete && foto.naturalWidth > 0,
            klei: !!klei && klei.complete && klei.naturalWidth > 0, kleiVrij: !!kr && kr.bottom <= nr.top && kr.left >= kaart.left,
            nrVrij: nr.width > 0 && nr.top >= paneel.bottom && nr.bottom <= titel.top && !over(nr, fig) && !over(nr, kr) };
        });
        const lijst = r(el.querySelector('.b-stapkaarten__lijst'));
        const knoppen = [...el.querySelectorAll('.b-stapkaarten__knoppen .knop')].map(r);
        const knoppenOnder = Math.min(...knoppen.map(k => k.top)) - lijst.bottom;
        // net onder de paneelrand, midden onder de figuur: het witte deel van de kaart, geen uitsnede of schaduw.
        // elementFromPoint ziet alleen wat in beeld is, dus per kaart eerst naar het midden van het scherm.
        [...el.querySelectorAll('.b-stapkaarten__stap')].forEach((li, i) => {
          li.scrollIntoView({ block: 'center' });
          const f = r(li.querySelector('.b-stapkaarten__fig')), p = r(li.querySelector('.b-stapkaarten__paneel'));
          const onder = document.elementFromPoint((f.left + f.right) / 2, p.bottom + 3);
          kaarten[i].onderIsKaart = !!onder && !!onder.closest('.b-stapkaarten__kaart') && !onder.closest('.b-stapkaarten__fig');
        });
        return { kaarten, knoppenOnder, knoppen: knoppen.length,
          cta: el.querySelectorAll('.knop--cta').length };
      });
      for (const k of m.kaarten) {
        assert.ok(k.boven >= 24, `${width}: ${k.id}: het hoofd komt boven de kaart uit (${Math.round(k.boven)}px)`);
        assert.ok(Math.abs(k.snede) <= 1, `${width}: ${k.id}: de snijlijn valt op de rand van het paneel (${k.snede.toFixed(1)}px)`);
        assert.ok(k.binnen, `${width}: ${k.id}: de figuur blijft binnen de kaart`);
        assert.ok(k.titelVrij, `${width}: ${k.id}: de titel staat onder het paneel`);
        assert.ok(k.geladen, `${width}: ${k.id}: het beeld is geladen`);
        assert.ok(k.onderIsKaart, `${width}: ${k.id}: onder de snijlijn ligt het wit van de kaart`);
        assert.ok(k.klei, `${width}: ${k.id}: het klei-icoon is geladen`);
        assert.ok(k.kleiVrij, `${width}: ${k.id}: het klei-icoon blijft boven de tekst en binnen de kaart`);
        assert.ok(k.nrVrij, `${width}: ${k.id}: "Stap n" staat op het wit tussen paneel en titel, los van figuur en klei`);
      }
      const tops = m.kaarten.map(k => k.top), rijen = new Set(tops).size;
      if (width > 1100) assert.equal(rijen, 1, `${width}: de vijf kaarten op een rij (tops ${tops.join(', ')})`);
      else if (width > 700) assert.ok(rijen === 2 && tops[2] === tops[0] && tops[3] > tops[0], `${width}: drie en twee kaarten (tops ${tops.join(', ')})`);
      else assert.ok(tops.every((t, i) => i === 0 || t > tops[i - 1]), `${width}: de kaarten onder elkaar (tops ${tops.join(', ')})`);
      assert.equal(m.knoppen, 2, `${width}: offerte en werkwijze onder de kaarten`);
      assert.equal(m.cta, 1, `${width}: een primaire knop in de sectie`);
      assert.ok(m.knoppenOnder > 0, `${width}: de knoppen staan na de kaarten`);
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${width}: geen horizontale overloop`);
      if (!snel && (width === 1440 || width === 390)) {
        await section.screenshot({ path: path.join(UIT, `werkwijze-stapkaarten-${width}.png`),
          style: '.header, .mcta, .whatsapp, .skiplink { visibility: hidden !important; }' });
      }
      await page.evaluate(() => { location.hash = 'stap-3'; });
      await page.waitForFunction(() => { const r = document.querySelector('#stap-3').getBoundingClientRect(); return r.top >= 0 && r.bottom <= innerHeight; });
      assert.deepEqual(errors, []);
      meld(`${width}px: gecontroleerd`);
    });
    await page.close();
  }

  const page = kit.temmen(await browser.newPage({ viewport: { width: 1440, height: 900 } }));
  await omhul('hover', async () => {
    await page.goto(basis, { waitUntil: 'load' });
    /* het recept uit section-library/steps-four-green: de kaart 4px omhoog, de pil 3px opzij, alleen met hover
       en zonder reduce. Met translate op de kaart binnen de li, want de li is het element van de reveal en
       diens transition (opacity, transform) zou een eigen transition daar overschrijven. */
    const regels = await page.evaluate(() => [...document.styleSheets].flatMap(sheet => {
      try { return [...sheet.cssRules]; } catch { return []; }
    }).filter(r => r instanceof CSSMediaRule && /hover:\s*hover/.test(r.conditionText) && /reduced-motion:\s*no-preference/.test(r.conditionText))
      .flatMap(r => [...r.cssRules]).filter(r => /b-stapkaarten__stap:hover/.test(r.selectorText)).map(r => r.style.translate));
    assert.deepEqual(regels, ['0px -4px', '3px'], 'hover van de kaarten volgt het patroon');
    const overgang = await page.locator('#werkwijze .b-stapkaarten__kaart').first().evaluate(el => getComputedStyle(el).transitionProperty);
    assert.ok(/translate/.test(overgang), `de kaart glijdt omhoog en springt niet (transition-property: ${overgang})`);
    meld('hover: gecontroleerd');
  });
  await page.close();

  const zonderJs = kit.temmen(await browser.newPage({ javaScriptEnabled: false, viewport: { width: 390, height: 900 } }));
  await omhul('zonder JavaScript', async () => {
    await zonderJs.goto(basis, { waitUntil: 'load' });
    assert.equal(await zonderJs.locator('#stap-5').evaluate(el => getComputedStyle(el).opacity), '1', 'stappen zichtbaar zonder JS');
    assert.equal(await zonderJs.locator('#stap-5 p').isVisible(), true);
    meld('zonder JavaScript: gecontroleerd');
  });
  await zonderJs.close();

  return rapport();
}

module.exports = { draai };

if (require.main === module) {
  (async () => {
    const args = kit.argumenten();
    const omgeving = await kit.opzet(args);
    try {
      const uitslag = await draai({ ...omgeving, snel: args.snel });
      process.exitCode = uitslag.fouten.length ? 1 : 0;
    } finally {
      await omgeving.op();
    }
  })().catch(error => { console.error(error); process.exitCode = 1; });
}
