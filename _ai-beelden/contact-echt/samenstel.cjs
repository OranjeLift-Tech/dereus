// Drukt inhoud op de echte foto's: belscherm op de telefoon, briefkaart met logo, formulier op het klembord.
// Elk vlak krijgt zijn inhoud via een perspectieftransformatie (vier hoeken uit vlak.cjs), met multiply,
// zodat papierstructuur en schaduw van de foto erdoorheen blijven komen. Uit: uit/<naam>-klaar.png
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');
const url = b => 'file:///' + path.resolve(b).split(path.sep).join('/');
const SITE = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus/dereus';
const LOGO = 'file:///' + SITE + '/img/logo/dereus-logo.svg';
const LOGO_H = 'file:///' + SITE + '/img/logo/dereus-logo-horizontaal.svg';
const BEELDMERK = 'file:///' + SITE + '/img/logo/dereus-beeldmerk.svg';
const FONTS = `@font-face{font-family:Inter;font-weight:400 800;src:url(file:///${SITE}/fonts/inter-latin.woff2)}
@font-face{font-family:Archivo;font-weight:700 800;font-stretch:75%;src:url(file:///${SITE}/fonts/archivo-condensed-latin.woff2)}`;

// homografie van rechthoek (0,0,w,h) naar vier punten -> matrix3d
function adj(m) { return [m[4] * m[8] - m[5] * m[7], m[2] * m[7] - m[1] * m[8], m[1] * m[5] - m[2] * m[4], m[5] * m[6] - m[3] * m[8], m[0] * m[8] - m[2] * m[6], m[2] * m[3] - m[0] * m[5], m[3] * m[7] - m[4] * m[6], m[1] * m[6] - m[0] * m[7], m[0] * m[4] - m[1] * m[3]]; }
function mm(a, b) { const c = []; for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) { let s = 0; for (let k = 0; k < 3; k++) s += a[3 * i + k] * b[3 * k + j]; c[3 * i + j] = s; } return c; }
function mv(m, v) { return [m[0] * v[0] + m[1] * v[1] + m[2] * v[2], m[3] * v[0] + m[4] * v[1] + m[5] * v[2], m[6] * v[0] + m[7] * v[1] + m[8] * v[2]]; }
function basis(p) { const m = [p[0][0], p[1][0], p[2][0], p[0][1], p[1][1], p[2][1], 1, 1, 1]; const v = mv(adj(m), [p[3][0], p[3][1], 1]); return mm(m, [v[0], 0, 0, 0, v[1], 0, 0, 0, v[2]]); }
function matrix3d(w, h, naar) {
  const t = mm(basis(naar), adj(basis([[0, 0], [w, 0], [w, h], [0, h]])));
  const n = t.map(x => x / t[8]);
  return `matrix3d(${[n[0], n[3], 0, n[6], n[1], n[4], 0, n[7], 0, 0, 1, 0, n[2], n[5], 0, n[8]].join(',')})`;
}

const TELEFOON_UI = `
<div style="position:absolute;inset:0;background:radial-gradient(120% 70% at 50% 18%,#2C62C9 0%,#1746A2 38%,#0B2352 100%);color:#fff;font-family:Inter,'Segoe UI',sans-serif">
  <div style="position:absolute;top:18px;left:34px;font:600 17px Inter">9:41</div>
  <div style="position:absolute;top:120px;left:0;right:0;text-align:center">
    <div style="margin:0 auto 22px;width:118px;height:118px;border-radius:50%;background:#fff;display:grid;place-items:center">
      <img src="${BEELDMERK}" style="width:84px">
    </div>
    <div style="font:500 30px/1.15 Inter;letter-spacing:-.01em">Verhuisbedrijf<br>De Reus</div>
    <div style="margin-top:10px;font:400 19px Inter;opacity:.72">085 000 5647</div>
    <div style="margin-top:6px;font:400 17px Inter;opacity:.55">bellen…</div>
  </div>
  <div style="position:absolute;left:44px;right:44px;bottom:210px;display:grid;grid-template-columns:repeat(3,76px);justify-content:space-between;row-gap:28px">
    ${Array.from({ length: 6 }, () => '<div style="width:76px;height:76px;border-radius:50%;background:rgba(255,255,255,.2)"></div>').join('')}
  </div>
  <div style="position:absolute;left:50%;bottom:80px;width:78px;height:78px;margin-left:-39px;border-radius:50%;background:#EB4E3D;display:grid;place-items:center">
    <svg width="40" height="40" viewBox="0 0 24 24"><path fill="#fff" transform="rotate(135 12 12)" d="M6.6 10.8a15.2 15.2 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>
  </div>
  <div style="position:absolute;left:50%;bottom:12px;width:140px;height:5px;margin-left:-70px;border-radius:3px;background:rgba(255,255,255,.85)"></div>
</div>`;

