"""Adres en kaart (/contact/, #kaart), opgezet zoals "Waar u ons vindt" op de contactpagina van De Kievit:
links de kaart in een afgeronde kaart met een adrespil, rechts het adres als kop, een korte tekst, twee
gegevenskaarten (adres en openingstijden met de bereikbaarheidsstatus) en de knoppen. Telefoon en e-mail staan niet
hier maar in de kanaalkaarten van contactkaarten (design review 1.7, C1: het nummer niet op elke plek).

Kopij: contact.md, blok {#kaart}: label, kop (het adres), intro, knop.
Gegevens (adres, telefoon, e-mail, tijden, route) komen uit config.py.
Optionele velden: label-adres, label-tijden, offerte-link.
Het beeld is img/kaart-den-haag.svg (_werk/kaart/maak_kaart.py, OpenStreetMap-data, ODbL): geen embed.
"""

NAAM = "kaart"
CSS = True
JS = False

BEELD = "/img/kaart-den-haag.svg"
BREEDTE, HOOGTE = 1400, 933


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


def _gegeven(ctx, soort, icoon, label, inhoud):
    return f'''<li class="b-{NAAM}__gegeven b-{NAAM}__gegeven--{soort}">
              <span class="b-{NAAM}__ic" aria-hidden="true">{ctx.icoon(icoon)}</span>
              <div><p class="b-{NAAM}__lbl">{ctx.esc(label)}</p>{inhoud}</div>
            </li>'''


def html(ctx, kopij, **opties) -> str:
    k = kopij
    sid = opties.get("id", k.id or "kaart")
    grond = opties.get("grond", "mist")
    c = ctx.cfg
    alt = f"Kaart van Den Haag met de locatie van {c.NAAM} aan de {c.STRAAT}"
    gegevens = "".join([
        _gegeven(ctx, "adres", "pin", k.veld("label-adres", "Hoofdkantoor"),
                 f'<address class="b-{NAAM}__waarde">{ctx.esc(c.STRAAT)}<br>{ctx.esc(c.POSTCODE)} {ctx.esc(c.PLAATS)}</address>'),
        _gegeven(ctx, "tijden", "klok", k.veld("label-tijden", "Bereikbaar"),
                 tijden(ctx, f"b-{NAAM}") + f'<p class="b-{NAAM}__status">{ctx.bereikbaar("bereikbaar")}</p>'),
    ])
    route = ctx.knop(k.veld("knop", "Route plannen"), c.ROUTE, soort="blauw", icoon="route",
                     klasse="knop--icoon-voor", attrs='rel="noopener"')
    offerte = ctx.knop(k.veld("offerte-link", "Offerte aanvragen"), "/offerte/", soort="link")
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap b-{NAAM}__in">
        <figure class="b-{NAAM}__beeld" data-reveal>
          <div class="b-{NAAM}__venster">{ctx.beeld(BEELD, alt, BREEDTE, HOOGTE, klasse=f"b-{NAAM}__img", sizes="(min-width: 1024px) 40vw, 100vw")}</div>
          <p class="b-{NAAM}__pil">{ctx.icoon("pin")}<span>{ctx.esc(c.STRAAT)}, {ctx.esc(c.PLAATS)}</span></p>
          <figcaption class="b-{NAAM}__bron">Kaartgegevens © <a href="https://www.openstreetmap.org/copyright" rel="noopener">OpenStreetMap-bijdragers</a></figcaption>
        </figure>
        <div class="b-{NAAM}__tekst">
          {ctx.kopgroep(k, klasse=f"b-{NAAM}__kop")}
          <ul class="b-{NAAM}__gegevens" role="list" data-reveal-groep>{gegevens}</ul>
          <div class="knoppen">{route}{offerte}</div>
        </div>
      </div>
    </section>'''
