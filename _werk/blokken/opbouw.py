"""Hoe de prijs tot stand komt: de prijsfactoren als kaarten, daaronder all-in prijs tegenover regieprijs.

Pagina: /kosten/. Kopij: ## ... {#opbouw} met label, intro, lijstkop, lijst (regels in de vorm "**Kop.** uitleg"),
slot, en items: de eerste twee staan tegenover elkaar (all-in en regie), de rest komt als strook eronder.
"""
import re

NAAM = "opbouw"
CSS = True
JS = False

_FACTOR = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$")

# Optie voorwerpen (/kosten/): per factor een 3D-voorwerp op een gele schijf, bestand in img/kosten-3d/ met breedte bij
# 420 px hoogte. Renders uit _ai-beelden/kosten-3d (three.js, het echte logo); vormgeving in css/blok/opbouw-3d.css.
VOORWERPEN = [("dozen", 437), ("wagen", 594), ("trap", 371), ("gereedschap", 477), ("opslag", 589)]


def _factor(ctx, regel, nr, voorwerp=None):
    m = _FACTOR.match(regel)
    kop, uitleg = (m.group(1).rstrip("."), m.group(2)) if m else (regel, "")
    podium = ""
    if voorwerp:
        podium = (f'<span class="b-{NAAM}__podium" aria-hidden="true"><img class="b-{NAAM}__obj" src="/img/kosten-3d/{voorwerp[0]}.webp" alt="" '
                  f'width="{voorwerp[1]}" height="420" loading="lazy" decoding="async"></span>')
    return (f'<li class="b-{NAAM}__factor">{podium}<span class="b-{NAAM}__nr" aria-hidden="true">{nr:02d}</span>'
            f'<h3 class="b-{NAAM}__factorkop">{ctx.inline(kop)}</h3><p>{ctx.inline(uitleg)}</p></li>')


def _soort(ctx, it, klasse=""):
    lijst = "".join(f"<li>{ctx.inline(r)}</li>" for r in it.lijst)
    lijst = f"<ul>{lijst}</ul>" if lijst else ""
    return (f'<article class="b-{NAAM}__soort {klasse}" id="{it.id}"><h3 class="b-{NAAM}__soortkop">{ctx.inline(it.kop)}</h3>'
            f'{ctx.alineas(it.tekst)}{lijst}</article>')


def html(ctx, kopij, **opties) -> str:
    k = kopij
    drie_d = bool(opties.get("voorwerpen"))
    factoren = "".join(_factor(ctx, r, i + 1, VOORWERPEN[i] if drie_d and i < len(VOORWERPEN) else None) for i, r in enumerate(k.lijst))
    accolade = f'<div class="b-{NAAM}__accolade" aria-hidden="true"></div>' if drie_d else ""
    variant = f" b-{NAAM}--3d" if drie_d else ""
    lijstkop = f'<h3 class="b-{NAAM}__lijstkop">{ctx.inline(k.veld("lijstkop"))}</h3>' if k.veld("lijstkop") else ""
    duo, rest = k.items[:2], k.items[2:]
    duo_html = ""
    if len(duo) == 2:
        duo_html = (f'<div class="b-{NAAM}__duo" data-reveal>{_soort(ctx, duo[0], "b-" + NAAM + "__soort--a")}'
                    f'<span class="b-{NAAM}__of" aria-hidden="true">{ctx.esc(opties.get("of", "of"))}</span>'
                    f'{_soort(ctx, duo[1], "b-" + NAAM + "__soort--b")}</div>')
    else:
        rest = k.items
    rest_html = "".join(_soort(ctx, it, "b-" + NAAM + "__soort--strook") for it in rest)
    rest_html = f'<div class="b-{NAAM}__stroken" data-reveal-groep>{rest_html}</div>' if rest_html else ""
    slot = f'<p class="b-{NAAM}__slot">{ctx.inline(k.veld("slot"))}</p>' if k.veld("slot") else ""
    intro = f'<p class="b-{NAAM}__intro">{ctx.inline(k.veld("intro"))}</p>' if k.veld("intro") else ""
    return f'''<section class="b-{NAAM}{variant} sectie sectie--mist" id="{k.id}" aria-labelledby="{k.id}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div class="b-{NAAM}__kop" data-reveal>
          {ctx.label(k.veld("label"))}
          <h2 class="h2" id="{k.id}-kop">{ctx.inline(k.kop)}</h2>
          {intro}{ctx.alineas(k.tekst)}
        </div>
        {lijstkop}
        <ol class="b-{NAAM}__factoren" data-reveal-groep>{factoren}</ol>
        {accolade}
        {duo_html}
        {slot}
        {rest_html}
      </div>
    </section>'''
