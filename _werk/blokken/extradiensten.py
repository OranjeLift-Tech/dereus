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

# Het 3D-voorwerp dat op elke kaart staat en er bovenuit steekt (img/kosten-3d/, alle 420 px hoog):
# naam en breedte. Vormgeving: css/blok/extradiensten.css en css/blok/kosten-diepte.css.
VOORWERP = {"opslag": ("opslagopen", 569), "verhuislift": ("lift", 210), "montage": ("boor", 509),
            "woningontruiming": ("huis", 425)}


def html(ctx, kopij, **opties) -> str:
    kaarten = ""
    for cid in opties.get("kopij_ids") or STANDAARD:
        k = ctx.kopij.blok(cid)
        # "Meer over deze dienst": het anker op /diensten/, of de eigen dienstpagina zodra die live is
        meer = ctx.knop(k.veld("linktekst"), _b4.schakel(ctx, k.veld("link")), soort="link") if k.veld("link") else ""
        kaarten += f'''<article class="b-{NAAM}__kaart" id="{k.id}" aria-labelledby="{k.id}-kop">
          <img class="b-{NAAM}__obj" src="/img/kosten-3d/{VOORWERP[k.id][0]}.webp" alt="" width="{VOORWERP[k.id][1]}" height="420" loading="lazy" decoding="async">
          <h2 class="b-{NAAM}__kop" id="{k.id}-kop">{ctx.inline(k.kop)}</h2>
          {ctx.alineas(k.tekst)}
          <p class="b-{NAAM}__acties">{meer}</p>
        </article>'''
    return f'''<section class="b-{NAAM} sectie sectie--mist" data-b="{NAAM}">
      <div class="wrap"><div class="b-{NAAM}__rooster" data-reveal-groep>{kaarten}</div></div>
    </section>'''
