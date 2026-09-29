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

Sinds 28-09-2026 uit website/review/werkgebied-20260928/r2/ ("add the arrows, the offerte buttons, the adresplaat"):
  route=True        de gouden routelijn met pijlpunten tussen de tegels (versie 2, Routelijn)
  adresplaat=True   het adres met een routelink op de linkerbovenhoek van de kaart (versie 3, Adresplaat)
  acties=True       "Offerte aanvragen" en de belknop onder de regels (versie 5, Offerte en bellen)
/over-ons/ zet adresplaat en acties uit: het adres en de routeknop staan daar al, en het grote formulier volgt direct.

Sinds 29-09-2026 staan in de gele tegels echte voorwerpen in plaats van lijniconen, zoals op /contact/ #kaart: "bu
bölümdeki figürleri de gerçek ve kutudan çıkacakmış gibi yap". Den Haag de blauwe punaise (dezelfde als op /contact/),
Nederland de bakwagen van De Reus (uitsnede uit img/footer-wagen-breed.webp), het buitenland een wereldbol (Unsplash).
Bestanden en bronnen: VOORWERP hieronder, img/LICENTIES.md en _ai-beelden/contact-echt/LEESMIJ.md.
"""
NAAM = "werkgebied"
CSS = True
JS = False

KAART = "/img/kaart-den-haag.svg"
ICONEN = {"hoofdkantoor": "pin", "nederland": "vrachtwagen", "internationaal": "wereld"}
# icoon -> (bestand in img/contact-echt, breedte 1x, breedte 2x, hoogte 1x, sizes). Een icoon zonder voorwerp blijft
# een lijnicoon in de tegel.
VOORWERP = {
    "pin": ("punaise", 44, 88, 76, "2.75rem"),           # Unsplash 46Tg56viOUg, ook op /contact/ #kaart
    "vrachtwagen": ("bakwagen", 96, 192, 63, "5.6rem"),  # eigen beeld (5.2rem onder 1280 px), img/footer-wagen-breed.webp
    "wereld": ("wereldbol", 58, 116, 86, "3.6rem"),      # Unsplash 9tmrYLRL7Ww
}
# De man met de deken en de hoge doos: live op /contact/, niet op de home of /over-ons/. Het logo op de doos
# loopt tot 88 procent van zijn hoogte, dus de voetplaat mag hooguit de onderste 10,7 procent bedekken.
MAN = ("/img/verhuizer-doos-deken-uit.webp", 698, 1200)


def _tegel(ctx, icoon):
    if icoon in VOORWERP:
        naam, b, b2, h, maat = VOORWERP[icoon]
        pad = f"/img/contact-echt/{naam}"
        return (f'<span class="wg__icoon wg__tegel wg__tegel--{naam}" aria-hidden="true"><img class="wg__obj wg__obj--{naam}" '
                f'src="{pad}-{b}.webp" srcset="{pad}-{b}.webp {b}w, {pad}-{b2}.webp {b2}w" '
                f'sizes="{maat}" alt="" width="{b}" height="{h}" loading="lazy" decoding="async"></span>')
    return f'<span class="wg__icoon" aria-hidden="true">{ctx.icoon(icoon)}</span>'


def html(ctx, kopij, sectie="diep", regels_van=None, alineas=True, man=MAN, route=True, adresplaat=True, acties=True, **opties):
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
          {_tegel(ctx, ICONEN.get(it.id, "pin"))}
          <div>
            <h3 class="wg__titel">{ctx.inline(it.titel)}</h3>
            <p>{ctx.inline(it.veld("tekst"))}</p>
            {meer}
          </div>
        </li>''')
    alt = f"Kaart van Den Haag met het hoofdkantoor van {cfg.NAAM} aan de {cfg.STRAAT}"
    alineas = ctx.alineas(k.tekst, "wg__alinea") if alineas else ""
    nieuw_tabblad = '<span class="vh"> (opent OpenStreetMap in een nieuw tabblad)</span>'
    routeknop = ""
    if k.veld("knop"):
        routeknop = (f'<div class="knoppen"><a class="knop knop--licht" href="{ctx.esc(cfg.ROUTE)}" rel="noopener" target="_blank">'
                     f'{ctx.icoon("route")}<span>{ctx.inline(k.veld("knop"))}</span>{nieuw_tabblad}</a></div>')
    knoppen = ""
    if acties:
        knoppen = (f'<div class="knoppen wg__acties">{ctx.knop("Offerte aanvragen", "/offerte/")}'
                   f'{ctx.knop(f"Bel {cfg.TEL}", cfg.TELHREF, soort="licht", icoon="telefoon", klasse="knop--icoon-voor", attrs="data-geen-whatsapp")}</div>')
    plaat = ""
    if adresplaat:
        plaat = (f'<div class="wg__adres"><span class="wg__adres-ic" aria-hidden="true">{ctx.icoon("pin")}</span><div>'
                 f'<p><strong>{ctx.esc(cfg.STRAAT)}</strong>{ctx.esc(cfg.POSTCODE)} {ctx.esc(cfg.PLAATS)}</p>'
                 f'<a class="wg__link" href="{ctx.esc(cfg.ROUTE)}" rel="noopener" target="_blank"><span>Route plannen</span>{ctx.icoon("pijl")}{nieuw_tabblad}</a>'
                 f'</div></div>')
    soort = "wg__regels wg__regels--route" if route else "wg__regels"
    lijst = f'<ul class="{soort}" role="list" data-reveal-groep>{"".join(regels)}</ul>' if regels else ""
    msrc, mb, mh = man
    return f'''<section class="sectie sectie--{sectie} b-werkgebied" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap wg">
    <div class="wg__tekst">
      {ctx.kopgroep(k)}
      {lijst}
      {knoppen}
      {alineas}
      {routeknop}
    </div>
    <figure class="wg__kaart" data-reveal>
      <span class="wg__plaat" aria-hidden="true"></span>
      <div class="wg__kaartvlak">
        {ctx.beeld(KAART, alt, 1400, 933, klasse="wg__beeld")}
      </div>
      {ctx.beeld(msrc, "", mb, mh, klasse="wg__man")}
      {plaat}
      <figcaption class="wg__bron"><span>Kaartgegevens © <a href="https://www.openstreetmap.org/copyright" rel="noopener" target="_blank">OpenStreetMap-bijdragers</a></span></figcaption>
    </figure>
  </div>
</section>'''
