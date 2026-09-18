"""Hulpfuncties voor pagina's en blokken (API: website/BOUWPLAN.md, hoofdstuk 3).

Een pagina declareert zich met Pagina(...); een blok krijgt een Ctx mee met alle hulpjes.
"""
import html as _html
import re
from html.parser import HTMLParser
from dataclasses import dataclass, field
from pathlib import Path

import config as cfg
import kopij as _kopij
from kopij import BouwFout

WORTEL = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Pagina
# ---------------------------------------------------------------------------
@dataclass
class Pagina:
    pad: str                                  # "/diensten/" of "/404.html"
    kopij: str = None                         # naam van website/content/<kopij>.md
    blokken: list = field(default_factory=list)
    header: str = "transparant"               # "transparant" of "vast"
    noindex: bool = False
    in_sitemap: bool = True
    body_klasse: str = ""
    preload_beeld: dict = None                # {"href":..., "imagesrcset":..., "imagesizes":..., "media":...}
    titel: str = None                         # overschrijft de voorkant van de kopij
    beschrijving: str = None
    og_beeld: str = "/img/og.jpg"
    letterlijk: bool = False                  # juridische tekst letterlijk: geen controle op verboden woorden
    concept: bool = False                     # pas live als config.PUBLICEER[pad] True is (BOUWPLAN 12)
    wacht_op: str = ""                        # waar de conceptpagina op wacht, voor het overzicht op /_concept/
    feiten: tuple = ()                        # namen uit config.FEITEN die deze pagina gebruikt

    @property
    def live(self):
        """Hoort deze pagina in de deploy? Gewone pagina's altijd, concepten alleen als ze aan staan."""
        return (not self.concept) or bool(getattr(cfg, "PUBLICEER", {}).get(self.pad, False))

    @property
    def bestand(self):
        """Het uitvoerbestand, relatief aan de root."""
        if self.pad.endswith(".html"):
            return self.pad.lstrip("/")
        return (self.pad.strip("/") + "/index.html").lstrip("/") if self.pad != "/" else "index.html"

    @property
    def url(self):
        return cfg.DOMEIN + (self.pad if self.pad != "/404.html" else "/404.html")


# ---------------------------------------------------------------------------
# Iconen: lijniconen (Lucide, ISC-licentie, 24x24, streep 2) als sprite
# ---------------------------------------------------------------------------
LIJN = {
    "pijl": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "chevron-rechts": '<path d="m9 18 6-6-6-6"/>',
    "telefoon": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "sluit": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "klok": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "schild": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "kalender": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "route": '<polygon points="3 11 22 2 13 21 11 13 3 11"/>',
    "extern": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "persoon": '<circle cx="12" cy="8" r="4"/><path d="M20 21a8 8 0 0 0-16 0"/>',
    "doos": '<path d="M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z"/><path d="M12 22V12"/><path d="m3.3 7 7.7 4.73a2 2 0 0 0 2 0L20.7 7"/><path d="m7.5 4.27 9 5.15"/>',
    "euro": '<path d="M4 10h12"/><path d="M4 14h9"/><path d="M19 6a7.7 7.7 0 0 0-5.2-2A7.9 7.9 0 0 0 6 12c0 4.4 3.5 8 7.8 8 2 0 3.8-.8 5.2-2"/>',
    "document": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 13h4"/><path d="M10 17h6"/>',
    "vrachtwagen": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    "wereld": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "quote": '<path d="M16 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z"/><path d="M5 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z"/>',
}
# WhatsApp: gespreksballon met de bestaande telefoonlijn, als lokale SVG.
LIJN["whatsapp"] = ('<path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.45L3 21l1.8-5.55A8.5 8.5 0 1 1 21 11.5Z"/>'
                    + '<g transform="translate(6 5) scale(.5)">' + LIJN["telefoon"] + '</g>')

# Gevulde symbolen (geen streep)
VOL = {
    "ster": '<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>',
    "google": '<path fill="#4285F4" d="M22.6 12.2c0-.8-.1-1.5-.2-2.2H12v4.2h5.9a5 5 0 0 1-2.2 3.3v2.7h3.6c2.1-1.9 3.3-4.7 3.3-8z"/><path fill="#34A853" d="M12 23c3 0 5.5-1 7.3-2.7l-3.6-2.7c-1 .7-2.2 1-3.7 1-2.9 0-5.3-1.9-6.2-4.5H2.1v2.8A11 11 0 0 0 12 23z"/><path fill="#FBBC05" d="M5.8 14.1a6.6 6.6 0 0 1 0-4.2V7.1H2.1a11 11 0 0 0 0 9.8z"/><path fill="#EA4335" d="M12 5.4c1.6 0 3.1.6 4.2 1.6l3.2-3.2A11 11 0 0 0 2.1 7.1l3.7 2.8C6.7 7.3 9.1 5.4 12 5.4z"/>',
    # Het huis uit het logo, met deur (voor labels en de FAQ)
    "huisje": '<path d="M12 .35l2.39 2.03V0h1.61v3.76L24 10.58h-3.48V22.9h-5.89v-5.63H9.37v5.63H3.48V10.58H0z"/>',
}

