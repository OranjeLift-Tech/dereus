// Ronde 2: 15 ontwerpen voor /werkwijze/ #stappen op basis van referentie A en referentie B
// node gen-stappen-2.cjs  ->  _ontwerpen/werkwijze-stappen-varianten-2.html
const fs = require('fs');
const path = require('path');
const REPO = path.resolve(__dirname, '../..');
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
// een echte medewerker per stap (uitsnedes met het echte logo), met eigen hoogte/verschuiving
const P = [
  { src: '/img/contact-klantenservice-uit.webp', w: 1200, h: 800, ph: 10.5, pb: 0, dx: 8 },
  { src: '/img/helpen-drie-uit.webp', w: 685, h: 591, ph: 9.6, pb: 0, dx: 0 },
  { src: '/img/aanvraag-foto-uit.webp', w: 720, h: 540, ph: 9.4, pb: 0, dx: -2 },
  { src: '/img/verhuizer-twee-dozen-uit.webp', w: 407, h: 1200, ph: 22, pb: -10.4, dx: 0 },
  { src: '/img/verhuizer-steekwagen-uit.webp', w: 734, h: 1200, ph: 22, pb: -10.4, dx: 6 },
];
// foto + passende uitsnede (zelfde verhouding) per stap, voor "mensen boven de lijst"
const F = [
  { foto: '/img/contact-klantenservice-foto.webp', uit: '/img/contact-klantenservice-uit.webp', w: 1200, h: 800, r: .3, pos: '50% 0%' },
  { foto: '/img/dienst-woningontruiming-v2.webp', uit: '/img/dienst-woningontruiming-v2-uit.webp', w: 720, h: 540, r: .3, pos: '50% 0%' },
  { foto: '/img/dienst-opslag-v2.webp', uit: '/img/dienst-opslag-v2-uit.webp', w: 720, h: 540, r: .4, pos: '50% 0%' },
  { foto: '/img/dienst-internationaal-v2b.webp', uit: '/img/dienst-internationaal-v2b-uit.webp', w: 720, h: 540, r: .27, pos: '50% 0%' },
  { foto: '/img/dienst-particulier-v2.webp', uit: '/img/dienst-particulier-v2-uit.webp', w: 720, h: 540, r: .42, pos: '50% 0%' },
];

const pijl = '<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-pijl"/></svg>';
const img = (src, w, h, cls = '', extra = '') => `<img class="${cls}" src="${src}" alt="" width="${w}" height="${h}" loading="lazy" decoding="async"${extra}>`;
const obj = (s, cls = '') => img(s.obj[0], s.obj[1], s.obj[2], `obj ${cls}`.trim(), ` style="--f:${s.obj[3]}"`);
const huisRender = (cls = '') => img('/img/kosten-3d/huis.webp', 425, 420, `obj obj--huis ${cls}`.trim(), ' style="--f:1"');
const huisFoto = (cls = '') => `<span class="huisfoto ${cls}" aria-hidden="true">${img('/img/nieuw-huis.webp', 400, 450)}</span>`;
const pers = (i, cls = '') => { const p = P[i]; return img(p.src, p.w, p.h, `pers ${cls}`.trim(), ` style="--ph:${p.ph}rem;--pb:${p.pb}rem;--dx:${p.dx}%"`); };
const pop = (i, cls = '') => { const f = F[i]; return `<span class="pop ${cls}" style="--r:${f.r};--pos:${f.pos}" aria-hidden="true">${img(f.foto, f.w, f.h, 'pop__foto')}${img(f.uit, f.w, f.h, 'pop__uit')}</span>`; };
const titel = (s, cls = '') => `<h3 class="${cls}"><span class="vh">Stap ${+s.nr}: </span>${s.titel}</h3>`;
const nr = (s, cls, tekst) => `<span class="${cls} nr" aria-hidden="true">${tekst || s.nr}</span>`;
const meer = s => s.meer ? `<p class="uk__meer"><a class="knop knop--link" href="/kosten/"><span>Wat de prijs bepaalt</span>${pijl}</a></p>` : '';
const duo = s => `<dl class="uk__duo"><div class="uk__wie uk__wie--u"><dt>Wat u doet</dt><dd>${s.u}</dd></div><div class="uk__wie uk__wie--wij"><dt>Wat wij doen</dt><dd>${s.wij}</dd></div></dl>`;
const uk = (s, v, cls = '') => `<details class="uk ${cls}" name="uk-${v}"><summary><span>Wat u doet en wat wij doen</span><span class="uk__plus" aria-hidden="true"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-plus"/></svg></span></summary><div class="uk__paneel">${duo(s)}${meer(s)}</div></details>`;
const label = '<p class="label">In vijf stappen</p>';
const h2 = (v, accent) => `<h2 id="kop-${v}">${accent ? 'Van aanvraag tot <span class="accent">verhuisdag</span>' : 'Van aanvraag tot verhuisdag'}</h2>`;
const intro = '<p class="intro">Elke verhuizing loopt bij ons via dezelfde vijf stappen. Zo weet u steeds waar u aan toe bent.</p>';
const kop = (v, cls = '', accent) => `<div class="kopgroep ${cls}">${label}${h2(v, accent)}${intro}</div>`;
const slotB = '<b class="slot__kop">Uw nieuwe huis</b>';
const slotP = '<p class="slot__tekst">Van uw eerste vraag tot de sleutel in uw nieuwe deur. Eén vaste verhuisadviseur loopt de hele route met u mee.</p>';
const cta = (cls = '') => `<a class="knop knop--cta ${cls}" href="/offerte/"><span>Offerte aanvragen</span>${pijl}</a>`;
const sec = (v, cls, inner) => `<section class="sectie ${cls} v w${v}" aria-labelledby="kop-${v}">\n<div class="wrap">\n${inner}\n</div>\n</section>`;
const ol = (cls, items) => `<ol class="${cls}" role="list">${S.map(items).join('')}</ol>`;

