"""Andere diensten: een rij kaarten met het merkicoon, de naam en de eerste zin van elke dienst.

Sjablonen dienstdetail, land en plaats. De kop komt uit gedeeld.md #verwant; zonder dat blok vervalt de rij.
De kaarten komen uit diensten.md (label, kop, eerste alinea). Een kaart linkt naar de eigen dienstpagina als die
live is, anders naar het anker op /diensten/.
Opties: zonder (sleutel van de dienst van deze pagina), kies (lijst sleutels, "alle" voor alle acht, anders de
hoofddiensten), grond, en kopij_id: dan komt de kop uit dat blok van de eigen pagina (plaats: #diensten).
"""
import re

import _b4

NAAM = "verwant"
CSS = True
JS = False

STANDAARD = ["particulier", "zakelijk", "internationaal", "verhuislift", "opslag", "montage"]
ALLE = ["particulier", "zakelijk", "nationaal", "internationaal", "verhuislift", "opslag", "montage", "woningontruiming"]


def _eerste_zin(tekst):
    m = re.match(r"(.+?[.?!])(\s|$)", tekst)
    return m.group(1) if m else tekst


def html(ctx, kopij, **opties) -> str:
    if kopij is not None:
        kop = kopij
    else:
        gedeeld = ctx.kopij_van("gedeeld")
        if not gedeeld.heeft("verwant"):
            return ""
        kop = gedeeld.blok("verwant")
    diensten = ctx.kopij_van("diensten")
    grond = "wit" if opties.get("grond") == "wit" else "mist"
    alle = opties.get("kies") == "alle"
    kies = [d for d in (ALLE if alle else opties.get("kies") or STANDAARD) if d != opties.get("zonder") and diensten.heeft(d)]
    kies = kies if alle else kies[:4]
    if not kies:
        return ""
    kaarten = ""
    for d in kies:
        b = diensten.blok(d)
        href = _b4.dienst_href(ctx, d)
        zin = _eerste_zin(b.tekst[0]) if b.tekst else ""
        kaarten += f'''<li class="b-{NAAM}__kaart">
          <span class="b-{NAAM}__icoon" aria-hidden="true">{ctx.dienst_icoon(d, inline=True)}</span>
          <h3><a href="{ctx.esc(href)}">{ctx.inline(b.veld("label") or b.kop)}</a></h3>
          <p>{ctx.inline(zin)}</p>
          <span class="b-{NAAM}__pijl" aria-hidden="true">{ctx.icoon("pijl")}</span>
        </li>'''
    sid = ctx.esc(kop.id or NAAM)
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{sid}" aria-labelledby="{sid}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div data-reveal>{ctx.kopgroep(kop)}{ctx.alineas(kop.tekst)}</div>
        <ul class="b-{NAAM}__rij{" b-" + NAAM + "__rij--alle" if alle else ""}" style="--aantal:{min(4, len(kies))}" data-reveal-groep>{kaarten}</ul>
      </div>
    </section>'''
