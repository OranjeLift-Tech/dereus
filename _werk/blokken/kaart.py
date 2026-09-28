"""Adres en kaart (/contact/, #kaart). Sinds 28-09-2026 in de vorm van het werkgebied op de home ("Sectiestijlen
keuze: 7. Map and service area: A: Navy, three area rows and a tall map"): de Diepblauwe band, links de kop met
intro, het adres en de openingstijden als regels en de knoppen, rechts de kaart in de lagen van blok werkgebied
(gouden plaat, kaart, verhuizer, Koningsblauwe voetplaat met de bronvermelding). Die lagen staan in
css/blok/werkgebied.css; kaart.css zet alleen wat hier anders is. Hiervoor stond de kaart links in een eigen bord,
met het adres en de tijden in een witte plaat en een 3D-kantoortje ernaast (opzet De Kievit, "Waar u ons vindt").
Telefoon en e-mail staan niet hier maar in de kanaalkaarten van contactkaarten (design review 1.7, C1: het nummer
niet op elke plek).

Kopij: contact.md, blok {#kaart}: label, kop (het adres), intro, knop.
Gegevens (adres, telefoon, e-mail, tijden, route) komen uit config.py.
Optionele velden: label-adres, label-tijden, offerte-link, kaart-knop.
Het beeld is img/kaart-den-haag.svg (_werk/kaart/maak_kaart.py, OpenStreetMap-data, ODbL). Die getekende kaart is de
terugval in het paneel van blok wereld: een klik erop (of op de knop) laadt de echte kaart, een wereldbol die naar
Den Haag vliegt. Het adreskaartje van dat paneel staat in de HTML maar niet in beeld (kaart.css): de regels ernaast
tonen hetzelfde, en onderin staan hier de verhuizer en de voetplaat. wereld.js leest er de routelink uit voor de pin.
De verhuizer: /contact/ heeft de man met de deken al in contactkaarten en die met de zijgreep in het formulier, dus
hier de man met de twee dozen (live op de home, /over-ons/, /werkwijze/, /diensten/ en /kosten/).
"""

NAAM = "kaart"
CSS = True
JS = False
AFHANKELIJK = ["wereld", "werkgebied"]   # het paneel van de wereldbol, en de lagen en regels van het werkgebied

BEELD = "/img/kaart-den-haag.svg"
BREEDTE, HOOGTE = 1400, 933
MAN = ("/img/verhuizer-twee-dozen-uit.webp", 407, 1200)


def _dagen_attr(nummers):
    """Voor site.js: '1-6' voor maandag tot en met zaterdag, '0' voor zondag."""
    n = sorted(nummers)
    if len(n) > 1 and n == list(range(n[0], n[-1] + 1)):
        return f"{n[0]}-{n[-1]}"
    return ",".join(str(x) for x in n)


def tijden(ctx, klasse):
    rijen = []
    for t in ctx.cfg.TIJDEN:
        dagen = t["dagen"][:1].upper() + t["dagen"][1:]
        rijen.append(f'<div class="{klasse}__tijd" data-dagen="{_dagen_attr(t["nummers"])}">'
                     f'<dt>{ctx.esc(dagen)}</dt><dd>{ctx.esc(t["van"])} tot {ctx.esc(t["tot"])} uur</dd></div>')
    return f'<dl class="{klasse}__tijden">{"".join(rijen)}</dl>'


def _regel(ctx, soort, icoon, titel, inhoud):
    return f'''<li class="wg__regel b-{NAAM}__regel b-{NAAM}__regel--{soort}">
          <span class="wg__icoon" aria-hidden="true">{ctx.icoon(icoon)}</span>
          <div>
            <h3 class="wg__titel">{ctx.esc(titel)}</h3>
            {inhoud}
          </div>
        </li>'''


def html(ctx, kopij, man=MAN, **opties) -> str:
    k = kopij
    sid = opties.get("id", k.id or "kaart")
    grond = opties.get("grond", "diep")
    c = ctx.cfg
    alt = f"Kaart van Den Haag met de locatie van {c.NAAM} aan de {c.STRAAT}"
    regels = "".join([
        _regel(ctx, "adres", "pin", k.veld("label-adres", "Hoofdkantoor"),
               f'<address class="b-{NAAM}__waarde">{ctx.esc(c.STRAAT)}<br>{ctx.esc(c.POSTCODE)} {ctx.esc(c.PLAATS)}</address>'),
        _regel(ctx, "tijden", "klok", k.veld("label-tijden", "Bereikbaar"),
               tijden(ctx, f"b-{NAAM}") + f'<p class="b-{NAAM}__status">{ctx.bereikbaar("bereikbaar")}</p>'),
    ])
    route = ctx.knop(k.veld("knop", "Route plannen"), c.ROUTE, soort="licht", icoon="route",
                     klasse="knop--icoon-voor", attrs='rel="noopener"')
    offerte = ctx.knop(k.veld("offerte-link", "Offerte aanvragen"), "/offerte/", soort="link")
    msrc, mb, mh = man
    return f'''<section class="b-{NAAM} b-werkgebied sectie sectie--{grond}" id="{sid}" aria-labelledby="{sid}-kop">
  <div class="wrap wg">
    <div class="wg__tekst">
      {ctx.kopgroep(k)}
      <ul class="wg__regels" role="list" data-reveal-groep>{regels}</ul>
      <div class="knoppen">{route}{offerte}</div>
    </div>
    <figure class="wg__kaart" data-reveal>
      <span class="wg__plaat" aria-hidden="true"></span>
      <div class="wg__kaartvlak">
        <div class="wereld b-{NAAM}__wereld" data-wereld data-lat="{c.GEO[0]}" data-lng="{c.GEO[1]}">
          {ctx.beeld(BEELD, alt, BREEDTE, HOOGTE, klasse="wereld__terugval wg__beeld", sizes="(min-width: 900px) 40vw, 100vw")}
          <button class="wereld__start knop knop--licht" type="button" data-wereld-start>{ctx.icoon("wereld")}{ctx.esc(k.veld("kaart-knop", "Bekijk interactieve kaart"))}</button>
          <p class="wereld__melding vh" role="status" data-wereld-melding></p>
          <div class="wereld__info"><span class="wereld__ic">{ctx.icoon("pin")}</span><div>
            <address class="wereld__adres">{ctx.esc(c.STRAAT)}<br>{ctx.esc(c.POSTCODE)} {ctx.esc(c.PLAATS)}</address>
            <a class="wereld__route" href="{c.ROUTE}" rel="noopener">{ctx.esc(k.veld("knop", "Route plannen"))}{ctx.icoon("pijl")}</a>
          </div></div>
        </div>
      </div>
      {ctx.beeld(msrc, "", mb, mh, klasse="wg__man")}
      <figcaption class="wg__bron"><span>Kaartgegevens © <a href="https://www.openstreetmap.org/copyright" rel="noopener" target="_blank">OpenStreetMap-bijdragers</a></span></figcaption>
    </figure>
  </div>
</section>'''
