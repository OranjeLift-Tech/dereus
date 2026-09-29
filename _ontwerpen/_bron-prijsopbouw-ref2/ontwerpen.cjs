// De tien ontwerpen van ronde 5. Elk ontwerp is de opbouw van een echt blok (bronklasse in het bijschrift), met de
// teksten van /kosten/ #opbouw, De Reus-tokens en eigen klassen .pNN (CSS in var.css).
module.exports = ({ add, T, TEL, img, ic, nr2, P, FAC, SNEDE, pop, rond, obj, VAK_OBJ, SOORT_OBJ, EIGEN }) => {
  const F = T.factoren, D = T.vakken, S = T.soorten;
  const kid = v => `kop-p${v}`;
  const h2 = (v, o = {}) => `<h2 class="h2" id="${kid(v)}">${o.accent ? T.h2.replace('prijs', '<span class="accent">prijs</span>') : T.h2}</h2>`;
  const kop = (v, cls = '', o = {}) => `<div class="kopgroep ${cls}"><p class="label">${T.label}</p>${h2(v, o)}${o.geenIntro ? '' : `<p class="intro">${T.intro}</p>`}</div>`;
  const sec = (v, cls, inner) => `<section class="v p${v} ${cls}" aria-labelledby="${kid(v)}">\n${inner}\n</section>`;
  const of = (cls = '') => `<span class="of ${cls}" aria-hidden="true">${T.of}</span>`;
  const schijf = (i, cls = '') => `<span class="schijf ${cls}" aria-hidden="true">${nr2(i)}</span>`;
  const vink = () => `<span class="vink" aria-hidden="true">${ic('check')}</span>`;
  const lijstkop = (cls = '') => `<h3 class="lijstkop ${cls}">${T.lijstkop}</h3>`;
  const soorten = (cls, o = {}) => `<ul class="${cls}">${S.map((s, i) => `<li>${o.obj ? obj(SOORT_OBJ[i]) : vink()}<div><h3>${s.titel}</h3><p>${s.tekst}</p></div></li>`).join('')}</ul>`;
  // All-in prijs of Regieprijs, elk met zijn voorwerp; de "of"-schijf staat los (absoluut) tussen de twee
  const duo = (cls, extra = ['', '']) => `<div class="${cls}">${D.map((d, i) => `<div class="${cls}__vak ${extra[i]}">${obj(VAK_OBJ[i])}<h3>${d.titel}</h3><p>${d.tekst}</p></div>`).join(of(`${cls}__of`))}</div>`;
  const fotoImg = (i, cls = '') => img(FAC[i].foto, cls, ` style="object-position:${SNEDE[i]}"`);

  // ================= referentie C =================

  add('01', "Vijf foto's op de lijn", 'Referentie C · .b-historie + .b-historie__tl + .b-historie__plaat + .b-historie__jaar ("Van paard en wagen in 1923 tot uw verhuizing van nu")',
    'Het historieblok op de Koningsblauwe band met dakrand: vijf scheefgezette fotoplaten op een rij, en in elke foto stappen de verhuizers met hun hoofd boven het kader uit (dozen, de wagen, de verhuislift, de boormachine, de opslag). Onder de platen een lijn met gele nummerschijven en witte plusjes: de vijf tellen op. Het "="-teken leidt naar een witte plaat met All-in prijs of Regieprijs, waar het klembord en de wekker bovenuit steken, met de slottekst als voet. Daaronder de twee zekerheden met de bakwagen en de munten.',
    v => sec(v, 'sectie sectie--blauw', `<div class="wrap">
  ${kop(v, 'p01__kop')}
  ${lijstkop('p01__lijstkop')}
  <ol class="p01__tl">${F.map((f, i) => `<li class="p01__stap"><figure class="p01__fig">${pop(FAC[i], 'p01__pop')}</figure>${schijf(i, 'p01__nr')}<h3>${f.titel}</h3><p>${f.tekst}</p></li>`).join('')}</ol>
  <div class="p01__uitkomst">
    <span class="p01__is" aria-hidden="true">=</span>
    <div class="p01__plaat">${duo('p01__duo')}<p class="p01__slot">${T.slot}</p></div>
    ${soorten('p01__soorten', { obj: true })}
  </div>
</div>`));

  add('02', 'Prijskaartjes aan de rail', 'Referentie C · .b-belofte + .b-belofte__band + .b-belofte__kaart + .b-belofte__haak (het belofteblok op de homepage)',
    'Het belofteblok: een Goudgele rail over de volle breedte, met aan haken vijf scheef hangende kaartjes, elk met een foto, een gele nummerschijf, titel en uitleg. Achter de onderste helft loopt een schuine lichtblauwe baan. Onder het "="-teken een kortere rail met de twee grote kaartjes: All-in prijs (Goudgeel, klembord) of Regieprijs (wit, wekker). Beweeg de muis over een kaartje en het hangt recht.',
    v => sec(v, 'sectie sectie--wit', `<div class="wrap">${kop(v, 'p02__kop')}${lijstkop('p02__lijstkop')}</div>
<div class="p02__baan">
  <span class="p02__band" aria-hidden="true"></span>
  <div class="wrap"><ol class="p02__lijst">${F.map((f, i) => `<li class="p02__kaart"><span class="p02__haak" aria-hidden="true"></span><figure class="p02__foto">${fotoImg(i)}</figure>${schijf(i, 'p02__nr')}<h3>${f.titel}</h3><p>${f.tekst}</p></li>`).join('')}</ol></div>
</div>
<div class="wrap p02__onder">
  <span class="p02__is" aria-hidden="true">=</span>
  <div class="p02__baan2"><span class="p02__band p02__band--kort" aria-hidden="true"></span>
    <div class="p02__duo">${D.map((d, i) => `<div class="p02__tag${i === 0 ? ' p02__tag--geel' : ''}"><span class="p02__haak" aria-hidden="true"></span>${obj(VAK_OBJ[i])}<h3>${d.titel}</h3><p>${d.tekst}</p></div>`).join(of('p02__of'))}</div>
  </div>
  <p class="p02__slot">${T.slot}</p>
  ${soorten('p02__soorten', { obj: true })}
</div>`));

  add('03', 'De verhuizers en de stapel dozen', 'Referentie C · .b-doos + .b-doos__paneel + .b-doos__lijst + .b-doos__etiket + .b-doos__dozen + .b-doos__keuze ("Zoveel of zo weinig als u wilt")',
    'Het dozenblok: links de kop en de vijf factoren met gele nummerblokjes, rechts de foto met de twee verhuizers en de logodoos, schuin afgesneden aan de linkerkant; hun hoofden steken boven de foto uit. Achter de foto een Goudgeel vlak tot de schermrand, linksonder het witte etiket met het logo en het nummer, rechtsonder de echte stapel De Reus-dozen. Onder een dikke lijn de keuze: links de slottekst, rechts All-in prijs, Regieprijs en de twee zekerheden als regels met plusjes.',
    v => sec(v, 'sectie sectie--wit', `<div class="wrap p03__in">
  <div class="p03__tekst">
    ${kop(v, 'p03__kop', { accent: true })}
    ${lijstkop('p03__lijstkop')}
    <ol class="p03__factoren">${F.map((f, i) => `<li>${schijf(i, 'p03__nr')}<div><h3>${f.titel}</h3><p>${f.tekst}</p></div></li>`).join('')}</ol>
  </div>
  <div class="p03__beeld">
    <span class="p03__paneel" aria-hidden="true"></span>
    ${rond(P.dozen, [.21, .235, 1, 1], 'p03__foto rond--schuin')}
    <p class="p03__etiket" aria-hidden="true">${img('/img/logo/dereus-logo.svg', 'p03__logo')}<span class="p03__tel">${TEL}</span></p>
    ${obj('dozen', 'p03__dozen')}
  </div>
  <div class="p03__keuze">
    <p class="p03__uitleg">${T.slot}</p>
    <dl class="p03__menu">${D.map((d, i) => `<div class="p03__regel"><dt>${obj(VAK_OBJ[i])}<span>${d.titel}</span></dt><dd>${d.tekst}</dd></div>`).join(`<div class="p03__ofrij" aria-hidden="true">${of('p03__of')}</div>`)}<div class="p03__regel p03__regel--extra"><dt><span>&nbsp;</span></dt><dd><ul class="p03__extra">${S.map(s => `<li><h3>${s.titel}</h3> <span>${s.tekst}</span></li>`).join('')}</ul></dd></div></dl>
  </div>
</div>`));

  // ================= referentie A =================

  add('04', 'De ploeg op de schuine band', 'Referentie A · .opslag + .opslag__band + .opslag__lijn + .opslag__kaart + .opslag__persoon ("Even geen plek? Wij slaan uw inboedel op")',
    'Het opslagblok: een schuine Koningsblauwe band met een gele lijn erboven en een Diepblauwe streep eronder, het logo als watermerk erin. Links staat de Diepblauwe kaart met de kop en de vijf factoren met gele schijven, rechts staan drie De Reus-verhuizers met dozen en een deken levensgroot op de band. Onder de band All-in prijs of Regieprijs als twee dikke platen met het klembord en de wekker, de slottekst en de twee zekerheden.',
    v => sec(v, 'sectie sectie--wit', `<div class="p04__top">
  <div class="p04__band" aria-hidden="true">${img('/img/logo/dereus-beeldmerk-negatief.svg', 'p04__mark')}${img('/img/logo/dereus-logo-horizontaal-negatief.svg', 'p04__script')}</div>
  <div class="p04__lijn" aria-hidden="true"></div>
  <div class="wrap p04__in">
    <div class="p04__kaart">
      ${kop(v, 'p04__kop')}
      ${lijstkop('p04__lijstkop')}
      <ol class="p04__factoren">${F.map((f, i) => `<li>${schijf(i, 'p04__nr')}<div><h3>${f.titel}</h3><p>${f.tekst}</p></div></li>`).join('')}</ol>
    </div>
    <div class="p04__fig" aria-hidden="true">${img('/img/team/team-hero-dozen-1100.webp', 'p04__ploeg')}</div>
  </div>
</div>
<div class="wrap p04__onder">
  ${duo('p04__duo', ['p04__duo__vak--blauw', ''])}
  <p class="p04__slot">${T.slot}</p>
  ${soorten('p04__soorten', { obj: true })}
</div>`));

  add('05', 'Het team achter de prijsbalie', 'Referentie A · .venster + .venster__boog + .venster__persoon + .venster__mark ("Benieuwd naar de kosten? Vraag vandaag nog een offerte aan")',
    'Het vensterblok op een Goudgele band met dakrand: rechts staat het huis uit het logo als wit venster met een Diepblauwe binnenlijn, en daarvoor drie lachende De Reus-verhuizers. Links de kop en de vijf factoren als lichte plaatjes met Diepblauwe schijven. Een witte balie schuift voor de verhuizers langs: daarop staan All-in prijs en Regieprijs met het klembord en de wekker, en de slottekst als voet. Daaronder de twee zekerheden als Diepblauwe pillen.',
    v => sec(v, 'band-geel', `${img('/img/logo/dereus-beeldmerk.svg', 'p05__mark', ' aria-hidden="true"')}
<div class="wrap">
  <div class="p05__in">
    <div class="p05__tekst">
      ${kop(v, 'p05__kop')}
      ${lijstkop('p05__lijstkop')}
      <ol class="p05__factoren">${F.map((f, i) => `<li>${schijf(i, 'p05__nr')}<div><h3>${f.titel}</h3><p>${f.tekst}</p></div></li>`).join('')}</ol>
    </div>
    <div class="p05__fig" aria-hidden="true">
      <svg class="p05__huis" viewBox="0 0 535.3 509.8" focusable="false"><path fill="#fff" d="M267.6 7.8L320.9 53.2V0H356.8V83.9L535.3 236.2H457.6V509.8H326.2V384.1H209.1V509.8H77.7V236.2H0Z"/><path fill="none" stroke="#0B2352" stroke-width="3" vector-effect="non-scaling-stroke" transform="translate(29.4 36) scale(.89)" d="M267.6 7.8L320.9 53.2V0H356.8V83.9L535.3 236.2H457.6V509.8H326.2V384.1H209.1V509.8H77.7V236.2H0Z"/></svg>
      ${img('/img/review-verhuizers-lachend-breed.webp', 'p05__ploeg')}
    </div>
  </div>
  <div class="p05__balie">${duo('p05__duo')}<p class="p05__slot">${T.slot}</p></div>
  ${soorten('p05__soorten', { obj: true })}
</div>`));

  add('06', 'De prijskaart met de wagen erop', 'Referentie A · .zeker + .zeker__card + .zeker__head + .zeker__logo + .zeker__list + .zeker__houder ("Acht zekerheden die in de prijs zitten")',
    'Het zekerheidsblok: een grote Diepblauwe kaart met de driekleurige streep bovenaan, links het logo, dan de kop, en rechts rijdt de echte De Reus-bakwagen over de bovenrand van de kaart. De vijf factoren staan in twee kolommen met gele schijven, daaronder All-in prijs (Goudgele plaat) of Regieprijs (witte plaat) met het klembord en de wekker die bovenuit steken, dan de twee zekerheden als kaders met een gele rand, en de slottekst als voetregel.',
    v => sec(v, 'sectie sectie--lucht', `<div class="wrap">
  <div class="p06__kaart">
    ${obj('bakwagen', 'p06__wagen')}<span class="p06__grond" aria-hidden="true"></span>
    <div class="p06__head">
      ${img('/img/logo/dereus-logo-negatief.svg', 'p06__logo', ' aria-hidden="true"')}
      ${kop(v, 'p06__intro')}
    </div>
    ${lijstkop('p06__lijstkop')}
    <ol class="p06__list">${F.map((f, i) => `<li>${schijf(i, 'p06__nr')}<div><h3>${f.titel}</h3><p>${f.tekst}</p></div></li>`).join('')}</ol>
    ${duo('p06__duo', ['p06__duo__vak--geel', ''])}
    <ul class="p06__houders">${S.map(s => `<li><h3>${s.titel}</h3><p>${s.tekst}</p></li>`).join('')}</ul>
    <p class="p06__bron">${T.slot}</p>
  </div>
</div>`));

  // ================= referentie B =================

  add('07', 'De gele plaat met twee afdrukken', 'Referentie B · .sgt + .sgt__paneel + .sgt__fotos + .sgt__team + .sgt__pand + .sgt__knoppen (het blok over het team en het pand op de homepage)',
    'Het blok van de gele plaat: links de kop en twee scheve foto-afdrukken met een wit randje en een label, "All-in prijs" (de handtekening onder de offerte) en "Regieprijs" (uitladen op de verhuisdag); uit de hoek van de ene afdruk steekt het klembord, uit de andere de wekker, met een Diepblauwe "of"-schijf ertussen. Daaronder de twee zekerheden als knoppen met de bakwagen en de munten. Rechts de inleiding vet, de vijf factoren als lichte regels met Diepblauwe blokjes en de slottekst.',
    v => sec(v, 'sectie sectie--mist', `<div class="wrap">
  <div class="p07__paneel">
    <div class="p07__links">
      <p class="label">${T.label}</p>${h2(v)}
      <div class="p07__fotos">
        <figure class="p07__print p07__print--1">${img('/img/stap-3-offerte.webp', 'p07__img')}<figcaption aria-hidden="true">${D[0].titel}</figcaption>${obj(VAK_OBJ[0], 'p07__obj')}</figure>
        ${of('p07__of')}
        <figure class="p07__print p07__print--2">${img('/img/verhuisdag-uitladen.webp', 'p07__img')}<figcaption aria-hidden="true">${D[1].titel}</figcaption>${obj(VAK_OBJ[1], 'p07__obj')}</figure>
      </div>
      <div class="p07__onderschrift">${D.map(d => `<div><h3>${d.titel}</h3><p>${d.tekst}</p></div>`).join('')}</div>
      ${soorten('p07__knoppen', { obj: true })}
    </div>
    <div class="p07__rechts">
      <p class="p07__lead">${T.intro}</p>
      ${lijstkop('p07__lijstkop')}
      <ol class="p07__factoren">${F.map((f, i) => `<li>${schijf(i, 'p07__nr')}<div><h3>${f.titel}</h3><p>${f.tekst}</p></div></li>`).join('')}</ol>
      <p class="p07__slot">${T.slot}</p>
    </div>
  </div>
</div>`));

  add('08', 'Zes kaarten, de verhuizers stappen eruit', 'Referentie B · .sgd1 + .sgd1-grid + .sgd1-kaart + .sgd1-pop + .sgd1-ico ("Waarmee wij je helpen")',
    'Het dienstenblok op een lichtgele band met dakrand: zes kaarten in twee rijen. In de vijf factorkaarten stappen de verhuizers met hoofd en schouders boven de kaart uit, met een gele nummerschijf op de naad tussen foto en tekst. De zesde kaart is Diepblauw: daar staan het klembord en de wekker boven op een Goudgeel vlak met de "of"-schijf ertussen, en eronder All-in prijs en Regieprijs. Onder de kaarten de slottekst en de twee zekerheden.',
    v => sec(v, 'band-licht', `<div class="wrap">
  ${kop(v, 'p08__kop')}
  ${lijstkop('p08__lijstkop')}
  <ul class="p08__grid">${F.map((f, i) => `<li class="p08__kaart"><div class="p08__beeld">${pop(FAC[i], 'p08__pop')}${schijf(i, 'p08__nr')}</div><div class="p08__tekst"><h3>${f.titel}</h3><p>${f.tekst}</p></div></li>`).join('')}<li class="p08__kaart p08__kaart--prijs"><div class="p08__beeld p08__beeld--prijs" aria-hidden="true">${obj(VAK_OBJ[0], 'p08__obj p08__obj--1')}${of('p08__of')}${obj(VAK_OBJ[1], 'p08__obj p08__obj--2')}</div><div class="p08__tekst p08__tekst--duo">${D.map(d => `<div><h3>${d.titel}</h3><p>${d.tekst}</p></div>`).join('')}</div></li></ul>
  <div class="p08__meer"><p class="p08__slot">${T.slot}</p>${soorten('p08__soorten', { obj: true })}</div>
</div>`));

  add('09', 'Gekleurde tegels en de verhuizer ernaast', 'Referentie B · .sgw + .sgw-rij + .sgw-tegels + .sgw-tegel + .sgw-foto + .sgw-foto__uit ("Jouw regionale partner in duurzame energie")',
    'Het waaromblok: links vijf tegels in de merkkleuren (Diepblauw, Goudgeel, lichtblauw, Koningsblauw, Crème), elk met een ronde foto en een nummer; rechts de grote foto van de wagen, waar de verhuizer met zijn doos en zijn collega in de wagen met hun hoofd bovenuit komen. Daaronder All-in prijs (Diepblauw) of Regieprijs (Goudgeel) als twee dikke platen met het klembord en de wekker, de slottekst en de twee zekerheden.',
    v => sec(v, 'sectie sectie--wit', `<div class="wrap">
  ${kop(v, 'p09__kop')}
  <div class="p09__rij">
    <div class="p09__links">${lijstkop('p09__lijstkop')}<ol class="p09__tegels">${F.map((f, i) => `<li class="p09__tegel p09__tegel--${i + 1}"><span class="p09__med">${fotoImg(i)}</span><h3><span class="p09__nr" aria-hidden="true">${nr2(i)}</span>${f.titel}</h3><p>${f.tekst}</p></li>`).join('')}</ol></div>
    <figure class="p09__foto">${pop(P.afstandGroot, 'p09__pop')}</figure>
  </div>
  ${duo('p09__duo', ['p09__duo__vak--blauw', 'p09__duo__vak--geel'])}
  <p class="p09__slot">${T.slot}</p>
  ${soorten('p09__soorten', { obj: true })}
</div>`));

  add('10', 'Blauwe band met de verhuizer op de naad', 'Referentie B · /bedrijven/ .sgdp-hero + .sgdp-hero__band + .sgdp-hero__foto + .sgdp-hero__figuur ("Zonnepanelen op maat voor bedrijven")',
    'De kop van /bedrijven/ als band: links Koningsblauw met de kop, de inleiding en All-in prijs of Regieprijs als twee witte platen met het klembord en de wekker; rechts de echte De Reus-bakwagen in de straat tot de schermrand, schuin aangesneden, en op de naad staat de verhuizer met zijn doos. De vijf factoren schuiven als dikke witte platen over de onderrand van de band, en ook daar stappen de verhuizers met hun hoofd uit de foto. Daaronder de slottekst en de twee zekerheden.',
    v => sec(v, '', `<div class="p10__band">
  ${img('/img/footer-wagen-breed.webp', 'p10__foto', ' aria-hidden="true"')}
  ${img(EIGEN + 'verhuizer-doos.webp', 'p10__figuur', ' aria-hidden="true"')}
  <div class="wrap p10__tekst">
    <p class="label">${T.label}</p>
    ${h2(v, { accent: true })}
    <p class="p10__lead">${T.intro}</p>
    ${duo('p10__duo')}
    ${lijstkop('p10__lijstkop')}
  </div>
</div>
<div class="wrap">
  <ol class="p10__factoren">${F.map((f, i) => `<li class="p10__plaat">${pop(FAC[i], 'p10__pop')}${schijf(i, 'p10__nr')}<h3>${f.titel}</h3><p>${f.tekst}</p></li>`).join('')}</ol>
  <p class="p10__slot">${T.slot}</p>
  ${soorten('p10__soorten', { obj: true })}
</div>`));
};
