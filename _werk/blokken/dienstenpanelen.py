"""Acht dienstenpanelen zonder zijbalk; bestaande ankers blijven bereikbaar.

Pagina: /diensten/. Kopij: de acht ##-blokken uit diensten.md (opties["kopij_ids"]).
Velden per blok: label (korte naam voor de index), tekst, lijstkop, lijst, slot,
kosten-linktekst, kosten-link, knop, en optioneel pagina-linktekst en (bij particulier) doelgroepen-kop.
Heeft een dienst een eigen pagina die live is (config.PUBLICEER), dan linkt het paneel ernaar: met de knoptekst uit
pagina-linktekst, en anders via de kop van het paneel. Staat de pagina uit, dan verandert er niets.
"""

import _b4
from kit import WORTEL

NAAM = "dienstenpanelen"
CSS = True
JS = False

DIENSTEN = ["particulier", "zakelijk", "nationaal", "internationaal",
            "verhuislift", "opslag", "montage", "woningontruiming"]

# Welke dienstfoto in het huis komt. Dezelfde kaart als in blok diensten (home); alleen montage
# wijkt af, want dat beeld heet handyman.
FOTOS = {"particulier": "particulier", "zakelijk": "zakelijk", "nationaal": "nationaal",
         "internationaal": "internationaal", "verhuislift": "verhuislift", "opslag": "opslag",
         "montage": "handyman", "woningontruiming": "woningontruiming"}

# Van welke dienstfoto een uitsnede zonder achtergrond bestaat (/img/dienst-<naam>-uit.webp, uit
# _ai-beelden/diensten-uitsnede.mjs + diensten-uit-export.cjs). Die laag komt over de foto heen
# zonder in de huisvorm geknipt te worden, dus de verhuizer stapt uit het huis. Bij handymanservice
# is het geen persoon maar de hand met de boor die naar buiten komt (uitsnede met de hand gemaakt:
# _ai-beelden/handyman-uitsnede.cjs; de maatvoering staat bij paneel 07 in de CSS).
UITSNEDEN = {"particulier", "zakelijk", "nationaal", "internationaal", "verhuislift", "opslag",
             "handyman", "woningontruiming"}


def _met_tel(ctx, tekst):
    """Opgemaakte tekst, met het telefoonnummer als tel-link (handig op een telefoon).

    Een punt die direct achter het nummer staat laten we weg. ctx.contactlinks hangt de
    WhatsApp-knop aan de tel-link vast en die moet er onmiddellijk op volgen, anders komt er een
    tweede bij; de punt zou dan achter de knop belanden en als een typefout lezen.
    """
    t = ctx.inline(tekst)
    if ctx.tel not in t:
        return t
    link = f'<a href="{ctx.telhref}">{ctx.tel}</a>'
    return t.replace(f"{ctx.tel}.", link, 1) if f"{ctx.tel}." in t else t.replace(ctx.tel, link, 1)