# Dienstsleutel (anker) naar het bestand van het merkicoon
DIENST_ICOON = {
    "particulier": "particulier", "zakelijk": "zakelijk", "nationaal": "nationaal",
    "internationaal": "internationaal", "verhuislift": "verhuislift", "opslag": "opslag",
    "montage": "handyman", "woningontruiming": "woningontruiming",
}


def sprite(namen):
    """De <svg>-sprite met alleen de iconen die op de pagina gebruikt zijn."""
    delen = []
    for n in sorted(namen):
        if n in LIJN:
            delen.append(f'<symbol id="i-{n}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{LIJN[n]}</symbol>')
        elif n in VOL:
            vb = "0 0 24 23" if n == "huisje" else "0 0 24 24"
            inhoud = f'<g transform="translate(2.64 2.64) scale(.78)">{VOL[n]}</g>' if n == "google" else VOL[n]
            delen.append(f'<symbol id="i-{n}" viewBox="{vb}" fill="currentColor">{inhoud}</symbol>')
    if not delen:
        return ""
    return '<svg class="sprite" width="0" height="0" aria-hidden="true" focusable="false">' + "".join(delen) + "</svg>"


# ---------------------------------------------------------------------------
# Live of verborgen (conceptpagina's) en feiten
# ---------------------------------------------------------------------------
# De build zet deze twee sets voor het renderen: alle paden van pagina's, en de paden die in deze
# build zichtbaar zijn (live build: gewone pagina's plus aangezette concepten; --concept: alles).
ALLE_PADEN = set()
ZICHTBAAR = set()


ASSETS = ("/css/", "/js/", "/img/", "/fonts/", "/docs/", "/favicon")


def is_live(href):
    """True als een link naar href in deze build mag staan. Externe links, mailto, tel, ankers op de eigen
    pagina en bestanden: True. Een pagina: alleen als ze in deze build zit (een concept dat uit staat, of
    een pagina die nog niet bestaat, geeft False)."""
    pad = (href or "").split("#")[0].split("?")[0]
    if not pad or not pad.startswith("/") or pad.startswith("//") or pad.startswith(ASSETS):
        return True
    return pad in ZICHTBAAR


def _lijst_tekst(waarden):
    waarden = [str(w) for w in waarden if w not in (None, "")]
    if len(waarden) < 2:
        return "".join(waarden)
    return ", ".join(waarden[:-1]) + " en " + waarden[-1]


def feit(naam, sjabloon=None):
    """De waarde uit config.FEITEN, of None. Met sjabloon: de ingevulde zin, of "" als het feit onbekend is.
    Lijsten worden "a, b en c". Voorbeeld: feit("OPGERICHT", "Opgericht in {}.")"""
    alle = getattr(cfg, "FEITEN", {})
    if naam not in alle:
        raise BouwFout(f"onbekend feit '{naam}' (niet in config.FEITEN)")
    waarde = alle[naam]
    if isinstance(waarde, (list, tuple)):
        waarde = _lijst_tekst(waarde) or None
    if waarde in (None, ""):
        return "" if sjabloon is not None else None
    return sjabloon.format(waarde) if sjabloon is not None else waarde


# ---------------------------------------------------------------------------
# Tekstopmaak
# ---------------------------------------------------------------------------
def esc(tekst):
    return _html.escape(str(tekst or ""), quote=True)


_VET = re.compile(r"\*\*(.+?)\*\*")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_MARK = re.compile(r"==(.+?)==")


def inline(tekst):
    """Escape en daarna alleen **vet**, [link](/pad/) en ==markering==."""
    t = esc(tekst)
    t = _VET.sub(r"<strong>\1</strong>", t)
    t = _LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)
    t = _MARK.sub(r"<mark>\1</mark>", t)
    return t


