// 10 ontwerpen voor "Hoe de prijs tot stand komt" op /kosten/ (#opbouw), elk op de code van een echt blok van
// referentie A, referentie B (de pagina /bedrijven/ en het prijzenblok) of referentie C.
// node gen.cjs  ->  _ontwerpen/prijsopbouw-referentie-varianten.html
// Alle teksten komen letterlijk uit kosten/index.html (sectie #opbouw); 00 is dat blok zoals het nu live staat.
// Beelden: echte foto's uit img/ en de echte fotovoorwerpen van /contact/ (bakwagen, munten, wekker, klembord),
// hier groter geexporteerd in img/ naast dit script. Geen klei-iconen.
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

// ---- beelden ----
const EIGEN = '/_ontwerpen/_bron-prijsopbouw-ref/img/';
// een foto per factor (zelfde volgorde als de vijf factoren)
const FOTO = [
  { src: '/img/voorbereiding-dozen.webp', pos: '50% 60%' },      // hoeveel er mee moet: de dozen met logo in de gang
  { src: '/img/dienst-nationaal-v2.webp', pos: '58% 45%' },      // de afstand: de wagen op de weg
  { src: '/img/voorbereiding-trap.webp', pos: '40% 40%' },       // de bereikbaarheid: de trap
  { src: '/img/verwachten-inpakken.webp', pos: '50% 45%' },      // wat u zelf doet: inpakken
  { src: '/img/dienst-verhuislift.webp', pos: '60% 40%' },       // extra diensten: de verhuislift
];
// foto + uitsnede van precies dezelfde foto, voor een persoon die boven het kader uitsteekt (--top: de rij die op de
// bovenrand valt, --d0: de kruin, --mid: het midden van het onderwerp; alles als fractie van de foto)
const POP = [
  { foto: '/img/dienst-woningontruiming.webp', uit: '/img/dienst-woningontruiming-uit.webp', ar: 4 / 3, top: .27, d0: .09, mid: .64 },
  { foto: '/img/dienst-nationaal-v2.webp', uit: '/img/dienst-nationaal-v2-uit.webp', ar: 4 / 3, top: .39, d0: .27, mid: .56 },
  { foto: '/img/voorbereiding-kast.webp', uit: '/img/voorbereiding-kast-man.webp', ar: 1200 / 1030, top: .33, d0: .21, mid: .62 },
  { foto: '/img/dienst-montage-v2.webp', uit: '/img/dienst-montage-v2-uit.webp', ar: 4 / 3, top: .19, d0: .03, mid: .62 },
  { foto: '/img/dienst-verhuislift.webp', uit: '/img/dienst-verhuislift-uit.webp', ar: 4 / 3, top: .33, d0: .22, mid: .58 },
];
const pop = (p, cls = '') => `<div class="pop ${cls}" style="--ar:${p.ar.toFixed(4)};--top:${p.top};--d0:${p.d0};--mid:${p.mid}" aria-hidden="true"><div class="pop__raam">${img(p.foto, 'pop__foto')}</div><div class="pop__uit">${img(p.uit, '')}</div></div>`;
const OBJ = {
  klembord: EIGEN + 'klembord.webp', wekker: EIGEN + 'wekker.webp', bakwagen: EIGEN + 'bakwagen.webp',
  munten: EIGEN + 'munten.webp', dozen: '/img/contact-echt/dozen-307.webp',
};
const obj = (n, cls = '') => img(OBJ[n], `obj obj--${n} ${cls}`, ' aria-hidden="true"');
// bij All-in het klembord met de offerte, bij regie de wekker; bij de twee stroken de wagen en de munten
const VAK_OBJ = ['klembord', 'wekker'];
const SOORT_OBJ = ['bakwagen', 'munten'];
const foto = (i, cls = '') => img(FOTO[i].src, cls, ` style="object-position:${FOTO[i].pos}"`);
const nr2 = i => String(i + 1).padStart(2, '0');