const V = [];
const add = (n, naam, bron, uitleg, html) => V.push({ n, naam, bron, uitleg, html });

add('01', 'Stapkaarten met een medewerker', 'Referentie B /onze-werkwijze/ #werkwijze (.sgdp-stap)',
  'Zoals de stappen op referentie B: elke kaart heeft bovenin een warm vlak waar een echte De Reus-medewerker boven de kaart uitkomt, een klein 3D-voorwerp linksonder en een "Stap 1"-pil. Daaronder titel, tekst en de uitklap.',
  v => sec(v, 'sectie--lucht', `${kop(v, 'w01__kop')}
${ol('w01__lijst', (s, i) => `<li class="w01__kaart"><div class="w01__beeld">${pers(i)}${obj(s)}${nr(s, 'w01__pil', 'Stap ' + (+s.nr))}</div><div class="w01__tekst">${titel(s)}<p>${s.regel}</p>${uk(s, v)}</div></li>`)}
<div class="w01__slot">${huisFoto('w01__huis')}<div>${slotB}${slotP}</div>${cta()}</div>`));

add('02', 'Oplopende kaarten met mensen erachter', 'Referentie B /onze-werkwijze/ en /contact/ (.sgm, .sgm__kaart, .sgm__band)',
  'De "Bel ons, videobel ons of kom langs"-opzet van referentie B, uitgebreid naar vijf: de kaarten lopen trapsgewijs op (zoals de trap die u mooi vond) en achter elke kaart staat een medewerker. Een gele band ligt achter de onderkant, het slot staat naast de kop.',
  v => sec(v, 'sectie--wit', `<div class="w02__top">${kop(v)}<div class="w02__slot">${huisFoto('w02__huis')}<div>${slotB}${slotP}${cta()}</div></div></div>
<div class="w02__veld"><span class="w02__band" aria-hidden="true"></span>${ol('w02__lijst', (s, i) => `<li class="w02__stap" style="--i:${i}"><span class="w02__mens" aria-hidden="true">${pers(i)}</span><div class="w02__kaart"><div class="w02__boven">${obj(s)}${nr(s, 'w02__pil', 'Stap ' + (+s.nr))}</div>${titel(s)}<p>${s.regel}</p>${uk(s, v)}</div></li>`)}</div>`));