def zonder_opmaak(tekst):
    """Platte tekst (voor alt, aria-label, meta): opmaaktekens weg."""
    t = _LINK.sub(r"\1", str(tekst or ""))
    t = _VET.sub(r"\1", t)
    return _MARK.sub(r"\1", t)


class _ContactTekst(HTMLParser):
    """Koppel alleen zichtbare bedrijfsnummers, nooit invoervelden of attributen."""
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.delen = []
        self.beschermd = []

    def handle_starttag(self, tag, attrs):
        self.delen.append(self.get_starttag_text())
        if tag in {"a", "script", "style", "textarea", "select", "svg"}:
            self.beschermd.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.delen.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        self.delen.append(f"</{tag}>")
        if self.beschermd and self.beschermd[-1] == tag:
            self.beschermd.pop()

    def handle_data(self, data):
        if not self.beschermd:
            data = data.replace(cfg.TEL, f'<a href="{cfg.TELHREF}">{cfg.TEL}</a>')
        self.delen.append(data)

    def handle_entityref(self, name):
        self.delen.append(f"&{name};")

    def handle_charref(self, name):
        self.delen.append(f"&#{name};")

    def handle_comment(self, data):
        self.delen.append(f"<!--{data}-->")


# ---------------------------------------------------------------------------
# Ctx: wat een blok meekrijgt
# ---------------------------------------------------------------------------
# Weergavebreedte van het teambeeld in de hero: voor srcset in het blok en de preload van de home.
# Houd gelijk met css/blok/hero.css (.hero__team).
HERO_SIZES = "(min-width: 768px) and (min-height: 850px) 440px, (min-width: 768px) 400px, min(88vw, 390px)"


def headerbeeld(pad):
    """Elke route heeft een eigen achtergrond in de gedeelde headerbeeldenlijst."""
    import json
    bron = WORTEL / "img" / "headers" / "manifest.json"
    if not bron.exists():
        raise BouwFout("De headerbeeldenlijst img/headers/manifest.json ontbreekt")
    beelden = json.loads(bron.read_text(encoding="utf-8"))
    if pad not in beelden:
        raise BouwFout(f"Geen eigen headerachtergrond voor {pad}")
    return beelden[pad]


def responsief(basis):
    """Gegevens van een responsief beeld dat _werk/teambeeld.py maakte: <basis>-<breedte>.webp, een
    png-terugval en <basis>.json. Geeft een dict met srcset, webp, src (png), breedte en hoogte."""
    import json
    meta = WORTEL / (basis.lstrip("/") + ".json")
    if not meta.exists():
        raise BouwFout(f"responsief beeld {basis}: {meta.name} ontbreekt (draai _werk/teambeeld.py)")
    m = json.loads(meta.read_text(encoding="utf-8"))
    w, h = m["verhouding"]
    return {
        "srcset": ", ".join(f"{basis}-{b}.webp {b}w" for b in m["breedtes"]),
        "webp": f"{basis}-{m['png']}.webp",
        "src": f"{basis}-{m['png']}.png",
        "breedte": m["png"], "hoogte": round(h * m["png"] / w),
    }


