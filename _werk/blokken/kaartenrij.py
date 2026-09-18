"""Een rij van drie of vier genummerde kaarten: wanneer deze dienst handig is, of welke keuzes u heeft.

Sjabloon dienstdetail, blok-id "keuze" of "wanneer" (opties["kopij_id"]). Opties: grond ("wit" of "mist").
Kopij: label, intro, ###-items met tekst, optioneel slot.
"""

NAAM = "kaartenrij"
CSS = True
JS = False


def html(ctx, kopij, **opties) -> str:
    k = kopij
    if not k.items:
        return ""
    grond = "wit" if opties.get("grond") == "wit" else "mist"
    kaarten = "".join(
        f'<li class="b-{NAAM}__kaart"><span class="b-{NAAM}__nr" aria-hidden="true">{i:02d}</span>'
        f'<h3>{ctx.inline(it.titel)}</h3>{ctx.alineas(it.tekst)}</li>'
        for i, it in enumerate(k.items, 1))
    slot = f'<p class="b-{NAAM}__slot">{ctx.inline(k.veld("slot"))}</p>' if k.veld("slot") else ""
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div data-reveal>{ctx.kopgroep(k)}{ctx.alineas(k.tekst)}</div>
        <ol class="b-{NAAM}__rij" role="list" style="--aantal:{len(k.items)}" data-reveal-groep>{kaarten}</ol>
        {slot}
      </div>
    </section>'''
