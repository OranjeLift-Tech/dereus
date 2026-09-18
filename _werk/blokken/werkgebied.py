"""Werkgebied (#werkgebied): de Diepblauwe band met dakrand. Links de kop en drie regels (Den Haag,
Nederland, buitenland), rechts de lichte kaart van Den Haag (img/kaart-den-haag.svg van dereus-e7,
OpenStreetMap-data onder ODbL) met de bronvermelding zichtbaar eronder.
Geen wijken of plaatsen noemen tot De Reus ze bevestigt (open vraag 1.3).
"""
NAAM = "werkgebied"
CSS = True
JS = False

KAART = "/img/kaart-den-haag.svg"
ICONEN = {"hoofdkantoor": "pin", "nederland": "vrachtwagen", "internationaal": "wereld"}


def html(ctx, kopij, sectie="diep", **opties):
    k = kopij
    cfg = ctx.cfg
    regels = []
    for it in k.items:
        link = it.veld("link")
        linktekst = it.veld("linktekst")
        meer = (f'<a class="wg__link" href="{ctx.esc(link)}"><span>{ctx.inline(linktekst or "Lees meer")}</span>{ctx.icoon("pijl")}</a>'
                if link else "")
        regels.append(f'''<li class="wg__regel">
          <span class="wg__icoon" aria-hidden="true">{ctx.icoon(ICONEN.get(it.id, "pin"))}</span>
          <div>
            <h3 class="wg__titel">{ctx.inline(it.titel)}</h3>
            <p>{ctx.inline(it.veld("tekst"))}</p>
            {meer}
          </div>
        </li>''')
    alt = f"Kaart van Den Haag met het hoofdkantoor van {cfg.NAAM} aan de {cfg.STRAAT}"
    alineas = ctx.alineas(k.tekst, "wg__alinea")
    route = ""
    if k.veld("knop"):
        route = (f'<div class="knoppen"><a class="knop knop--licht" href="{ctx.esc(cfg.ROUTE)}" rel="noopener" target="_blank">'
                 f'{ctx.icoon("route")}<span>{ctx.inline(k.veld("knop"))}</span><span class="vh"> (opent OpenStreetMap in een nieuw tabblad)</span></a></div>')
    lijst = f'<ul class="wg__regels" role="list" data-reveal-groep>{"".join(regels)}</ul>' if regels else ""
    return f'''<section class="sectie sectie--{sectie} b-werkgebied" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap wg">
    <div class="wg__tekst">
      {ctx.kopgroep(k)}
      {alineas}
      {lijst}
      {route}
    </div>
    <figure class="wg__kaart" data-reveal>
      <div class="wg__kaartvlak">
        {ctx.beeld(KAART, alt, 1400, 933, klasse="wg__beeld")}
      </div>
      <figcaption class="wg__bron">Kaartgegevens © <a href="https://www.openstreetmap.org/copyright" rel="noopener" target="_blank">OpenStreetMap-bijdragers</a></figcaption>
    </figure>
  </div>
</section>'''
