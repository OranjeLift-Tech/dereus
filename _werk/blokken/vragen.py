"""Veelgestelde vragen (#vragen): links de kop, de belregel en de bereikbaarheid (plakt mee), rechts de
vragen als details/summary, genummerd. Werkt zonder JS. De FAQPage in de JSON-LD (jsonld.py, dereus-e7)
leest hetzelfde blok, dus wat hier staat, staat ook daar.

Antwoorden mogen als tekst:-veld of als losse alinea's onder de ###-vraag staan.
Opties: sectie ("mist" standaard, of "wit"), open (nummer van de vraag die open staat, standaard geen).
"""
NAAM = "vragen"
CSS = True
JS = False

# Optie beeld (/contact/): een voorwerp uit de 3D-reeks dat uit het paneel steekt. Naam -> bron, breedte, hoogte.
# De vormgeving staat onderaan css/blok/vragen.css en geldt alleen op /contact/.
BEELDEN = {"headset": ("/img/contact-3d/headset.webp", 287, 320)}


def html(ctx, kopij, sectie="mist", open=None, **opties):
    k = kopij
    kid = ctx.esc(k.id or "vragen")
    beeld = ""
    if opties.get("beeld") in BEELDEN:
        src, bb, bh = BEELDEN[opties["beeld"]]
        beeld = (f'<img class="vragen__beeld" src="{src}" alt="" width="{bb}" height="{bh}" '
                 f'loading="lazy" decoding="async">')
    vragen = []
    for i, it in enumerate(k.items, 1):
        antwoord = ctx.alineas(it.tekst) + (ctx.lijst(it.lijst, "vinklijst") if it.lijst else "")
        vragen.append(f'''<details class="vraag" id="{kid}-{i}"{" open" if open == i else ""}>
        <summary><span class="vraag__nr" aria-hidden="true">{i:02d}</span><span class="vraag__tekst">{ctx.inline(it.titel)}</span><span class="vraag__plus" aria-hidden="true">{ctx.icoon("plus")}</span></summary>
        <div class="vraag__antwoord">{antwoord}</div>
      </details>''')
    bel = k.veld("belregel")
    if bel and ctx.tel in bel:
        # "Staat uw vraag er niet bij? Bel 085 000 5647." -> de vraag blijft, het nummer staat op de knop
        bel = bel.replace(f"Bel {ctx.tel}.", "").replace(f"Bel {ctx.tel}", "").replace(ctx.tel, "").strip()
    kaart = f'''<div class="vragen__bel">
        {ctx.bereikbaar("bereikbaar vragen__status")}
        <p>{ctx.inline(bel) if bel else "Staat uw vraag er niet bij?"}</p>
        {ctx.belknop("blauw")}
      </div>'''
    return f'''<section class="sectie sectie--{sectie} b-vragen" id="{kid}" aria-labelledby="{kid}-kop">
  <div class="wrap vragen">
    <div class="vragen__kop">
      {beeld}{ctx.kopgroep(k)}
      {kaart}
    </div>
    <div class="vragen__lijst" data-reveal>
      {"".join(vragen)}
    </div>
  </div>
</section>'''
