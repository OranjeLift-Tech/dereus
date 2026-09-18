"""Een kleine kaart van de plaats, volgens de aanpak van dereus-e7: een vooraf gemaakte SVG uit OpenStreetMap-data
(img/kaart-<slug>.svg, gemaakt met _werk/kaart/maak_kaart.py), geen embed en geen verzoek naar een kaartdienst.

Sjabloon plaats (#kaart). Opties: slug, grond. Kopij: label, intro, tekst, optioneel knop (tekst van de routeknop).
Bestaat het kaartbeeld van deze plaats nog niet, dan blijft alleen de tekst staan; zonder tekst vervalt het blok.
"""
from kit import WORTEL

NAAM = "plaatskaart"
CSS = True
JS = False

BREEDTE, HOOGTE = 1400, 933          # gelijk aan img/kaart-den-haag.svg


def html(ctx, kopij, **opties) -> str:
    k = kopij
    slug = opties.get("slug", "")
    beeld = f"/img/kaart-{slug}.svg"
    heeft_beeld = bool(slug) and (WORTEL / beeld.lstrip("/")).exists()
    if not heeft_beeld and not (k.tekst or k.veld("intro")):
        return ""
    grond = "mist" if opties.get("grond") == "mist" else "wit"
    kaart = ""
    if heeft_beeld:
        alt = k.veld("alt") or ctx.zonder_opmaak(k.kop)
        bron = ('<p class="b-plaatskaart__bron">© <a href="https://www.openstreetmap.org/copyright" rel="noopener">'
                'OpenStreetMap</a></p>')
        kaart = f'<figure class="b-{NAAM}__kaart" data-reveal>{ctx.beeld(beeld, alt, BREEDTE, HOOGTE)}{bron}</figure>'
    sid = ctx.esc(k.id or NAAM)
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{sid}" aria-labelledby="{sid}-kop" data-b="{NAAM}">
      <div class="wrap b-{NAAM}__in{"" if kaart else " b-" + NAAM + "__in--zonder"}">
        <div class="b-{NAAM}__tekst" data-reveal>{ctx.kopgroep(k)}{ctx.alineas(k.tekst)}</div>
        {kaart}
      </div>
    </section>'''
