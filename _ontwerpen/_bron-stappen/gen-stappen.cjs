// Genereert _ontwerpen/werkwijze-stappen-varianten.html (15 ontwerpen voor /werkwijze/ #stappen)
const fs = require('fs');
const path = require('path');
const REPO = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus/dereus';
const live = fs.readFileSync(path.join(REPO, 'werkwijze/index.html'), 'utf8');
const hash = n => (live.match(new RegExp(`/css/min/${n}\\.min\\.css\\?v=([0-9a-f]+)`)) || [])[1];
const sprite = live.match(/<svg class="sprite"[\s\S]*?<\/svg>/)[0];
const liveSectie = live.match(/<section class="b-tijdlijn[\s\S]*?<\/section>/)[0];

const S = [
  { nr: '01', titel: 'Offerte aanvragen', regel: 'U vertelt ons kort waar u vandaan komt, waar u naartoe gaat en wanneer u wilt verhuizen.',
    u: 'U vult het formulier in, of u belt ons op <a href="tel:+31850005647">085 000 5647</a>.', wij: 'Wij lezen uw aanvraag en koppelen u aan een vaste verhuisadviseur.',
    obj: ['/img/contact-3d/formulier.webp', 346, 400, 1] },
  { nr: '02', titel: 'Persoonlijk contact', regel: 'Binnen 24 uur na uw aanvraag belt uw verhuisadviseur u.',
    u: 'U vertelt wat er mee moet, hoe beide adressen bereikbaar zijn en wat u zelf wilt doen.', wij: 'Wij denken mee, beantwoorden uw vragen en schatten in hoeveel werk de verhuizing is.',
    obj: ['/img/contact-3d/telefoon.webp', 208, 400, 1.08] },
  { nr: '03', titel: 'Offerte ontvangen', regel: 'U krijgt een duidelijke, vrijblijvende offerte op maat.',
    u: 'U leest de offerte rustig door.', wij: 'Wij stellen de offerte op, doorgaans nog dezelfde dag als het gesprek.', meer: true,
    obj: ['/img/kaart-3d/klembord.webp', 600, 792, .98] },
  { nr: '04', titel: 'Planning bevestigen', regel: 'Pas als u de offerte accepteert, is de afspraak rond.',
    u: 'U accepteert de offerte.', wij: 'Wij zetten de datum vast en bereiden de verhuisdag voor.',
    obj: ['/img/contact-3d/klok.webp', 279, 320, .87] },
  { nr: '05', titel: 'Verhuisdag', regel: 'Onze verhuizers staan op het afgesproken tijdstip voor de deur.',
    u: 'U wijst aan waar alles moet komen.', wij: 'Wij doen het zware werk, van de eerste doos tot de laatste kast.',
    obj: ['/img/kosten-3d/wagen.webp', 594, 420, .75] },
];

const pijl = '<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-pijl"/></svg>';
const img = (src, w, h, cls = '', extra = '') => `<img class="${cls}" src="${src}" alt="" width="${w}" height="${h}" loading="lazy" decoding="async"${extra}>`;
const obj = (s, cls = '') => img(s.obj[0], s.obj[1], s.obj[2], `obj ${cls}`.trim(), ` style="--f:${s.obj[3]}"`);
const huisRender = (cls = '') => img('/img/kosten-3d/huis.webp', 425, 420, `obj obj--huis ${cls}`.trim(), ' style="--f:1"');
const huisFoto = (cls = '') => `<span class="huisfoto ${cls}" aria-hidden="true">${img('/img/nieuw-huis.webp', 400, 450)}</span>`;
const titel = (s, cls = '') => `<h3 class="${cls}"><span class="vh">Stap ${+s.nr}: </span>${s.titel}</h3>`;
const nr = (s, cls) => `<span class="${cls} nr" aria-hidden="true">${s.nr}</span>`;
const meer = s => s.meer ? `<p class="uk__meer"><a class="knop knop--link" href="/kosten/"><span>Wat de prijs bepaalt</span>${pijl}</a></p>` : '';
const duo = s => `<dl class="uk__duo"><div class="uk__wie uk__wie--u"><dt>Wat u doet</dt><dd>${s.u}</dd></div><div class="uk__wie uk__wie--wij"><dt>Wat wij doen</dt><dd>${s.wij}</dd></div></dl>`;
const uk = (s, v, cls = '') => `<details class="uk ${cls}" name="uk-${v}"><summary><span>Wat u doet en wat wij doen</span><span class="uk__plus" aria-hidden="true"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-plus"/></svg></span></summary><div class="uk__paneel">${duo(s)}${meer(s)}</div></details>`;
const kop = (v, cls = '') => `<div class="kopgroep ${cls}"><p class="label">In vijf stappen</p><h2 id="kop-${v}">Van aanvraag tot verhuisdag</h2><p class="intro">Elke verhuizing loopt bij ons via dezelfde vijf stappen. Zo weet u steeds waar u aan toe bent.</p></div>`;
const slotB = '<b class="slot__kop">Uw nieuwe huis</b>';
const slotP = '<p class="slot__tekst">Van uw eerste vraag tot de sleutel in uw nieuwe deur. Eén vaste verhuisadviseur loopt de hele route met u mee.</p>';
const cta = (cls = '') => `<a class="knop knop--cta ${cls}" href="/offerte/"><span>Offerte aanvragen</span>${pijl}</a>`;
const sec = (v, cls, inner, style = '') => `<section class="sectie ${cls} v v${v}" aria-labelledby="kop-${v}"${style}>\n<div class="wrap">\n${inner}\n</div>\n</section>`;

const V = [];

// 01 referentie A-plaat
V.push({ n: '01', naam: 'Referentie A-plaat met het team', bron: 'Referentie A: .werkwijze__top + .stappen', uitleg: 'Kop links, het team met dozen rechts staat op één witte plaat met dikte. Vijf kolommen met dunne lijnen en grote blauwe cijfers met een gele zijkant; het slot staat onderin dezelfde plaat.',
  html: v => sec(v, 'sectie--mist', `<div class="v01__top">${kop(v)}<figure class="v01__team" aria-hidden="true">${img('/img/team/team-hero-dozen-1100.webp', 1100, 1195)}</figure></div>
<div class="v01__plaat"><ol class="v01__lijst" role="list">${S.map(s => `<li class="v01__stap"><div class="v01__nrrij">${nr(s, 'v01__nr')}${obj(s)}</div>${titel(s)}<p class="v01__regel">${s.regel}</p>${uk(s, v)}</li>`).join('')}</ol>
<div class="v01__slot">${huisFoto('v01__huis')}<div>${slotB}${slotP}</div>${cta()}</div></div>`) });

// 02 referentie A-dienstkaarten
V.push({ n: '02', naam: 'Dienstkaarten met geel nummerblok', bron: 'Referentie A: .dienst + .dienst__nr', uitleg: 'Vijf Koningsblauwe kaarten zoals de dienstkaarten van referentie A: bovenin een lichte nis waar het 3D-voorwerp boven de kaart uitsteekt, links onderin het gele nummerblok. Hover zoals referentie A: 3px omhoog, kaart wordt donkerder.',
  html: v => sec(v, 'sectie--lucht', `${kop(v, 'kopgroep--midden')}
<ol class="v02__lijst" role="list">${S.map(s => `<li class="v02__kaart"><div class="v02__nis">${obj(s)}${nr(s, 'v02__nr')}</div><div class="v02__tekst">${titel(s)}<p>${s.regel}</p>${uk(s, v, 'uk--donker')}</div></li>`).join('')}</ol>
<div class="v02__slot"><div class="v02__foto">${img('/img/nieuw-huis.webp', 400, 450)}</div><div>${slotB}${slotP}</div>${cta()}</div>`) });

// 03 Trap
V.push({ n: '03', naam: 'De trap naar uw nieuwe huis', bron: 'De Reus: treden op /kosten/ (niet van referentie A)', uitleg: 'Vijf treden die van links naar rechts oplopen, met het cijfer op de blauwe stootbord. Bovenaan staat de voordeur als zesde, gele trede met de knop.',
  html: v => sec(v, 'sectie--wit', `${kop(v, 'kopgroep--midden')}
<div class="v03__trap"><ol class="v03__lijst" role="list">${S.map((s, i) => `<li class="v03__trede" style="--i:${i}"><div class="v03__kaart">${obj(s)}${titel(s)}<p>${s.regel}</p>${uk(s, v)}</div><div class="v03__stoot">${nr(s, 'v03__nr')}</div></li>`).join('')}</ol>
<div class="v03__trede v03__trede--huis" style="--i:5"><div class="v03__kaart">${huisFoto('v03__huis')}${slotB}${slotP}${cta()}</div><div class="v03__stoot"></div></div></div>`) });

// 04 Diepblauwe band
V.push({ n: '04', naam: 'Diepblauwe band met gele schijven', bron: 'Referentie A: donkere band + .trust, De Reus: dakrand', uitleg: 'De enige Diepblauwe band van de pagina, met de dakrand. Witte platen met een gele 3D-zijkant; elk voorwerp staat op een gele schijf op een gestippelde route. Slot als gele plaat met het huis dat eruit omhoog komt.',
  html: v => sec(v, 'sectie--diep', `${kop(v, 'kopgroep--midden')}
<ol class="v04__lijst" role="list">${S.map(s => `<li class="v04__kaart"><span class="v04__schijf" aria-hidden="true">${obj(s)}</span>${nr(s, 'v04__nr')}${titel(s)}<p>${s.regel}</p>${uk(s, v)}</li>`).join('')}</ol>
<div class="v04__slot">${huisRender()}<div>${slotB}${slotP}</div>${cta()}</div>`) });

// 05 Verticale route met team
V.push({ n: '05', naam: 'Route naast het team', bron: 'Referentie A: .werkwijze__top op zijn kant', uitleg: 'Links blijven kop, team en slot staan (sticky), rechts loopt de gele route omlaag langs vijf brede platen. Elk voorwerp staat in het gele huis uit het logo.',
  html: v => sec(v, 'sectie--mist', `<div class="v05__raster"><div class="v05__links">${kop(v)}<figure class="v05__team" aria-hidden="true">${img('/img/team/team-hero-dozen-1100.webp', 1100, 1195)}</figure>
<div class="v05__slot">${huisFoto('v05__huis')}<div>${slotB}${slotP}${cta()}</div></div></div>
<ol class="v05__lijst" role="list">${S.map(s => `<li class="v05__stap"><span class="v05__badge" aria-hidden="true">${obj(s)}</span><div class="v05__kaart"><div class="v05__tekst"><div class="v05__kopregel">${nr(s, 'v05__nr')}${titel(s)}</div><p>${s.regel}</p></div>${uk(s, v)}</div></li>`).join('')}</ol></div>`) });

// 06 Fotoband met overlap
V.push({ n: '06', naam: 'Echte foto met overlappende platen', bron: 'Referentie A: hero met foto van rand tot rand', uitleg: 'Een brede foto van de verhuisdag met de kop links op een Diepblauw verloop. De vijf platen schuiven over de onderrand van de foto heen; de voorwerpen steken er rechtsboven uit.',
  html: v => sec(v, 'sectie--mist', `<div class="v06__foto">${img('/img/verhuisdag-aankomst.webp', 1400, 1050)}${kop(v)}</div>
<ol class="v06__lijst" role="list">${S.map(s => `<li class="v06__kaart">${obj(s)}${nr(s, 'v06__nr')}${titel(s)}<p>${s.regel}</p>${uk(s, v)}</li>`).join('')}</ol>
<div class="v06__slot">${huisFoto('v06__huis')}<div>${slotB}${slotP}</div>${cta()}</div>`) });

// 07 Weg naar de voordeur
V.push({ n: '07', naam: 'De weg naar de voordeur', bron: 'De Reus: weg op de homepage, referentie A: .route-lijn', uitleg: 'Vijf platen staan langs een echte asfaltweg die van de schermrand komt; op de weg ligt onder elke stap een gele halte met het cijfer. De weg eindigt bij de echte voordeur, met daarboven het slot en de knop.',
  html: v => sec(v, 'sectie--lucht', `${kop(v, 'kopgroep--midden')}
<div class="v07__veld"><ol class="v07__lijst" role="list">${S.map(s => `<li class="v07__stap"><div class="v07__kaart">${obj(s)}${titel(s)}<p>${s.regel}</p>${uk(s, v)}</div><span class="v07__halte" aria-hidden="true">${s.nr}</span></li>`).join('')}</ol>
<div class="v07__eind"><div class="v07__eindtekst">${slotB}${slotP}${cta()}</div>${huisFoto('v07__huis')}</div></div>`) });

// 08 Grote cijfers 3x2
V.push({ n: '08', naam: 'Zes tegels met grote cijfers', bron: 'Referentie A: .stap__nr (groot cijfer) + .tips-grid', uitleg: 'Drie bij twee: vijf brede witte tegels met een groot blauw cijfer dat over de rand valt en het voorwerp dat rechtsboven uitsteekt. De zesde tegel is het slot in Diepblauw met de voordeur.',
  html: v => sec(v, 'sectie--mist', `${kop(v, 'v08__kop')}
<div class="v08__raster"><ol class="v08__lijst" role="list">${S.map(s => `<li class="v08__tegel">${nr(s, 'v08__nr')}${obj(s)}${titel(s)}<p>${s.regel}</p>${uk(s, v)}</li>`).join('')}</ol>
<div class="v08__tegel v08__tegel--slot">${huisFoto('v08__huis')}${slotB}${slotP}${cta()}</div></div>`) });

// 09 Blauwverloop
V.push({ n: '09', naam: 'Blauwverloop', bron: 'De Reus: extradiensten (gekozen ontwerp 06)', uitleg: 'Dezelfde taal als de gekozen extradiensten op /kosten/: vijf kaarten die van wit naar Diepblauw lopen, met het 3D-voorwerp bovenop elke kaart en gele knoppen op de donkere kaarten.',
  html: v => sec(v, 'sectie--wit', `${kop(v, 'kopgroep--midden')}
<ol class="v09__lijst" role="list">${S.map((s, i) => `<li class="v09__kaart${i > 2 ? ' v09__kaart--donker' : ''}">${obj(s)}${nr(s, 'v09__nr')}${titel(s)}<p>${s.regel}</p>${uk(s, v, i > 2 ? 'uk--geel' : '')}</li>`).join('')}</ol>
<div class="v09__slot">${huisRender()}<div>${slotB}${slotP}</div>${cta()}</div>`) });

// 10 Adviseur leidt de route
V.push({ n: '10', naam: 'Uw verhuisadviseur loopt mee', bron: 'Referentie A: .tips-grid + .werkwijze__wagen', uitleg: 'Links één witte plaat met vijf rijen (cijfer, voorwerp, tekst, uitklap). Rechts de verhuisadviseur die boven een Koningsblauwe kaart uitstapt, met de slottekst "Eén vaste verhuisadviseur loopt de hele route met u mee".',
  html: v => sec(v, 'sectie--lucht', `${kop(v, 'v10__kop')}
<div class="v10__raster"><ol class="v10__plaat" role="list">${S.map(s => `<li class="v10__stap">${nr(s, 'v10__nr')}<span class="v10__obj" aria-hidden="true">${obj(s)}</span><div class="v10__tekst">${titel(s)}<p>${s.regel}</p></div>${uk(s, v)}</li>`).join('')}</ol>
<div class="v10__adviseur"><div class="v10__beeld" aria-hidden="true"><span class="v10__clip">${img('/img/contact-adviseur-uit.webp', 640, 954)}</span></div><div class="v10__slottekst">${slotB}${slotP}${cta()}</div></div></div>`) });

// 11 Gele schijven
V.push({ n: '11', naam: 'Gele schijven met pijlen', bron: 'De Reus: prijsopbouw (gekozen "Gele schijven")', uitleg: 'Geen kaarten: elk voorwerp staat op een gele schijf met dikte, met Diepblauwe pijlschijven ertussen. Een accolade leidt naar het slot, net als op /kosten/ #opbouw.',
  html: v => sec(v, 'sectie--wit', `${kop(v, 'kopgroep--midden')}
<ol class="v11__lijst" role="list">${S.map(s => `<li class="v11__stap"><span class="v11__podium" aria-hidden="true">${obj(s)}</span>${nr(s, 'v11__nr')}${titel(s)}<p>${s.regel}</p>${uk(s, v)}</li>`).join('')}</ol>
<svg class="v11__accolade" viewBox="0 0 1200 40" preserveAspectRatio="none" aria-hidden="true"><path d="M3 2 Q3 20 40 20 L560 20 Q600 20 600 38 Q600 20 640 20 L1160 20 Q1197 20 1197 2" fill="none" stroke="currentColor" stroke-width="3" vector-effect="non-scaling-stroke" stroke-linecap="round"/></svg>
<div class="v11__slot"><span class="v11__podium v11__podium--klein" aria-hidden="true">${huisRender()}</span><div>${slotB}${slotP}</div>${cta()}</div>`) });

// 12 Koningsblauwe plaat
V.push({ n: '12', naam: 'Koningsblauwe plaat met verhuizer', bron: 'Referentie A: .werkwijze__top + .stappen (omgekeerd)', uitleg: 'Referentie A-opzet in merkkleur: kop links, een echte verhuizer met steekwagen rechts die op de Koningsblauwe plaat rijdt. Witte tekst, gele cijfers met dikte, dunne witte lijnen.',
  html: v => sec(v, 'sectie--wit', `<div class="v12__top">${kop(v)}<figure class="v12__figuur" aria-hidden="true">${img('/img/verhuizer-steekwagen-uit.webp', 734, 1200)}</figure></div>
<div class="v12__plaat"><ol class="v12__lijst" role="list">${S.map(s => `<li class="v12__stap"><div class="v12__nrrij">${nr(s, 'v12__nr')}${obj(s)}</div>${titel(s)}<p>${s.regel}</p>${uk(s, v, 'uk--donker')}</li>`).join('')}</ol>
<div class="v12__slot">${huisFoto('v12__huis')}<div>${slotB}${slotP}</div>${cta()}</div></div>`) });

// 13 Rail naar de voordeur
V.push({ n: '13', naam: 'Rail met de voordeur als zesde station', bron: 'Huidige opzet, referentie A-hover', uitleg: 'Het huidige idee groter en afgemaakt: een dikke gele rail, grotere voorwerpen in de gele huizen, platen met een blauwe zijkant. De rail eindigt bij de echte voordeur. Hover = de gekozen groene 3D-zijkant van /contact/.',
  html: v => sec(v, 'sectie--mist', `${kop(v, 'kopgroep--midden')}
<div class="v13__rail"><ol class="v13__lijst" role="list">${S.map(s => `<li class="v13__stap"><span class="v13__ic" aria-hidden="true">${obj(s)}</span><div class="v13__kaart">${nr(s, 'v13__nr')}${titel(s)}<p>${s.regel}</p>${uk(s, v)}</div></li>`).join('')}</ol>
<div class="v13__stap v13__stap--eind"><span class="v13__ic v13__ic--foto" aria-hidden="true">${huisFoto('v13__huis')}</span><div class="v13__kaart">${slotB}${slotP}${cta()}</div></div></div>`) });

// 14 Planken
V.push({ n: '14', naam: 'Vijf planken onder elkaar', bron: 'Referentie A: .werkwijze__top + .tip-rijen', uitleg: 'Brede witte planken met dikte, één per stap: groot cijfer, voorwerp dat boven de plank uitkomt, tekst, en de uitklap rechts. De verhuisadviseur achter haar bureau zit boven de eerste plank; het slot is de gele laatste plank.',
  html: v => sec(v, 'sectie--mist', `<div class="v14__top">${kop(v)}<figure class="v14__figuur" aria-hidden="true">${img('/img/contact-klantenservice-uit.webp', 1200, 800)}</figure></div>
<ol class="v14__lijst" role="list">${S.map(s => `<li class="v14__plank">${nr(s, 'v14__nr')}<span class="v14__obj" aria-hidden="true">${obj(s)}</span><div class="v14__tekst">${titel(s)}<p>${s.regel}</p></div>${uk(s, v)}</li>`).join('')}</ol>
<div class="v14__plank v14__plank--slot">${huisFoto('v14__huis')}<div class="v14__tekst">${slotB}${slotP}</div>${cta()}</div>`) });

// 15 U en wij
V.push({ n: '15', naam: 'U en wij, zij aan zij', bron: 'Referentie A: .stappen-kolommen als tabel', uitleg: 'Het "wat u doet / wat wij doen" wordt het ontwerp zelf: per stap een kolom met het voorwerp, daaronder een witte rij "Wat u doet" en een Koningsblauwe rij "Wat wij doen". Geen uitklap meer nodig; het slot staat naast de kop.',
  html: v => sec(v, 'sectie--lucht', `<div class="v15__top">${kop(v)}<div class="v15__slot">${huisFoto('v15__huis')}<div>${slotB}${slotP}</div>${cta()}</div></div>
<div class="v15__matrix"><div class="v15__labels" aria-hidden="true"><span></span><span>Wat u doet</span><span>Wat wij doen</span></div><ol class="v15__lijst" role="list">${S.map(s => `<li class="v15__stap"><div class="v15__kopcel"><div class="v15__nrrij">${nr(s, 'v15__nr')}${obj(s)}</div>${titel(s)}<p>${s.regel}</p></div><dl class="v15__duo"><div class="v15__wie v15__wie--u"><dt class="vh">Wat u doet</dt><dd>${s.u}</dd></div><div class="v15__wie v15__wie--wij"><dt class="vh">Wat wij doen</dt><dd>${s.wij}</dd>${s.meer ? '<p class="v15__meer"><a href="/kosten/">Wat de prijs bepaalt</a></p>' : ''}</div></dl></li>`).join('')}</ol></div>`) });

const css = fs.readFileSync(path.join(__dirname, 'stappen-varianten.css'), 'utf8');

const nav = ['00', ...V.map(x => x.n)].map(n => `<a href="#v${n}">${n}</a>`).join('');
const kap = (n, naam, bron, uitleg) => `<div class="vkap" id="v${n}"><div class="wrap"><span class="vkap__nr">${n}</span><div><b>${naam}</b><small>${bron}</small><p>${uitleg}</p></div><span class="vkap__maat" data-maat></span></div></div>`;

const html = `<!doctype html>
<html lang="nl" class="js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Van aanvraag tot verhuisdag · 15 ontwerpen</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="/css/min/site.min.css?v=${hash('site')}">
<link rel="stylesheet" href="/css/min/tijdlijn.min.css?v=${hash('tijdlijn')}">
<style>
${css}
</style>
</head>
<body>
${sprite}
<nav class="vnav" aria-label="Ontwerpen"><div class="wrap"><b>/werkwijze/ #stappen · 15 ontwerpen</b><div class="vnav__links">${nav}</div></div></nav>
${kap('00', 'Nu live', 'Ter vergelijking', 'Het huidige blok op /werkwijze/, ongewijzigd.')}
${liveSectie.replace('id="stappen"', 'id="stappen-live"')}
${V.map(x => kap(x.n, x.naam, x.bron, x.uitleg) + '\n' + x.html(x.n)).join('\n')}
<div class="vkap vkap--eind"><div class="wrap"><p>Alle teksten zijn letterlijk die van de live pagina. Geen beweging behalve hover waar dat erbij staat. Kies een nummer.</p></div></div>
<script>
(function(){function meet(){document.querySelectorAll('[data-maat]').forEach(function(m){var s=m.closest('.vkap').nextElementSibling;if(!s)return;var h=Math.round(s.getBoundingClientRect().height);m.textContent='Blokhoogte '+h+' px';m.classList.toggle('is-hoog',h>760);});}
addEventListener('load',meet);addEventListener('resize',meet);document.addEventListener('toggle',meet,true);})();
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(REPO, '_ontwerpen/werkwijze-stappen-varianten.html'), html);
console.log('ok', html.length);
