// 15 ontwerpen voor de vier vragen onder "Wat kost een verhuizing?" op /kosten/ (blok extradiensten: opslag,
// verhuislift, montage, woningontruiming). Elk ontwerp neemt de opbouw van een echt blok van referentie A, B of C
// over; de bronklasse staat in het bijschrift.
// node gen.cjs  ->  _ontwerpen/extradiensten-referentie-varianten.html
// Teksten en links komen letterlijk uit kosten/index.html. De beelden zijn de vier dienstfoto's van /diensten/
// met hun uitsnede, zodat de mensen boven het kader uitsteken (zelfde rekensom als de uitsteekfoto van referentie B).
const fs = require('fs');
const path = require('path');
const REPO = path.resolve(__dirname, '../..');
const PAG = fs.readFileSync(path.join(REPO, 'kosten/index.html'), 'utf8');
const SEC = PAG.match(/<section class="b-extradiensten[\s\S]*?<\/section>/)[0];
const sprite = PAG.match(/<svg class="sprite"[\s\S]*?<\/svg>/)[0];
const link = n => PAG.match(new RegExp(`<link rel="stylesheet" href="/css/min/${n}\\.min\\.css\\?v=[0-9a-f]+">`))[0];
const jsTag = (PAG.match(/<script src="\/js\/site\.js\?v=[0-9a-f]+" defer><\/script>/) || [''])[0];

// ---- de live teksten ----
const D = [...SEC.matchAll(/<article class="b-extradiensten__kaart" id="([^"]+)"[\s\S]*?<h2 class="b-extradiensten__kop" id="[^"]+">([\s\S]*?)<\/h2>\s*<p>([\s\S]*?)<\/p>\s*<p class="b-extradiensten__acties"><a class="knop knop--link" href="([^"]+)"><span>([\s\S]*?)<\/span>/g)]
  .map(m => ({ id: m[1], kop: m[2], tekst: m[3], href: m[4], link: m[5] }));
if (D.length !== 4) throw new Error('live tekst niet gevonden: ' + D.length);

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
const ic = n => `<svg class="ic" aria-hidden="true" focusable="false" overflow="visible"><use href="#i-${n}"/></svg>`;

// ---- beelden: de dienstfoto's van /diensten/ + hun uitsnede (zelfde 4:3-kader) ----
// d0 = bovenkant van het onderwerp in de uitsnede, mid = midden van het onderwerp (gemeten op het alfakanaal)
const BEELD = {
  opslag: { foto: '/img/dienst-opslag-v3.webp', uit: '/img/dienst-opslag-v3-uit.webp', d0: .132, mid: .45, gezicht: '44% 22%' },
  verhuislift: { foto: '/img/dienst-verhuislift.webp', uit: '/img/dienst-verhuislift-uit.webp', d0: .225, mid: .56, gezicht: '62% 40%' },
  montage: { foto: '/img/dienst-montage-v2.webp', uit: '/img/dienst-montage-v2-uit.webp', d0: .033, mid: .64, gezicht: '60% 16%' },
  woningontruiming: { foto: '/img/dienst-woningontruiming-v2.webp', uit: '/img/dienst-woningontruiming-v2-uit.webp', d0: .093, mid: .6, gezicht: '50% 25%' },
};
const B = i => BEELD[D[i].id];
const popStijl = (b, extra) => `--d0:${b.d0};--mid:${b.mid};--ar:1.3333${extra ? ';' + extra : ''}`;
// foto in een raam, uitsnede van dezelfde foto in een strook erboven
const pop = (i, cls = '', extra = '') => `<div class="pop ${cls}" style="${popStijl(B(i), extra)}" aria-hidden="true"><div class="pop__raam">${img(B(i).foto, 'pop__foto')}</div><div class="pop__boven">${img(B(i).uit, '')}</div></div>`;
// alleen de uitsnede, voor een kleurvlak (boog, schijf)
const popLos = (i, cls = '', extra = '') => `<div class="pop pop--los ${cls}" style="${popStijl(B(i), extra)}" aria-hidden="true"><div class="pop__raam"></div><div class="pop__boven">${img(B(i).uit, '')}</div></div>`;

