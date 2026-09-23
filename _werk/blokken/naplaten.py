"""Twee brede platen die een pagina afsluiten (/werkwijze/, #na-de-verhuizing).

Dezelfde plaat als de vertrouwensrij op /contact/: wit, met een zichtbare dikte en één schaduw, allebei naar
rechtsonder. Boven elke plaat staat het goudgele huis uit het logo met daarvoor een 3D-voorwerp uit img/contact-3d,
dat over de bovenrand heen komt. Groter dan de platen in een lijstsectie, zodat twee punten als slot lezen en niet
als nog een lijstje. Alles staat stil (css/blok/naplaten.css).

Optie beeld: (pad, bestand_breed, bestand_hoog, x, y, w, h) zet de kop links en een uitsnede rechts, op de
gedeelde plaat uit css/blok/uitsnede.css (zelfde behandeling als "Zo werken wij" en "Kennismaken?"). De foto
komt NAAST de twee platen, niet in plaats van de 3D-voorwerpen: die voorwerpen benoemen elk hun eigen plaat
(headset = vragen, ster = review) en zijn de vormtaal die dit blok deelt met de vertrouwensrij op /contact/.
De pagina moet dan extra_css=("uitsnede",) hebben. Zonder de optie blijft de kop gecentreerd zoals hij was.

Kopij: werkwijze.md, blok {#na-de-verhuizing}: label, kop, intro en een lijst waarvan elke regel begint met een
vette kop, zoals bij checklist: "**Tevreden?** uitleg". Opties: grond ("mist" of "wit").
Het voorwerp volgt uit die vette kop; staat er geen voorwerp bij, dan blijft het lijnicoon in het goudgele huis staan.
"""
import re

NAAM = "naplaten"
CSS = True
JS = False

# Per trefwoord in de vette kop het 3D-voorwerp: map, bestandsnaam, breedte en hoogte.
# Dezelfde renders als de vertrouwensrij op /contact/, met één uitzondering: voor "tevreden" staat hier de
# gouden ster en niet de reviewkaart img/contact-3d/score.webp. Die kaart draagt het logo van Google, het merk
# van een ander bedrijf, en staat daarom op de afkeurlijst van website/review/beeldcontrole/rapport.md.
VOORWERP = [
    ("vraag", ("contact-3d", "headset", 287, 320)),
    ("vragen", ("contact-3d", "headset", 287, 320)),
    ("tevreden", ("kaart-3d", "ster", 240, 240)),
    ("review", ("kaart-3d", "ster", 240, 240)),
    ("verzeker", ("contact-3d", "schild", 251, 320)),
    ("bericht", ("contact-3d", "envelop", 347, 400)),
    ("bel", ("contact-3d", "telefoon", 208, 400)),
]

# Zonder voorwerp valt het blok terug op een lijnicoon in het goudgele huis, net als de vertrouwensrij.
ICOON = [("vraag", "persoon"), ("tevreden", "ster"), ("review", "ster"), ("bel", "telefoon")]

# Voorwerpen die zelf goudgeel zijn, krijgen een wit huis achter zich in plaats van een goudgeel:
# twee keer dezelfde kleur wordt één vlek. Dezelfde uitzondering als de Googlekaart in de vertrouwensrij.
LICHT_HUIS = {"ster"}

_VET = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$")


def _deel(regel):
    """Splitst '**Kop.** uitleg' in (kop, uitleg). Zonder vette kop is de hele regel de uitleg."""
    m = _VET.match(regel)
    return (m.group(1), m.group(2)) if m else ("", regel)


def _voorwerp(kop):
    t = kop.lower()
    for sleutel, gegevens in VOORWERP:
        if sleutel in t:
            return gegevens
    return None


def _icoon(kop):
    t = kop.lower()
    for sleutel, naam in ICOON:
        if sleutel in t:
            return naam
    return "check"


def _beeld(ctx, kop):
    """Het goudgele huis met daarvoor het voorwerp. Het huis zelf staat in de CSS, als ::before en ::after."""
    gegevens = _voorwerp(kop)
    if gegevens:
        map_, naam, b, h = gegevens
        licht = f" b-{NAAM}__huis--licht" if naam in LICHT_HUIS else ""
        # met de hand opgebouwd en dus zonder loading="lazy": het voorwerp staat boven de vouw zodra
        # de sectie in beeld komt, en een laat beeld laat de plaat zichtbaar verspringen
        return (f'<span class="b-{NAAM}__huis{licht}" aria-hidden="true"><img class="b-{NAAM}__obj b-{NAAM}__obj--{naam}" '
                f'src="/img/{map_}/{naam}.webp" alt="" width="{b}" height="{h}" decoding="async"></span>')
    return f'<span class="b-{NAAM}__huis b-{NAAM}__huis--icoon" aria-hidden="true">{ctx.icoon(_icoon(kop))}</span>'


def html(ctx, kopij, **opties) -> str:
    k = kopij
    if not k.lijst:
        return ""
    grond = "wit" if opties.get("grond") == "wit" else "mist"
    platen = []
    for regel in k.lijst:
        kop, uitleg = _deel(regel)
        titel = f'<b class="b-{NAAM}__titel">{ctx.inline(kop)}</b>' if kop else ""
        platen.append(f'''<li class="b-{NAAM}__plaat">
            {_beeld(ctx, kop)}
            {titel}
            <p>{ctx.inline(uitleg)}</p>
          </li>''')
    beeld = opties.get("beeld")
    if beeld:
        src, breed, hoog, ux, uy, uw, uh = beeld
        # alt leeg: de uitsnede illustreert de kop ernaast en voegt er niets aan toe
        foto = ctx.beeld(src, "", breed, hoog, klasse=f"uitsnede__beeld b-{NAAM}__foto")
        maten = f"--uit-breed:{breed};--uit-hoog:{hoog};--uit-x:{ux};--uit-y:{uy};--uit-w:{uw};--uit-h:{uh}"
        hoofd = (f'<div class="b-{NAAM}__hoofd">{ctx.kopgroep(k, klasse=f"b-{NAAM}__tekst")}'
                 f'<div class="uitsnede b-{NAAM}__beeld" style="{maten}" data-reveal>{foto}</div></div>')
    else:
        hoofd = ctx.kopgroep(k, klasse="kopgroep--midden")
    return f'''<section class="b-{NAAM} b-{NAAM}--{grond} sectie sectie--{grond}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        {hoofd}
        <ul class="b-{NAAM}__rij" role="list" data-reveal-groep>{"".join(platen)}</ul>
      </div>
    </section>'''
