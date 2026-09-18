"""Zo gaat het, in het kort: tekst plus een strook met genummerde goudgele schijven, met een link naar /werkwijze/.
Familie van werkwijze (home) en stappenlang (/werkwijze/).

Sjabloon dienstdetail, blok-id "hoe". Opties: grond ("wit" of "mist").
Heeft het blok eigen ###-items (zoals bij zakelijk), dan zijn dat de stappen. Anders komen de vijf staptitels uit
home.md #werkwijze, zodat ze op één plek staan. De link naar de hele werkwijze komt uit het blok zelf
(linktekst en link), anders uit gedeeld.md #korte-stappen.
"""

NAAM = "kortestappen"
CSS = True
JS = False


def _stappen(ctx, k):
    if k.items:
        return [(it.titel, it.tekst) for it in k.items]
    home = ctx.kopij_van("home")
    if home.heeft("werkwijze"):
        return [(it.titel, []) for it in home.blok("werkwijze").items]
    return []


def html(ctx, kopij, **opties) -> str:
    k = kopij
    grond = "mist" if opties.get("grond") == "mist" else "wit"
    stappen = _stappen(ctx, k)
    strook = "".join(
        f'<li class="b-{NAAM}__stap"><span class="b-{NAAM}__schijf" aria-hidden="true"><b>{i}</b></span>'
        f'<div><h3>{ctx.inline(titel)}</h3>{ctx.alineas(tekst)}</div></li>'
        for i, (titel, tekst) in enumerate(stappen, 1))
    strook = (f'<ol class="b-{NAAM}__strook{"" if k.items else " b-" + NAAM + "__strook--kort"}" role="list" '
              f'style="--aantal:{len(stappen)}" data-reveal-groep>{strook}</ol>') if strook else ""
    gedeeld = ctx.kopij_van("gedeeld")
    bron = k if k.veld("link") else (gedeeld.blok("korte-stappen") if gedeeld.heeft("korte-stappen") else None)
    link = ""
    if bron is not None and bron.veld("link") and bron.veld("linktekst") and ctx.live(bron.veld("link")):
        link = f'<p class="b-{NAAM}__acties">{ctx.knop(bron.veld("linktekst"), bron.veld("link"), soort="link")}</p>'
    vinkjes = "".join(f"<li>{ctx.inline(r)}</li>" for r in k.lijst)
    vinkjes = f'<ul class="b-{NAAM}__lijst">{vinkjes}</ul>' if vinkjes else ""
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div class="b-{NAAM}__tekst" data-reveal>{ctx.kopgroep(k)}{ctx.alineas(k.tekst)}{vinkjes}</div>
        {strook}
        {link}
      </div>
    </section>'''
