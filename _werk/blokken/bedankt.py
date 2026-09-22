"""Bedankt (/offerte/bedankt/, /contact/bedankt/): bevestiging, wat er nu gebeurt, en de weg terug.

Kopij: systeem.md, blok {#offerte-bedankt} of {#contact-bedankt}. De kop en de intro staan in het blok
"kop" (zelfde kopij_id). Dit blok toont de items als stappen, de belregel en de knoppen.
Optionele velden: knop en knop-link (standaard terug naar de home).
Optie beeld: ("/img/...", breedte, hoogte) zet een 3D-render voor het goudgele huis uit het logo
rechtsboven op de kaart. Zonder die optie verandert er niets aan de kaart.
"""

NAAM = "bedankt"
CSS = True
JS = False


def _beeld(ctx, beeld):
    """De render voor het goudgele huis, als de pagina er een meegeeft. Vormgeving: css/blok/bedankt.css."""
    if not beeld:
        return ""
    src, breed, hoog = beeld
    return (f'<span class="b-{NAAM}__beeld" aria-hidden="true"><span class="b-{NAAM}__huis"></span>'
            f'{ctx.beeld(src, "", breed, hoog, klasse=f"b-{NAAM}__obj")}</span>')


def html(ctx, kopij, **opties) -> str:
    k = kopij
    beeld = _beeld(ctx, opties.get("beeld"))
    stappen = ""
    if k.items:
        li = "".join(f'''<li class="b-{NAAM}__stap">
              <span class="b-{NAAM}__nr" aria-hidden="true">{i}</span>
              <div><h2 class="b-{NAAM}__titel">{ctx.inline(it.kop)}</h2>{ctx.alineas(it.tekst)}</div>
            </li>''' for i, it in enumerate(k.items, 1))
        stappen = f'<ol class="b-{NAAM}__stappen" role="list">{li}</ol>'
    belregel = k.veld("belregel")
    terug = ctx.knop(k.veld("knop", "Terug naar de home"), k.veld("knop-link", "/"), soort="licht", icoon="pijl")
    return f'''<section class="b-{NAAM} sectie sectie--mist" aria-label="Wat er nu gebeurt">
      <div class="wrap">
        <div class="b-{NAAM}__kaart{" b-" + NAAM + "__kaart--beeld" if beeld else ""}" data-reveal>{beeld}
          <span class="b-{NAAM}__vink" aria-hidden="true">{ctx.icoon("check")}</span>
          {stappen}
          {ctx.alineas(k.tekst)}
          {ctx.belregel(belregel, klasse=f"belregel b-{NAAM}__bel")}
          <div class="knoppen">{ctx.belknop(soort="blauw")}{terug}</div>
        </div>
      </div>
    </section>'''