const kop = (i, cls = '') => `<h2 class="x-kop ${cls}">${D[i].kop}</h2>`;
const tekst = (i, cls = '') => `<p class="x-tekst ${cls}">${D[i].tekst}</p>`;
// het laatste woord en het pijltje breken niet los van elkaar
const knop = (i, cls = '') => { const w = D[i].link.split(' '), last = w.pop(); return `<a class="knop knop--link x-link ${cls}" href="${D[i].href}"><span>${w.join(' ')} <b class="x-nw">${last}${ic('pijl')}</b></span></a>`; };
const alles = i => kop(i) + tekst(i) + knop(i);
const naam = i => D[i].id[0].toUpperCase() + D[i].id.slice(1);
const nr2 = i => String(i + 1).padStart(2, '0');
const vier = f => D.map((_, i) => f(i)).join('');
const merk = (cls = '') => img('/img/logo/dereus-beeldmerk.svg', cls, ' aria-hidden="true"');
const merkNeg = (cls = '') => img('/img/logo/dereus-beeldmerk-negatief.svg', cls, ' aria-hidden="true"');
const sectie = (n, grond, inner) => `<section class="sectie v s${n} ${grond}" aria-label="Ontwerp ${n}">${inner}</section>`;

const V = [];
const add = (n, naam_, bron, uitleg, html) => V.push({ n, naam: naam_, bron, uitleg, html });

// ============ referentie A ============
add('01', 'Gele nis, nummer en blauw vlak', 'Referentie A · .diensten, .dienst, .dienst__nis, .dienst__nr, .dienst__tekst (style.css, blok diensten op de home)',
  'De dienstkaart van de referentie: bovenin de nis met de dienstfoto, linksonder een goudgeel nummerlabel, daaronder een Koningsblauw vlak met witte tekst en een gele link. De mensen steken boven de kaart uit. Onder de muis de hover van de referentie: 3px omhoog en het vlak wordt Diepblauw.',
  n => sectie(n, 'v--mist', `<div class="wrap"><ul class="xl o01" role="list">${vier(i => `<li class="o01-kaart x-donker"><div class="o01-nis">${pop(i)}<span class="o01-nr" aria-hidden="true">${nr2(i)}</span></div><div class="o01-tekst">${alles(i)}</div></li>`)}</ul></div>`));

add('02', 'Vier bogen', 'Referentie A · .venster__boog, .venster__boog::after, .venster__persoon (style.css, blok "Na uw aanvraag")',
  'Elke kaart heeft bovenin een boog zoals het venster van de referentie: lichtblauw met een goudgele binnenlijn. In de boog staan de mensen van de dienstfoto als uitsnede, zonder achtergrond, en ze komen er bovenuit. Daaronder de tekst op wit.',
  n => sectie(n, 'v--lucht', `<div class="wrap"><ul class="xl o02" role="list">${vier(i => `<li class="o02-kaart"><div class="o02-fig">${popLos(i)}</div><div class="o02-tekst">${alles(i)}</div></li>`)}</ul></div>`));

add('03', 'Schuine band met de mensen erop', 'Referentie A · .opslag, .opslag__band, .opslag__lijn, .opslag__kaart, .opslag__fig, .opslag__persoon (style.css, blok Inboedelopslag)',
  'Het opslagblok van de referentie: een schuine band van rand tot rand (Koningsblauw naar Diepblauw) met een goudgele lijn aan de onderkant. Links een Diepblauwe kaart met de vier vragen, rechts staan de twee verhuizers van de woningontruiming met de doos achter de lijn, zoals de persoon bij de referentie.',
  n => sectie(n, '', `<div class="o03-band" aria-hidden="true">${merkNeg('o03-merk')}</div><div class="o03-lijn" aria-hidden="true"></div><div class="wrap o03-in"><div class="o03-kaart x-donker"><ul class="xl o03-lijst" role="list">${vier(i => `<li>${alles(i)}</li>`)}</ul></div><div class="o03-fig">${img(BEELD.woningontruiming.uit, 'o03-persoon', ' aria-hidden="true"')}</div></div>`));

