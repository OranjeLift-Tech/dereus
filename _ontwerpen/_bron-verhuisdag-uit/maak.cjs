// Ontwerppagina /werkwijze/ #verhuisdag: mensen en spullen stappen uit de foto (15 ontwerpen).
//   node _ontwerpen/_bron-verhuisdag-uit/maak.cjs  ->  _ontwerpen/verhuisdag-uit-de-foto.html
// Per foto ligt een uitsnede (img/verhuisdag-uit/*.webp, zelfde formaat en plek als de foto) precies over de
// foto. De foto wordt op het kader geknipt, de uitsnede alleen BUITEN het kader getoond (clip-path met een gat
// in de vorm van het kader). Wat buiten het kader uitsteekt is dus de verhuizer of de bank zelf. Alles staat stil.
const fs = require('node:fs');
const path = require('node:path');
const UIT = path.join(__dirname, '..', 'verhuisdag-uit-de-foto.html');

// ---- de drie momenten, teksten letterlijk van /werkwijze/ ----
const MOMENTEN = [
  { titel: 'Aankomst', zak: '0.6667',
    tekst: 'Onze verhuizers staan op het afgesproken tijdstip voor de deur. U laat zien wat er mee moet.',
    foto: '/img/dienst-particulier.webp', uit: '/img/verhuisdag-uit/aankomst.webp',
    // r = beeldverhouding, top/bot = kruin en voeten, l/rgt = breedte van de mensen, cx = midden (als deel van het beeld)
    p: { r: 4 / 3, top: 0.338, bot: 0.954, l: 0.2, rgt: 0.821, cx: 0.51 } },
  { titel: 'Inladen', zak: '0.0000',
    tekst: 'Wij beschermen uw spullen en dragen alles zorgvuldig naar buiten. Moet er iets uit elkaar, dan doen wij dat als het zo is afgesproken.',
    foto: '/img/dienst-internationaal.webp', uit: '/img/verhuisdag-uit/inladen.webp',
    p: { r: 4 / 3, top: 0.214, bot: 0.85, l: 0.43, rgt: 0.70, cx: 0.56 },
    // de stapel De Reus-dozen rechts in de wagen: steekt boven en rechts uit het kader
    doos: [[85.9, 22.8], [99.3, 20.9], [100, 20.9], [100, 100], [83.7, 100], [84, 64], [85.4, 62.7]] },
  { titel: 'Uitladen en opbouwen', zak: '0.6667',
    tekst: 'In uw nieuwe huis zetten wij alles op de plek die u aanwijst. Is montage afgesproken, dan bouwen wij uw meubels weer op.',
    foto: '/img/stap-5-bank-voordeur.webp', uit: '/img/verhuisdag-uit/uitladen.webp',
    p: { r: 1120 / 760, top: 0.134, bot: 0.993, l: 0.114, rgt: 0.502, cx: 0.36 } },
];

// ---- maatvoering: waar ligt het beeld achter het kadervenster ----
// Eenheden: breedte van het venster = 1 (x), hoogte van het venster = 1 (y). R = venster breedte/hoogte.
// u = hoever de kruin boven het venster staat, f = hoever de voeten onder het venster staan (null = binnen).
const r4 = (n) => +n.toFixed(4);
function maat(p, R, u, f) {
  const k = R / p.r;                        // beeldhoogte per eenheid schaal, in vensterhoogtes
  const m = 0.012;                          // de foto loopt altijd iets voorbij de onderrand
  let s, y;
  if (u == null) {                          // alleen de voeten naar buiten, kruin blijft binnen
    s = Math.max(1, (1 + f) / (k * p.bot));
    y = 1 + f - p.bot * k * s;
  } else {
    s = Math.max(1, (1 + m + u) / (k * (1 - p.top)));
    if (f != null) s = Math.max(s, (1 + f + u) / (k * (p.bot - p.top)));
    y = -u - p.top * k * s;
  }
  const start = Math.min(Math.max(p.cx - 0.5 / s, 0), 1 - 1 / s);
  return { s: r4(s), x: r4(-start * s), y: r4(y), k, start,
    voet: y + p.bot * k * s, links: (p.l - start) * s, rechts: (p.rgt - start) * s, eind: start + 1 / s };
}

