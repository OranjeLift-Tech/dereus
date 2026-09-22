"""De vijf stappen als compacte tijdlijn: vijf stations op een goudgele lijn, elk met een 3D-render die
op het huis uit het logo staat en boven de kaartrand uitkomt.

Pagina: /werkwijze/. Kopij: ## ... {#stappen} met label, intro, u-label en wij-label, en per stap een
###-item (stap-1 tot stap-5) met tekst, u en wij. Het slot onderaan komt uit einde-titel, einde-tekst,
einde-linktekst en einde-link.

Waarom deze vorm: de rail (stappenlang) zette vijf volle kaarten onder elkaar, waardoor het overzicht
pas ontstond na de hele sectie. Hier staan de vijf stations naast elkaar op een lijn, zodat de route in
een oogopslag te zien is. Boven 1180 px loopt de lijn horizontaal door de huisjes; daaronder kantelt
dezelfde lijn naar verticaal en staan de huisjes in de linkermarge, zodat de lijn tussen de platen door
zichtbaar blijft in plaats van erachter te verdwijnen. Op 1440 px scheelt dat ruim 650 px hoogte.
De bouw van een plaat komt van /contact/: zichtbare dikte, een schaduw naar rechtsonder, en een render
voor het gele huis langs. Alles staat stil.

Knippen gebeurt hier en niet in de kopij. De kolommen zijn smal, dus van tekst, u en wij staat alleen de
eerste zin op de kaart. Wil een redacteur een andere korte regel, dan zet hij die in het veld kort: bij
de stap; dat veld gaat voor. website/content/werkwijze.md houdt zo de volledige tekst.

Een stapknop vervalt als hij naar dezelfde plek wijst als de knop in het slot: een sectie krijgt een
primaire handeling (website/review/design-notes.md, A5). De knop naar /kosten/ bij stap 3 blijft dus
staan, die naar /offerte/ bij stap 1 niet.

Beeld per stap: de renders staan hier vast, zoals stappenlang de lijniconen vastlegde. Het veld beeld:
in de kopij doet in dit blok niets. Dat wees naar de stapfoto's, en die vielen af op A3 (geen
stockfoto's van onbekende mensen); einde-alt hoort bij dezelfde vervallen foto.
"""
import re

NAAM = "tijdlijn"
CSS = True
JS = False

# Per station een 3D-render: map, bestandsnaam, breedte en hoogte. Bron: img/contact-3d/, img/kaart-3d/
# en img/kosten-3d/, dezelfde reeks als de kaarten op /contact/ en /kosten/. Een klok bij stap 4, want
# daar wordt de datum vastgezet; de wagen komt voorrijden bij stap 5.
VOORWERPEN = [
    ("contact-3d", "formulier", 346, 400),
    ("contact-3d", "telefoon", 208, 400),
    ("kaart-3d", "klembord", 600, 792),
    ("contact-3d", "klok", 279, 320),
    ("kosten-3d", "wagen", 594, 420),
]

# Het slot: het huis met de dozen ervoor, in plaats van de foto van een voordeur
SLOTBEELD = ("kosten-3d", "huis", 425, 420)

_ZIN = re.compile(r"(.+?[.?!])(\s|$)")


def _eerste_zin(tekst):
    m = _ZIN.match(tekst or "")
    return m.group(1) if m else (tekst or "")


def _kort(blok, sleutel):
    """De korte regel: het veld kort: als de redacteur er een zet, anders de eerste zin."""
    if sleutel == "tekst" and blok.veld("kort"):
        return blok.veld("kort")
    if sleutel != "tekst" and blok.veld(sleutel + "-kort"):
        return blok.veld(sleutel + "-kort")
    return _eerste_zin(blok.veld(sleutel))


def _render(ctx, map_, naam, breedte, hoogte):
    beeld = ctx.beeld(f"/img/{map_}/{naam}.webp", "", breedte, hoogte, klasse=f"b-{NAAM}__obj b-{NAAM}__obj--{naam}")
    return f'<span class="b-{NAAM}__ic" aria-hidden="true">{beeld}</span>'


def _stap(ctx, k, it, nr):
    duo = ""
    for sleutel in ("u", "wij"):
        if it.veld(sleutel):
            duo += (f'<div class="b-{NAAM}__wie b-{NAAM}__wie--{sleutel}"><dt>{ctx.inline(k.veld(sleutel + "-label"))}</dt>'
                    f'<dd>{ctx.inline(_kort(it, sleutel))}</dd></div>')
    duo = f'<dl class="b-{NAAM}__duo">{duo}</dl>' if duo else ""
    # de stapknop vervalt als hij hetzelfde doet als de slotknop (A5)
    link = ""
    href = it.veld("link")
    if href and href != k.veld("einde-link") and ctx.live(href):
        link = f'<p class="b-{NAAM}__meer">{ctx.knop(it.veld("linktekst"), href, soort="link")}</p>'
    map_, naam, breedte, hoogte = VOORWERPEN[(nr - 1) % len(VOORWERPEN)]
    return f'''<li class="b-{NAAM}__stap" id="{ctx.esc(it.id)}">
            {_render(ctx, map_, naam, breedte, hoogte)}
            <div class="b-{NAAM}__plaat">
              <p class="b-{NAAM}__nr" aria-hidden="true">{nr:02d}</p>
              <h3 class="b-{NAAM}__titel"><span class="vh">{ctx.esc(k.veld("stap-woord", "Stap"))} {nr}: </span>{ctx.inline(it.titel)}</h3>
              <p class="b-{NAAM}__regel">{ctx.inline(_kort(it, "tekst"))}</p>
              {duo}
              {link}
            </div>
          </li>'''


def _slot(ctx, k):
    """De afsluitende balk: het huis, de belofte en de enige primaire knop van de sectie."""
    titel = k.veld("einde-titel")
    if not titel:
        return ""
    tekst = k.veld("einde-tekst")
    knop = ctx.knop(k.veld("einde-linktekst"), k.veld("einde-link"), klasse=f"b-{NAAM}__cta") if k.veld("einde-link") else ""
    map_, naam, breedte, hoogte = SLOTBEELD
    beeld = ctx.beeld(f"/img/{map_}/{naam}.webp", "", breedte, hoogte, klasse=f"b-{NAAM}__obj b-{NAAM}__obj--{naam}")
    return f'''<div class="b-{NAAM}__slot" data-reveal>
          <span class="b-{NAAM}__ic b-{NAAM}__ic--slot" aria-hidden="true">{beeld}</span>
          <div class="b-{NAAM}__slottekst"><b>{ctx.inline(titel)}</b>{f"<p>{ctx.inline(tekst)}</p>" if tekst else ""}</div>
          {knop}
        </div>'''


def html(ctx, kopij, **opties) -> str:
    k = kopij
    grond = "mist" if opties.get("grond", "mist") == "mist" else "wit"
    stappen = "".join(_stap(ctx, k, it, i) for i, it in enumerate(k.items, 1))
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        {ctx.kopgroep(k, "kopgroep--midden")}
        <ol class="b-{NAAM}__lijst" role="list" data-reveal-groep>{stappen}</ol>
        {_slot(ctx, k)}
      </div>
    </section>'''