add('04', 'Kaart met foto en blauw paneel', 'Referentie A · .leadblock__card, .leadblock__media, .leadblock__panel, .leadblock__panel::before (style.css, het slotblok)',
  'Eén grote kaart zoals het slotblok van de referentie: links de foto van de verhuislift, waarvan de lift met de lading boven de kaart uitsteekt, rechts een Koningsblauw paneel met de lichtvlek rechtsboven. De vier vragen staan erin als uitklapregels; de eerste staat open. Past op één laptopscherm.',
  n => sectie(n, 'v--mist', `<div class="wrap"><div class="o04-kaart"><div class="o04-media">${pop(1, 'pop--vul')}</div><div class="o04-paneel x-donker">${vier(i => `<details class="o04-vraag"${i ? '' : ' open'}><summary>${kop(i)}<span class="o04-plus" aria-hidden="true">${ic('plus')}</span></summary><div class="o04-antwoord">${tekst(i)}${knop(i)}</div></details>`)}</div></div></div>`));

add('05', 'Vier kaarten met een portret', 'Referentie A · .otk-kaarten, .otk-kaart (over-ons, blok "Waar wij voor staan")',
  'De kaarten van de over-onspagina van de referentie: twee bij twee, wit met een dunne rand, links een vaste kolom en rechts de tekst. In de linkerkolom staat de dienstfoto als staand portret en het hoofd steekt boven de kaart uit.',
  n => sectie(n, 'v--mist', `<div class="wrap"><ul class="xl o05" role="list">${vier(i => `<li class="o05-kaart">${pop(i)}<div class="o05-tekst">${alles(i)}</div></li>`)}</ul></div>`));

// ============ referentie B ============
add('06', 'Foto-strook op een lichtblauwe V-band', 'Referentie B · .sgd1, .sgd1::before/::after, .sgd1-kaart, .sgd1-pop, .sgd1-pop__boven (blokken/diensten.css)',
  'Het dienstenblok van de referentie, dezelfde familie als de kanaalkaarten die op /contact/ gekozen zijn: een lichtblauwe band met een V-inkeping aan de bovenkant en een schuine punt onderaan, witte kaarten met een brede, lage foto waar de mensen bovenuit steken. Onder de muis komt de kaart 4px omhoog.',
  n => sectie(n, '', `<div class="wrap"><ul class="xl o06" role="list">${vier(i => `<li class="o06-kaart">${pop(i)}<div class="o06-tekst">${alles(i)}</div></li>`)}</ul></div>`));

add('07', 'Trap op de gele band', 'Referentie B · .sgm__beeld, .sgm__band, .sgm__kaarten, .sgm__kaart:nth-child, .sgm__figuur, .sgm__pil (blokken/manieren.css)',
  'De kaarten lopen als een trap op naar rechts, elk 2,5rem hoger, op een dikke goudgele band. Achter de bovenrand van elke kaart staan de mensen van die dienst, zoals de monteurs bij de referentie. Bovenin de kaart een pil met de dienst en het nummer. Onder de muis groeien de mensen iets.',
  n => sectie(n, 'v--wit', `<div class="wrap"><div class="o07-beeld"><div class="o07-band" aria-hidden="true"></div><ul class="xl o07" role="list">${vier(i => `<li class="o07-kaart" style="--d0:${B(i).d0};--mid:${B(i).mid}">${img(B(i).uit, 'o07-figuur', ' aria-hidden="true"')}<div class="o07-doos"><p class="o07-boven" aria-hidden="true"><span class="o07-pil">${naam(i)}</span><span class="o07-nr">${nr2(i)}</span></p>${alles(i)}</div></li>`)}</ul></div></div>`));

add('08', 'Vier kleurtegels met een fotoschijf', 'Referentie B · .sgw-tegel:nth-child(1-4), .sgw-tegel__3d (blokken/waarom.css)',
  'Vier tegels in vier merkkleuren: Diepblauw, Goudgeel, Lucht en Koningsblauw. Rechtsboven een ronde foto in een witte ring die boven de tegel uitsteekt, met het hoofd weer boven de ring, zoals het 3D-element bij de referentie.',
  n => sectie(n, 'v--mist', `<div class="wrap"><ul class="xl o08" role="list">${vier(i => `<li class="o08-tegel">${pop(i)}${alles(i)}</li>`)}</ul></div>`));

