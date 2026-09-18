"""Wat wij doen: de kern van een dienstpagina. Links de tekst en de punten, rechts het merkicoon in het huisvormige
kader (dezelfde vorm als op /diensten/).

Sjabloon dienstdetail, blok-id "wat". Opties: dienst (sleutel van het merkicoon), grond ("wit" of "mist").
Kopij: label, intro, tekst, lijstkop, lijst, slot. Regels met een vette kop ("**Inpakken.** uitleg") worden kaarten,
gewone regels een vinklijst. Alinea's met een onbekend feit heeft de kopijlezer al weggelaten.
"""
import re

NAAM = "watwijdoen"
CSS = True
JS = False

_VET = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$")


def html(ctx, kopij, **opties) -> str:
    k = kopij
    grond = "mist" if opties.get("grond") == "mist" else "wit"
    kaarten, vinkjes = "", ""
    for regel in k.lijst:
        m = _VET.match(regel)
        if m:
            kaarten += (f'<li class="b-{NAAM}__kaart"><h3>{ctx.inline(m.group(1).rstrip("."))}</h3>'
                        f'<p>{ctx.inline(m.group(2))}</p></li>')
        else:
            vinkjes += f"<li>{ctx.inline(regel)}</li>"
    lijstkop = f'<h3 class="b-{NAAM}__lijstkop">{ctx.inline(k.veld("lijstkop"))}</h3>' if k.veld("lijstkop") and k.lijst else ""
    kaarten = f'<ul class="b-{NAAM}__kaarten" data-reveal-groep>{kaarten}</ul>' if kaarten else ""
    vinkjes = f'<ul class="b-{NAAM}__vinkjes">{vinkjes}</ul>' if vinkjes else ""
    slot = f'<p class="b-{NAAM}__slot">{ctx.inline(k.veld("slot"))}</p>' if k.veld("slot") else ""
    icoon = opties.get("dienst")
    beeld = (f'<div class="b-{NAAM}__beeld" aria-hidden="true"><span class="b-{NAAM}__huis">'
             f'{ctx.dienst_icoon(icoon, inline=True)}</span></div>') if icoon else ""
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div class="b-{NAAM}__in{"" if beeld else " b-" + NAAM + "__in--breed"}">
          <div class="b-{NAAM}__tekst" data-reveal>
            {ctx.kopgroep(k)}
            {ctx.alineas(k.tekst)}
            {lijstkop}{vinkjes}
            {slot}
          </div>
          {beeld}
        </div>
        {kaarten}
      </div>
    </section>'''
