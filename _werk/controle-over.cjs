/* Controle van "Sterk waar het zwaar is" (blok over-ons): /over-ons/ #verhaal en de kopie op de home
   (#over-ons). Sinds 28-09-2026 het patroon about-address-team: de uitsnede staat met de kruin op de
   bovenrand van het podium en met de rechte snede op de onderrand van de platen, de platen beginnen op
   --over-plaat-top van de hoogte van de uitsnede. Sinds de tweede ronde (ook 28-09-2026) staat de tekst
   onder het beeld en lopen vijf feitenkaarten ernaast van de bovenrand van het beeld tot de onderrand van
   de tekst (vanaf 900 px; smaller volgen beeld, tekst en kaarten elkaar op in een kolom). Verder: de
   adresregel letterlijk, de hoverregels, dat hover niets verschuift, de kaarten zonder JS, en op de home
   geen voorwerp meer op de naad met het werkgebied.

   node _werk/controle-over.cjs [pad-naar-playwright] [basis-url] [--snel]
   Beide argumenten mogen weg: dan zoekt controle-kit.cjs Playwright zelf en start het een
   eigen server. Onder _werk/controle.cjs draait dit als module, op de gedeelde browser. */
const kit = require('./controle-kit.cjs');

const PLEKKEN = [['/over-ons/', 'verhaal'], ['/', 'over-ons']];
const KAARTEN = ['Vakmensen, geen studenten', 'Standaard verzekerd', 'Eén vaste verhuisadviseur', 'Geen voorrijkosten', '7 dagen per week bereikbaar'];
const ADRES = 'Hoofdkantoor: Lau Mazirellaan 336, Den Haag';

