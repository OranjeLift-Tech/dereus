"""Menu, topbalk, header, drawer, footer en mobiele belbalk. Eén bron voor alle pagina's.

Hoofdmenu (besluit gebruiker): Over ons, Diensten, Werkwijze, Contact, plus de CTA-knop. Kosten staat niet
in het menu maar wel in de footer. Volgorde en labels komen uit website/content/gedeeld.md (#menu, de lijst
van #footer); de standaard hieronder geldt als die ontbreken. Conceptpagina's (BOUWPLAN 12) verschijnen
vanzelf in megamenu, lade en footer zodra ze in config.PUBLICEER aan staan.
"""
import datetime
import re

import config as cfg
import kit
import kopij
from kit import esc, inline

# sleutel (anker op /diensten/), naam, kort label. De eigen pagina van een dienst (conceptpagina) staat in
# DIENST_PAGINA; zodra die live is, linken megamenu, lade en footer ernaar in plaats van naar het anker.
DIENSTEN = [
    ("particulier", "Particuliere verhuizingen", "Particulier"),
    ("zakelijk", "Zakelijke verhuizingen", "Zakelijk"),
    ("nationaal", "Door heel Nederland", "Door heel Nederland"),
    ("internationaal", "Internationale verhuizingen", "Internationaal"),
    ("verhuislift", "Verhuislift", "Verhuislift"),
    ("opslag", "Tijdelijke opslag", "Tijdelijke opslag"),
    ("montage", "Handymanservice", "Handymanservice"),
    ("woningontruiming", "Woningontruiming", "Woningontruiming"),
]
DIENST_PAGINA = {
    "particulier": "/diensten/particuliere-verhuizingen/",
    "zakelijk": "/diensten/zakelijke-verhuizingen/",
    "internationaal": "/diensten/internationale-verhuizingen/",
    "opslag": "/diensten/tijdelijke-opslag/",
}

# Standaardmenu: label, href. Diensten krijgt het megamenu.
MENU = [
    ("Over ons", "/over-ons/"),
    ("Diensten", "/diensten/"),
    ("Werkwijze", "/werkwijze/"),
    ("Contact", "/contact/"),
]
# Standaard voor de footerkolom De Reus
DE_REUS = [
    ("Over ons", "/over-ons/"),
    ("Werkwijze", "/werkwijze/"),
    ("Kosten", "/kosten/"),
    ("Reviews", "/#reviews"),
    ("Veelgestelde vragen", "/#vragen"),
]
# Pagina's die in de footer verschijnen zodra ze live zijn (conceptpagina's), label en href
FOOTER_EXTRA = [
    ("Werkgebied", "/werkgebied/"),
]

_LINK = re.compile(r"^\[([^\]]+)\]\(([^)\s]+)\)$")
_CIJFER = re.compile(r"(\d+(?:[.,]\d+)?)")


def _cijfer(score):
    """Alleen het cijfer uit een scorezin: "4,9 uit 5 op Google" geeft 4,9."""
    m = _CIJFER.search(score or "")
    return m.group(1) if m else cfg.GOOGLE_SCORE


def _links(blok, standaard):
    """Lijstregels "[label](/pad/)" uit gedeeld.md, anders de standaard."""
    uit = []
    for regel in blok.lijst:
        m = _LINK.match(regel.strip())
        if m:
            uit.append((m.group(1), m.group(2)))
    return uit or standaard


def dienst_href(sleutel):
    """De eigen pagina van een dienst als die live is, anders het anker op /diensten/."""
    pagina = DIENST_PAGINA.get(sleutel)
    return pagina if pagina and kit.is_live(pagina) else f"/diensten/#{sleutel}"


def menu():
    return _links(_gedeeld("menu"), MENU)


def _gedeeld(id_):
    doc = kopij.document("gedeeld")
    return doc.blok_of_leeg(id_)


def _huidig(pad, href):
    if href == pad:
        return ' aria-current="page"'
    if href != "/" and not href.startswith("/#") and pad.startswith(href.split("#")[0]) and href.split("#")[0] != "/":
        return ' aria-current="true"'
    return ""


def tijden_regels():
    return [f'{t["kort"]} {t["van"]} tot {t["tot"]} uur' for t in cfg.TIJDEN]