add('09', 'Goudgele plaat met foto-afdrukken', 'Referentie B · .sgt__paneel, .sgt__fotos figure, figcaption (blokken/toennu.css)',
  'Eén goudgele plaat over de hele breedte met een dikke onderrand. Daarop vier licht scheve foto-afdrukken met een witte rand en de dienst als donkere pil, zoals de team- en pandfoto bij de referentie. De mensen komen boven de afdruk uit.',
  n => sectie(n, 'v--wit', `<div class="wrap"><div class="o09-plaat"><ul class="xl o09" role="list">${vier(i => `<li class="o09-kaart"><figure class="o09-afdruk">${pop(i)}<figcaption>${naam(i)}</figcaption></figure>${alles(i)}</li>`)}</ul></div></div>`));

add('10', 'Prijskaart met vier vakken', 'Referentie B · .sgpr__kaart, .sgpr__rijen, .sgpr-rij, .sgpr-rij--uitgelicht, .sgpr__media, .sgpr__boven, .sgpr__badge (blokken/prijzen.css)',
  'De prijskaart van de referentie: één witte kaart met een Koningsblauwe rand. Links de vier vragen als vakken, twee bij twee; het vak onder de muis licht op (eerst het eerste, zoals "uitgelicht"). Rechts de foto van de woningontruiming waar de twee verhuizers boven de kaart uitkomen, met een goudgele strook "Alles in één offerte" uit de tekst over opslag.',
  n => sectie(n, 'v--mist', `<div class="wrap"><div class="o10-kaart"><div class="o10-body"><ul class="xl o10-rijen" role="list">${vier(i => `<li class="o10-rij">${alles(i)}</li>`)}</ul></div><div class="o10-media">${pop(3)}<p class="o10-badge"><b>Alles in één offerte</b></p></div></div></div>`));

// ============ referentie C ============
add('11', 'Vier foto\'s op schuine naden', 'Referentie C · .b-liftopslag__duo, __vak, __foto (clip-path), __kaart, __kaart::before, __vak::after (liftopslag.min.css, blok "Een verhuislift of opslag erbij")',
  'Het blok "Een verhuislift of opslag erbij" van de referentie, van twee naar vier foto\'s: de foto\'s staan op schuine naden met een smalle lucht ertussen, een witte kaart valt over de onderkant van elke foto, een nummerschijf met gele ring zit op de hoek van de kaart en op elke naad staat een goudgele "+". De mensen steken boven de fotorij uit.',
  n => sectie(n, 'v--mist', `<div class="wrap"><ul class="xl o11" role="list">${vier(i => `<li class="o11-vak">${pop(i)}<div class="o11-kaart" data-nr="${nr2(i)}">${alles(i)}</div></li>`)}</ul></div>`));

add('12', 'Grote foto met een bon', 'Referentie C · .b-voorwerk__foto, __kader (clip-path), __foto::before, __bon, __bonkop, __regel (voorwerk.min.css, blok "Wij regelen ook")',
  'Het blok "Wij regelen ook" van de referentie: links een grote schuin afgesneden foto (de monteur) tot aan de schermrand met een lichtblauw vlak eronder, rechts een bon die over de foto valt. Bovenaan de bon een Diepblauwe kop "Extra diensten" (de naam van deze factor hoger op /kosten/) met het beeldmerk, daaronder de vier vragen als regels.',
  n => sectie(n, 'v--wit', `<div class="wrap o12-in"><div class="o12-foto">${pop(2, 'pop--vul')}</div><div class="o12-bon"><p class="o12-bonkop"><span>Extra diensten</span>${merk('o12-merk')}</p><ul class="xl o12-regels" role="list">${vier(i => `<li class="o12-regel"><div class="o12-vraag">${ic('check')}${kop(i)}</div><div class="o12-antwoord">${tekst(i)}${knop(i)}</div></li>`)}</ul></div></div>`));

