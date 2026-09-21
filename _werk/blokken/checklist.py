"""Een afvinklijst in een witte kaart: links de kop, rechts de punten. Voor #voorbereiding en #na-de-verhuizing.

Pagina: /werkwijze/. Opties: kopij_id (welk blok), grond = "wit" of "mist", beeld (aan of uit).
Kopij: label, intro, lijstkop, lijst (een regel mag beginnen met een vette kop: "**Dozen op tijd.** uitleg"), slot,
en optioneel linktekst en link.
"""
import re

NAAM = "checklist"
CSS = True
JS = False

# de verhuisadviseur bij het tipvak: dezelfde uitsnede als op /contact/
ADVIES = ("/img/contact-uit.webp", 1200, 800)

# Het beeld van de optie "beeld": de tafel met agenda, rolmaat en ingepakte dozen op de achtergrond.
# Geen mensen in beeld, dus A3 blijft staan. Hetzelfde bestand als de kop van /kosten/; Brocken doet
# dat ook, daar staat de seniorenfoto van de home op de werkwijzepagina.
BEELD = ("/img/headers/kosten.webp", 1600, 900)

_VET = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$")


def _punt(ctx, regel):
    m = _VET.match(regel)
    if m:
        return f'<li><b>{ctx.inline(m.group(1))}</b> <span>{ctx.inline(m.group(2))}</span></li>'
    return f"<li><span>{ctx.inline(regel)}</span></li>"


def html(ctx, kopij, **opties) -> str:
    k = kopij
    grond = "mist" if opties.get("grond") == "mist" else "wit"
    punten = "".join(_punt(ctx, r) for r in k.lijst)
    lijstkop = f'<h3 class="b-{NAAM}__lijstkop">{ctx.inline(k.veld("lijstkop"))}</h3>' if k.veld("lijstkop") else ""
    slot = ""
    if k.veld("slot"):
        gezicht = ctx.beeld(ADVIES[0], "", ADVIES[1], ADVIES[2])      # sier: de tekst ernaast zegt het al
        slot = (f'<div class="b-{NAAM}__slot"><span class="b-{NAAM}__advies">{gezicht}</span>'
                f'<p>{ctx.inline(k.veld("slot"))}</p></div>')
    link = ctx.knop(k.veld("linktekst"), k.veld("link"), soort="link") if k.veld("link") else ""
    link = f'<p class="b-{NAAM}__acties">{link}</p>' if link else ""
    # Met beeld is de sectie geen kaart maar een stapeling: kop, foto en bord over elkaar heen.
    # De vormgeving staat in css/blok/checklist.css; alt blijft leeg, want de lijst ernaast zegt alles
    # wat het beeld laat zien.
    beeld, compositie = "", ""
    if opties.get("beeld"):
        beeld = (f'<figure class="b-{NAAM}__beeld" data-reveal>'
                 f'{ctx.beeld(BEELD[0], "", BEELD[1], BEELD[2], klasse=f"b-{NAAM}__foto")}</figure>')
        compositie = f" b-{NAAM}--compositie"
    return f'''<section class="b-{NAAM} b-{NAAM}--{grond}{compositie} sectie sectie--{grond}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div class="b-{NAAM}__kaart">
          <div class="b-{NAAM}__kop" data-reveal>{ctx.kopgroep(k)}{ctx.alineas(k.tekst)}{slot}{link}</div>
          {beeld}
          <div class="b-{NAAM}__lijstdeel">
            {lijstkop}
            <ul class="b-{NAAM}__lijst" data-reveal-groep>{punten}</ul>
          </div>
        </div>
      </div>
    </section>'''
