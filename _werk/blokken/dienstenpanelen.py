"""Acht dienstsecties, elk met een eigen compositie; de bestaande ankers blijven bereikbaar.

Pagina: /diensten/. Kopij: de acht ##-blokken uit diensten.md (opties["kopij_ids"]).
Velden per blok: label (korte naam voor de index), tekst, lijstkop, lijst, slot,
kosten-linktekst, kosten-link, knop, en optioneel pagina-linktekst en (bij particulier) doelgroepen-kop.
Heeft een dienst een eigen pagina die live is (config.PUBLICEER), dan linkt het paneel ernaar: met de knoptekst uit
pagina-linktekst, en anders via de kop van het paneel. Staat de pagina uit, dan verandert er niets.

Waarom acht composities en niet acht sjablonen: de kopij geeft per dienst alleen een kop, een label, twee tot drie
alinea's, twee tot vier lijstregels, knoppen en een foto. Er zijn nergens ###-items, dus de patronen uit de
bibliotheek die op k.items draaien (kaartenrij, treden, stappenlang, verhuisdag, kernwaarden, kortestappen) kunnen
hier niet gevuld worden zonder kopij te verzinnen. De afwisseling komt daarom uit de indeling van wat er wel staat.
De taal blijft één: dezelfde labels met volgnummer, dezelfde kopmaat, dezelfde knoppen, hetzelfde sectieritme.
Per dienst ligt de variant vast in VARIANTEN, met de ondergrond erbij (STIJLANALYSE 2.5: hoogstens één donkere
band per pagina, en die staat achter een witte sectie zodat de nok van het dak zichtbaar blijft).
"""

import re

import _b4

NAAM = "dienstenpanelen"
CSS = True
JS = False

DIENSTEN = ["particulier", "zakelijk", "nationaal", "internationaal",
            "verhuislift", "opslag", "montage", "woningontruiming"]
FOTOS = {"montage": "handyman"}

# dienst -> (variant, ondergrond). De volgorde wit, mist, wit, blauw, wit, mist, wit, mist houdt het ritme
# en zet de enige blauwe band achter een witte sectie (kernlaag: .sectie--wit + .sectie--blauw).
VARIANTEN = {
    "particulier": ("venster", "wit"),
    "zakelijk": ("kaart", "mist"),
    "nationaal": ("band", "wit"),
    "internationaal": ("grens", "blauw"),
    "verhuislift": ("staand", "wit"),
    "opslag": ("situaties", "mist"),
    "montage": ("citaat", "wit"),
    "woningontruiming": ("rustig", "mist"),
}

# "Een klant schreef erover: "De montage liep vlekkeloos."": een hele zin aan het eind van een alinea die eindigt
# op een citaat tussen aanhalingstekens. Wordt los gezet, met dezelfde woorden in dezelfde volgorde.
_CITAATZIN = re.compile(r'(?:^|(?<=[.!?])\s+)([^.!?]*:\s*"[^"]+")\s*$')
_CITAATDELEN = re.compile(r'^(.*?:)\s*("[^"]+")$')


def _met_tel(ctx, tekst):
    """Opgemaakte tekst, met het telefoonnummer als tel-link (handig op een telefoon)."""
    t = ctx.inline(tekst)
    return t.replace(ctx.tel, f'<a href="{ctx.telhref}">{ctx.tel}</a>', 1) if ctx.tel in t else t


def _lijstkop(ctx, k):
    kop = k.veld("lijstkop")
    return f'<p class="b-{NAAM}__lijstkop">{ctx.inline(kop)}</p>' if kop else ""


def _vinkjes(ctx, k):
    """De standaardlijst: vinkjes uit de kernlaag (.vinklijst), zodat blauw en licht vanzelf goed staan."""
    if not k.lijst:
        return ""
    li = "".join(f'<li>{ctx.icoon("check")}<span>{ctx.inline(r)}</span></li>' for r in k.lijst)
    return f'<ul class="vinklijst b-{NAAM}__vinkjes">{li}</ul>'


def _rijen(ctx, k):
    """Twee of drie regels als brede rijen met een haarlijn ertussen: geeft een korte lijst gewicht."""
    if not k.lijst:
        return ""
    li = "".join(f'<li><span class="b-{NAAM}__vak" aria-hidden="true">{ctx.icoon("check")}</span>'
                 f'<span>{ctx.inline(r)}</span></li>' for r in k.lijst)
    return f'<ul class="b-{NAAM}__rijen">{li}</ul>'


