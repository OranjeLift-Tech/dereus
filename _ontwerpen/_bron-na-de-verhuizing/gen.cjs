// Maakt _ontwerpen/na-de-verhuizing-varianten.html (15 ontwerpen voor /werkwijze/ #na-de-verhuizing).
// node gen.cjs  — leest var.css hiernaast en het sprite-blok uit werkwijze/index.html.
const fs = require('fs'), path = require('path');
const REPO = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus/dereus';
const UIT = path.join(REPO, '_ontwerpen/na-de-verhuizing-varianten.html');
const css = fs.readFileSync(path.join(__dirname, 'var.css'), 'utf8');
const werkwijze = fs.readFileSync(path.join(REPO, 'werkwijze/index.html'), 'utf8');
const sprite = werkwijze.match(/<svg class="sprite"[\s\S]*?<\/svg>(?=\s*<header)/)[0];
const siteCss = werkwijze.match(/href="(\/css\/min\/site\.min\.css\?v=[0-9a-f]+)"/)[1];

// ---- letterlijke tekst van /werkwijze/ ----
const T = {
  label: 'Daarna',
  kop: 'Na de verhuizing',
  intro: 'Na de verhuisdag staat alles op zijn plek in uw nieuwe huis. Wat nu nog handig is:',
  v1: 'Vragen achteraf?',
  v1p: 'Bel of mail gewoon uw verhuisadviseur. Die kent uw verhuizing van begin tot eind.',
  v2: 'Tevreden?',
  v2p: 'Een review op Google helpt andere mensen die een verhuisbedrijf zoeken.',
};
const GOOGLE = 'https://www.google.com/search?q=reviews+voor+verhuisbedrijf+de+reus';
const ic = n => `<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-${n}"/></svg>`;
const img = (src, w, h, k = '', alt = '') => `<img${k ? ` class="${k}"` : ''} src="/img/${src}" alt="${alt}" width="${w}" height="${h}" decoding="async">`;
const I = {
  groot: k => img('dienst-nationaal-v2-groot.webp', 1440, 1080, k),
  nationaalUit: k => img('dienst-nationaal-v2-uit.webp', 1080, 810, k),
  tel3d: k => img('contact-3d/telefoon.webp', 208, 400, k),
  ster3d: k => img('kaart-3d/ster.webp', 240, 240, k),
};
const P = {
  tel: (k = 'geel') => `<a class="pil pil--${k}" href="tel:+31850005647">${ic('telefoon')}085 000 5647</a>`,
  mail: (k = 'wit') => `<a class="pil pil--${k}" href="mailto:info@verhuisbedrijfdereus.nl">${ic('mail')}Mailen</a>`,
  review: (k = 'wit') => `<a class="pil pil--${k}" href="${GOOGLE}" target="_blank" rel="noopener">${ic('google')}Review op Google</a>`,
};
const streepTel = `<a class="streep" href="tel:+31850005647">${ic('telefoon')}085 000 5647</a>`;
const streepReview = `<a class="streep" href="${GOOGLE}" target="_blank" rel="noopener">Review op Google${ic('pijl')}</a>`;
const kop = (lab = '', h2 = T.kop) => `<p class="label${lab ? ' ' + lab : ''}">${T.label}</p>
        <h2>${h2}</h2>
        <p class="intro">${T.intro}</p>`;
const sterren = `<span class="sterren5" aria-hidden="true">${ic('ster').repeat(5)}</span>`;

const V = [];
const variant = (naam, bron, uitleg, html, na) => V.push({ naam, bron, uitleg, html, na });

// 01
variant('Huisvenster', 'Referentie A · venster (“Benieuwd naar de kosten?”)',
  'Tekst links met label-lijn; rechts het huis uit het logo als venster met een gele dikte, de drie lachende verhuizers staan ervoor en steken buiten het huis uit. Rond stempel met de Google-score.',
  `<section class="sectie sectie--mist vv v01"><div class="wrap v01__raster">
      <div>
        ${kop('label--lijn')}
        <ul class="v01__punten" role="list">
          <li><span class="rond">${ic('telefoon')}</span><div><h3>${T.v1}</h3><p>${T.v1p}</p></div></li>
          <li><span class="rond">${ic('ster')}</span><div><h3>${T.v2}</h3><p>${T.v2p}</p></div></li>
        </ul>
        <div class="pillen">${P.tel()}${P.review()}</div>
      </div>
      <div class="v01__beeld" aria-hidden="true">
        <span class="v01__huisrand"></span><span class="v01__huis"></span>
        ${img('review-verhuizers-lachend.webp', 760, 504, 'v01__mensen')}
        <span class="v01__stempel"><b>4,9</b>${sterren}<small>${ic('google')}Google</small></span>
      </div>
    </div></section>`);

