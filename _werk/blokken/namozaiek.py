"""Na de verhuizing als mozaiek van vier tegels (/werkwijze/, #na-de-verhuizing).

Keuze van de gebruiker uit website/review/werkwijze-na-de-verhuizing-r7-20260923/, versie 3 "Mozaiek":
"Versie 3 (Mozaiek): houden". Vervangt het blok naplaten op deze pagina; naplaten zelf blijft bestaan.
De kop breed in een witte tegel, de foto hoog ernaast, en daaronder de twee punten als een Diepblauwe en een
zachtgele tegel, elk met een eigen 3D-voorwerp dat van de rand valt. Alles staat stil (css/blok/namozaiek.css).

Kopij: werkwijze.md, blok {#na-de-verhuizing}: label, kop, intro en een lijst van twee regels die elk beginnen
met een vette kop: "**Tevreden?** uitleg". De vette kop wordt de titel van de tegel.
Optie foto: (pad, breedte, hoogte) van de foto in de hoge tegel. Die is nodig: zonder foto blijft er een leeg
vak in het raster staan.
Optie foto_srcset: een srcset voor die foto, zodat een scherm op 1x de kleine versie laadt. De sizes erbij
staat hieronder (FOTO_SIZES) en volgt de tegel uit de CSS.
"""
import re

NAAM = "namozaiek"
CSS = True
JS = False

# Per tegel: de naam (de CSS kent precies deze twee, met een eigen kleur en plek in het raster), de
# trefwoorden in de vette kop die bij die tegel horen, en het 3D-voorwerp: map, bestandsnaam, breedte, hoogte.
# Voor "tevreden" de gouden ster en niet de reviewkaart img/contact-3d/score.webp: die draagt het logo van
# Google (zie naplaten.py).
TEGELS = [
    ("vragen", ("vraag",), ("contact-3d", "telefoon", 208, 400)),
    ("tevreden", ("tevreden", "review"), ("kaart-3d", "ster", 240, 240)),
]

# Hoe breed de foto getekend wordt. Hij vult de tegel met object-fit: cover, dus vanaf 1024 (drie kolommen,
# tegel hoger dan 4:3) bepaalt de hoogte van de tegel de breedte: rond 480 hoog is 640 breed. Daaronder
# is de tegel breder dan 4:3 en telt zijn eigen breedte: de helft van het scherm, en op de telefoon het
# hele scherm min de marges.
FOTO_SIZES = "(max-width: 659.98px) calc(100vw - 2rem), (max-width: 1023.98px) 50vw, 40rem"

_VET = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$")


def _deel(regel):
    """Splitst '**Kop.** uitleg' in (kop, uitleg). Zonder vette kop is de hele regel de uitleg."""
    m = _VET.match(regel)
    return (m.group(1), m.group(2)) if m else ("", regel)


def _tegel(kop, plek):
    """De tegel bij deze vette kop; zonder trefwoord valt hij terug op de volgorde in de kopij."""
    t = kop.lower()
    for tegel in TEGELS:
        if any(w in t for w in tegel[1]):
            return tegel
    return TEGELS[min(plek, len(TEGELS) - 1)]


def html(ctx, kopij, **opties) -> str:
    k = kopij
    if not k.lijst:
        return ""
    if len(k.lijst) != len(TEGELS):
        ctx.waarschuw(f"namozaiek: {len(k.lijst)} punten in #{k.id}, het raster heeft plek voor {len(TEGELS)}")
    punten = []
    for plek, regel in enumerate(k.lijst):
        kop, uitleg = _deel(regel)
        naam, _, (map_, ding, b, h) = _tegel(kop, plek)
        titel = f'<h3 class="b-{NAAM}__titel">{ctx.inline(kop)}</h3>' if kop else ""
        voorwerp = ctx.beeld(f"/img/{map_}/{ding}.webp", "", b, h, klasse=f"b-{NAAM}__ding b-{NAAM}__ding--{ding}")
        punten.append(f'''<li class="b-{NAAM}__tegel b-{NAAM}__tegel--{naam}">
              {titel}
              <p>{ctx.inline(uitleg)}</p>
              {voorwerp}
            </li>''')
    # alt leeg: de foto illustreert de kop ernaast en voegt er niets aan toe
    foto = ""
    if opties.get("foto"):
        src, breed, hoog = opties["foto"]
        srcset = opties.get("foto_srcset")
        foto = ctx.beeld(src, "", breed, hoog, klasse=f"b-{NAAM}__foto",
                         srcset=srcset, sizes=FOTO_SIZES if srcset else None)
    else:
        ctx.waarschuw(f"namozaiek: geen foto voor #{k.id}, de hoge tegel blijft leeg")
    intro = f'<p class="intro b-{NAAM}__intro">{ctx.inline(k.veld("intro"))}</p>' if k.veld("intro") else ""
    return f'''<section class="b-{NAAM} sectie sectie--mist" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div class="b-{NAAM}__raster">
          <div class="b-{NAAM}__tegel b-{NAAM}__tegel--kop">
            {ctx.label(k.veld("label"))}
            <h2 id="{ctx.esc(k.id)}-kop">{ctx.inline(k.kop)}</h2>
            {intro}
          </div>
          <div class="b-{NAAM}__tegel b-{NAAM}__tegel--foto">{foto}</div>
          <ul class="b-{NAAM}__punten" role="list">
            {"".join(punten)}
          </ul>
        </div>
      </div>
    </section>'''
