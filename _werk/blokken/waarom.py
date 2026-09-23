"""Waarom De Reus: vier afspraken naast een foto van twee verhuizers die samen een fauteuil dragen."""
NAAM = "waarom"
CSS = True
JS = False

# Per kaart het 3D-voorwerp, op volgorde van de kopij: map, bestandsnaam, breedte en hoogte.
# Allemaal renders uit dezelfde reeks als de contactkaarten en /kosten/ (één lichtbron linksboven),
# dus vier gelijke pictogrammen in plaats van vier badges in vier kleurcombinaties.
VOORWERP = [
    ("contact-3d", "headset", 287, 320),   # één vaste verhuisadviseur
    ("kosten-3d", "trap", 371, 420),       # vakmensen: de kast veilig de trap af
    ("kosten-3d", "wagen", 594, 420),      # geen voorrijkosten: de rit naar uw adres
    ("contact-3d", "schild", 251, 320),    # standaard verzekerd
]

# Ondergrond per kaart, op dezelfde volgorde. Vier lichte tinten uit het palet die net van elkaar
# verschillen; zie waarom.css.
ONDERGROND = ["blauw", "creme", "mint", "mist"]


def html(ctx, kopij, **opties):
    k = kopij
    kaarten = []
    for i, it in enumerate(k.items):
        map_, naam, b, h = VOORWERP[i % len(VOORWERP)]
        grond = ONDERGROND[i % len(ONDERGROND)]
        kaarten.append(f'''<li class="wkaart wkaart--{grond}">
        <span class="wkaart__voorwerp" aria-hidden="true"><img class="wkaart__obj wkaart__obj--{naam}" src="/img/{map_}/{naam}.webp" alt="" width="{b}" height="{h}" loading="lazy" decoding="async"></span>
        <h3 class="wkaart__titel">{ctx.inline(it.titel)}</h3>
        <p>{ctx.inline(it.veld("tekst"))}</p>
      </li>''')
    # Eén knop, en dus één doorverwijzing die een handeling is. De sleutels linktekst en link zijn
    # hier ook uit home.md gehaald, zodat er geen veld staat dat niets doet. Zie design-notes A5.
    knop = ctx.knop(k.veld("knop", "Offerte aanvragen"), "/offerte/") if k.veld("knop") else ""
    return f'''<section class="sectie sectie--wit b-waarom" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap waarom">
    <div class="waarom__kop" data-reveal>
      {ctx.kopgroep(k)}
    </div>
    <div class="waarom__inhoud">
      <figure class="waarom__beeld" data-reveal>
        {ctx.beeld("/img/verhuisdag-dragen.webp", "Twee verhuizers dragen samen een fauteuil, ingepakt in een deken en folie", 1400, 1050)}
      </figure>
      <ul class="wkaarten" role="list" data-reveal-groep>{"".join(kaarten)}</ul>
    </div>
    {f'<div class="knoppen waarom__knoppen">{knop}</div>' if knop else ""}
  </div>
</section>'''