// 02
variant('Wagen met paneel', 'Brocken · livrei (contactpagina)',
  'De wagenfoto loopt door tot de linker schermrand met een schuine onderkant en een lichtblauwe plaat erachter; een wit paneel schuift erover met label-pil, kop en de twee punten als rijen met een bovenlijn.',
  `<section class="sectie sectie--mist vv v02"><div class="wrap v02__raster">
      <figure class="v02__foto" aria-hidden="true">${I.groot()}</figure>
      <div class="v02__paneel">
        ${kop('label--pil')}
        <ul class="v02__punten" role="list">
          <li><span class="rond">${ic('telefoon')}</span><div><h3>${T.v1}</h3><p>${T.v1p}</p>${streepTel}</div></li>
          <li><span class="rond">${ic('ster')}</span><div><h3>${T.v2}</h3><p>${T.v2p}</p>${streepReview}</div></li>
        </ul>
      </div>
    </div></section>`);

// 03
variant('Gele schuine band', 'Referentie A · opslag (“Even geen plek?”)',
  'Een schuine Goudgele band met een Diepblauwe streep eronder loopt door het blok; links een Diepblauwe kaart met alles erin, rechts staat de ploeg met dozen op de band.',
  `<section class="sectie sectie--mist vv v03">
      <div class="v03__band" aria-hidden="true"></div>
      <div class="wrap v03__raster">
        <div class="v03__kaart">
          ${kop('label--lijn')}
          <ul class="v03__punten" role="list">
            <li><span class="rond rond--donker">${ic('telefoon')}</span><div><h3>${T.v1}</h3><p>${T.v1p}</p></div></li>
            <li><span class="rond rond--donker">${ic('ster')}</span><div><h3>${T.v2}</h3><p>${T.v2p}</p></div></li>
          </ul>
          <div class="pillen">${P.tel()}${P.review('lijn')}</div>
        </div>
        <div class="v03__beeld" aria-hidden="true">${img('team/team-hero-dozen-1100.webp', 1100, 1195)}</div>
      </div>
    </section>`);

// 04
variant('Aanspreekpunt', 'Referentie A · werkwijze “Een verhuizing, een aanspreekpunt”',
  'Lichtblauwe band. Kop links, rechts de verhuisadviseur met headset die met hoofd en schouders boven haar foto uitkomt. Eronder de twee punten naast elkaar met een 3D-voorwerp, zoals referentie A-rij.',
  `<section class="sectie sectie--lucht vv v04"><div class="wrap">
      <div class="v04__top">
        <div>${kop('label--lijn')}<div class="pillen">${P.tel()}${P.mail()}</div></div>
        <div class="v04__beeld" aria-hidden="true">${img('contact-klantenservice-foto.webp', 1200, 800, 'v04__foto')}${img('contact-klantenservice-uit.webp', 1200, 800, 'v04__uit')}</div>
      </div>
      <ul class="v04__rij" role="list">
        <li><span class="v04__ding" aria-hidden="true">${I.tel3d()}</span><div><h3>${T.v1}</h3><p>${T.v1p}</p>${streepTel}</div></li>
        <li><span class="v04__ding v04__ding--ster" aria-hidden="true">${I.ster3d()}</span><div><h3>${T.v2}</h3><p>${T.v2p}</p>${streepReview}</div></li>
      </ul>
    </div></section>`, 'var(--primary-50)');

// 05
variant('Afdrukken', 'Referentie A · historie (“Meer dan honderd jaar”)',
  'Links de kop en de twee punten als tijdlijn met stippellijn; rechts drie scheve foto-afdrukken met een witte rand: de wagen, de verhuizers en de voordeur van het nieuwe huis.',
  `<section class="sectie sectie--mist vv v05"><div class="wrap v05__raster">
      <div>
        ${kop('label--lijn')}
        <ol class="v05__lijn" role="list">
          <li><span class="v05__mark">${ic('telefoon')}</span><h3>${T.v1}</h3><p>${T.v1p}</p></li>
          <li><span class="v05__mark">${ic('ster')}</span><h3>${T.v2}</h3><p>${T.v2p}</p></li>
        </ol>
        <div class="pillen">${P.tel()}${P.review()}</div>
      </div>
      <div class="v05__afdrukken" aria-hidden="true">
        <figure class="v05__afdruk v05__afdruk--1">${img('dienst-nationaal-v2.webp', 720, 540)}</figure>
        <figure class="v05__afdruk v05__afdruk--3">${img('nieuw-huis.webp', 400, 450)}</figure>
        <figure class="v05__afdruk v05__afdruk--2">${img('verhuisdag-verhuizers.webp', 709, 787)}</figure>
      </div>
    </div></section>`);