def bereikbaar_html(ctx, klasse="bereikbaar", tijden_id=None):
    """Live status 'Nu bereikbaar'. js/site.js vult hem in; zonder JS blijft hij verborgen.

    Met tijden_id erbij klapt de chip de openingstijden uit. Dat is bewust een echte knop en niet
    alleen hover: hover bestaat niet op een telefoon, en een span vangt geen toetsenbord. Tikken en
    Enter doen dus hetzelfde als de muis met hover krijgt, en de hover zelf zit er gewoon bij. Zo
    komt iedereen bij de tijden en houdt de muisgebruiker de beweging die gevraagd was.

    De regels komen uit tijden_regels() en dus uit config.TIJDEN, zodat ze niet uit de pas kunnen
    lopen met de lijsten in de voet, de contactband, de kaart en het homecontactblok.

    tijden_id moet je zelf meegeven en per pagina uniek houden, want aria-controls wijst ernaar.
    Een teller hier zou per bouwronde andere ids geven en dat maakt de diffs onleesbaar.

    Let op bij het inbouwen: in de hero staat de chip binnen een <p>, dus het paneel mag alleen
    phrasing content bevatten. Daarom spans en geen <ul> of <div>.
    """
    b = _gedeeld("bereikbaar")
    data = (f' data-open="{esc(b.veld("open", "Nu bereikbaar"))}"'
            f' data-dicht="{esc(b.veld("dicht", "Nu gesloten"))}"'
            f' data-morgen="{esc(b.veld("morgen", "Morgen weer bereikbaar vanaf {tijd} uur"))}"')
    binnen = '<span class="bereikbaar__stip" aria-hidden="true"></span><span class="bereikbaar__tekst"></span>'
    if not tijden_id:
        return f'<span class="{klasse}" data-bereikbaar{data} hidden>{binnen}</span>'
    regels = " ".join(f'<span class="bereikbaar__regel">{esc(r)}</span>' for r in tijden_regels())
    return (f'<span class="{klasse} bereikbaar--tijden" data-bereikbaar{data} hidden>'
            f'<button class="bereikbaar__knop" type="button" aria-expanded="false" aria-controls="{esc(tijden_id)}">'
            f'{binnen}<span class="vh">, bekijk onze openingstijden</span>'
            f'{ctx.icoon("chevron")}</button>'
            f'<span class="bereikbaar__tijden" id="{esc(tijden_id)}" hidden>'
            f'<span class="bereikbaar__tijden-kop">{esc(b.veld("tijden-kop", "Openingstijden"))}</span> '
            f'{regels}</span></span>')


def header_acties(ctx):
    """Reviewblok, telefoon en CTA rechts in de header.

    Het reviewblok is compact: de Google-G, één ster en het cijfer. De ster is hier een merkteken dat zegt
    dat het over reviews gaat, geen meter; het cijfer ernaast draagt de score. Daarom staat hier
    ctx.icoon("ster") en niet ctx.sterren(1), want dat laatste zou een schaal van één ster betekenen.
    De volledige score staat in aria-label van de link, zodat schermlezers hem onverkort voorlezen.
    """
    t = _gedeeld("topbalk")
    score = t.veld("score", ctx.score)
    return f'''<div class="header__acties">
      <a class="header__reviews" href="{esc(t.veld("score-link", "/#reviews"))}" aria-label="{esc(score)}">{ctx.icoon("google")}<span class="header__reviews__ster" aria-hidden="true">{ctx.icoon("ster")}</span><b aria-hidden="true">{esc(_cijfer(score))}</b></a>
      <a class="header__tel" href="{cfg.TELHREF}">{ctx.icoon("telefoon")}<span>{esc(t.veld("telefoon", cfg.TEL))}</span></a>
      <a class="knop knop--cta header__cta" href="/offerte/"><span>{esc(_gedeeld("menu").veld("knop", "Offerte aanvragen"))}</span>{ctx.icoon("pijl")}</a>
    </div>'''


def _mega(ctx):
    groepen = []
    labels = _gedeeld("menu")
    for label, diensten in [(labels.veld("groep-verhuizen", "Verhuizen"), DIENSTEN[:4]),
                             (labels.veld("groep-extra", "Extra hulp"), DIENSTEN[4:])]:
        items = "".join(f'<li><a href="{dienst_href(sl)}">{esc(naam)}</a></li>' for sl, naam, _ in diensten)
        groepen.append(f'<div class="mega__kolom"><p class="mega__label">{esc(label)}</p><ul class="mega__lijst">{items}</ul></div>')
    return f'''<div class="mega" id="menu-diensten">
        <div class="mega__grid">{"".join(groepen)}</div>
        <a class="mega__alle" href="/diensten/">Alle diensten{ctx.icoon("pijl")}</a>
      </div>'''