def _situaties(ctx, k):
    """De regels onder "Handig als" zijn situaties, geen diensten. Daarom kaarten en geen vinkjes."""
    if not k.lijst:
        return ""
    li = "".join(f'<li class="b-{NAAM}__situatie">{ctx.inline(r)}</li>' for r in k.lijst)
    return f'<ul class="b-{NAAM}__situaties">{li}</ul>'


def _slot(ctx, k):
    slot = k.veld("slot")
    return f'<p class="b-{NAAM}__slot">{_met_tel(ctx, slot)}</p>' if slot else ""


def _doelgroepen(ctx, k):
    """Alleen bij particulier, en alleen zolang die pagina's live staan. Staat er niets live, dan komt er niets:
    de compositie van dat paneel mag er niet van afhangen (afspraak met dereus-35)."""
    if k.id != "particulier":
        return ""
    links = "".join(f'<li><a href="{ctx.esc(pad)}">{ctx.inline(ctx.kopij_van(naam).h1.kop)}</a></li>'
                    for pad, naam in _b4.DOELGROEPEN if ctx.live(pad) and ctx.kopij_van(naam).h1)
    if not links:
        return ""
    kopje = (f'<p class="b-{NAAM}__lijstkop">{ctx.inline(k.veld("doelgroepen-kop"))}</p>'
             if k.veld("doelgroepen-kop") else "")
    return f'{kopje}<ul class="b-{NAAM}__doelgroepen">{links}</ul>'


def _acties(ctx, k, pagina, eigen_pagina, klasse=""):
    """"Offerte aanvragen" heeft overal de CTA-stijl (besluit van de gebruiker, via dereus-28): de kleur komt uit
    de tokens --color-cta van de kernlaag, dit blok legt zelf geen knopkleur vast."""
    knop = ctx.knop(k.veld("knop"), f"/offerte/?dienst={k.id}", soort="cta")
    meer = ctx.knop(k.veld("pagina-linktekst"), pagina, soort="link") if eigen_pagina and k.veld("pagina-linktekst") else ""
    kosten = ctx.knop(k.veld("kosten-linktekst"), k.veld("kosten-link"), soort="link") if k.veld("kosten-link") else ""
    k_ = f'b-{NAAM}__acties {klasse}'.strip()
    return f'<p class="{k_}">{knop}{meer}{kosten}</p>'


def _kop(ctx, k, nr, kop_html, klasse="", extra=""):
    k_ = f'b-{NAAM}__kop {klasse}'.strip()
    return f'''<header class="{k_}">
          {extra}
          <p class="label"><span aria-hidden="true">{nr:02d} · </span>{ctx.esc(k.veld('label') or k.kop)}</p>
          <h2 class="h2" id="{k.id}-kop">{kop_html}</h2>
        </header>'''


def _foto(ctx, k, vorm, sizes, huis=False):
    """De foto is versiering: de kopij draagt de betekenis. Elke vorm snijdt met object-fit, zodat het ontwerp
    niet afhangt van één uitsnede of beeldverhouding."""
    bestand = FOTOS.get(k.id, k.id)
    beeld = ctx.beeld(f'/img/dienst-{bestand}.webp', '', 720, 540, klasse=f'b-{NAAM}__foto', sizes=sizes)
    binnen = f'<div class="huisvenster">{beeld}</div>' if huis else beeld
    return f'<div class="b-{NAAM}__beeld b-{NAAM}__beeld--{vorm}" aria-hidden="true">{binnen}</div>'


def _tekst_met_citaat(ctx, k):
    """Alinea's van montage, met de klantzin los gezet als citaat, op de plek waar hij in de kopij staat.
    Dezelfde woorden, dezelfde volgorde, geen naam erbij: het is typografie, geen herschrijving.
    Past het patroon niet, dan blijft de alinea gewoon staan."""
    delen, gevonden = [], False
    for a in k.tekst or []:
        m = None if gevonden else _CITAATZIN.search(a)
        if not m:
            delen.append(f"<p>{ctx.inline(a)}</p>")
            continue
        gevonden = True
        rest = a[:m.start(1)].strip()
        if rest:
            delen.append(f"<p>{ctx.inline(rest)}</p>")
        stukken = _CITAATDELEN.match(m.group(1))
        aanhef, woorden = (stukken.group(1), stukken.group(2)) if stukken else ("", m.group(1))
        aanhef = f'<p class="b-{NAAM}__citaataanhef">{ctx.inline(aanhef)}</p>' if aanhef else ""
        delen.append(f'<figure class="b-{NAAM}__citaat">'
                     f'<span class="b-{NAAM}__citaatmerk" aria-hidden="true">{ctx.icoon("quote")}</span>'
                     f'{aanhef}<blockquote><p>{ctx.inline(woorden)}</p></blockquote></figure>')
    return "".join(delen)


