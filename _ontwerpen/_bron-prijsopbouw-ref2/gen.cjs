// Ronde 5 voor "Hoe de prijs tot stand komt" op /kosten/ (#opbouw): 10 ontwerpen, elk op de code van een echt blok
// van referentie A, referentie B of referentie C, maar nu met de diepte van het blok "Op de verhuisdag" op /werkwijze/:
// gekleurde banden, verhuizers die uit hun foto stappen en echte voorwerpen die boven dikke platen uitkomen.
// Ronde 4 (_bron-prijsopbouw-ref, prijsopbouw-referentie-varianten.html) vond de gebruiker te sober.
// node gen.cjs  ->  _ontwerpen/prijsopbouw-referentie-varianten-2.html
// Alle teksten komen letterlijk uit kosten/index.html (sectie #opbouw); 00 is dat blok zoals het nu live staat.
const fs = require('fs');
const path = require('path');
const REPO = path.resolve(__dirname, '../..');
const PAG = fs.readFileSync(path.join(REPO, 'kosten/index.html'), 'utf8');
const SEC = PAG.match(/<section class="b-opbouw[^"]*"[^>]*id="opbouw"[\s\S]*?<\/section>/)[0];
const sprite = PAG.match(/<svg class="sprite"[\s\S]*?<\/svg>/)[0];
const link = n => PAG.match(new RegExp(`<link rel="stylesheet" href="/css/min/${n}\\.min\\.css\\?v=[0-9a-f]+">`))[0];
const jsTag = (PAG.match(/<script src="\/js\/site\.js\?v=[0-9a-f]+" defer><\/script>/) || [''])[0];

