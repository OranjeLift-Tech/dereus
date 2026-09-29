// Voorstel klant (29-09-2026): de armen in het De Reus-logo hoger, over het huis heen, en de biceps groter.
// Leest de logo's uit /img/logo en schrijft per sterkte een map naast dit script; /img/logo blijft zoals het is.
//   node armen.mjs
// Werkt op de linkerarm; de rechterarm is exact gespiegeld en krijgt dezelfde vervorming.
//
// Opzet: de arm draait om de schouder omhoog (elleboog hoger, vuist naar binnen boven het dak) en gaat als
// geheel iets omhoog. De arm zelf blijft de originele tekening, alleen de biceps wordt groter. De armen
// liggen vóór het huis: waar ze over het dak komen, wordt het huis uitgespaard met dezelfde witte naad als nu.
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const HIER = path.dirname(fileURLToPath(import.meta.url));
const BRON = path.join(HIER, '..', '..', 'img', 'logo');

// Sterktes: draai = hoek (graden) om de schouder, omhoog = hoeveel de hele arm stijgt, naarBinnen = hoeveel de
// arm richting het huis schuift (pad-eenheden, logo is 1000 breed); bol en piek = hoeveel de biceps groeit.
// Grens: de rechtervuist mag niet in de schoorsteen komen (zie controle.cjs in de scratchpad van 29-09).
export const STERKTES = {
  licht:  { draai: 9, omhoog: 45, naarBinnen: 12, bol: 0.16, piek: 10 },
  midden: { draai: 12, omhoog: 50, naarBinnen: 10, bol: 0.22, piek: 16 },
  sterk:  { draai: 15, omhoog: 70, naarBinnen: 8, bol: 0.28, piek: 22 },
};

const glad = (a, b, v) => { const t = Math.min(1, Math.max(0, (v - a) / (b - a))); return t * t * (3 - 2 * t); };

// Linkerarm in de coördinaten van het staande logo: schouder = verticale snede langs de huismuur (x ~307,
// y 282-508), elleboog linksonder (0, 380), vuist boven (190-330, 0-160). Biceps = de koepel x 150-265,
// top y ~282, onderlijn (glimlach) y ~390. Draaipunt midden op de schoudersnede.
const BICEPS = { x: 200, y: 350, rx: 120, ry: 110 };
const SCHOUDER = { x: 300, y: 390 };
const NAAD = 19.4;     // witte naad tussen arm en huis in het huidige logo (schoudersnede x 307 ↔ muur x 325)

export function maakVervorming({ draai, omhoog, naarBinnen, bol, piek }) {
  const c = Math.cos(draai * Math.PI / 180), sn = Math.sin(draai * Math.PI / 180);
  return (x, y) => {
    // 1. Biceps groter: de koepel als geheel vergroten (binnen r 0,5 gelijkmatig, daarbuiten aflopend),
    //    vooral omhoog en naar buiten, nauwelijks richting het huis.
    const u = (x - BICEPS.x) / BICEPS.rx, v = (y - BICEPS.y) / BICEPS.ry, r = Math.hypot(u, v);
    if (r < 1) {
      const k = 1 - glad(0.5, 1, r), naarHuis = x > BICEPS.x ? 0.3 * (1 - glad(240, 300, x)) : 1;
      x += (x - BICEPS.x) * bol * k * naarHuis;
      y += (y - BICEPS.y) * bol * k * (y < BICEPS.y ? 1 : 0.35) - piek * k * (y < BICEPS.y ? 1 : 0.4);
    }
    // 2. Draaien om de schouder en iets naar binnen. De schoudersnede tegen de muur (onder de vuist) doet
    //    niet mee, zodat hij recht naast de muur blijft staan; de hele arm gaat daarna `omhoog`.
    const w = Math.max(1 - glad(170, 260, y), 1 - glad(262, 307, x));
    const dx = x - SCHOUDER.x, dy = y - SCHOUDER.y;
    const rx = SCHOUDER.x + dx * c - dy * sn, ry = SCHOUDER.y + dx * sn + dy * c;
    return [x + (rx - x + naarBinnen) * w, y + (ry - y) * w - omhoog];
  };
}