async function draai({ browser, basis, snel = false } = {}) {
  const { assert, omhul, meld, rapport } = kit.zacht('over');
  const breedtes = snel ? [1440, 390] : [1920, 1440, 1180, 1024, 1000, 960, 910, 900, 899, 768, 390, 320];

  for (const [route, id] of PLEKKEN) {
    for (const width of breedtes) {
      const page = kit.temmen(await browser.newPage({ viewport: { width, height: 900 }, reducedMotion: 'reduce' }));
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await omhul(`${route} ${width}px`, async () => {
        await page.goto(new URL(route, basis).href, { waitUntil: 'load' });
        const section = page.locator(`#${id}`);
        assert.equal(await section.count(), 1);
        assert.equal(await section.evaluate(el => el.classList.contains('b-over')), true, `${route}: #${id} is het blok over-ons`);
        await section.scrollIntoViewIfNeeded();
        // een lui beeld dat nooit laadt mag de controle niet laten hangen: hoogstens 5 s wachten
        await section.evaluate(el => { for (const i of el.querySelectorAll('img')) i.loading = 'eager'; });
        await section.evaluate(el => Promise.race([new Promise(r => setTimeout(r, 5000)),
          Promise.all([...el.querySelectorAll('img')].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))]));
        const m = await section.evaluate(el => {
          const r = s => el.querySelector(s).getBoundingClientRect();
          const podium = r('.over__podium'), platen = r('.over__platen'), team = r('.over__team'), kop = r('.over__kop'), rij = r('.over__rij'), links = r('.over__links');
          const lijst = el.querySelector('.over__kaarten'), kaarten = [...lijst.children];
          const img = el.querySelector('.over__team');
          const achter = new DOMMatrixReadOnly(getComputedStyle(el.querySelector('.over__platen'), '::before').transform);
          const offset = parseFloat(getComputedStyle(el).getPropertyValue('--over-offset')) * parseFloat(getComputedStyle(document.documentElement).fontSize);
          return {
            geladen: img.complete && img.naturalWidth > 0, alt: img.getAttribute('alt'),
            kruin: team.top - podium.top, snede: team.bottom - platen.bottom,
            plaatTop: (platen.top - team.top) / team.height,
            achterX: achter.e, achterY: achter.f, offset,
            lijstBoven: lijst.getBoundingClientRect().top - podium.top,
            lijstOnder: lijst.getBoundingClientRect().bottom - kop.bottom,
            naast: lijst.getBoundingClientRect().left >= links.right,
            tekstOnderBeeld: kop.top >= podium.bottom,
            onderTekst: lijst.getBoundingClientRect().top >= kop.bottom,
            kopLinks: kop.left - podium.left, podiumLinks: podium.left - rij.left,
            overloopKaart: kaarten.filter(k => k.scrollHeight > k.clientHeight + 1 || k.scrollWidth > k.clientWidth + 1).length,
            titels: kaarten.map(k => k.querySelector('h3').textContent.trim()),
            // sinds 28-09-2026 klei-iconen: geladen, en rechts vrij van de kop en de tekst van de kaart
            klei: kaarten.map(k => { const i = k.querySelector('.over__klei'); if (!i) return 'geen';
              const b = i.getBoundingClientRect(), t = k.querySelector('div').getBoundingClientRect();
              return !(i.complete && i.naturalWidth > 0) ? 'niet geladen' : b.right > t.left ? 'raakt de tekst' : 'goed'; }),
            adres: el.querySelector('.over__adres').textContent.trim(),
          };
        });
        assert.equal(m.geladen, true, `${width}: het teambeeld laadt`);
        assert.equal(m.alt, '', `${width}: het teambeeld is gegenereerd en claimt niet wie het zijn (alt leeg)`);
        assert.ok(Math.abs(m.kruin) <= 1, `${width}: de kruin staat op de bovenrand van het podium (${m.kruin.toFixed(1)}px)`);
        assert.ok(Math.abs(m.snede) <= 1, `${width}: de snede door de heupen valt op de onderrand van de platen (${m.snede.toFixed(1)}px)`);
        assert.ok(Math.abs(m.plaatTop - .23) < .01, `${width}: de platen beginnen op 23% van de uitsnede (${(m.plaatTop * 100).toFixed(1)}%)`);
        assert.ok(Math.abs(m.achterX + m.offset) < .5 && Math.abs(m.achterY + m.offset) < .5, `${width}: de achterste plaat staat --over-offset links boven de voorste (${m.achterX}, ${m.achterY})`);
        assert.equal(m.overloopKaart, 0, `${width}: geen tekst die uit een kaart loopt`);
        assert.deepEqual(m.titels, KAARTEN);
        assert.deepEqual(m.klei, KAARTEN.map(() => 'goed'), `${width}: elke kaart heeft een geladen klei-icoon naast de tekst`);
        assert.equal(m.adres, ADRES);
        assert.equal(m.tekstOnderBeeld, true, `${width}: de tekst staat onder het beeld`);
        assert.ok(Math.abs(m.kopLinks) <= 1, `${width}: de kop begint op dezelfde lijn als het podium (${m.kopLinks.toFixed(1)}px)`);
        if (width >= 900) {
          assert.equal(m.naast, true, `${width}: de kaarten staan naast beeld en tekst`);
          assert.ok(Math.abs(m.lijstBoven) <= 1, `${width}: de kaarten beginnen op de bovenrand van het beeld (${m.lijstBoven.toFixed(1)}px)`);
          // gelijke rijen: worden de kaarten hoger dan beeld plus tekst, dan groeit de rij en zakt deze onderrand
          assert.ok(Math.abs(m.lijstOnder) <= 1, `${width}: de kaarten eindigen op de onderrand van de tekst (${m.lijstOnder.toFixed(1)}px)`);
        } else {
          assert.equal(m.onderTekst, true, `${width}: de kaarten staan onder de tekst`);
          assert.ok(Math.abs(m.podiumLinks) <= 1, `${width}: het beeld begint op de lijn van de kolom (${m.podiumLinks.toFixed(1)}px)`);
        }
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${width}: geen horizontale overloop`);
        if (route === '/') {
          const voorwerp = await page.evaluate(() => getComputedStyle(document.querySelector('#over-ons + .b-werkgebied > .wrap'), '::before').content);
          assert.equal(voorwerp, 'none', `${width}: geen voorwerp meer op de naad met het werkgebied`);
        }
        assert.deepEqual(errors, []);
        meld(`${route} ${width}px: gecontroleerd`);
      });
      await page.close();
    }
  }

  const page = kit.temmen(await browser.newPage({ viewport: { width: 1440, height: 900 } }));
  await omhul('hover', async () => {
    await page.goto(new URL('/over-ons/', basis).href, { waitUntil: 'load' });
    // het recept uit section-library/about-address-team (de achterste plaat schuift verder, het icoon van
    // de aangewezen kaart 3px omhoog en 4 graden gekanteld) plus de tweede ronde: het beeld groeit vanaf
    // de snede en de rand van de kaart kleurt. Alleen met hover en zonder reduce.
    const regels = await page.evaluate(() => [...document.styleSheets].flatMap(sheet => {
      try { return [...sheet.cssRules]; } catch { return []; }
    }).filter(r => r instanceof CSSMediaRule && /hover:\s*hover/.test(r.conditionText) && /reduced-motion:\s*no-preference/.test(r.conditionText))
      .flatMap(r => [...r.cssRules]).filter(r => /over__/.test(r.selectorText) && /:hover/.test(r.selectorText))
      .map(r => [r.selectorText, r.style.transform || r.style.scale || r.style.opacity || r.style.getPropertyValue('--over-shift').trim()]));
    assert.deepEqual(regels, [['.over__podium:hover .over__platen', 'var(--over-offset-hover)'],
      ['.over__podium:hover .over__team', '1.02'],
      ['.over__kaart:hover::after', '1'],
      ['.over__kaart:hover .over__icoon', 'translateY(-3px) rotate(-4deg)']], 'hover volgt het patroon');
    // hover mag niets verschuiven: de vakken van rij, podium, tekst en kaarten blijven gelijk
    const vakken = () => page.evaluate(() => [...document.querySelectorAll('#verhaal .over__rij, #verhaal .over__podium, #verhaal .over__kop, #verhaal .over__kaart')]
      .map(e => { const b = e.getBoundingClientRect(); return [b.left + scrollX, b.top + scrollY, b.width, b.height].map(v => Math.round(v * 10) / 10).join(','); }));
    await page.locator('#verhaal').scrollIntoViewIfNeeded();
    await page.evaluate(() => { for (const e of document.querySelectorAll('#verhaal [data-reveal], #verhaal [data-reveal-groep] > *')) e.classList.add('in'); });
    await page.waitForTimeout(900);
    const rust = await vakken();
    await page.locator('#verhaal .over__podium').hover();
    await page.waitForTimeout(800);
    assert.equal(await page.locator('#verhaal .over__team').evaluate(e => getComputedStyle(e).scale), '1.02', 'het beeld groeit bij hover');
    assert.deepEqual(await vakken(), rust, 'hover op het beeld verschuift niets');
    await page.locator('#verhaal .over__kaart').nth(1).hover();
    await page.waitForTimeout(500);
    const rand = await page.locator('#verhaal .over__kaart').nth(1).evaluate(e => { const s = getComputedStyle(e, '::after'); return [s.opacity, s.boxShadow]; });
    assert.deepEqual(rand, ['1', 'rgb(23, 70, 162) 0px 0px 0px 2px inset'], 'de rand van de kaart verschijnt bij hover');
    assert.deepEqual(await vakken(), rust, 'hover op een kaart verschuift niets');
    meld('hover: gecontroleerd');
  });
  await page.close();

  const zonderJs = kit.temmen(await browser.newPage({ javaScriptEnabled: false, viewport: { width: 390, height: 900 } }));
  await omhul('zonder JavaScript', async () => {
    await zonderJs.goto(new URL('/over-ons/', basis).href, { waitUntil: 'load' });
    assert.equal(await zonderJs.locator('#verhaal .over__kaart').last().evaluate(el => getComputedStyle(el).opacity), '1', 'kaarten zichtbaar zonder JS');
    assert.equal(await zonderJs.locator('#verhaal .over__team').isVisible(), true);
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