// ---- gatvormen voor de uitsnede (alles buiten het venster zichtbaar) ----
const BUITEN = '-120% -260%, 220% -260%, 220% 260%, -120% 260%, -120% -260%';
const gat = (binnen) => `polygon(evenodd, ${BUITEN}, ${binnen}, ${binnen.split(', ')[0]})`;
const GAT_RECHT = gat('0% 0%, 0% 100%, 100% 100%, 100% 0%');
const GAT_DAK = (h) => gat(`0% ${h}%, 0% 100%, 100% 100%, 100% ${h}%, 50% 0%`);
function GAT_BOOG(ry) {                     // halve ellips bovenop, ry als deel van de hoogte
  const pt = [`0% ${ry * 100}%`, '0% 100%', '100% 100%', `100% ${ry * 100}%`];
  for (let i = 1; i < 24; i++) {
    const t = Math.PI * i / 24;
    pt.push(`${r4(50 + 50 * Math.cos(t))}% ${r4((ry - ry * Math.sin(t)) * 100)}%`);
  }
  return gat(pt.join(', '));
}

// ---- de ontwerpen ----
// u/f: uitsteken boven/onder; R: vensterverhouding; gat: vorm van het gat (null = uitsnede overal, ook op de foto)
const ONTWERPEN = [
  { nr: '01', naam: 'Over de rand', u: 0.15,
    uitleg: 'Het kader blijft zoals het nu is. Hoofden, schouders en de dozenstapel komen boven de bovenrand uit, met een eigen slagschaduw op de band.' },
  { nr: '02', naam: 'Witte afdruk', binnen: 10, onder: 18, u: 0.15,
    uitleg: 'De foto als dikke afdruk met een witte rand en een zijkant. De verhuizers stappen over de witte rand heen; hun schaduw valt op het wit.' },
  { nr: '03', naam: 'Diepblauwe plaat', binnen: 10, onder: 22, u: 0.19,
    uitleg: 'Een dikke Diepblauwe plaat met zijkant, zoals de dieptelaag van de site. De mensen komen er hoog bovenuit, met een lange schaduw.' },
  { nr: '04', naam: 'Gedraaide kaarten', u: 0.15,
    uitleg: 'De drie kaders staan in een waaier naar u toe gedraaid, met een witte zijkant. De verhuizers stappen boven uit elke kaart.' },
  { nr: '05', naam: 'Goudgele plaat erachter', u: 0.16,
    uitleg: 'Zoals referentie A (.blok--vlak): een Goudgele plaat half achter de foto, rechtsonder. Bovenaan komen de verhuizers eruit.' },
  { nr: '06', naam: 'Door het dak', binnen: 8, onder: 16, u: 0.08, gat: GAT_DAK(20), badge: 0.2,
    uitleg: 'Elke foto heeft de vorm van het huis uit het logo, met een Goudgele rand. De verhuizers komen door het dak naar buiten.' },
  { nr: '07', naam: 'Boog', binnen: 10, onder: 16, u: 0.08, gat: GAT_BOOG(0.3), badge: 0.17,
    uitleg: 'De foto in een boog met een witte rand en een Goudgele binnenlijn. De mensen stappen door de boog naar voren.' },
  { nr: '08', naam: 'Naar voren gestapt', binnen: 0, onder: 10, u: null, f: 0.13,
    uitleg: 'Zoals referentie A: foto met een Goudgele onderrand. De voeten komen over die rand heen de band op, met een schaduw op de grond.' },
  { nr: '09', naam: 'Rondom uit het kader', u: 0.2, f: 0.1,
    uitleg: 'Het kader is een raam in de foto: hoofden boven, voeten onder en armen en bank opzij steken erbuiten. Het meest "uit de laptop".' },
  { nr: '10', naam: 'Uit de foto opgestaan', u: 0.17, gat: null,
    uitleg: 'Zoals referentie A-hero: de foto loopt boven en opzij zacht over in de band, de mensen blijven scherp en staan erboven uit.' },
  { nr: '11', naam: 'Scherp op zacht', u: 0.15, gat: null,
    uitleg: 'De achtergrond van de foto is iets vervaagd, de verhuizers zijn scherp en liggen met een schaduw los op de foto.' },
  { nr: '12', naam: 'Ingelijst', binnen: 12, onder: 22, u: 0.15,
    uitleg: 'Een Diepblauwe lijst met dikte en een dunne Goudgele lijn. De verhuizers komen voor de lijst langs naar buiten.' },
  { nr: '13', naam: 'Kijkdoos', binnen: 12, onder: 14, u: 0.15,
    uitleg: 'De foto ligt verzonken in de band, met schaduw in de binnenranden. De mensen staan vooraan en stappen uit de diepte omhoog.' },
  { nr: '14', naam: 'Op een gele sokkel', u: 0.16,
    uitleg: 'Elk kader staat op een Goudgele schijf met dikte, zoals de 3D-schijven op /kosten/. Hoofden en dozen komen boven het kader uit.' },
  { nr: '15', naam: 'Witte kaart', u: 0.2,
    uitleg: 'Elk moment is een witte kaart met dikte: foto, kop en tekst samen. De verhuizers steken boven de kaart uit.' },
];

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const kopgroep = (id) => `<div class="kopgroep kopgroep--midden"><p class="label">De verhuisdag</p><h2 id="${id}">Op de verhuisdag</h2><p class="intro">Op de verhuisdag doen wij het zware werk. U houdt het overzicht.</p></div>`;
const SLOT = '<p class="b-verhuisdag__slot">Betalen doet u op de verhuisdag, tenzij we samen iets anders hebben afgesproken. Ziet u schade aan uw spullen? Meld het dan meteen op de dag zelf aan onze verhuizers, dan bekijken en noteren we het direct samen. Zo staat het ook in onze <a href="/algemene-voorwaarden/">algemene voorwaarden</a>.</p>';

