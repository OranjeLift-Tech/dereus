// Maakt _ontwerpen/annuleren-varianten.html: 10 ontwerpen voor "Annuleren en wijzigen" (/kosten/ #annuleren).
// Links een echte 3D-kalender (renders in img/kosten-kalender/), rechts de tekst. Teksten zijn letterlijk die van de site.
const fs = require('fs');
const ROOT = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus';
const kosten = fs.readFileSync(`${ROOT}/kosten/index.html`, 'utf8');
const symbool = id => (kosten.match(new RegExp(`<symbol id="${id}"[^]*?</symbol>`)) || [''])[0];
const SPRITE = `<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">${symbool('i-pijl')}</svg>`;
const K = { bureau: [769, 720], blok: [449, 720], wand: [363, 720], kubus: [832, 612], schuif: [719, 720], pen: [469, 720] };
const kal = n => `<img class="kal kal--${n}" src="/img/kosten-kalender/${n}.webp" alt="" width="${K[n][0]}" height="${K[n][1]}" loading="lazy" decoding="async">`;
const tekst = `<div class="kop"><p class="label">Annuleren</p><h2 class="h2">Annuleren en wijzigen</h2></div>
<p class="in">Plannen veranderen soms. Dit staat er in onze algemene voorwaarden (artikel 8) over annuleren:</p>
<ul class="rg"><li>U mag de verhuisovereenkomst annuleren.</li><li>Annuleert u tot twee weken voor de geplande verhuisdatum, dan kost dat € 250.</li><li>Annuleert u binnen twee weken voor de verhuisdatum, dan kunnen er aanvullende kosten bij komen.</li></ul>
<p class="slot">Moet uw verhuisdatum verschuiven? Neem dan zo snel mogelijk contact op met uw verhuisadviseur. Dan kijken we samen naar een nieuwe datum.</p>
<p class="ac"><a class="knop knop--link" href="/algemene-voorwaarden/"><span>Lees de algemene voorwaarden</span><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-pijl"/></svg></a></p>`;

const V = [
  ['Bureaukalender op de Crème plaat', 'bureau', 'De plaat van nu (Crème, blauwe rand), maar met een dikte. De bureaukalender staat ervoor, steekt links en boven uit de plaat en werpt een schaduw op de grond.'],
  ['Scheurkalender op een blauw paneel', 'blok', 'Links een Diepblauw paneel dat vóór de witte plaat staat, zoals op /offerte/. De scheurkalender met de 14 van twee weken komt boven het paneel uit.'],
  ['Wandkalender aan de kaartrand', 'wand', 'De kalender hangt met zijn punaise aan de bovenrand van de kaart en valt eroverheen naar beneden. De regels liggen verzonken in de plaat.'],
  ['Blokjeskalender op een plank', 'kubus', 'De blokjes 1 en 4 staan op een goudgele plank. De drie regels zijn losse platen met een gele schijf, elk een stap hoger dan de vorige.'],
  ['De datum verschuift', 'schuif', 'Twee kalenders met een goudgele pijl ertussen. Het stuk over verschuiven krijgt een eigen Koningsblauwe plaat, want daar gaat het beeld over.'],
  ['Kalender met pen, regels op papier', 'pen', 'De kalender met een omcirkelde dag en de pen. De regels staan op een vel papier met een klem, als een afvinklijst.'],
  ['Koningsblauwe band, kalender breekt uit', 'bureau', 'Een Koningsblauwe band met de dakrand. De kalender is groot en komt links uit de band naar voren; de tekst ligt op een witte plaat die over de band valt.'],
  ['Tijdlijn van twee weken', 'blok', 'De regels hangen aan een Diepblauwe rail met goudgele schijven, van boven naar beneden: eerst mag het, dan tot twee weken, dan binnen twee weken.'],
  ['Memoblaadjes', 'wand', 'Elke regel is een memoblaadje met een stukje plakband, licht gedraaid, naast de wandkalender. Speels, maar met de kleuren van het merkboek.'],
  ['3D-blokken op Diepblauw', 'kubus', 'Dezelfde blokken als de trap erboven: de regels hebben een boven- en zijvlak. De blokjeskalender staat groot links en komt uit de band.'],
];
const css = fs.readFileSync(`${__dirname}/annuleren-varianten.css`, 'utf8');
const nav = V.map((_, i) => `<a href="#o${i + 1}">${String(i + 1).padStart(2, '0')}</a>`).join('');
const secties = V.map(([naam, k, uitleg], i) => { const n = i + 1;
  return `<section class="ov" id="o${n}"><div class="wrap ov__kop"><span class="ov__nr">${String(n).padStart(2, '0')}</span><div><h3>${naam}</h3><p>${uitleg}</p></div></div>
<div class="aq a${n}"><div class="wrap"><div class="vak"><div class="beeld" aria-hidden="true">${kal(k)}</div><div class="tekst">${tekst}</div></div></div></div></section>`; }).join('\n');
fs.writeFileSync(`${ROOT}/_ontwerpen/annuleren-varianten.html`, `<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Annuleren en wijzigen · 10 ontwerpen</title>
<!-- Merkboek: kleuren, Archivo Condensed + Inter, label met huisje, .h2, .wrap en .knop komen uit de echte kernlaag van de site. -->
<link rel="stylesheet" href="/css/min/site.min.css">
<style>
${css}
</style>
</head>
<body>
${SPRITE}
<nav class="onav" aria-label="Ontwerpen"><div class="wrap"><strong>Annuleren en wijzigen · 10 ontwerpen</strong>${nav}</div></nav>
<main>
${secties}
</main>
</body>
</html>
`);
console.log('geschreven');
