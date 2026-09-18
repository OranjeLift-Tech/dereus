"""De plaatsen (of landen) waar al een eigen pagina van live staat, als rij kaartjes.

Pagina /werkgebied/ (#plaatsen) en het sjabloon dienstdetail voor internationaal (soort="landen").
Alleen pagina's die live zijn krijgen een kaartje (ctx.live); staat er geen enkele aan, dan vervalt het blok.
Kopij: label, intro; optioneel per plaats een ###-item met de slug als id en een regel tekst.
"""
import _b4

NAAM = "plaatsenlijst"
CSS = True
JS = False


def html(ctx, kopij, **opties) -> str:
    k = kopij
    bron = _b4.landen() if opties.get("soort") == "landen" else _b4.plaatsen()
    actief = [(slug, naam, pad) for slug, naam, pad in bron if ctx.live(pad) and pad != ctx.pagina.pad]
    if not actief or not k.kop:
        return ""
    grond = "wit" if opties.get("grond") == "wit" else "mist"
    eigen = {it.id: it for it in k.items}
    kaartjes = ""
    for slug, naam, pad in actief:
        tekst = ctx.alineas(eigen[slug].tekst) if slug in eigen else ""
        kaartjes += (f'<li class="b-{NAAM}__kaart"><h3><a href="{ctx.esc(pad)}">{ctx.esc(naam)}</a></h3>{tekst}'
                     f'<span class="b-{NAAM}__pijl" aria-hidden="true">{ctx.icoon("pijl")}</span></li>')
    sid = ctx.esc(k.id or NAAM)
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{sid}" aria-labelledby="{sid}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div data-reveal>{ctx.kopgroep(k)}{ctx.alineas(k.tekst)}</div>
        <ul class="b-{NAAM}__rij" data-reveal-groep>{kaartjes}</ul>
      </div>
    </section>'''
