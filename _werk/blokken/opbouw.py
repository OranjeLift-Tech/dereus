"""Hoe de prijs tot stand komt: de prijsfactoren als kaarten, daaronder all-in prijs tegenover regieprijs.

Pagina: /kosten/. Kopij: ## ... {#opbouw} met label, intro, lijstkop, lijst (regels in de vorm "**Kop.** uitleg"),
slot, en items: de eerste twee staan tegenover elkaar (all-in en regie), de rest komt als strook eronder.
"""
import re

NAAM = "opbouw"
CSS = True
JS = False

_FACTOR = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$")

# Optie voorwerpen (/kosten/): per factor een voorwerp op een gele schijf. Sinds 28-09-2026 de klei-iconen
# (img/clay/<naam>-240/480.webp, vierkant; website/review/clay-iconen-20260928/) in plaats van de 3D-renders uit
# img/kosten-3d/. Het vak is 11.6 rem hoog met object-fit contain; vormgeving in css/blok/opbouw-3d.css.
# Sinds 29-09-2026 staat bij dozen, trap en opslag het De Reus-logo op de dozen (<naam>-logo-240/480.webp, zelfde
# klei-icoon met het kleurenlogo in perspectief op de zijkant gezet; de gewone iconen blijven voor de andere pagina's).
VOORWERPEN = ["dozen-logo", "nationaal", "trap-logo", "montage", "opslag-logo"]

# Optie duo="foto" (/kosten/, 29-09-2026): all-in prijs en regieprijs als het blok "Een verhuislift of opslag
# erbij" van referentie C (.b-liftopslag__duo: twee foto's die op een schuine naad tegen elkaar staan, met een
# schijf op de naad, en een witte kaart met een rond icoon die over de onderkant van elke foto valt). De gebruiker
# vond de twee betaalpassen geen blok. Per item-id: foto, breedte, hoogte, icoon, uitsnede (object-position).
# All-in: de offerte die getekend wordt (één vast bedrag zoals in de offerte). Regie: de verhuizers aan het werk
# (de tijd die de verhuizing werkelijk kost).
FOTODUO = {
    "all-in": ("/img/stap-3-offerte.webp", 560, 380, "document", "50% 38%"),
    "regie": ("/img/verhuisdag-uitladen.webp", 1400, 1050, "klok", "50% 14%"),
}

# Optie stijl="balie" (/kosten/, 29-09-2026): ontwerp 05 uit _ontwerpen/prijsopbouw-referentie-varianten-2.html, naar
# het vensterblok van referentie A (.venster: een figuur voor een boog, het beeldmerk als watermerk). Een Goudgele band
# met dakrand. Links de kop en de vijf factoren als lichte plaatjes met een Diepblauwe schijf (wit bij hover, wens van
# de gebruiker), rechts het huis uit het logo als wit venster met drie lachende verhuizers ervoor. Een witte balie
# schuift voor de verhuizers langs met all-in prijs en regieprijs en de slottekst als voet; daaronder de twee
# zekerheden als Diepblauwe pillen. Vormgeving in css/blok/opbouw-balie.css (via extra_css, na kosten-diepte).
BALIE_PLOEG = ("/img/review-verhuizers-lachend-breed.webp", 914, 504)
# Per item-id een echt voorwerp uit img/contact-echt/ (dezelfde reeks als /contact/): naam, breedte 1x en 2x,
# hoogte 1x, sizes. All-in: het klembord met de offerte, regie: de wekker, voorrijkosten: de bakwagen, betalen: munten.
BALIE_VOORWERP = {
    "all-in": ("klembord", 136, 272, 218, "(max-width:700px) 4.3rem, 5.5rem"),
    "regie": ("wekker", 96, 192, 144, "(max-width:700px) 4.3rem, 5.5rem"),
    "voorrijkosten": ("bakwagen", 96, 192, 63, "4.4rem"),
    "betalen": ("munten", 80, 160, 55, "4.4rem"),
}
# het huis uit het logo (zelfde vorm als --huisje in css/style.css), viewBox 0 0 535.3 509.8
HUIS = "M267.6 7.8L320.9 53.2V0H356.8V83.9L535.3 236.2H457.6V509.8H326.2V384.1H209.1V509.8H77.7V236.2H0Z"


def _vak(ctx, it):
    """Een helft van het fotoduo: foto, dan de kaart met icoon, kop en tekst."""
    foto = ""
    if it.id in FOTODUO:
        src, b, h, ic, snede = FOTODUO[it.id]
        foto = (f'<figure class="b-{NAAM}__foto" style="--snede:{snede}">'
                f'{ctx.beeld(src, "", b, h, sizes="(max-width:760px) 92vw, 50vw")}</figure>')
        ic = f'<span class="b-{NAAM}__ic" aria-hidden="true">{ctx.icoon(ic)}</span>'
    else:
        ic = ""
    return (f'<article class="b-{NAAM}__vak" id="{it.id}">{foto}<div class="b-{NAAM}__vakkaart">{ic}'
            f'<h3 class="b-{NAAM}__vakkop">{ctx.inline(it.kop)}</h3>{ctx.alineas(it.tekst)}</div></article>')


