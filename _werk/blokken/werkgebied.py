"""Werkgebied (#werkgebied): de Diepblauwe band met dakrand. Links de kop met intro en drie regels (Den Haag,
Nederland, buitenland), rechts de lichte kaart van Den Haag (img/kaart-den-haag.svg van dereus-e7,
OpenStreetMap-data onder ODbL).
Geen wijken of plaatsen noemen tot De Reus ze bevestigt (open vraag 1.3).

Sinds 28-09-2026 op elke pagina deze vorm ("Sectiestijlen keuze: 7. Map and service area: A: Navy, three
area rows and a tall map"), en de kaart in lagen volgens het patroon area-rows-map-mover uit
../section-library ("add a worker cutout and the rectangles that other sections have"). Van achter naar voor:
een goudgele plaat links boven de kaart, de kaart, een verhuizer (MAN) die over de rechterrand van de kaart
stapt, en een Koningsblauwe voetplaat met de bronvermelding die zijn voeten bedekt en rechts uitsteekt.

Twee plekken:
  home #werkgebied       kopij uit home.md
  /over-ons/ #den-haag   eigen kop en intro, de regels via regels_van=("home", "werkgebied"), zodat ze op
                         één plek staan, en "knop" als routeknop eronder. alineas=False laat de alinea
                         van dat blok weg (zie de notitie in over-ons.md); met True staat hij onder de regels.
De verhuizer: een uitsnede van de hele man, alt leeg (gegenereerd beeld, het claimt niet wie het is). Een
pagina met deze man al elders kiest er een andere via man=(src, breedte, hoogte).
"""
NAAM = "werkgebied"
CSS = True
JS = False

KAART = "/img/kaart-den-haag.svg"
ICONEN = {"hoofdkantoor": "pin", "nederland": "vrachtwagen", "internationaal": "wereld"}
# De man met de deken en de hoge doos: live op /contact/, niet op de home of /over-ons/. Het logo op de doos
# loopt tot 88 procent van zijn hoogte, dus de voetplaat mag hooguit de onderste 10,7 procent bedekken.
MAN = ("/img/verhuizer-doos-deken-uit.webp", 698, 1200)


def html(ctx, kopij, sectie="diep", regels_van=None, alineas=True, man=MAN, **opties):
    k = kopij
    cfg = ctx.cfg
    items = ctx.kopij_van(regels_van[0]).blok(regels_van[1]).items if regels_van else k.items
    regels = []
    for it in items:
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
    alineas = ctx.alineas(k.tekst, "wg__alinea") if alineas else ""
    route = ""
    if k.veld("knop"):
        route = (f'<div class="knoppen"><a class="knop knop--licht" href="{ctx.esc(cfg.ROUTE)}" rel="noopener" target="_blank">'
                 f'{ctx.icoon("route")}<span>{ctx.inline(k.veld("knop"))}</span><span class="vh"> (opent OpenStreetMap in een nieuw tabblad)</span></a></div>')
    lijst = f'<ul class="wg__regels" role="list" data-reveal-groep>{"".join(regels)}</ul>' if regels else ""
    msrc, mb, mh = man
    return f'''<section class="sectie sectie--{sectie} b-werkgebied" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap wg">
    <div class="wg__tekst">
      {ctx.kopgroep(k)}
      {lijst}
      {alineas}
      {route}
    </div>
    <figure class="wg__kaart" data-reveal>
      <span class="wg__plaat" aria-hidden="true"></span>
      <div class="wg__kaartvlak">
        {ctx.beeld(KAART, alt, 1400, 933, klasse="wg__beeld")}
      </div>
      {ctx.beeld(msrc, "", mb, mh, klasse="wg__man")}
      <figcaption class="wg__bron"><span>Kaartgegevens © <a href="https://www.openstreetmap.org/copyright" rel="noopener" target="_blank">OpenStreetMap-bijdragers</a></span></figcaption>
    </figure>
  </div>
</section>'''
