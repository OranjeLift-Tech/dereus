"""Vier kaarten in een raster van 2 x 2: wat opslag, verhuislift, montage en woningontruiming kosten.

Pagina: /kosten/. Kopij: de vier ##-blokken uit kosten.md (opties["kopij_ids"]), elk met tekst, linktekst en link.
Geen offerteknop in de kaarten (review K2): die staat in het antwoord, bij de treden en in de offertepil.
Het blok-id is ook de sleutel van het merkicoon en van /offerte/?dienst=.
"""

import _b4

NAAM = "extradiensten"
CSS = True
JS = False

STANDAARD = ["opslag", "verhuislift", "montage", "woningontruiming"]


def html(ctx, kopij, **opties) -> str:
    kaarten = ""
    for cid in opties.get("kopij_ids") or STANDAARD:
        k = ctx.kopij.blok(cid)
        # "Meer over deze dienst": het anker op /diensten/, of de eigen dienstpagina zodra die live is
        meer = ctx.knop(k.veld("linktekst"), _b4.schakel(ctx, k.veld("link")), soort="link") if k.veld("link") else ""
        kaarten += f'''<article class="b-{NAAM}__kaart" id="{k.id}" aria-labelledby="{k.id}-kop">
          <span class="b-{NAAM}__icoon">{ctx.dienst_icoon(k.id, inline=True)}</span>
          <h2 class="b-{NAAM}__kop" id="{k.id}-kop">{ctx.inline(k.kop)}</h2>
          {ctx.alineas(k.tekst)}
          <p class="b-{NAAM}__acties">{meer}</p>
        </article>'''
    return f'''<section class="b-{NAAM} sectie sectie--mist" data-b="{NAAM}">
      <div class="wrap"><div class="b-{NAAM}__rooster" data-reveal-groep>{kaarten}</div></div>
    </section>'''