class Ctx:
    def __init__(self, pagina):
        self.cfg = cfg
        self.pagina = pagina
        self.kopij = _kopij.document(pagina.kopij) if pagina.kopij else _kopij.Document("", WORTEL / "leeg.md")
        self.iconen = set()
        self.extra_css = []          # bloknamen waarvan de CSS mee moet (afhankelijkheden)
        self.extra_js = []
        self.waarschuwingen = []
        self._uniek = 0
        self.register = {}           # gezet door build.py: naam -> blokmodule
        self.gebruikt = []           # bloknamen waarvan CSS en JS mee moeten (ook geneste blokken)

    # ---- gegevens ------------------------------------------------------
    tel = property(lambda s: cfg.TEL)
    telhref = property(lambda s: cfg.TELHREF)
    mail = property(lambda s: cfg.MAIL)
    esc = staticmethod(esc)
    inline = staticmethod(inline)
    zonder_opmaak = staticmethod(zonder_opmaak)

    def blok(self, naam, **opties):
        """Render een ander blok binnen dit blok (bijvoorbeeld het formulier in een contactkaart).
        De CSS en JS van dat blok gaan automatisch mee."""
        if naam not in self.register:
            raise BouwFout(f"{self.pagina.pad}: onbekend blok '{naam}'")
        mod = self.register[naam]
        if "kopij_ids" in opties or ("kopij" in opties and opties["kopij"] is None):
            k = None
        else:
            kid = opties.get("kopij_id") or naam
            if kid in self.kopij.verborgen:
                return ""
            k = self.kopij.blok(kid) if self.kopij.heeft(kid) else _kopij.Leeg(self.pagina.kopij or "", kid)
        for dep in [naam] + list(getattr(mod, "AFHANKELIJK", [])):
            if dep not in self.gebruikt:
                self.gebruikt.append(dep)
        schone = {a: b for a, b in opties.items() if a != "kopij"}
        return mod.html(self, k, **schone)

    def bereikbaar(self, klasse="bereikbaar"):
        import navigatie
        return navigatie.bereikbaar_html(self, klasse)

    def live(self, href):
        """Mag een link naar href in deze build staan? False voor een conceptpagina die nog uit staat.
        Gebruik: {ctx.knop(...) if ctx.live("/diensten/tijdelijke-opslag/") else ""}"""
        return is_live(href)

    def href(self, voorkeur, anders):
        """voorkeur als die pagina live is, anders de terugval (bijvoorbeeld een anker op /diensten/)."""
        return voorkeur if is_live(voorkeur) else anders

    def feit(self, naam, sjabloon=None):
        return feit(naam, sjabloon)

    def kopij_van(self, naam):
        return _kopij.document(naam)

    def waarschuw(self, bericht):
        self.waarschuwingen.append(bericht)

    def uniek(self, voorvoegsel="u"):
        self._uniek += 1
        return f"{voorvoegsel}{self._uniek}"

    @property
    def score(self):
        return f"{cfg.GOOGLE_SCORE} uit 5 op Google"

    # ---- opmaakhulpjes -------------------------------------------------
    def alineas(self, lijst, klasse=None):
        k = f' class="{klasse}"' if klasse else ""
        return "".join(f"<p{k}>{inline(a)}</p>" for a in lijst or [])

    def lijst(self, items, klasse="vinklijst", icoon="check"):
        if not items:
            return ""
        li = "".join(f"<li>{self.icoon(icoon)}<span>{inline(t)}</span></li>" for t in items)
        return f'<ul class="{klasse}">{li}</ul>'

    def kopgroep(self, blok, klasse="", h="h2", extra="", label=True):
        """Label met huisje, kop en intro van een blok. De kop krijgt id '<blok-id>-kop' voor aria-labelledby."""
        kid = f"{blok.id}-kop" if blok.id else self.uniek("kop-")
        lab = self.label(blok.veld("label")) if label else ""
        intro = blok.veld("intro")
        it = f'<p class="intro">{inline(intro)}</p>' if intro else ""
        k = f"kopgroep {klasse}".strip()
        return f'<div class="{k}">{lab}<{h} id="{kid}">{inline(blok.kop)}</{h}>{it}{extra}</div>'

    def belregel(self, tekst, klasse="belregel"):
        """Zin met het telefoonnummer: het nummer wordt een tel-link met icoon."""
        if not tekst:
            return ""
        t = inline(tekst)
        if cfg.TEL in t:
            t = t.replace(cfg.TEL, f'<a href="{cfg.TELHREF}">{cfg.TEL}</a>', 1)
        return f'<p class="{klasse}">{self.icoon("telefoon")}<span>{t}</span></p>'

    def label(self, tekst, klasse=""):
        if not tekst:
            return ""
        k = f"label {klasse}".strip()
        return f'<p class="{k}">{inline(tekst)}</p>'

    def knop(self, tekst, href, soort="cta", icoon="pijl", klasse="", attrs=""):
        ic = self.icoon(icoon) if icoon else ""
        k = f"knop knop--{soort} {klasse}".strip()
        extra = f" {attrs}" if attrs else ""
        return f'<a class="{k}" href="{esc(href)}"{extra}><span>{inline(tekst)}</span>{ic}</a>'

    def belknop(self, soort="blauw", tekst=None, klasse=""):
        t = tekst or f"Bel {cfg.TEL}"
        return self.knop(t, cfg.TELHREF, soort=soort, icoon="telefoon", klasse=f"knop--icoon-voor {klasse}".strip())

    def whatsapp(self, klasse="wa-link", tekst="WhatsApp"):
        return (f'<a class="{esc(klasse)}" href="{cfg.WHATSAPP}" data-whatsapp-business '
                f'aria-label="Contact met {esc(cfg.NAAM)} via WhatsApp" title="Contact via WhatsApp">'
                f'{self.icoon("whatsapp")}<span class="wa-link__tekst">{esc(tekst)}</span></a>')

    def contactlinks(self, fragment):
        """Eén gedeelde regel voor alle blokken: naast bellen ook WhatsApp."""
        parser = _ContactTekst()
        parser.feed(fragment)
        parser.close()
        fragment = "".join(parser.delen)
        patroon = re.compile(r'<a\b(?=[^>]*\bhref=[\"\']' + re.escape(cfg.TELHREF)
                             + r'[\"\'])[^>]*>(?:(?!</a>).)*</a>(?!\s*<a\b[^>]*data-whatsapp-business)', re.S)
        return patroon.sub(lambda m: m.group(0) + self.whatsapp(), fragment)

    def icoon(self, naam, klasse="ic", label=None):
        if naam not in LIJN and naam not in VOL:
            raise BouwFout(f"onbekend icoon '{naam}'")
        self.iconen.add(naam)
        if label:
            return f'<svg class="{klasse}" role="img" aria-label="{esc(label)}"><use href="#i-{naam}"/></svg>'
        return f'<svg class="{klasse}" aria-hidden="true" focusable="false"><use href="#i-{naam}"/></svg>'

    def sterren(self, aantal=5, klasse="sterren"):
        s = "".join(self.icoon("ster") for _ in range(aantal))
        return f'<span class="{klasse}" aria-hidden="true">{s}</span>'

    def dienst_icoon(self, sleutel, inline=False, klasse="dicoon"):
        """Gevuld tweekleurig merkicoon. inline=True maakt kleuren via CSS aanpasbaar (op blauw)."""
        bestand = DIENST_ICOON.get(sleutel, sleutel)
        pad = f"/img/iconen/icoon-{bestand}.svg"
        if not inline:
            return f'<img class="{klasse}" src="{pad}" alt="" width="48" height="48" loading="lazy" decoding="async">'
        bron = WORTEL / "brandbook" / "assets" / "imagery" / f"icoon-{bestand}.svg"
        svg = bron.read_text(encoding="utf-8")
        svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
        svg = re.sub(r"<title[^>]*>.*?</title>", "", svg, flags=re.S)
        svg = re.sub(r'\s(role|aria-labelledby)="[^"]*"', "", svg)
        achter = self.uniek("-")
        svg = re.sub(r'id="([^"]+)"', lambda m: f'id="{m.group(1)}{achter}"', svg)
        svg = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{m.group(1)}{achter})", svg)
        svg = svg.replace("<svg ", f'<svg class="{klasse}" aria-hidden="true" focusable="false" ', 1)
        return " ".join(r.strip() for r in svg.splitlines() if r.strip())

    def beeld(self, src, alt, breedte, hoogte, lui=True, klasse="", sizes=None, srcset=None, prioriteit=False):
        a = [f'src="{esc(src)}"', f'alt="{esc(alt)}"', f'width="{breedte}"', f'height="{hoogte}"']
        if klasse:
            a.insert(0, f'class="{klasse}"')
        if srcset:
            a.append(f'srcset="{esc(srcset)}"')
        if sizes:
            a.append(f'sizes="{esc(sizes)}"')
        if prioriteit:
            a.append('fetchpriority="high"')
        elif lui:
            a.append('loading="lazy"')
        a.append('decoding="async"')
        return f"<img {' '.join(a)}>"

    def responsief(self, basis):
        return responsief(basis)

    def logo(self, variant="logo"):
        """Pad naar een logobestand in img/logo/. variant: 'logo', 'logo-negatief', 'logo-zonder-tagline',
        'logo-zonder-tagline-negatief', 'logo-horizontaal', 'logo-horizontaal-negatief', 'beeldmerk', ..."""
        return f"/img/logo/dereus-{variant}.svg"

    def dienst_opties(self):
        """De opties voor 'Soort verhuizing' uit offerte.md #formulier, item dienst: '- waarde = tekst'."""
        doc = _kopij.document("offerte")
        if doc.heeft("formulier"):
            blok = doc.blok("formulier")
            for it in blok.items:
                if it.id == "dienst" and it.lijst:
                    uit = []
                    for regel in it.lijst:
                        waarde, _, tekst = regel.partition(" = ")
                        uit.append((waarde.strip(), (tekst or waarde).strip()))
                    return it, uit
        return None, []

    def formulierveld(self, naam):
        """Item uit offerte.md #formulier (label = kop, placeholder, hulp), of None."""
        doc = _kopij.document("offerte")
        if doc.heeft("formulier"):
            for it in doc.blok("formulier").items:
                if it.id == naam:
                    return it
        return None