def header(ctx):
    pad = ctx.pagina.pad
    items = []
    for label, href in menu():
        if not ctx.live(href):
            continue
        cur = _huidig(pad, href)
        if href == "/diensten/":
            # Label en chevron zitten in dezelfde link: klikken gaat naar /diensten/,
            # het paneel komt bij hover en bij focus. De ARIA verhuist mee naar de link.
            items.append(f'''<li class="nav__item nav__item--sub">
        <a class="nav__link nav__link--sub" href="{href}"{cur} aria-expanded="false" aria-controls="menu-diensten">{esc(label)}<span class="vh"> met submenu</span>{ctx.icoon("chevron")}</a>
        {_mega(ctx)}
      </li>''')
        else:
            items.append(f'<li class="nav__item"><a class="nav__link" href="{href}"{cur}>{esc(label)}</a></li>')
    hl = cfg.HEADER_LOGO
    naam = "logo-horizontaal" if hl == "horizontaal" else "logo"
    neg = ctx.logo(f"{naam}-negatief")
    kleur = ctx.logo(naam)
    b_, h_ = cfg.LOGO_MATEN[hl]
    maat = f'width="{b_}" height="{h_}"'
    soort = "transparant" if ctx.pagina.header == "transparant" else "vast"
    return f'''<header class="header header--{soort}" data-header>
  <div class="header__balk"><div class="wrap">
    <a class="header__logo header__logo--{hl}" href="/" aria-label="{esc(cfg.NAAM)}, naar de homepage">
      <img class="header__logo-neg" src="{neg}" alt="" {maat} decoding="async">
      <img class="header__logo-kleur" src="{kleur}" alt="" {maat} decoding="async">
    </a>
    <nav class="nav" aria-label="Hoofdmenu"><ul class="nav__lijst">
      {"".join(items)}
    </ul></nav>
    {header_acties(ctx)}
    <button class="header__menu" type="button" aria-expanded="false" aria-controls="lade">{ctx.icoon("menu")}<span class="vh">Menu openen</span></button>
  </div></div>
</header>'''


def lade(ctx):
    """Het uitschuifmenu voor mobiel en tablet. Focus-trap en Escape in js/site.js."""
    pad = ctx.pagina.pad
    diensten = "".join(f'<li><a href="{dienst_href(sl)}">{esc(kort)}</a></li>' for sl, _, kort in DIENSTEN)
    regels = []
    for label, href in menu():
        if not ctx.live(href):
            continue
        cur = _huidig(pad, href)
        if href == "/diensten/":
            regels.append(f'''<details class="lade__groep"><summary>{esc(label)}{ctx.icoon("chevron")}</summary>
        <ul><li><a href="/diensten/"{cur}>Alle diensten</a></li>{diensten}</ul></details>''')
        else:
            regels.append(f'<a class="lade__link" href="{href}"{cur}>{esc(label)}</a>')
    return f'''<div class="lade" id="lade" hidden>
  <div class="lade__scrim" data-lade-sluit></div>
  <div class="lade__paneel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="lade__kop">
      <a href="/" class="lade__logo" aria-label="{esc(cfg.NAAM)}, naar de homepage"><img src="{ctx.logo("logo-horizontaal")}" alt="" width="{cfg.LOGO_MATEN["horizontaal"][0]}" height="{cfg.LOGO_MATEN["horizontaal"][1]}"></a>
      <button class="lade__sluit" type="button" data-lade-sluit>{ctx.icoon("sluit")}<span class="vh">Menu sluiten</span></button>
    </div>
    <nav class="lade__nav" aria-label="Menu">
      {"".join(regels)}
    </nav>
    <div class="lade__voet">
      <a class="knop knop--cta" href="/offerte/"><span>{esc(_gedeeld("menu").veld("knop", "Offerte aanvragen"))}</span>{ctx.icoon("pijl")}</a>
      <a class="lade__tel" href="{cfg.TELHREF}">{ctx.icoon("telefoon")}<span>{cfg.TEL}</span></a>
      <a class="lade__mail" href="mailto:{cfg.MAIL}">{ctx.icoon("mail")}<span>{cfg.MAIL}</span></a>
      {bereikbaar_html(ctx)}
    </div>
  </div>
</div>'''