# ---- de acht composities ------------------------------------------------
# Elke functie krijgt de gedeelde onderdelen al opgemaakt binnen (delen) en bepaalt alleen de indeling.
# De kop staat overal náást de tekst in het raster, niet erin. Op één kolom leest het daardoor altijd in de
# volgorde kop, beeld, tekst; op twee kolommen zet het raster de kop bij de tekstkolom.

def _venster(ctx, k, d):
    """01 particulier: het huisvormige kader uit het logo, één keer op de pagina (STIJLANALYSE 6.5), bij de
    dienst met de meeste kopij. De doelgroeplinks hangen er los onder, zodat het paneel ook klopt als ze wegvallen."""
    return f'''<div class="wrap b-{NAAM}__in b-{NAAM}__in--venster">
        {d["kop"]}
        {_foto(ctx, k, "huis", "(min-width: 961px) 40vw, 100vw", huis=True)}
        <div class="b-{NAAM}__tekst">
          {d["alineas"]}{d["lijstkop"]}{_vinkjes(ctx, k)}{d["doelgroepen"]}{d["slot"]}{d["acties"]}
        </div>
      </div>'''


def _kaart(ctx, k, d):
    """02 zakelijk: de vier regels en de slotzin in een witte kaart met haarlijn, als de afspraak vooraf.
    De kaart ligt over de volle breedte onder de tekst en de foto, zodat geen van beide kolommen leeg uitloopt."""
    return f'''<div class="wrap b-{NAAM}__in b-{NAAM}__in--kaart">
        {d["kop"]}
        {_foto(ctx, k, "vullend", "(min-width: 961px) 42vw, 100vw")}
        <div class="b-{NAAM}__tekst">{d["alineas"]}</div>
        <div class="b-{NAAM}__onder">
          <div class="b-{NAAM}__afspraak">{d["lijstkop"]}{_vinkjes(ctx, k)}{d["slot"]}</div>
          {d["acties"]}
        </div>
      </div>'''


def _band(ctx, k, d):
    """03 nationaal: een brede beeldband over de volle kolom. Breedte is het enige middel dat afstand laat zien
    zonder kaart of getal, en die staan niet in de kopij. De kop staat boven de band: anders landt het anker
    op de foto en valt de kop op een laag scherm buiten beeld."""
    return f'''<div class="wrap">
        {d["kopmet"](f"b-{NAAM}__kop--band")}
        {_foto(ctx, k, "breed", "(min-width: 1281px) 1200px, 100vw")}
        <div class="b-{NAAM}__in b-{NAAM}__in--band">
          <div class="b-{NAAM}__tekst">{d["alineas"]}{d["acties"]}</div>
          <div class="b-{NAAM}__naast">{d["lijstkop"]}{_vinkjes(ctx, k)}</div>
        </div>
      </div>'''


def _grens(ctx, k, d):
    """04 internationaal: de enige blauwe band van de pagina. Geen foto en geen kaart: wereld.py levert geen
    markup, er is geen wereldkaart in img/, en de kopij mag geen landen noemen. Het accent geeft het gewicht."""
    wereld = f'<span class="b-{NAAM}__wereld" aria-hidden="true">{ctx.icoon("wereld")}</span>'
    return f'''<div class="wrap">
        {d["kopmet"](f"b-{NAAM}__kop--midden", wereld)}
        <div class="b-{NAAM}__in b-{NAAM}__in--grens">
          <div class="b-{NAAM}__tekst">{d["alineas"]}</div>
          <div class="b-{NAAM}__naast">{d["lijstkop"]}{_vinkjes(ctx, k)}</div>
        </div>
        {_acties(ctx, k, d["pagina"], d["eigen_pagina"], klasse=f"b-{NAAM}__acties--midden")}
      </div>'''