// 06
variant('Score in de ring', 'Brocken · score (reviewpagina)',
  'Witte band. Links “Vragen achteraf?” met het telefoonnummer groot en een gele onderstreep. Rechts de wagenfoto op een schuine blauwe band met stippen, een ronde 4,9-score met gele ring en een scheve crème notitie “Tevreden?”.',
  `<section class="sectie sectie--wit vv v06"><div class="wrap v06__raster">
      <div>
        ${kop('label--pil', 'Na de <em>verhuizing</em>')}
        <div class="v06__vraag"><h3>${T.v1}</h3><p>${T.v1p}</p>
          <a class="v06__nummer" href="tel:+31850005647"><span class="rond rond--geel">${ic('telefoon')}</span><span>085 000 5647</span></a>
          <a class="v06__mail" href="mailto:info@verhuisbedrijfdereus.nl">info@verhuisbedrijfdereus.nl</a>
        </div>
      </div>
      <div class="v06__beeld">
        <span class="v06__band" aria-hidden="true"></span>
        ${I.groot('v06__foto')}
        <div class="v06__score" aria-hidden="true"><svg class="ring" viewBox="0 0 120 120"><circle cx="60" cy="60" r="56" fill="none" stroke="#E2E5EB" stroke-width="3"/><circle cx="60" cy="60" r="56" fill="none" stroke="#FFCC33" stroke-width="5" stroke-linecap="round" pathLength="100" stroke-dasharray="94 100"/></svg><b>4,9</b>${sterren}<small>${ic('google')}Google</small></div>
        <div class="v06__notitie"><h3>${T.v2}</h3><p>${T.v2p}</p>${streepReview}</div>
      </div>
    </div></section>`, '#fff');

// 07
variant('Mensen uit de tegels', 'Referentie A + Brocken · uitsnede die boven het kader uitstapt',
  'Kop in het midden. Twee grote tegels: Diepblauw met de verhuisadviseur, Goudgeel met een verhuizer met dozen; de mensen staan in de tegel en komen er ver bovenuit.',
  `<section class="sectie sectie--mist vv v07"><div class="wrap">
      <div class="kopgroep">${kop()}</div>
      <ul class="v07__tegels" role="list">
        <li class="v07__tegel v07__tegel--vragen"><div class="v07__tekst"><h3>${T.v1}</h3><p>${T.v1p}</p><div class="pillen">${P.tel()}${P.mail('lijn')}</div></div>${img('contact-adviseur-uit.webp', 640, 954, 'v07__mens v07__mens--adviseur')}</li>
        <li class="v07__tegel v07__tegel--tevreden"><div class="v07__tekst"><h3>${T.v2}</h3><p>${T.v2p}</p><div class="pillen">${P.review('blauw')}</div></div>${img('verhuizer-twee-dozen-uit.webp', 407, 1200, 'v07__mens v07__mens--ploeg')}</li>
      </ul>
    </div></section>`);

// 08
variant('Diepblauwe band, schuin', 'Brocken · dag (werkwijze, donkere band met schuine randen)',
  'Diepblauwe band met schuine boven- en onderrand en een stippenraster. De twee punten als kolommen met een dunne lijn erboven; de foto heeft een schuine bovenrand met een gele streep en de twee verhuizers stappen er bovenuit.',
  `<section class="vv v08"><div class="wrap v08__raster">
      <div>
        ${kop('label--pil label--donker')}
        <ul class="v08__punten" role="list">
          <li><span class="rond rond--donker">${ic('telefoon')}</span><h3>${T.v1}</h3><p>${T.v1p}</p></li>
          <li><span class="rond rond--donker">${ic('ster')}</span><h3>${T.v2}</h3><p>${T.v2p}</p></li>
        </ul>
        <div class="pillen">${P.tel()}${P.review('lijn')}</div>
      </div>
      <div class="v08__beeld" aria-hidden="true">${img('dienst-particulier-v2.webp', 720, 540, 'v08__foto')}${img('dienst-particulier-v2-uit.webp', 1080, 810, 'v08__uit')}</div>
    </div></section>`);

