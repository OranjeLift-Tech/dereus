"""Acht dienstsecties zonder zijbalk; bestaande ankers blijven bereikbaar.

Pagina: /diensten/. Kopij: de acht ##-blokken uit diensten.md (opties["kopij_ids"]).
Velden per blok: label (korte naam, ook de chiptekst), tekst, lijstkop, lijst, slot,
kosten-linktekst, kosten-link, knop, knop-schermlezer (wat een schermlezer achter de knoptekst hoort), en
optioneel pagina-linktekst en (bij particulier) doelgroepen-kop.
Heeft een dienst een eigen pagina die live is (config.PUBLICEER), dan linkt het paneel ernaar: met de knoptekst uit
pagina-linktekst, en anders via de kop van het paneel. Staat de pagina uit, dan verandert er niets.

Opbouw per paneel (sinds 28-09-2026, de gebruiker: "the 8 unique sections should have different stylings, use the
existing ones from the section-library"): elke dienst heeft een eigen patroon uit ../section-library, aangepast via
AGENTS.md (de beeld- en tekstvakken van de demo vervangen door de eigen foto, uitsnede en kopij). VORMEN legt vast welk
patroon bij welke dienst hoort; het staat als data-vorm op de sectie en de CSS kiest daarop de opbouw. De inhoud is
overal dezelfde: label, kop, alinea's, de lijst, de knoppen en de dienstfoto met de verhuizers die boven de fotorand
uitkomen. De volgorde in de HTML begint altijd met de tekst, zodat een schermlezer de kop eerst hoort. Op een telefoon
zetten vier patronen (fixed-price-cards, closing-panel-truck, text-photo-left, careers-split-crew) de foto met CSS
boven de tekst; de foto is niet focusbaar, dus de tabvolgorde blijft die van de HTML.

Elke dienst is een eigen sectie (sinds 28-09-2026, de gebruiker: "B bands should be their own sections"): acht
<section>-elementen direct in <main>, elk met het dienst-id als anker en de h2 als naam, dus acht regio's voor een
schermlezer. Tot dan waren het acht <article>-elementen in een naamloze sectie #diensten; niets linkt naar dat anker.
Het blok levert de acht secties achter elkaar; de paginadefinitie verandert daar niet voor.
"""

import sys

import _b4
from kit import WORTEL

NAAM = "dienstenpanelen"
CSS = True
JS = False

DIENSTEN = ["particulier", "zakelijk", "nationaal", "internationaal",
            "verhuislift", "opslag", "montage", "woningontruiming"]

# Welk patroon uit ../section-library elke dienst krijgt (de map heet zo in de bibliotheek). Elk patroon één keer.
VORMEN = {"particulier": "service-story-tabs", "zakelijk": "fixed-price-cards", "nationaal": "closing-panel-truck",
          "internationaal": "about-window-intro", "verhuislift": "text-photo-left", "opslag": "disc-callout-pills",
          "montage": "careers-split-crew", "woningontruiming": "two-col-checklist"}

# Welke dienstfoto in het paneel komt. Dezelfde kaart als in blok diensten (home).
FOTOS = {"particulier": "particulier-v2", "zakelijk": "zakelijk-v2", "nationaal": "nationaal-v2",
         "internationaal": "internationaal-v2b", "verhuislift": "verhuislift", "opslag": "opslag-v3",
         "montage": "montage-v2", "woningontruiming": "woningontruiming-v2"}


def _pop(beeldnaam):
    """Hoe ver de fotolaag boven het kader uitsteekt, als fractie van de kaderhoogte, of None.

    De getallen staan één keer in de repo: UITSTAP in blok diensten (home), berekend uit het alfamasker van de
    uitsnede (de kaderlijn ligt 11% van de beeldhoogte onder de bovenkant van de persoon). Dat blok is al geladen
    als dit blok rendert, want build.py laadt de blokken op alfabet. Zonder waarde komt er geen uitstap.
    """
    home = sys.modules.get("blokken_diensten")
    waarde = getattr(home, "UITSTAP", {}).get(beeldnaam, (None,))[0] if home else None
    return float(waarde.rstrip("%")) / 100 if waarde else None


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