const V = [];
const add = (n, naam, bron, uitleg, html) => V.push({ n, naam, bron, uitleg, html });
require('./ontwerpen.cjs')({ add, T, img, ic, foto, FOTO, POP, pop, obj, OBJ, VAK_OBJ, SOORT_OBJ, nr2, EIGEN });

// ---- pagina ----
const css = fs.readFileSync(path.join(__dirname, 'var.css'), 'utf8');
const navl = ['00', ...V.map(x => x.n)].map(n => `<a href="#v${n}">${n}</a>`).join('');
const kap = (n, naam, bron, uitleg) => `<div class="vkap" id="v${n}"><div class="wrap"><span class="vkap__nr">${n}</span><div><b>${naam}</b><small>${bron}</small><p>${uitleg}</p></div><span class="vkap__maat" data-maat></span></div></div>`;
// op /kosten/ staat erboven "Direct antwoord" (wit) en eronder de Diepblauwe trapband "Wat kost een verhuizing?"
const boven = `<div class="vctx vctx--wit" aria-hidden="true"><div class="wrap">Hierboven op /kosten/: het directe antwoord (wit)</div></div>`;
const onder = `<div class="vctx" aria-hidden="true"><div class="wrap">Hieronder: Wat kost een verhuizing? (de Diepblauwe trapband)</div></div>`;
const live = `<div class="p-kosten">${SEC.replace(/id="(opbouw|all-in|regie|voorrijkosten|betalen)"/g, 'id="$1-live"').replace(/opbouw-kop/g, 'opbouw-kop-live')}</div>`;

const html = `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=' js'</script>
<title>Hoe de prijs tot stand komt · 10 ontwerpen · referentie A, B en C</title>
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
<nav class="vnav" aria-label="Ontwerpen"><div class="wrap"><b>/kosten/ Hoe de prijs tot stand komt · 10 ontwerpen</b><div class="vnav__links">${navl}</div></div></nav>
${kap('00', 'Zo staat het blok nu live', 'Ter vergelijking', 'Gele schijven met klei-voorwerpen, de accolade naar het fotoduo All-in / Regieprijs, de slottekst en de twee stroken. Elk ontwerp hieronder vervangt dit hele blok en houdt precies dezelfde teksten.')}
${boven}
${live}
${onder}
${V.map(x => kap(x.n, x.naam, x.bron, x.uitleg) + '\n' + boven + '\n' + x.html(x.n) + '\n' + onder).join('\n')}
<div class="vkap vkap--eind"><div class="wrap"><p>Alle teksten zijn letterlijk die van /kosten/ #opbouw: kop, inleiding, de vijf factoren, All-in prijs of Regieprijs, de slottekst en de twee stroken. Er staan geen klei-iconen meer in: de factoren hebben echte foto's uit de eigen map, en bij All-in, Regie, voorrijkosten en betalen staan de echte fotovoorwerpen van /contact/ (klembord met de offerte, wekker, de bakwagen, munten). Elke bronklasse hierboven bestaat echt in de code van referentie A, B of C; in de De Reus-code komen die namen niet terug. Kies een nummer.</p></div></div>
<script>
(function(){
function meet(){document.querySelectorAll('[data-maat]').forEach(function(m){var s=m.closest('.vkap').nextElementSibling;while(s&&!(s.tagName==='SECTION'||s.classList.contains('p-kosten')))s=s.nextElementSibling;if(!s)return;var h=Math.round(s.getBoundingClientRect().height);m.textContent='Blokhoogte '+h+' px';m.classList.toggle('is-hoog',h>900);});}
addEventListener('load',meet);addEventListener('resize',meet);
})();
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(REPO, '_ontwerpen/prijsopbouw-referentie-varianten.html'), html);
console.log('ok', html.length, V.length, T.factoren.map(f => f.titel).join(' | '));