def _staand(ctx, k, d):
    """05 verhuislift: staand beeld, en de twee regels als brede rijen. Twee vinkjes naast vier elders oogt
    mager; rijen geven ze gewicht. Een echte specificatiekaart kan pas als de maten bekend zijn
    (open vragen 1.6 en 2.4), tot dan staat er geen enkel getal in de kopij."""
    return f'''<div class="wrap b-{NAAM}__in b-{NAAM}__in--staand">
        {d["kop"]}
        {_foto(ctx, k, "staand", "(min-width: 961px) 34vw, 100vw")}
        <div class="b-{NAAM}__tekst">
          {d["alineas"]}{d["lijstkop"]}{_rijen(ctx, k)}{d["acties"]}
        </div>
      </div>'''


def _situatiepaneel(ctx, k, d):
    """06 opslag: "Handig als" is een rij situaties, geen dienstenlijst. Kaarten onder elkaar naast een hoge
    foto, zodat het paneel ook anders staat dan zakelijk."""
    return f'''<div class="wrap b-{NAAM}__in b-{NAAM}__in--situaties">
        {d["kop"]}
        {_foto(ctx, k, "hoog", "(min-width: 961px) 38vw, 100vw")}
        <div class="b-{NAAM}__tekst">
          {d["alineas"]}
          {_lijstkop(ctx, k)}{_situaties(ctx, k)}
          {d["acties"]}
        </div>
      </div>'''


def _citaat(ctx, k, d):
    """07 montage: de enige dienst met een klantzin in de kopij. Die zin komt uit een echte review
    (website/content/home.md) en wordt hier alleen anders gezet, zonder naam erbij."""
    return f'''<div class="wrap b-{NAAM}__in b-{NAAM}__in--citaat">
        {d["kop"]}
        {_foto(ctx, k, "vierkant", "(min-width: 961px) 38vw, 100vw")}
        <div class="b-{NAAM}__tekst">
          {_tekst_met_citaat(ctx, k)}{d["lijstkop"]}{_vinkjes(ctx, k)}{d["acties"]}
        </div>
      </div>'''


def _rustig(ctx, k, d):
    """08 woningontruiming: het stilste paneel. Smalle kolom, ruimte ernaast en een lage beeldstrook eronder.
    De kopij vraagt om rust (geen grapjes, geen haast), en dit is het laatste paneel voor de reviews."""
    return f'''<div class="wrap b-{NAAM}__rust">
        <div class="b-{NAAM}__smal">
          {d["kop"]}
          <div class="b-{NAAM}__tekst">{d["alineas"]}{d["lijstkop"]}{_vinkjes(ctx, k)}{d["acties"]}</div>
        </div>
        {_foto(ctx, k, "strook", "(min-width: 1281px) 1200px, 100vw")}
      </div>'''


COMPOSITIE = {
    "venster": _venster, "kaart": _kaart, "band": _band, "grens": _grens,
    "staand": _staand, "situaties": _situatiepaneel, "citaat": _citaat, "rustig": _rustig,
}


def _paneel(ctx, k, nr):
    variant, grond = VARIANTEN.get(k.id, ("kaart", "wit"))
    pagina = _b4.dienst_href(ctx, k.id)
    eigen_pagina = not pagina.startswith("/diensten/#")
    kop_html = ctx.inline(k.kop)
    if eigen_pagina and not k.veld("pagina-linktekst"):
        kop_html = f'<a href="{ctx.esc(pagina)}">{kop_html}</a>'
    delen = {
        "kop": _kop(ctx, k, nr, kop_html),
        "kopmet": lambda klasse="", extra="": _kop(ctx, k, nr, kop_html, klasse, extra),
        "alineas": ctx.alineas(k.tekst),
        "lijstkop": _lijstkop(ctx, k),
        "slot": _slot(ctx, k),
        "doelgroepen": _doelgroepen(ctx, k),
        "pagina": pagina,
        "eigen_pagina": eigen_pagina,
        "acties": _acties(ctx, k, pagina, eigen_pagina),
    }
    inhoud = COMPOSITIE[variant](ctx, k, delen)
    return f'''<section class="b-{NAAM}__paneel b-{NAAM}__paneel--{variant} sectie sectie--{grond}"
      id="{k.id}" aria-labelledby="{k.id}-kop">{inhoud}</section>'''


def html(ctx, kopij, **opties) -> str:
    ids = opties.get("kopij_ids") or DIENSTEN
    blokken = [ctx.kopij.blok(i) for i in ids]
    panelen = "".join(_paneel(ctx, k, i + 1) for i, k in enumerate(blokken))
    return f'''<div class="b-{NAAM}" id="{opties.get("id", "diensten")}" data-b="{NAAM}">
      <div class="b-{NAAM}__panelen">{panelen}</div>
    </div>'''