add('03', 'De trap, met het team boven bij de deur', 'Referentie A /werkwijze/ (.werkwijze__top) + De Reus /kosten/ treden',
  'Ontwerp 03 uit ronde 1 (de trap) met referentie A-opzet erbij: de kop staat links, en het team met de verhuisdozen staat rechts bovenaan op de gele trede, bij de voordeur. De vijf treden en het cijfer op het blauwe stootbord blijven.',
  v => sec(v, 'sectie--wit', `<div class="w03__trap"><div class="w03__kop">${kop(v)}</div>${ol('w03__lijst', (s, i) => `<li class="w03__trede" style="--i:${i}"><div class="w03__kaart">${obj(s)}${titel(s)}<p>${s.regel}</p>${uk(s, v)}</div><div class="w03__stoot">${nr(s, 'w03__nr')}</div></li>`)}
<div class="w03__trede w03__trede--huis" style="--i:5"><figure class="w03__team" aria-hidden="true">${img('/img/team/team-hero-dozen-1100.webp', 1100, 1195)}</figure><div class="w03__kaart">${huisFoto('w03__huis')}${slotB}${slotP}${cta()}</div><div class="w03__stoot"></div></div></div>`));

add('04', 'Offerteblok met genummerde stappen', 'Referentie B _partials/offerteblok.html (.ob__paneel, .ob__stappen, .ob__nr)',
  'De opzet van het offerteblok van referentie B (dezelfde die /contact/ nu heeft): één witte kaart, links drie medewerkers boven een schuin Koningsblauw paneel met de kop en het slot, rechts de vijf stappen als genummerde lijst met een verbindingslijn.',
  v => sec(v, 'sectie--mist', `<div class="w04__kaart"><div class="w04__zij"><span class="w04__fig" aria-hidden="true">${img('/img/helpen-drie-uit.webp', 685, 591)}</span><div class="w04__paneel">${label}${h2(v, true)}${intro}<div class="w04__slot">${slotB}${slotP}${cta('w04__cta')}</div></div></div>
${ol('w04__lijst', s => `<li class="w04__stap">${nr(s, 'w04__nr', +s.nr)}<div class="w04__tekst">${titel(s)}<p>${s.regel}</p>${uk(s, v, 'uk--link')}</div>${obj(s)}</li>`)}</div>`));

add('05', 'Tijdlijn met foto-afdrukken', 'Referentie A homepage #historie (.hist5, .hist5__tl, .hist5__stapel)',
  'Zoals "Meer dan honderd jaar verhuizen vanuit Venlo" op referentie A-homepage: links een tijdlijn (groot cijfer, stip op de lijn, titel en tekst), rechts schuin gestapelde foto-afdrukken met een bijschrift, en de gele pil als knop.',
  v => sec(v, 'sectie--mist', `<div class="w05__raster"><div class="w05__links">${kop(v)}
${ol('w05__tl', s => `<li class="w05__rij">${nr(s, 'w05__nr')}<div class="w05__tekst">${titel(s)}<p>${s.regel}</p>${uk(s, v, 'uk--link')}</div></li>`)}
</div>
<div class="w05__rechts"><div class="w05__stapel" aria-hidden="true"><figure class="w05__afdruk w05__afdruk--1">${img('/img/contact-klantenservice-foto.webp', 1200, 800)}<figcaption>Offerte aanvragen</figcaption></figure><figure class="w05__afdruk w05__afdruk--2">${img('/img/dienst-particulier-v2.webp', 720, 540)}<figcaption>Verhuisdag</figcaption></figure><figure class="w05__afdruk w05__afdruk--3">${img('/img/nieuw-huis.webp', 400, 450)}<figcaption>Uw nieuwe huis</figcaption></figure></div><div class="w05__slot">${slotB}${slotP}${cta('w05__cta')}</div></div></div>`));

add('06', 'Diepblauwe kaart op de schuine band', 'Referentie A homepage #opslag (.opslag__kaart, .opslag__band) = referentie B homepage #opslag (.sgo__band)',
  'Het blok "Even geen plek?" van referentie A en "Onze voorraad" van referentie B: een schuine Koningsblauwe band met een gele streep, links een Diepblauwe kaart met de kop en de vijf stappen als lijst, rechts twee verhuizers die over de band heen staan.',
  v => sec(v, 'sectie--wit', `<span class="w06__band" aria-hidden="true"></span><div class="w06__raster"><div class="w06__kaart">${kop(v)}
${ol('w06__lijst', s => `<li class="w06__stap">${nr(s, 'w06__nr', +s.nr)}<div class="w06__tekst">${titel(s)}<p>${s.regel}</p>${uk(s, v, 'uk--link')}</div></li>`)}</div>
<div class="w06__rechts"><div class="w06__duo" aria-hidden="true">${img('/img/verhuizer-twee-dozen-uit.webp', 407, 1200, 'w06__een')}${img('/img/verhuizer-steekwagen-uit.webp', 734, 1200, 'w06__twee')}</div><div class="w06__slot">${huisFoto('w06__huis')}<div>${slotB}${slotP}${cta()}</div></div></div></div>`));

