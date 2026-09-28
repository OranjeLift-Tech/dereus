// Ronde 2: 15 ontwerpen voor het vragenblok op /contact/ (#vragen), elk op de code van een echt blok van
// referentie A (Referentie A/assets/css/style.css) of referentie B (assets/css/blokken, pages).
// Geen bron uit ronde 1 (vragen-referentie-ronde1.html) opnieuw gebruikt.
// node gen.cjs  ->  _ontwerpen/vragen-contact-referentie.html
// Teksten komen letterlijk uit contact/index.html (sectie b-vragen, plus twee regels uit de vertrouwensrij).
const fs = require('fs');
const path = require('path');
const REPO = path.resolve(__dirname, '../..');
const lees = p => fs.readFileSync(path.join(REPO, p), 'utf8');
const PAG = lees('contact/index.html');
const hash = n => (PAG.match(new RegExp(`/css/min/${n}\\.min\\.css\\?v=([0-9a-f]+)`)) || [])[1];
const jsHash = (PAG.match(/\/js\/site\.js\?v=([0-9a-f]+)/) || [])[1];
const sprite = PAG.match(/<svg class="sprite"[\s\S]*?<\/svg>/)[0];

function maat(src) {
  const b = fs.readFileSync(path.join(REPO, src));
  if (src.endsWith('.svg')) return null;
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

// ---- de live teksten ----
const SEC = PAG.match(/<section class="sectie[^"]*b-vragen[\s\S]*?<\/section>/)[0];
const VRAGEN = [...SEC.matchAll(/<span class="vraag__tekst">([\s\S]*?)<\/span><span class="vraag__plus"[\s\S]*?<div class="vraag__antwoord">([\s\S]*?)<\/div>\s*<\/details>/g)]
  .map(m => ({ tekst: m[1], antwoord: m[2].trim() }));