def _factor(ctx, regel, nr, voorwerp=None):
    m = _FACTOR.match(regel)
    kop, uitleg = (m.group(1).rstrip("."), m.group(2)) if m else (regel, "")
    podium = ""
    if voorwerp:
        podium = (f'<span class="b-{NAAM}__podium" aria-hidden="true"><img class="b-{NAAM}__obj" src="/img/clay/{voorwerp}-240.webp" '
                  f'srcset="/img/clay/{voorwerp}-240.webp 240w, /img/clay/{voorwerp}-480.webp 480w" '
                  f'sizes="(max-width:479px) 6.8rem, (max-width:799px) 9.8rem, 11.6rem" alt="" '   # de hoogte van het vak in opbouw-3d.css
                  f'width="240" height="240" loading="lazy" decoding="async"></span>')
    return (f'<li class="b-{NAAM}__factor">{podium}<span class="b-{NAAM}__nr" aria-hidden="true">{nr:02d}</span>'
            f'<h3 class="b-{NAAM}__factorkop">{ctx.inline(kop)}</h3><p>{ctx.inline(uitleg)}</p></li>')


def _soort(ctx, it, klasse=""):
    lijst = "".join(f"<li>{ctx.inline(r)}</li>" for r in it.lijst)
    lijst = f"<ul>{lijst}</ul>" if lijst else ""
    return (f'<article class="b-{NAAM}__soort {klasse}" id="{it.id}"><h3 class="b-{NAAM}__soortkop">{ctx.inline(it.kop)}</h3>'
            f'{ctx.alineas(it.tekst)}{lijst}</article>')


def _balie_voorwerp(ctx, item_id, klasse):
    if item_id not in BALIE_VOORWERP:
        return ""
    naam, b1, b2, h1, sizes = BALIE_VOORWERP[item_id]
    basis = f"/img/contact-echt/{naam}"
    return ctx.beeld(f"{basis}-{b1}.webp", "", b1, h1, klasse=klasse, sizes=sizes,
                     srcset=f"{basis}-{b1}.webp {b1}w, {basis}-{b2}.webp {b2}w")


def _balie(ctx, k, opties):
    """stijl="balie": de gele band met de verhuizers achter de prijsbalie (zie BALIE_PLOEG hierboven)."""
    punten = []
    for i, regel in enumerate(k.lijst):
        m = _FACTOR.match(regel)
        kop, uitleg = (m.group(1).rstrip("."), m.group(2)) if m else (regel, "")
        punten.append(f'<li class="b-{NAAM}__punt"><span class="b-{NAAM}__schijf" aria-hidden="true">{i + 1:02d}</span>'
                      f'<div><h3 class="b-{NAAM}__puntkop">{ctx.inline(kop)}</h3><p>{ctx.inline(uitleg)}</p></div></li>')
    duo, rest = (k.items[:2], k.items[2:]) if len(k.items) >= 2 else ([], k.items)

    def lijst(it):
        rijen = "".join(f"<li>{ctx.inline(r)}</li>" for r in it.lijst)
        return f"<ul>{rijen}</ul>" if rijen else ""

    of = f'<span class="b-{NAAM}__keuzeof" aria-hidden="true">{ctx.esc(opties.get("of", "of"))}</span>'
    prijzen = of.join(f'<article class="b-{NAAM}__prijs" id="{it.id}">{_balie_voorwerp(ctx, it.id, "b-" + NAAM + "__voorwerp")}'
                      f'<h3 class="b-{NAAM}__prijskop">{ctx.inline(it.kop)}</h3>{ctx.alineas(it.tekst)}{lijst(it)}</article>'
                      for it in duo)
    pillen = "".join(f'<li class="b-{NAAM}__pil" id="{it.id}">{_balie_voorwerp(ctx, it.id, "b-" + NAAM + "__pilbeeld")}'
                     f'<div><h3 class="b-{NAAM}__pilkop">{ctx.inline(it.kop)}</h3>{ctx.alineas(it.tekst)}{lijst(it)}</div></li>'
                     for it in rest)
    pillen = f'<ul class="b-{NAAM}__pillen" data-reveal-groep>{pillen}</ul>' if pillen else ""
    voet = f'<p class="b-{NAAM}__voet">{ctx.inline(k.veld("slot"))}</p>' if k.veld("slot") else ""
    balie = f'<div class="b-{NAAM}__balie" data-reveal><div class="b-{NAAM}__keuze">{prijzen}</div>{voet}</div>' if prijzen else voet
    intro = f'<p class="b-{NAAM}__intro">{ctx.inline(k.veld("intro"))}</p>' if k.veld("intro") else ""
    lijstkop = f'<h3 class="b-{NAAM}__lijstkop">{ctx.inline(k.veld("lijstkop"))}</h3>' if k.veld("lijstkop") else ""
    merk = ctx.beeld(ctx.logo("beeldmerk"), "", 1000, 509, klasse=f"b-{NAAM}__merk")
    ploeg = ctx.beeld(BALIE_PLOEG[0], "", BALIE_PLOEG[1], BALIE_PLOEG[2], klasse=f"b-{NAAM}__ploeg")
    huis = (f'<svg class="b-{NAAM}__huis" viewBox="0 0 535.3 509.8" focusable="false"><path class="b-{NAAM}__huisvlak" d="{HUIS}"/>'
            f'<path class="b-{NAAM}__huislijn" d="{HUIS}" transform="translate(29.4 36) scale(.89)"/></svg>')
    return f'''<section class="b-{NAAM} b-{NAAM}--balie sectie sectie--wit" id="{k.id}" aria-labelledby="{k.id}-kop" data-b="{NAAM}">
      {merk}
      <div class="wrap">
        <div class="b-{NAAM}__raster">
          <div class="b-{NAAM}__links">
            <div class="b-{NAAM}__kop" data-reveal>
              {ctx.label(k.veld("label"))}
              <h2 class="h2" id="{k.id}-kop">{ctx.inline(k.kop)}</h2>
              {intro}{ctx.alineas(k.tekst)}
            </div>
            {lijstkop}
            <ol class="b-{NAAM}__punten" data-reveal-groep>{"".join(punten)}</ol>
          </div>
          <div class="b-{NAAM}__team" aria-hidden="true">{huis}{ploeg}</div>
        </div>
        {balie}
        {pillen}
      </div>
    </section>'''


