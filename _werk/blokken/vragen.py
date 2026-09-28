"""Veelgestelde vragen (#vragen): links de kop, de belregel en de bereikbaarheid (plakt mee), rechts de
vragen als details/summary, genummerd. Werkt zonder JS. De FAQPage in de JSON-LD (jsonld.py, dereus-e7)
leest hetzelfde blok, dus wat hier staat, staat ook daar.

Antwoorden mogen als tekst:-veld of als losse alinea's onder de ###-vraag staan.
Opties: sectie ("mist" standaard, of "wit"), open (nummer van de vraag die open staat, standaard geen),
kopkaart (zet de kop IN de belkaart in plaats van erboven), foto (een vrijstaande verhuizer rechts in
die kaart), stijl ("paneel" voor de blauwe paneelopmaak, "geel" voor de Goudgele band met foto-afdruk, met
afdruk= uit AFDRUK; sectie, beeld, kopkaart, vulling en werker doen dan niets), vulling (standaard aan: de
vraagtekens (klei-icoon) in het blauwe paneel, zie VULLING; zonder paneel blijft het vak onzichtbaar) en
werker (standaard aan in het paneel met kopkaart en zonder foto: een verhuizer rechtsonder in het paneel,
zie WERKER; False zet hem uit, een naam uit WERKER kiest een andere uitsnede).
Live staat het paneel met de verhuizer (/, /werkwijze/, /kosten/, /contact/). "geel" is de versie van Tugche
(origin/main 9dbb9a8, 28-09-2026) voor /contact/ en /werkwijze/; die staat als regel in de paginabestanden.
Er staat hoogstens een vraag tegelijk open: de <details> van een blok delen een name, dus de browser klapt
de vorige dicht zodra er een andere opengaat. Geen JS; een browser zonder die name laat ze gewoon openstaan. Die laatste twee horen bij elkaar: zonder kopkaart staat de foto in een kaart die er te laag
voor is. Standaard staan ze uit, dus de pagina's die ze niet vragen veranderen geen byte.
"""
NAAM = "vragen"
CSS = True
JS = False

# Optie beeld: een voorwerp uit de 3D-reeks. Naam -> bron, breedte, hoogte, behandeling.
#   "steekt-uit" (/contact/): de uitsnede steekt rechtsboven uit het Diepblauwe paneel. Absoluut geplaatst,
#     dus de plek in de markup doet er niet toe en hij staat vóór de kopgroep.
#   "vult-gat" (home): het voorwerp staat vóór het goudgele huis uit het logo en vult als flexkind de vrije
#     hoogte tussen de kop en de belkaart. Die plek in de markup is hier wél de plek op het scherm, dus het
#     staat tussen de kopgroep en de belkaart in.
# Vormgeving: onderaan css/blok/vragen.css.
# Sinds 28-09-2026 het klei-icoon (img/clay/, vierkant, 240 en 480 via srcset) in plaats van de 3D-render.
BEELDEN = {
    "headset": ("/img/clay/headset-240.webp", 240, 240, "steekt-uit"),
    "headset-huis": ("/img/clay/headset-240.webp", 240, 240, "vult-gat"),
    "headset-hoek": ("/img/clay/headset-240.webp", 240, 240, "hoek"),
}


def _srcset(src, sizes):
    """Voor een klei-icoon (img/clay/<naam>-240.webp) de 480 ernaast; andere beelden krijgen niets."""
    if not src.startswith("/img/clay/") or not src.endswith("-240.webp"):
        return ""
    return f' srcset="{src} 240w, {src[:-9]}-480.webp 480w" sizes="{sizes}"'

#   "hoek" (home, met kopkaart): het voorwerp hangt op de rechterbovenhoek van de belkaart en steekt
#     er een stukje uit. Het hoort dan IN die kaart te staan, want het is daar absoluut geplaatst.
#     Deze behandeling heeft kopkaart nodig; zonder kopkaart is de kaart te laag en hangt het
#     voorwerp over de vragen heen.