add('07', 'Venster met boog op Diepblauw', 'Referentie A homepage (.venster, .venster__boog, .venster__persoon)',
  'Het blok "Benieuwd naar de kosten?" van referentie A: een Diepblauwe band, links de kop en de stappen als tegels (twee kolommen, het slot als gele zesde tegel), rechts een boogvenster met een gele rand waarin drie medewerkers staan.',
  v => sec(v, 'sectie--diep', `<div class="w07__raster"><div class="w07__links">${kop(v)}
<div class="w07__tegels">${ol('w07__lijst', s => `<li class="w07__tegel">${obj(s)}<div class="w07__tekst">${nr(s, 'w07__nr')}${titel(s)}<p>${s.regel}</p>${uk(s, v, 'uk--donker')}</div></li>`)}<div class="w07__tegel w07__tegel--slot">${huisRender()}<div class="w07__tekst">${slotB}${slotP}${cta()}</div></div></div></div>
<figure class="w07__venster" aria-hidden="true"><span class="w07__boog"></span>${img('/img/helpen-drie-uit.webp', 685, 591, 'w07__mensen')}</figure></div>`));

add('08', 'Gekleurde tegels en een foto waar ze uitstappen', 'Referentie B homepage #waarom (.sgw-tegel, .sgw-tegel__3d, .sgw-foto__uit)',
  'Het "Waarom referentie B"-blok: tegels in vijf merkkleuren (Koningsblauw, Goudgeel, Crème, Lucht, Diepblauw), elk met een rond wit schijfje met het 3D-voorwerp; rechts een hoge foto waar de verhuizers bovenuit stappen. Het slot is de zesde tegel.',
  v => sec(v, 'sectie--wit', `${kop(v, 'kopgroep--midden')}
<div class="w08__raster">${ol('w08__lijst', s => `<li class="w08__tegel"><div class="w08__kopje"><span class="w08__schijf" aria-hidden="true">${obj(s)}</span>${nr(s, 'w08__nr')}${titel(s)}</div><p>${s.regel}</p>${uk(s, v)}</li>`)}
<div class="w08__tegel w08__tegel--slot"><div class="w08__kopje"><span class="w08__schijf" aria-hidden="true">${huisRender()}</span>${slotB}</div>${slotP}${cta()}</div>
<div class="w08__foto">${pop(4, 'w08__pop')}</div></div>`));

add('09', 'Fotokaarten, mensen boven de lijst', 'Referentie B homepage #sgd1-diensten (.sgd1-pop__raam, .sgd1-pop__boven, .sgd1-ico)',
  'Het dienstenblok van referentie B: per stap een echte De Reus-foto in een kader, de persoon op de foto steekt met het hoofd boven de lijst uit, het 3D-voorwerp staat op de hoek van de foto. Daaronder titel, tekst en de uitklap.',
  v => sec(v, 'sectie--lucht', `${kop(v, 'kopgroep--midden')}
${ol('w09__lijst', (s, i) => `<li class="w09__kaart">${pop(i, 'w09__pop')}${obj(s)}<div class="w09__tekst">${nr(s, 'w09__nr', 'Stap ' + (+s.nr))}${titel(s)}<p>${s.regel}</p>${uk(s, v)}</div></li>`)}
<div class="w09__slot">${huisFoto('w09__huis')}<div>${slotB}${slotP}</div>${cta()}</div>`));