add('13', 'Kaarten met een grote plus', 'Referentie C · .b-combineer__plus, __kaarten, __vak, __vak::after, __tekst::before (combineer.min.css, blok "Combineer de lift met")',
  'Het blok "Combineer de lift met" van de referentie: achter de kaarten een reusachtige omlijnde plus, schuin gedraaid. Elke kaart heeft een foto met een goudgeel streepje eronder dat onder de muis de hele breedte vult, en een nummerschijf op de naad tussen foto en tekst. De mensen steken boven de kaart uit.',
  n => sectie(n, 'v--mist', `<div class="wrap"><svg class="o13-plus" viewBox="0 0 100 100" aria-hidden="true" focusable="false"><path d="M37 1h26v36h36v26H63v36H37V63H1V37h36z"/></svg><ul class="xl o13" role="list">${vier(i => `<li class="o13-kaart">${pop(i)}<div class="o13-tekst" data-nr="${nr2(i)}">${alles(i)}</div></li>`)}</ul></div>`));

add('14', 'Lijst met wisselende foto', 'Referentie C · .b-diensten__lijst, __rij, __link::after, __nr, __naam, __pijl, __beeld, __cijfer, __vak (diensten.min.css, blok "Wat wij voor u doen" op de home)',
  'Het dienstenblok van de home van de referentie: links de vier vragen als lijst met nummer, grote kop en een pijlrondje, rechts één foto met een groot omlijnd cijfer erachter. Ga met de muis over een vraag: de gele lijn loopt eronder door en rechts verschijnt de foto van die dienst (zonder script, met :has).',
  n => sectie(n, 'v--wit', `<div class="wrap o14-in"><ul class="xl o14-lijst" role="list">${vier(i => `<li class="o14-rij"><span class="o14-nr" aria-hidden="true">${nr2(i)}</span><div class="o14-tekst">${alles(i)}</div><span class="o14-pijl" aria-hidden="true">${ic('pijl')}</span></li>`)}</ul><div class="o14-beeld" aria-hidden="true">${vier(i => `<div class="o14-foto"><span class="o14-cijfer">${nr2(i)}</span><div class="o14-vak">${pop(i, 'pop--vul')}</div></div>`)}</div></div>`));

add('15', 'Tabbladen met foto', 'Referentie C · .b-kiezer__tabs, __tab, __nr, __tabicoon, __schuif::before, __paneel, __foto, __groot, __tekst (kiezer.min.css, /diensten/ "Waarmee kunnen wij u helpen")',
  'De kiezer van de dienstenpagina van de referentie: vier tabbladen met nummer, een rond fotootje en de dienst; het gekozen tabblad is Diepblauw met een gele streep. Daaronder één paneel: een witte kaart met de vraag over een grote foto heen, met een groot omlijnd nummer erachter. Klik op een tabblad om te wisselen. Het laagste blok van de vijftien.',
  n => sectie(n, 'v--mist', `<div class="wrap"><div class="o15" data-kiezer><div class="o15-tabs" role="tablist" aria-label="Extra diensten">${vier(i => `<button class="o15-tab" type="button" role="tab" id="o15-t${n}${i}" aria-controls="o15-p${n}${i}" aria-selected="${i ? 'false' : 'true'}"${i ? ' tabindex="-1"' : ''}><span class="o15-nr">${nr2(i)}</span><span class="o15-tabicoon">${img(B(i).foto, '', ` style="object-position:${B(i).gezicht}"`)}</span><span class="o15-tabtekst">${naam(i)}</span></button>`)}</div><div class="o15-panelen">${vier(i => `<div class="o15-paneel" role="tabpanel" id="o15-p${n}${i}" aria-labelledby="o15-t${n}${i}"${i ? ' hidden' : ''}><div class="o15-foto">${pop(i)}</div><span class="o15-groot" aria-hidden="true">${nr2(i)}</span><div class="o15-tekst">${alles(i)}</div></div>`)}</div></div></div>`));