// Masker op het huis: waar een arm (plus NAAD eromheen) over het huis komt, valt het huis weg.
const maskerVoor = (s, sc) => `<defs><mask id="huis-vrij" maskUnits="userSpaceOnUse" x="-9999" y="-9999" width="29999" height="29999">`
  + `<rect x="-9999" y="-9999" width="29999" height="29999" fill="#fff"/>`
  + ['arm-links', 'arm-rechts'].map(id => `<path d="${padVan(s, id)}" fill="#000" stroke="#000" stroke-width="${(2 * NAAD * sc).toFixed(2)}" stroke-linejoin="round"/>`).join('')
  + `</mask></defs>`;

const bbox = d => {
  const n = d.match(/-?\d+(?:\.\d+)?/g).map(Number); let b = [1e9, 1e9, -1e9, -1e9];
  for (let k = 0; k < n.length; k += 2) b = [Math.min(b[0], n[k]), Math.min(b[1], n[k + 1]), Math.max(b[2], n[k]), Math.max(b[3], n[k + 1])];
  return b;
};
const padVan = (s, id) => s.match(new RegExp(`<path id="${id}"[^>]*? d="([^"]*)"`))[1];

// Maat van de linkerarm in het staande logo: daarop zijn BICEPS en de grenzen hierboven afgemeten.
const REF = bbox(padVan(fs.readFileSync(path.join(BRON, 'dereus-logo.svg'), 'utf8'), 'arm-links'));

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  const bestanden = fs.readdirSync(BRON).filter(f => f.endsWith('.svg') && !f.includes('favicon')
    && fs.readFileSync(path.join(BRON, f), 'utf8').includes('id="arm-links"'));
  for (const [naam, sterkte] of Object.entries(STERKTES)) {
    const map = path.join(HIER, naam); fs.mkdirSync(map, { recursive: true });
    const f = maakVervorming(sterkte);
    for (const bestand of bestanden) {
      let s = fs.readFileSync(path.join(BRON, bestand), 'utf8');
      const [vx, vy, vw, vh] = s.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
      const bl = bbox(padVan(s, 'arm-links')), br = bbox(padVan(s, 'arm-rechts'));
      const sc = (bl[2] - bl[0]) / (REF[2] - REF[0]), ox = bl[0] - REF[0] * sc, oy = bl[1] - REF[1] * sc, m = (bl[0] + br[2]) / 2;
      for (const [id, links] of [['arm-links', true], ['arm-rechts', false]]) {
        const d = padVan(s, id), n = d.match(/-?\d+(?:\.\d+)?/g).map(Number), uit = [];
        for (let k = 0; k < n.length; k += 2) {
          const X = links ? n[k] : 2 * m - n[k];
          const [x, y] = f((X - ox) / sc, (n[k + 1] - oy) / sc);
          uit.push(links ? x * sc + ox : 2 * m - (x * sc + ox), y * sc + oy);
        }
        let i = 0;
        s = s.replace(d, () => d.replace(/-?\d+(?:\.\d+)?/g, () => (+uit[i++].toFixed(2)).toString()));
      }
      s = s.replace(/(<g id="beeldmerk"[^>]*>)/, `${maskerVoor(s, sc)}$1`)
        .replace('<path id="huis"', '<path id="huis" mask="url(#huis-vrij)"');
      // viewBox uitbreiden met wat vuisten (boven) en ellebogen (opzij) nu buiten de oude rand steken
      const nl = bbox(padVan(s, 'arm-links')), nr = bbox(padVan(s, 'arm-rechts'));
      const nx = Math.min(vx, Math.floor(nl[0])), ny = Math.min(vy, Math.floor(Math.min(nl[1], nr[1])));
      const nw = Math.max(vx + vw, Math.ceil(nr[2])) - nx, nh = vh + (vy - ny);
      s = s.replace(/viewBox="[^"]+"/, `viewBox="${nx} ${ny} ${nw.toFixed(2)} ${nh.toFixed(2)}"`);
      // horizontaal: woordmerk weer midden naast het (nu hogere) beeldmerk
      if (bestand.includes('horizontaal')) s = s.replace('<g id="woordmerk">', `<g id="woordmerk" transform="translate(0 ${((ny - vy) / 2).toFixed(2)})">`);
      const w = +(s.match(/<svg[^>]* width="([\d.]+)"/)?.[1] || 0);
      if (w) s = s.replace(/(<svg[^>]* width=")[\d.]+(")/, `$1${Math.round(nw * w / vw)}$2`)
        .replace(/(<svg[^>]* height=")[\d.]+(")/, `$1${Math.round(nh * w / vw)}$2`);
      fs.writeFileSync(path.join(map, bestand), s);
    }
    console.log('OK', naam, bestanden.length, 'bestanden');
  }
}
