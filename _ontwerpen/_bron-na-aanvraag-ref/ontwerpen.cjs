// De 15 ontwerpen. Elk ontwerp krijgt zijn nummer v en geeft de sectie terug; klassen .nNN in var.css.
module.exports = function (h) {
  const { add, sec, wrap, kop, bel, wa, google, gDelen, status, acties, voet, stappen, nr, nr2, ic, img, vrouw, vrouwZacht, obj, merk, merkNeg, STAPPEN } = h;
  const lijst = (cls, li) => `<ol class="${cls}" role="list">${STAPPEN.map(li).join('')}</ol>`;
  // de Google-score als ronde schijf (referentie A .ev-score, referentie B .sgr__boog)
  const score = (cls, o = {}) => {
    const g = gDelen();
    const ring = o.ring ? `<svg class="${cls}-ring" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="46" pathLength="100"/></svg>` : '';
    return `<a class="${cls}" href="${g.href}" rel="noopener" target="_blank">${ring}<b class="${cls}-cijfer">${g.cijfer}</b><span class="${cls}-tekst">${g.sterren}<span>${g.rest}</span></span>${g.vh}</a>`;
  };

  // ================= referentie A =================
  add('01', 'De medewerker in een witte boog op Koningsblauw', 'Referentie A, blok "Na uw aanvraag" (.venster, .venster__in, .venster__tekst, .venster__fig, .venster__boog, .venster__boog::after, .venster__persoon, .venster__mark)',
    'Het blok waarmee referentie A zelf uitlegt wat er na de aanvraag gebeurt: een gekleurde band, links de tekst, rechts een lichte boog met een dunne binnenlijn waarin de persoon staat, onderaan op de rand van de band. Een groot beeldmerk zacht in de hoek. Hier Koningsblauw (de footer eronder is Diepblauw), de boog wit met een Goudgele binnenlijn, zij aan haar bureau op de onderrand.',
    v => sec(v, 'blauw', `${merkNeg('n01__mark')}
${wrap(`<div class="n01__in"><div class="n01__tekst op-donker">${kop(v)}${stappen('n01__stappen')}${voet('n01__voet')}</div>
<div class="n01__fig" aria-hidden="true"><span class="n01__boog"></span>${vrouw('n01__persoon')}</div></div>`)}`, 'n01--band'));

  add('02', 'Schuine band, zij zit erop', 'Referentie A homepage #opslag (.opslag__band, .opslag__mark, .opslag__lijn, .opslag__in, .opslag__kaart, .opslag__fig, .opslag__persoon met de schuine clip-path)',
    'Het opslagblok van referentie A: onderin een band die 5 graden oploopt, met een lijn eronder. Links een donkere kaart die over de band valt, rechts staat de persoon op de lijn; de onderkant is net zo schuin afgesneden als de band. Hier een Koningsblauwe band met een Goudgele lijn, de stappen in een Diepblauwe kaart en de medewerker met haar bureau op de lijn.',
    v => sec(v, 'wit', `<span class="n02__band" aria-hidden="true">${merkNeg('n02__mark')}</span><span class="n02__lijn" aria-hidden="true"></span>
${wrap(`<div class="n02__in"><div class="n02__kaart op-donker">${kop(v)}${stappen('n02__stappen')}${voet('n02__voet')}</div>
<div class="n02__fig">${vrouw('n02__persoon')}</div></div>`)}`));

  add('03', 'Kop naast de medewerker, drie stappen op één plaat', 'Referentie A /werkwijze/ #aanspreekpunt en homepage #werkwijze (.werkwijze__top, .werkwijze__wagen, .wkw-staand, .stappen, .stap, .stap__nr, .wa-rij)',
    'De stappenopzet van referentie A: boven een raster van twee kolommen dat onderaan uitlijnt, links de kop, rechts de uitgeknipte persoon. Daaronder één witte plaat met de stappen in kolommen, dunne lijnen ertussen en grote cijfers (01, 02, 03) in plaats van schijven. De medewerker zit achter de plaat, zodat haar bureau op de rand lijkt te staan. Onderaan de knoppenrij in het midden.',
    v => sec(v, 'lucht', wrap(`<div class="n03__top"><div class="n03__kop">${kop(v)}${bel('n03__bel')}</div><figure class="n03__fig" aria-hidden="true">${vrouwZacht()}</figure></div>
${lijst('n03__stappen', (s, i) => `<li class="n03__stap"><span class="n03__nr" aria-hidden="true">${nr2(i)}</span><h3>${s.titel}</h3><p>${s.tekst}</p></li>`)}
${acties('n03__rij')}`)));

  add('04', 'Schijven op een stippellijn, donkere belkaart met score', 'Referentie A /erkende-verhuizer/ (.ev-stappen, .ev-stappen::before, .ev-stappen li::before, .ev-cta, .ev-score__cijfer)',
    'Drie onderdelen van dezelfde pagina van referentie A: de stappen naast elkaar met een genummerde schijf op een stippellijn (de schijf krijgt een witte ring, zodat de lijn erachter wegvalt), een donkere kaart met tekst links en een beeld rechts, en de score als ronde schijf met een dubbele ring. Hier is de kaart Diepblauw met de belregel groot, en zit de medewerker rechts met haar hoofd boven de kaart uit.',
    v => sec(v, 'wit', wrap(`<div class="n04__kop">${kop(v)}${score('n04__score')}</div>
${lijst('n04__stappen', (s, i) => `<li class="n04__stap"><span class="n04__nr" aria-hidden="true">${nr2(i)}</span><h3>${s.titel}</h3><p>${s.tekst}</p></li>`)}
<div class="n04__cta"><div class="n04__cta-tekst op-donker">${bel('n04__bel')}<div class="n04__knoppen">${wa()}${status('n04__status')}</div></div><div class="n04__cta-beeld" aria-hidden="true">${vrouw('n04__vrouw')}</div></div>`)));

  add('05', 'Lichte beeldhelft, blauw paneel, witte Google-pil', 'Referentie A /contact/ leadblock (.leadblock__card, .leadblock__media, .leadblock__panel, .leadblock__panel::before, .lead-google, .lead-google__stars)',
    'Het afsluitende blok van referentie A op /contact/: één kaart met ronde hoeken, links het beeld, rechts een paneel met een schuin kleurverloop en een zachte lichtvlek rechtsboven, en een witte pil met de Google-sterren in de hoek van het beeld. Hier een lichtblauwe beeldhelft met het beeldmerk zacht erachter en de medewerker aan haar bureau, en een Koningsblauw paneel met de stappen.',
    v => sec(v, 'lucht', wrap(`<div class="n05__card"><div class="n05__media">${merk('n05__merk')}${vrouw('n05__vrouw')}${google('n05__google')}</div>
<div class="n05__panel op-donker">${kop(v)}${stappen('n05__stappen')}${bel('n05__bel')}<div class="n05__knoppen">${wa()}${status('n05__status')}</div></div></div>`)));

  add('06', 'Paneel met gele rand, foto met een vlak erachter', 'Referentie A #wonen en /werkwijze/ (.blok--paneel .blok__tekst, .blok--vlak .blok__foto, .blok--vlak .blok__foto::before)',
    'Twee regels van referentie A samen: het tekstpaneel (lichte kleur, dikke gekleurde rand links, grote ronding) en de foto met een gekleurd vlak dat rechtsonder achter de foto uitsteekt. Hier een lichtblauw paneel met een Goudgele rand, en een Goudgeel beeldvlak met een Koningsblauw vlak erachter. Het hoofd van de medewerker komt boven het gele vlak uit.',
    v => sec(v, 'wit', wrap(`<div class="n06__blok"><div class="n06__tekst">${kop(v)}${stappen('n06__stappen')}${voet('n06__voet')}</div>
<figure class="n06__foto" aria-hidden="true"><span class="n06__raam"></span>${vrouw('n06__vrouw')}</figure></div>`)));

  // ================= referentie B =================
  add('07', 'Witte kaart, zij boven de kaart uit, blauw paneel met een knik', 'Referentie B offerteblok (.ob__kaart, .ob__kaart::before, .ob__zij, .ob__beeld, .ob__fig, .ob__paneel::before met clip-path, .ob__kop span, .ob__stappen, .ob__nr)',
    'Het offerteblok dat referentie B onder elke pagina heeft: een witte kaart met een dunne gekleurde rand, links een figuur die 44 px boven de kaart uitsteekt, daaronder een gekleurd paneel waarvan de bovenrand schuin oploopt en over het onderlichaam valt. Rechts staan de stappen met schijven en een verbindingslijn. Hier zit de medewerker aan haar bureau in de figuurplek, het paneel is Koningsblauw met de belregel, WhatsApp en Google.',
    v => sec(v, 'wit', wrap(`<div class="n07__kaart"><div class="n07__zij"><div class="n07__beeld" aria-hidden="true">${vrouw('n07__fig')}</div>
<div class="n07__paneel op-donker">${bel('n07__bel')}${acties('n07__acties')}</div></div>
<div class="n07__rechts">${kop(v, 'n07__kop', { accent: true })}${stappen('n07__stappen')}</div></div>`)));

  add('08', 'Diepblauwe kaart, zij komt erboven uit, gele badge', 'Referentie B voorraadblok (.sgdp-voorraad__kaart, .sgdp-voorraad__media, .sgdp-figuur, .sgdp-badge, .sgdp-badge__ic)',
    'Het voorraadblok van referentie B: een donkere kaart met links de tekst en rechts een uitgeknipte figuur die op de onderrand staat en met hoofd en schouders boven de kaart uitkomt, met een felle badge links onder. Hier Diepblauw (haar Koningsblauwe shirt blijft zo los van de kaart), de stappen met gele schijven en de Google-score als Goudgele badge.',
    v => sec(v, 'wit', wrap(`<div class="n08__kaart"><div class="n08__body op-donker">${kop(v)}${stappen('n08__stappen')}<div class="n08__bel">${bel()}${wa()}</div></div>
<div class="n08__media">${vrouw('n08__figuur')}${google('n08__badge')}</div></div>`)));

  add('09', 'Band met V-rand, alles komt uit de kaart', 'Referentie B homepage #diensten (.sgd1::before, .sgd1::after, .sgd1-grid, .sgd1-kaart, .sgd1-pop, .sgd1-pop__boven, .sgd1-ico, .sgd1-kaart:hover)',
    'Het dienstenblok van referentie B: een lichte band met een V aan de bovenkant en een schuine punt onderaan, witte kaarten met een kleine hoek, bovenin een beeldvak waar het onderwerp bovenuit steekt en een ronde schijf op de onderrand van het vak. De eerste kaart is de medewerker (breder), de drie andere zijn de stappen met de echte voorwerpen: telefoon, dozen en de envelop met de offerte.',
    v => sec(v, 'wit', `<div class="n09__band" aria-hidden="true"></div>
${wrap(`<div class="n09__kop">${kop(v)}</div>
<div class="n09__rij"><div class="n09__kaart n09__kaart--mens"><div class="n09__beeld" aria-hidden="true"><span class="n09__raam"></span>${vrouw('n09__pop')}</div><div class="n09__tekst">${bel()}${acties()}</div></div>
${lijst('n09__lijst', (s, i) => `<li class="n09__kaart"><div class="n09__beeld"><span class="n09__raam"></span>${obj(i, 'n09__pop')}<span class="n09__ico" aria-hidden="true">${nr(i)}</span></div><div class="n09__tekst"><h3>${s.titel}</h3><p>${s.tekst}</p></div></li>`)}</div>`)}`));

  add('10', 'Bladvormig paneel met de medewerker, drie kaarten eronder', 'Referentie B /contact/ (.sgct-blad, .sgct-blad__foto, .sgct__kaarten, .sgct-kaart, .sgct-kaart:hover)',
    'Het contactblok van referentie B: een paneel met twee kleine en twee grote hoeken (een bladvorm), een zacht verloop, en de persoon in een smalle kolom rechts die met hoofd en schouders boven het paneel uitkomt. Daaronder kaarten met een dikke gekleurde onderrand die bij hover iets optillen. Hier van Lucht naar zacht Goudgeel, de kaarten met Goudgele onderrand en het echte voorwerp per stap.',
    v => sec(v, 'wit', wrap(`<div class="n10__blad"><div class="n10__tekst">${kop(v)}${bel()}${acties()}</div><div class="n10__foto" aria-hidden="true">${vrouw()}</div></div>
${lijst('n10__kaarten', (s, i) => `<li class="n10__kaart">${obj(i, 'n10__obj')}<div><span class="n10__nr" aria-hidden="true">${nr(i)}</span><h3>${s.titel}</h3><p>${s.tekst}</p></div></li>`)}`)));

  add('11', 'Zij op twee platen, score in een ronde schijf', 'Referentie B #reviews (.sgr__score, .sgr__stapel::before/::after, .sgr__persoon, .sgr__boog, .sgr__ring, .sgr__gemiddeld-vol), zelf geport uit referentie C .b-stemmen',
    'Het podium uit het reviewblok van referentie B: twee platen achter elkaar (achter een verloop, iets naar rechtsboven geschoven, voor een lichte), de persoon staat op de voorste plaat en komt erboven uit, en vooraan een witte ronde schijf met een ring en de sterren. Bij hover schuift de achterste plaat verder en groeit de persoon een klein beetje. Links de kop en de stappen.',
    v => sec(v, 'wit', wrap(`<div class="n11__in"><div class="n11__tekst">${kop(v)}${stappen('n11__stappen')}<div class="n11__bel">${bel()}${wa()}</div></div>
<div class="n11__podium"><span class="n11__stapel" aria-hidden="true"></span>${vrouw('n11__persoon')}${score('n11__boog', { ring: true })}</div></div>`)));

  add('12', 'Goudgeel paneel met gekantelde afdrukken', 'Referentie B #toennu (.sgt, .sgt__paneel, .sgt__fotos, .sgt__kaart, .sgt__uit met clip-path, .sgt__pil)',
    'Het toen-en-nu-blok van referentie B: een zongeel paneel met grote ronding, links de tekst, rechts twee foto\'s als witte afdrukken die schuin over elkaar liggen, en een stuk van het onderwerp dat boven de lijst uitsteekt. Hier de envelop met de offerte achteraan en de medewerker vooraan, met haar hoofd boven de witte lijst; een donkere pil toont of we nu bereikbaar zijn.',
    v => sec(v, 'wit', wrap(`<div class="n12__paneel"><div class="n12__tekst">${kop(v)}${stappen('n12__stappen')}${voet('n12__voet')}</div>
<div class="n12__fotos"><figure class="n12__kaart n12__kaart--achter" aria-hidden="true"><span class="n12__raam"></span>${obj(2, 'n12__env')}</figure><figure class="n12__kaart n12__kaart--voor"><span class="n12__raam" aria-hidden="true"></span>${vrouw('n12__vrouw')}${status('n12__pil')}</figure></div></div>`)));

  // ================= referentie C =================
  add('13', 'Donkere kolom met podium en gele streep', 'Referentie C offerteblok (.b-offerte__kaart, .b-offerte__zij, .b-offerte__podium, .b-offerte__podium::after, .b-offerte__verhuizer, .b-offerte__stappen li::before)',
    'Het offerteblok van referentie C: een witte kaart, links een donkere kolom met bovenin een podium waar de persoon op staat, met een schuine felle streep onder de voeten, daaronder de belknop; rechts de kop en de stappen met grote cijfers in de accentkleur in plaats van schijven. Hier Diepblauw met een Goudgele streep; zij komt met haar hoofd boven de kaart uit en groeit iets onder de muis.',
    v => sec(v, 'wit', wrap(`<div class="n13__kaart"><div class="n13__zij"><div class="n13__podium" aria-hidden="true">${vrouw('n13__verhuizer')}</div><div class="n13__zijtekst op-donker">${bel()}${acties()}</div></div>
<div class="n13__rechts">${kop(v, 'n13__kop', { accent: true })}${stappen('n13__stappen', { voor: () => '' })}</div></div>`)));

  add('14', 'Beeld met een verschoven plaat en een schrijfblok erover', 'Referentie C /werkwijze/ #kanaal (.b-kanaal__beeld::before, .b-kanaal__blok, .b-kanaal__blok::before, .b-kanaal__wegen, .b-kanaal__weg--bel, .b-kanaal__tel)',
    'Het kanaalblok van referentie C: een beeld met een lichte plaat die linksboven verschoven achter het beeld ligt, en een schrijfblok met lijntjes, een kantlijn en ringgaatjes dat over de linkeronderhoek van het beeld valt. Ernaast de manieren om contact op te nemen, de telefoon met een donkere schijf en het nummer groot. Op het schrijfblok staan de drie stappen, op de lijnen.',
    v => sec(v, 'wit', wrap(`<div class="n14__in"><div class="n14__kop">${kop(v)}<ul class="n14__wegen" role="list"><li class="n14__weg n14__weg--bel">${ic('telefoon')}<p>${h.BEL}</p></li><li class="n14__weg">${wa()}${google()}</li></ul></div>
<div class="n14__beeld"><div class="n14__foto" aria-hidden="true">${vrouw('n14__vrouw')}</div><div class="n14__blok">${stappen('n14__stappen', { voor: i => `<span class="n14__nr" aria-hidden="true">${nr(i)}.</span>` })}</div></div></div>`)));

  add('15', 'Gele band met schuine onderkant, witte kaart hangt eronder', 'Referentie C /contact/ (.b-livrei, .b-livrei__foto met clip-path en --hoek, .b-livrei__paneel in grid-column 2 / grid-row 2 tot 4)',
    'Het eerste blok van referentie C op /contact/: een beeld van rand tot rand met een schuine onderkant, en een wit paneel in de rechterkolom dat over het beeld valt en eronder uithangt. Hier is het beeld een Goudgele band met de medewerker groot aan haar bureau, afgesneden door de schuine rand, en staat alles van het blok in het witte paneel.',
    v => sec(v, 'wit', `<div class="n15__in"><div class="n15__foto" aria-hidden="true"><div class="n15__binnen">${vrouwZacht('n15__vrouw')}</div></div>
<div class="n15__paneel">${kop(v)}${stappen('n15__stappen')}${voet('n15__voet')}</div></div>`));
};