def _beeld(ctx, k):
    """De foto in het kader met de uitsnede erover, of niets als de dienst geen foto heeft."""
    beeldnaam = FOTOS.get(k.id)
    if not beeldnaam:
        return "", ""
    foto = ctx.beeld(f"/img/dienst-{beeldnaam}.webp", "", 720, 540, klasse=f"b-{NAAM}__foto")
    uit, stijl = "", ""
    pop = _pop(beeldnaam)
    # de tweede test: zonder het bestand zou een export die nog niet gedraaid heeft een kapot beeld opleveren
    if pop is not None and (WORTEL / "img" / f"dienst-{beeldnaam}-uit.webp").exists():
        uit = f'<span class="b-{NAAM}__uit">{ctx.beeld(f"/img/dienst-{beeldnaam}-uit.webp", "", 1080, 810)}</span>'
        # de kaderlijn als fractie van de beeldhoogte: dezelfde knip als op de home, pop / (1 + pop)
        stijl = f' style="--dp-knip:{pop / (1 + pop):.4f}"'
    # Het kleiobject van de dienst op een hoek van het kader (sinds 28-09-2026, de gebruiker: "add slight hover effect
    # to the diensten sections like images moving just sligtly, and add more clay icons to them too"). Dezelfde
    # objecten als op de home-tegels; de hoek staat per patroon in de CSS, weg van de tekst en de hoofden.
    klei = ""
    if (WORTEL / "img" / "clay" / f"{k.id}-240.webp").exists():
        klei = ctx.beeld(f"/img/clay/{k.id}-240.webp", "", 240, 240, klasse=f"b-{NAAM}__klei")
    return (f'<div class="b-{NAAM}__kader" aria-hidden="true"><span class="b-{NAAM}__vak">{foto}</span>{uit}{klei}</div>',
            stijl)