const KAART_UI = `
<div style="position:absolute;inset:0;padding:54px 60px;font-family:Inter,sans-serif;color:#0E1A33">
  <img src="${LOGO_H}" style="height:92px;display:block">
  <div style="margin-top:44px;display:grid;gap:22px">
    ${[88, 96, 72, 90, 54].map(w => `<div style="height:9px;width:${w}%;border-radius:5px;background:#9AA6BC;opacity:.75"></div>`).join('')}
  </div>
</div>`;

const veld = (label, h = 40) => `<div style="margin-top:22px"><div style="font:600 15px Inter;color:#0B2352">${label}</div><div style="margin-top:7px;height:${h}px;border:2px solid #AEB9CC;border-radius:6px"></div></div>`;
const FORMULIER_UI = `
<div style="position:absolute;inset:0;padding:112px 52px 40px;font-family:Inter,sans-serif;color:#0E1A33">
  <div style="display:flex;align-items:center;justify-content:space-between;padding-bottom:22px;border-bottom:4px solid #1746A2">
    <img src="${LOGO}" style="height:118px">
    <div style="text-align:right;font:800 40px/1 Archivo;font-stretch:75%;color:#1746A2;text-transform:uppercase">Contact-<br>formulier</div>
  </div>
  ${veld('Naam')}${veld('E-mailadres')}${veld('Telefoonnummer')}${veld('Uw vraag of bericht', 150)}
  <div style="margin-top:24px;display:flex;align-items:center;gap:12px;font:500 15px Inter"><span style="width:22px;height:22px;border:2px solid #AEB9CC;border-radius:4px"></span>Bel mij terug</div>
  <div style="margin-top:22px;width:210px;height:50px;border-radius:25px;background:#1B7F45;color:#fff;display:grid;place-items:center;font:700 17px Inter">Versturen</div>
</div>`;

const TAKEN = [
  { naam: 'telefoon', beeld: 'uit/telefoon-m.png', masker: 'uit/telefoon-scherm.png', w: 390, h: 844, ui: TELEFOON_UI,
    hoeken: [[978.2, 17.9], [1544.5, 232.7], [577.8, 931.4], [5.9, 649.9]], glans: true },
  { naam: 'envelop', beeld: 'uit/envelop-m.png', masker: 'uit/envelop-kaart.png', w: 740, h: 525, ui: KAART_UI,
    hoeken: [[358.2, 538.2], [1103.5, 302.2], [1253.7, 821.6], [526.2, 1053.2]] },
  { naam: 'klembord', beeld: 'uit/klembord-m.png', masker: 'uit/klembord-papier.png', w: 595, h: 842, ui: FORMULIER_UI,
    hoeken: [[30, 171], [609, 170], [608, 990], [28, 990]] },
];

(async () => {
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--allow-file-access-from-files'], env: { ...process.env, TMP: 'D:/claude-tmp-c3', TEMP: 'D:/claude-tmp-c3' } });
  const alleen = process.argv[2];
  for (const t of TAKEN) {
    if (alleen && t.naam !== alleen) continue;
    const meta = await require('sharp')(t.beeld).metadata();
    const W = meta.width, H = meta.height;
    const html = `<!doctype html><style>${FONTS}html,body{margin:0;background:transparent}
      #s{position:relative;width:${W}px;height:${H}px;isolation:isolate}
      #s>img{position:absolute;inset:0}
      .laag{position:absolute;inset:0;-webkit-mask:url(${url(t.masker)}) 0 0/${W}px ${H}px no-repeat}
      .ui{position:absolute;left:0;top:0;width:${t.w}px;height:${t.h}px;transform-origin:0 0;transform:${matrix3d(t.w, t.h, t.hoeken)};overflow:hidden}
    </style><div id="s"><img src="${url(t.beeld)}">
      <div class="laag" style="mix-blend-mode:multiply;filter:blur(${t.naam === 'telefoon' ? 0.4 : 0.7}px)"><div class="ui">${t.ui}</div></div>
      ${t.glans ? `<div class="laag" style="background:linear-gradient(118deg,rgba(255,255,255,0) 30%,rgba(255,255,255,.16) 46%,rgba(255,255,255,.05) 58%,rgba(255,255,255,0) 70%)"></div>` : ''}
    </div>`;
    fs.writeFileSync(`samen-${t.naam}.html`, html);
    const page = await browser.newPage({ viewport: { width: W, height: H } });
    await page.goto(url(`samen-${t.naam}.html`), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    await page.locator('#s').screenshot({ path: `uit/${t.naam}-klaar.png`, omitBackground: true });
    await page.close();
    console.log('klaar', t.naam, W, H);
  }
  await browser.close();
})();
