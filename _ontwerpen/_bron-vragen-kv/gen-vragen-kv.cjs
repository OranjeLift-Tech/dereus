// 15 ontwerpen voor het vragenblok (#vragen) op /contact/ en /werkwijze/, op basis van referentie A en referentie B
// node gen-vragen-kv.cjs  ->  _ontwerpen/vragen-referentie-ronde1.html
// Teksten komen letterlijk uit contact/index.html en werkwijze/index.html (sectie b-vragen).
const fs = require('fs');
const path = require('path');
const REPO = path.resolve(__dirname, '../..');
const lees = p => fs.readFileSync(path.join(REPO, p), 'utf8');
const PAG = { contact: lees('contact/index.html'), werkwijze: lees('werkwijze/index.html') };
const hash = n => (PAG.contact.match(new RegExp(`/css/min/${n}\\.min\\.css\\?v=([0-9a-f]+)`)) || [])[1];
const jsHash = (PAG.contact.match(/\/js\/site\.js\?v=([0-9a-f]+)/) || [])[1];
const sprite = PAG.contact.match(/<svg class="sprite"[\s\S]*?<\/svg>/)[0];

// breedte x hoogte uit de webp-kop, zodat width/height altijd kloppen
function maat(src) {
  const b = fs.readFileSync(path.join(REPO, src));
  const soort = b.toString('ascii', 12, 16);
  if (soort === 'VP8X') return [1 + b.readUIntLE(24, 3), 1 + b.readUIntLE(27, 3)];
  if (soort === 'VP8 ') return [b.readUInt16LE(26) & 0x3fff, b.readUInt16LE(28) & 0x3fff];
  if (soort === 'VP8L') { const n = b.readUInt32LE(21); return [(n & 0x3fff) + 1, ((n >> 14) & 0x3fff) + 1]; }
  throw new Error('geen webp: ' + src);
}
const img = (src, cls = '', extra = '') => { const [w, h] = maat(src); return `<img class="${cls}" src="${src}" alt="" width="${w}" height="${h}" loading="lazy" decoding="async"${extra}>`; };