// 09
variant('Gele schijven', 'De Reus · zelfde idioom als /kosten/ #opbouw (door u gekozen)',
  'Kop links, de wagenfoto hoog rechts. De twee punten staan elk als 3D-voorwerp (telefoon, ster) op een dikke gele schijf, tekst eronder.',
  `<section class="sectie sectie--mist vv v09"><div class="wrap v09__raster">
      <div class="v09__kop">${kop()}</div>
      <figure class="v09__foto" aria-hidden="true">${I.groot()}</figure>
      <ul class="v09__punten" role="list">
        <li><span class="v09__podium" aria-hidden="true">${I.tel3d()}</span><h3>${T.v1}</h3><p>${T.v1p}</p>${streepTel}</li>
        <li><span class="v09__podium v09__podium--ster" aria-hidden="true">${I.ster3d()}</span><h3>${T.v2}</h3><p>${T.v2p}</p>${streepReview}</li>
      </ul>
    </div></section>`);

// 10
variant('Fotoband', 'Referentie A · footer / De Reus-footer (foto tot de rand, verloop naar Diepblauw)',
  'Een Diepblauwe band met de wagenfoto tot de rechter schermrand die naar links dichtloopt. Kop in wit; de twee punten als witte kaarten die half over de onderrand vallen, met telefoon en ster erbovenop.',
  `<section class="vv v10">
      <div class="v10__band">${I.groot('v10__foto')}<div class="wrap v10__tekst">${kop()}</div></div>
      <div class="wrap"><ul class="v10__kaarten" role="list">
        <li>${I.tel3d('v10__ding')}<h3>${T.v1}</h3><p>${T.v1p}</p><div class="pillen">${P.tel()}${P.mail()}</div></li>
        <li>${I.ster3d('v10__ding v10__ding--ster')}<h3>${T.v2}</h3><p>${T.v2p}</p><div class="pillen">${P.review()}</div></li>
      </ul></div>
    </section>`);

// 11
variant('Dikke plaat', 'De Reus · diepte (plaat met dikte, voorwerpen breken uit de rand)',
  'Alles op één witte plaat met een Koningsblauwe dikte naar rechtsonder; foto links in de plaat verzonken, rechts de tekst en twee kolommen. Telefoon en ster steken boven de plaat uit.',
  `<section class="sectie sectie--mist vv v11"><div class="wrap">
      <div class="v11__plaat">
        ${I.tel3d('v11__ding v11__ding--tel')}${I.ster3d('v11__ding v11__ding--ster')}
        <figure class="v11__foto" aria-hidden="true">${I.groot()}</figure>
        <div class="v11__inhoud">
          ${kop()}
          <ul class="v11__punten" role="list">
            <li><h3>${T.v1}</h3><p>${T.v1p}</p></li>
            <li><h3>${T.v2}</h3><p>${T.v2p}</p></li>
          </ul>
          <div class="pillen">${P.tel()}${P.review()}</div>
        </div>
      </div>
    </div></section>`);

// 12
variant('Gestapelde platen', 'Brocken · stemmen (reviews: persoon voor twee verschoven platen)',
  'Witte band. Links de verhuisadviseur voor een crème en een verschoven blauwe plaat. Rechts de kop en twee witte kaarten: een groot geel vraagteken bij “Vragen achteraf?”, een 4,9-badge bij “Tevreden?”.',
  `<section class="sectie sectie--wit vv v12"><div class="wrap v12__raster">
      <div class="v12__beeld" aria-hidden="true"><span class="v12__plaat v12__plaat--blauw"></span><span class="v12__plaat v12__plaat--creme"></span>${img('contact-adviseur-uit.webp', 640, 954, 'v12__mens')}</div>
      <div>
        ${kop('label--pil')}
        <ul class="v12__kaarten" role="list">
          <li class="v12__kaart"><span class="v12__teken" aria-hidden="true">?</span><h3>${T.v1}</h3><p>${T.v1p}</p>${streepTel}</li>
          <li class="v12__kaart"><span class="v12__score" aria-hidden="true">4,9${ic('ster')}</span><h3>${T.v2}</h3><p>${T.v2p}</p>${streepReview}</li>
        </ul>
      </div>
    </div></section>`, '#fff');

// 13
variant('Gekanteld stippenpaneel', 'Brocken · vragen (belregel met monogram, scheef stippenpaneel)',
  'Links de kop en een belregel met het beeldmerk in een rondje en het nummer met gele onderstreep. Rechts een licht gekanteld crème paneel met stippen en een groot omlijnd vraagteken, de twee punten als witte kaarten en een verhuizer met doos ernaast.',
  `<section class="sectie sectie--mist vv v13"><div class="wrap v13__raster">
      <div>
        ${kop()}
        <a class="v13__bel" href="tel:+31850005647"><span class="v13__merk"><img src="/img/logo/dereus-beeldmerk.svg" alt="" width="60" height="57"></span><span><b>085 000 5647</b><small>info@verhuisbedrijfdereus.nl</small></span></a>
      </div>
      <div class="v13__paneel">
        <span class="v13__vraagteken" aria-hidden="true">?</span>
        <ul class="v13__kaarten" role="list">
          <li><span class="rond">${ic('telefoon')}</span><div><h3>${T.v1}</h3><p>${T.v1p}</p></div></li>
          <li><span class="rond">${ic('ster')}</span><div><h3>${T.v2}</h3><p>${T.v2p}</p>${streepReview}</div></li>
        </ul>
        ${img('verhuizer-doos-schouder-uit.webp', 489, 1200, 'v13__mens')}
      </div>
    </div></section>`);

