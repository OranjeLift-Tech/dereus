// 15 ontwerpen voor "Zo gaat het verder" op /offerte/ (#na-aanvraag), elk op de code van een echt blok van
// referentie A, referentie B of referentie C. De klantenservicemedewerker staat er steeds zonder kamer in
// (img/contact-klantenservice-boog-uit.webp: zij, het bureau, het schrijfblok en de kop; geen muur, raam,
// plant, scherm of toetsenbord).
// node gen.cjs  ->  _ontwerpen/offerte-na-aanvraag-varianten.html
// Teksten komen letterlijk uit offerte/index.html (sectie #na-aanvraag), vastgelegd op 29-09-2026 in
// live-offerte.json: een andere sessie zette het blok die dag terug, en "00 nu live" moet het blok blijven dat
// de gebruiker liet zien (de Diepblauwe plaat met foto).
const fs = require('fs');
const path = require('path');
const REPO = path.resolve(__dirname, '../..');
const LIVE = JSON.parse(fs.readFileSync(path.join(__dirname, 'live-offerte.json'), 'utf8'));
const PAG = LIVE.sectie + LIVE.status;
const hash = n => LIVE.hashes[n];
const jsHash = LIVE.hashes.js;
const sprite = LIVE.sprite;

function maat(src) {
  const b = fs.readFileSync(path.join(REPO, src));
  if (src.endsWith('.svg')) return null;
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

// ---- de live teksten ----
const SEC = PAG.match(/<section class="b-na-bericht[^"]*" id="na-aanvraag"[\s\S]*?<\/section>/)[0];
const H2 = SEC.match(/<h2 id="na-aanvraag-kop">([\s\S]*?)<\/h2>/)[1];
const INTRO = SEC.match(/<p class="intro">([\s\S]*?)<\/p>/)[1];
const STAPPEN = [...SEC.matchAll(/<h3 class="b-na-bericht__titel">([\s\S]*?)<\/h3><p>([\s\S]*?)<\/p>/g)].map(m => ({ titel: m[1], tekst: m[2] }));
const BEL = SEC.match(/<p data-reveal class="belregel b-na-bericht__bel">[\s\S]*?<span>([\s\S]*?)<\/span><\/p>/)[1];
const WA = SEC.match(/<a class="wa-link"[\s\S]*?<\/a>/)[0];
const GOOGLE = SEC.match(/<a class="b-na-bericht__google"[\s\S]*?<\/a>/)[0];
// de bereikbaarheid staat al op de pagina (header), dus geen nieuwe tekst
const STATUS = PAG.match(/<span class="bereikbaar" data-bereikbaar[\s\S]*?<span class="bereikbaar__tekst"><\/span><\/span>/)[0];
if (STAPPEN.length !== 3 || !BEL || !WA || !GOOGLE || !STATUS) throw new Error('tekst niet gevonden');

// ---- bouwstenen ----
const ic = n => `<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-${n}"/></svg>`;
const kid = v => `kop-n${v}`;
const kop = (v, cls = '', o = {}) => {
  let h = H2;
  if (o.accent) { const w = h.split(' '); const l = w.pop(); h = `${w.join(' ')} <span class="accent">${l}</span>`; }
  return `<div class="kopgroep ${cls}"><h2 id="${kid(v)}">${h}</h2>${o.geenIntro ? '' : `<p class="intro">${INTRO}</p>`}</div>`;
};
const intro = (cls = '') => `<p class="intro ${cls}">${INTRO}</p>`;
const bel = (cls = '') => `<p class="n-bel ${cls}">${ic('telefoon')}<span>${BEL}</span></p>`;
const wa = () => WA;
let gTel = 0;
const google = (cls = '') => GOOGLE.replace('class="b-na-bericht__google"', `class="n-google ${cls}"`)
  .replace(/b-na-bericht__g\b/, 'n-google__g').replace(/b-na-bericht__sterren/, 'n-google__sterren')
  .replace(/sterknip2/g, `sterknip-n${++gTel}`);
// dezelfde Google-link in delen, voor een scoreschijf: href, sterren, "4,9", "uit 5 op Google"
const gDelen = () => {
  const g = google();
  return {
    href: g.match(/href="([^"]+)"/)[1],
    sterren: g.match(/<span class="sterren[\s\S]*?<\/svg><\/span>/)[0],
    cijfer: g.match(/<strong>([^<]+)<\/strong>/)[1],
    rest: g.match(/<\/strong>([^<]+)<\/span>/)[1].trim(),
    vh: g.match(/<span class="vh">[^<]*<\/span>/)[0],
  };
};
const status = (cls = '') => STATUS.replace('class="bereikbaar"', `class="bereikbaar n-status ${cls}"`);
const acties = (cls = '') => `<div class="n-acties ${cls}">${wa()}${google()}</div>`;
const voet = (cls = '') => `<div class="n-voet ${cls}">${bel()}${acties()}</div>`;
const nr = i => String(i + 1);
const nr2 = i => String(i + 1).padStart(2, '0');
// de stappen als echte lijst; o.voor(i) zet iets voor de tekst (schijf, voorwerp), o.na(i) erachter
const stappen = (cls, o = {}) => `<ol class="n-stappen ${cls}" role="list">${STAPPEN.map((s, i) => `<li class="n-stap">${o.voor ? o.voor(i) : `<span class="n-nr" aria-hidden="true">${nr(i)}</span>`}<div class="n-stap__tekst"><h3>${s.titel}</h3><p>${s.tekst}</p></div>${o.na ? o.na(i) : ''}</li>`).join('')}</ol>`;
const sec = (v, grond, inner, cls = '') => `<section class="sectie sectie--${grond} v n${v} ${cls}" aria-labelledby="${kid(v)}">
${inner}
</section>`;
const wrap = inner => `<div class="wrap">\n${inner}\n</div>`;

// de medewerker zonder kamer: 850x730, kruin y 52, bovenkant bureau y 522, rechts houdt het bureau op bij x 850
const VROUW = '/img/contact-klantenservice-boog-uit.webp';
const vrouw = (cls = '') => img(VROUW, `n-vrouw ${cls}`, ' aria-hidden="true"');
// dezelfde uitsnede met een bureau dat rechts zacht uitloopt (uitsnede.cjs), voor waar zij vrij staat
const vrouwZacht = (cls = '') => img('/img/offerte-klantenservice-uit.webp', `n-vrouw ${cls}`, ' aria-hidden="true"');
// echte fotovoorwerpen met het logo (zelfde reeks als /contact/): bellen, wat moet er mee, de offerte
const OBJ = ['/img/contact-echt/telefoon-480.webp', '/img/contact-echt/dozen-307.webp', '/img/contact-echt/envelop-432.webp'];
const obj = (i, cls = '') => img(OBJ[i], `n-obj n-obj--${i + 1} ${cls}`, ' aria-hidden="true"');
const merk = (cls = '') => img('/img/logo/dereus-beeldmerk.svg', cls, ' aria-hidden="true"');
const merkNeg = (cls = '') => img('/img/logo/dereus-beeldmerk-negatief.svg', cls, ' aria-hidden="true"');

const V = [];
const add = (n, naam, bron, uitleg, html) => V.push({ n, naam, bron, uitleg, html });

require('./ontwerpen.cjs')({ add, sec, wrap, kop, intro, bel, wa, google, gDelen, status, acties, voet, stappen, nr, nr2, ic, img, vrouw, vrouwZacht, obj, merk, merkNeg, STAPPEN, H2, INTRO, BEL });

// ---- pagina ----
const css = fs.readFileSync(path.join(__dirname, 'var.css'), 'utf8');
const navl = ['00', ...V.map(x => x.n)].map(n => `<a href="#v${n}">${n}</a>`).join('');
const kap = (n, naam, bron, uitleg) => `<div class="vkap" id="v${n}"><div class="wrap"><span class="vkap__nr">${n}</span><div><b>${naam}</b><small>${bron}</small><p>${uitleg}</p></div><span class="vkap__maat" data-maat></span></div></div>`;
// erboven staat op /offerte/ het formulier (Mist), eronder direct de Diepblauwe footer
const boven = `<div class="vctx vctx--mist" aria-hidden="true"><div class="wrap">Hierboven op /offerte/: het offerteformulier (Mist)</div></div>`;
const onder = `<div class="vctx" aria-hidden="true"><div class="wrap">Hieronder: de footer (Diepblauw)</div></div>`;
const live = SEC.replace('id="na-aanvraag"', 'id="na-aanvraag-live"').replace(/na-aanvraag-kop/g, 'na-aanvraag-kop-live').replace(/sterknip2/g, 'sterknip-live');

const html = `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=' js'</script>
<title>Zo gaat het verder · 15 ontwerpen · referentie A, B en C</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="/css/min/site.min.css?v=${hash('site')}">
<link rel="stylesheet" href="/css/min/na-bericht.min.css?v=${hash('na-bericht')}">
<style>
${css}
</style>
<script src="/js/site.js?v=${jsHash}" defer></script>
</head>
<body class="p-offerte">
${sprite}
<nav class="vnav" aria-label="Ontwerpen"><div class="wrap"><b>/offerte/ Zo gaat het verder · 15 ontwerpen</b><div class="vnav__links">${navl}</div></div></nav>
${kap('00', 'Het blok van de schermafdruk', 'Ter vergelijking, tot 29-09-2026 live', 'Het blok waarvan deze 15 ontwerpen uitgaan: Diepblauwe plaat, de foto met de kamer in een lijst en haar hoofd erboven. Sinds 29-09-2026 staat op /offerte/ weer de Koningsblauwe band met de man met de steekwagen (dezelfde teksten); een gekozen ontwerp komt in de plaats van die band.')}
${boven}
${live}
${onder}
${V.map(x => kap(x.n, x.naam, x.bron, x.uitleg) + '\n' + boven + '\n' + x.html(x.n) + '\n' + onder).join('\n')}
<div class="vkap vkap--eind"><div class="wrap"><p>Alle teksten zijn letterlijk die van /offerte/ (het blok "Zo gaat het verder", de bereikbaarheid uit de header). De medewerker staat overal zonder kamer: zij, haar bureau, het schrijfblok en de kop, zonder muur, raam, plant, scherm en toetsenbord. De voorwerpen bij de stappen zijn de echte fotovoorwerpen met het logo (telefoon, dozen, envelop). Elke bronklasse hierboven bestaat echt in de code van referentie A, B of C; in de De Reus-code komen die namen niet terug. Kies een nummer.</p></div></div>
<script>
(function(){
function meet(){document.querySelectorAll('[data-maat]').forEach(function(m){var s=m.closest('.vkap').nextElementSibling;while(s&&s.tagName!=='SECTION')s=s.nextElementSibling;if(!s)return;var h=Math.round(s.getBoundingClientRect().height);m.textContent='Blokhoogte '+h+' px';m.classList.toggle('is-hoog',h>730);});}
addEventListener('load',meet);addEventListener('resize',meet);
})();
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(REPO, '_ontwerpen/offerte-na-aanvraag-varianten.html'), html);
console.log('ok', html.length, V.length, STAPPEN.map(s => s.titel).join(' | '));
