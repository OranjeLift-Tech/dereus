// Maakt _ontwerpen/vragen-contact-varianten.html: 20 ontwerpen voor "Vragen over contact" (/contact/ #vragen).
// Teksten zijn letterlijk die van de site. Iconen komen uit de sprite van contact/index.html.
const fs = require('fs');
const ROOT = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus';
const contact = fs.readFileSync(`${ROOT}/contact/index.html`, 'utf8');
const symbool = id => (contact.match(new RegExp(`<symbol id="${id}"[^]*?</symbol>`)) || [''])[0];
const SPRITE = `<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">${['i-telefoon', 'i-whatsapp', 'i-pijl'].map(symbool).join('')}</svg>`;
const ic = n => `<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-${n}"/></svg>`;
const WA = `<a class="wa-link" href="https://wa.me/31850005647" aria-label="Contact met Verhuisbedrijf De Reus via WhatsApp" title="Contact via WhatsApp">${ic('whatsapp')}<span class="wa-link__tekst">WhatsApp</span></a>`;

const VRAGEN = [
  ['Hoe snel krijg ik antwoord?', `Binnen 24 uur, telefonisch of per mail. Heeft u haast? Bel ons dan op <a href="tel:+31850005647">085 000 5647</a>${WA}.`],
  ["Kan ik ook 's avonds of in het weekend bellen?", 'Ja. Wij zijn bereikbaar van maandag tot en met zaterdag van 08.00 tot 20.00 uur, en op zondag van 09.00 tot 17.00 uur.'],
  ['Wat zet ik in mijn bericht?', 'Vertel kort waar uw vraag over gaat. Gaat het om een verhuizing, noem dan ook waar u vandaan komt, waar u naartoe gaat en wanneer. Dan kunnen wij u meteen goed helpen.'],
  ['Gebruik ik het contactformulier of het offerteformulier?', 'Wilt u weten wat uw verhuizing kost? Gebruik dan het <a href="/offerte/">offerteformulier</a>. Voor alle andere vragen is het contactformulier op deze pagina handig.'],
];
const lijst = (n, open = 0) => VRAGEN.map(([v, a], i) => `<details class="vr"${i === open ? ' open' : ''}><summary><span class="nr" aria-hidden="true">0${i + 1}</span><span class="tk">${v}</span><span class="pl" aria-hidden="true"></span></summary><div class="an"><p>${a}</p></div></details>`).join('');
const kop = `<div class="kopgroep"><p class="label">Veelgestelde vragen</p><h2 class="h2">Vragen over contact</h2></div>`;
const bel = `<div class="bel"><span class="st"><i></i>Nu bereikbaar</span><p>Staat uw vraag er niet bij?</p><div class="kn"><a class="knop knop--blauw knop--icoon-voor" href="tel:+31850005647"><span>Bel 085 000 5647</span>${ic('telefoon')}</a>${WA}</div></div>`;
const img = (src, kl, w, h) => `<img class="${kl}" src="${src}" alt="" width="${w}" height="${h}" loading="lazy" decoding="async">`;
const O = { tel: ['/img/contact-3d/telefoon.webp', 208, 400], env: ['/img/contact-3d/envelop.webp', 347, 400], form: ['/img/contact-3d/formulier.webp', 346, 400], doos: ['/img/contact-3d/doos.webp', 425, 400],
  score: ['/img/contact-3d/score.webp', 411, 320], schild: ['/img/contact-3d/schild.webp', 251, 320], head: ['/img/contact-3d/headset.webp', 287, 320], klok: ['/img/contact-3d/klok.webp', 279, 320] };
const obj = (k, kl = 'ob') => img(O[k][0], kl, O[k][1], O[k][2]);

