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

# Het voorwerp dat op elke kaart staat en er bovenuit steekt: sinds 28-09-2026 het klei-icoon van die dienst
# (img/clay/<naam>-240/480.webp, vierkant; website/review/clay-iconen-20260928/). Het vak is 12 rem hoog met
# object-fit contain. Vormgeving: css/blok/extradiensten.css en css/blok/kosten-diepte.css.
VOORWERP = {"opslag": "opslag", "verhuislift": "verhuislift", "montage": "montage",
            "woningontruiming": "woningontruiming"}


def html(ctx, kopij, **opties) -> str:
    kaarten = ""
    for cid in opties.get("kopij_ids") or STANDAARD:
        k = ctx.kopij.blok(cid)
        # "Meer over deze dienst": het anker op /diensten/, of de eigen dienstpagina zodra die live is
        meer = ctx.knop(k.veld("linktekst"), _b4.schakel(ctx, k.veld("link")), soort="link") if k.veld("link") else ""
        kaarten += f'''<article class="b-{NAAM}__kaart" id="{k.id}" aria-labelledby="{k.id}-kop">
          <img class="b-{NAAM}__obj" src="/img/clay/{VOORWERP[k.id]}-240.webp" srcset="/img/clay/{VOORWERP[k.id]}-240.webp 240w, /img/clay/{VOORWERP[k.id]}-480.webp 480w" sizes="12rem" alt="" width="240" height="240" loading="lazy" decoding="async">
          <h2 class="b-{NAAM}__kop" id="{k.id}-kop">{ctx.inline(k.kop)}</h2>
          {ctx.alineas(k.tekst)}
          <p class="b-{NAAM}__acties">{meer}</p>
        </article>'''
    return f'''<section class="b-{NAAM} sectie sectie--mist" data-b="{NAAM}">
      <div class="wrap"><div class="b-{NAAM}__rooster" data-reveal-groep>{kaarten}</div></div>
    </section>'''