// ---- de live teksten ----
function data(p) {
  const t = PAG[p];
  const sec = t.match(/<section class="sectie[^"]*b-vragen[\s\S]*?<\/section>/)[0];
  const vragen = [...sec.matchAll(/<span class="vraag__tekst">([\s\S]*?)<\/span><span class="vraag__plus"[\s\S]*?<div class="vraag__antwoord">([\s\S]*?)<\/div>\s*<\/details>/g)]
    .map(m => ({ tekst: m[1], antwoord: m[2] }));
  return {
    p, sec,
    grond: (sec.match(/sectie--(\w+)/) || [])[1],
    label: sec.match(/<p class="label">([\s\S]*?)<\/p>/)[1],
    h2: sec.match(/<h2 id="vragen-kop">([\s\S]*?)<\/h2>/)[1],
    status: sec.match(/<span class="bereikbaar[^>]*>[\s\S]*?<span class="bereikbaar__tekst"><\/span><\/span>/)[0],
    zin: sec.match(/<\/span>\s*<p>([^<]*)<\/p>\s*<a class="knop/)[1],
    wa: sec.match(/<a class="wa-link"[\s\S]*?<\/a>/)[0],
    vragen,
  };
}
const D = { contact: data('contact'), werkwijze: data('werkwijze') };

// ---- beeld per pagina ----
// een 3D-voorwerp per vraag (zelfde renders als de contactkaarten en /kosten/)
const OBJ = {
  contact: ['/img/contact-3d/klok.webp', '/img/contact-3d/telefoon.webp', '/img/contact-3d/envelop.webp', '/img/contact-3d/formulier.webp'],
  werkwijze: ['/img/contact-3d/formulier.webp', '/img/contact-3d/schild.webp', '/img/contact-3d/headset.webp', '/img/contact-3d/doos.webp', '/img/kosten-kalender/pen.webp'],
};
// de medewerker. Nooit iemand die al op dezelfde pagina staat: /contact/ heeft de klantenservice (blok erboven),
// de adviseur (in helpen-drie) en de verhuizer-reeks al, dus daar het trio helpen-wij-u-snel (nog nergens gebruikt;
// aanvraag-foto-uit viel af: daar staat nog achtergrond in). /werkwijze/ heeft het team met dozen en
// verhuizer-doos-schouder, dus daar de vaste verhuisadviseur.
const MENS = { contact: 'drie', werkwijze: 'adv' };
const MENS_SRC = { drie: '/img/helpen-wij-u-snel.webp', adv: '/img/contact-adviseur-uit.webp' };
// foto + uitsnede met dezelfde verhouding (voor "persoon steekt boven de foto uit"). /werkwijze/ heeft al twee
// bankscènes (dienst-particulier, verhuisdag-uit), dus daar de woningontruiming; /contact/ het kantoor (zakelijk).
const FOTO = {
  contact: { foto: '/img/dienst-zakelijk-v2.webp', uit: '/img/dienst-zakelijk-v2-uit.webp', cx: '50%' },
  werkwijze: { foto: '/img/dienst-woningontruiming-v2.webp', uit: '/img/dienst-woningontruiming-v2-uit.webp', cx: '56%' },
};

// ---- bouwstenen ----
const ic = n => `<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-${n}"/></svg>`;
const kid = (v, d) => `kop-${v}-${d.p}`;
const kop = (v, d, cls = '', accent = false) => {
  let h = d.h2;
  if (accent) { const w = h.split(' '); const laatste = w.pop(); h = `${w.join(' ')} <span class="accent">${laatste}</span>`; }
  return `<div class="kopgroep ${cls}"><p class="label">${d.label}</p><h2 id="${kid(v, d)}">${h}</h2></div>`;
};
const status = (d, cls = '') => d.status.replace('bereikbaar vragen__status', `bereikbaar q-status ${cls}`.trim());
const zin = (d, cls = '') => `<p class="q-zin ${cls}">${d.zin}</p>`;
const bel = (cls = '') => `<a class="q-bel ${cls}" href="tel:+31850005647">${ic('telefoon')}<span>Bel 085 000 5647</span></a>`;
const knoppen = (d, cls = '') => `<div class="q-knoppen ${cls}">${bel()}${d.wa}</div>`;
const belrij = (d, cls = '', stCls = '') => `<div class="q-belrij ${cls}">${status(d, stCls)}${zin(d)}${knoppen(d)}</div>`;
const obj = (d, i, cls = '') => img(OBJ[d.p][i], `q-obj ${cls}`.trim());
const mens = (d, cls = '', deel = 'boven') => `<span class="mens mens--${MENS[d.p]} mens--${deel} ${cls}" aria-hidden="true">${img(MENS_SRC[MENS[d.p]])}</span>`;
// --cx (waar de persoon horizontaal staat) staat in de css per pagina, zodat een ontwerp het kan bijstellen
const pop = (d, cls = '') => { const f = FOTO[d.p]; return `<span class="pop ${cls}" aria-hidden="true"><span class="pop__raam">${img(f.foto, 'pop__foto')}</span><span class="pop__boven">${img(f.uit, 'pop__uit')}</span></span>`; };
// een vraag: echte <details>, per blok dezelfde name zodat er één tegelijk openstaat
const vraag = (v, d, i, o = {}) => {
  const q = d.vragen[i]; const nr = String(i + 1).padStart(2, '0');
  return `<details class="q ${o.cls || ''}" name="q${v}${d.p}"${o.open && i === 0 ? ' open' : ''}${o.stijl ? ` style="${o.stijl(i)}"` : ''}>
<summary>${o.voor ? o.voor(i) : ''}${o.geenNr ? '' : `<span class="q__nr" aria-hidden="true">${nr}</span>`}<span class="q__tekst">${q.tekst}</span><span class="q__plus" aria-hidden="true">${ic('plus')}</span></summary>
<div class="q__antwoord">${q.antwoord}</div>
</details>`;
};
const lijst = (v, d, cls, o = {}) => `<div class="q-lijst ${cls}">${d.vragen.map((_, i) => vraag(v, d, i, o)).join('')}</div>`;
const sec = (v, d, grond, inner, cls = '') => `<section class="sectie sectie--${grond || d.grond} v x${v} ${cls}" aria-labelledby="${kid(v, d)}">
<div class="wrap">
${inner}
</div>
</section>`;

const V = [];
const add = (n, naam, bron, uitleg, html) => V.push({ n, naam, bron, uitleg, html });

add('01', 'Een 3D-voorwerp bij elke vraag', 'Referentie B /veelgestelde-vragen/ (.sgfaq-kop__3d, .sgfaq-snel img, .sgdp-vraag)',
  'Zoals de vragenpagina van referentie B: links de kop met een 3D-voorwerp erboven, rechts witte vraagkaarten met een haarlijn en een rond plusje. Nieuw is dat elke vraag zijn eigen voorwerp heeft (klok, telefoon, envelop, formulier; op /werkwijze/ klembord, schild, headset, doos, kalender). Het voorwerp staat op een gele schijf en steekt boven de kaart uit.',
  (v, d) => sec(v, d, null, `<div class="x01__raster"><div class="x01__kop">${img('/img/contact-3d/headset.webp', 'x01__3d')}${kop(v, d)}${belrij(d, '', 'q-status--pil')}</div>
${lijst(v, d, 'x01__lijst', { geenNr: true, voor: i => `<span class="x01__schijf" aria-hidden="true">${obj(d, i)}</span>` })}</div>`));

add('02', 'Paneel met de medewerker erboven', 'Referentie B /contact/ (.sgct, .sgct__kaarten, .sgct-kaart)',
  'Het blok "Rechtstreeks contact met je regionale installateur": een breed paneel met een zacht verloop van Lucht naar Crème, de kop links, de belknoppen in het midden en rechts de medewerker die boven het paneel uitkomt (op /werkwijze/ de verhuisadviseur, op /contact/ drie verhuizers die nog niet op die pagina staan). Daaronder de vragen in twee kolommen als witte kaarten met een gele onderrand, zoals de contactkaarten van referentie B.',
  (v, d) => sec(v, d, null, `<div class="x02__paneel"><div class="x02__tekst">${kop(v, d)}${belrij(d, '', 'q-status--pil')}</div>${mens(d, 'x02__mens')}</div>
${lijst(v, d, 'x02__lijst')}`));

add('03', 'Eén kaart: medewerker boven een schuin paneel', 'Referentie B _partials/offerteblok.html (.ob__zij, .ob__fig, .ob__paneel)',
  'De opzet van het offerteblok van referentie B, die "Zo helpen wij u snel" op /contact/ ook heeft: één witte kaart met een blauwe rand. Links steekt de medewerker boven de kaart uit en loopt een schuin Koningsblauw paneel over de heup met de kop, de bereikbaarheid en de knoppen. Rechts de vragen als rijen met dunne lijnen.',
  (v, d) => sec(v, d, null, `<div class="x03__kaart"><div class="x03__zij"><span class="x03__beeldvak">${mens(d, 'x03__mens')}</span><div class="x03__paneel">${kop(v, d, '', true)}${belrij(d, '', 'q-status--donker')}</div></div>
${lijst(v, d, 'x03__lijst')}</div>`));

add('04', 'Venster met boog', 'Referentie A /contact/ #na-uw-aanvraag (.venster, .venster__boog, .venster__persoon, .venster__mark)',
  'Het blok "Uw aanvraag komt bij een mens terecht" van referentie A, als Diepblauwe kaart in de witte sectie (geen extra band op de pagina): links de kop, de vragen als lichte regels met gele nummers en de knoppen; rechts een Crème boog met een gouden binnenlijn waar de medewerker in staat. Linksonder het beeldmerk heel zacht, zoals het referentie A-merk.',
  (v, d) => sec(v, d, null, `<div class="x04__kaart"><img class="x04__merk" src="/img/logo/dereus-beeldmerk-negatief.svg" alt="" aria-hidden="true"><div class="x04__tekst">${kop(v, d)}
${lijst(v, d, 'x04__lijst')}${belrij(d, 'x04__bel', 'q-status--donker')}</div><div class="x04__venster" aria-hidden="true"><span class="x04__boog"></span>${mens(d, 'x04__mens', 'lang')}</div></div>`));

add('05', 'Belkaart op een gele band, medewerker erboven', 'Referentie B /contact/ (.sgm, .sgm__band, .sgm__kaart, .sgm__figuur, .sgm__pil, .sgm__3d)',
  'Het blok "Bel ons, videobel ons of kom langs" van referentie B: links de kop en de vragen, rechts een witte kaart op een gele band, met de medewerker die boven de kaart uitkomt, een 3D-telefoon op de hoek en de bereikbaarheid als pil rechtsboven (waar referentie B "Vrijblijvend" heeft).',
  (v, d) => sec(v, d, null, `<div class="x05__raster"><div class="x05__links">${kop(v, d)}${lijst(v, d, 'x05__lijst')}</div>
<div class="x05__rechts"><span class="x05__band" aria-hidden="true"></span><div class="x05__kaart">${mens(d, 'x05__mens')}${img('/img/contact-3d/telefoon.webp', 'x05__3d')}${status(d, 'q-status--pil x05__pil')}${zin(d, 'x05__zin')}${knoppen(d, 'x05__knoppen')}</div></div></div>`));

add('06', 'Referentie A-lijst op een witte plaat', 'Referentie A homepage #faq en /contact/ #contact-faq (.ring, .faq, .faq__tk, .art-4)',
  'Het FAQ-blok van referentie A: kop in het midden, genummerde regels over de volle breedte met dunne lijnen en een dun plusje, de witte cirkellijn (.ring) op de achtergrond en rechtsboven een beeld (bij referentie A de vogel, hier de 3D-vraagtekens). Voor de diepte staan de regels op één witte plaat, en onderaan staat de knoppenrij zoals referentie A "Andere vraag? App ons".',
  (v, d) => sec(v, d, 'lucht', `<span class="x06__ring" aria-hidden="true"></span>${kop(v, d, 'kopgroep--midden x06__kop')}
<div class="x06__plaat">${img('/img/kaart-3d/vraagtekens.webp', 'x06__vt')}${lijst(v, d, 'x06__lijst')}</div>
${belrij(d, 'x06__bel', 'q-status--pil')}`));

add('07', 'Goudgele band met een foto-afdruk', 'Referentie B /contact/ #toennu (.sgt__fotos, .sgt__foto, .sgt__uit) + gele band van /werkwijze/ #na-de-verhuizing',
  'Ontwerp 07, aangepast op verzoek: het geel is geen blok meer maar vult de hele sectie van rand tot rand, met hetzelfde geelverloop als de gele band op /werkwijze/. Links een schuine foto-afdruk met witte rand waar de persoon bovenuit stapt (bij referentie B .sgt__uit), met de 3D-headset tegen de hoek. Rechts de kop in Diepblauw, de vragen als witte kaarten en de knoppen.',
  (v, d) => sec(v, d, 'wit', `<div class="x07__paneel"><div class="x07__fotos"><span class="x07__afdruk">${pop(d, 'x07__pop')}</span>${img('/img/contact-3d/headset.webp', 'x07__3d')}</div>
<div class="x07__rechts">${kop(v, d)}${lijst(v, d, 'x07__lijst')}${belrij(d, 'x07__bel', 'q-status--pil')}</div></div>`, 'x07__band'));

add('08', 'Foto links, blauw paneel met de vragen', 'Referentie A /contact/ #offerte (.leadblock__card, .leadblock__media, .leadblock__panel)',
  'Het leadblock van referentie A: één afgeronde kaart, links een echte foto over de volle hoogte, rechts een gekleurd paneel met een lichtvlek rechtsboven. Hier het Koningsblauwe paneel met de kop, de vragen als lichte regels met een geel plusje en de knoppen. De persoon op de foto steekt boven de kaart uit.',
  (v, d) => sec(v, d, null, `<div class="x08__kaart"><div class="x08__media">${pop(d, 'x08__pop')}</div><div class="x08__paneel">${kop(v, d)}
${lijst(v, d, 'x08__lijst')}${belrij(d, 'x08__bel', 'q-status--donker')}</div></div>`));

add('09', 'Blauwe kaarten met een geel nummerblok', 'Referentie A homepage #diensten (.dienst, .dienst__nr, .dienst:hover)',
  'De dienstkaarten van referentie A: gekleurde kaarten met het nummer als geel blok in de hoek, bij hover een donkerder kaart die 3px omhoog komt. Hier Koningsblauw met het 3D-voorwerp dat rechtsboven uit de kaart steekt; het antwoord klapt in de kaart open. De kop en de knoppen staan erboven, naast elkaar.',
  (v, d) => sec(v, d, null, `<div class="x09__top">${kop(v, d)}${belrij(d, 'x09__bel', 'q-status--pil')}</div>
${lijst(v, d, `x09__lijst x09__lijst--${d.vragen.length}`, { voor: i => obj(d, i, 'x09__obj') })}`));

add('10', 'Grote kaart met omlijnde rijen en een foto', 'Referentie B homepage #prijzen (.sgpr__kaart, .sgpr__rijen, .sgpr-rij, .sgpr-rij__bedrag, .sgpr__media, .sgpr__badge)',
  'Het prijzenblok van referentie B: één grote witte kaart, links de kop en omlijnde rijen met rechts een groot getal (waar referentie B de prijs heeft staat hier het vraagnummer), rechts een foto met een geel vak onderaan. In dat gele vak staan de bereikbaarheid en de knoppen.',
  (v, d) => sec(v, d, null, `<div class="x10__kaart"><div class="x10__body">${kop(v, d)}${lijst(v, d, 'x10__lijst')}</div>
<div class="x10__media">${pop(d, 'x10__pop')}<div class="x10__badge">${status(d, 'q-status--pil')}${zin(d)}${knoppen(d)}</div></div></div>`));

add('11', 'Medewerker achter de balie', 'Referentie A /werkwijze/ (.werkwijze__top, .stappen, .stap)',
  'De bovenkant van referentie A-werkwijze: de kop links, rechts een figuur die op de plaat staat. Hier staat de medewerker achter één brede witte plaat, als achter een balie; op de plaat de vragen in twee kolommen met een dunne scheidingslijn en grote nummers, zoals referentie A-stappen.',
  (v, d) => sec(v, d, null, `<div class="x11__top"><div>${kop(v, d)}${belrij(d, 'x11__bel', 'q-status--pil')}</div>${mens(d, 'x11__mens')}</div>
<div class="x11__plaat">${lijst(v, d, 'x11__lijst')}</div>`));

add('12', 'Tegels in de merkkleuren', 'Referentie B homepage #waarom (.sgw-tegels, .sgw-tegel, .sgw-tegel__3d)',
  'Het "Waarom referentie B"-blok: tegels in verschillende kleuren, elk met een wit schijfje waar het 3D-voorwerp in staat. Hier de merkkleuren Koningsblauw, Goudgeel, Crème, Lucht en Diepblauw; de kop is de eerste tegel en de belkaart de laatste. Het antwoord klapt in de tegel open.',
  (v, d) => sec(v, d, null, `<div class="x12__tegels x12__tegels--${d.vragen.length}"><div class="x12__kop">${kop(v, d)}</div>
${d.vragen.map((_, i) => vraag(v, d, i, { cls: `x12__tegel x12__tegel--${i + 1}`, voor: j => `<span class="x12__schijf" aria-hidden="true">${obj(d, j)}</span>` })).join('')}
<div class="x12__bel">${img('/img/contact-3d/headset.webp', 'x12__3d')}${belrij(d, '', 'q-status--pil')}</div></div>`));

add('13', 'Medewerker op gestapelde panelen', 'Referentie B homepage #team (.sgteam__stapel, .sgteam__podium, .sgteam__team)',
  'Het teamblok van referentie B: mensen die op twee gestapelde panelen staan (Koningsblauw achter, Lucht ervoor), het hoofd steekt boven de panelen uit. Links staan de kop, de panelen met de medewerker en de knoppen; rechts de vragen als regels met dunne lijnen, de open vraag wordt een witte plaat.',
  (v, d) => sec(v, d, null, `<div class="x13__raster"><div class="x13__links">${kop(v, d)}<div class="x13__stapel" aria-hidden="true"><span class="x13__achter"></span><span class="x13__voor"></span>${mens(d, 'x13__mens')}</div>${belrij(d, 'x13__bel', 'q-status--pil')}</div>
${lijst(v, d, 'x13__lijst')}</div>`));

add('14', 'Referentie B: onderwerpband, puur', 'Referentie B /veelgestelde-vragen/ en dienstpagina\'s (.sgfaq-onderwerp, .sgfaq-kop__3d, .sgdp-faq__rij, .sgdp-vraag, .sgdp-link)',
  'Zo dicht mogelijk bij referentie B: een Crème band, links een 3D-voorwerp boven de kop en de belregel als tekstlink met pijl (zoals "Stel je vraag aan ons"), rechts witte kaarten met een haarlijn en een rond plusje dat bij openen geel wordt en draait. Rustig, zonder mensen.',
  (v, d) => sec(v, d, null, `<div class="x14__rij"><div class="x14__kop">${img(d.p === 'contact' ? '/img/contact-3d/envelop.webp' : '/img/contact-3d/formulier.webp', 'x14__3d')}${kop(v, d)}${status(d, 'q-status--pil')}<p class="x14__zin">${d.zin}</p><a class="x14__link" href="tel:+31850005647"><span>Bel 085 000 5647</span>${ic('pijl')}</a>${d.wa}</div>
${lijst(v, d, 'x14__lijst', { geenNr: true })}</div>`, 'x14__band'));

add('15', 'Blauwe kop met foto, vragen op de plaat eronder', 'Referentie B paginakop (.sgdp-hero, .sgdp-hero__band, .sgdp-hero__foto) + referentie A (.faq)',
  'Bovenaan de opzet van de referentie B-paginakop: een Koningsblauw vlak met de kop (gele streep onder het laatste woord) en de knoppen, rechts een echte foto met een schuine naad waar de persoon bovenuit komt. Daaronder, over de rand heen, een witte plaat met de vragen in twee kolommen als referentie A-regels.',
  (v, d) => sec(v, d, null, `<div class="x15__kop"><div class="x15__vlak">${kop(v, d, '', true)}${belrij(d, '', 'q-status--donker')}</div><div class="x15__foto">${pop(d, 'x15__pop')}</div></div>
<div class="x15__plaat">${lijst(v, d, 'x15__lijst')}</div>`));

// ---- pagina ----
const css = fs.readFileSync(path.join(__dirname, 'vragen-kv.css'), 'utf8');
const nav = ['00', ...V.map(x => x.n)].map(n => `<a href="#v${n}">${n}</a>`).join('');
const kap = (n, naam, bron, uitleg) => `<div class="vkap" id="v${n}"><div class="wrap"><span class="vkap__nr">${n}</span><div><b>${naam}</b><small>${bron}</small><p>${uitleg}</p></div><span class="vkap__maat" data-maat></span></div></div>`;
const beide = f => ['contact', 'werkwijze'].map(p => `<div class="pv pv--${p}">\n${f(D[p])}\n</div>`).join('\n');
const live = d => d.sec
  .replace('id="vragen"', `id="vragen-live-${d.p}"`).replace('id="vragen-kop"', `id="vragen-kop-live-${d.p}"`)
  .replace('aria-labelledby="vragen-kop"', `aria-labelledby="vragen-kop-live-${d.p}"`)
  .replace(/id="vragen-(\d)"/g, `id="vragen-live-${d.p}-$1"`).replace(/name="vragen"/g, `name="vragen-live-${d.p}"`);

const html = `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=' js'</script>
<title>Vragenblok · 15 ontwerpen · referentie A + referentie B</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="/css/min/site.min.css?v=${hash('site')}">
<link rel="stylesheet" href="/css/min/vragen.min.css?v=${hash('vragen')}">
<style>
${css}
</style>
<script src="/js/site.js?v=${jsHash}" defer></script>
</head>
<body class="toon-contact">
${sprite}
<nav class="vnav" aria-label="Ontwerpen"><div class="wrap"><b>#vragen · 15 ontwerpen</b>
<div class="vnav__pagina" role="group" aria-label="Tekst van"><button type="button" data-toon="contact" aria-pressed="true">/contact/</button><button type="button" data-toon="werkwijze" aria-pressed="false">/werkwijze/</button></div>
<div class="vnav__links">${nav}</div></div></nav>
${kap('00', 'Nu live', 'Ter vergelijking', 'Het huidige blok, ongewijzigd. Bovenaan wisselt u tussen de tekst van /contact/ (4 vragen, witte sectie) en /werkwijze/ (5 vragen, Mist).')}
${beide(live)}
${V.map(x => kap(x.n, x.naam, x.bron, x.uitleg) + '\n' + beide(d => x.html(x.n, d))).join('\n')}
<div class="vkap vkap--eind"><div class="wrap"><p>Alle teksten zijn letterlijk die van de live pagina's; er is geen tekst bijgeschreven. Beelden zijn bestaande De Reus-foto's, -uitsnedes en 3D-renders uit /img, en per pagina alleen mensen die daar nog niet staan (dus op /contact/ niet de klantenservice, de adviseur of de verhuizer met deken, op /werkwijze/ geen bankscène). Elke bron hierboven bestaat echt in de code van referentie A of referentie B. Kies een nummer (en zeg of het voor /contact/, /werkwijze/ of allebei is).</p></div></div>
<script>
(function(){
function meet(){document.querySelectorAll('[data-maat]').forEach(function(m){var k=m.closest('.vkap'),s=k.nextElementSibling;while(s&&!(s.classList.contains('pv')&&s.offsetParent!==null))s=s.nextElementSibling;if(!s||s.classList.contains('vkap'))return;var sec=s.querySelector('section');if(!sec)return;var h=Math.round(sec.getBoundingClientRect().height);m.textContent='Blokhoogte '+h+' px';m.classList.toggle('is-hoog',h>740);});}
document.querySelectorAll('[data-toon]').forEach(function(b){b.addEventListener('click',function(){document.body.className='toon-'+b.dataset.toon;document.querySelectorAll('[data-toon]').forEach(function(x){x.setAttribute('aria-pressed',x===b)});try{localStorage.setItem('vragen-kv-toon',b.dataset.toon)}catch(e){}meet();});});
try{var t=localStorage.getItem('vragen-kv-toon');if(t){var b=document.querySelector('[data-toon="'+t+'"]');if(b)b.click();}}catch(e){}
addEventListener('load',meet);addEventListener('resize',meet);document.addEventListener('toggle',meet,true);
})();
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(REPO, '_ontwerpen/vragen-referentie-ronde1.html'), html);
console.log('ok', html.length, D.contact.vragen.length, D.werkwijze.vragen.length, D.contact.zin, D.werkwijze.grond);