add('10', 'Grote kaart met stappenrijen en foto', 'Referentie B homepage #prijzen (.sgpr__kaart, .sgpr-rij, .sgpr__pillen, .sgpr__badge)',
  'Het prijzenblok van referentie B: één grote witte kaart met links vijf omlijnde rijen (titel en tekst links, het grote cijfer rechts waar bij referentie B de prijs staat), drie vinkpillen met woorden uit de eigen tekst, de knop, en rechts een foto met een geel vak onderaan.',
  v => sec(v, 'sectie--mist', `<div class="w10__kaart"><div class="w10__body">${kop(v)}
<div class="w10__rijen">${ol('w10__lijst', s => `<li class="w10__rij"><div class="w10__tekst">${titel(s)}<p>${s.regel}</p>${uk(s, v, 'uk--link')}</div>${nr(s, 'w10__nr')}</li>`)}<div class="w10__rij w10__rij--slot"><div class="w10__tekst">${slotB}${slotP}</div></div></div>
<ul class="w10__pillen" role="list"><li>Binnen 24 uur</li><li>Vrijblijvend</li><li>Eén vaste verhuisadviseur</li></ul>${cta()}</div>
<div class="w10__media">${img('/img/verhuisdag-aankomst.webp', 1400, 1050, 'w10__foto')}<div class="w10__badge"><b>5 stappen</b><span>Van aanvraag tot verhuisdag</span></div></div></div>`));

add('11', 'Kop-paneel met team, kaarten met gele rand', 'Referentie B /contact/ (.sgct, .sgct-kaart, .sgct-kaart__icoon)',
  'De contactpagina van referentie B: bovenaan een afgerond paneel met een zacht verloop, de kop links en drie medewerkers rechts die boven het paneel uitkomen. Daaronder vijf kaarten met het 3D-voorwerp, een klein "STAP 1"-label en een gele onderrand.',
  v => sec(v, 'sectie--mist', `<div class="w11__paneel">${kop(v)}<div class="w11__slot">${slotB}${slotP}${cta()}</div><span class="w11__fig" aria-hidden="true">${img('/img/helpen-drie-uit.webp', 685, 591)}</span></div>
${ol('w11__lijst', s => `<li class="w11__kaart">${obj(s)}${nr(s, 'w11__nr', 'Stap ' + (+s.nr))}${titel(s)}<p>${s.regel}</p>${uk(s, v, 'uk--link')}</li>`)}`));

add('12', 'Missiekaarten, twee bij drie', 'Referentie B /over-ons-zonnepanelen-specialist/ (.sgoo-missie in "Onze doelen")',
  'Het blok "Onze visie / Onze missie" van referentie B op een Crème grond: links de kop, rechts zes kaarten in twee kolommen, elk met een groot 3D-voorwerp bovenin. De zesde kaart is Goudgeel, zoals de groene uitgelichte kaart bij referentie B, en is het slot.',
  v => sec(v, 'w12__grond', `<div class="w12__raster">${kop(v)}
<div class="w12__kaarten">${ol('w12__lijst', s => `<li class="w12__kaart">${obj(s)}${nr(s, 'w12__nr')}${titel(s)}<p>${s.regel}</p>${uk(s, v, 'uk--link')}</li>`)}<div class="w12__kaart w12__kaart--slot">${huisRender()}${slotB}${slotP}${cta()}</div></div></div>`));

add('13', 'Team op gestapelde panelen met een lijst', 'Referentie B /over-ons-zonnepanelen-specialist/ (.sgoo-team, .sgoo-stapel, .sgoo-feiten)',
  'Het blok "Gewoon een adres in Rotterdam-Nesselande": links het team met de verhuisdozen op twee gestapelde panelen (Koningsblauw achter, Lucht voor), de hoofden steken erboven uit. Rechts de vijf stappen als omlijnde rijen met het voorwerp, en het slot als gele rij.',
  v => sec(v, 'sectie--wit', `<div class="w13__raster"><div class="w13__links">${kop(v, 'w13__kop')}<div class="w13__stapel" aria-hidden="true"><span class="w13__achter"></span><span class="w13__voor"></span>${img('/img/team/team-hero-dozen-1100.webp', 1100, 1195, 'w13__team')}</div></div>
<div class="w13__rechts">${ol('w13__lijst', s => `<li class="w13__rij">${obj(s)}<div class="w13__tekst"><div class="w13__kopregel">${nr(s, 'w13__nr')}${titel(s)}</div><p>${s.regel}</p>${uk(s, v, 'uk--link')}</div></li>`)}
<div class="w13__rij w13__rij--slot">${huisFoto('w13__huis')}<div class="w13__tekst">${slotB}${slotP}</div>${cta()}</div></div></div>`));

