"""Bedankt (/offerte/bedankt/, /contact/bedankt/): bevestiging, wat er nu gebeurt, en de weg terug.

Kopij: systeem.md, blok {#offerte-bedankt} of {#contact-bedankt}. De kop en de intro staan in het blok
"kop" (zelfde kopij_id). Dit blok toont de items als stappen, de belregel en de knoppen.
Optionele velden: knop en knop-link (standaard terug naar de home).
"""

NAAM = "bedankt"
CSS = True
JS = False


def html(ctx, kopij, **opties) -> str:
    k = kopij
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
        <div class="b-{NAAM}__kaart" data-reveal>
          <span class="b-{NAAM}__vink" aria-hidden="true">{ctx.icoon("check")}</span>
          {stappen}
          {ctx.alineas(k.tekst)}
          {ctx.belregel(belregel, klasse=f"belregel b-{NAAM}__bel")}
          <div class="knoppen">{ctx.belknop(soort="blauw")}{terug}</div>
        </div>
      </div>
    </section>'''
