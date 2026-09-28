// Maakt _ontwerpen/verhuisdag-referentie-varianten.html: 15 ontwerpen voor /werkwijze/ #verhuisdag,
// elk gebouwd op de code van een echt blok van brockenverhuizingen.nl, referentie A of referentie B.
//   node _ontwerpen/_bron-verhuisdag-ref/gen.cjs
// Leest var.css hiernaast, het sprite-blok, de css-hashes en de live sectie uit werkwijze/index.html.
const fs = require('fs'), path = require('path');
const REPO = path.join(__dirname, '..', '..');
const UIT = path.join(REPO, '_ontwerpen/verhuisdag-referentie-varianten.html');
const css = fs.readFileSync(path.join(__dirname, 'var.css'), 'utf8');
const werkwijze = fs.readFileSync(path.join(REPO, 'werkwijze/index.html'), 'utf8');
const sprite = werkwijze.match(/<svg class="sprite"[\s\S]*?<\/svg>(?=\s*<header)/)[0];
const siteCss = werkwijze.match(/href="(\/css\/min\/site\.min\.css\?v=[0-9a-f]+)"/)[1];
const vdCss = werkwijze.match(/href="(\/css\/min\/verhuisdag\.min\.css\?v=[0-9a-f]+)"/)[1];
const live = werkwijze.match(/<section class="b-verhuisdag[\s\S]*?<\/section>/)[0];

// ---- letterlijke tekst van /werkwijze/ #verhuisdag ----
const T = { label: 'De verhuisdag', kop: 'Op de verhuisdag', intro: 'Op de verhuisdag doen wij het zware werk. U houdt het overzicht.' };
// per moment: foto + uitsnede (zelfde maat en plek), waar de mensen staan (deel van het beeld) en een 3D-voorwerp
const M = [
  { t: 'Aankomst', p: 'Onze verhuizers staan op het afgesproken tijdstip voor de deur. U laat zien wat er mee moet.',
    foto: ['dienst-particulier.webp', 720, 540], uit: ['verhuisdag-uit/aankomst.webp', 1080, 810],
    ar: 4 / 3, top: 0.338, bot: 0.954, cx: 0.51, pos: '50% 62%', obj: ['kosten-3d/huis.webp', 425, 420] },
  { t: 'Inladen', p: 'Wij beschermen uw spullen en dragen alles zorgvuldig naar buiten. Moet er iets uit elkaar, dan doen wij dat als het zo is afgesproken.',
    foto: ['dienst-internationaal.webp', 720, 540], uit: ['verhuisdag-uit/inladen.webp', 1080, 810],
    ar: 4 / 3, top: 0.209, bot: 0.85, cx: 0.56, pos: '60% 50%', obj: ['kosten-3d/dozen.webp', 437, 420] },
  { t: 'Uitladen en opbouwen', p: 'In uw nieuwe huis zetten wij alles op de plek die u aanwijst. Is montage afgesproken, dan bouwen wij uw meubels weer op.',
    foto: ['stap-5-bank-voordeur.webp', 1120, 760], uit: ['verhuisdag-uit/uitladen.webp', 1120, 760],
    ar: 1120 / 760, top: 0.134, bot: 0.993, cx: 0.36, pos: '32% 50%', obj: ['kosten-3d/boor.webp', 509, 420] },
];
// het slot, woord voor woord; het begin van elke afspraak vet (zoals live)
const A = [
  { b: 'Betalen doet u op de verhuisdag,', r: 'tenzij we samen iets anders hebben afgesproken.', obj: ['kosten-kalender/blok.webp', 449, 720] },
  { b: 'Ziet u schade aan uw spullen?', r: 'Meld het dan meteen op de dag zelf aan onze verhuizers, dan bekijken en noteren we het direct samen.', obj: ['contact-3d/schild.webp', 251, 320] },
];
const VW = 'Zo staat het ook in onze <a href="/algemene-voorwaarden/">algemene voorwaarden</a>.';
const afspraak = a => `<b>${a.b}</b> ${a.r}`;
const SLOT = `${afspraak(A[0])} ${afspraak(A[1])} ${VW}`;

const ic = n => `<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-${n}"/></svg>`;
const img = ([src, w, h], k = '', extra = '') => `<img${k ? ` class="${k}"` : ''} src="/img/${src}" alt="" width="${w}" height="${h}"${extra}>`;
const foto = (m, k = '') => img(m.foto, k, ` style="object-position:${m.pos}"`);
const nr = i => String(i + 1).padStart(2, '0');
const r4 = n => +n.toFixed(4);
// uitsnede als losse figuur: alleen de mensen, van kruin tot voeten precies de hoogte van het vak (zie .fig in var.css)
const fig = (m, k) => `<span class="fig ${k}" style="--top:${m.top};--bot:${m.bot};--cx:${m.cx};--ar:${r4(m.ar)}">${img(m.uit)}</span>`;
// foto-pop zoals .sgd1-pop (Referentie B): foto op het kader geknipt, uitsnede alleen in een strook erboven
const pop = (m, k = '', p = '') => `<div class="pop ${k}" style="--d0:${m.top};--mid:${m.cx};--ar:${r4(m.ar)}${p ? `;--p:${p}` : ''}">
          <span class="pop__raam">${img(m.foto, 'pop__foto')}</span>
          <span class="pop__boven" aria-hidden="true">${img(m.uit)}</span>`;
const kopB = (extra = '') => `<p class="label lab-b">${T.label}</p><h2>Op de <em>verhuisdag</em></h2>${extra}`;
const kopK = () => `<p class="label lab-k">${T.label}</p><h2>${T.kop}</h2><p class="intro">${T.intro}</p>`;
const kopS = (lab = '') => `<p class="label lab-s${lab}">${T.label}</p><h2>${T.kop}</h2>`;

const V = [];
const variant = (naam, site, bron, uitleg, html) => V.push({ naam, site, bron, uitleg, html });

/* ======================= brockenverhuizingen.nl ======================= */

variant('Mozaïek met noot', 'brockenverhuizingen.nl', '/werkwijze/ “De verhuisdag, zoals afgesproken” · .b-dag, .b-dag__kop, .b-dag__mozaiek, .b-dag__feiten (dag.min.css)',
  'Het verhuisdagblok van Brocken zelf. Kop links met een deel in Goudgeel, de intro als noot rechts. Daaronder het fotomozaïek op 12 kolommen (5/3/4) met een donkere onderschrift-balk per foto, en de afspraken als feitenrij met een bovenlijn en een rond icoon.',
  `<section class="sectie sectie--blauw vv v01"><div class="wrap">
      <div class="b-dag__kop"><div class="b-kopgroep">${kopB()}</div><p class="b-dag__noot">${T.intro}</p></div>
      <div class="b-dag__mozaiek">${M.map((m, i) => `
        <figure class="b-dag__tegel b-dag__tegel--${'abc'[i]}">${foto(m)}<figcaption><h3>${m.t}</h3><p>${m.p}</p></figcaption></figure>`).join('')}
      </div>
      <ul class="b-dag__feiten">${A.map(a => `
        <li class="b-dag__feit"><span class="b-dag__ic">${img(a.obj)}</span><div><p><b class="kopregel">${a.b}</b> ${a.r}</p></div></li>`).join('')}
        <li class="b-dag__feit"><span class="b-dag__ic b-dag__ic--lijn">${ic('check')}</span><div><p>${VW}</p></div></li>
      </ul>
    </div></section>`);

variant('Foto met notitieblok', 'brockenverhuizingen.nl', '/werkwijze/ “Kennismaken zoals het u uitkomt” · .b-kanaal, .b-kanaal__adviseur, .b-kanaal__beeld, .b-kanaal__blok, .b-kanaal__wegen (kanaal.min.css)',
  'Kop links, de foto loopt rechts door tot de schermrand met een plaat erachter. Over de onderrand ligt het gelinieerde notitieblok (ringetjes, kantlijn) met de twee afspraken: “dan noteren we het direct samen”. De verhuizers staan uitgesneden op de lijn van de drie momenten eronder.',
  `<section class="sectie sectie--blauw vv v02"><div class="wrap b-kanaal__in">
      <div class="b-kopgroep">${kopB(`<p class="intro">${T.intro}</p>`)}</div>
      ${img(['verhuisdag-verhuizers.webp', 709, 787], 'b-kanaal__adviseur')}
      <figure class="b-kanaal__beeld">
        <div class="b-kanaal__foto">${foto(M[1])}</div>
        <figcaption class="b-kanaal__blok"><ol class="b-kanaal__agenda">${A.map(a => `<li>${afspraak(a)}</li>`).join('')}</ol><p class="b-kanaal__voet">${VW}</p></figcaption>
      </figure>
      <ul class="b-kanaal__wegen">${M.map(m => `
        <li class="b-kanaal__weg"><span class="b-kanaal__ic">${img(m.obj)}</span><div><h3>${m.t}</h3><p>${m.p}</p></div></li>`).join('')}
      </ul>
    </div></section>`);

variant('Tijdlijn met platen', 'brockenverhuizingen.nl', 'home “Van paard en wagen in 1923 tot uw verhuizing van nu” · .b-historie__tl, .b-historie__plaat, .b-historie__jaar, .b-historie__voet (historie.min.css)',
  'De dag als tijdlijn: drie licht gedraaide fotoplaten, een lijn die van zacht naar Goudgeel loopt en een nummer met stip onder elke plaat (de laatste stip geel, zoals “Nu” bij Brocken). De afspraken staan in de voet onder een dunne lijn.',
  `<section class="sectie sectie--blauw vv v03"><div class="wrap">
      <div class="b-kopgroep">${kopB(`<p class="intro">${T.intro}</p>`)}</div>
      <ol class="b-historie__tl">${M.map((m, i) => `
        <li class="b-historie__stap${i === 2 ? ' b-historie__stap--nu' : ''}"><figure class="b-historie__fig"><div class="b-historie__plaat">${foto(m)}</div><figcaption class="b-historie__jaar">${nr(i)}</figcaption></figure><h3>${m.t}</h3><p>${m.p}</p></li>`).join('')}
      </ol>
      <div class="b-historie__voet"><p class="b-historie__cijfers">${afspraak(A[0])} ${afspraak(A[1])}</p><p class="b-historie__link">${ic('check')}<span>${VW}</span></p></div>
    </div></section>`);

variant('Kaarten aan de band', 'brockenverhuizingen.nl', 'home “Waarom kiezen voor Brocken?” · .b-belofte__baan, .b-belofte__band, .b-belofte__kaart, .b-belofte__haak (belofte.min.css)',
  'Een Goudgele band over de volle breedte; aan haakjes hangen vijf witte kaarten, elk een tikje scheef: de drie momenten met hun foto en de twee afspraken met hun 3D-voorwerp. De verwijzing naar de voorwaarden staat gecentreerd eronder.',
  `<section class="sectie sectie--blauw vv v04">
      <div class="wrap"><div class="b-kopgroep b-kopgroep--midden">${kopB(`<p class="intro">${T.intro}</p>`)}</div></div>
      <div class="b-belofte__baan"><div class="b-belofte__band" aria-hidden="true"></div><div class="wrap">
        <ul class="b-belofte__lijst">${M.map(m => `
          <li class="b-belofte__kaart"><span class="b-belofte__haak" aria-hidden="true"></span><span class="b-belofte__foto">${foto(m)}</span><h3>${m.t}</h3><p>${m.p}</p></li>`).join('')}${A.map(a => `
          <li class="b-belofte__kaart"><span class="b-belofte__haak" aria-hidden="true"></span>${img(a.obj, 'b-belofte__ico')}<p><b class="kopregel">${a.b}</b> ${a.r}</p></li>`).join('')}
        </ul></div></div>
      <div class="wrap"><p class="b-belofte__knoppen">${ic('check')}<span>${VW}</span></p></div>
    </section>`);

variant('Foto’s met kaart erover', 'brockenverhuizingen.nl', '/diensten/particulier-verhuizingen/ “Een piano, kunst, antiek of een kluis” · .b-bijzonder__kop, .b-bijzonder__noot, .b-bijzonder__lijst, .b-bijzonder__kaart (bijzonder.min.css)',
  'Kop links, de afspraken als noot rechts achter een Goudgele streep. Drie foto’s in een lijst met een witte binnenlijn en een zware schaduw; over de onderrand van elke foto schuift een witte kaart met het 3D-voorwerp in de kop. De middelste zakt iets, zoals de rechterkolom bij Brocken.',
  `<section class="sectie sectie--blauw vv v05"><div class="wrap">
      <div class="b-bijzonder__kop"><div class="b-kopgroep">${kopB(`<p class="intro">${T.intro}</p>`)}</div><p class="b-bijzonder__noot">${SLOT}</p></div>
      <div class="b-bijzonder__helften">${M.map(m => `
        <article class="b-bijzonder__helft"><figure class="b-bijzonder__foto"><span class="b-bijzonder__lijst">${foto(m)}</span></figure>
          <div class="b-bijzonder__kaart"><h3>${img(m.obj, 'b-bijzonder__icoon')}${m.t}</h3><p>${m.p}</p></div></article>`).join('')}
      </div>
    </div></section>`);

/* ======================= referentie A ======================= */

variant('Foto met gouden vlak', 'Referentie A', '/werkwijze/ #verhuisdag “Hoe uw spullen de wagen in gaan” · .blok.blok--vlak, .blok__foto, .blok__tekst, .d4, .d4--actief (assets/css/style.css)',
  'Het verhuisdagblok van referentie A. Links de foto met een Goudgeel vlak dat rechtsonder achter de foto uitsteekt, rechts label met lijntje, kop en intro. De momenten staan als witte kaartjes in het 2x2-raster (.d4); het vierde, gemarkeerde kaartje is de betaalafspraak. De rest van het slot is de slotalinea.',
  `<section class="sectie sectie--blauw vv v06"><div class="wrap"><div class="blok blok--vlak">
      <figure class="blok__foto">${foto(M[2])}</figure>
      <div class="blok__tekst">${kopK()}
        <ul class="d4">${M.map(m => `
          <li>${img(m.obj)}<div><b>${m.t}</b><span>${m.p}</span></div></li>`).join('')}
          <li class="d4--actief">${img(A[0].obj)}<div><b>${A[0].b}</b><span>${A[0].r}</span></div></li>
        </ul>
        <p class="blok__slot">${afspraak(A[1])} ${VW}</p>
      </div>
    </div></div></section>`);

variant('Stappen onder de ploeg', 'Referentie A', '/werkwijze/ “Wat gebeurt er nu eigenlijk op zo’n verhuisdag?” · .werkwijze__top, .werkwijze__wagen, .stappen, .stap, .stap__nr (assets/css/style.css)',
  'Kop links, rechts de uitgesneden verhuizers op de onderlijn. Eronder vier kolommen met een Goudgele bovenlijn en grote nummers, zoals bij referentie A waar stap 04 ook over het betalen gaat: hier is de vierde kolom het slot, met de kalender in plaats van een nummer.',
  `<section class="sectie sectie--blauw vv v07"><div class="wrap">
      <div class="werkwijze__top"><div class="sectiekop">${kopK()}</div>
        <figure class="werkwijze__wagen" aria-hidden="true">${img(['verhuisdag-verhuizers.webp', 709, 787])}</figure></div>
      <ol class="stappen">${M.map((m, i) => `
        <li class="stap"><span class="stap__nr" aria-hidden="true">${nr(i)}</span><h3>${m.t}</h3><p>${m.p}</p></li>`).join('')}
        <li class="stap stap--slot"><span class="stap__nr" aria-hidden="true">${img(A[0].obj)}</span><p>${SLOT}</p></li>
      </ol>
    </div></section>`);

variant('Donker paneel met rij', 'Referentie A', '/antiek-en-kunst-verhuizen/ en /dozencalculator/ · .blok.blok--stapel.blok--navy, .blok__boven, .usps.usps--rij, .ico (assets/css/style.css)',
  'Bovenin een Diepblauw paneel met afgeronde hoeken: tekst en afspraken links, de foto rechts met een Goudgele onderrand van 6 px. Onder het paneel de drie momenten als rij, elk met een rond vlak met het 3D-voorwerp.',
  `<section class="sectie sectie--blauw vv v08"><div class="wrap"><div class="blok blok--stapel blok--navy">
      <div class="blok__boven">
        <div class="blok__tekst">${kopK()}<p class="blok__slot">${SLOT}</p></div>
        <figure class="blok__foto">${foto(M[0])}</figure>
      </div>
      <ul class="usps usps--rij">${M.map(m => `
        <li><span class="ico">${img(m.obj)}</span><div><h3>${m.t}</h3><p>${m.p}</p></div></li>`).join('')}
      </ul>
    </div></div></section>`);

variant('Tijdlijn met polaroids', 'Referentie A', 'home “Meer dan honderd jaar verhuizen vanuit Venlo” · .hist5__in, .hist5__tl, .hist5__jaar, .hist5__stapel, .pol, .pol--trucks/--kar/--ad (assets/css/style.css)',
  'Links de kop en de momenten als tijdlijn met nummer, stip en lijn; het slot eronder. Rechts de polaroidstapel van referentie A met exact dezelfde verhoudingen (88 %, 46 %, 36 %, gedraaid en overlappend), maar in kleur: dit is vandaag, geen geschiedenis.',
  `<section class="sectie sectie--blauw vv v09"><div class="wrap hist5__in">
      <div class="hist5__tekst">${kopK()}
        <ol class="hist5__tl">${M.map((m, i) => `
          <li><span class="hist5__jaar">${nr(i)}</span><div><h3>${m.t}</h3><p>${m.p}</p></div></li>`).join('')}
        </ol>
        <p class="hist5__slot">${SLOT}</p>
      </div>
      <div class="hist5__stapel" aria-hidden="true">${M.map((m, i) => `
        <figure class="pol pol--${['trucks', 'kar', 'ad'][i]}">${foto(m)}<figcaption>${m.t}</figcaption></figure>`).join('')}
      </div>
    </div></section>`);

variant('Dienstkaarten met nummer', 'Referentie A', '/diensten/ · .diensten, .dienst, .dienst__nis, .dienst__nr + /werkwijze/ .tips-grid, .tip (assets/css/style.css)',
  'Kop in het midden. Drie Diepblauwe kaarten zoals de dienstkaarten van referentie A: foto bovenin met een Goudgeel nummerblok op de onderrand, daaronder kop en tekst (hover: alleen de kleur). De afspraken staan als twee witte, genummerde tegels uit referentie A-werkwijze eronder.',
  `<section class="sectie sectie--blauw vv v10"><div class="wrap">
      <div class="sectiekop sectiekop--midden">${kopK()}</div>
      <div class="diensten">${M.map((m, i) => `
        <article class="dienst"><div class="dienst__nis">${foto(m)}<span class="dienst__nr">${nr(i)}</span></div><div class="dienst__tekst"><h3>${m.t}</h3><p>${m.p}</p></div></article>`).join('')}
      </div>
      <div class="tips-grid">
        <div class="tip"><div><strong>${A[0].b}</strong><span>${A[0].r}</span></div></div>
        <div class="tip"><div><strong>${A[1].b}</strong><span>${A[1].r} ${VW}</span></div></div>
      </div>
    </div></section>`);

/* ======================= referentie B ======================= */

variant('Fotokaarten, mensen uit de foto', 'Referentie B (127.0.0.1:4760)', 'home “Waarmee wij je helpen” · .sgd1-grid, .sgd1-kaart, .sgd1-pop (__raam + __boven), .sgd1-ico, .sgd1-meer (blokken/diensten.css)',
  'Het dienstenblok van de referentie B-home. Witte kaarten met een smalle hoek; de foto wordt op het kader geknipt en de uitsnede staat alleen in een strook erboven, dus de verhuizers komen met hoofd en schouders boven de kaart uit. Het 3D-voorwerp hangt over de onderrand van de foto. Het slot is de verwijzende zin onder het raster.',
  `<section class="sectie sectie--blauw vv v11"><div class="wrap">
      <div class="sgd1-head">${kopS()}<p class="intro sgd1-intro">${T.intro}</p></div>
      <ul class="sgd1-grid">${M.map(m => `
        <li class="sgd1-kaart">
          ${pop(m, 'sgd1-beeld')}<span class="sgd1-ico">${img(m.obj)}</span></div>
          <div class="sgd1-tekst"><h3>${m.t}</h3><p>${m.p}</p></div>
        </li>`).join('')}
      </ul>
      <p class="sgd1-meer">${SLOT}</p>
    </div></section>`);

variant('Stapkaarten met verhuizers erboven', 'Referentie B (127.0.0.1:4760)', '/onze-werkwijze/ “In 4 stappen geregeld” · .sgdp-stappen, .sgdp-stap, .sgdp-stap__beeld, __figuur, __no, __ico + .sgdp-kaart--uitgelicht (blokken/dienst.css)',
  'Vier kaarten zoals de stappen van referentie B. Bovenin een warm geel vlak waarop de uitgesneden verhuizers staan, met hun hoofd boven de kaart; een nummerpil linksboven en het 3D-voorwerp op de onderrand. De vierde, Goudgele kaart (uitgelicht) draagt de afspraken.',
  `<section class="sectie sectie--blauw vv v12"><div class="wrap">
      <div class="sgdp-kop">${kopS()}<p class="intro sgdp-kop__sub">${T.intro}</p></div>
      <ol class="sgdp-stappen">${M.map((m, i) => `
        <li class="sgdp-kaart sgdp-stap"><div class="sgdp-stap__beeld">${fig(m, 'sgdp-stap__figuur')}<span class="sgdp-stap__ico">${img(m.obj)}</span></div><span class="sgdp-stap__no">${nr(i)}</span><h3>${m.t}</h3><p>${m.p}</p></li>`).join('')}
        <li class="sgdp-kaart sgdp-kaart--uitgelicht">${img(A[0].obj, 'sgdp-kaart__3d')}<p>${afspraak(A[0])}</p><p>${afspraak(A[1])}</p><p>${VW}</p></li>
      </ol>
    </div></section>`);

variant('Oplopende kaarten op een gele band', 'Referentie B (127.0.0.1:4760)', '/onze-werkwijze/ “Bel ons, videobel ons of kom langs” · .sgm__binnen, .sgm__beeld, .sgm__band, .sgm__kaart, .sgm__figuur, .sgm__doos (blokken/manieren.css)',
  'Tekst en afspraken links. Rechts drie witte kaarten die als een trap oplopen (48 px per kaart) boven een Goudgele band; achter de bovenrand van elke kaart staan de verhuizers van dat moment, uitgesneden uit de eigen foto. In de kaart het 3D-voorwerp en een nummerpil.',
  `<section class="sectie sectie--blauw vv v13"><div class="wrap sgm__binnen">
      <div class="sgm__tekst">${kopS()}<p class="intro sgm__intro">${T.intro}</p>
        <ul class="sgm__afspraken">${A.map(a => `<li>${img(a.obj)}<p>${afspraak(a)}</p></li>`).join('')}</ul>
        <p class="sgm__link">${ic('check')}<span>${VW}</span></p>
      </div>
      <div class="sgm__beeld"><div class="sgm__band" aria-hidden="true"></div>
        <ul class="sgm__kaarten">${M.map((m, i) => `
          <li class="sgm__kaart">${fig(m, 'sgm__figuur')}<div class="sgm__doos"><div class="sgm__boven">${img(m.obj, 'sgm__3d')}<span class="sgm__pil">${nr(i)}</span></div><h3>${m.t}</h3><p>${m.p}</p></div></li>`).join('')}
        </ul>
      </div>
    </div></section>`);

variant('Gekleurde tegels naast de foto', 'Referentie B (127.0.0.1:4760)', '/onze-werkwijze/ en home “Jouw regionale partner…” · .sgw-kop, .sgw-rij, .sgw-tegels, .sgw-tegel, .sgw-tegel__3d, .sgw-foto (foto + uitsnede boven de lijst) (blokken/waarom.css)',
  'Kop in het midden. Links vier tegels in vier kleuren (Diepblauw, wit, Lucht, Goudgeel) met het 3D-voorwerp in een wit rondje; de Goudgele tegel is die met de afspraken. Rechts de foto van het uitladen in een Goudgele lijn, waarbij verhuizer en bank boven de lijst uitkomen.',
  `<section class="sectie sectie--blauw vv v14"><div class="wrap">
      <div class="sgw-kop">${kopS()}<p class="intro">${T.intro}</p></div>
      <div class="sgw-rij">
        <ul class="sgw-tegels">${M.map(m => `
          <li class="sgw-tegel">${img(m.obj, 'sgw-tegel__3d')}<h3>${m.t}</h3><p>${m.p}</p></li>`).join('')}
          <li class="sgw-tegel sgw-tegel--slot">${img(A[0].obj, 'sgw-tegel__3d')}<p class="sgw-tegel__lead">${afspraak(A[0])}</p><p>${afspraak(A[1])} ${VW}</p></li>
        </ul>
        <figure class="sgw-foto">
          ${pop(M[2], 'pop--cq', '52px')}</div>
        </figure>
      </div>
    </div></section>`);

const sgtPos = (m, u) => {                  // .sgt__pand-rekensom: raam 16/10, kruin u (deel van de raamhoogte) erboven
  const s = (1 + u) * m.ar / (1.6 * (1 - m.top));
  const left = Math.min(0, Math.max(1 - s, 0.5 - m.cx * s));
  const top = 1 - s * 1.6 / m.ar;
  const uitH = s * 1.6 / m.ar;
  return `--l:${r4(left * 100)}%;--t:${r4(top * 100)}%;--w:${r4(s * 100)}%;--knip:${r4((uitH + top) / uitH * 100)}%`;
};
variant('Geel paneel met foto’s', 'Referentie B (127.0.0.1:4760)', 'home “Het team en het pand achter referentie B” · .sgt__paneel, .sgt__links/__rechts, .sgt__fotos, .sgt__raam + .sgt__uit, .sgt__lead (blokken/toennu.css)',
  'Een Goudgeel paneel met ronde hoeken op de blauwe band. Links de kop en drie gekantelde foto’s met een witte rand en een nummerpil; bij de middelste (Inladen) komen de verhuizer en de dozen boven de lijst uit, zoals het pand bij referentie B. Rechts de intro als vetgedrukte lead, de momenten en de afspraken.',
  `<section class="sectie sectie--blauw vv v15"><div class="wrap"><div class="sgt__paneel">
      <div class="sgt__links">${kopS(' lab-donker')}
        <div class="sgt__fotos" aria-hidden="true">
          <figure class="sgt__team">${foto(M[0])}<figcaption>${nr(0)}</figcaption></figure>
          <figure class="sgt__pand"><div class="sgt__beeld" style="${sgtPos(M[1], 0.3)}"><div class="sgt__raam">${img(M[1].foto, 'sgt__foto')}</div>${img(M[1].uit, 'sgt__uit')}</div><figcaption>${nr(1)}</figcaption></figure>
          <figure class="sgt__derde">${foto(M[2])}<figcaption>${nr(2)}</figcaption></figure>
        </div>
      </div>
      <div class="sgt__rechts">
        <p class="sgt__lead">${T.intro}</p>
        <ol class="sgt__momenten">${M.map((m, i) => `<li><span class="sgt__nr">${nr(i)}</span><div><h3>${m.t}</h3><p>${m.p}</p></div></li>`).join('')}</ol>
        <p class="sgt__slot">${SLOT}</p>
      </div>
    </div></div></section>`);

const html = `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Op de verhuisdag: 15 ontwerpen op referentiecode | De Reus</title>
<link rel="preload" href="/fonts/archivo-condensed-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="${siteCss}">
<link rel="stylesheet" href="${vdCss}">
<style>
${css}
</style>
</head>
<body class="p p-werkwijze">
${sprite}
<nav class="vnav" aria-label="Ontwerpen"><span class="vnav__titel">Op de verhuisdag · 15 ontwerpen</span><a href="#v00" title="Nu live">00</a>${V.map((v, i) => `<a href="#v${nr(i)}" title="${v.naam}" class="vnav__${v.site.slice(0, 5)}">${nr(i)}</a>`).join('')}<span class="vnav__uitleg"><i class="vnav__brock"></i>Brocken <i class="vnav__de-ki"></i>referentie A <i class="vnav__solar"></i>referentie B</span></nav>
<p class="vuitleg">/werkwijze/ #verhuisdag. Elk ontwerp is gebouwd op de HTML en CSS van één bestaand blok van brockenverhuizingen.nl (01–05), referentie A (06–10) of referentie B (11–15). Welk blok, staat erbij met de klassen uit het bronbestand. Kleuren, lettertypes en tekst zijn van De Reus, en de tekst is letterlijk die van de pagina. De foto’s en uitsnedes zijn de drie van nu, de 3D-voorwerpen komen van /kosten/ en /contact/. Niets beweegt. Rechts in elke kop staat de hoogte op dit scherm (een laptop toont zo’n 730 px). 00 is het blok zoals het nu live staat. Noem het nummer dat u wilt.</p>
<div class="variant" id="v00">
  <header class="vkop"><span class="vkop__nr">00</span><div><b>Nu live</b><small>Ontwerp 09 “Rondom uit het kader” met het afsprakenblok, ter vergelijking.</small></div><span class="vkop__h"></span></header>
  ${live}
  <div class="ctx-onder" aria-hidden="true"></div>
</div>
${V.map((v, i) => `<div class="variant" id="v${nr(i)}">
  <header class="vkop vkop--${v.site.slice(0, 5)}"><span class="vkop__nr">${nr(i)}</span><div><b>${v.naam}</b><small><span class="vkop__site">${v.site}</span> ${v.bron}</small><small>${v.uitleg}</small></div><span class="vkop__h"></span></header>
  ${v.html}
  <div class="ctx-onder" aria-hidden="true"></div>
</div>`).join('\n')}
<script>
// hoogte van elk blok op dit scherm, rechts in de kop
function meet(){document.querySelectorAll('.variant').forEach(function(v){var s=v.querySelector('section');var h=v.querySelector('.vkop__h');if(s&&h)h.textContent=Math.round(s.getBoundingClientRect().height)+' px hoog'})}
addEventListener('load',meet);addEventListener('resize',meet);
</script>
</body>
</html>
`;
fs.writeFileSync(UIT, html.replace(/\r?\n/g, '\r\n'));
console.log('geschreven', UIT, V.length, 'ontwerpen', Math.round(html.length / 1024) + ' kB');
