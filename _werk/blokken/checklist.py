"""Een afvinklijst in een kaart. Voor #voorbereiding en #na-de-verhuizing op /werkwijze/ en voor #tips en
#waarom op de dienst- en landpagina's.

Opties: kopij_id (welk blok), grond = "wit" of "mist", en indeling:
  "naast" (standaard) links de kop, rechts de punten. Dit is de indeling van de dienst- en landpagina's.
  "breed"             de kop op het midden boven, de punten eronder in twee kolommen, slot en link onderaan.
                      Gebruikt op /werkwijze/, waar de kop kort is en de lijst het blok anders scheef trekt.
Kopij: label, intro, lijstkop, lijst (een regel mag beginnen met een vette kop: "**Dozen op tijd.** uitleg"), slot,
en optioneel linktekst en link.
"""
import re

NAAM = "checklist"
CSS = True
JS = False

# de verhuisadviseur bij het tipvak: dezelfde uitsnede als op /contact/
ADVIES = ("/img/contact-uit.webp", 1200, 800)

_VET = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$")


def _punt(ctx, regel):
    m = _VET.match(regel)
    if m:
        return f'<li><b>{ctx.inline(m.group(1))}</b> <span>{ctx.inline(m.group(2))}</span></li>'
    return f"<li><span>{ctx.inline(regel)}</span></li>"


def html(ctx, kopij, **opties) -> str:
    k = kopij
    grond = "mist" if opties.get("grond") == "mist" else "wit"
    breed = opties.get("indeling") == "breed"
    punten = "".join(_punt(ctx, r) for r in k.lijst)
    lijstkop = f'<h3 class="b-{NAAM}__lijstkop">{ctx.inline(k.veld("lijstkop"))}</h3>' if k.veld("lijstkop") else ""
    slot = ""
    if k.veld("slot"):
        gezicht = ctx.beeld(ADVIES[0], "", ADVIES[1], ADVIES[2])      # sier: de tekst ernaast zegt het al
        slot = (f'<div class="b-{NAAM}__slot"><span class="b-{NAAM}__advies">{gezicht}</span>'
                f'<p>{ctx.inline(k.veld("slot"))}</p></div>')
    link = ctx.knop(k.veld("linktekst"), k.veld("link"), soort="link") if k.veld("link") else ""
    link = f'<p class="b-{NAAM}__acties">{link}</p>' if link else ""
    # Breed zet slot en link onder de lijst; anders zouden ze in een halflege kolom naast de punten hangen.
    voet = f'<div class="b-{NAAM}__voet">{slot}{link}</div>' if breed and (slot or link) else ""
    kop_staart = "" if breed else f"{slot}{link}"
    extra = f" b-{NAAM}--breed" if breed else ""
    kopgroep = ctx.kopgroep(k, "kopgroep--midden") if breed else ctx.kopgroep(k)
    return f'''<section class="b-{NAAM} b-{NAAM}--{grond}{extra} sectie sectie--{grond}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div class="b-{NAAM}__kaart">
          <div class="b-{NAAM}__kop" data-reveal>{kopgroep}{ctx.alineas(k.tekst)}{kop_staart}</div>
          <div class="b-{NAAM}__lijstdeel">
            {lijstkop}
            <ul class="b-{NAAM}__lijst" data-reveal-groep>{punten}</ul>
          </div>{voet}
        </div>
      </div>
    </section>'''