function sectieNu() {
  const li = MOMENTEN.map((m, i) => `<li class="b-verhuisdag__moment" style="--zak:${m.zak};--i:${i}"><span class="b-verhuisdag__kader" aria-hidden="true"><img src="${m.foto}" alt="" width="1400" height="1050"></span><h3 class="b-verhuisdag__titel">${m.titel}</h3><p>${esc(m.tekst)}</p></li>`).join('');
  return `<section class="b-verhuisdag b-verhuisdag--kaders sectie sectie--blauw" aria-labelledby="vd-00" style="--detail-inhoud:1440px">
      <div class="wrap">
        ${kopgroep('vd-00')}
        <ol class="b-verhuisdag__dag" role="list" style="--aantal:3">${li}</ol>
        ${SLOT}
      </div>
    </section>`;
}

function sectie(o) {
  const R = o.R || 1.6;
  const li = MOMENTEN.map((m, i) => {
    const g = maat(m.p, R, o.u, o.f);
    const doos = m.doos && o.gat !== null && g.eind > 0.93;
    // de stapel stopt op de onderrand van het venster, anders hangt hij onder het kader uit
    const onder = Math.min(100, r4((1 - g.y) / (g.k * g.s) * 100));
    const doosVorm = m.doos && `polygon(${m.doos.map(([px, py]) => `${px}% ${Math.min(py, onder)}%`).join(', ')})`;
    const vars = [`--s:${g.s}`, `--x:${g.x}`, `--y:${g.y}`];
    const vloer = o.f != null
      ? `<span class="vu__vloer" style="left:${r4(g.links * 100)}%;width:${r4((g.rechts - g.links) * 100)}%;top:${r4((g.voet - 0.05) * 100)}%"></span>` : '';
    return `<li class="b-verhuisdag__moment" style="--zak:${m.zak};--i:${i}"><span class="b-verhuisdag__kader vu" aria-hidden="true" style="${vars.join(';')}">`
      + `<span class="vu__raam"><img class="vu__foto" src="${m.foto}" alt=""></span>${vloer}`
      + `<span class="vu__buiten">${doos ? `<img class="vu__doos" src="${m.foto}" alt="" style="clip-path:${doosVorm}">` : ''}<img class="vu__uit" src="${m.uit}" alt=""></span>`
      + `</span><h3 class="b-verhuisdag__titel">${m.titel}</h3><p>${esc(m.tekst)}</p></li>`;
  }).join('');
  const gatVorm = o.gat === null ? 'none' : (o.gat || GAT_RECHT);
  const stijl = [`--detail-inhoud:1440px`, `--binnen:${o.binnen || 0}px`, `--onder:${o.onder || 0}px`, `--ar:${R}`, `--u:${o.u == null ? 0 : o.u}`, `--f:${o.f || 0}`, `--gat-vorm:${gatVorm}`, `--badge-dy:${o.badge || 0}`];
  return `<section class="b-verhuisdag b-verhuisdag--kaders sectie sectie--blauw vx vx--${o.nr}" aria-labelledby="vd-${o.nr}" style="${stijl.join(';')}">
      <div class="wrap">
        ${kopgroep('vd-' + o.nr)}
        <ol class="b-verhuisdag__dag" role="list" style="--aantal:3">${li}</ol>
        ${SLOT}
      </div>
    </section>`;
}