def html(ctx, kopij, **opties) -> str:
    k = kopij
    if opties.get("stijl") == "balie":
        return _balie(ctx, k, opties)
    drie_d = bool(opties.get("voorwerpen"))
    factoren = "".join(_factor(ctx, r, i + 1, VOORWERPEN[i] if drie_d and i < len(VOORWERPEN) else None) for i, r in enumerate(k.lijst))
    accolade = f'<div class="b-{NAAM}__accolade" aria-hidden="true"></div>' if drie_d else ""
    variant = f" b-{NAAM}--3d" if drie_d else ""
    lijstkop = f'<h3 class="b-{NAAM}__lijstkop">{ctx.inline(k.veld("lijstkop"))}</h3>' if k.veld("lijstkop") else ""
    duo, rest = k.items[:2], k.items[2:]
    duo_html = ""
    if len(duo) == 2 and opties.get("duo") == "foto":
        duo_html = (f'<div class="b-{NAAM}__duo b-{NAAM}__duo--foto" data-reveal>{_vak(ctx, duo[0])}'
                    f'<span class="b-{NAAM}__naad" aria-hidden="true">{ctx.esc(opties.get("of", "of"))}</span>'
                    f'{_vak(ctx, duo[1])}</div>')
    elif len(duo) == 2:
        duo_html = (f'<div class="b-{NAAM}__duo" data-reveal>{_soort(ctx, duo[0], "b-" + NAAM + "__soort--a")}'
                    f'<span class="b-{NAAM}__of" aria-hidden="true">{ctx.esc(opties.get("of", "of"))}</span>'
                    f'{_soort(ctx, duo[1], "b-" + NAAM + "__soort--b")}</div>')
    else:
        rest = k.items
    rest_html = "".join(_soort(ctx, it, "b-" + NAAM + "__soort--strook") for it in rest)
    rest_html = f'<div class="b-{NAAM}__stroken" data-reveal-groep>{rest_html}</div>' if rest_html else ""
    slot = f'<p class="b-{NAAM}__slot">{ctx.inline(k.veld("slot"))}</p>' if k.veld("slot") else ""
    intro = f'<p class="b-{NAAM}__intro">{ctx.inline(k.veld("intro"))}</p>' if k.veld("intro") else ""
    return f'''<section class="b-{NAAM}{variant} sectie sectie--mist" id="{k.id}" aria-labelledby="{k.id}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div class="b-{NAAM}__kop" data-reveal>
          {ctx.label(k.veld("label"))}
          <h2 class="h2" id="{k.id}-kop">{ctx.inline(k.kop)}</h2>
          {intro}{ctx.alineas(k.tekst)}
        </div>
        {lijstkop}
        <ol class="b-{NAAM}__factoren" data-reveal-groep>{factoren}</ol>
        {accolade}
        {duo_html}
        {slot}
        {rest_html}
      </div>
    </section>'''