// ---- pagina ----
const css = fs.readFileSync(path.join(__dirname, 'var.css'), 'utf8');
const navl = ['00', ...V.map(x => x.n)].map(n => `<a href="#v${n}">${n}</a>`).join('');
const kap = (n, naam_, bron, uitleg) => `<div class="vkap" id="v${n}"><div class="wrap"><span class="vkap__nr">${n}</span><div><b>${naam_}</b><small>${bron}</small><p>${uitleg}</p></div><span class="vkap__maat" data-maat></span></div></div>`;
// op /kosten/ staat erboven de Diepblauwe trapband "Wat kost een verhuizing?" en eronder "Annuleren en wijzigen" (wit)
const boven = `<div class="vctx" aria-hidden="true"><div class="wrap">Hierboven op /kosten/: Wat kost een verhuizing? (de Diepblauwe trapband)</div></div>`;
const onder = `<div class="vctx vctx--wit" aria-hidden="true"><div class="wrap">Hieronder: Annuleren en wijzigen (wit, Crème plaat met de bureaukalender)</div></div>`;
const live = `<div class="p-kosten">${SEC.replace(/id="(opslag|verhuislift|montage|woningontruiming)(-kop)?"/g, 'id="$1$2-live"').replace(/aria-labelledby="([a-z]+)-kop"/g, 'aria-labelledby="$1-kop-live"')}</div>`;

const html = `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=' js'</script>
<title>Extra diensten op /kosten/ · 15 ontwerpen · referentie A, B en C</title>
<meta name="robots" content="noindex">
<link rel="preload" href="/fonts/archivo-condensed-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
${link('site')}
${link('extradiensten')}
${link('kosten-diepte')}
<style>
${css}
</style>
${jsTag}
</head>
<body>
${sprite}
<nav class="vnav" aria-label="Ontwerpen"><div class="wrap"><b>/kosten/ Wat kost opslag, een verhuislift, montage, een woningontruiming · 15 ontwerpen</b><div class="vnav__links">${navl}</div></div></nav>
${kap('00', 'Zo staat het blok nu live', 'Ter vergelijking', 'Vier platen van wit naar Diepblauw met een klei-voorwerp erbovenop. Elk ontwerp hieronder vervangt alleen dit blok en houdt precies dezelfde vier koppen, teksten en links.')}
${boven}
${live}
${onder}
${V.map(x => kap(x.n, x.naam, x.bron, x.uitleg) + '\n' + boven + '\n' + x.html(x.n) + '\n' + onder).join('\n')}
<div class="vkap vkap--eind"><div class="wrap"><p>Alle koppen, teksten en links zijn letterlijk die van /kosten/. De beelden zijn de vier dienstfoto's die nu op /diensten/ staan (opslag, verhuislift, montage, woningontruiming) met hun eigen uitsnede, dus geen klei-iconen en geen nieuwe mensen. Alleen de woorden "Extra diensten" (12, de factor hoger op /kosten/) en "Alles in één offerte" (10, uit de tekst over opslag) staan er als label bij. Elke bronklasse hierboven bestaat echt in de code van referentie A, B of C; in de De Reus-code komen die namen niet terug. Rechts in elke kop staat de hoogte van het blok op dit scherm (een laptop toont zo'n 730 px). Kies een nummer.</p></div></div>
<script>
(function(){
function meet(){document.querySelectorAll('[data-maat]').forEach(function(m){var s=m.closest('.vkap').nextElementSibling;while(s&&!(s.tagName==='SECTION'||s.classList.contains('p-kosten')))s=s.nextElementSibling;if(!s)return;var h=Math.round(s.getBoundingClientRect().height);m.textContent='Blokhoogte '+h+' px';m.classList.toggle('is-hoog',h>760);});}
addEventListener('load',meet);addEventListener('resize',meet);
document.querySelectorAll('[data-kiezer]').forEach(function(k){var t=[].slice.call(k.querySelectorAll('[role=tab]')),p=[].slice.call(k.querySelectorAll('[role=tabpanel]'));
function kies(i,focus){t.forEach(function(u,j){var aan=i===j;u.setAttribute('aria-selected',aan);u.tabIndex=aan?0:-1;p[j].hidden=!aan;});if(focus)t[i].focus();}
t.forEach(function(u,i){u.addEventListener('click',function(){kies(i);});u.addEventListener('keydown',function(e){var d=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(d){e.preventDefault();kies((i+d+t.length)%t.length,true);}});});});
})();
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(REPO, '_ontwerpen/extradiensten-referentie-varianten.html'), html);
console.log('ok', html.length, V.length, D.map(d => d.id).join(' | '));
