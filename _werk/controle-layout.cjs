/* Controle van de gedeelde navigatie en de pagina's op desktop en mobiel.

   node _werk/controle-layout.cjs [pad-naar-playwright] [basis-url] [--snel]
   Beide argumenten mogen weg: dan zoekt controle-kit.cjs Playwright zelf en start het een
   eigen server. Onder _werk/controle.cjs draait dit als module, op de gedeelde browser.

   Dit is het net waarmee te zien is of parallelle sessies elkaar niet gesloopt hebben. Het
   loopt daarom alle breedtes en alle routes af voordat het een uitslag geeft: een run levert
   de hele lijst op, niet alleen de eerste fout. --snel doet 1440 en 390, voor tussendoor. */
const fs = require('node:fs');
const path = require('node:path');
const kit = require('./controle-kit.cjs');

const UIT = path.resolve(__dirname, '../website/review/cleanup');
const ROUTES = ['/', '/diensten/', '/kosten/', '/offerte/', '/contact/', '/over-ons/', '/werkwijze/',
  '/algemene-voorwaarden/', '/privacyverklaring/', '/offerte/bedankt/', '/contact/bedankt/', '/404.html'];
/* Testlijn test/diensten-paginas (29-09-2026): de acht secties van /diensten/ als eigen pagina
   (paginas/dienstpaginas.py). Sleutel van de sectie en adres, in de volgorde van /diensten/. */
const DIENSTPAGINAS = [['particulier', '/diensten/particuliere-verhuizingen/'], ['zakelijk', '/diensten/zakelijke-verhuizingen/'],
  ['nationaal', '/diensten/nationale-verhuizingen/'], ['internationaal', '/diensten/internationale-verhuizingen/'],
  ['verhuislift', '/diensten/verhuislift/'], ['opslag', '/diensten/tijdelijke-opslag/'], ['montage', '/diensten/montage/'],
  ['woningontruiming', '/diensten/woningontruiming/']];
ROUTES.push(...DIENSTPAGINAS.map(([, pad]) => pad));
const BREEDTES = [1440, 1100, 768, 390, 320];
const BREEDTES_SNEL = [1440, 390];