const LABEL = SEC.match(/<p class="label">([\s\S]*?)<\/p>/)[1];
const H2 = SEC.match(/<h2 id="vragen-kop">([\s\S]*?)<\/h2>/)[1];
const STATUS = SEC.match(/<span class="bereikbaar[^>]*>[\s\S]*?<span class="bereikbaar__tekst"><\/span><\/span>/)[0];
const ZIN = SEC.match(/<\/span>\s*<p>([^<]*)<\/p>\s*<a class="knop/)[1];
const WA = SEC.match(/<a class="wa-link"[\s\S]*?<\/a>/)[0];
// twee regels uit de vertrouwensrij van dezelfde pagina (geen nieuwe tekst)
const VR = PAG.match(/<section class="b-vertrouwensrij[\s\S]*?<\/section>/)[0];
const VR_B = [...VR.matchAll(/<p><b>([^<]*)<\/b><span>([^<]*)<\/span><\/p>/g)].map(m => ({ b: m[1], s: m[2] }));
const GOOGLE = VR_B.find(x => /Google/.test(x.b));            // 4,9 uit 5 op Google
const ZEVEN = VR_B.find(x => /dagen per week/.test(x.b));      // 7 dagen per week bereikbaar
const ADVISEUR = VR_B.find(x => /verhuisadviseur/.test(x.b));  // Eén vaste verhuisadviseur
if (VRAGEN.length !== 4 || !GOOGLE || !ZEVEN || !ADVISEUR) throw new Error('tekst niet gevonden');
const zonderWa = html => html.replace(/<a class="wa-link"[\s\S]*?<\/a>/g, '');
const tekstVan = html => html.replace(/<[^>]+>/g, '');

// ---- bouwstenen ----
const ic = n => `<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-${n}"/></svg>`;
const kid = v => `kop-y${v}`;
const kop = (v, cls = '', accent = false) => {
  let h = H2;
  if (accent) { const w = h.split(' '); const l = w.pop(); h = `${w.join(' ')} <span class="accent">${l}</span>`; }
  return `<div class="kopgroep ${cls}"><p class="label">${LABEL}</p><h2 id="${kid(v)}">${h}</h2></div>`;
};
const status = (cls = '') => STATUS.replace('bereikbaar vragen__status', `bereikbaar q-status ${cls}`.trim());
const zin = (cls = '') => `<p class="q-zin ${cls}">${ZIN}</p>`;
const bel = (cls = '') => `<a class="q-bel ${cls}" href="tel:+31850005647">${ic('telefoon')}<span>Bel 085 000 5647</span></a>`;
const knoppen = (cls = '') => `<div class="q-knoppen ${cls}">${bel()}${WA}</div>`;
const nr = i => String(i + 1).padStart(2, '0');
// een vraag: echte <details>, per blok dezelfde name zodat er één tegelijk openstaat
const vraag = (v, i, o = {}) => {
  const q = VRAGEN[i];
  return `<details class="q ${o.cls || ''}" name="y${v}"${o.open && i === 0 ? ' open' : ''}>
<summary>${o.voor ? o.voor(i) : ''}${o.geenNr ? '' : `<span class="q__nr" aria-hidden="true">${nr(i)}</span>`}<span class="q__tekst">${q.tekst}</span><span class="q__plus" aria-hidden="true">${ic('plus')}</span></summary>
<div class="q__antwoord">${q.antwoord}</div>
</details>`;
};
const lijst = (v, cls, o = {}) => `<div class="q-lijst ${cls}">${VRAGEN.map((_, i) => vraag(v, i, o)).join('')}</div>`;
const sec = (v, grond, inner, cls = '') => `<section class="sectie sectie--${grond} v y${v} ${cls}" aria-labelledby="${kid(v)}">
${inner}
</section>`;
const wrap = inner => `<div class="wrap">\n${inner}\n</div>`;

// 3D-voorwerp per vraag: klok (hoe snel), kalender (avond/weekend), envelop (bericht), formulier (welk formulier)
const OBJ = ['/img/contact-3d/klok.webp', '/img/kosten-kalender/blok.webp', '/img/contact-3d/envelop.webp', '/img/contact-3d/formulier.webp'];
// een letterlijk stuk uit elk antwoord, voor de tegels van 15
const KERN = ['Binnen 24 uur', '08.00 tot 20.00 uur', 'Vertel kort', 'Offerteformulier'];

const V = [];
const add = (n, naam, bron, uitleg, html) => V.push({ n, naam, bron, uitleg, html });

// ================= referentie A =================
add('01', 'Diepblauwe kaart met de driekleurige streep', 'Referentie A, blok Erkende Verhuizer (.zeker__card, .zeker__head, .zeker__list, .zeker__ok, .zeker__cta)',
  'Het keurmerkblok van referentie A: een donkere kaart met een streep in drie kleuren bovenaan, links het logo, in het midden de kop en rechts een beeldmerk (hier de 3D-vraagtekens). De vragen staan in twee kolommen met een dunne lijn erboven en een gele schijf met het nummer, zoals de vinkschijven van referentie A. Onderaan de knoppenrij.',
  v => sec(v, 'wit', wrap(`<div class="y01__kaart">
<div class="y01__kop"><span class="y01__logo">${img('/img/logo/dereus-logo-negatief.svg')}</span><div class="y01__intro">${kop(v)}${status('q-status--donker')}</div>${img('/img/kaart-3d/vraagtekens.webp', 'y01__merk')}</div>
<ul class="y01__lijst" role="list">${VRAGEN.map((_, i) => `<li>${vraag(v, i, { geenNr: true, voor: j => `<span class="y01__ok" aria-hidden="true">${nr(j)}</span>` })}</li>`).join('')}</ul>
<div class="y01__cta">${zin()}${knoppen()}</div>
</div>`)));

add('02', 'Uitgelichte vraag naast een scorepaneel', 'Referentie A homepage #reviews (.reviews__hoofd, .uitgelicht, .scorepaneel, .rgrid, .review)',
  'De reviewopzet van referentie A: links één uitgelichte review met een groot citaat, rechts een donker cijferpaneel, daaronder compacte kaarten. Hier is vraag 01 de uitgelichte, met het antwoord als citaat van De Reus. Het paneel toont 4,9 uit 5 op Google en twee regels uit de vertrouwensrij van dezelfde pagina, met de knoppen. De andere drie vragen staan als kaarten eronder. Alle antwoorden zijn meteen te lezen, zonder klikken.',
  v => sec(v, 'wit', wrap(`<div class="y02__hoofd"><div class="y02__links">${kop(v)}
<figure class="y02__uitgelicht"><p class="y02__rate"><span class="y02__nr">${nr(0)}</span><span class="y02__vraag">${VRAGEN[0].tekst}</span></p>
<blockquote>${zonderWa(VRAGEN[0].antwoord)}</blockquote>
<figcaption><span class="y02__av" aria-hidden="true">${img('/img/logo/dereus-beeldmerk.svg')}</span><span class="y02__wie"><b>Verhuisbedrijf De Reus</b>${status()}</span></figcaption></figure></div>
<aside class="y02__score" aria-label="Bereikbaarheid"><p class="y02__cijfer"><b>${GOOGLE.b.split(' ')[0]}</b><span>${GOOGLE.b.split(' ').slice(1).join(' ')}</span></p>
<ul class="y02__feiten" role="list"><li>${ZEVEN.b}</li><li>${ADVISEUR.b}</li></ul>
<div class="y02__acties">${zin()}${bel()}${WA}</div></aside></div>
<ul class="y02__rgrid" role="list">${[1, 2, 3].map(i => `<li class="y02__kaart"><p class="y02__rate"><span class="y02__nr">${nr(i)}</span></p><h3>${VRAGEN[i].tekst}</h3><div class="y02__tekst">${VRAGEN[i].antwoord}</div></li>`).join('')}</ul>`)));

add('03', 'Gedraaid vlak achter de foto', 'Referentie A, vierkant-blok "Goed voorbereid verhuizen" (.vierkant__hoek, .vierkant__vinkjes, .vierkant__vorm, .vierkant__duo)',
  'Het vierkant-blok van referentie A in zijn laatste vorm: links de kop en de punten als vinkjeslijst, rechts een foto in een afgeronde rechthoek met een gedraaid lichtblauw vlak en een gouden lijn erachter. Rechtsboven de Diepblauwe cirkel met het beeldmerk. De vinkjes zijn hier de vragen; het antwoord klapt eronder open. Foto: de verhuizer met dozen (nog niet op /contact/).',
  v => sec(v, 'wit', `<span class="y03__hoek" aria-hidden="true">${img('/img/logo/dereus-beeldmerk-negatief.svg')}</span>
${wrap(`<div class="y03__in"><div class="y03__tekst">${kop(v)}
<div class="y03__vinkjes">${VRAGEN.map((_, i) => vraag(v, i, { geenNr: true, voor: () => `<span class="y03__vink" aria-hidden="true">${ic('check')}</span>` })).join('')}</div>
<div class="y03__knoprij">${zin()}${knoppen()}</div></div>
<div class="y03__fig" aria-hidden="true"><span class="y03__vorm"></span>${img('/img/over-verhuizer.webp', 'y03__foto')}</div></div>`)}`));

add('04', 'Schuine band, de verhuizer staat erop', 'Referentie A homepage #opslag (.opslag__band, .opslag__mark, .opslag__script, .opslag__lijn, .opslag__kaart, .opslag__persoon)',
  'Het opslagblok van referentie A: onderin een schuine band (hier Koningsblauw naar Diepblauw) met links het beeldmerk en rechts het woordmerk, met een gele lijn eronder. Links een kaart met de kop, de vragen en de knoppen, die over de band valt; rechts staat de verhuizer met baard op de band, schuin afgesneden zodat hij op de lijn lijkt te staan.',
  v => sec(v, 'wit', `<span class="y04__band" aria-hidden="true">${img('/img/logo/dereus-beeldmerk-negatief.svg', 'y04__mark')}${img('/img/logo/dereus-logo-zonder-tagline-negatief.svg', 'y04__script')}</span><span class="y04__lijn" aria-hidden="true"></span>
${wrap(`<div class="y04__in"><div class="y04__kaart">${kop(v)}${lijst(v, 'y04__lijst')}<div class="y04__bel">${status('q-status--pil')}${knoppen()}</div></div>
<div class="y04__fig" aria-hidden="true">${img('/img/offerte-figuur-uit.webp', 'y04__persoon')}</div></div>`)}`));

add('05', 'Tijdlijn met een fotostapel', 'Referentie A homepage #historie (.hist5__in, .hist5__tl, .hist5__jaar, .hist5__stapel, .pol, .pol--trucks/--kar/--ad)',
  'Het historieblok van referentie A: links een tijdlijn met een lijn, een stip en een groot getal per regel, rechts drie foto\'s als polaroids over elkaar (verhoudingen letterlijk van referentie A). Hier is elke regel een vraag met het antwoord eronder, meteen leesbaar. De onderschriften zijn woorden uit de antwoorden. Geen beweging bij hover (Referentie A kantelt de foto recht).',
  v => sec(v, 'wit', wrap(`<div class="y05__in"><div class="y05__tekst">${kop(v)}
<ol class="y05__tl">${VRAGEN.map((q, i) => `<li><span class="y05__nr">${nr(i)}</span><div><h3>${q.tekst}</h3>${q.antwoord}</div></li>`).join('')}</ol>
<div class="y05__bel">${zin()}${knoppen()}</div></div>
<div class="y05__stapel" aria-hidden="true">
<figure class="y05__pol y05__pol--a">${img('/img/stap-2-bellen.webp')}<figcaption>085 000 5647</figcaption></figure>
<figure class="y05__pol y05__pol--b">${img('/img/stap-1-formulier.webp')}<figcaption>Contactformulier</figcaption></figure>
<figure class="y05__pol y05__pol--c">${img('/img/stap-3-offerte.webp')}<figcaption>Offerteformulier</figcaption></figure>
</div></div>`)));

add('06', 'Blauwe kaart met foto en badge', 'Referentie A homepage #dozen (.dozen__card, .dozen__card::before, .dozen__body, .dozen__media, .badge)',
  'De dozenkaart van referentie A: één kaart met ronde hoeken, links een gekleurd vlak met een zacht beeldmerk als watermerk, rechts een foto over de volle hoogte met een donkere badge in de hoek. Hier Koningsblauw met de kop en de vragen als lichte regels; de badge toont of we nu bereikbaar zijn en "7 dagen per week bereikbaar" uit de vertrouwensrij.',
  v => sec(v, 'wit', wrap(`<div class="y06__kaart"><div class="y06__body">${kop(v)}${lijst(v, 'y06__lijst')}<div class="y06__bel">${zin()}${knoppen()}</div></div>
<div class="y06__media">${img('/img/stap-2-bellen.webp', 'y06__foto')}<span class="y06__badge">${status('y06__ab')}<span class="y06__abk">${ZEVEN.b}</span></span></div></div>`)));

add('07', 'Lichtblauw paneel met tegeltjes, foto op een geel vlak', 'Referentie A #wonen en #team (.blok--paneel .blok__tekst, .d4, .d4--actief, .blok--vlak .blok__foto::before)',
  'Twee referentie A-regels samen: het tekstpaneel van #wonen (lichte kleur, dikke rand links, witte tegeltjes met een klein icoon) en de foto van #team met een gekleurd vlak dat rechtsonder achter de foto uitsteekt. De tegeltjes zijn de vragen met een klein 3D-voorwerp; open wordt de tegel lichtblauw met een blauwe rand (.d4--actief). De foto: drie verhuizers die nog nergens op de site staan.',
  v => sec(v, 'wit', wrap(`<div class="y07__rij"><div class="y07__tekst">${kop(v)}
<div class="y07__d4">${VRAGEN.map((_, i) => vraag(v, i, { geenNr: true, voor: j => img(OBJ[j], 'y07__ic') })).join('')}</div>
<div class="y07__bel">${status('q-status--pil')}${knoppen()}</div></div>
<figure class="y07__foto" aria-hidden="true"><span class="y07__raam">${img('/img/helpen-wij-u-snel.webp', 'y07__mens')}</span></figure></div>`)));

add('08', 'Tekst en foto boven, vier vragen op een rij', 'Referentie A /contact/ #contact-intro (.blok--stapel, .blok__boven, .blok__foto figcaption, .usps--rij)',
  'Het eerste contactblok van referentie A zelf: boven de tekst met de knoppen naast een foto met een donker glazen label (hier de klantenservicemedewerker met headset, een foto die nog nergens op de site staat), daaronder vier punten over de volle breedte, elk met een rond icoon, een kop en een alinea. De vier punten zijn hier de vier vragen, met het antwoord er direct onder.',
  v => sec(v, 'wit', wrap(`<div class="y08__boven"><div class="y08__tekst">${kop(v)}${status('q-status--pil')}${zin()}${knoppen()}</div>
<figure class="y08__foto">${img('/img/headers/contact.webp')}<figcaption>${ZEVEN.b}</figcaption></figure></div>
<ul class="y08__usps" role="list">${VRAGEN.map((q, i) => `<li><span class="y08__ico" aria-hidden="true">${img(OBJ[i])}</span><div><h3>${q.tekst}</h3>${q.antwoord}</div></li>`).join('')}</ul>`)));

// ================= referentie B =================
add('09', 'Witte kaart met een geel uitkomstvak', 'Referentie B /zonnepanelen-kopen/ #berekenen (.sgdp-calc__kaart, .sgdp-calc__uit, .sgdp-calc__label, .sgdp-calc__getal, .sgdp-calc__bel)',
  'De rekenkaart van referentie B: links de invoer, rechts een zongeel vak met een klein label, een groot getal in een vlakje, een regel eronder en de knop. Hier staan links de vragen als rijen (zoals de staffelrijen), en in het gele vak "Staat uw vraag er niet bij?", het telefoonnummer als groot getal (klikbaar), de bereikbaarheid en WhatsApp. De 3D-telefoon steekt boven het vak uit.',
  v => sec(v, 'wit', wrap(`<div class="y09__kaart"><div class="y09__intro">${kop(v)}</div>${lijst(v, 'y09__lijst')}
<div class="y09__uit">${img('/img/contact-3d/telefoon.webp', 'y09__3d', ' aria-hidden="true"')}<span class="y09__label">${ZIN}</span><a class="y09__getal" href="tel:+31850005647">085 000 5647</a>${status('y09__bereik')}<span class="y09__detail">${ZEVEN.b}</span>${WA}</div></div>`)));

add('10', 'Blauwe kaart, de medewerker komt erboven uit', 'Referentie B /zonnepanelen-kopen/ voorraad (.sgdp-voorraad__kaart, .sgdp-voorraad__media, .sgdp-figuur, .sgdp-badge)',
  'Het voorraadblok van referentie B: een groene kaart met links de tekst en rechts een uitgeknipte figuur die op de onderrand staat en met hoofd en schouders boven de kaart uitkomt, met een lime badge linksonder. Hier Koningsblauw, de vragen als lichte regels, de klantenservicemedewerker met headset (nog nergens op de site) en een gele badge met de bereikbaarheid.',
  v => sec(v, 'wit', wrap(`<div class="y10__kaart"><div class="y10__body">${kop(v)}${lijst(v, 'y10__lijst')}<div class="y10__bel">${zin()}${knoppen()}</div></div>
<div class="y10__media">${img('/img/contact-uit.webp', 'y10__figuur', ' aria-hidden="true"')}<span class="y10__badge"><span class="y10__badge-ic" aria-hidden="true">${ic('telefoon')}</span>${status('y10__st')}</span></div></div>`)));

add('11', 'Witte balk met vier vragen en een brede belkaart', 'Referentie B kerncijferbalk (.kerncijfers__rij, .kerncijfer, .kerncijfer__ic) + /warmtepomp-kopen/ (.sgdp-kaart--breed)',
  'De kerncijferbalk die referentie B op elke pagina heeft: één witte balk met vier vakken, gescheiden door een dunne lijn, elk met een 3D-voorwerp en een vetgedrukte regel. Elk vak is een vraag; open valt het antwoord in hetzelfde vak. Daaronder de brede kaart van referentie B (voorwerp links, tekst, knoppen rechts) voor "Staat uw vraag er niet bij?".',
  v => sec(v, 'lucht', wrap(`${kop(v, 'y11__kop')}
<div class="y11__rij">${VRAGEN.map((_, i) => vraag(v, i, { cls: 'y11__cel', geenNr: true, voor: j => img(OBJ[j], 'y11__ic') })).join('')}</div>
<div class="y11__breed">${img('/img/contact-3d/headset.webp', 'y11__3d', ' aria-hidden="true"')}<div class="y11__tekst"><h3>${ZIN}</h3>${status('q-status--pil')}</div>${knoppen('y11__knoppen')}</div>`)));

add('12', 'Vraag kiezen, antwoord in de gele pil', 'Referentie B scanvak onder elke paginakop (.sv-kaart, .sv-kop, .sv-logos, .sv-logo, .sv-keuze, .sv-chip:has(input:checked), .sv-pil, .sv-veld, .sv-knop)',
  'Het scanvak van referentie B: een lichte kaart met een blauwe rand, de kop links en kleine witte tegels rechtsboven, daaronder keuzechips en een brede pil met een wit veld en een knop. Hier zijn de chips de vier vragen (echte keuzerondjes, zonder JavaScript): het antwoord van de gekozen vraag staat in het witte veld van de gele pil, met de belknop ernaast. De tegels: Google-score, bereikbaarheid en de vaste verhuisadviseur.',
  v => sec(v, 'wit', wrap(`<div class="y12__kaart"><div class="y12__kop"><div class="y12__tekst">${kop(v)}</div>
<div class="y12__logos"><span class="y12__logo">${ic('google')}<span><b>${GOOGLE.b.split(' ')[0]}</b> ${GOOGLE.b.split(' ').slice(1).join(' ')}</span></span><span class="y12__logo">${status()}</span><span class="y12__logo">${img('/img/contact-3d/headset.webp', 'y12__3d', ' aria-hidden="true"')}<span>${ADVISEUR.b}</span></span></div></div>
<fieldset class="y12__keuze"><legend class="vh">${H2}</legend><div class="y12__chips">${VRAGEN.map((q, i) => `<label class="y12__chip"><input type="radio" name="y12" value="${i + 1}"${i === 0 ? ' checked' : ''}><span>${q.tekst}</span></label>`).join('')}</div></fieldset>
<div class="y12__pil"><div class="y12__veld" aria-live="polite">${VRAGEN.map((q, i) => `<div class="y12__antw y12__antw--${i + 1}">${zonderWa(q.antwoord)}</div>`).join('')}</div>${bel('y12__knop')}${WA}</div></div>`)));

add('13', 'Zachte band met V-rand, voorwerpen steken uit de kaart', 'Referentie B homepage #diensten (.sgd1 ::before/::after, .sgd1-grid, .sgd1-kaart, .sgd1-pop, .sgd1-ico, .sgd1-meer) + .sgdp-pop--raam',
  'Het dienstenblok van referentie B: een lichte band met een V aan de bovenkant en een schuine punt onderaan, witte kaarten met een kleine hoek, bovenin een beeldvak waar het onderwerp bovenuit steekt en een rond icoon op de onderrand. Hier staat in elk vak een 3D-voorwerp op een lichtblauw vlak (de --raam-variant van referentie B), het nummer als gele schijf op de rand, de vraag en het antwoord in de kaart. Onder het raster de verwijzende zin.',
  v => sec(v, 'wit', `<span class="y13__band" aria-hidden="true"></span>
${wrap(`<div class="y13__kop">${kop(v)}${status('q-status--pil')}</div>
<ul class="y13__grid" role="list">${VRAGEN.map((q, i) => `<li class="y13__kaart"><div class="y13__beeld"><span class="y13__raam"></span>${img(OBJ[i], `y13__obj y13__obj--${i + 1}`, ' aria-hidden="true"')}<span class="y13__ico" aria-hidden="true">${nr(i)}</span></div><div class="y13__tekst"><h3>${q.tekst}</h3>${q.antwoord}</div></li>`).join('')}</ul>
<p class="y13__meer">${ZIN} <a href="tel:+31850005647">Bel 085 000 5647</a>${WA}</p>`)}`));

add('14', 'Grote foto links, vragen als gegevensrijen', 'Referentie B /contact/ (.sgct-plek__in, .sgct-kaartbeeld, .sgct-kaartbeeld__pin, .sgct-route, .sgct-bron, .sgct-gegevens dl)',
  'Het adresblok van referentie B: links een groot beeld met een lijn en schaduw, met een markering, een knop linksonder en een klein label rechtsboven; rechts een kop en een lijst met rijen tussen dunne lijnen (links vet, rechts de waarde). Hier is het beeld een foto van iemand die een bericht typt, de markering de bereikbaarheid, de knop "Bel" en het label WhatsApp; rechts elke vraag met het antwoord ernaast, zonder klikken.',
  v => sec(v, 'wit', wrap(`<div class="y14__in"><figure class="y14__beeld">${img('/img/stap-1-formulier.webp', 'y14__foto')}${status('q-status--pil y14__pin')}${bel('y14__route')}<span class="y14__bron">${WA}</span></figure>
<div class="y14__gegevens">${kop(v)}<dl>${VRAGEN.map((q, i) => `<div><dt><span class="y14__nr">${nr(i)}</span>${q.tekst}</dt><dd>${q.antwoord}</dd></div>`).join('')}</dl></div></div>`)));

add('15', 'Lichte kaart met vier tegels', 'Referentie B homepage #duurzaam (.sgz__kaart, .sgz__tekst, .sgz__link, .sgz__tegels, .sgz__tegel, .sgz__3d, .sgz__tegel--woord)',
  'Het duurzaamblok van referentie B: een lichte kaart, links de kop en een tekstlink met pijl, rechts witte tegels met een 3D-voorwerp, een groot woord en een klein onderschrift. Hier is het grote woord een stukje uit het antwoord (Binnen 24 uur, 08.00 tot 20.00 uur, Vertel kort, Offerteformulier) en het onderschrift de vraag; open staat het hele antwoord in de tegel.',
  v => sec(v, 'wit', wrap(`<div class="y15__kaart"><div class="y15__tekst">${kop(v)}${status('q-status--pil')}<p class="y15__zin">${ZIN}</p><a class="y15__link" href="tel:+31850005647"><span>Bel 085 000 5647</span>${ic('pijl')}</a>${WA}</div>
<div class="y15__tegels">${VRAGEN.map((q, i) => `<details class="q y15__tegel" name="y${v}"><summary>${img(OBJ[i], 'y15__3d')}<b>${KERN[i]}</b><small>${q.tekst}</small><span class="q__plus" aria-hidden="true">${ic('plus')}</span></summary><div class="q__antwoord">${q.antwoord}</div></details>`).join('')}</div></div>`)));

// controle: elk kernwoord staat echt in zijn antwoord
KERN.forEach((k, i) => { if (!tekstVan(VRAGEN[i].antwoord).toLowerCase().includes(k.toLowerCase())) throw new Error('kern niet letterlijk: ' + k); });

// ---- pagina ----
const css = fs.readFileSync(path.join(__dirname, 'var.css'), 'utf8');
const navl = ['00', ...V.map(x => x.n)].map(n => `<a href="#v${n}">${n}</a>`).join('');
const kap = (n, naam, bron, uitleg) => `<div class="vkap" id="v${n}"><div class="wrap"><span class="vkap__nr">${n}</span><div><b>${naam}</b><small>${bron}</small><p>${uitleg}</p></div><span class="vkap__maat" data-maat></span></div></div>`;
// het blok erboven op /contact/ is de Diepblauwe band "Wat er gebeurt na uw bericht"
const ctx = `<div class="vctx" aria-hidden="true"><div class="wrap">Hierboven op /contact/: Diepblauwe band "Wat er gebeurt na uw bericht"</div></div>`;
const live = SEC.replace('id="vragen"', 'id="vragen-live"').replace(/id="vragen-kop"/, 'id="vragen-kop-live"')
  .replace('aria-labelledby="vragen-kop"', 'aria-labelledby="vragen-kop-live"')
  .replace(/id="vragen-(\d)"/g, 'id="vragen-live-$1"').replace(/name="vragen"/g, 'name="vragen-live"');

const html = `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=' js'</script>
<title>Vragen over contact · ronde 2 · referentie A + referentie B</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="/css/min/site.min.css?v=${hash('site')}">
<link rel="stylesheet" href="/css/min/vragen.min.css?v=${hash('vragen')}">
<style>
${css}
</style>
<script src="/js/site.js?v=${jsHash}" defer></script>
</head>
<body>
${sprite}
<nav class="vnav" aria-label="Ontwerpen"><div class="wrap"><b>/contact/ #vragen · ronde 2 · 15 ontwerpen</b><div class="vnav__links">${navl}</div></div></nav>
${kap('00', 'Nu live', 'Ter vergelijking', 'Het huidige blok op /contact/, ongewijzigd. Ronde 1 (15 andere ontwerpen) staat nog in vragen-referentie-ronde1.html; deze ronde gebruikt geen enkele bron daaruit opnieuw.')}
${ctx}
${live}
${V.map(x => kap(x.n, x.naam, x.bron, x.uitleg) + '\n' + ctx + '\n' + x.html(x.n)).join('\n')}
<div class="vkap vkap--eind"><div class="wrap"><p>Alle teksten zijn letterlijk die van /contact/ (het vragenblok, plus "4,9 uit 5 op Google", "7 dagen per week bereikbaar" en "Eén vaste verhuisadviseur" uit de vertrouwensrij van dezelfde pagina). Beelden zijn bestaande De Reus-foto's, uitsnedes en 3D-renders uit /img, en geen mensen die al op /contact/ staan. Elke bronklasse hierboven bestaat echt in de code van referentie A of referentie B; in de De Reus-code komen die namen niet terug. Kies een nummer.</p></div></div>
<script>
(function(){
function meet(){document.querySelectorAll('[data-maat]').forEach(function(m){var s=m.closest('.vkap').nextElementSibling;while(s&&s.tagName!=='SECTION')s=s.nextElementSibling;if(!s)return;var h=Math.round(s.getBoundingClientRect().height);m.textContent='Blokhoogte '+h+' px';m.classList.toggle('is-hoog',h>730);});}
addEventListener('load',meet);addEventListener('resize',meet);document.addEventListener('toggle',meet,true);document.addEventListener('change',meet);
})();
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(REPO, '_ontwerpen/vragen-contact-referentie.html'), html);
console.log('ok', html.length, VRAGEN.length, GOOGLE.b, ZEVEN.b, ADVISEUR.b);
