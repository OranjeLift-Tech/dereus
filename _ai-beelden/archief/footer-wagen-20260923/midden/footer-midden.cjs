// "make the truck be seen more and in the center" — drie lezingen naast de huidige toestand.
// Alles geinjecteerd; css/style.css blijft ongemoeid en er wordt niets gebouwd.
//
// Wat er nu gebeurt en waarom het klemt: het vak is 1094x372 (2,94:1) en de foto is 1,417:1, dus
// object-fit cover schaalt op de breedte en gooit de helft van de hoogte weg. Het vak staat bovendien
// rechts uitgelijnd met een masker dat de linkerkant wegvaagt. Groter maken maakte dat alleen erger.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('C:/users/arnas/git_repos/tandartsvanschiedam/node_modules/playwright');

const UIT = path.join(__dirname, 'midden');
fs.mkdirSync(UIT, { recursive: true });

// gemeenschappelijk voor elke "midden"-lezing: niet meer rechts plakken, en het masker symmetrisch,
// anders vaagt het de linkerhelft van een gecentreerd beeld weg.
const MIDDEN = `
.footer__wagen{
  right: auto !important; left: 50% !important; transform: translateX(-50%) !important;
  -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 16%, #000 84%, transparent 100%) !important;
  mask-image: linear-gradient(90deg, transparent 0, #000 16%, #000 84%, transparent 100%) !important;
}`;

const NIVEAUS = {
  nu: null,
  // C: alleen centreren, zelfde maat. De wagen staat midden, maar er wordt niet meer van hem getoond.
  C: MIDDEN,
  // D: centreren en het vak smaller, zodat de verhouding dichter bij die van de foto komt en cover
  //    minder hoogte hoeft weg te snijden. De wagen wordt kleiner maar completer.
  D: MIDDEN + `.footer__wagen{ width: min(58%, 54rem) !important; }`,
  // E: centreren en de band hoger, zodat er meer hoogte te tonen is bij dezelfde breedte.
  //    De wagen wordt groter en completer, maar de footer groeit.
  E: MIDDEN + `.footer__intro{ min-height: 30rem !important; }`,
};
const MATEN = [{ n: '1440x900', w: 1440, h: 900 }, { n: '1920x1080', w: 1920, h: 1080 }];

(async () => {
  const b = await chromium.launch({ channel: 'msedge', headless: true });
  for (const [naam, css] of Object.entries(NIVEAUS)) {
    for (const z of MATEN) {
      const ctx = await b.newContext({ viewport: { width: z.w, height: z.h } });
      const p = await ctx.newPage();
      await p.goto('http://127.0.0.1:8000/', { waitUntil: 'networkidle' });
      await p.evaluate(() => {
        document.querySelectorAll('img').forEach(i => { i.loading = 'eager'; });
        window.scrollTo(0, document.body.scrollHeight);
      });
      if (css) await p.addStyleTag({ content: css });
      await p.waitForFunction(() => {
        const i = document.querySelector('.footer__wagen');
        return i && i.complete && i.naturalWidth > 0;
      }, { timeout: 15000 });
      await p.waitForTimeout(450);
      if (z.n === '1440x900') {
        const m = await p.evaluate(() => {
          const img = document.querySelector('.footer__wagen');
          const band = document.querySelector('.footer__intro');
          const knop = document.querySelector('.footer__intro a[href^="tel"]');
          const r = img.getBoundingClientRect(), br = band.getBoundingClientRect();
          const s = Math.max(r.width / img.naturalWidth, r.height / img.naturalHeight);
          const getoondB = Math.min(1, r.width / (img.naturalWidth * s));
          const getoondH = Math.min(1, r.height / (img.naturalHeight * s));
          // de belettering zit op 55,8 tot 88,9 procent van de foto (gemeten bij het exporteren)
          const fotoL = r.left - (img.naturalWidth * s - r.width) / 2;
          const letterL = fotoL + 0.558 * img.naturalWidth * s;
          const letterR = fotoL + 0.889 * img.naturalWidth * s;
          return {
            vak: Math.round(r.width) + 'x' + Math.round(r.height),
            bandH: Math.round(br.height),
            getoond: Math.round(getoondB * 100) + '% breed, ' + Math.round(getoondH * 100) + '% hoog',
            vanDeFoto: +(getoondB * getoondH * 100).toFixed(1),
            letteringBreed: Math.round(letterR - letterL),
            afstandTotKnop: knop ? Math.round(letterL - knop.getBoundingClientRect().right) : null,
          };
        });
        console.log(naam.padEnd(3), JSON.stringify(m));
      }
      const el = await p.$('.footer__intro');
      await el.screenshot({ path: path.join(UIT, `${naam}-${z.n}.png`) });
      await ctx.close();
    }
  }
  // en de telefoon, om te bevestigen dat er daar nog steeds niets staat
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, deviceScaleFactor: 2 });
  const p = await ctx.newPage();
  await p.goto('http://127.0.0.1:8000/', { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: NIVEAUS.E });
  await p.waitForTimeout(400);
  console.log('390x844 display =', await p.evaluate(() => getComputedStyle(document.querySelector('.footer__wagen')).display));
  await (await p.$('.footer__intro')).screenshot({ path: path.join(UIT, 'E-390x844.png') });
  await ctx.close();
  await b.close();
})();
