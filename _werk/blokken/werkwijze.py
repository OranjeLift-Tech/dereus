"""Werkwijze (#werkwijze): de Koningsblauwe band met dakrand. Vijf stappen met genummerde goudgele schijven
aan een gestippelde route (SVG); er rijdt één keer een busje langs als de band in beeld komt.
Geen foto's van onbekende herkomst (besluit dereus-28): de stap-*.webp van de basis-site blijven ongebruikt.
"""
NAAM = "werkwijze"
CSS = True
JS = False

ICONEN = ["document", "telefoon", "mail", "kalender", "vrachtwagen"]


def html(ctx, kopij, **opties):
    k = kopij
    stappen = []
    for i, it in enumerate(k.items, 1):
        icoon = ICONEN[(i - 1) % len(ICONEN)]
        stappen.append(f'''<li class="stap" id="{ctx.esc(it.id)}">
        <span class="stap__schijf" aria-hidden="true"><b>{i}</b></span>
        <div class="stap__tekst">
          <span class="stap__icoon" aria-hidden="true">{ctx.icoon(icoon)}</span>
          <h3 class="stap__titel"><span class="vh">Stap {i}: </span>{ctx.inline(it.titel)}</h3>
          <p>{ctx.inline(it.veld("tekst"))}</p>
        </div>
      </li>''')
    knoppen = []
    if k.veld("knop"):
        knoppen.append(ctx.knop(k.veld("knop"), "/offerte/"))
    if k.veld("linktekst"):
        knoppen.append(ctx.knop(k.veld("linktekst"), k.veld("link", "/kosten/"), soort="licht"))
    route = ('<svg class="route" viewBox="0 0 1000 40" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
             '<path class="route__lijn" d="M0 20 C 100 2, 150 2, 250 20 S 400 38, 500 20 S 650 2, 750 20 S 900 38, 1000 20"/></svg>'
             f'<span class="route__bus" aria-hidden="true">{ctx.icoon("vrachtwagen")}</span>')
    return f'''<section class="sectie sectie--blauw b-werkwijze" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    {ctx.kopgroep(k, "kopgroep--midden")}
    <div class="stappen" data-reveal>
      <div class="stappen__route">{route}</div>
      <ol class="stappen__lijst" role="list">
        {"".join(stappen)}
      </ol>
    </div>
    {f'<div class="knoppen knoppen--midden">{"".join(knoppen)}</div>' if knoppen else ""}
  </div>
</section>'''
