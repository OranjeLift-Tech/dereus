// De tien ontwerpen. Elk ontwerp is de opbouw van een echt blok (bronklasse in het bijschrift), met de teksten van
// /kosten/ #opbouw, De Reus-tokens en eigen klassen .oNN (CSS in var.css).
module.exports = ({ add, T, img, ic, foto, FOTO, POP, pop, obj, VAK_OBJ, SOORT_OBJ, nr2, EIGEN }) => {
  const F = T.factoren, D = T.vakken, S = T.soorten;
  const kid = v => `kop-o${v}`;
  const kop = (v, cls = '', o = {}) => `<div class="kopgroep ${cls}"><p class="label">${T.label}</p><h2 class="h2" id="${kid(v)}">${T.h2}</h2>${o.geenIntro ? '' : `<p class="intro">${T.intro}</p>`}</div>`;
  const sec = (v, grond, inner, cls = '') => `<section class="sectie sectie--${grond} v o${v} ${cls}" aria-labelledby="${kid(v)}">\n${inner}\n</section>`;
  const of = (cls = '') => `<span class="of ${cls}" aria-hidden="true">${T.of}</span>`;
  const vink = () => `<span class="vink" aria-hidden="true">${ic('check')}</span>`;
  const soorten = (cls, o = {}) => `<ul class="${cls}">${S.map((s, i) => `<li>${o.obj ? obj(SOORT_OBJ[i]) : vink()}<div><h3>${s.titel}</h3><p>${s.tekst}</p></div></li>`).join('')}</ul>`;

  // ================= referentie A =================

  add('01', 'Wagen boven het stappenpaneel', 'Referentie A · .werkwijze__top + .stappen ("Zo verloopt uw verhuizing")',
    'Kop links, rechts de echte De Reus-bakwagen die op het paneel staat; het paneel heeft de vijf factoren als genummerde kolommen met een lijn ertussen, zoals de stappen van referentie A. Onder het paneel All-in prijs (Koningsblauwe plaat, klembord met de offerte) of Regieprijs (witte plaat, wekker), en rechts de slottekst met de twee zekerheden.',
    v => sec(v, 'lucht', `<div class="wrap">
  <div class="o01__top">${kop(v)}<figure class="o01__wagen">${obj('bakwagen')}</figure></div>
  <div class="o01__paneel">
    <h3 class="lijstkop">${T.lijstkop}</h3>
    <ol class="o01__stappen">${F.map((f, i) => `<li class="o01__stap"><span class="o01__nr" aria-hidden="true">${nr2(i)}</span><h3>${f.titel}</h3><p>${f.tekst}</p></li>`).join('')}</ol>
  </div>
  <div class="o01__onder">
    <div class="o01__duo">${D.map((d, i) => `<div class="o01__vak${i === 0 ? ' o01__vak--blauw' : ''}">${obj(VAK_OBJ[i])}<h3>${d.titel}</h3><p>${d.tekst}</p></div>`).join(of())}</div>
    <div class="o01__rest"><p class="o01__slot">${T.slot}</p>${soorten('o01__soorten')}</div>
  </div>
</div>`));

  add('02', 'Tijdlijn met twee afdrukken', 'Referentie A · .hist5 + .hist5__tl + .pol ("Meer dan honderd jaar verhuizen")',
    'De opbouw van het historieblok: links de kop en de vijf factoren als tijdlijn (nummer, punt op de lijn, titel en uitleg), rechts een stapel foto-afdrukken. De twee afdrukken zijn All-in prijs (de handtekening onder de offerte) en Regieprijs (uitladen op de verhuisdag), met een gele "of"-sticker ertussen. Onder de tijdlijn de slottekst en de twee zekerheden.',
    v => sec(v, 'wit', `<div class="wrap o02__in">
  <div class="o02__tekst">
    ${kop(v)}
    <h3 class="lijstkop">${T.lijstkop}</h3>
    <ol class="o02__tl">${F.map((f, i) => `<li><span class="o02__nr" aria-hidden="true">${nr2(i)}</span><div><h3>${f.titel}</h3><p>${f.tekst}</p></div></li>`).join('')}</ol>
    <p class="o02__slot">${T.slot}</p>
    ${soorten('o02__soorten')}
  </div>
  <div class="o02__stapel">
    <figure class="o02__pol o02__pol--1">${img('/img/stap-3-offerte.webp', '')}<figcaption><h3>${D[0].titel}</h3><p>${D[0].tekst}</p></figcaption></figure>
    <figure class="o02__pol o02__pol--2">${img('/img/verhuisdag-uitladen.webp', '')}<figcaption><h3>${D[1].titel}</h3><p>${D[1].tekst}</p></figcaption></figure>
    ${of('o02__of')}
  </div>
</div>`));

  add('03', 'Open kaart: paneel met tabel en foto', 'Referentie A · .blok.blok--stapel.blok--paneel + .dzc-tabel + .usps--rij ("Waar dit getal vandaan komt")',
    'Links een lichtblauw paneel met een dikke gele rand links (blok--paneel) met de kop en de vijf factoren als tabel, rechts een hoge foto met een donkere bijschriftbalk. Daaronder de rij van vier (usps--rij): All-in prijs of Regieprijs, Geen voorrijkosten, Betalen op de verhuisdag, elk met een echt voorwerp in een ronde tegel. De slottekst sluit af.',
    v => sec(v, 'wit', `<div class="wrap">
  <div class="o03__boven">
    <div class="o03__paneel">
      ${kop(v)}
      <p class="lijstkop">${T.lijstkop}</p>
      <div class="o03__tabelvak"><table class="o03__tabel"><tbody>${F.map((f, i) => `<tr><th scope="row"><span class="o03__nr" aria-hidden="true">${nr2(i)}</span>${f.titel}</th><td>${f.tekst}</td></tr>`).join('')}</tbody></table></div>
    </div>
    <figure class="o03__foto">${foto(2)}<figcaption>${F[2].titel}</figcaption></figure>
  </div>
  <ul class="o03__rij">${D.map((d, i) => `<li><span class="o03__ico">${obj(VAK_OBJ[i])}</span>${i === 1 ? of('o03__of') : ''}<div><h3>${d.titel}</h3><p>${d.tekst}</p></div></li>`).join('')}${S.map((s, i) => `<li><span class="o03__ico">${obj(SOORT_OBJ[i])}</span><div><h3>${s.titel}</h3><p>${s.tekst}</p></div></li>`).join('')}</ul>
  <p class="o03__slot">${T.slot}</p>
</div>`));

  // ================= referentie B =================

  const FIG = [
    { src: EIGEN + 'fig-woningontruiming.webp', cls: 'breed' },
    { src: EIGEN + 'verhuizer-doos.webp', cls: '' },
    { src: EIGEN + 'fig-verhuislift.webp', cls: 'breed' },
    { src: EIGEN + 'fig-montage.webp', cls: 'rechts' },
    { src: EIGEN + 'fig-opslag.webp', cls: '' },
  ];
  add('04', 'Kaarten met de verhuizer erboven uit', 'Referentie B · /bedrijven/ .sgdp-stappen + .sgdp-stap + .sgdp-stap__figuur ("In vier stappen …") en .sgz ("Een boom bij elke klus")',
    'Het blok "Zo werkt het" van /bedrijven/: vijf witte kaarten met een warm vlak bovenin, waar een echte De Reus-verhuizer boven de kaart uitsteekt (twee man met een doos, de oudere verhuizer met een doos, de verhuislift, de boormachine, de opslag), een Koningsblauw nummer-label en daaronder titel en uitleg. Daaronder het paneel uit hetzelfde referentieblok (.sgz): links de slottekst met de twee zekerheden, rechts de tegels All-in prijs of Regieprijs met het klembord en de wekker.',
    v => sec(v, 'lucht', `<div class="wrap">
  <div class="o04__kop">${kop(v)}</div>
  <h3 class="lijstkop">${T.lijstkop}</h3>
  <ol class="o04__stappen">${F.map((f, i) => `<li class="o04__stap"><div class="o04__beeld">${img(FIG[i].src, `o04__figuur ${FIG[i].cls}`, ' aria-hidden="true"')}<span class="o04__no">${nr2(i)}</span></div><h3>${f.titel}</h3><p>${f.tekst}</p></li>`).join('')}</ol>
  <div class="o04__paneel">
    <div class="o04__paneeltekst"><p class="o04__slot">${T.slot}</p>${soorten('o04__soorten')}</div>
    <div class="o04__tegels">${D.map((d, i) => `<div class="o04__tegel">${obj(VAK_OBJ[i])}<h3>${d.titel}</h3><p>${d.tekst}</p></div>`).join(of('o04__of'))}</div>
  </div>
</div>`));

  add('05', 'Zes kaarten, de zesde uitgelicht', 'Referentie B · /bedrijven/ .sgdp-kaarten + .sgdp-kaart + .sgdp-kaart--uitgelicht ("Wat levert zonnestroom je bedrijf op?") en .kerncijfers',
    'Het voordelenblok van /bedrijven/ op een zachte gele grond: zes kaarten in drie kolommen. De vijf factoren hebben elk een echte foto als tegel linksboven (in plaats van de klei-iconen van de referentie), de zesde kaart is uitgelicht in Goudgeel en draagt All-in prijs of Regieprijs. Daaronder de kerncijferbalk van dezelfde pagina: de slottekst, Geen voorrijkosten (bakwagen) en Betalen op de verhuisdag (munten).',
    v => sec(v, 'wit', `<div class="wrap">
  ${kop(v, 'o05__kop')}
  <ul class="o05__kaarten">${F.map((f, i) => `<li class="o05__kaart"><span class="o05__foto">${foto(i)}</span><span class="o05__nr" aria-hidden="true">${nr2(i)}</span><h3>${f.titel}</h3><p>${f.tekst}</p></li>`).join('')}<li class="o05__kaart o05__kaart--uitgelicht">${D.map((d, i) => `<div class="o05__prijs">${obj(VAK_OBJ[i])}<div><h3>${d.titel}</h3><p>${d.tekst}</p></div></div>`).join(of('o05__of'))}</li></ul>
  <div class="o05__cijfers"><p class="o05__slot">${T.slot}</p>${S.map((s, i) => `<div class="o05__cijfer">${obj(SOORT_OBJ[i])}<div><h3>${s.titel}</h3><p>${s.tekst}</p></div></div>`).join('')}</div>
</div>`, 'o05--zacht'));

  add('06', 'De ploeg op het podium, gele band eronder', 'Referentie B · /bedrijven/ .sgteam + .sgteam__feiten + .sgteam__podium + .sgteam__cta ("Eigen monteurs, eigen voorraad, eigen pand")',
    'Het teamblok van /bedrijven/: links de kop en de vijf factoren als gestapelde witte kaartjes met een ronde foto, rechts drie De Reus-verhuizers met dozen op twee platen (achter Koningsblauw verloop, voor lichtblauw); hun hoofden komen boven de voorste plaat uit. Daaronder de Goudgele band van hetzelfde blok met All-in prijs of Regieprijs, de slottekst en de twee zekerheden als witte knoppen met echt voorwerp.',
    v => sec(v, 'wit', `<div class="wrap">
  <div class="o06__rij">
    <div>${kop(v, 'o06__kop')}<h3 class="lijstkop">${T.lijstkop}</h3><ol class="o06__feiten">${F.map((f, i) => `<li><span class="o06__foto">${foto(i)}</span><div><h3>${f.titel}</h3><p>${f.tekst}</p></div></li>`).join('')}</ol></div>
    <div class="o06__podium" aria-hidden="true"><span class="o06__stapel"></span>${img('/img/team/team-hero-dozen-1100.webp', 'o06__team')}</div>
  </div>
  <div class="o06__cta">
    <div class="o06__duo">${D.map(d => `<div class="o06__prijs"><h3>${d.titel}</h3><p>${d.tekst}</p></div>`).join(of('o06__of'))}</div>
    <p class="o06__slot">${T.slot}</p>
    ${soorten('o06__knoppen', { obj: true })}
  </div>
</div>`));

  const P7 = { foto: '/img/dienst-nationaal-v2-groot.webp', uit: '/img/dienst-nationaal-v2-uit.webp', ar: 4 / 3, top: .35, d0: .27, mid: .56 };
  add('07', 'De prijskaart', 'Referentie B · .sgpr + .sgpr-rij + .sgpr-rij--uitgelicht + .sgpr__beeld + .sgpr__boven ("Vaste vanafprijzen, inclusief installatie")',
    'Het prijzenblok van referentie B, zonder bedragen want die staan niet op de site: een witte kaart met links de kop, de twee prijsvormen als prijsrijen (All-in uitgelicht, met het klembord en de wekker waar bij de referentie het bedrag staat), de vijf factoren en de slottekst als voetregel. Rechts de foto van de verhuizer met de doos; zijn hoofd steekt boven de kaart uit (dezelfde rekensom als .sgpr__boven), en daaronder het Goudgele vlak met de twee zekerheden.',
    v => sec(v, 'mist', `<div class="wrap">
  <div class="o07__kaart">
    <div class="o07__body">
      ${kop(v)}
      <div class="o07__rijen">${D.map((d, i) => `<div class="o07-rij${i === 0 ? ' o07-rij--uitgelicht' : ''}"><div><h3>${d.titel}</h3><p>${d.tekst}</p></div>${obj(VAK_OBJ[i])}</div>`).join(of('o07__of'))}</div>
      <h3 class="lijstkop">${T.lijstkop}</h3>
      <ol class="o07__factoren">${F.map((f, i) => `<li><span class="o07__nr" aria-hidden="true">${nr2(i)}</span><div><h3>${f.titel}</h3><p>${f.tekst}</p></div></li>`).join('')}</ol>
      <p class="o07__voet">${T.slot}</p>
    </div>
    <div class="o07__media">
      ${pop(P7, 'o07__beeld')}
      <div class="o07__badge">${S.map((s, i) => `<div>${obj(SOORT_OBJ[i])}<h3>${s.titel}</h3><p>${s.tekst}</p></div>`).join('')}</div>
    </div>
  </div>
</div>`));

  // ================= referentie C =================

  add('08', 'Foto met oplopende kaarten en de boog', 'Referentie C · .b-maten + .b-maten__podium + .b-maten__boog + .b-maten__maten ("Even geen plek? Wij bewaren het")',
    'Het opslagblok van referentie C: kop in twee kolommen (links titel en de twee zekerheden met gele ruitjes, rechts de inleiding met All-in prijs of Regieprijs), daaronder een brede foto van een lege kamer met dozen, met het wit label "Wat de prijs bepaalt" en de vijf factoren als kaarten die over de onderrand van de foto oplopen, van wit naar Diepblauw. Rechts staat de oudere verhuizer met de doos in een Koningsblauwe boog met gele lijn. De slottekst staat als noot onder de kaarten.',
    v => sec(v, 'lucht', `<div class="wrap">
  <div class="o08__kop">
    <div class="o08__titel"><p class="label">${T.label}</p><h2 class="h2" id="${kid(v)}">${T.h2}</h2></div>
    <p class="o08__lead">${T.intro}</p>
    ${soorten('o08__feiten')}
    <div class="o08__keuze">${D.map((d, i) => `<div class="o08__prijs">${obj(VAK_OBJ[i])}<div><h3>${d.titel}</h3><p>${d.tekst}</p></div></div>`).join(of('o08__of'))}</div>
  </div>
  <div class="o08__beeld">
    <div class="o08__podium">
      <figure class="o08__foto">${img('/img/headers/home.webp', 'o08__fotoimg')}</figure>
      <span class="o08__boog" aria-hidden="true"></span>${img(EIGEN + 'verhuizer-doos.webp', 'o08__verhuizer', ' aria-hidden="true"')}
      <p class="o08__vraag">${T.lijstkop}</p>
    </div>
    <div class="o08__schaal">
      <ol class="o08__maten">${F.map((f, i) => `<li class="o08__maat o08__maat--${i + 1}"><p class="o08__getal" aria-hidden="true"><b>${nr2(i)}</b></p><div><h3>${f.titel}</h3><p>${f.tekst}</p></div></li>`).join('')}</ol>
      <p class="o08__noot">${T.slot}</p>
    </div>
  </div>
</div>`));

  add('09', 'Het keurmerkvel met zijkolom', 'Referentie C · .b-certificaat + .b-certificaat__top + .b-certificaat__wagen + .b-certificaat__map + .b-certificaat__hoofd ("Uw verhuizing gegarandeerd")',
    'Het certificaatblok van referentie C: kop links met de echte bakwagen rechts ernaast, daaronder een wit vel met een Diepblauwe kop (logo, gele onderrand), de vijf factoren genummerd in twee kolommen, de twee zekerheden en de slottekst als bronregel. Rechts de zijkolom: een foto met een schuine onderkant en een Koningsblauw-naar-Diepblauw paneel met All-in prijs of Regieprijs, elk met zijn voorwerp.',
    v => sec(v, 'wit', `<div class="wrap">
  <div class="o09__top">${kop(v, 'o09__kop')}<figure class="o09__wagen">${obj('bakwagen')}</figure></div>
  <div class="o09__map">
    <div class="o09__vel">
      <div class="o09__hoofd">${img('/img/logo/dereus-logo-negatief.svg', 'o09__logo', ' aria-hidden="true"')}<h3 class="o09__titel">${T.lijstkop}</h3></div>
      <ol class="o09__lijst">${F.map((f, i) => `<li><span class="o09__nr" aria-hidden="true">${nr2(i)}</span><div><h3>${f.titel}</h3><p>${f.tekst}</p></div></li>`).join('')}</ol>
      ${soorten('o09__soorten')}
      <p class="o09__bron">${T.slot}</p>
    </div>
    <aside class="o09__zij" aria-label="${D[0].titel} of ${D[1].titel}">
      <figure class="o09__foto">${img('/img/verhuisdag-uitladen.webp', '')}</figure>
      <div class="o09__paneel">
        ${D.map((d, i) => `<div class="o09__prijs">${obj(VAK_OBJ[i])}<h3>${d.titel}</h3><p>${d.tekst}</p></div>`).join(of('o09__of'))}
      </div>
    </aside>
  </div>
</div>`));

  add('10', 'Het klembord met de vijf punten', 'Referentie C · .b-checklist + .b-checklist__beeld + .b-checklist__bord + .b-checklist__punt ("Hoe eerder de datum vastligt, hoe rustiger")',
    'Het checklistblok van referentie C: links de kop en een foto op een schuine Koningsblauwe band, daaronder All-in prijs of Regieprijs als twee platen. Rechts een klembord (Diepblauwe achterplaat, witte vel, klem met het beeldmerk) met "Wat de prijs bepaalt" en de vijf factoren als afgevinkte punten; onderaan het vel de slottekst, want daar vraagt de tekst om alles vooraf te melden, en de twee zekerheden.',
    v => sec(v, 'wit', `<div class="wrap o10__in">
  <div class="o10__links">
    ${kop(v)}
    <figure class="o10__beeld">${img('/img/verhuisdag-aankomst.webp', '')}</figure>
    <div class="o10__duo">${D.map((d, i) => `<div class="o10__prijs${i === 0 ? ' o10__prijs--blauw' : ''}">${obj(VAK_OBJ[i])}<div><h3>${d.titel}</h3><p>${d.tekst}</p></div></div>`).join(of('o10__of'))}</div>
  </div>
  <div class="o10__bord">
    <h3 class="o10__titel">${T.lijstkop}</h3>
    <ol class="o10__lijst">${F.map(f => `<li class="o10__punt">${vink()}<div><b>${f.titel}</b><span>${f.tekst}</span></div></li>`).join('')}</ol>
    <p class="o10__voet">${T.slot}</p>
    ${soorten('o10__soorten')}
  </div>
</div>`));
};
