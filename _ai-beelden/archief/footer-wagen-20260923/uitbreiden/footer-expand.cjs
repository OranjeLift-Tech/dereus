// Twee niveaus "groter" voor de footerfoto, gemeten en gefotografeerd zonder iets in de repo te
// wijzigen: de CSS gaat via een injectie in de pagina. Zo kan de gebruiker kiezen voordat er
// gebouwd wordt.
//
// Gebruik: node footer-expand.cjs
const path = require('node:path');
const { chromium } = require('C:/users/arnas/git_repos/tandartsvanschiedam/node_modules/playwright');

const UIT = __dirname;
const NIVEAUS = [
  { naam: 'nu', css: null },
  { naam: 'A', css: '.footer__wagen{ width: min(88%, 84rem) !important; }' },
  { naam: 'B', css: '.footer__wagen{ width: min(100%, 96rem) !important; }' },
  // los lever: minder wegmaskeren in plaats van groter maken
  { naam: 'M', css: '.footer__wagen{ -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 20%) !important;'
                  + ' mask-image: linear-gradient(90deg, transparent 0, #000 20%) !important; }' },
];
const MATEN = [{ w: 1440, h: 900 }, { w: 1920, h: 1080 }];

async function meet(p) {
  return p.evaluate(() => {
    const img = document.querySelector('.footer__wagen');
    const band = document.querySelector('.footer__intro');
    const r = img.getBoundingClientRect(), br = band.getBoundingClientRect();
    const schaal = Math.max(r.width / img.naturalWidth, r.height / img.naturalHeight);
    const cs = getComputedStyle(img);
    const mask = (cs.maskImage && cs.maskImage !== 'none' ? cs.maskImage : cs.webkitMaskImage) || '';
    const stop = mask.match(/(\d+(?:\.\d+)?)%/);
    // waar de belettering van de flank landt: die zit op 58 tot 89 procent van de foto
    const letterL = r.left + 0.58 * img.naturalWidth * schaal - (img.naturalWidth * schaal - r.width) / 2;
    const letterR = r.left + 0.89 * img.naturalWidth * schaal - (img.naturalWidth * schaal - r.width) / 2;
    return {
      vakB: Math.round(r.width), vakH: Math.round(r.height),
      bandB: Math.round(br.width),
      dekking: +(r.width / br.width * 100).toFixed(1),
      schaal: +schaal.toFixed(3),
      zichtH: +(Math.min(1, r.height / (img.naturalHeight * schaal)) * 100).toFixed(1),
      maskerStop: stop ? +stop[1] : null,
      belettering: Math.round(letterR - letterL),
    };
  });
}

(async () => {
  const b = await chromium.launch({ channel: 'msedge', headless: true });
  for (const maat of MATEN) {
    for (const n of NIVEAUS) {
      const ctx = await b.newContext({ viewport: { width: maat.w, height: maat.h } });
      const p = await ctx.newPage();
      await p.goto('http://127.0.0.1:8000/', { waitUntil: 'networkidle' });
      await p.evaluate(() => {
        document.querySelectorAll('img').forEach(i => { i.loading = 'eager'; });
        window.scrollTo(0, document.body.scrollHeight);
      });
      if (n.css) await p.addStyleTag({ content: n.css });
      // echt wachten tot de footerfoto geverfd is; lazy loading laat hem anders leeg
      await p.waitForFunction(() => {
        const i = document.querySelector('.footer__wagen');
        return i && i.complete && i.naturalWidth > 0;
      }, { timeout: 15000 });
      await p.waitForTimeout(400);
      const m = await meet(p);
      console.log(`${maat.w}  ${n.naam.padEnd(3)} vak ${m.vakB}x${m.vakH} = ${m.dekking}% van de band`
        + `, schaal ${m.schaal}, ${m.zichtH}% van de hoogte zichtbaar`
        + `, masker tot ${m.maskerStop}%, belettering ${m.belettering} px breed`);
      const el = await p.$('.footer__intro');
      await el.screenshot({ path: path.join(UIT, `footer-${n.naam}-${maat.w}x${maat.h}.png`) });
      await ctx.close();
    }
    console.log('');
  }
  // controle: onder 768 hoort er geen foto te staan
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, deviceScaleFactor: 2 });
  const p = await ctx.newPage();
  await p.goto('http://127.0.0.1:8000/', { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: NIVEAUS[2].css });
  await p.waitForTimeout(500);
  const zichtbaar = await p.evaluate(() => {
    const i = document.querySelector('.footer__wagen');
    return i ? getComputedStyle(i).display : 'element weg';
  });
  console.log('390x844: .footer__wagen display =', zichtbaar);
  await (await p.$('.footer__intro')).screenshot({ path: path.join(UIT, 'footer-B-390x844.png') });
  await ctx.close();
  await b.close();
})();