def _paneel(ctx, k, nr):
    lijst = ""
    if k.lijst:
        kop = k.veld("lijstkop")
        lijst = (f'<h3 class="b-{NAAM}__lijstkop">{ctx.inline(kop)}</h3>' if kop else "") + \
            f'<ul class="b-{NAAM}__lijst">' + "".join(f"<li>{ctx.inline(r)}</li>" for r in k.lijst) + "</ul>"
    slot = k.veld("slot")
    slot = f'<p class="b-{NAAM}__slot">{_met_tel(ctx, slot)}</p>' if slot else ""
    kosten = ""
    if k.veld("kosten-link"):
        kosten = ctx.knop(k.veld("kosten-linktekst"), k.veld("kosten-link"), soort="link")
    pagina = _b4.dienst_href(ctx, k.id)
    eigen_pagina = not pagina.startswith("/diensten/#")
    kop = ctx.inline(k.kop)
    meer = ""
    if eigen_pagina and k.veld("pagina-linktekst"):
        meer = ctx.knop(k.veld("pagina-linktekst"), pagina, soort="link")
    elif eigen_pagina:
        kop = f'<a href="{ctx.esc(pagina)}">{kop}</a>'
    doelgroepen = ""
    if k.id == "particulier":
        # doelgroeppagina's die live staan: de naam is de H1 van die pagina. Zonder live pagina's komt er niets.
        links = "".join(f'<li><a href="{ctx.esc(pad)}">{ctx.inline(ctx.kopij_van(naam).h1.kop)}</a></li>'
                        for pad, naam in _b4.DOELGROEPEN if ctx.live(pad) and ctx.kopij_van(naam).h1)
        if links:
            kopje = f'<p class="b-{NAAM}__lijstkop">{ctx.inline(k.veld("doelgroepen-kop"))}</p>' if k.veld("doelgroepen-kop") else ""
            doelgroepen = f'{kopje}<ul class="b-{NAAM}__doelgroepen">{links}</ul>'
    # "Offerte aanvragen" heeft overal de CTA-stijl (besluit van de gebruiker, via dereus-28): de kleur komt uit de
    # tokens --color-cta van de kernlaag, dit blok legt zelf geen knopkleur vast
    knop = ctx.knop(k.veld("knop"), f"/offerte/?dienst={k.id}", soort="cta")
    # De dienstfoto wordt in de huisvorm uit het logo geknipt; het merkicoon blijft als tegel op de hoek.
    # De uitsnede gaat er onafgeknipt overheen: wat het dak wegneemt steekt zo uit het huis (zie de CSS).
    beeldnaam = FOTOS.get(k.id)
    foto = uit = ""
    if beeldnaam:
        foto = ctx.beeld(f"/img/dienst-{beeldnaam}.webp", "", 720, 540, klasse=f"b-{NAAM}__foto")
        # UITSNEDEN zegt wélke dienst een uitsnede hóórt te hebben; de tweede test of het bestand er
        # ook echt is. Zonder die test levert een export die nog niet gedraaid heeft een kapot beeld
        # op de pagina in plaats van een paneel zonder uitstap.
        if beeldnaam in UITSNEDEN and (WORTEL / "img" / f"dienst-{beeldnaam}-uit.webp").exists():
            uit = f'<span class="b-{NAAM}__uit">{ctx.beeld(f"/img/dienst-{beeldnaam}-uit.webp", "", 1080, 810)}</span>'
    # elk paneel heeft een eigen stijl (grond, kaderkleur, opsomming); de klasse per dienst stuurt dat in de CSS
    return f'''<article class="b-{NAAM}__paneel b-{NAAM}__paneel--{k.id}" id="{k.id}" aria-labelledby="{k.id}-kop">
      <div class="b-{NAAM}__beeld" aria-hidden="true">
        <span class="b-{NAAM}__nr">{nr:02d}</span>
        <span class="b-{NAAM}__kader"><span class="b-{NAAM}__huis">{foto}</span>{uit}<span class="b-{NAAM}__merk">{ctx.dienst_icoon(k.id, inline=True)}</span></span>
      </div>
      <div class="b-{NAAM}__tekst">
        <h2 class="h2" id="{k.id}-kop">{kop}</h2>
        {ctx.alineas(k.tekst)}
        {lijst}
        {slot}
        {doelgroepen}
        <p class="b-{NAAM}__acties">{knop}{meer}{kosten}</p>
      </div>
    </article>'''


def html(ctx, kopij, **opties) -> str:
    ids = opties.get("kopij_ids") or DIENSTEN
    blokken = [ctx.kopij.blok(i) for i in ids]
    panelen = "".join(_paneel(ctx, k, i + 1) for i, k in enumerate(blokken))
    return f'''<section class="b-{NAAM} sectie sectie--mist" id="{opties.get("id", "diensten")}" data-b="{NAAM}">
      <div class="wrap b-{NAAM}__in">
        <div class="b-{NAAM}__panelen">{panelen}</div>
      </div>
    </section>'''