const okop = (nr, naam, uitleg) => `<div class="okop" id="v${nr}"><div class="wrap"><b>${nr}</b><span>${naam}</span><small>${uitleg}</small></div></div>`;

const CSS = fs.readFileSync(path.join(__dirname, 'stijl.css'), 'utf8');
const html = `<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Op de verhuisdag: uit de foto (15 ontwerpen)</title>
<meta name="robots" content="noindex">
<link rel="preload" href="/fonts/archivo-condensed-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/min/site.min.css">
<link rel="stylesheet" href="/css/min/verhuisdag.min.css">
<style>
${CSS}
</style>
</head>
<body>
<header class="otitel"><div class="wrap">
  <p class="label">/werkwijze/ · #verhuisdag</p>
  <h1>Op de verhuisdag: de verhuizers stappen uit de foto</h1>
  <p>15 ontwerpen voor de drie momenten Aankomst, Inladen en Uitladen en opbouwen. In elke foto zijn de verhuizers en de bank vrijgesteld (img/verhuisdag-uit/), bij Inladen ook de stapel De Reus-dozen. Die liggen precies op de foto; wat buiten het kader steekt, is dus echt de persoon of het meubel uit de foto. Teksten zijn letterlijk van de site, niets beweegt. Referentie: de uitsnedes en de Goudgele plaat van referentie A.</p>
</div></header>
<nav class="onav" aria-label="Ontwerpen"><div class="wrap"><strong>Verhuisdag uit de foto</strong><a href="#v00">00</a>${ONTWERPEN.map((o) => `<a href="#v${o.nr}" title="${o.naam}">${o.nr}</a>`).join('')}</div></nav>
<main>
${okop('00', 'Zo staat het nu', 'Ter vergelijking: drie foto\'s als rechthoek op de daklijn, alles blijft binnen het kader.')}
${sectieNu()}
${ONTWERPEN.map((o) => okop(o.nr, o.naam, o.uitleg) + '\n' + sectie(o)).join('\n')}
</main>
<script>
/* #solo-05 toont alleen ontwerp 05 (voor schermafdrukken) */
(function () {
  var m = /^#solo-(\\d\\d)$/.exec(location.hash);
  if (!m) return;
  document.querySelectorAll('.otitel,.onav').forEach(function (e) { e.hidden = true; });
  document.querySelectorAll('.okop').forEach(function (k) {
    var z = k.id !== 'v' + m[1];
    k.hidden = z; k.nextElementSibling.hidden = z;
  });
})();
</script>
</body>
</html>
`;
fs.writeFileSync(UIT, html);
console.log('geschreven:', UIT, Math.round(html.length / 1024) + ' kB');
for (const o of ONTWERPEN) console.log(o.nr, MOMENTEN.map((m) => { const g = maat(m.p, o.R || 1.6, o.u, o.f); return `s${g.s} x${g.x} y${g.y}`; }).join(' | '));
