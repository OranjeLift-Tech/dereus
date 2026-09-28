"""Na de verhuizing als Diepblauwe kaart op een schuine gele band (/werkwijze/, #na-de-verhuizing).

Keuze van de gebruiker uit _ontwerpen/na-de-verhuizing-varianten.html, nummer 03 "Gele schuine band"
(28-09-2026), naar het opslagblok van referentie A ("Even geen plek?"). Vervangt het blok namozaiek op deze
pagina; namozaiek zelf blijft bestaan. Een schuine Goudgele band met een Diepblauwe streep eronder loopt door
de Mist-sectie. Links een Diepblauwe kaart met label, kop, intro, de twee punten als rijen met een echt
klei-icoon op een gele schijf (VOORWERP, anders een rond lijnicoon) en de knoppen; rechts staat de ploeg met dozen op de band. Alles staat stil (css/blok/naband.css).

Kopij: werkwijze.md, blok {#na-de-verhuizing}: label, kop, intro en een lijst van twee regels die elk beginnen
met een vette kop: "**Tevreden?** uitleg". De vette kop wordt de titel van de rij.
Knoppen: het telefoonnummer (build.py hangt er de WhatsApp-knop achter) en de Google-reviews, beide uit config.
Optie beeld: False laat de ploeg weg (dan is de kaart het hele blok).
"""
import re

NAAM = "naband"
CSS = True
JS = False

# Per rij: de trefwoorden in de vette kop en het icoon ervoor. Zonder trefwoord telt de volgorde.
PUNTEN = [
    (("vraag",), "telefoon"),
    (("tevreden", "review"), "ster"),
]

# Per icoon het voorwerp dat op een gele schijf staat (28-09-2026, "figuren echt maken"). Sinds de samenvoeging
# van 28-09-2026 de klei-iconen (img/clay/<naam>-144/240.webp, vierkant) in plaats van de 3D-renders, dezelfde
# twee als in het mozaiek dat hier eerst stond. Een icoon zonder voorwerp blijft een lijnicoon.
VOORWERP = {"telefoon", "ster"}

# De ploeg met dozen (dezelfde uitsnede als de team-hero, img/team/team-hero-dozen.json).
BEELD = "/img/team/team-hero-dozen"
BEELD_MATEN = (1100, 1195)
BEELD_SRCSET = ", ".join(f"{BEELD}-{b}.webp {b}w" for b in (700, 1100, 1600))
# Vanaf 960 staat de ploeg in de rechterkolom en wordt hij hoogstens 600 breed; daaronder de volle breedte.
BEELD_SIZES = "(max-width: 959.98px) calc(100vw - 2rem), 37.5rem"

_VET = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$")


def _deel(regel):
    """Splitst '**Kop.** uitleg' in (kop, uitleg). Zonder vette kop is de hele regel de uitleg."""
    m = _VET.match(regel)
    return (m.group(1), m.group(2)) if m else ("", regel)


def _icoon(kop, plek):
    t = kop.lower()
    for woorden, icoon in PUNTEN:
        if any(w in t for w in woorden):
            return icoon
    return PUNTEN[min(plek, len(PUNTEN) - 1)][1]


def html(ctx, kopij, beeld=True, **opties) -> str:
    k = kopij
    if not k.lijst:
        return ""
    punten = []
    for plek, regel in enumerate(k.lijst):
        kop, uitleg = _deel(regel)
        titel = f'<h3 class="b-{NAAM}__titel">{ctx.inline(kop)}</h3>' if kop else ""
        icoon = _icoon(kop, plek)
        if icoon in VOORWERP:
            teken = (f'<span class="b-{NAAM}__icoon b-{NAAM}__icoon--3d" aria-hidden="true"><img class="b-{NAAM}__obj b-{NAAM}__obj--{icoon}" '
                     f'src="/img/clay/{icoon}-240.webp" srcset="/img/clay/{icoon}-144.webp 144w, /img/clay/{icoon}-240.webp 240w" '
                     f'sizes="4.4rem" alt="" width="240" height="240" loading="lazy" decoding="async"></span>')
        else:
            teken = f'<span class="b-{NAAM}__icoon">{ctx.icoon(icoon)}</span>'
        punten.append(f'''<li class="b-{NAAM}__punt">
              {teken}
              <div>{titel}<p>{ctx.inline(uitleg)}</p></div>
            </li>''')
    intro = f'<p class="intro">{ctx.inline(k.veld("intro"))}</p>' if k.veld("intro") else ""
    knoppen = (f'<a class="b-{NAAM}__knop b-{NAAM}__knop--bel" href="{ctx.telhref}">{ctx.icoon("telefoon")}{ctx.esc(ctx.tel)}</a>'
               f'<a class="b-{NAAM}__knop b-{NAAM}__knop--review" href="{ctx.esc(ctx.cfg.GOOGLE_PROFIEL)}" rel="noopener" target="_blank">'
               f'{ctx.icoon("google")}<span>Review op Google</span><span class="vh"> (opent Google in een nieuw tabblad)</span></a>')
    # alt leeg: de ploeg illustreert de kaart ernaast en voegt er niets aan toe
    ploeg = ""
    if beeld:
        breed, hoog = BEELD_MATEN
        ploeg = f'<div class="b-{NAAM}__beeld">{ctx.beeld(f"{BEELD}-1100.webp", "", breed, hoog, klasse=f"b-{NAAM}__ploeg", srcset=BEELD_SRCSET, sizes=BEELD_SIZES)}</div>'
    return f'''<section class="b-{NAAM} sectie sectie--mist" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="b-{NAAM}__band" aria-hidden="true"></div>
      <div class="wrap">
        <div class="b-{NAAM}__raster">
          <div class="b-{NAAM}__kaart">
            {ctx.label(k.veld("label"), f"b-{NAAM}__label")}
            <h2 id="{ctx.esc(k.id)}-kop">{ctx.inline(k.kop)}</h2>
            {intro}
            <ul class="b-{NAAM}__punten" role="list">
              {"".join(punten)}
            </ul>
            <div class="b-{NAAM}__knoppen">{knoppen}</div>
          </div>
          {ploeg}
        </div>
      </div>
    </section>'''
