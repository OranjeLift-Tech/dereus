"""Kernwaarden als gedrag (/over-ons/ #zo-werken-wij): de Koningsblauwe band met dakrand, de kop links
met de offerteknop rechts, en daaronder de eerste waarde uitgelicht met een foto naast de overige
waarden als rijen. Naar het patroon business-feature-rows uit ../section-library (featured card plus
rows): de kaart en de rijen delen hun boven- en onderlijn, de kaart staat op een gekantelde plaat en
de verhuizers stappen boven de foto uit. Werkt voor 3 tot 8 items (de uitgelichte plus 2 tot 7 rijen).
Tekst per item als tekst:-veld of als losse alinea's onder de ###-titel.
Iconen volgen de kernwaarden uit het merkboek via het item-id (sterk, zorgvuldig, betrouwbaar, eerlijk, betrokken).
Optie foto: de sleutel van een dienstfoto met uitsnede, bv. "particulier-v2" voor img/dienst-particulier-v2.webp
met img/dienst-particulier-v2-uit.webp erover. Hoe ver de verhuizers uitstappen staat in UITSTAP; zie
css/blok/kernwaarden.css voor de berekening. Zonder foto is de uitgelichte kaart alleen tekst.
Optie compact: "gematigd" of "krap" zet de band strakker. Het veld knop: in de kopij zet de offerteknop in de kopregel.
"""
NAAM = "kernwaarden"
CSS = True
JS = False

ICONEN = {"sterk": "doos", "zorgvuldig": "schild", "betrouwbaar": "klok", "eerlijk": "euro", "betrokken": "persoon"}
# Sinds 29-09-2026 een echt voorwerp in een dikke gele tegel, zoals /contact/ en het werkgebied ("bu over ons sayfasındaki
# figürleri de aynı şekilde istiyorum"): icoon -> (bestand in img/contact-echt, breedte 1x, breedte 2x, hoogte 1x, sizes).
# Bronnen in img/LICENTIES.md. Een icoon zonder voorwerp blijft een lijnicoon.
VOORWERP = {
    "doos": ("dozen", 58, 116, 72, "3.2rem"),           # de twee logodozen van /contact/, eigen beeld
    "schild": ("plant", 62, 124, 72, "3.9rem"),         # Unsplash 2LlRY-bMmig: een kamerplant, netjes neergezet
    "klok": ("wekker", 48, 96, 72, "3rem"),             # Unsplash flpCsXSVgoo, ook op /contact/ #kaart
    "euro": ("munten", 80, 160, 55, "4.7rem"),          # Unsplash OApHds2yEGQ, twee stapels eurocenten
    "persoon": ("headset", 53, 106, 77, "3.3rem"),      # Unsplash dJ2hnNSqsmk: de verhuisadviseur blijft bereikbaar
}


def _icoon(ctx, naam):
    if naam in VOORWERP:
        bestand, b, b2, h, maat = VOORWERP[naam]
        pad = f"/img/contact-echt/{bestand}"
        return (f'<span class="kw__icoon kw__tegel kw__tegel--{bestand}" aria-hidden="true"><img class="kw__obj kw__obj--{bestand}" '
                f'src="{pad}-{b}.webp" srcset="{pad}-{b}.webp {b}w, {pad}-{b2}.webp {b2}w" '
                f'sizes="{maat}" alt="" width="{b}" height="{h}" loading="lazy" decoding="async"></span>')
    return f'<span class="kw__icoon" aria-hidden="true">{ctx.icoon(naam)}</span>'

# pop: hoe ver de laag boven het kader uitsteekt (in % van de kaderhoogte); knip: waar het kader
# begint, gemeten over de laag (pop / (1 + pop)). Alfa van dienst-particulier-v2-uit begint op 21,98%.
UITSTAP = {"particulier-v2": ("37.2%", "27.11%")}


def html(ctx, kopij, sectie="blauw", foto=None, compact=None, **opties):
    k = kopij
    if not 3 <= len(k.items) <= 8:
        raise ValueError(f"kernwaarden: 3 tot 8 items, niet {len(k.items)}")
    if compact and compact not in ("gematigd", "krap"):
        raise ValueError(f"kernwaarden: compact is 'gematigd' of 'krap', niet {compact!r}")
    if foto and foto not in UITSTAP:
        raise ValueError(f"kernwaarden: geen uitstapmaten voor foto {foto!r}, meet ze en zet ze in UITSTAP")

    eerste, *rest = k.items
    icoon = lambda it: _icoon(ctx, ICONEN.get(it.id, "check"))
    beeld, stijl = "", ""
    if foto:
        pop, knip = UITSTAP[foto]
        stijl = f' style="--pop:{pop};--knip:{knip}"'
        # alt leeg: de foto illustreert de waarde ernaast en voegt er niets aan toe
        beeld = f'''<div class="kwkaart__beeld"><span class="kwkaart__laag">\
{ctx.beeld(f"/img/dienst-{foto}.webp", "", 720, 540, klasse="kwkaart__foto")}\
<span class="kwkaart__uit">{ctx.beeld(f"/img/dienst-{foto}-uit.webp", "", 1080, 810)}</span></span></div>'''
    items = [f'''<li class="kw kw--uitgelicht"{stijl}>
        <div class="kwkaart">
          {beeld}
          <div class="kwkaart__tekst">
            <div class="kwkaart__titelrij">{icoon(eerste)}<h3 class="kw__titel">{ctx.inline(eerste.titel)}</h3></div>
            {ctx.alineas(eerste.tekst)}
          </div>
        </div>
      </li>''']
    for it in rest:
        items.append(f'''<li class="kw">
        {icoon(it)}
        <div class="kw__tekst"><h3 class="kw__titel">{ctx.inline(it.titel)}</h3>{ctx.alineas(it.tekst)}</div>
      </li>''')

    actie = ctx.knop(k.veld("knop"), "/offerte/", klasse="kwkop__actie") if k.veld("knop") else ""
    klassen = "sectie sectie--" + sectie + " b-kernwaarden"
    if compact:
        klassen += f" b-kernwaarden--{compact}"
    return f'''<section class="{klassen}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    <div class="kwkop">{ctx.kopgroep(k)}{actie}</div>
    <ul class="kwlijst" role="list" style="--kw-rijen:{len(rest)}" data-reveal-groep>
      {"".join(items)}
    </ul>
  </div>
</section>'''
