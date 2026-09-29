// 15 ontwerpen voor de vier kanaalkaarten op /contact/ (#contactkaarten: Bel ons, Mail ons, Stuur een bericht,
// Vraag een offerte aan). De klant vond de gele schijven mooi, maar niet "wow". Elk ontwerp neemt de opbouw van een
// echt blok van referentie A, B of C over; de bronklasse staat in het bijschrift.
// node gen.cjs  ->  _ontwerpen/contactkanalen-wow-varianten.html
// Teksten, links, de kop, de verhuizer en de belkaart komen letterlijk uit contact/index.html.
const fs = require('fs');
const path = require('path');
const REPO = path.resolve(__dirname, '../..');
const PAG = fs.readFileSync(path.join(REPO, 'contact/index.html'), 'utf8');
const hash = n => PAG.match(new RegExp(`/css/min/${n}\\.min\\.css\\?v=([0-9a-f]+)`))[1];
const jsHash = PAG.match(/\/js\/site\.js\?v=([0-9a-f]+)/)[1];
const sprite = PAG.match(/<svg class="sprite"[\s\S]*?<\/svg>/)[0];

function maat(src) {
  const b = fs.readFileSync(path.join(REPO, src));
  const soort = b.toString('ascii', 12, 16);
  if (soort === 'VP8X') return [1 + b.readUIntLE(24, 3), 1 + b.readUIntLE(27, 3)];
  if (soort === 'VP8 ') return [b.readUInt16LE(26) & 0x3fff, b.readUInt16LE(28) & 0x3fff];
  if (soort === 'VP8L') { const n = b.readUInt32LE(21); return [(n & 0x3fff) + 1, ((n >> 14) & 0x3fff) + 1]; }
  throw new Error('geen webp: ' + src);
}
const img = (src, cls = '', extra = '') => {
  const m = src.endsWith('.svg') ? null : maat(src);
  return `<img class="${cls}" src="${src}" alt=""${m ? ` width="${m[0]}" height="${m[1]}"` : ''} loading="lazy" decoding="async"${extra}>`;
};