def _paneel(ctx, k, nr):
    kaart = ""
    if k.lijst:
        kop = k.veld("lijstkop")
        kaart = (f'<div class="b-{NAAM}__kaart">'
                 + (f'<h3 class="b-{NAAM}__lijstkop">{ctx.inline(kop)}</h3>' if kop else "")
                 + f'<ul class="b-{NAAM}__lijst">' + "".join(f"<li>{ctx.inline(r)}</li>" for r in k.lijst)
                 + "</ul></div>")
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
    # De dienst in de naam van de knop (29-09-2026, SEO-ronde; Lighthouse identical-links-same-purpose): acht keer
    # "Offerte aanvragen" naar acht verschillende adressen. De zichtbare tekst blijft gelijk; een schermlezer hoort
    # knop-schermlezer erachter, dus de naam van de link begint met wat er te zien is.
    extra = k.veld("knop-schermlezer")
    if extra:
        knop = knop.replace("</span>", f'<span class="vh"> {ctx.esc(extra)}</span></span>', 1)
    # het label boven de kop is dezelfde naam als de chip die hierheen springt, met het volgnummer ervoor
    label = k.veld("label")
    label = (f'<p class="label b-{NAAM}__label"><span class="b-{NAAM}__nr">{nr:02d}</span>{ctx.inline(label)}</p>'
             if label else "")
    kader, stijl = _beeld(ctx, k)
    vorm = VORMEN.get(k.id, "service-story-tabs")
    # fixed-price-cards zet de losse opmerking in het goudgele vak onder de foto, de andere vormen in de tekst
    in_voet = vorm == "fixed-price-cards"
    tekst = (f'<div class="b-{NAAM}__tekst">{label}<h2 class="h2" id="{k.id}-kop">{kop}</h2>'
             f'{ctx.alineas(k.tekst)}{"" if in_voet else slot}{doelgroepen}</div>')
    acties = f'<p class="b-{NAAM}__acties">{knop}{meer}{kosten}</p>'
    # data-grond="donker" staat op het vlak waar de tekst wit wordt; de kleuren zelf staan in de CSS
    donker = ' data-grond="donker"'
    if vorm == "fixed-price-cards":
        # een witte kaart: tekst, de lijst als rijen en de knop links; rechts de foto in de hoek van de kaart, met de
        # verhuizers boven de kaartrand, en eronder het goudgele vak (in het patroon de korting) met de losse
        # opmerking en de kostenlink
        voet = f'<div class="b-{NAAM}__voet">{slot}{kosten}</div>' if slot or kosten else ""
        binnen = (f'<div class="b-{NAAM}__vlak"><div class="b-{NAAM}__kolom">{tekst}{kaart}'
                  f'<p class="b-{NAAM}__acties">{knop}{meer}</p></div>'
                  f'<div class="b-{NAAM}__beeld">{kader}</div>{voet}</div>')
    elif vorm == "closing-panel-truck":
        # een donker paneel op een lichte band; de foto staat op een schuin blok en steekt boven de paneelrand uit.
        # De lijst staat onder de foto: zo is de beeldkolom net zo vol als de tekstkolom.
        binnen = (f'<div class="b-{NAAM}__vlak"{donker}><div class="b-{NAAM}__kolom">{tekst}{acties}</div>'
                  f'<div class="b-{NAAM}__beeld">{kader}{kaart}</div></div>')
    elif vorm in ("about-window-intro", "text-photo-left"):
        # about-window-intro: de tekst op de donkere band, de foto in een boog die op de onderrand van de band staat.
        # text-photo-left: de foto links met een plaat achter de hoek, de tekst rechts.
        grond = donker if vorm == "about-window-intro" else ""
        binnen = (f'<div class="b-{NAAM}__kolom"{grond}>{tekst}{kaart}{acties}</div>'
                  f'<div class="b-{NAAM}__beeld">{kader}</div>')
    elif vorm == "disc-callout-pills":
        # sinds 29-09-2026 (ronde 2, de gebruiker hield versie 5 "Schijf"): rechts de tekst en de knoppen op de lichte
        # band; links de foto in een schijf met het hoofd erboven, en de lijst als pillen over de rand van de schijf.
        # De lijst staat na het kader: op een telefoon schuift hij onder de schijf over de onderrand.
        binnen = (f'<div class="b-{NAAM}__kolom">{tekst}{acties}</div>'
                  f'<div class="b-{NAAM}__beeld">{kader}{kaart}</div>')
    elif vorm == "careers-split-crew":
        # een witte kaart: links de tekst en de knoppen, rechts de foto in een schuin vlak met de verhuizer boven de
        # kaartrand, en de lijst als witte strook over de onderkant van de foto
        binnen = (f'<div class="b-{NAAM}__vlak"><div class="b-{NAAM}__kolom">{tekst}{acties}</div>'
                  f'<div class="b-{NAAM}__beeld">{kader}{kaart}</div></div>')
    elif vorm == "two-col-checklist":
        # een witte kaart: rechts de tekst en de knoppen (in het patroon het formulier), links de foto met een donkere
        # plank met een schuine, goudgele bovenrand erover, en daarop de lijst
        binnen = (f'<div class="b-{NAAM}__vlak"><div class="b-{NAAM}__kolom">{tekst}{acties}</div>'
                  f'<div class="b-{NAAM}__beeld">{kader}<div class="b-{NAAM}__plank"{donker}>{kaart}</div></div></div>')
    else:
        # service-story-tabs: tekst en knoppen links, rechts de foto op een schuin blok met de kaart eroverheen
        binnen = f'{tekst}<div class="b-{NAAM}__beeld">{kader}{kaart}</div>{acties}'
    # De sectie is de band: eigen grond via de klasse per dienst. De opbouw zit in .wrap, zodat de band van rand tot
    # rand loopt en de inhoud de breedte van de site houdt.
    # Geen .sectie: de band heeft een eigen padding, grond en naad. Met .sectie kreeg hij op brede schermen het
    # sectiemotief uit style.css op ::after (inset 0, z-index -2), en dat verving de naad naar de band erboven.
    return (f'<section class="b-{NAAM} b-{NAAM}--{k.id}" id="{k.id}" aria-labelledby="{k.id}-kop" data-b="{NAAM}" '
            f'data-vorm="{vorm}"{stijl}>\n      <div class="wrap b-{NAAM}__paneel">{binnen}</div>\n    </section>')


def html(ctx, kopij, **opties) -> str:
    ids = opties.get("kopij_ids") or DIENSTEN
    blokken = [ctx.kopij.blok(i) for i in ids]
    return "\n".join(_paneel(ctx, k, i + 1) for i, k in enumerate(blokken))