const V = [
  ['Platen met gele schijven', 'Witte platen met een zichtbare dikte, het nummer als goudgele schijf die erbovenop staat. De telefoon komt uit de belkaart.', `${kop}<div class="belw">${bel}${obj('tel')}</div>`],
  ['Verhuisdozen', 'Elke vraag is een kartonnen doos met plakband en een gestempeld nummer; het antwoord ligt als pakbon in de open doos.', `${kop}${bel}${obj('doos')}`],
  ['Servicebalie met headset', 'Links een Diepblauw paneel dat voor de sectie staat, met de headset van de verhuisadviseur. De vragen hebben een Koningsblauwe zijkant.', `<div class="paneel">${kop}${bel}${obj('head')}</div>`],
  ['Klok: altijd bereikbaar', 'De klok staat groot achter de belkaart. De vragen zijn pilvormige platen, zoals de knoppen van de site.', `${kop}<div class="belw">${obj('klok')}${bel}</div>`],
  ['Ladekast', 'Vier laden van een blauwe archiefkast: metalen greep, kaartje met het nummer. De open lade laat het antwoord op papier zien.', `${kop}${bel}`],
  ['Klembord', 'De vragen staan op een vel papier op een Koningsblauw klembord met een stalen klem. Het klembord ligt schuin naast de belkaart.', `${kop}${bel}${obj('form')}`],
  ['Trap', 'De vier vragen zijn traptreden die naar rechts omhoog lopen, met het beeldmerk bovenaan, net als de trap op /kosten/.', `${kop}${bel}`],
  ['Enveloppen', 'Elke vraag is een envelop; bij het openen schuift het antwoord er als brief uit. Links de Koningsblauwe envelop.', `${kop}${bel}${obj('env')}`],
  ['Kaartenstapel', 'Elke vraag ligt op een stapeltje kaarten: je ziet de randen van de kaarten eronder. Het nummer zit op een blauw tabje.', `${kop}${bel}${obj('score')}`],
  ['Diepblauwe band', 'De hele sectie is een Diepblauwe band met de dakrand. Donkere platen met goudgele nummers, de telefoon licht erbovenuit.', `${kop}${bel}${obj('tel')}`],
  ['Het team stapt uit de kaart', 'De echte teamfoto staat achter de belkaart: de mensen komen boven de kaart uit en staan zo letterlijk achter het nummer.', `${kop}<div class="belw">${img('/img/team/team-hero-700.webp', 'team', 700, 714)}${bel}</div>`],
  ['Hangmappen', 'Vier hangmappen in Crème met een verspringend goudgeel tabje. De open map laat het antwoord zien.', `${kop}${bel}`],
  ['Labels aan een rail', 'Elke vraag is een label met een oogje, aan een touwtje aan een stalen rail, zoals de labels op verhuisdozen.', `${kop}${bel}`],
  ['Verzendlabels', 'Hetzelfde idioom als het Van en Naar in het formulier: Koningsblauwe rand, harde schaduw, stippellijn, streepjescode en de gele pijlschijf.', `${kop}${bel}${obj('doos')}`],
  ['Vier tegels met een voorwerp', 'Een raster van 2 x 2. Bij elke vraag hoort een echt voorwerp dat uit de tegel komt: klok, telefoon, envelop en klembord.', `${kop}${bel}`],
  ['Gesprek op de telefoon', 'Een echte telefoon met een gesprek: de vraag is het bericht van de klant, het antwoord komt van De Reus.', `${kop}${bel}`],
  ['Route met schijven', 'Een Diepblauwe rail met goudgele nummerschijven, zoals "Zo gaat het verder" op /offerte/. De platen hangen met een pijltje aan de rail.', `${kop}${bel}${obj('schild')}`],
  ['Huisjes uit het logo', 'Het nummer staat in het goudgele huis uit het logo, met een donkergele zijkant. Links het beeldmerk groot op een Diepblauw paneel.', `${kop}<div class="merkp">${img('/img/logo/dereus-beeldmerk-negatief.svg', 'merk', 1000, 509)}</div>${bel}`],
  ['Tickets', 'Elke vraag is een ticket: een afscheurstrook met het nummer, een perforatie en inkepingen aan de zijkant.', `${kop}${bel}${obj('head')}`],
  ['Foto in het huis', 'Links het huis uit het logo als venster; de drie verhuizers stappen eruit. Rechts de vragen als platen die over de rand van het paneel vallen.', `${kop}<div class="huisw"><span class="huis"></span>${img('/img/helpen-wij-u-snel.webp', 'mensen', 900, 462)}</div>${bel}`],
];

const css = fs.readFileSync(`${__dirname}/vragen-varianten.css`, 'utf8');
const nav = V.map((_, i) => `<a href="#o${i + 1}">${String(i + 1).padStart(2, '0')}</a>`).join('');
const secties = V.map(([naam, uitleg, links], i) => { const n = i + 1;
  return `<section class="ov" id="o${n}"><div class="wrap ov__kop"><span class="ov__nr">${String(n).padStart(2, '0')}</span><div><h3>${naam}</h3><p>${uitleg}</p></div></div>
<div class="vq q${n}"><div class="wrap vq__in"><div class="vq__links">${links}</div><div class="vq__lijst">${lijst(n, n === 15 ? -1 : 0)}</div></div></div></section>`; }).join('\n');
const html = `<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Vragen over contact · 20 ontwerpen</title>
<!-- Merkboek: kleuren, Archivo Condensed + Inter, label met huisje, .h2, .wrap, .knop en .wa-link komen uit de echte kernlaag. -->
<link rel="stylesheet" href="/css/min/site.min.css">
<style>
${css}
</style>
</head>
<body>
${SPRITE}
<nav class="onav" aria-label="Ontwerpen"><div class="wrap"><strong>Vragen over contact · 20 ontwerpen</strong>${nav}</div></nav>
<main>
${secties}
</main>
</body>
</html>
`;
fs.writeFileSync(`${ROOT}/_ontwerpen/vragen-contact-varianten.html`, html);
console.log('geschreven:', html.length, 'tekens');
