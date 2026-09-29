"""Vier kaarten in een raster van 2 x 2: wat opslag, verhuislift, montage en woningontruiming kosten.

Pagina: /kosten/. Kopij: de vier ##-blokken uit kosten.md (opties["kopij_ids"]), elk met tekst, linktekst en link.
Geen offerteknop in de kaarten (review K2): die staat in het antwoord, bij de treden en in de offertepil.
Het blok-id is ook de sleutel van het merkicoon en van /offerte/?dienst=.

Optie stijl="lijst" (29-09-2026, keuze 14 uit _ontwerpen/extradiensten-referentie-varianten.html, naar het
dienstenblok van referentie C): links de vier vragen als genummerde lijst met een pijlrondje, rechts één foto met
een groot omlijnd cijfer. Onder de muis (of bij focus) op een vraag verschijnt rechts de foto van die dienst,
zonder script (:has in css/blok/extradiensten.css). De mensen steken boven de foto uit: dezelfde foto als
uitsnede in een strook erboven. Onder 1000px valt de grote foto weg en krijgt elke vraag een duimfoto.
"""

import _b4

NAAM = "extradiensten"
CSS = True
JS = False

STANDAARD = ["opslag", "verhuislift", "montage", "woningontruiming"]

# Het voorwerp dat op elke kaart staat en er bovenuit steekt: sinds 28-09-2026 het klei-icoon van die dienst
# (img/clay/<naam>-240/480.webp, vierkant; website/review/clay-iconen-20260928/). Het vak is 12 rem hoog met
# object-fit contain. Vormgeving: css/blok/extradiensten.css en css/blok/kosten-diepte.css.
# Sinds 29-09-2026 staat het De Reus-logo op de dozen (-logo, _ai-beelden/clay-logo/logo-op-doos.cjs); montage heeft geen doos.
VOORWERP = {"opslag": "opslag-logo", "verhuislift": "verhuislift-logo", "montage": "montage",
            "woningontruiming": "woningontruiming-logo"}


# stijl "lijst": de dienstfoto van /diensten/ met zijn uitsnede (zelfde 4:3-kader, 720x540 en 1080x810).
# d0 = bovenkant van het onderwerp in de uitsnede, mid = midden van het onderwerp (beide gemeten op het alfakanaal).
FOTO = {"opslag": ("dienst-opslag-v3", .132, .45), "verhuislift": ("dienst-verhuislift", .225, .56),
        "montage": ("dienst-montage-v2", .033, .64), "woningontruiming": ("dienst-woningontruiming-v2", .093, .6)}


def _lijst(ctx, ids) -> str:
    rijen, fotos = "", ""
    for i, cid in enumerate(ids, 1):
        k = ctx.kopij.blok(cid)
        meer = ctx.knop(k.veld("linktekst"), _b4.schakel(ctx, k.veld("link")), soort="link") if k.veld("link") else ""
        naam, d0, mid = FOTO[k.id]
        rijen += f'''<article class="b-{NAAM}__rij" id="{k.id}" aria-labelledby="{k.id}-kop">
          <span class="b-{NAAM}__nr" aria-hidden="true">{i:02d}</span>
          <img class="b-{NAAM}__duim" src="/img/{naam}.webp" alt="" width="720" height="540" loading="lazy" decoding="async">
          <div class="b-{NAAM}__tekst">
            <h2 class="b-{NAAM}__kop" id="{k.id}-kop">{ctx.inline(k.kop)}</h2>
            {ctx.alineas(k.tekst)}
            <p class="b-{NAAM}__meer">{meer}</p>
          </div>
          <span class="b-{NAAM}__pijl" aria-hidden="true">{ctx.icoon("pijl")}</span>
        </article>'''
        fotos += f'''<div class="b-{NAAM}__foto"><span class="b-{NAAM}__cijfer">{i:02d}</span><div class="b-{NAAM}__vak">
            <div class="b-{NAAM}__pop" style="--d0:{d0};--mid:{mid}"><div class="b-{NAAM}__raam"><img src="/img/{naam}.webp" alt="" width="720" height="540" loading="lazy" decoding="async"></div><div class="b-{NAAM}__boven"><img src="/img/{naam}-uit.webp" alt="" width="1080" height="810" loading="lazy" decoding="async"></div></div>
          </div></div>'''
    return f'''<section class="b-{NAAM} b-{NAAM}--lijst sectie sectie--mist" data-b="{NAAM}">
      <div class="wrap b-{NAAM}__in"><div class="b-{NAAM}__lijst" data-reveal-groep>{rijen}</div>
        <div class="b-{NAAM}__beeld" aria-hidden="true">{fotos}</div>
      </div>
    </section>'''


def html(ctx, kopij, **opties) -> str:
    if opties.get("stijl") == "lijst":
        return _lijst(ctx, opties.get("kopij_ids") or STANDAARD)
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