// 14
variant('Tegels onder de foto', 'Brocken · vinden (contact: brede foto met schuine onderrand, tegels erover)',
  'Witte band, kop in het midden. Een brede wagenfoto met schuine onderrand; twee witte tegels met een rond icoon schuiven er half over. Een verhuizer met dozen staat rechts over de rand.',
  `<section class="sectie sectie--wit vv v14"><div class="wrap">
      <div class="kopgroep">${kop('label--pil')}</div>
      <div class="v14__beeld" aria-hidden="true">${I.groot('v14__foto')}${img('verhuizer-twee-dozen-uit.webp', 407, 1200, 'v14__mens')}</div>
      <ul class="v14__tegels" role="list">
        <li><span class="v14__icoon">${ic('telefoon')}</span><h3>${T.v1}</h3><p>${T.v1p}</p>${streepTel}</li>
        <li><span class="v14__icoon">${ic('ster')}</span><h3>${T.v2}</h3><p>${T.v2p}</p>${streepReview}</li>
      </ul>
    </div></section>`, '#fff');

// 15
variant('Panorama met overlapkaart', 'Referentie A · hero met offertekaart eroverheen',
  'Grote kop links, intro rechts. Een brede foto waarvan de bovenkant wegvalt, zodat de verhuizer met de doos boven de lijst uitkomt. Eén witte kaart met de twee punten valt over de onderrand.',
  `<section class="sectie sectie--mist vv v15"><div class="wrap">
      <div class="v15__kop"><div><p class="label label--lijn">${T.label}</p><h2>${T.kop}</h2></div><p class="intro">${T.intro}</p></div>
      <div class="v15__beeld" aria-hidden="true">${I.groot('v15__foto')}${I.nationaalUit('v15__uit')}</div>
      <div class="v15__kaart">
        <div class="v15__punt"><span class="rond">${ic('telefoon')}</span><div><h3>${T.v1}</h3><p>${T.v1p}</p><div class="pillen">${P.tel()}${P.mail()}</div></div></div>
        <div class="v15__punt"><span class="rond">${ic('ster')}</span><div><h3>${T.v2}</h3><p>${T.v2p}</p><div class="pillen">${P.review()}</div></div></div>
      </div>
    </div></section>`);

const nr = i => String(i + 1).padStart(2, '0');
const html = `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Na de verhuizing: 15 ontwerpen | De Reus</title>
<link rel="preload" href="/fonts/archivo-condensed-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="${siteCss}">
<style>
${css}
</style>
</head>
<body class="p p-werkwijze">
${sprite}
<nav class="vnav" aria-label="Ontwerpen"><span class="vnav__titel">Na de verhuizing · 15 ontwerpen</span>${V.map((v, i) => `<a href="#v${nr(i)}" title="${v.naam}">${nr(i)}</a>`).join('')}</nav>
<p class="vuitleg">/werkwijze/ #na-de-verhuizing. Alle teksten zijn letterlijk van de pagina. Nieuw zijn alleen de knoppen (bellen, mailen, review op Google) en de 4,9-score uit het reviewblok eronder; die kunnen weg. De blauwe strook boven elk ontwerp is het einde van “Op de verhuisdag”, de schuine witte rand eronder het begin van de reviews. Noem het nummer dat u wilt.</p>
${V.map((v, i) => `<div class="variant" id="v${nr(i)}"${v.na ? ` style="--na:${v.na}"` : ''}>
  <header class="vkop"><span class="vkop__nr">${nr(i)}</span><div><b>${v.naam}</b><small>Referentie: ${v.bron}. ${v.uitleg}</small></div></header>
  <div class="ctx-boven" aria-hidden="true"></div>
  ${v.html}
  <div class="ctx-onder" aria-hidden="true"></div>
</div>`).join('\n')}
</body>
</html>
`;
fs.writeFileSync(UIT, html.replace(/\n/g, '\r\n'));
console.log('geschreven', UIT, V.length, 'ontwerpen', Math.round(html.length / 1024) + ' kB');