add('14', 'Paneel met tegels waar het voorwerp uitkomt', 'Referentie B homepage #duurzaam (.sgz__kaart, .sgz__tegels, .sgz__3d)',
  'Het duurzaamheidsblok van referentie B: één afgerond Lucht-paneel, links de kop en het slot, rechts vijf kleine witte tegels waar het 3D-voorwerp boven de tegel uitkomt, met het cijfer groot in Koningsblauw zoals "1 boom" en "30 jaar".',
  v => sec(v, 'sectie--wit', `<div class="w14__paneel"><div class="w14__links">${kop(v)}<div class="w14__slot">${huisFoto('w14__huis')}<div>${slotB}${slotP}</div></div>${cta()}</div>
${ol('w14__lijst', s => `<li class="w14__tegel">${obj(s)}${nr(s, 'w14__nr')}${titel(s)}<p>${s.regel}</p>${uk(s, v, 'uk--link')}</li>`)}</div>`));

add('15', 'Gekleurde kop met foto, referentie A-plaat eronder', 'Referentie B /onze-werkwijze/ (.sgdp-hero) + referentie A /werkwijze/ (.stappen)',
  'Bovenaan de opzet van de referentie B-paginakop: een Koningsblauw vlak met de kop, een gele onderstreping onder "verhuisdag" en de knop, rechts een echte foto met een schuine naad. Daaronder, over de rand heen, de witte referentie A-plaat met vijf kolommen en grote cijfers.',
  v => sec(v, 'sectie--mist', `<div class="w15__kop"><div class="w15__vlak">${label}${h2(v, true)}${intro}${cta('w15__cta')}</div><div class="w15__foto">${img('/img/verhuisdag-aankomst.webp', 1400, 1050)}</div></div>
<div class="w15__plaat">${ol('w15__lijst', s => `<li class="w15__stap"><div class="w15__nrrij">${nr(s, 'w15__nr')}${obj(s)}</div>${titel(s)}<p>${s.regel}</p>${uk(s, v)}</li>`)}<div class="w15__slot">${huisFoto('w15__huis')}<div>${slotB}${slotP}</div></div></div>`));

const css = fs.readFileSync(path.join(__dirname, 'stappen-varianten.css'), 'utf8').split('/* ===== 01')[0]
  + fs.readFileSync(path.join(__dirname, 'stappen-varianten-2.css'), 'utf8');
const nav = ['00', ...V.map(x => x.n)].map(n => `<a href="#v${n}">${n}</a>`).join('');
const kap = (n, naam, bron, uitleg) => `<div class="vkap" id="v${n}"><div class="wrap"><span class="vkap__nr">${n}</span><div><b>${naam}</b><small>${bron}</small><p>${uitleg}</p></div><span class="vkap__maat" data-maat></span></div></div>`;

const html = `<!doctype html>
<html lang="nl" class="js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Van aanvraag tot verhuisdag · ronde 2 · referentie A + referentie B</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="/css/min/site.min.css?v=${hash('site')}">
<link rel="stylesheet" href="/css/min/tijdlijn.min.css?v=${hash('tijdlijn')}">
<style>
${css}
</style>
</head>
<body>
${sprite}
<nav class="vnav" aria-label="Ontwerpen"><div class="wrap"><b>/werkwijze/ #stappen · ronde 2 · referentie A + referentie B</b><div class="vnav__links">${nav}</div></div></nav>
${kap('00', 'Nu live', 'Ter vergelijking', 'Het huidige blok op /werkwijze/, ongewijzigd.')}
${liveSectie.replace('id="stappen"', 'id="stappen-live"')}
${V.map(x => kap(x.n, x.naam, x.bron, x.uitleg) + '\n' + x.html(x.n)).join('\n')}
<div class="vkap vkap--eind"><div class="wrap"><p>Alle teksten zijn letterlijk die van de live pagina (alleen in 10 staan drie pillen met woorden uit diezelfde tekst). Elke bron hierboven bestaat echt in de code van referentie A of referentie B. Kies een nummer.</p></div></div>
<script>
(function(){function meet(){document.querySelectorAll('[data-maat]').forEach(function(m){var s=m.closest('.vkap').nextElementSibling;if(!s)return;var h=Math.round(s.getBoundingClientRect().height);m.textContent='Blokhoogte '+h+' px';m.classList.toggle('is-hoog',h>760);});}
addEventListener('load',meet);addEventListener('resize',meet);document.addEventListener('toggle',meet,true);})();
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(REPO, '_ontwerpen/werkwijze-stappen-varianten-2.html'), html);
console.log('ok', html.length);