// ---- de live teksten ----
const een = re => { const m = SEC.match(re); if (!m) throw new Error('niet gevonden: ' + re); return m[1]; };
const T = {
  label: een(/<p class="label">([\s\S]*?)<\/p>/),
  h2: een(/<h2 class="h2" id="opbouw-kop">([\s\S]*?)<\/h2>/),
  intro: een(/<p class="b-opbouw__intro">([\s\S]*?)<\/p>/),
  lijstkop: een(/<h3 class="b-opbouw__lijstkop">([\s\S]*?)<\/h3>/),
  factoren: [...SEC.matchAll(/<h3 class="b-opbouw__factorkop">([\s\S]*?)<\/h3><p>([\s\S]*?)<\/p>/g)].map(m => ({ titel: m[1], tekst: m[2] })),
  vakken: [...SEC.matchAll(/<h3 class="b-opbouw__vakkop">([\s\S]*?)<\/h3><p>([\s\S]*?)<\/p>/g)].map(m => ({ titel: m[1], tekst: m[2] })),
  of: een(/<span class="b-opbouw__naad" aria-hidden="true">([\s\S]*?)<\/span>/),
  slot: een(/<p class="b-opbouw__slot">([\s\S]*?)<\/p>/),
  soorten: [...SEC.matchAll(/<h3 class="b-opbouw__soortkop">([\s\S]*?)<\/h3><p>([\s\S]*?)<\/p>/g)].map(m => ({ titel: m[1], tekst: m[2] })),
};
if (T.factoren.length !== 5 || T.vakken.length !== 2 || T.soorten.length !== 2) throw new Error('tekst niet compleet');
// het telefoonnummer staat al in de header van /kosten/
const TEL = (PAG.match(/<a class="header__tel" href="tel:[^"]+">[\s\S]*?<span>([^<]+)<\/span><\/a>/) || [])[1];
if (!TEL) throw new Error('telefoonnummer niet gevonden');

function maat(src) {
  if (src.endsWith('.svg')) return null;
  const b = fs.readFileSync(path.join(REPO, src));
  const soort = b.toString('ascii', 12, 16);
  if (soort === 'VP8X') return [1 + b.readUIntLE(24, 3), 1 + b.readUIntLE(27, 3)];
  if (soort === 'VP8 ') return [b.readUInt16LE(26) & 0x3fff, b.readUInt16LE(28) & 0x3fff];
  if (soort === 'VP8L') { const n = b.readUInt32LE(21); return [(n & 0x3fff) + 1, ((n >> 14) & 0x3fff) + 1]; }
  throw new Error('geen webp: ' + src);
}
const img = (src, cls = '', extra = '') => {
  const m = maat(src);
  return `<img class="${cls}" src="${src}" alt=""${m ? ` width="${m[0]}" height="${m[1]}"` : ''} loading="lazy" decoding="async"${extra}>`;
};
const ic = n => `<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-${n}"/></svg>`;
const nr2 = i => String(i + 1).padStart(2, '0');

// ---- foto's met hun uitsnede (zelfde kader, zelfde plek) ----
// d0: kruin van het hoogste deel van het onderwerp, mid: midden van het onderwerp, beide als deel van het beeld.
// Gemeten met sharp op het alfakanaal van de uitsnede (profiel.cjs in de scratchpad van 29-09-2026).
const P = {
  dozen: { foto: '/img/dienst-woningontruiming.webp', uit: '/img/dienst-woningontruiming-uit.webp', ar: 4 / 3, d0: .093, mid: .6 },
  afstand: { foto: '/img/dienst-nationaal-v2.webp', uit: '/img/dienst-nationaal-v2-uit.webp', ar: 4 / 3, d0: .267, mid: .56 },
  afstandGroot: { foto: '/img/dienst-nationaal-v2-groot.webp', uit: '/img/dienst-nationaal-v2-uit.webp', ar: 4 / 3, d0: .267, mid: .57 },
  lift: { foto: '/img/dienst-verhuislift.webp', uit: '/img/dienst-verhuislift-uit.webp', ar: 4 / 3, d0: .225, mid: .53 },
  zelf: { foto: '/img/dienst-montage-v2.webp', uit: '/img/dienst-montage-v2-uit.webp', ar: 4 / 3, d0: .035, mid: .64 },
  opslag: { foto: '/img/dienst-opslag-v3.webp', uit: '/img/dienst-opslag-v3-uit.webp', ar: 4 / 3, d0: .132, mid: .48 },
};
// een foto per factor, in de volgorde van de vijf factoren
const FAC = [P.dozen, P.afstand, P.lift, P.zelf, P.opslag];
// uitsnede voor een foto op zichzelf (object-position)
const SNEDE = ['55% 42%', '58% 48%', '55% 34%', '62% 30%', '46% 38%'];

// Uitsteken naar boven (de rekensom van referentie B .sgd1-pop): het kader heeft een vaste verhouding --fa, de
// foto wordt zo groot dat de kruin precies --p boven het kader staat, en horizontaal op --mid gecentreerd. Boven het
// kader staat de uitsnede, geknipt op de strook boven het kader.
const pop = (p, cls = '', extra = '') => `<div class="pop ${cls}" style="--ar:${p.ar.toFixed(4)};--d0:${p.d0};--mid:${p.mid}${extra}" aria-hidden="true"><div class="pop__raam">${img(p.foto, 'pop__foto')}</div><div class="pop__boven">${img(p.uit, '')}</div></div>`;

// Uitsteken naar alle kanten (de techniek van "Op de verhuisdag" op /werkwijze/): het kader is een venster in de foto,
// win = [x0, y0, x1, y1] als deel van het beeld. De uitsnede staat erover maar laat alleen zien wat buiten het venster
// valt. Waar het onderwerp door de fotorand wordt afgesneden, valt het venster op die rand.
const rond = (p, win, cls = '') => {
  const [x0, y0, x1, y1] = win;
  const ar = ((x1 - x0) * p.ar) / (y1 - y0);
  const s = 1 / (x1 - x0), x = -x0 / (x1 - x0), y = -y0 / (y1 - y0);
  return `<div class="rond ${cls}" style="--ar:${ar.toFixed(4)};--s:${s.toFixed(4)};--x:${x.toFixed(4)};--y:${y.toFixed(4)}" aria-hidden="true"><div class="rond__raam">${img(p.foto, '')}</div><div class="rond__buiten">${img(p.uit, '')}</div></div>`;
};

// echte fotovoorwerpen (dezelfde reeks als /contact/), hier groter geexporteerd
const EIGEN = '/_ontwerpen/_bron-prijsopbouw-ref2/img/';
const OBJ = { klembord: EIGEN + 'klembord.webp', wekker: EIGEN + 'wekker.webp', bakwagen: EIGEN + 'bakwagen.webp', munten: EIGEN + 'munten.webp', dozen: '/img/contact-echt/dozen-307.webp' };
const obj = (n, cls = '') => img(OBJ[n], `obj obj--${n} ${cls}`, ' aria-hidden="true"');
const VAK_OBJ = ['klembord', 'wekker'];   // All-in: het klembord met de offerte, Regie: de wekker
const SOORT_OBJ = ['bakwagen', 'munten']; // voorrijkosten: de wagen, betalen: de munten

const V = [];
const add = (n, naam, bron, uitleg, html) => V.push({ n, naam, bron, uitleg, html });
require('./ontwerpen.cjs')({ add, T, TEL, img, ic, nr2, P, FAC, SNEDE, pop, rond, obj, VAK_OBJ, SOORT_OBJ, EIGEN });

// ---- pagina ----
const css = fs.readFileSync(path.join(__dirname, 'var.css'), 'utf8');
const navl = ['00', ...V.map(x => x.n)].map(n => `<a href="#v${n}">${n}</a>`).join('');
const kap = (n, naam, bron, uitleg) => `<div class="vkap" id="v${n}"><div class="wrap"><span class="vkap__nr">${n}</span><div><b>${naam}</b><small>${bron}</small><p>${uitleg}</p></div><span class="vkap__maat" data-maat></span></div></div>`;
const boven = `<div class="vctx vctx--wit" aria-hidden="true"><div class="wrap">Hierboven op /kosten/: het directe antwoord (wit)</div></div>`;
const onder = `<div class="vctx" aria-hidden="true"><div class="wrap">Hieronder: Wat kost een verhuizing? (de Diepblauwe trapband)</div></div>`;
const live = `<div class="p-kosten">${SEC.replace(/id="(opbouw|all-in|regie|voorrijkosten|betalen)"/g, 'id="$1-live"').replace(/opbouw-kop/g, 'opbouw-kop-live')}</div>`;

const html = `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=' js'</script>
<title>Hoe de prijs tot stand komt · ronde 5 · referentie A, B en C</title>
<meta name="robots" content="noindex">
${link('site')}
${link('opbouw')}
${link('kosten-diepte')}
${link('opbouw-3d')}
<style>
${css}
</style>
${jsTag}
</head>
<body>
${sprite}
<nav class="vnav" aria-label="Ontwerpen"><div class="wrap"><b>/kosten/ Hoe de prijs tot stand komt · ronde 5</b><div class="vnav__links">${navl}</div></div></nav>
${kap('00', 'Zo staat het blok nu live', 'Ter vergelijking', 'Gele schijven met klei-voorwerpen, de accolade naar het fotoduo All-in / Regieprijs, de slottekst en de twee stroken. Elk ontwerp hieronder vervangt dit hele blok en houdt precies dezelfde teksten.')}
${boven}
${live}
${onder}
${V.map(x => kap(x.n, x.naam, x.bron, x.uitleg) + '\n' + boven + '\n' + x.html(x.n) + '\n' + onder).join('\n')}
<div class="vkap vkap--eind"><div class="wrap"><p>Alle teksten zijn letterlijk die van /kosten/ #opbouw. Geen klei-iconen: de vijf factoren hebben echte foto's uit de eigen map (verhuizers met dozen, de wagen, de verhuislift, de boormachine, de opslag), waarbij de verhuizers uit hun foto stappen zoals in "Op de verhuisdag" op /werkwijze/. Bij All-in, Regie, voorrijkosten en betalen staan de echte fotovoorwerpen van /contact/ (klembord met de offerte, wekker, de bakwagen, munten). Elke bronklasse hierboven bestaat echt in de code van referentie A, B of C; in de De Reus-code komen die namen niet terug. Kies een nummer.</p></div></div>
<script>
(function(){
function meet(){document.querySelectorAll('[data-maat]').forEach(function(m){var s=m.closest('.vkap').nextElementSibling;while(s&&!(s.tagName==='SECTION'||s.classList.contains('p-kosten')))s=s.nextElementSibling;if(!s)return;var h=Math.round(s.getBoundingClientRect().height);m.textContent='Blokhoogte '+h+' px';m.classList.toggle('is-hoog',h>1000);});}
addEventListener('load',meet);addEventListener('resize',meet);
})();
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(REPO, '_ontwerpen/prijsopbouw-referentie-varianten-2.html'), html);
console.log('ok', html.length, V.length, TEL);
