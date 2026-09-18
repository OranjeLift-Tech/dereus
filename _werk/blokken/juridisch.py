"""Juridische tekst (/algemene-voorwaarden/, /privacyverklaring/): één tekstkolom van 68ch met de
inhoudsopgave als pilchips, en op de voorwaarden een samenvatting en de knop "Pdf downloaden".

Gebruik: ("juridisch", {"kopij": None, "pdf": "/docs/....pdf"}). Het blok leest zelf alle ##-blokken van
het kopijbestand (ctx.kopij.blokken), in volgorde. Van het #kop-blok gebruikt het lijstkop, lijst en knop
(de rest van de kop staat in het blok "kop").

Volgorde binnen een artikel: met een lijstkop eerst de lijstkop en de lijst, dan de alinea's; zonder
lijstkop eerst de alinea's, dan de lijst (zoals "In deze voorwaarden wordt verstaan onder:" en dan de leden).
Genummerde leden ("1. klant: ...") blijven letterlijk staan, zonder extra opsommingsteken.
"""
import re
from pathlib import Path

NAAM = "juridisch"
CSS = True
JS = False

WORTEL = Path(__file__).resolve().parents[2]
GENUMMERD = re.compile(r"^\d+\.\s")


def _lijst(ctx, regels):
    if not regels:
        return ""
    genummerd = all(GENUMMERD.match(r) for r in regels)
    if genummerd:
        li = "".join(
            f'<li><span class="b-{NAAM}__nr">{ctx.esc(r.split(" ", 1)[0])}</span><span>{ctx.inline(r.split(" ", 1)[1])}</span></li>'
            for r in regels)
        return f'<ul class="b-{NAAM}__leden" role="list">{li}</ul>'
    return f'<ul class="b-{NAAM}__lijst">{"".join(f"<li>{ctx.inline(r)}</li>" for r in regels)}</ul>'


def _deel(ctx, b):
    lijstkop = b.veld("lijstkop")
    kop_lijst = (f'<p class="b-{NAAM}__lijstkop">{ctx.inline(lijstkop)}</p>' if lijstkop else "") + _lijst(ctx, b.lijst)
    alineas = ctx.alineas(b.tekst)
    items = "".join(f'<h3 class="b-{NAAM}__h3">{ctx.inline(it.kop)}</h3>{ctx.alineas(it.tekst)}{_lijst(ctx, it.lijst)}'
                    for it in b.items)
    inhoud = (kop_lijst + alineas) if lijstkop else (alineas + kop_lijst)
    return f'''<section class="b-{NAAM}__deel" id="{b.id}" aria-labelledby="{b.id}-kop">
            <h2 class="b-{NAAM}__h2" id="{b.id}-kop">{ctx.inline(b.kop)}</h2>
            {inhoud}{items}
          </section>'''


def _pdf(ctx, pad, tekst):
    bestand = WORTEL / pad.lstrip("/")
    grootte = f", {max(1, round(bestand.stat().st_size / 1024))} kB" if bestand.exists() else ""
    return ctx.knop(f"{tekst} (pdf{grootte})", pad, soort="blauw", icoon=None,
                    klasse=f"b-{NAAM}__pdf", attrs='download type="application/pdf"')


def html(ctx, kopij, **opties) -> str:
    doc = ctx.kopij
    h1 = doc.h1
    delen = [b for b in doc.blokken if b.niveau == 2]
    chips = "".join(f'<li><a href="#{b.id}">{ctx.inline(b.veld("kort") or b.kop)}</a></li>' for b in delen)
    samenvatting = ""
    if h1 is not None and h1.lijst:
        samenvatting = f'''<aside class="b-{NAAM}__samenvatting" aria-labelledby="{NAAM}-samen-kop">
            <p class="b-{NAAM}__samenkop" id="{NAAM}-samen-kop">{ctx.inline(h1.veld("lijstkop", ""))}</p>
            {ctx.lijst(h1.lijst, klasse=f"vinklijst b-{NAAM}__punten")}
          </aside>'''
    pdf = _pdf(ctx, opties["pdf"], (h1.veld("knop") if h1 is not None else "") or "Pdf downloaden") if opties.get("pdf") else ""
    titel = ctx.zonder_opmaak(h1.kop) if h1 is not None else ""
    return f'''<section class="b-{NAAM} sectie sectie--wit" aria-label="{ctx.esc(titel)}">
      <div class="wrap b-{NAAM}__in">
        <nav class="b-{NAAM}__toc" aria-label="Op deze pagina">
          <p class="b-{NAAM}__tockop">Op deze pagina</p>
          <ul class="b-{NAAM}__chips" role="list">{chips}</ul>
          {f'<div class="b-{NAAM}__acties">{pdf}</div>' if pdf else ""}
        </nav>
        <div class="b-{NAAM}__tekst">
          {samenvatting}
          {"".join(_deel(ctx, b) for b in delen)}
        </div>
      </div>
    </section>'''