# Optie foto: een vrijstaande verhuizer rechts in de belkaart. Naam -> bron, breedte, hoogte, alt.
# De uitsneden staan in img/ en komen uit de ronde verhuizer-uitsnede van 23-09; ze zijn met rembg
# (isnet-general-use) van het studiodoek gehaald, net als het herotrio.
# Let op bij het kiezen: alle vier dragen een WITTE doos, en de belkaart is wit. Wat die doos op een
# witte kaart nog leesbaar maakt is het gedrukte merk erop, niet de omtrek. "twee-dozen" heeft het
# merk het grootst en het meest frontaal in beeld en is met 407x1200 ook de smalste, dus die houdt
# zich het best in een smalle kolom naast de tekst.
FOTOS = {
    "twee-dozen": ("/img/verhuizer-twee-dozen-uit.webp", 407, 1200,
                   "Verhuizer van De Reus met twee verhuisdozen"),
    "doos-schouder": ("/img/verhuizer-doos-schouder-uit.webp", 489, 1200,
                      "Verhuizer van De Reus met een verhuisdoos op zijn schouder"),
    "steekwagen": ("/img/verhuizer-steekwagen-uit.webp", 734, 1200,
                   "Verhuizer van De Reus met een steekwagen vol verhuisdozen"),
    "doos-deken": ("/img/verhuizer-doos-deken-uit.webp", 698, 1200,
                   "Verhuizer van De Reus met een verhuisdeken en een verhuisdoos"),
}


# Optie vulling: het paneel is sinds 23-09 even hoog als de vragenlijst ernaast (vraag van de gebruiker:
# "make the blue block be the same height as the question block ... and add image to the empty space
# to fill, something without background"). De vrije hoogte die dat oplevert verschilt per pagina, dus
# het beeld staat in een vak dat precies die hoogte krijgt en zich erin schikt; is er te weinig ruimte,
# dan blijft het weg (css/blok/vragen.css, "hoogte van het paneel"). Zonder kopkaart staat het vak
# tussen de kop en de belkaart, met kopkaart onder de kaart: dat is waar de ruimte vrijkomt.
VULLING = ("/img/clay/vraagtekens-240.webp", 240, 240)

# Optie werker (28-09-2026): gevraagd "Veelgestelde vragen - add worker cutout image te question clay icon and move
# the question icon to the left". Een vrijstaande verhuizer rechtsonder in het blauwe paneel, boven de knie
# afgesneden door de onderrand; de vraagtekens schuiven dan naar links (css/blok/vragen.css, onderaan).
# Naam -> bron, breedte, hoogte. Per pagina de uitsnede die er niet vlak naast staat: op /werkwijze/ komt
# twee-dozen direct na de vragen in #offertepil, dus daar de zijgreep. doos-schouder is dezelfde man met
# dezelfde doos als de zijgreep, en de steekwagen is te breed voor de ruimte naast de knoppen.
WERKER = {
    "twee-dozen": ("/img/verhuizer-twee-dozen-uit.webp", 407, 1200),
    "doos-zijgreep": ("/img/verhuizer-doos-zijgreep-uit.webp", 489, 1200),
}
WERKER_PAGINA = {"/werkwijze/": "doos-zijgreep"}    # de andere pagina's twee-dozen
# Het deel van de uitsnede dat boven de onderrand uitkomt: tot boven de knie, bij beide onder de dozen.
WERKER_ZICHTBAAR = .62

# Optie stijl="geel" (28-09-2026, /contact/ en /werkwijze/): ontwerp 07 uit _ontwerpen/vragen-referentie-ronde1.html,
# met op verzoek het geel over de hele sectie in plaats van als plaat in een witte sectie. Links een schuine foto-afdruk
# (naar de contactpagina van referentie B, .sgt__foto) waar de mensen bovenuit stappen, met de 3D-headset tegen de hoek; rechts de
# kop, de vragen als witte kaarten en de belrij. Vormgeving: onderaan css/blok/vragen.css, "Goudgele band".
# afdruk: naam -> foto, uitsnede (zelfde verhouding), maten, k = hoogte van de foto in afdrukhoogtes (hoe ver de
# mensen boven de lijst uitkomen), cx = waar ze horizontaal staan. Kies een foto met mensen die nog niet op de
# pagina staan: /contact/ heeft de klantenservice en de adviseur al, /werkwijze/ twee bankscènes.
# zakelijk: k 1.52 (was 1.4, gebruiker 28-09-2026: "de rechter man steekt niet echt uit"). Bij 1.4 stond zijn hoofd
# precies op de bovenrand, nu komt het er ~29 px boven; de linker man gaat mee omhoog, daarom staat de afdruk op
# /contact/ vanaf 900 px 2.25rem lager (vragen.css), anders raakt hij bij hover de band erboven.
AFDRUK = {
    "zakelijk": ("/img/dienst-zakelijk-v2.webp", "/img/dienst-zakelijk-v2-uit.webp", 720, 540, 1080, 810, "1.52", "50%"),
    "woningontruiming": ("/img/dienst-woningontruiming-v2.webp", "/img/dienst-woningontruiming-v2-uit.webp",
                         720, 540, 1080, 810, "1.26", "56%"),
}


