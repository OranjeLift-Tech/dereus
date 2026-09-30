// Bouwt de verhuisblog van De Reus:  node _werk/blog/bouw-blog.cjs
// Schrijft ALLEEN in blog/: blog/index.html en blog/<slug>/index.html. Verder raakt hij niets aan.
//
// Kop, lade, voet, snelbalk (mcta), iconen en het offerteblok komen letterlijk uit een gebouwde pagina van de
// site (BRON, standaard kosten/index.html). Zo loopt de blog vanzelf mee met de header en footer van de site:
// na een nieuwe build van de site draai je dit script opnieuw. De opmaak komt uit /css/min/site.min.css en
// /css/min/offertepil.min.css (die schrijft build.py) plus blog/blog.css; het gedrag uit /js/site.js plus
// blog/blog.js. De tekst staat in _werk/blog/inhoud/.
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const HIER = __dirname;
const WORTEL = path.resolve(HIER, '..', '..');
const BRON = process.argv[2] || 'kosten/index.html';
const site = require('./inhoud/site.cjs');
const artikelen = require('./inhoud/artikelen.cjs').slice().sort((a, b) => b.datum.localeCompare(a.datum));
const maten = JSON.parse(fs.readFileSync(path.join(HIER, 'inhoud/beeldmaten.json'), 'utf8'));
const DOMEIN = 'https://www.verhuisbedrijfdereus.nl';