async function draai({ browser, basis, snel = false } = {}) {
  const { assert, omhul, meld, rapport } = kit.zacht('layout');
  const context = await browser.newContext({ reducedMotion: 'reduce' });
  const page = kit.temmen(await context.newPage());
  fs.mkdirSync(UIT, { recursive: true });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', response => {
    if (response.status() >= 400 && response.url().startsWith(basis)) errors.push(`${response.status()} ${response.url()}`);
  });

  /* Lui geladen beelden mogen na het scrollen nog even onderweg zijn. Eerst wachten tot ze
     klaar zijn, dan pas oordelen: anders hangt de uitslag aan de laadsnelheid in plaats van
     aan het pad, en dat gaf om de andere run een andere uitslag. Loopt de tijd af, dan zegt
     de assert hieronder alsnog wat er mis is. */
  const beeldenKlaar = kies => page.waitForFunction(
    s => [...document.querySelectorAll(s)].every(el => el.complete), kies, { timeout: 5000 }).catch(() => {});
  try {
    for (const width of (process.env.LAYOUT_INTERACTIES ? [] : (snel ? BREEDTES_SNEL : BREEDTES))) {
      await page.setViewportSize({ width, height: 900 });
      for (const route of ROUTES) {
        await omhul(`${width} ${route}`, async () => {
          await page.goto(basis + route, { waitUntil: 'load' });
          await page.evaluate(() => document.fonts.ready);
          const layout = await page.evaluate(() => {
            const header = document.querySelector('.header');
            const visible = [...header.querySelectorAll('a, button')].filter(el => el.getClientRects().length);
            return {
              width: document.documentElement.scrollWidth,
              viewport: innerWidth,
              /* Wie steekt er werkelijk buiten beeld? scrollWidth telt ook inhoud mee die een
                 voorouder netjes afsnijdt, en dat is bij ons juist de bedoeling: een uitsnede
                 stapt uit zijn kader en het kader knipt hem af. Zulke breedte is geen fout.
                 Een element dat tot aan de vensterrand doorloopt is dat wel, want daar hakt de
                 vensterrand de figuur doormidden. Die zoeken we hier op, en de breedste wint.
                 Dit draait alleen als er iets mis is, dus het kost niets in de schone gang. */
              overloop: (() => {
                if (document.documentElement.scrollWidth <= innerWidth + 1) return null;
                const knipt = el => /hidden|clip|auto|scroll/.test(getComputedStyle(el).overflowX);
                const noem = el => {
                  const klassen = [...el.classList].map(klasse => '.' + klasse).join('');
                  const bron = el.tagName === 'IMG' ? ' ' + (el.currentSrc || el.src || '').split('/').pop() : '';
                  return el.tagName.toLowerCase() + klassen + bron;
                };
                let ergste = null;
                for (const el of document.querySelectorAll('body *')) {
                  const box = el.getBoundingClientRect();
                  if (!box.width || box.right <= innerWidth + 1) continue;
                  let afgesneden = false, eerste = null;
                  for (let ouder = el.parentElement; ouder && ouder !== document.body; ouder = ouder.parentElement) {
                    if (!eerste && ouder.classList.length) eerste = noem(ouder);
                    /* Knipt een voorouder, dan is dit element niet de schuldige. Steekt die voorouder
                       zelf ook buiten beeld, dan komt hij in deze zelfde ronde langs en wordt hij
                       gemeld; we hoeven hem hier dus niet apart te vangen. */
                    if (knipt(ouder)) { afgesneden = true; break; }
                  }
                  if (afgesneden) continue;
                  const over = Math.round(box.right - innerWidth);
                  if (!ergste || over > ergste.over) ergste = { naam: noem(el), over, breed: Math.round(box.width), ouder: eerste || 'body' };
                }
                return ergste;
              })(),
              headerOverflow: visible.some(el => el.getBoundingClientRect().right > innerWidth + 1),
              broken: [...document.images].filter(img => img.complete && !img.naturalWidth).map(img => img.src),
              duplicateIds: [...document.querySelectorAll('[id]')].map(el => el.id).filter((id, i, ids) => ids.indexOf(id) !== i),
              brokenLabels: [...document.querySelectorAll('label[for]')].filter(el => !document.getElementById(el.htmlFor)).map(el => el.htmlFor),
              brokenAria: [...document.querySelectorAll('[aria-controls],[aria-labelledby],[aria-describedby]')].flatMap(el =>
                ['aria-controls', 'aria-labelledby', 'aria-describedby'].flatMap(attr => (el.getAttribute(attr) || '').split(/\s+/).filter(id => id && !document.getElementById(id)))),
              h1: document.querySelectorAll('h1').length
            };
          });
          /* De melding noemt de schuldige. De naam van het element dat scrollWidth oprekt is niet
             vanzelf de naam van het element dat de fout maakt, en op die verwarring is eerder een
             halve dag weggelopen. De grens zelf blijft staan: hier niets oprekken om groen te
             worden, want juist het onzichtbare geval telt. De pagina schuift dan niet, maar de
             figuur wordt wel door de vensterrand doorgesneden. */
          assert.ok(layout.width <= layout.viewport + 1,
            `${width} ${route}: overflow ${layout.width} bij venster ${layout.viewport}. ${layout.overloop
              ? `${layout.overloop.naam} steekt ${layout.overloop.over}px buiten beeld (breed ${layout.overloop.breed}, in ${layout.overloop.ouder})`
              : 'geen enkel element steekt rechts ongeknipt buiten beeld, kijk naar de linkerrand of naar de wortel zelf'}`);
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
          /* WhatsApp naast een telefoonnummer is sinds 23-09-2026 een richtlijn en geen harde eis.
             De gebruiker: "remove the rule of always whatsapp by phone number, make it a guidance
             instead." De standaard blijft: ctx.contactlinks() hangt achter elk nummer een knop.
             Een tel-link met data-geen-whatsapp is een bewuste uitzondering in de bron en telt
             niet mee. Een nummer zonder knop wordt als richtlijn gemeld en laat de run niet
             vallen. Wel hard: een knop die er staat maar dubbel is of onveilig een tab opent. */
          const koppels = await page.evaluate(() => {
            const hard = [], richtlijn = [];
            const visible = el => !!el.getClientRects().length && getComputedStyle(el).visibility !== 'hidden';
            const waar = tel => `#${tel.closest('[id]')?.id || '?'}`;
            for (const tel of document.querySelectorAll('a[href="tel:+31850005647"]')) {
              if (tel.hasAttribute('data-geen-whatsapp')) continue;
              const wa = tel.nextElementSibling;
              if (!wa || wa.href !== 'https://wa.me/31850005647' || !wa.hasAttribute('data-whatsapp-business')) {
                richtlijn.push(`${waar(tel)}: nummer zonder WhatsApp-knop`);
                continue;
              }
              if (wa.nextElementSibling?.hasAttribute('data-whatsapp-business')) hard.push('Duplicate WhatsApp alternative');
              else if (wa.target === '_blank' && !wa.rel.includes('noopener')) hard.push('Unsafe new tab');
              else if (visible(tel) && !visible(wa)) richtlijn.push(`${waar(tel)}: nummer zichtbaar, WhatsApp-knop niet`);
            }
            return { hard, richtlijn };
          });
          assert.deepEqual(koppels.hard, [], `${width} ${route}: paired business phone contacts`);
          for (const r of koppels.richtlijn) meld(`richtlijn ${width} ${route}: ${r}`);
          /* Een CTA moet als knop leesbaar blijven: groot genoeg om te raken, geen kaderrand, en
             niet ingedrukt of uitgeschakeld ogend. De eerste versie verwierp elke inset-schaduw en
             dat is te bot: een lichte inset van 1px is een glansrandje dat een knop juist verhoogd
             laat lijken, terwijl een donkere inset hem ingedrukt maakt. We kijken daarom naar wat
             de laag doet in plaats van naar het woord inset: hoeveel donkerder maakt hij de knop.
             De ingedrukte stand mag een donkere inset hebben; die meet dit niet, want
             getComputedStyle geeft hier de ruststand. */
          assert.deepEqual(await page.locator('.knop--cta').evaluateAll(items => {
            const lagen = waarde => {                       // splitsen op komma's buiten haakjes
              const uit = []; let diep = 0, nu = '';
              for (const teken of waarde) {
                if (teken === '(') diep++;
                else if (teken === ')') diep--;
                else if (teken === ',' && !diep) { uit.push(nu.trim()); nu = ''; continue; }
                nu += teken;
              }
              if (nu.trim()) uit.push(nu.trim());
              return uit;
            };
            const verduistering = laag => {                 // 0 = laat de knop licht, 1 = maakt hem zwart
              const kleur = laag.match(/rgba?\(([^)]+)\)/);
              if (!kleur) return 0;
              const [r, g, b, a = 1] = kleur[1].split(',').map(Number);
              return (1 - (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255) * a;
            };
            return items.filter(el => el.getClientRects().length).flatMap(el => {
              const style = getComputedStyle(el), box = el.getBoundingClientRect(), redenen = [];
              if (box.height < 44) redenen.push(`hoogte ${Math.round(box.height)}px`);
              if (parseFloat(style.borderTopWidth) > 1) redenen.push(`rand ${style.borderTopWidth}`);
              for (const laag of lagen(style.boxShadow)) {
                if (laag.includes('inset') && verduistering(laag) > 0.12) redenen.push(`donkere inset ${laag}`);
              }
              return redenen.length ? [`${el.className}: ${redenen.join('; ')}`] : [];
            });
          }), [], `${width} ${route}: clean CTA styling and touch size`);
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
            /* Sinds 28-09-2026 is elke dienst een eigen sectie direct in <main>, met het dienst-id als anker
               en de h2 als naam (acht regio's). De oude vorm, acht <article>-panelen in een sectie, mag niet
               half blijven staan. */
            assert.deepEqual(await page.locator('main > section.b-dienstenpanelen').evaluateAll(els => els.map(el => {
              const kop = document.getElementById(el.getAttribute('aria-labelledby'));
              return `${el.id}:${kop && el.contains(kop) && kop.tagName === 'H2' ? 'h2' : 'geen naam'}`;
            })), ['particulier', 'zakelijk', 'nationaal', 'internationaal', 'verhuislift', 'opslag', 'montage', 'woningontruiming'].map(id => `${id}:h2`),
            `${width}: eight service sections with their own anchor and name`);
            assert.equal(await page.locator('main article').count(), 0, `${width}: no article panels left`);
            assert.deepEqual(await page.locator('.b-dienstenpanelen__paneel').evaluateAll(els => els.filter(el => {
              const box = el.getBoundingClientRect(); return Math.abs((box.left + box.right) / 2 - innerWidth / 2) >= 2;
            }).length), 0, `${width}: service panels centered without an empty sidebar`);
            /* Sinds 28-09-2026 heeft elke dienst een eigen patroon uit ../section-library (VORMEN in
               blokken/dienstenpanelen.py), als data-vorm op de sectie: acht secties, acht verschillende vormen. */
            const vormen = await page.locator('main > section.b-dienstenpanelen').evaluateAll(els => els.map(el => el.dataset.vorm || ''));
            assert.ok(vormen.every(Boolean) && new Set(vormen).size === 8, `${width}: eight service sections, eight different patterns (${vormen.join(', ')})`);
          }
          const dienstpagina = DIENSTPAGINAS.find(([, pad]) => pad === route);
          if (dienstpagina) {
            /* Een dienstpagina is een sectie van /diensten/: een H1, dan precies die ene sectie met haar eigen
               anker, patroon en H2, en die kop linkt niet naar de pagina zelf. */
            assert.equal(await page.locator('h1').count(), 1, `${width} ${route}: one h1`);
            assert.deepEqual(await page.locator('main > section.b-dienstenpanelen').evaluateAll(els => els.map(el => {
              const kop = document.getElementById(el.getAttribute('aria-labelledby'));
              return `${el.id}:${kop && el.contains(kop) && kop.tagName === 'H2' ? 'h2' : 'geen naam'}:${el.dataset.vorm ? 'vorm' : 'geen vorm'}`;
            })), [`${dienstpagina[0]}:h2:vorm`], `${width} ${route}: the one service section with its anchor, name and pattern`);
            assert.equal(await page.locator(`main a[href="${route}"]`).count(), 0, `${width} ${route}: no link to itself in main`);
          }
          /* De kaart op /contact/ begint op de regel van de kop. Sinds de samenvoeging van 8971f9e (29-09-2026) weer
             het blok kaart, de vorm van het werkgebied met haar speld en klok: .wg__kaartvlak, boven 1060. Van de
             ochtend van 29-09-2026 tot die samenvoeging haar oudere kaart (blok kaart-tugche, .b-kaart__beeld, boven
             960, zoals in haar controle van 9dbb9a8); de controle volgt het blok dat er staat. */
          const kaartBeeld = route === '/contact/' && await page.locator('.b-kaart__beeld').count()
            ? ['.b-kaart__beeld', 960] : ['.b-kaart .wg__kaartvlak', 1060];
          if (route === '/contact/' && width > kaartBeeld[1]) {
            assert.ok(await page.evaluate(kies => Math.abs(document.querySelector(kies).getBoundingClientRect().top
              - document.querySelector('#kaart-kop').getBoundingClientRect().top) < 2, kaartBeeld[0]), `${width}: map top aligns address heading`);
          }
          if (route === '/werkwijze/') {
            /* De stappen. Sinds de samenvoeging van 28-09-2026 de trap van Tugche (blok tijdlijn: "Die van Tugche:
               1. /werkwijze/ #stappen (tijdlijn)", "with new clay icons"); daarvoor de stapkaarten (optie A
               steps-four-green), die in werkwijze.py als regel om terug te wisselen staan. De controle volgt het
               blok dat er staat. De ankers stap-1 tot stap-5 blijven, want daar kan van buiten naar gelinkt worden.
               De vorige vormen mogen niet half blijven staan: dat is de manier waarop zo'n vervanging stilletjes
               misgaat. */
            await page.locator('#stappen').scrollIntoViewIfNeeded();
            if (await page.locator('#stappen.b-stappentrap').count()) {
              /* Sinds de samenvoeging van 8971f9e (29-09-2026) de trap van Tugche in drie stappen (blok stappentrap:
                 "de klant vond vijf stappen te veel, drie leest rustiger"). Dus drie ankers, stap-1 tot stap-3; naar
                 stap-4 en stap-5 linkt niets. Een knop in de sectie, en de figuren en klei-iconen moeten er echt zijn. */
              assert.equal(await page.locator('.b-stappenlang, .b-tijdlijn, .b-stapkaarten').count(), 0,
                `${width}: de stappenrail, de tijdlijn of de stapkaarten staan er nog`);
              assert.deepEqual(await page.locator('#stappen .b-stappentrap__kaart').evaluateAll(items => items.map(el => el.id)),
                ['stap-1', 'stap-2', 'stap-3'], `${width}: de drie kaarten en hun ankers`);
              assert.equal(await page.locator('#stappen .knop--cta').count(), 1, `${width}: een primaire knop in de sectie`);
              await page.locator('#stappen img').evaluateAll(els => els.forEach(el => { el.loading = 'eager'; }));
              await beeldenKlaar('#stappen img');
              assert.deepEqual(await page.locator('#stappen img').evaluateAll(els => els
                .filter(el => !el.complete || !el.naturalWidth).map(el => el.getAttribute('src'))), [],
                `${width}: figuren en klei-iconen van de trap geladen`);
            } else if (await page.locator('#stappen.b-tijdlijn').count()) {
              assert.equal(await page.locator('.b-stappenlang, .b-stapkaarten').count(), 0, `${width}: de stappenrail of de stapkaarten staan er nog`);
              assert.deepEqual(await page.locator('#stappen .b-tijdlijn__stap').evaluateAll(items => items.map(el => el.id)),
                ['stap-1', 'stap-2', 'stap-3', 'stap-4', 'stap-5'], `${width}: de vijf treden en hun ankers`);
              assert.equal(await page.locator('#stappen .knop--cta').count(), 1, `${width}: een primaire knop in de sectie`);
              /* Stap 1 noemt het nummer zonder WhatsApp-knop ernaast (23-09-2026, data-geen-whatsapp). */
              assert.deepEqual(await page.evaluate(() => [document.querySelectorAll('#stap-1 a[href^="tel:"][data-geen-whatsapp]').length,
                document.querySelectorAll('#stap-1 .wa-link').length]), [1, 0], `${width}: stap 1 heeft het nummer zonder WhatsApp-knop`);
              /* Het klei-icoon (sinds de samenvoeging, in plaats van de 3D-render) komt boven de plaat uit en mag de
                 tekst niet afdekken. Zakt het terug achter de plaatrand of laadt het niet, dan is de vorm weg zonder
                 dat er iets stuk lijkt. De iconen onder de vouw zijn lui: laad ze eerst. */
              await page.locator('#stappen .b-tijdlijn__obj, #stappen .b-tijdlijn__team').evaluateAll(els => els.forEach(el => { el.loading = 'eager'; }));
              await beeldenKlaar('#stappen .b-tijdlijn__obj, #stappen .b-tijdlijn__team');
              assert.deepEqual(await page.locator('#stappen .b-tijdlijn__stap').evaluateAll(items => items.flatMap(el => {
                const img = el.querySelector('.b-tijdlijn__obj');
                if (!img || !img.complete || !img.naturalWidth) return [`${el.id}: klei-icoon niet geladen`];
                if (!img.getAttribute('src').startsWith('/img/clay/')) return [`${el.id}: geen klei-icoon maar ${img.getAttribute('src')}`];
                const obj = img.getBoundingClientRect();
                const plaat = el.querySelector('.b-tijdlijn__plaat').getBoundingClientRect();
                const fout = [];
                if (obj.top >= plaat.top - 4) fout.push(`${el.id}: klei-icoon steekt niet boven de plaat uit`);
                for (const naam of ['nr', 'titel']) {
                  const t = el.querySelector(`.b-tijdlijn__${naam}`).getBoundingClientRect();
                  if (obj.right > t.left && obj.left < t.right && obj.top < t.bottom && obj.bottom > t.top) {
                    fout.push(`${el.id}: klei-icoon ligt over ${naam}`);
                  }
                }
                return fout;
              })), [], `${width}: klei-iconen geladen, boven de plaatrand en vrij van de tekst`);
              assert.ok(await page.locator('#stappen .b-tijdlijn__team').evaluate(el => el.complete && el.naturalWidth > 0),
                `${width}: het team op de gele trede is geladen`);
              /* De WhatsApp-knop komt van ctx.contactlinks en landt in "Wat u doet"; hij mag de kolom ernaast
                 niet raken (controle van Tugche, origin/main 9dbb9a8). */
              assert.deepEqual(await page.evaluate(() => [...document.querySelectorAll('.b-tijdlijn__duo .wa-link')].flatMap(wa => {
                const box = wa.getBoundingClientRect();
                const buur = wa.closest('.b-tijdlijn__wie').nextElementSibling?.querySelector('dd');
                if (!buur) return [];
                const t = buur.getBoundingClientRect();
                return box.right > t.left && box.left < t.right && box.top < t.bottom && box.bottom > t.top
                  ? [`WhatsApp-knop overlapt "${buur.textContent.slice(0, 30)}..."`] : [];
              })), [], `${width}: WhatsApp-knop vrij van de kolom ernaast`);
              /* De vorm van de trap: breed vijf treden op een rij, onderaan gelijk en van links naar rechts hoger;
                 tot 1180 drie en twee per rij (onderaan gelijk per rij); tot 760 onder elkaar. Tops tegen de lijst,
                 zodat beelden die erboven nog laden de meting niet verschuiven. */
              const treden = await page.locator('#stappen .b-tijdlijn__stap').evaluateAll(items => items.map(el => {
                const r = el.getBoundingClientRect(), o = el.closest('.b-tijdlijn__trap').getBoundingClientRect();
                return [Math.round(r.top - o.top), Math.round(r.bottom - o.top)];
              }));
              const tops = treden.map(v => v[0]), bodems = treden.map(v => v[1]);
              if (width > 1180) {
                assert.ok(Math.max(...bodems) - Math.min(...bodems) <= 2 && tops.every((v, i) => i === 0 || v < tops[i - 1]),
                  `${width}: vijf treden op een rij die van links naar rechts oplopen (tops ${tops.join(', ')}, bodems ${bodems.join(', ')})`);
              } else if (width > 760) {
                assert.ok(Math.max(...bodems.slice(0, 3)) - Math.min(...bodems.slice(0, 3)) <= 2 && Math.abs(bodems[3] - bodems[4]) <= 2
                  && bodems[3] > bodems[0] + 2, `${width}: drie en twee treden per rij (bodems ${bodems.join(', ')})`);
              } else {
                assert.ok(tops.every((v, i) => i === 0 || v > tops[i - 1]), `${width}: de treden horen onder elkaar (tops ${tops.join(', ')})`);
              }
            } else {
              assert.equal(await page.locator('.b-stappenlang, .b-tijdlijn').count(), 0, `${width}: de stappenrail of de tijdlijn staat er nog`);
              assert.deepEqual(await page.locator('#stappen .b-stapkaarten__stap').evaluateAll(items => items.map(el => el.id)),
                ['stap-1', 'stap-2', 'stap-3', 'stap-4', 'stap-5'], `${width}: de vijf kaarten en hun ankers`);
              assert.equal(await page.locator('#stappen .knop--cta').count(), 1, `${width}: een primaire knop in de sectie`);
              /* Wat u doet en wat wij doen staan open op de kaart: geen uitklap meer, dus openen en sluiten
                 kan niets verschuiven. */
              assert.equal(await page.locator('#stappen details').count(), 0, `${width}: geen uitklap in de stappen`);
              assert.deepEqual(await page.locator('#stappen .b-stapkaarten__duo').evaluateAll(dls => dls.map(dl => dl.querySelectorAll('dt').length)),
                [2, 2, 2, 2, 2], `${width}: elke kaart heeft wat u doet en wat wij doen`);
              /* Stap 1 noemt het nummer zonder WhatsApp-knop ernaast (23-09-2026, data-geen-whatsapp). */
              assert.deepEqual(await page.evaluate(() => [document.querySelectorAll('#stap-1 a[href^="tel:"][data-geen-whatsapp]').length,
                document.querySelectorAll('#stap-1 .wa-link').length]), [1, 0], `${width}: stap 1 heeft het nummer zonder WhatsApp-knop`);
              // de kaarten onder de vouw zijn lui; laad ze nu, anders telt een beeld dat nog niet gevraagd is als kapot
              await page.locator('#stappen .b-stapkaarten__foto, #stappen .b-stapkaarten__klei').evaluateAll(els => els.forEach(el => { el.loading = 'eager'; }));
              await beeldenKlaar('#stappen .b-stapkaarten__foto, #stappen .b-stapkaarten__klei');
              /* De figuur staat op de onderrand van het paneel (daar is hij afgesneden) en komt met het hoofd
                 boven de kaart uit; zakt hij terug of schuift hij onder de rand door, dan is de snijlijn te zien
                 of de vorm weg zonder dat er iets stuk lijkt. En het beeld moet er echt zijn. Het klei-icoon
                 (sinds 28-09-2026) hangt onder de paneelrand, maar mag de tekst eronder niet raken. */
              assert.deepEqual(await page.locator('#stappen .b-stapkaarten__stap').evaluateAll(items => items.flatMap(el => {
                const fig = el.querySelector('.b-stapkaarten__fig').getBoundingClientRect();
                const paneel = el.querySelector('.b-stapkaarten__paneel').getBoundingClientRect();
                const kaart = el.querySelector('.b-stapkaarten__kaart').getBoundingClientRect();
                const foto = el.querySelector('.b-stapkaarten__foto');
                const fout = [];
                if (fig.top > kaart.top - 24) fout.push(`${el.id}: figuur komt niet boven de kaart uit`);
                if (Math.abs(fig.bottom - paneel.bottom) > 1) fout.push(`${el.id}: figuur staat niet op de rand van het paneel`);
                if (fig.left < kaart.left - 1 || fig.right > kaart.right + 1) fout.push(`${el.id}: figuur steekt buiten de kaart`);
                if (!foto.complete || !foto.naturalWidth) fout.push(`${el.id}: beeld niet geladen`);
                const klei = el.querySelector('.b-stapkaarten__klei');
                if (!klei || !klei.complete || !klei.naturalWidth) fout.push(`${el.id}: klei-icoon niet geladen`);
                else if (klei.getBoundingClientRect().bottom > el.querySelector('.b-stapkaarten__nr').getBoundingClientRect().top)
                  fout.push(`${el.id}: klei-icoon raakt de tekst`);
                /* "Stap n" staat sinds 28-09-2026 op het wit tussen paneel en titel, niet meer als pil over de figuur */
                const nr = el.querySelector('.b-stapkaarten__nr').getBoundingClientRect(), titel = el.querySelector('.b-stapkaarten__titel').getBoundingClientRect();
                const over = (a, b) => Math.min(a.right, b.right) > Math.max(a.left, b.left) && Math.min(a.bottom, b.bottom) > Math.max(a.top, b.top);
                if (!nr.width || nr.top < paneel.bottom || nr.bottom > titel.top || over(nr, fig) || over(nr, klei.getBoundingClientRect()))
                  fout.push(`${el.id}: "Stap n" ligt niet vrij tussen paneel en titel`);
                return fout;
              })), [], `${width}: figuren op de paneelrand, boven de kaart uit en geladen`);
              // tops tegen de lijst: beelden boven de sectie die nog laden verschuiven de pagina, niet de rijen
              const kaarten = await page.locator('#stappen .b-stapkaarten__stap').evaluateAll(items =>
                items.map(el => Math.round(el.getBoundingClientRect().top - el.parentElement.getBoundingClientRect().top)));
              const rijen = [...new Set(kaarten)].length;
              if (width > 1100) {
                assert.equal(rijen, 1, `${width}: de vijf kaarten horen op een rij (tops ${kaarten.join(', ')})`);
              } else if (width > 700) {
                assert.ok(rijen === 2 && kaarten[2] === kaarten[0] && kaarten[3] > kaarten[0],
                  `${width}: drie en twee kaarten (tops ${kaarten.join(', ')})`);
              } else {
                assert.ok(kaarten.every((top, i) => i === 0 || top > kaarten[i - 1]),
                  `${width}: de kaarten horen onder elkaar (tops ${kaarten.join(', ')})`);
              }
            }
            /* De voorbereiding (blok lijstplaat, sinds ronde 6) verving de witte checklistkaart. Het blok
               checklist bestaat nog, voor de dienst- en landpagina's, maar staat sinds ronde 6 niet meer op
               deze pagina; de regel bij #na-de-verhuizing hieronder telt dat er nergens meer een staat. */
            await page.locator('#voorbereiding').scrollIntoViewIfNeeded();
            /* Sinds de samenvoeging van 28-09-2026 de Goudgele plaat van Tugche (blok lijstplaat-geel: "Die van Tugche:
               2. /werkwijze/ #voorbereiding (gele lijstplaat)"); de Koningsblauwe lijstplaat staat in werkwijze.py als
               regel om terug te wisselen. Beide hebben dezelfde opbouw onder een eigen voorvoegsel. */
            const lp = await page.locator('#voorbereiding.b-lijstplaat-geel').count() ? 'b-lijstplaat-geel' : 'b-lijstplaat';
            assert.equal(await page.locator('#voorbereiding .b-checklist__kaart').count(), 0,
              `${width}: de oude checklistkaart staat nog in de voorbereiding`);
            assert.equal(await page.locator(`.${lp}__lijst > li`).count(), 6, `${width}: de zes punten van het lijstje`);
            if (lp === 'b-lijstplaat-geel') {
              /* De foto en de uitsnede van de verhuizer die eruit leunt (controle van Tugche, origin/main 9dbb9a8): een
                 pad dat verschuift laat een lege plaat of een verhuizer zonder hoofd achter. Foto en uitsnede moeten
                 even groot zijn, anders liggen ze niet op elkaar (zie UITSNEDE in lijstplaat-geel.py). En het
                 voorwerp op de plaatrand is een klei-icoon (sinds de samenvoeging). */
              await beeldenKlaar('.b-lijstplaat-geel__podium img, .b-lijstplaat-geel__klembord');
              assert.deepEqual(await page.locator('.b-lijstplaat-geel__podium img').evaluateAll(els => els.map(el =>
                el.complete && el.naturalWidth > 0 ? `${el.className} ${el.naturalWidth}x${el.naturalHeight}` : `${el.className} niet geladen`)),
                ['b-lijstplaat-geel__uit 1200x1030', 'b-lijstplaat-geel__foto 1200x1030', 'b-lijstplaat-geel__voor 1200x1030'],
                `${width}: foto en uitsnede van de verhuizer zijn geladen en even groot`);
              assert.ok(await page.locator('.b-lijstplaat-geel__klembord').evaluate(el => el.complete && el.naturalWidth > 0
                && el.getAttribute('src').startsWith('/img/clay/')), `${width}: het klei-icoon op de plaatrand is geladen`);
            } else {
              /* Sinds 29-09-2026 leunt de verhuizer ook uit de blauwe plaat (zelfde opbouw als lijstplaat-geel): foto
                 en uitsnede moeten geladen en even groot zijn, anders liggen ze niet op elkaar (UITSNEDE in lijstplaat.py). */
              await beeldenKlaar('.b-lijstplaat__podium img');
              assert.deepEqual(await page.locator('.b-lijstplaat__podium img').evaluateAll(els => els.map(el =>
                el.complete && el.naturalWidth > 0 ? `${el.className} ${el.naturalWidth}x${el.naturalHeight}` : `${el.className} niet geladen`)),
                ['b-lijstplaat__uit 1200x1030', 'b-lijstplaat__foto 1200x1030', 'b-lijstplaat__voor 1200x1030'],
                `${width}: foto en uitsnede van de verhuizer zijn geladen en even groot`);
            }
            /* Wat boven het kader uitsteekt (zijn hoofd en opgeheven hand: bron x 626 tot 966, vanaf y 218 in de
               1200x1030 uitsnede) mag "Uw lijstje" niet raken. Op 1001 viel zijn hoofd over de laatste letter
               voordat de rugmarge in lijstplaat.css ging wijken. */
            assert.deepEqual(await page.evaluate(lp => {
              const kop = document.querySelector(`.${lp}__lijstkop`), im = document.querySelector(`.${lp}__voor`);
              const kader = document.querySelector(`.${lp}__beeld`).getBoundingClientRect();
              const r = document.createRange(); r.selectNodeContents(kop); const tekst = r.getBoundingClientRect();
              const b = im.getBoundingClientRect(), s = b.height / 1030;
              const uit = { l: b.left + 626 * s, t: b.top + 218 * s, r: b.left + 966 * s, b: kader.top };
              const raakt = tekst.right > uit.l - 4 && tekst.bottom > uit.t - 4 && tekst.left < uit.r && tekst.top < uit.b;
              return raakt ? [`tekst ${Math.round(tekst.left)}-${Math.round(tekst.right)} x ${Math.round(tekst.top)}-${Math.round(tekst.bottom)}`,
                `verhuizer ${Math.round(uit.l)}-${Math.round(uit.r)} x ${Math.round(uit.t)}-${Math.round(uit.b)}`] : [];
            }, lp), [], `${width}: de verhuizer steekt over "Uw lijstje"`);
            /* Zelfde val als bij de tijdlijn: het klembord steekt boven de plaatrand uit en mag de lijstkop
               en de eerste regel niet afdekken. Het staat rechtsboven, de lijstkop links, en die twee
               kwamen op smal scherm tegen elkaar aan. */
            assert.deepEqual(await page.evaluate(lp => {
              const obj = document.querySelector(`.${lp}__klembord`).getBoundingClientRect();
              const plaat = document.querySelector(`.${lp}__plaat`).getBoundingClientRect();
              const fout = [];
              if (obj.top >= plaat.top - 4) fout.push('klembord steekt niet boven de plaat uit');
              for (const kies of [`.${lp}__lijstkop`, `.${lp}__lijst > li`]) {
                const t = document.querySelector(kies).getBoundingClientRect();
                if (obj.right > t.left && obj.left < t.right && obj.top < t.bottom && obj.bottom > t.top) {
                  fout.push(`klembord ligt over ${kies}`);
                }
              }
              /* en de foto mag niet over de lijst heen vallen als de kolommen krap worden */
              const foto = document.querySelector(`.${lp}__beeld`).getBoundingClientRect();
              const lijst = document.querySelector(`.${lp}__lijst`).getBoundingClientRect();
              if (foto.right > lijst.left + 1 && foto.left < lijst.right - 1
                && foto.top < lijst.bottom - 1 && foto.bottom > lijst.top + 1) fout.push('foto ligt over de lijst');
              return fout;
            }, lp), [], `${width}: klembord boven de plaatrand, foto en tekst vrij van elkaar`);
            /* Het gereedschap op de naad met de tijdlijn (optie A, 23-09-2026) is een ::before op de wrap
               en rekent vanaf de sectie. Op de telefoon loopt de kop over de volle breedte en staat het
               voorwerp er rechts boven; het mag de letters van de label en de kop niet raken. Gemeten op
               de tekst zelf (Range), niet op het blok, want dat loopt altijd door tot de rechterrand.
               De CSS zet het alleen na de tijdlijn of de stapkaarten; na de stappentrap (8971f9e) is er geen. */
            assert.deepEqual(await page.evaluate(lp => {
              if (!document.querySelector('#stappen:is(.b-tijdlijn, .b-stapkaarten)')) return [];
              const sectie = document.querySelector('#voorbereiding');
              const s = getComputedStyle(sectie.querySelector(':scope > .wrap'), '::before');
              if (s.content === 'none') return ['geen gereedschap op de naad'];
              const r = sectie.getBoundingClientRect();
              const obj = { top: r.top + parseFloat(s.top), right: r.right - parseFloat(s.right) };
              obj.left = obj.right - parseFloat(s.width);
              obj.bottom = obj.top + parseFloat(s.height);
              const fout = [];
              for (const kies of [`.${lp}__kop .label`, `.${lp}__kop h2`, `.${lp}__kop .intro`]) {
                const el = sectie.querySelector(kies);
                if (!el) continue;
                const bereik = document.createRange();
                bereik.selectNodeContents(el);
                if ([...bereik.getClientRects()].some(t => obj.right > t.left && obj.left < t.right
                  && obj.top < t.bottom && obj.bottom > t.top)) fout.push(`gereedschap ligt over ${kies}`);
              }
              return fout;
            }, lp), [], `${width}: gereedschap op de naad vrij van de kop`);
            /* Na de verhuizing (blok namozaiek, versie 3 uit ronde 7, 23-09-2026) verving het blok naplaten,
               dat zelf de laatste checklistkaart verving. Blijft er ergens een halve checklist staan, dan
               staan er twee vormen van hetzelfde lijstje onder elkaar zonder dat er iets stuk lijkt. */
            await page.locator('#na-de-verhuizing').scrollIntoViewIfNeeded();
            assert.equal(await page.locator('.b-checklist').count(), 0, `${width}: er staat nog een checklist op de werkwijze`);
            /* Samenvoeging 28-09-2026: live staat het mozaiek (namozaiek). De controle van Tugche voor haar
               gele band (naband, origin/main 9dbb9a8) loopt mee zodra die op de pagina staat. */
            if (await page.locator('.b-naband').count()) {
              assert.equal(await page.locator('.b-namozaiek').count(), 0, `${width}: het oude mozaiek staat er nog`);
              assert.equal(await page.locator('.b-naband__punten > li').count(), 2, `${width}: de twee punten in de kaart`);
              /* De ploeg moet er ook echt staan: een pad dat verschuift laat een lege gele band achter, en die
                 leest als een bedoeld vlak. */
              await beeldenKlaar('.b-naband__ploeg');
              assert.ok(await page.locator('.b-naband__ploeg').evaluate(el => el.complete && el.naturalWidth > 0),
                `${width}: de ploeg op de band is geladen`);
              /* De telefoon en de ster staan als echt voorwerp op een gele schijf (28-09-2026). Laadt er een niet,
                 dan staat er een lege gele schijf, en die leest als een knop. */
              assert.equal(await page.locator('.b-naband__obj').count(), 2, `${width}: twee voorwerpen in de punten`);
              await beeldenKlaar('.b-naband__obj');
              assert.ok((await page.locator('.b-naband__obj').evaluateAll(els => els.every(el => el.complete && el.naturalWidth > 0))),
                `${width}: de voorwerpen in de punten zijn geladen`);
              /* Breed staat de ploeg naast de kaart, smal eronder; nooit over de kaart heen. */
              const naband = await page.evaluate(() => {
                const k = document.querySelector('.b-naband__kaart').getBoundingClientRect();
                const p = document.querySelector('.b-naband__ploeg').getBoundingClientRect();
                return { naast: p.left >= k.right - 1, onder: p.top >= k.bottom - 1 };
              });
              if (width >= 960) {
                assert.ok(naband.naast, `${width}: de ploeg hoort rechts naast de kaart`);
              } else {
                assert.ok(naband.onder, `${width}: de ploeg hoort onder de kaart`);
              }
            } else {
              assert.equal(await page.locator('.b-namozaiek__punten > li').count(), 2, `${width}: de twee tegels met een punt`);
              /* De foto en de twee voorwerpen moeten er ook echt zijn: een pad dat verschuift laat een lege
                 lichtblauwe tegel achter, en die leest als een bedoeld vlak. */
              await beeldenKlaar('.b-namozaiek__foto, .b-namozaiek__ding');
              assert.deepEqual(await page.locator('.b-namozaiek__foto, .b-namozaiek__ding').evaluateAll(items =>
                items.filter(el => !(el.complete && el.naturalWidth > 0)).map(el => el.getAttribute('src'))),
                [], `${width}: foto en voorwerpen in het mozaiek zijn geladen`);
              assert.equal(await page.locator('.b-namozaiek__foto').count(), 1, `${width}: de foto in de hoge tegel`);
              /* De telefoon en de ster staan rechts in hun tegel en mogen de titel niet afdekken; de tegel
                 houdt er rechts ruimte voor vrij. Ook hier op de tekst gemeten. */
              assert.deepEqual(await page.locator('.b-namozaiek__punten > li').evaluateAll(items => items.flatMap(el => {
                const titelEl = el.querySelector('.b-namozaiek__titel');
                const naam = titelEl.textContent.trim();
                const obj = el.querySelector('.b-namozaiek__ding').getBoundingClientRect();
                const fout = [];
                for (const tekst of [titelEl, el.querySelector('p')]) {
                  const bereik = document.createRange();
                  bereik.selectNodeContents(tekst);
                  if ([...bereik.getClientRects()].some(t => obj.right > t.left && obj.left < t.right
                    && obj.top < t.bottom && obj.bottom > t.top)) fout.push(`${naam}: voorwerp ligt over de ${tekst.tagName.toLowerCase()}`);
                }
                return fout;
              })), [], `${width}: voorwerpen in het mozaiek vrij van de tekst`);
              const tegels = await page.locator('.b-namozaiek__punten > li').evaluateAll(items =>
                items.map(el => Math.round(el.getBoundingClientRect().top)));
              if (width >= 660) {
                assert.ok(Math.abs(tegels[0] - tegels[1]) <= 2,
                  `${width}: de twee tegels horen naast elkaar (tops ${tegels.join(', ')})`);
              } else {
                assert.ok(tegels[1] > tegels[0],
                  `${width}: de tegels horen onder elkaar (tops ${tegels.join(', ')})`);
              }
            }
          }
          /* /offerte/ #na-aanvraag: sinds de samenvoeging van 28-09-2026 de stappen van Tugche op de Koningsblauwe band
             (blok stappen-na-aanvraag: "11. /offerte/ #na-aanvraag (stappen op de blauwe band)", "clay icons"); het
             blok na-bericht staat in offerte.py als regel om terug te wisselen. Een klei-icoon dat niet laadt laat een
             leeg geel huis achter, en een icoon over de titel dekt de stap af. */
          if (route === '/offerte/' && await page.locator('#na-aanvraag.b-stappen-na-aanvraag').count()) {
            await page.locator('#na-aanvraag').scrollIntoViewIfNeeded();
            await page.locator('#na-aanvraag .b-stappen-na-aanvraag__obj').evaluateAll(els => els.forEach(el => { el.loading = 'eager'; }));
            await beeldenKlaar('#na-aanvraag .b-stappen-na-aanvraag__obj');
            assert.equal(await page.locator('#na-aanvraag .b-stappen-na-aanvraag__stap').count(), 3, `${width}: de drie stappen na de aanvraag`);
            assert.deepEqual(await page.locator('#na-aanvraag .b-stappen-na-aanvraag__stap').evaluateAll(items => items.flatMap((el, i) => {
              const img = el.querySelector('.b-stappen-na-aanvraag__obj');
              if (!img || !img.complete || !img.naturalWidth || !img.getAttribute('src').startsWith('/img/clay/')) return [`stap ${i + 1}: klei-icoon niet geladen`];
              const o = img.getBoundingClientRect(), t = el.querySelector('.b-stappen-na-aanvraag__titel').getBoundingClientRect();
              return o.right > t.left && o.left < t.right && o.top < t.bottom && o.bottom > t.top ? [`stap ${i + 1}: klei-icoon ligt over de titel`] : [];
            })), [], `${width}: drie klei-iconen geladen en vrij van de titels`);
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
        });
      }
      meld(`${width}px: ${ROUTES.length} pagina's gecontroleerd`);
    }

    await omhul('interacties desktop', async () => {
      await page.setViewportSize({ width: 1440, height: 900 });
      await page.goto(basis, { waitUntil: 'load' });
      await page.screenshot({ path: path.join(UIT, 'home-desktop.png') });
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
      await page.screenshot({ path: path.join(UIT, 'menu-desktop.png') });
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
      await Promise.all([page.waitForNavigation({ waitUntil: 'load' }), page.locator('.nav__link--sub .ic').click()]);
      assert.equal(new URL(page.url()).pathname, '/diensten/', 'clicking the chevron opens the services page');
      await page.goto(basis, { waitUntil: 'load' });
      await page.locator('.footer').scrollIntoViewIfNeeded();
      await page.locator('.footer').screenshot({ path: path.join(UIT, 'footer-desktop.png'), style: '.header, .mcta, .skiplink { visibility: hidden !important; }' });
      assert.equal(await page.locator('.header').evaluate(el => el.classList.contains('is-vast')), true);
    });

    await omhul('interacties mobiel', async () => {
      await page.setViewportSize({ width: 390, height: 844 });
      await page.goto(basis, { waitUntil: 'load' });
      await page.screenshot({ path: path.join(UIT, 'home-mobile.png') });
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
      await page.screenshot({ path: path.join(UIT, 'menu-mobile.png') });
      await page.keyboard.press('Escape');
      assert.equal(await page.locator('main').evaluate(el => el.inert), false);
      assert.equal(await page.locator('.header__menu').evaluate(el => el === document.activeElement), true);
      await page.locator('.footer').scrollIntoViewIfNeeded();
      await page.locator('.header__menu').blur();
      await page.locator('.footer').screenshot({ path: path.join(UIT, 'footer-mobile.png'), style: '.header, .mcta, .skiplink { visibility: hidden !important; }' });
    });

    await omhul('interacties formulieren', async () => {
      await page.setViewportSize({ width: 1366, height: 650 });
      await page.goto(basis, { waitUntil: 'load' });
      await page.locator('.hero').screenshot({ path: path.join(UIT, 'home-laptop.png') });
      await page.locator('#header-of-van').fill('Den Haag');
      await page.locator('#header-of-naar').fill('Delft');
      await page.locator('#header-of-dienst').selectOption('particulier');
      await page.locator('.of-box--header .of-knop').click();
      await page.waitForURL('**/offerte/?**');
      assert.equal(await page.locator('#f-van').inputValue(), 'Den Haag');
      assert.equal(await page.locator('#f-naar').inputValue(), 'Delft');
      assert.equal(await page.locator('#f-dienst').inputValue(), 'particulier');

      // Het berichtformulier stond ook op de home (homecontact, #contact-formulier) tot 28-09-2026;
      // sindsdien staat het alleen nog op /contact/.
      for (const [route, id, field] of [['/', 'aanvraag', 'aanvraag-van'], ['/contact/', 'formulier', 'f-naam']]) {
        await page.goto(basis + route, { waitUntil: 'load' });
        const form = page.locator(`#${id} form`);
        await form.locator('button[type=submit]').click();
        assert.equal(await page.locator(`#${field}`).getAttribute('aria-invalid'), 'true');
        assert.equal(await page.locator(`#${id} .b-formulier__foutlijst`).isVisible(), true);
      }
    });
    await omhul('interacties secties en kaart', async () => {
      await page.goto(basis, { waitUntil: 'load' });
      for (const id of ['diensten', 'waarom', 'cijfers', 'werkwijze', 'over-ons', 'aanvraag']) {
        const section = page.locator(`#${id}`);
        assert.equal(await section.count(), 1, `Missing restored section: ${id}`);
        await section.scrollIntoViewIfNeeded();
        await section.screenshot({ path: path.join(UIT, `${id}-desktop.png`), style: '.header, .mcta, .skiplink { visibility: hidden !important; }' });
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
      // De interactieve kaart staat sinds 28-09-2026 alleen nog op /contact/ (blok kaart).
      await page.route('https://cdn.jsdelivr.net/**', route => route.abort());
      await page.route('https://cdnjs.cloudflare.com/**', route => route.abort());
      await page.goto(basis + '/contact/', { waitUntil: 'load' });
      await page.locator('[data-wereld-start]').click();
      await page.waitForFunction(() => !document.querySelector('[data-wereld-melding]').classList.contains('vh'));
      assert.equal(await page.locator('.wereld__terugval').isVisible(), true);
      assert.equal(await page.locator('[data-wereld-start]').isEnabled(), true);

      await page.setViewportSize({ width: 1440, height: 900 });
      await page.goto(basis + '/diensten/', { waitUntil: 'load' });
      await page.locator('.b-dienstenpanelen').first().scrollIntoViewIfNeeded();
      await page.screenshot({ path: path.join(UIT, 'diensten-desktop.png') });
      await page.setViewportSize({ width: 390, height: 844 });
      await page.goto(basis + '/diensten/', { waitUntil: 'load' });
      await page.locator('.b-dienstenpanelen').first().scrollIntoViewIfNeeded();
      await page.screenshot({ path: path.join(UIT, 'diensten-mobile.png') });
      assert.deepEqual(errors, [], 'Browser errors');
      meld('navigatie, focus, afbeeldingen en browserconsole: gecontroleerd');
    });
  } finally {
    await context.close();
  }

  meld(`schermafdrukken: ${UIT}`);
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