// ---- de live sectie ----
const SEC = PAG.match(/<section class="b-contactkaarten[\s\S]*?<\/section>/)[0];
const BOVEN = SEC.match(/<div class="b-contactkaarten__boven">[\s\S]*?<\/ul>\s*<\/div>\s*<\/div>/)[0];
const K = [...SEC.matchAll(/<h3 class="b-contactkaarten__titel">([\s\S]*?)<\/h3>\s*<p>([\s\S]*?)<\/p>\s*<a class="b-contactkaarten__link" href="([^"]+)"( data-geen-whatsapp)?><span>([\s\S]*?)<\/span>/g)]
  .map(m => ({ titel: m[1], tekst: m[2], href: m[3], geenWa: !!m[4], link: m[5] }));
if (K.length !== 4 || !BOVEN.includes('b-contactkaarten__belkaart')) throw new Error('live tekst niet gevonden');

// ---- bouwstenen ----
const ic = n => `<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-${n}"/></svg>`;
const NAAM = ['telefoon', 'envelop', 'klembord', 'dozen'];
// de echte fotovoorwerpen in groot formaat (zelfde bestanden als op /contact/, bron _ai-beelden/contact-echt)
const obj = (i, cls = '') => img(`/_ontwerpen/_bron-contact-echt/${NAAM[i]}.webp`, `k-obj k-obj--${NAAM[i]} ${cls}`, ' aria-hidden="true"');
// echte foto's uit de eigen map, per kanaal: bellen, laptop, typen, de dozen met het logo
const FOTO = ['/img/stap-2-bellen.webp', '/img/stap-1-laptop.webp', '/img/stap-1-formulier.webp', '/img/stap-3-offerte.webp'];
const foto = (i, cls = '') => img(FOTO[i], `k-foto ${cls}`, ' aria-hidden="true"');
const titel = (i, cls = '') => `<h3 class="k-titel ${cls}">${K[i].titel}</h3>`;
const tekst = (i, cls = '') => `<p class="k-tekst ${cls}">${K[i].tekst}</p>`;
const link = (i, cls = '') => `<a class="k-link ${cls}" href="${K[i].href}"${K[i].geenWa ? ' data-geen-whatsapp' : ''}><span>${K[i].link}</span>${ic('pijl')}</a>`;
const nr2 = i => String(i + 1).padStart(2, '0');
const merk = (cls = '') => img('/img/logo/dereus-beeldmerk.svg', cls, ' aria-hidden="true"');
const merkNeg = (cls = '') => img('/img/logo/dereus-beeldmerk-negatief.svg', cls, ' aria-hidden="true"');
const lijst = (cls, li) => `<ul class="kk ${cls}" role="list">${K.map((_, i) => li(i)).join('')}</ul>`;

const V = [];
const add = (n, naam, bron, uitleg, kanalen) => V.push({ n, naam, bron, uitleg, kanalen });

// ============ referentie B ============
add('01', 'Trap op de gele band', 'Referentie B · .sgm__kaarten, .sgm__band, .sgm__figuur (blokken/manieren.css)',
  'De kaarten lopen als een trap op naar rechts, elk 2,5rem hoger. Onder de trap ligt een dikke goudgele band met een donkergele zijkant. Het voorwerp staat achter de bovenrand van zijn kaart, zoals de monteurs bij de referentie achter hun kaart staan.',
  () => lijst('k01', i => `<li class="k01-kaart">${obj(i)}<div class="k01-doos k-neon">${titel(i)}${tekst(i)}${link(i)}</div></li>`));

add('02', 'Foto met voorwerp op de naad', 'Referentie B · .sgd1-kaart, .sgd1-beeld, .sgd1-ico, .sgd1::before (blokken/diensten.css)',
  'Elke kaart krijgt een echte foto van het kanaal: iemand die belt, een laptop, typende handen, een hand die een offerte tekent. Het voorwerp staat groot op de naad tussen foto en tekst. De kaarten liggen op een lichtblauwe band met een V-inkeping aan de bovenkant.',
  () => lijst('k02', i => `<li class="k02-kaart k-neon"><div class="k02-beeld">${foto(i)}${obj(i)}</div><div class="k02-tekst">${titel(i)}${tekst(i)}${link(i)}</div></li>`));

add('03', 'Vier kleurtegels', 'Referentie B · .sgw-tegel:nth-child(1-4), .sgw-tegel__3d (blokken/waarom.css)',
  'Vier tegels in vier merkkleuren: Diepblauw, Goudgeel, Lucht en Koningsblauw. Het voorwerp staat in een witte schijf rechtsboven en steekt ver boven de tegel uit; de titel staat ernaast.',
  () => lijst('k03', i => `<li class="k03-tegel k-neon"><span class="k03-schijf">${obj(i)}</span>${titel(i)}${tekst(i)}${link(i)}</li>`));

add('04', 'Goudgele plaat met foto-afdrukken', 'Referentie B · .sgt__paneel, .sgt__fotos figure, figcaption (blokken/toennu.css)',
  'Eén goudgele plaat over de hele breedte. Daarop vier scheve foto-afdrukken met een witte rand en de titel als donkere pil, zoals de team- en pandfoto bij de referentie. Het echte voorwerp ligt op de hoek van de afdruk.',
  () => `<div class="k04-plaat">${lijst('k04', i => `<li class="k04-kaart"><figure class="k04-afdruk">${foto(i)}<figcaption>${titel(i)}</figcaption>${obj(i)}</figure>${tekst(i)}${link(i)}</li>`)}</div>`);

add('05', 'Dikke gele onderrand', 'Referentie B · .sgct__kaarten, .sgct-kaart, __icoon, __titel, __waarde (pages/contact.css, hun eigen contactpagina)',
  'De kanaalkaarten van de contactpagina van de referentie: de titel klein en in hoofdletters, daaronder het nummer of adres groot als link, en een dikke goudgele onderrand met een donkergele zijkant. Het voorwerp steekt linksboven uit de kaart.',
  () => lijst('k05', i => `<li class="k05-kaart k-neon"><span class="k05-icoon">${obj(i)}</span>${titel(i)}${link(i, 'k05-waarde')}${tekst(i)}</li>`));

add('06', 'Gele nis, nummer en blauw vlak', 'Referentie A · .diensten, .dienst__nis, .dienst__nr, .dienst__tekst (style.css)',
  'De dienstkaart van de referentie: bovenin een lichtgele nis met het voorwerp, dat boven de kaart uitsteekt, linksonder een goudgeel nummerlabel, daaronder een Koningsblauw vlak met witte tekst en een gele link. Onder de muis de hover van de referentie: 3px omhoog, het vlak wordt Diepblauw, het voorwerp groeit iets.',
  () => lijst('k06', i => `<li class="k06-kaart"><div class="k06-nis">${obj(i)}<span class="k06-nr" aria-hidden="true">${nr2(i)}</span></div><div class="k06-tekst">${titel(i)}${tekst(i)}${link(i)}</div></li>`));

add('07', 'Eén plaat, vier vakken', 'Referentie A · .stappen, .stap:not(:nth-child(4n+1)), .stap h3 (style.css, blok "Zo verloopt uw verhuizing")',
  'Geen losse kaarten maar één dikke lichtblauwe plaat met vier vakken, gescheiden door dunne lijnen. De voorwerpen breken door de bovenrand van de plaat, elk boven zijn eigen vak.',
  () => `<div class="k07-plaat">${lijst('k07', i => `<li class="k07-vak">${obj(i)}${titel(i)}${tekst(i)}${link(i)}</li>`)}</div>`);

add('08', 'Schuine gele band', 'Referentie A · .opslag__band, .opslag__lijn, .opslag__mark (style.css, blok Inboedelopslag)',
  'Een schuine goudgele band loopt van rand tot rand achter de kaarten, met een Diepblauwe streep eronder en het beeldmerk op de band. De witte kaarten staan op de band; de voorwerpen staan op de kaarten.',
  () => `<div class="k08-baan"><div class="k08-band" aria-hidden="true">${merkNeg('k08-merk')}</div><div class="k08-lijn" aria-hidden="true"></div>${lijst('k08', i => `<li class="k08-kaart k-neon">${obj(i)}${titel(i)}${tekst(i)}${link(i)}</li>`)}</div>`);

add('09', 'Vier bogen', 'Referentie A · .venster__boog, .venster__boog::after, .venster__persoon (style.css, blok "Na uw aanvraag")',
  'Elke kaart heeft bovenin een boog zoals het venster bij de referentie: lichtblauw met een goudgele binnenlijn. Het voorwerp staat onderin de boog en steekt er bovenuit. Daaronder de tekst op wit.',
  () => lijst('k09', i => `<li class="k09-kaart k-neon"><div class="k09-boog">${obj(i)}</div><div class="k09-tekst">${titel(i)}${tekst(i)}${link(i)}</div></li>`));

add('10', 'Diepblauwe plaat met driekleurenstreep', 'Referentie A · .zeker__card, .zeker__card::before, .zeker__list li, .zeker__ok (style.css, blok Erkende Verhuizer)',
  'Eén Diepblauwe plaat met bovenaan een streep in Koningsblauw, Goudgeel en lichtblauw. De vier kanalen staan naast elkaar met een dunne lijn erboven; de voorwerpen staan op goudgele schijven en steken boven de plaat uit. Witte tekst, gele links.',
  () => `<div class="k10-plaat">${merkNeg('k10-merk')}${lijst('k10', i => `<li class="k10-vak"><span class="k10-schijf">${obj(i)}</span>${titel(i)}${tekst(i)}${link(i)}</li>`)}</div>`);

// ============ referentie C ============
add('11', 'Aan de gele lijn', 'Referentie C · .b-belofte__band, __kaart, __haak, __baan::before (belofte.min.css)',
  'Een goudgele lijn van rand tot rand, met vier witte kaarten die er aan zwarte klemmen onder hangen, elk een fractie scheef. Onder de muis hangt de kaart recht, net als bij de referentie. Het voorwerp staat bovenin de kaart.',
  () => lijst('k11', i => `<li class="k11-kaart"><span class="k11-haak" aria-hidden="true"></span><span class="k11-voorwerp">${obj(i)}</span>${titel(i)}${tekst(i)}${link(i)}</li>`));

add('12', 'Grote fototegels met blauwe strook', 'Referentie C · .b-gezichten__raster, __tegel--thuis, __link, __tekst (gezichten.min.css)',
  'Vier grote foto\'s als tegels, "Bel ons" breder, zoals de thuisbasis bij de referentie. Onderaan elke tegel een doorschijnende Koningsblauwe strook met titel, tekst en link. Onder de muis komt de tegel omhoog en zoomt de foto iets in.',
  () => lijst('k12', i => `<li class="k12-tegel">${foto(i)}<div class="k12-strook">${titel(i)}${tekst(i)}${link(i)}</div></li>`));

add('13', 'Oplopende kaarten op een luchtfoto', 'Referentie C · .b-maten__foto, .b-maten__schaal, .b-maten__maat--2/--3, .b-maten__maat::before (maten.min.css)',
  'Een brede luchtfoto van een verhuizing: de wagen en de dozen op straat (de foto van de home-hero). Over de onderkant schuiven vier kaarten die oplopen in hoogte en in kleur, van wit naar Diepblauw, elk met een goudgeel lipje. Het voorwerp staat op de rechterbovenhoek van de kaart.',
  () => `<div class="k13-beeld"><figure class="k13-foto">${img('/img/hero-bg-1920.webp', 'k13-fotoimg', ' aria-hidden="true"')}</figure>${lijst('k13', i => `<li class="k13-maat k-neon">${obj(i)}${titel(i)}${tekst(i)}${link(i)}</li>`)}</div>`);

add('14', 'Fotoplaten aan één lijn', 'Referentie C · .b-historie__tl, __tl::before, __plaat, __jaar::before (historie.min.css)',
  'Op een goudgele band van rand tot rand: vier scheve fotoplaten met een witte rand, en onder de platen één Diepblauwe lijn met een stip per kanaal. De titel staat groot naast de stip, zoals de jaartallen bij de referentie.',
  () => `<div class="k14-band">${lijst('k14', i => `<li class="k14-stap"><figure class="k14-fig"><div class="k14-plaat">${foto(i)}</div></figure>${titel(i)}${tekst(i)}${link(i)}</li>`)}</div>`);

add('15', 'Kanaalvakken met foto en gele strook', 'Referentie B · .sgpr__kaart, .sgpr__rijen, .sgpr-rij, .sgpr__media, .sgpr__badge (blokken/prijzen.css)',
  'Eén witte kaart met een Koningsblauwe rand. Links de vier kanalen als vakken in een raster van twee bij twee, met het voorwerp klein linksboven en de link groot, zoals de prijzen bij de referentie. Rechts een hoge foto van de dozen met het logo en onderaan een goudgele strook met "7 dagen per week bereikbaar" uit de intro.',
  () => `<div class="k15-kaart"><div class="k15-body">${lijst('k15', i => `<li class="k15-rij">${obj(i)}<div class="k15-rijtekst">${titel(i)}${tekst(i)}</div>${link(i, 'k15-waarde')}</li>`)}</div><div class="k15-media"><div class="k15-beeld">${img('/img/voorbereiding-dozen.webp', 'k15-foto', ' aria-hidden="true"')}</div><p class="k15-badge"><b>7 dagen</b><span>per week bereikbaar</span></p></div></div>`);

// ---- pagina ----
const css = fs.readFileSync(path.join(__dirname, 'var.css'), 'utf8');
const boven = v => BOVEN.replace(/contactkaarten-kop/g, `kop-k${v}`);
const sectie = (v, inner) => `<section class="b-contactkaarten sectie sectie--wit v k s${v}" aria-labelledby="kop-k${v}">
  <div class="wrap">
    ${boven(v)}
    ${inner}
  </div>
</section>`;
const kap = (n, naam, bron, uitleg) => `<div class="vkap" id="v${n}"><div class="wrap"><span class="vkap__nr">${n}</span><div><b>${naam}</b><small>${bron}</small><p>${uitleg}</p></div><span class="vkap__maat" data-maat></span></div></div>`;
const bovenCtx = `<div class="vctx" aria-hidden="true"><div class="wrap">Hierboven op /contact/: "Zo vindt u ons" (Diepblauw)</div></div>`;
const onderCtx = `<div class="vctx vctx--blauw" aria-hidden="true"><div class="wrap">Hieronder: de schuine Koningsblauwe band (4,9 uit 5 op Google · Standaard verzekerd · ...)</div></div>`;
const live = SEC.replace('id="contactkaarten"', 'id="contactkaarten-live"').replace(/contactkaarten-kop/g, 'contactkaarten-kop-live');
const navl = ['00', ...V.map(x => x.n)].map(n => `<a href="#v${n}">${n}</a>`).join('');

const html = `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=' js'</script>
<title>Zo bereikt u ons · 15 ontwerpen voor de kanaalkaarten · referentie A, B en C</title>
<meta name="robots" content="noindex">
<link rel="preload" href="/fonts/archivo-condensed-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/min/site.min.css?v=${hash('site')}">
<link rel="stylesheet" href="/css/min/contactkaarten.min.css?v=${hash('contactkaarten')}">
<link rel="stylesheet" href="/css/min/uitsnede.min.css?v=${hash('uitsnede')}">
<link rel="stylesheet" href="/css/min/logomotief.min.css?v=${hash('logomotief')}">
<style>
${css}
</style>
<script src="/js/site.js?v=${jsHash}" defer></script>
</head>
<body class="p-contact">
${sprite}
<nav class="vnav" aria-label="Ontwerpen"><div class="wrap"><b>/contact/ Zo bereikt u ons · 15 ontwerpen</b><button class="vnav__knop" type="button" data-kop aria-pressed="false">Kop en belkaart verbergen</button><div class="vnav__links">${navl}</div></div></nav>
${kap('00', 'Nu live', 'Ter vergelijking, zo staat het op /contact/', 'De vier kaarten met de echte voorwerpen op een goudgele schijf. De klant vond dit mooi, maar niet "wow". In alle ontwerpen hieronder blijven de kop, de verhuizer en de belkaart gelijk; alleen de rij met de vier kanalen verandert.')}
${bovenCtx}
${live}
${onderCtx}
${V.map(x => kap(x.n, x.naam, x.bron, x.uitleg) + '\n' + bovenCtx + '\n' + sectie(x.n, x.kanalen()) + '\n' + onderCtx).join('\n')}
<div class="vkap vkap--eind"><div class="wrap"><p>Alle teksten en links zijn letterlijk die van /contact/. De voorwerpen zijn de echte foto's die nu live staan (telefoon, envelop, klembord, dozen); de foto's komen uit de eigen map (stap-2-bellen, stap-1-laptop, stap-1-formulier, stap-3-offerte, voorbereiding-dozen, hero-bg-1920). Geen nieuwe mensen: de verhuizer boven de kaarten staat er al. Elke bronklasse hierboven bestaat echt in de code van referentie A, B of C; in de De Reus-code komen die namen niet terug. Kies een nummer.</p></div></div>
<script>
(function(){
function meet(){document.querySelectorAll('[data-maat]').forEach(function(m){var s=m.closest('.vkap').nextElementSibling;while(s&&s.tagName!=='SECTION')s=s.nextElementSibling;if(!s)return;var h=Math.round(s.getBoundingClientRect().height);var k=s.querySelector('.kk,.k04-plaat,.k07-plaat,.k08-baan,.k10-plaat,.k13-beeld,.k14-band,.k15-kaart,.b-contactkaarten__kanalen');var r=k?Math.round(s.getBoundingClientRect().bottom-k.getBoundingClientRect().top):0;m.textContent='Sectie '+h+' px · kaartenrij '+r+' px';});}
addEventListener('load',meet);addEventListener('resize',meet);
var b=document.querySelector('[data-kop]');b.addEventListener('click',function(){var aan=document.body.classList.toggle('zonder-kop');b.setAttribute('aria-pressed',aan);b.textContent=aan?'Kop en belkaart tonen':'Kop en belkaart verbergen';meet();});
})();
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(REPO, '_ontwerpen/contactkanalen-wow-varianten.html'), html);
console.log('ok', html.length, V.length, K.map(k => k.titel).join(' | '));