// zelfde cache-sleutel als build.py: sha1 van de inhoud (CRLF als LF), eerste 10 tekens
const hashVan = (rel) => crypto.createHash('sha1').update(fs.readFileSync(path.join(WORTEL, rel), 'utf8').replace(/\r\n/g, '\n')).digest('hex').slice(0, 10);
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const zonderTags = (s) => String(s).replace(/<[^>]+>/g, '');
const slug = (s) => zonderTags(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const MAANDEN = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december'];
const datum = (iso) => { const [j, m, d] = iso.split('-').map(Number); return `${d} ${MAANDEN[m - 1]} ${j}`; };
const telHref = `tel:${site.telHref}`;
const aantalTekst = (n) => (n === 1 ? '1 artikel' : `${n} artikelen`);
const amp = (s) => s.replace(/&(?!amp;)/g, '&amp;');

/* =====================================================================
   DELEN VAN DE SITE: uit de gebouwde bronpagina
   ===================================================================== */
const bron = fs.readFileSync(path.join(WORTEL, BRON), 'utf8').replace(/\r\n/g, '\n');
function pak(naam, re) {
  const m = bron.match(re);
  if (!m) throw new Error(`${BRON}: ${naam} niet gevonden. Is de opbouw van de pagina veranderd? Pas het patroon in bouw-blog.cjs aan.`);
  return m[0];
}
const zonderHuidig = (s) => s.replace(/\s+aria-current="[^"]*"/g, '');
const SITE = {
  jsKlasse: pak('js-klasse', /<script>document\.documentElement\.className[^<]*<\/script>/),
  iconen: bron.match(/<link rel="(?:icon|apple-touch-icon)"[^>]*>/g).join('\n'),
  preload: bron.match(/<link rel="preload"[^>]*>/g).join('\n'),
  themakleur: pak('theme-color', /<meta name="theme-color"[^>]*>/),
  telefoon: pak('format-detection', /<meta name="format-detection"[^>]*>/),
  sitejs: pak('site.js', /<script src="\/js\/site\.js[^"]*" defer><\/script>/),
  sprite: pak('sprite', /<svg class="sprite"[\s\S]*?<\/svg>/),
  header: zonderHuidig(pak('header', /<header class="header[\s\S]*?<\/header>/)),
  lade: zonderHuidig(pak('lade', /<div class="lade" id="lade"[\s\S]*?(?=\n<main)/)),
  voet: pak('footer', /<footer class="footer">[\s\S]*?(?=\n<\/body>)/),
  offerte: pak('offerteblok', /<section class="[^"]*\bb-offertepil\b[^"]*"[\s\S]*?<\/section>/)
    .replace('sectie--mist', 'sectie--wit'),
  // paginakop (.pk: foto, label, h1, intro, bellen en WhatsApp) plus de offertekaart eronder (.pk-pil),
  // zoals elke pagina van de site begint
  paginakop: pak('paginakop', /<section class="pk"[\s\S]*?<div class="pk-pil">[\s\S]*?(?=<section )/).trimEnd(),
  waLink: pak('wa-link', /<a class="wa-link" href="https:\/\/wa\.me\/[^"]*"[^>]*>[\s\S]*?<\/a>/),
};

// De paginakop met de tekst en de foto van de blog. Elke vervanging moet precies één keer raken.
function paginakop({ label, titel, intro, foto, positie }) {
  let t = SITE.paginakop;
  const vervang = (naam, re, door) => {
    if (!re.test(t)) throw new Error(`paginakop: ${naam} niet gevonden in ${BRON}`);
    t = t.replace(re, door);
  };
  vervang('foto', /(<img class="pk__foto" )[^>]*>/, `$1src="${foto.src}" alt="" width="${foto.w}" height="${foto.h}" style="object-position:${positie}" decoding="async" fetchpriority="high">`);
  vervang('label', /(<p class="label pk__label">)[^<]*(<\/p>)/, `$1${label}$2`);
  vervang('h1', /(<h1 class="pk__h1" id="kop-h1">)[^<]*(<\/h1>)/, `$1${titel}$2`);
  vervang('intro', /(<p class="intro pk__intro">)[^<]*(<\/p>)/, `$1${intro}$2`);
  return t;
}
// De kop van een artikel: dezelfde paginakop als de rest van de site (met de offertekaart eronder), met
// achter de waas een van de kopfoto's van de site zelf (per onderwerp, zie inhoud/site.cjs). De foto van het
// artikel zelf staat verderop als afdruk boven de tekst, dus die komt hier niet nog een keer.
// Kruimelpad boven het label, het onderwerp op de plek van het label, de lead als intro en daaronder
// schrijver, datum en leestijd.
// Diepte in de kop: de verhuizer van de site (img/verhuizer-*-uit.webp, altijd dezelfde man, één per pagina) staat
// op brede schermen scherp vóór de gedimde foto, rechts van de tekst, en komt achter de offertekaart omhoog.
const KOPFIGUUR = {
  inpakken: ['verhuizer-twee-dozen-uit', 407, 1200],
  planning: ['verhuizer-doos-schouder-uit', 489, 1200],
  kosten: ['verhuizer-doos-zijgreep-uit', 489, 1200],
  gezin: ['verhuizer-doos-deken-uit', 698, 1200],
  meubels: ['verhuizer-steekwagen-uit', 734, 1200],
  zakelijk: ['verhuizer-steekwagen-uit', 734, 1200],
};
function artikelkop(a) {
  const naam = onderwerpNaam(a.onderwerp);
  const kop = site.onderwerpen[a.onderwerp].kop;
  if (!kop) throw new Error(`Onderwerp ${a.onderwerp} heeft geen kopfoto in inhoud/site.cjs`);
  const figuur = KOPFIGUUR[a.onderwerp];
  if (!figuur) throw new Error(`Onderwerp ${a.onderwerp} heeft geen kopfiguur (KOPFIGUUR in bouw-blog.cjs)`);
  let t = SITE.paginakop;
  const vervang = (wat, re, door) => {
    if (!re.test(t)) throw new Error(`artikelkop: ${wat} niet gevonden in ${BRON}`);
    t = t.replace(re, door);
  };
  vervang('sectie', /<section class="pk"/, '<section class="pk pk--artikel"');
  vervang('foto', /(<img class="pk__foto" )[^>]*>/, `$1src="${kop.src}" alt="" width="${kop.w}" height="${kop.h}" style="object-position:${kop.positie}" decoding="async" fetchpriority="high">`);
  vervang('label', /<p class="label pk__label">[^<]*<\/p>/,
    `<nav class="kruimels" aria-label="Kruimelpad"><ol><li><a href="/">Home</a></li><li><a href="/blog/">Blog</a></li><li><a href="/blog/?onderwerp=${a.onderwerp}">${naam}</a></li></ol></nav>`
    + `<p class="label pk__label">${naam}</p>`);
  vervang('h1', /(<h1 class="pk__h1" id="kop-h1">)[^<]*(<\/h1>)/, `$1${a.titel}$2`);
  vervang('intro', /<p class="intro pk__intro">[^<]*<\/p>/, `<p class="intro pk__intro">${a.lead}</p>${meta(a, true)}`);
  // de figuur naast de tekst, binnen .pk__wrap (de tekst bevat zelf geen div, dus de eerste </div> sluit .pk__tekst)
  vervang('figuur', /(<div class="pk__tekst">[\s\S]*?<\/div>)/, (m0, tekst) => `${tekst}\n    <div class="pk__figuur" style="--bw:${figuur[1]};--bh:${figuur[2]}" aria-hidden="true"><img src="/img/${figuur[0]}.webp" alt="" width="${figuur[1]}" height="${figuur[2]}" decoding="async"></div>`);
  return t;
}
// Het menu-item Blog als huidige pagina markeren (de bronpagina markeert haar eigen item; dat is al weggehaald)
const huidigBlog = (html, waarde) => html
  .replace('<a class="nav__link" href="/blog/"', `<a class="nav__link" href="/blog/" aria-current="${waarde}"`)
  .replace('<a class="lade__link" href="/blog/"', `<a class="lade__link" href="/blog/" aria-current="${waarde}"`);

const V = {
  site: hashVan('css/min/site.min.css'),
  kop: hashVan('css/min/kop.min.css'),
  offerte: hashVan('css/min/offertepil.min.css'),
  // het vragenblok van de site (stijl "kaart" van /contact/), alleen geladen op artikelen met vragen
  vragen: hashVan('css/min/vragen.min.css'),
  gesprek: hashVan('css/min/vragen-gesprek.min.css'),
  css: hashVan('blog/blog.css'),
  js: hashVan('blog/blog.js'),
};

/* ---------- iconen: die van de site waar ze bestaan, anders een eigen lijnicoon (bi-) ---------- */
const SITE_ICOON = { tel: 'i-telefoon', pijl: 'i-pijl', vink: 'i-check', mail: 'i-mail', wa: 'i-whatsapp' };
const ic = (id) => (SITE_ICOON[id]
  ? `<svg class="ic" aria-hidden="true" focusable="false" overflow="visible"><use href="#${SITE_ICOON[id]}"/></svg>`
  : `<svg class="bic" aria-hidden="true" focusable="false"><use href="#bi-${id}"/></svg>`);
const LIJN = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const BLOGSPRITE = `<svg class="sprite" width="0" height="0" aria-hidden="true" focusable="false">
<symbol id="bi-zoek" ${LIJN}><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></symbol>
<symbol id="bi-klok" ${LIJN}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
<symbol id="bi-kalender" ${LIJN}><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></symbol>
<symbol id="bi-link" ${LIJN}><path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/></symbol>
</svg>`;
const knopTekst = (t, pijl = false) => `<span>${t}</span>${pijl ? ic('pijl') : ''}`;
const belKnop = (klasse, tekst = 'Bel ons') => `<a class="knop ${klasse}" href="${telHref}">${ic('tel')}<span>${tekst}</span></a>`;
const AVATAR = '/img/logo/dereus-beeldmerk.svg';
// De verhuizers van de site (img/*-uit) die per band boven de sectiekop uitstappen; per onderwerp een eigen reeks,
// om en om per band. De eerste band krijgt de eigen foto van het artikel (uit de foto), dus die telt hier niet mee.
const UIT = (b, w = 1080, h = 810, mx = 50) => ({ b, w, h, mx });          // losse uitsnede; mx = midden van de figuur in % van de breedte (voor de schijf erachter)
const FOTO = (b, alt, tekst) => ({ b, alt, tekst, foto: true });             // foto + uitsnede van de site (img/<b>.webp + -uit), gemeten in profielen.json
const F = {
  dragen: FOTO('dienst-woningontruiming-v2', 'Twee verhuizers van De Reus dragen samen een verhuisdoos', 'Onze verhuizers dragen alles voor u'),
  doos: FOTO('dienst-nationaal-v2', 'Verhuizer van De Reus met een verhuisdoos in zijn armen', 'Elke doos gaat door onze handen'),
  opslag: FOTO('dienst-opslag-v3', 'Verhuizer van De Reus zet een doos in de opslag', 'Ook tijdelijke opslag regelen wij'),
  kantoor: FOTO('dienst-zakelijk-v2', 'Twee verhuizers van De Reus met dozen en een bureaustoel', 'Kantoor of winkel: alles gaat mee'),
  bank: FOTO('dienst-particulier-v2', 'Twee verhuizers van De Reus dragen een bank naar buiten', 'Zwaar werk laat u aan ons over'),
  lift: FOTO('dienst-verhuislift', 'Twee verhuizers van De Reus bij een verhuislift', 'Met de verhuislift via het raam'),
  vast: FOTO('dienst-internationaal-v2b', 'Verhuizers van De Reus zetten ingepakte meubels vast met een spanband', 'Alles vast, niets schuift onderweg'),
  drie: UIT('helpen-drie-uit', 685, 591),
  adviseur: UIT('contact-adviseur-uit', 640, 954),
  montage: UIT('dienst-montage-v2-uit', 1080, 810, 67),   // de man staat rechts op het canvas
};
// 30-09 avond (verhuischecklist deel 02): de losse adviseur en het drietal op een grote goudgele schijf naast een
// afvinklijst oogden amateuristisch; die reeksen gebruiken nu alleen fotoparen, zodat elke band dezelfde plaat krijgt.
const FIGUREN = {
  inpakken: [F.dragen, F.doos, F.vast, F.lift],
  planning: [F.doos, F.dragen, F.vast, F.opslag],
  kosten: [F.doos, F.dragen, F.kantoor, F.vast],
  gezin: [F.doos, F.dragen, F.bank, F.opslag],
  meubels: [F.bank, F.montage, F.lift, F.vast],
  zakelijk: [F.kantoor, F.vast, F.opslag, F.lift],
};
// Uit de foto van de site: de geometrie komt uit het gemeten silhouet van de uitsnede (profielen.json: bovenkant
// en per 2 % van de breedte de bovenste rij). Het kader (4:3) valt binnen de foto, de uitsnede steekt er p boven uit.
const PROF = JSON.parse(fs.readFileSync(path.join(HIER, 'inhoud/profielen.json'), 'utf8'));
function geometrie(naam, { ar = 4 / 3, p = 0.12, band = 0.14, marge = 0.03 } = {}) {
  const Pr = PROF[naam]; if (!Pr) throw new Error(`Geen profiel voor ${naam} in inhoud/profielen.json`);
  const H = 0.75, fh = 1 / ar;
  for (let pp = p; pp >= 0.03 - 1e-9; pp -= 0.01) {
    for (let Z = 1; Z <= 2.4; Z += 0.01) {
      const t = Pr.top * H * Z + pp;
      if (H * Z - t < fh - 1e-9) continue;
      const grens = t / (H * Z);
      const uit = Pr.prof.map((y, i) => (y < grens ? i : -1)).filter((i) => i >= 0);
      const a = Math.min(...uit) / 50, b = (Math.max(...uit) + 1) / 50, breed = 1 / Z;
      const lo = Math.max(0, b + marge - breed), hi = Math.min(1 - breed, a - marge);
      if (lo > hi) break;
      const f0 = Math.min(hi, Math.max(lo, (Pr.x0 + Pr.x1) / 2 - breed / 2));
      return { z: +Z.toFixed(3), l: +(f0 * Z).toFixed(4), t: +t.toFixed(4),
        zicht: +(((t + band * fh) / (H * Z)) * 100).toFixed(2) };
    }
  }
  throw new Error('geen uitstap mogelijk voor ' + naam);
}
function fotopop(basis, alt, { p = 0.16 } = {}) {
  const g = geometrie(basis, { p });
  return `<div class="fotopop fotopop--plaat" style="--ar:4 / 3;--z:${g.z};--l:${g.l};--t:${g.t};--zicht:${g.zicht}%"><div class="fotopop__raam"><img class="fotopop__laag" src="/img/${basis}.webp" alt="${esc(alt)}" width="720" height="540" loading="lazy" decoding="async"></div><span class="fotopop__buiten" aria-hidden="true"><img class="fotopop__laag fotopop__uit" src="/img/${basis}-uit.webp" alt="" width="1080" height="810" loading="lazy" decoding="async"></span></div>`;
}

/* =====================================================================
   UIT DE FOTO: rekent zoom en verschuiving uit de alfa-omtrek van de uitsnede.
   P = hoeveel het onderwerp boven het kader uitsteekt (procent van de kaderbreedte).
   De onderkant van het kader valt op de onderkant van de foto, de bovenkant zo
   dat er precies P boven uitsteekt; horizontaal staat het onderwerp in het midden.
   ===================================================================== */
function popMaat(naam, P, arn) {
  const m = maten[naam];
  if (!m) throw new Error(`Geen beeldmaten voor ${naam} in inhoud/beeldmaten.json`);
  const H = 100 / arn;
  let T = (H + P) / (1 - m.s);
  let z = T / (100 * m.r);
  if (z < 1) { z = 1; T = 100 * m.r; }
  const y = Math.min(m.s * T + P, T - H);
  const x = Math.max(0, Math.min(m.cx * z * 100 - 50, z * 100 - 100));
  return { z, x, y };
}
const r3 = (n) => Math.round(n * 1000) / 1000;
function pop(naam, o = {}) {
  const arn = o.arn || 4 / 3;
  const { z, x, y } = o.maat || popMaat(naam, o.P ?? 22, arn);
  const groot = naam === 'verhuizers-kop' ? 1600 : 1400;
  const breed = o.breed || 380;
  const sizes = `(max-width: 767px) ${Math.round(z * 90)}vw, ${Math.round(z * breed)}px`;
  const bron = (map) => `src="/blog/img/${map}/${naam}.webp" srcset="/blog/img/${map}/${naam}-760.webp 760w, /blog/img/${map}/${naam}.webp ${groot}w" sizes="${sizes}"`;
  const laden = o.laden === 'eager' ? 'fetchpriority="high"' : 'loading="lazy"';
  const uit = `<img class="pop__laag" ${bron('uit')} alt="" ${laden} decoding="async">`;
  const zij = o.zij ? `;--uit-l:${o.zij[0]}%;--uit-r:${o.zij[1]}%` : '';
  return `<figure class="pop${o.afdruk ? ' pop--afdruk' : ''}" style="--arn:${r3(arn)};--z:${r3(z)};--x:${r3(x)};--y:${r3(y)}${zij}">`
    + `<div class="pop__raam"><img class="pop__laag" ${bron('foto')} alt="${esc(o.alt || '')}" ${laden} decoding="async"></div>`
    + `<div class="pop__boven" aria-hidden="true">${uit}</div>`
    + (o.onder ? `<div class="pop__onder" aria-hidden="true">${uit}</div>` : '')
    + `</figure>`;
}

/* ---------- bouwstenen voor in een artikel ---------- */
const h = {
  tip: (wie, tekst) => {
    const t = site.tippers[wie];
    if (!t) throw new Error(`Onbekende tipgever ${wie}`);
    return `<aside class="tip"><div class="tip__wie"><img class="tip__foto" src="/blog/img/team/${t.uit}.webp" alt="" width="560" height="420" loading="lazy"></div>`
      + `<div><p class="tip__label">${t.label}</p><p>${tekst}</p><cite>${t.wie}</cite></div></aside>`;
  },
  stappen: (lijst) => `<ol class="stappen">${lijst.map(([t, x]) => `<li><div><b>${t}</b>${x}</div></li>`).join('')}</ol>`,
  tabel: (koppen, rijen) => `<div class="tabelvak" role="region" aria-label="${esc(koppen.join(', '))}" tabindex="0"><table class="tabel"><thead><tr>${koppen.map((k) => `<th scope="col">${k}</th>`).join('')}</tr></thead><tbody>${rijen.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`,
  foto: (naam, alt, bijschrift) => `<figure class="foto"><div class="foto__afdruk"><img src="/blog/img/sfeer/${naam}.webp" alt="${esc(alt)}" width="1200" height="800" loading="lazy"><figcaption>${bijschrift}</figcaption></div><span class="plakband plakband--rechts" aria-hidden="true"></span></figure>`,
  // tabel met rechts een Diepblauw kader (voorwerp op goudgele schijf, tekst, knop), zodat de rechterhelft naast
  // de tabel niet leeg blijft (30-09, verhuisdozen-inpakken)
  tabelmet: (koppen, rijen, k) => `<div class="tabelrij">${h.tabel(koppen, rijen)}<aside class="tabelkader"><span class="tabelkader__schijf" aria-hidden="true"></span><img class="tabelkader__ding" src="/blog/img/voorwerp/${k.ding}.webp" alt="" style="--h:${k.h || '5.2rem'}" loading="lazy" decoding="async"><p class="tabelkader__label">${k.label}</p><p>${k.tekst}</p>${k.knop ? `<a class="knop knop--cta knop--klein" href="${k.href || '/offerte/'}"><span>${k.knop}</span>${ic('pijl')}</a>` : ''}</aside></div>`,
  // kleinere foto met rechts een witte tekstplaat en een etiket (30-09, verhuisdozen-inpakken)
  fotomet: (naam, alt, bijschrift, k) => `<div class="fotorij">${h.foto(naam, alt, bijschrift)}<div class="fotorij__vak">${k.etiket ? `<span class="fotorij__etiket" aria-hidden="true"><span class="plakband plakband--links"></span>${k.etiket}</span>` : ''}${k.label ? `<p class="fotorij__label">${k.label}</p>` : ''}${k.tekst}</div></div>`,
  citaat: (tekst, wie) => `<blockquote class="citaat"><p>${tekst}</p><cite>${wie}</cite></blockquote>`,
  afvink: (id, titel, items) => `<div class="afvink" data-afvink="${id}"><div class="afvink__kop"><b>${titel}</b><span class="afvink__stand" data-stand aria-live="polite">0 van ${items.length} klaar</span></div><ul>${items.map((t) => `<li><label><input type="checkbox"><span>${t}</span></label></li>`).join('')}</ul><button class="afvink__wis" type="button" data-wis>Alles leegmaken</button></div>`,
  schatter: () => `<div class="schatter" data-schatter><div class="schatter__velden"><p class="schatter__kop">Dozenschatter</p>`
    + `<label>Woonoppervlak (m²)<input name="m2" type="number" inputmode="numeric" min="10" max="600" value="90"></label>`
    + `<label>Kamers<input name="kamers" type="number" inputmode="numeric" min="1" max="20" value="3"></label>`
    + `<label>Bewoners<input name="bewoners" type="number" inputmode="numeric" min="1" max="12" value="2"></label>`
    + `<label>Hoeveel spullen<select name="spullen"><option value="licht">Weinig, ik woon licht</option><option value="gemiddeld" selected>Gemiddeld</option><option value="zwaar">Veel, ik bewaar graag</option></select></label></div>`
    + `<div class="schatter__uit" aria-live="polite"><small>Onze schatting</small><span class="schatter__getal" data-getal>...</span><span class="schatter__bereik" data-bereik></span><span class="schatter__detail" data-detail></span></div></div>`,
  aanbod: ({ label = 'Inpakservice', titel, tekst, knop }) => `<aside class="aanbod">${pop('verhuizers-kop', { P: 20, afdruk: true, alt: 'Twee verhuizers met verhuisdozen in een lege kamer', breed: 300 })}`
    + `<div><p class="label">${label}</p><h3>${titel}</h3><p>${tekst}</p><div class="knoppen-rij"><a class="knop knop--cta knop--klein" href="/offerte/">${knopTekst(knop, true)}</a> ${belKnop('knop--licht knop--klein')}</div></div></aside>`,
  // Dezelfde vragenregels als het blok #vragen op /contact/ (stijl "kaart", css/blok/vragen.css + vragen-gesprek.css);
  // artikelpagina zet er de blauwe kaart met de collega omheen. Gevraagd 30-09: "Deel 07 Veelgestelde vragen" in
  // de stijl van de contactpagina.
  vragen: (lijst) => `<div class="vragen__gesprek" data-reveal>${lijst.map(([v, a], i) => `<details class="vraag" id="vragen-${i + 1}" name="vragen"><summary><span class="vraag__nr" aria-hidden="true">${String(i + 1).padStart(2, '0')}</span><span class="vraag__tekst">${v}</span><span class="vraag__plus" aria-hidden="true"><svg class="ic" aria-hidden="true" focusable="false" overflow="visible"><use href="#i-plus"/></svg></span></summary><div class="vraag__antwoord"><p>${a}</p></div></details>`).join('')}</div>`,
};

/* ---------- pagina ---------- */
function pagina({ titel, beschrijving, pad, soort, klasse, inhoud, leesbalk = false, jsonld = [], beeld = '', huidig = 'page', vragenCss = false }) {
  return `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
${SITE.jsKlasse}
<title>${esc(titel)}</title>
<meta name="description" content="${esc(beschrijving)}">
<link rel="canonical" href="${DOMEIN}${pad}">
<meta property="og:type" content="${soort}">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="${site.naam}">
<meta property="og:url" content="${DOMEIN}${pad}">
<meta property="og:title" content="${esc(titel)}">
<meta property="og:description" content="${esc(beschrijving)}">
<meta property="og:image" content="${DOMEIN}/blog/img/foto/${beeld}.webp">
<meta name="twitter:card" content="summary_large_image">
${SITE.themakleur}
${SITE.telefoon}
${SITE.iconen}
${SITE.preload}
<link rel="stylesheet" href="/css/min/site.min.css?v=${V.site}">
<link rel="stylesheet" href="/css/min/kop.min.css?v=${V.kop}">
<link rel="stylesheet" href="/css/min/offertepil.min.css?v=${V.offerte}">
${vragenCss ? `<link rel="stylesheet" href="/css/min/vragen.min.css?v=${V.vragen}">
<link rel="stylesheet" href="/css/min/vragen-gesprek.min.css?v=${V.gesprek}">
` : ''}<link rel="stylesheet" href="/blog/blog.css?v=${V.css}">
${SITE.sitejs}
<script src="/blog/blog.js?v=${V.js}" defer></script>
${jsonld.map((j) => `<script type="application/ld+json">${JSON.stringify(j)}</script>`).join('\n')}
</head>
<body class="p p-blog ${klasse} header-transparant">
<a class="skiplink" href="#inhoud">Naar de inhoud</a>
${SITE.sprite}
${BLOGSPRITE}
${leesbalk ? '<div class="leesbalk" aria-hidden="true"><span></span></div>\n' : ''}${huidigBlog(SITE.header, huidig)}
${huidigBlog(SITE.lade, huidig)}
<main id="inhoud" tabindex="-1">
${inhoud}
</main>
${SITE.voet}
</body>
</html>
`;
}

/* ---------- kaarten ---------- */
function zoektekst(a) { return [a.titel, a.kort, a.zoek, site.onderwerpen[a.onderwerp].naam].join(' ').toLowerCase(); }
const onderwerpNaam = (k) => amp(site.onderwerpen[k].naam);
function kaart(a, { verborgen = false, laden } = {}) {
  const kant = maten[a.foto].cx > 0.5 ? 'links' : 'rechts';
  return `<li data-onderwerp="${a.onderwerp}" data-zoek="${esc(zoektekst(a))}"${a.uitgelicht ? ' data-uitgelicht' : ''}${verborgen ? ' hidden' : ''}>
      <article class="artikelkaart">
        ${pop(a.foto, { P: 22, alt: a.alt, breed: 380, laden, ...(a.pop || {}) })}
        <span class="plakband plakband--${kant}" aria-hidden="true"></span>
        <div class="artikelkaart__tekst">
          <a class="onderwerp" href="/blog/?onderwerp=${a.onderwerp}">${onderwerpNaam(a.onderwerp)}</a>
          <h3><a href="/blog/${a.slug}/">${a.titel}</a></h3>
          <p>${a.kort}</p>
          <div class="artikelkaart__voet">
            <p class="meta"><span class="meta__wie"><img src="${AVATAR}" alt="" width="30" height="30" loading="lazy"><b>${site.auteur.kort}</b></span><span class="meta__los">${ic('klok')}${a.leestijd} min</span></p>
            <a class="pijl" href="/blog/${a.slug}/" aria-label="Lees: ${esc(a.titel)}">Lees ${ic('pijl')}</a>
          </div>
        </div>
      </article>
    </li>`;
}
function ctakaart() {
  return `<li class="artikelrij__cta">
      <div class="ctakaart">
        ${pop('verhuizer-wagen', { P: 22, alt: 'Verhuizer tilt een doos uit de bus', breed: 380 })}
        <div class="ctakaart__tekst">
          <p class="label">Liever niet zelf sjouwen?</p>
          <h3>Wij pakken in, dragen en bouwen alles weer op</h3>
          <p>Een offerte op maat, gratis en vrijblijvend. Binnen 24 uur belt uw verhuisadviseur u.</p>
          <div class="knoppen-rij"><a class="knop knop--cta knop--klein" href="/offerte/">${knopTekst('Offerte aanvragen')}</a>${belKnop('knop--diep knop--klein')}</div>
        </div>
      </div>
    </li>`;
}
const meta = (a, lang = false) => `<p class="meta"><span class="meta__wie"><img src="${AVATAR}" alt="" width="34" height="34"><span><b>${site.auteur.naam}</b>${lang ? `<small>${site.auteur.rol}</small>` : ''}</span></span>`
  + `<span class="meta__los">${ic('kalender')}<time datetime="${a.datum}">${datum(a.datum)}</time></span><span class="meta__los">${ic('klok')}${a.leestijd} min lezen</span></p>`;

/* =====================================================================
   BLOGOVERZICHT
   Banden: Diepblauw kop, wit (tegels + uitgelicht), Koningsblauw (artikelen, met dak),
   Lucht (begin hier + checklist), wit (offerteblok), footer.
   ===================================================================== */
function blogoverzicht() {
  const uit = artikelen.find((a) => a.uitgelicht) || artikelen[0];
  const tellen = (k) => (k === 'alles' ? artikelen.length : artikelen.filter((a) => a.onderwerp === k).length);
  const rij = artikelen.map((a) => kaart(a, { verborgen: a === uit }));
  rij.splice(5, 0, ctakaart());   // de offertekaart als vijfde plek: midden in de tweede rij
  const top = ['wat-kost-een-verhuizing', 'verhuischecklist', 'verhuisdozen-inpakken', 'bank-de-trap-af', 'opslag-tijdens-verbouwing'].map((s) => artikelen.find((a) => a.slug === s));

  const inhoud = `${paginakop({
    label: 'Verhuisblog',
    titel: 'Verhuistips van de mensen die elke dag sjouwen',
    intro: 'Geen algemene lijstjes, maar wat onze verhuizers en verhuisadviseurs elke week tegenkomen. Van dozen tellen tot een bank de trap af.',
    foto: { src: '/blog/img/sfeer/bus-straat.webp', w: 1920, h: 1081 }, positie: '50% 60%',
  })}

<section class="onderwerpen" aria-labelledby="onderwerpen-titel">
  <div class="wrap">
    <div class="onderwerpen__kop">
      <p class="label">Onderwerpen</p>
      <h2 class="h2" id="onderwerpen-titel">Waar wilt u meer over lezen?</h2>
      <form class="zoek" role="search" data-zoek action="/blog/"><label class="vh" for="zoekveld">Zoek in de blog</label>${ic('zoek')}<input id="zoekveld" name="zoek" type="search" placeholder="Zoek op dozen, bank, kosten..." autocomplete="off"><button class="knop knop--cta knop--klein" type="submit"><span>Zoeken</span></button></form>
      <p class="onderwerpen__vaak"><span>Vaak gezocht:</span> <button type="button" data-zoekterm="dozen">dozen</button> <button type="button" data-zoekterm="kosten">kosten</button> <button type="button" data-zoekterm="opslag">opslag</button> <button type="button" data-zoekterm="verhuislift">verhuislift</button></p>
    </div>
    <ul class="onderwerpen__lijst">
    ${Object.entries(site.onderwerpen).map(([k, o]) => `<li><button class="tegel" type="button" data-filter="${k}" aria-pressed="${k === 'alles'}" aria-controls="artikelrij"><span class="tegel__schijf" aria-hidden="true"></span><img class="tegel__ding" src="/blog/img/voorwerp/${o.ding}.webp" alt="" style="--h:${o.h}"><span class="tegel__naam">${amp(o.naam)}</span><span class="tegel__aantal">${aantalTekst(tellen(k))}</span></button></li>`).join('\n    ')}
    </ul>
  </div>
</section>

<section class="uitgelicht" aria-labelledby="uitgelicht-titel" data-uitgelicht-blok>
  <div class="wrap uitgelicht__rooster">
    <div class="uitgelicht__beeld">
      ${pop(uit.foto, { P: 24, arn: 5 / 4, afdruk: true, alt: uit.alt, breed: 620 })}
      <span class="plakband plakband--rechts" aria-hidden="true"></span>
      <span class="uitgelicht__vlag" aria-hidden="true">Nieuw</span>
    </div>
    <div class="uitgelicht__tekst">
      <p class="label">Uitgelicht</p>
      <div><a class="onderwerp" href="/blog/?onderwerp=${uit.onderwerp}">${onderwerpNaam(uit.onderwerp)}</a></div>
      <h2 id="uitgelicht-titel"><a href="/blog/${uit.slug}/">${uit.titel}</a></h2>
      <p>${uit.kort}</p>
      ${meta(uit)}
      <a class="knop knop--blauw" href="/blog/${uit.slug}/">${knopTekst('Lees het artikel', true)}</a>
    </div>
  </div>
</section>

<section class="sectie sectie--blauw artikelen" id="artikelen" aria-labelledby="artikelen-titel">
  <div class="wrap">
    <div class="artikelen__kop">
      <div><p class="label" data-kop-label>Alle artikelen</p><h2 class="h2" id="artikelen-titel" data-kop-titel>Nieuw op de blog</h2></div>
      <div class="artikelen__stand">
        <p class="artikelen__aantal" data-aantal aria-live="polite">${aantalTekst(artikelen.length)}</p>
        <p class="artikelen__filter" data-filterbalk><button type="button" data-alles>Toon alle artikelen</button></p>
      </div>
    </div>
    <ul class="artikelrij" id="artikelrij" data-artikelrij>
    ${rij.join('\n    ')}
    </ul>
    <div class="artikelen__leeg" data-leeg hidden><p>Geen artikelen gevonden voor <b data-leeg-term>dit onderwerp</b>. Probeer een ander woord, of bel ons: dan zoeken we het samen uit.</p><button class="knop knop--licht knop--klein" type="button" data-alles><span>Toon alle artikelen</span></button></div>
  </div>
</section>

<section class="sectie sectie--lucht leesband" aria-labelledby="meest-titel">
  <div class="wrap leesband__rooster">
    <div>
      <p class="label">Begin hier</p>
      <h2 class="h2" id="meest-titel">Vijf artikelen om mee te beginnen</h2>
      <ol class="toplijst">
        ${top.map((a) => `<li><div><a href="/blog/${a.slug}/">${a.titel}</a><span>${onderwerpNaam(a.onderwerp)} &middot; ${a.leestijd} min lezen</span></div></li>`).join('\n        ')}
      </ol>
    </div>
    <div class="lijstpaneel">
      <img class="lijstpaneel__wekker" src="/blog/img/voorwerp/wekker.webp" alt="" width="340" height="440" loading="lazy">
      <div class="lijstvel" aria-hidden="true"><b>Verhuischecklist</b><ul><li class="is-af">Verhuizer gekozen</li><li class="is-af">Huur opgezegd</li><li class="is-af">Adreswijziging doorgegeven</li><li>Dozen ingepakt</li><li>Ontheffing aangevraagd</li></ul></div>
      <h2>De verhuischecklist, week voor week</h2>
      <p>Van acht weken vooraf tot de verhuisdag, in één lijst die u kunt afvinken. Uw browser onthoudt wat al klaar is.</p>
      <a class="knop knop--diep" href="/blog/verhuischecklist/">${knopTekst('Naar de checklist', true)}</a>
    </div>
  </div>
</section>

${SITE.offerte}`;

  return pagina({
    titel: `Verhuisblog: tips van onze verhuizers | ${site.naam}`,
    beschrijving: `Verhuistips van mensen die elke dag sjouwen: dozen inpakken, kosten, planning, opslag en verhuizen met kinderen of huisdieren. Door de verhuizers van ${site.naam}.`,
    pad: '/blog/', soort: 'website', klasse: 'p-blog-overzicht', inhoud, beeld: 'verhuizers-kop',
    jsonld: [{
      '@context': 'https://schema.org', '@type': 'Blog', name: `Verhuisblog van ${site.naam}`, url: `${DOMEIN}/blog/`,
      publisher: { '@type': 'MovingCompany', name: site.naam, url: `${DOMEIN}/` },
      blogPost: artikelen.map((a) => ({ '@type': 'BlogPosting', headline: a.titel, url: `${DOMEIN}/blog/${a.slug}/`, datePublished: a.datum, author: { '@type': 'Organization', name: site.naam } })),
    }],
  });
}

/* =====================================================================
   ARTIKEL
   Banden: kop, ankers (wit), per h2 een band (Lucht, wit, Mist om en om), slotband met schrijver en delen,
   Koningsblauw (lees ook, met dak), wit (offerteblok), footer.
   ===================================================================== */
function artikelpagina(a) {
  const inhoudsopgave = [];
  const tekst = a.tekst(h).replace(/<h2>(.*?)<\/h2>/g, (m, kopTekst) => {
    const id = slug(kopTekst);
    inhoudsopgave.push([id, zonderTags(kopTekst)]);
    return `<h2 id="${id}">${kopTekst}</h2>`;
  });
  const titelEnc = encodeURIComponent(`${a.titel} ${DOMEIN}/blog/${a.slug}/`);
  const verwant = [
    ...artikelen.filter((b) => b !== a && b.onderwerp === a.onderwerp),
    ...artikelen.filter((b) => b !== a && b.onderwerp !== a.onderwerp),
  ].slice(0, 3);
  const naam = onderwerpNaam(a.onderwerp);
  // Het lichaam is een reeks volle banden (wit, Koningsblauw, Lucht, Koningsblauw), naar de opbouw van de inpaktips-pagina
  // van referentie A: per h2 een band met links de sectiekop en rechts iemand die boven de band uitstapt (in de
  // eerste band de eigen foto van het artikel, daarna de verhuizers van de site). De bouwstenen staan in de
  // volle breedte. Geen zijbalk: de ankers staan onder de kop, delen en schrijver in de slotband.
  const delen = tekst.split(/(?=<h2 id=")/);
  const aanhef = delen.shift().trim();   // <p class="intro">: de intro van de eerste band
  const figuren = a.banden ? a.banden.map((k) => { if (!F[k]) throw new Error(`Onbekende bandfoto ${k}`); return F[k]; }) : (FIGUREN[a.onderwerp] || FIGUREN.inpakken);
  const eigenFoto = !a.banden;   // met a.banden (sleutels uit F) krijgt ook de eerste band een sitefoto in plaats van de eigen afdruk
  const BANDEN = ['wit', 'blauw', 'lucht', 'blauw'];   // om en om licht en Koningsblauw (met dak): duidelijke overgang per deel
  let nf = 0;
  let band = '';   // de kleur van de laatst gerenderde band, voor de slotband
  const secties = delen.map((d, i) => {
    const [, id, kopTekst] = d.match(/<h2 id="([^"]+)">([\s\S]*?)<\/h2>/);
    let rest = d.replace(/<h2[^>]*>[\s\S]*?<\/h2>\s*/, '');
    let intro = i === 0 ? aanhef : '';
    if (!intro) { const m = rest.match(/^<p>([\s\S]*?)<\/p>\s*/); if (m) { intro = `<p class="intro">${m[1]}</p>`; rest = rest.slice(m[0].length); } }
    // losse lijsten in de tekst worden een rij punten met een goudgele schijf (afvinklijsten niet)
    rest = rest.replace(/<ul>\s*((?:<li>[\s\S]*?<\/li>\s*)+)<\/ul>/g, (m, li) => (m.includes('<input') ? m
      : `<ul class="punten">${li.replace(/<li>([\s\S]*?)<\/li>/g, (x, t) => `<li><span class="punt__ic" aria-hidden="true">${ic('vink')}</span><p>${t.trim()}</p></li>`)}</ul>`));
    if (i === delen.length - 1 && !tekst.includes('class="aanbod"')) {
      rest += h.aanbod({ label: 'Offerte op maat', titel: 'Liever uit handen geven?', tekst: 'U wijst aan wat mee moet, wij pakken in, dragen en bouwen alles weer op. Een offerte op maat, gratis en vrijblijvend. Binnen 24 uur belt uw verhuisadviseur u.', knop: 'Offerte aanvragen' });
    }
    const vragen = rest.includes('class="vragen__gesprek"');
    let figuur = '';
    if (i === 0 && eigenFoto) {
      figuur = `<div class="arttop__pop">${pop(a.foto, { P: 24, arn: 4 / 3, afdruk: true, alt: a.alt, breed: 460, laden: 'eager', ...(a.pop || {}) })}<span class="plakband plakband--${maten[a.foto].cx > 0.5 ? 'links' : 'rechts'}" aria-hidden="true"></span></div>`;
    } else if (!vragen) {   // ook de band met het aanbod krijgt rechts een foto; het aanbod staat er met clear:both onder
      const f = figuren[nf++ % figuren.length];
      figuur = f.foto
        ? `<figure class="arttop__foto">${fotopop(f.b, f.alt)}<figcaption>${f.tekst}</figcaption></figure>`
        : `<figure class="arttop__figuur" style="--mx:${f.mx}%" aria-hidden="true"><img src="/img/${f.b}.webp" alt="" width="${f.w}" height="${f.h}" loading="lazy" decoding="async"></figure>`;
    }
    const nr = String(i + 1).padStart(2, '0');
    if (vragen) {
      // De vragen staan niet in een band maar in de Koningsblauwe kaart van #vragen op /contact/: links de collega
      // met headset die boven de kaart uitsteekt met de pil "Nu bereikbaar", rechts de kop, de regels en de belrij.
      // De sectiekleur wisselt met de band ervoor, zoals de banden onderling; de slotband kijkt daar weer naar.
      band = BANDEN[(i - 1 + BANDEN.length) % BANDEN.length] === 'wit' ? 'lucht' : 'wit';
      const kaart = rest.match(/<div class="vragen__gesprek"[\s\S]*?<\/details><\/div>/)[0];
      const overig = rest.replace(kaart, '').trim();
      return `<section class="sectie sectie--${band} b-vragen b-vragen--gesprek b-vragen--kaart" id="vragen" aria-labelledby="${id}">
  <div class="wrap vragen__in">
    <div class="vragen__zij">
      <div class="kopgroep"><p class="label">Deel ${nr}</p><h2 id="${id}">${kopTekst}</h2>${intro}</div>
      <p class="vragen__beller"><span class="vragen__belvraag">Staat uw vraag er niet bij?</span><span class="vragen__belnr"><a href="${telHref}">Bel ${site.tel}</a>${SITE.waLink}</span></p>
      <div class="vragen__podium"><span class="vragen__staan" aria-hidden="true"><img class="vragen__collega" src="/img/contact-uit.webp" alt="" width="1200" height="800" loading="lazy" decoding="async"></span><span class="bereikbaar vragen__nu" data-bereikbaar data-open="Nu bereikbaar" data-dicht="Nu gesloten" data-morgen="Morgen weer bereikbaar vanaf {tijd} uur" hidden><span class="bereikbaar__stip" aria-hidden="true"></span><span class="bereikbaar__tekst"></span></span></div>
    </div>
    ${kaart}
  </div>${overig ? `\n  <div class="wrap tekst">${overig}</div>` : ''}
</section>`;
    }
    // a.kopdingen[id] = voorwerp uit blog/img/voorwerp: staat op een goudgele schijf rechts van de kop, in de
    // rechterkolom boven de fotoplaat (rooster met stappen, zie blog.css "Voorwerp naast de kop")
    const kd = a.kopdingen && a.kopdingen[id];
    const ding = kd ? `<div class="artding" aria-hidden="true"><span class="artding__schijf"></span><img class="artding__ding" src="/blog/img/voorwerp/${kd.ding || kd}.webp" alt="" style="--h:${kd.h || '8rem'}" loading="lazy" decoding="async"></div>` : '';
    band = BANDEN[i % BANDEN.length];
    return `<section class="sectie sectie--${band} artsectie${i === 0 ? ' artsectie--eerste' : ''}${vragen ? ' artsectie--midden' : ''}" aria-labelledby="${id}">
  <div class="wrap tekst">
    <div class="arttop${figuur ? '' : ' arttop--breed'}">
      ${figuur}   ${""/* figuur vóór de kop: als float staat hij dan naast de kop (30-09) */}
      ${ding}<div class="artkop"><p class="label">Deel ${nr}</p><h2 id="${id}">${kopTekst}</h2>${intro}</div>
    </div>
${rest.trim()}
  </div>
</section>`;
  });
  const voetband = band === 'lucht' ? 'wit' : 'lucht';

  const inhoud = `<article class="artikel" data-slug="${a.slug}">
  ${artikelkop(a)}

  <div class="ankerrij"><div class="wrap">
    <nav class="ankers" data-inhoud aria-label="In dit artikel">
      <p class="ankers__kop">In dit artikel <span>${a.leestijd} min lezen</span></p>
      <ol>${inhoudsopgave.map(([id, t], i) => `<li><a href="#${id}"><b>${String(i + 1).padStart(2, '0')}</b>${t}</a></li>`).join('')}</ol>
    </nav>
  </div></div>

  <div class="artikel__lichaam" data-tekst>
${secties.join('\n')}
  </div>

  <section class="sectie sectie--${voetband} artvoet" aria-label="Over de schrijver">
    <div class="wrap artvoet__rooster">
      <div class="auteur">
        <div class="auteur__beeld"><span class="auteur__schijf" aria-hidden="true"></span><img class="auteur__foto" src="${AVATAR}" alt="Beeldmerk van ${site.naam}" width="1000" height="509" loading="lazy"></div>
        <div><p class="label">Geschreven door</p><h2>${site.auteur.naam}</h2><p>${site.auteur.bio}</p><div class="knoppen-rij">${belKnop('knop--diep knop--klein', site.tel)}${SITE.waLink}<a class="pijl" href="/over-ons/">Over De Reus ${ic('pijl')}</a></div></div>
      <div class="artvoet__zij">
        <div class="deel">
          <p class="deel__label">Delen</p>
          <button class="deelknop" type="button" data-kopieer aria-label="Kopieer de link">${ic('link')}</button>
          <a class="deelknop" href="https://wa.me/?text=${titelEnc}" aria-label="Deel via WhatsApp">${ic('wa')}</a>
          <a class="deelknop" href="mailto:?subject=${encodeURIComponent(a.titel)}&amp;body=${titelEnc}" aria-label="Deel via e-mail">${ic('mail')}</a>
        </div>
        <div class="labels"><a class="onderwerp" href="/blog/?onderwerp=${a.onderwerp}">${naam}</a><a class="onderwerp" href="/blog/">Alle artikelen</a></div>
      </div>
      </div>
    </div>
  </section>
</article>

<section class="sectie sectie--blauw artikelen gerelateerd" aria-labelledby="verwant-titel">
  <div class="wrap">
    <div class="artikelen__kop"><div><p class="label">Lees ook</p><h2 class="h2" id="verwant-titel">Meer over ${naam.toLowerCase()} en verhuizen</h2></div><a class="knop knop--licht knop--klein" href="/blog/">${knopTekst('Alle artikelen', true)}</a></div>
    <ul class="artikelrij">
    ${verwant.map((b) => kaart(b)).join('\n    ')}
    </ul>
  </div>
</section>

${SITE.offerte}`;

  return pagina({
    titel: `${a.titel} | ${site.naam}`,
    beschrijving: a.kort, pad: `/blog/${a.slug}/`, soort: 'article', klasse: 'p-blog-artikel', inhoud, leesbalk: true, beeld: a.foto, huidig: 'true',
    vragenCss: inhoud.includes('b-vragen--kaart'),
    jsonld: [
      { '@context': 'https://schema.org', '@type': 'BlogPosting', headline: a.titel, description: a.kort, datePublished: a.datum, dateModified: a.datum,
        image: `${DOMEIN}/blog/img/foto/${a.foto}.webp`, author: { '@type': 'Organization', name: site.naam, url: `${DOMEIN}/` },
        publisher: { '@type': 'MovingCompany', name: site.naam, url: `${DOMEIN}/` }, mainEntityOfPage: `${DOMEIN}/blog/${a.slug}/` },
      { '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Home', item: `${DOMEIN}/` },
        { '@type': 'ListItem', position: 2, name: 'Blog', item: `${DOMEIN}/blog/` },
        { '@type': 'ListItem', position: 3, name: a.titel, item: `${DOMEIN}/blog/${a.slug}/` }] },
    ],
  });
}

/* ---------- schrijven: alleen binnen blog/ ---------- */
const BLOG = path.join(WORTEL, 'blog');
const schrijf = (rel, html) => {
  const doel = path.join(BLOG, rel);
  if (!doel.startsWith(BLOG + path.sep)) throw new Error(`weigert buiten blog/ te schrijven: ${doel}`);
  fs.mkdirSync(path.dirname(doel), { recursive: true });
  fs.writeFileSync(doel, html);
  console.log('  ', path.relative(WORTEL, doel).replace(/\\/g, '/'));
};
// huisregels controleren: geen gedachtestreepjes en geen je/jij/jouw in de tekst (de site zegt "u")
for (const a of artikelen) {
  const tekst = zonderTags([a.titel, a.kort, a.lead, a.tekst(h)].join(' '));
  if (/[–—]/.test(tekst)) console.warn(`let op: gedachtestreepje in ${a.slug}`);
  const je = tekst.match(/\b(je|jij|jou|jouw)\b/gi);   // "jullie" mag: zo spreekt de klant ons aan in een vraag
  if (je) console.warn(`let op: ${je.join(', ')} in ${a.slug} (de site zegt "u")`);
}
console.log(`Bouwen (kop en voet uit ${BRON}):`);
schrijf('index.html', blogoverzicht());
for (const a of artikelen) schrijf(`${a.slug}/index.html`, artikelpagina(a));
console.log(`Klaar: ${artikelen.length} artikelen.`);