def _geel(ctx, kid, kopgroep, vragen, bel, afdruk):
    """De Goudgele band. Eigen klassen voor alles buiten de vragen zelf: op /contact/ hangen er aan .p-contact
    paneelregels op .vragen__kop, .vragen__bel en .vragen__beeld die hier niets te zoeken hebben."""
    if afdruk not in AFDRUK:
        raise ValueError(f'vragen: onbekende afdruk "{afdruk}", kies uit {", ".join(AFDRUK)}')
    foto, uit, fb, fh, ub, uh, k, cx = AFDRUK[afdruk]
    return f'''<section class="sectie b-vragen b-vragen--geel" id="{kid}" aria-labelledby="{kid}-kop">
  <div class="wrap vragen__raster">
    <div class="vragen__fotos" aria-hidden="true">
      <span class="vragen__afdruk" style="--k:{k};--cx:{cx}"><span class="vragen__raam"><img class="vragen__afdrukfoto" src="{foto}" alt="" width="{fb}" height="{fh}" loading="lazy" decoding="async"></span><span class="vragen__boven"><img class="vragen__afdrukuit" src="{uit}" alt="" width="{ub}" height="{uh}" loading="lazy" decoding="async"></span></span>
      <img class="vragen__headset" src="/img/contact-3d/headset.webp" alt="" width="287" height="320" loading="lazy" decoding="async">
    </div>
    <div class="vragen__tekst">
      {kopgroep}
      <div class="vragen__lijst" data-reveal>
      {"".join(vragen)}
      </div>
      <div class="vragen__belrij">
        {ctx.bereikbaar("bereikbaar vragen__bereikbaar")}
        <p class="vragen__zin">{ctx.inline(bel) if bel else "Staat uw vraag er niet bij?"}</p>
        <div class="vragen__knoppen">{ctx.belknop("blauw")}</div>
      </div>
    </div>
  </div>
</section>'''