def footer(ctx):
    f = _gedeeld("footer")
    claim = f.veld("claim", "Sterk in verhuizen. Zorgeloos geregeld.")
    diensten = "".join(f'<li><a href="{dienst_href(sl)}">{esc(naam)}</a></li>' for sl, naam, _ in DIENSTEN)
    links = [(l, h) for l, h in _links(f, DE_REUS) if ctx.live(h)]
    links += [(l, h) for l, h in FOOTER_EXTRA if h in kit.ALLE_PADEN and ctx.live(h) and h not in [x for _, x in links]]
    dereus = "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for l, h in links)
    tijden = "".join(f"<li>{esc(r)}</li>" for r in tijden_regels())
    jaar = datetime.date.today().year
    return f'''<footer class="footer">
  <div class="wrap footer__intro">
    <div class="footer__uitnodiging">
      <p class="label">{esc(cfg.NAAM)}</p>
      <h2>{inline(f.veld("contact-kop", "Uw verhuizing begint met een goed gesprek."))}</h2>
      <p>{inline(f.veld("contact-tekst", "Vertel ons waar u naartoe verhuist en welke hulp u nodig heeft. Uw vaste verhuisadviseur denkt met u mee."))}</p>
      <a class="footer__tel" href="{cfg.TELHREF}">{ctx.icoon("telefoon")}<span>{cfg.TEL}</span></a>
      <div class="knoppen">
        <a class="knop knop--cta" href="/offerte/"><span>{esc(f.veld("knop", "Offerte aanvragen"))}</span>{ctx.icoon("pijl")}</a>
        <a class="knop knop--licht" href="mailto:{cfg.MAIL}">{ctx.icoon("mail")}<span>{esc(f.veld("mail-knop", "Mail ons"))}</span></a>
      </div>
    </div>
    <img class="footer__wagen" src="/img/footer-wagen.webp" alt="" width="1380" height="974" loading="lazy" decoding="async">
  </div>
  <div class="wrap footer__top">
    <div class="footer__merk">
      <a href="/" aria-label="{esc(cfg.NAAM)}, naar de homepage"><img class="footer__logo" src="{ctx.logo("logo-horizontaal-negatief")}" alt="" width="{cfg.LOGO_MATEN["horizontaal"][0]}" height="{cfg.LOGO_MATEN["horizontaal"][1]}" loading="lazy" decoding="async"></a>
      <p class="footer__claim">{inline(claim)}</p>
      <p class="footer__omschrijving">{inline(f.veld("omschrijving", "Vanuit Den Haag verhuizen wij u door heel Nederland. Met één vast aanspreekpunt, van aanvraag tot verhuisdag."))}</p>
    </div>
    <nav class="footer__kolom footer__kolom--diensten" aria-labelledby="f-diensten"><p class="footer__kop" id="f-diensten">{esc(f.veld("kolom-diensten", "Diensten"))}</p><ul>{diensten}</ul></nav>
    <nav class="footer__kolom" aria-labelledby="f-dereus"><p class="footer__kop" id="f-dereus">{esc(f.veld("kolom-dereus", "De Reus"))}</p><ul>{dereus}</ul></nav>
    <div class="footer__kolom"><p class="footer__kop">{esc(f.veld("kolom-contact", "Contact"))}</p>
      <div class="footer__blokken">
        <div class="footer__blok">
          <address><span class="footer__sub">{esc(f.veld("adres-label", "Hoofdkantoor"))}</span>{esc(cfg.STRAAT)}<br>{esc(cfg.POSTCODE)} {esc(cfg.PLAATS)}</address>
          <ul><li><a href="{cfg.TELHREF}">{cfg.TEL}</a></li><li><a href="mailto:{cfg.MAIL}">{cfg.MAIL}</a></li><li><a href="{cfg.ROUTE}" rel="noopener">Route plannen{ctx.icoon("extern")}</a></li></ul>
        </div>
        <div class="footer__blok">
          <p class="footer__sub">{esc(f.veld("bereikbaar-kop", "Bereikbaar"))}</p>
          <ul class="footer__tijden">{tijden}</ul>
          {bereikbaar_html(ctx, "bereikbaar bereikbaar--footer")}
        </div>
      </div>
    </div>
  </div>
  <div class="footer__onder"><div class="wrap">
    <p>{esc(f.veld("onderregel", f"© {jaar} {cfg.NAAM}"))}</p>
    <ul><li><a href="/algemene-voorwaarden/">Algemene voorwaarden</a></li><li><a href="/privacyverklaring/">Privacyverklaring</a></li></ul>
  </div></div>
</footer>'''


def belbalk(ctx):
    b = _gedeeld("belbalk")
    return f'''<nav class="mcta" aria-label="Snel contact">
  <a class="knop knop--licht" href="{cfg.TELHREF}">{ctx.icoon("telefoon")}<span>{esc(b.veld("bellen", "Bellen"))}</span></a>{ctx.whatsapp(glyph="whatsapp")}
  <a class="knop knop--cta" href="/offerte/"><span>{esc(b.veld("offerte", "Offerte aanvragen"))}</span></a>
</nav>
{ctx.whatsapp(klasse="whatsapp")}'''