def html(ctx, kopij, sectie="mist", open=None, stijl=None, **opties):
    k = kopij
    kid = ctx.esc(k.id or "vragen")
    beeld = beeld_tussen = beeld_hoek = ""
    if opties.get("beeld") in BEELDEN:
        src, bb, bh, behandeling = BEELDEN[opties["beeld"]]
        img = (f'<img class="vragen__beeld" src="{src}"{_srcset(src, "(max-width: 899.98px) 7rem, 11rem")} alt="" width="{bb}" height="{bh}" '
               f'loading="lazy" decoding="async">')
        if behandeling == "vult-gat":
            beeld_tussen = (f'<span class="vragen__vulling" aria-hidden="true">'
                            f'<span class="vragen__huis"></span>{img}</span>')
        elif behandeling == "hoek":
            if not opties.get("kopkaart"):
                raise ValueError('vragen: beeld "hoek" hoort bij kopkaart; zonder kopkaart '
                                 'hangt het voorwerp over de vragen')
            beeld_hoek = img
        else:
            beeld = img
    vragen = []
    for i, it in enumerate(k.items, 1):
        antwoord = ctx.alineas(it.tekst) + (ctx.lijst(it.lijst, "vinklijst") if it.lijst else "")
        vragen.append(f'''<details class="vraag" id="{kid}-{i}" name="{kid}"{" open" if open == i else ""}>
        <summary><span class="vraag__nr" aria-hidden="true">{i:02d}</span><span class="vraag__tekst">{ctx.inline(it.titel)}</span><span class="vraag__plus" aria-hidden="true">{ctx.icoon("plus")}</span></summary>
        <div class="vraag__antwoord">{antwoord}</div>
      </details>''')
    bel = k.veld("belregel")
    if bel and ctx.tel in bel:
        # "Staat uw vraag er niet bij? Bel 085 000 5647." -> de vraag blijft, het nummer staat op de knop
        bel = bel.replace(f"Bel {ctx.tel}.", "").replace(f"Bel {ctx.tel}", "").replace(ctx.tel, "").strip()
    if stijl == "geel":
        return _geel(ctx, kid, ctx.kopgroep(k), vragen, bel, opties.get("afdruk", "zakelijk"))
    binnen =f'''{ctx.bereikbaar("bereikbaar vragen__status")}
        <p>{ctx.inline(bel) if bel else "Staat uw vraag er niet bij?"}</p>
        {ctx.belknop("blauw")}'''
    kopgroep = ctx.kopgroep(k)
    kopkaart = bool(opties.get("kopkaart"))
    # Het vak met de vraagtekens (VULLING). Zonder kopkaart staat het tussen de kop en de belkaart; met kopkaart
    # onder de kaart, of, als er een verhuizer in de kaart staat, onder de tekst naast hem.
    vul = ""
    if opties.get("vulling", True):
        src, vb, vh = VULLING
        vul = (f'<span class="vragen__vul" aria-hidden="true"><img class="vragen__vulbeeld" src="{src}"{_srcset(src, "12rem")} '
               f'alt="" width="{vb}" height="{vh}" loading="lazy" decoding="async"></span>')
    met_foto = opties.get("foto") in FOTOS
    vul_voor = "" if kopkaart else vul
    vul_na = vul if kopkaart and not met_foto else ""
    vul_tekst = vul if kopkaart and met_foto else ""
    if kopkaart:
        # De kop gaat de kaart IN. De foto staat op een getinte plaat, niet los op het wit van de
        # kaart: de dozen van de verhuizer zijn wit en verliezen op wit hun omtrek. Zijn hoofd steekt
        # boven die plaat uit, zoals de uitsneden elders op de site.
        figuur = ""
        if opties.get("foto") in FOTOS:
            src, fb, fh, alt = FOTOS[opties["foto"]]
            figuur = (f'<span class="vragen__figuur" aria-hidden="true">'
                      f'<img class="vragen__foto" src="{src}" alt="" width="{fb}" height="{fh}" '
                      f'loading="lazy" decoding="async"></span>')
        kaart = f'''<div class="vragen__bel vragen__bel--kop">
        {beeld_hoek}<div class="vragen__beltekst">
          {kopgroep}
          {binnen}{vul_tekst}
        </div>{figuur}
      </div>'''
        kopgroep = ""
    else:
        kaart = f'''<div class="vragen__bel">
        {binnen}
      </div>'''
    paneel = " b-vragen--paneel" if stijl == "paneel" else ""
    # De verhuizer (WERKER) hangt absoluut aan het paneel en staat daarom als laatste in de kop; zonder paneel of
    # naast een foto is er geen plek voor hem.
    werker = ""
    keuze = opties.get("werker", WERKER_PAGINA.get(ctx.pagina.pad, "twee-dozen"))
    if keuze and paneel and kopkaart and not met_foto:
        src, wb, wh = WERKER[keuze]
        werker = (f'<span class="vragen__werker" aria-hidden="true" style="--werker-b:{wb};--werker-h:{round(wh * WERKER_ZICHTBAAR)}">'
                  f'<img class="vragen__werkerbeeld" src="{src}" alt="" width="{wb}" height="{wh}" '
                  f'loading="lazy" decoding="async"></span>')
    return f'''<section class="sectie sectie--{sectie} b-vragen{paneel}" id="{kid}" aria-labelledby="{kid}-kop">
  <div class="wrap vragen">
    <div class="vragen__kop{" vragen__kop--kaart" if kopkaart else ""}">
      {beeld}{kopgroep}{beeld_tussen}{vul_voor}
      {kaart}{vul_na}{werker}
    </div>
    <div class="vragen__lijst" data-reveal>
      {"".join(vragen)}
    </div>
  </div>
</section>'''
