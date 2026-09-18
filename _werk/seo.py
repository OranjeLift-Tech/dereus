"""sitemap.xml, robots.txt en de SEO-regels in de <head> (eigenaar: dereus-e7).

schrijf(paginas, cfg)  schrijft /sitemap.xml en /robots.txt naar de root, na het bouwen van de pagina's.
                       De build geeft alleen pagina's die live zijn (gewone pagina's en concepten die in
                       config.PUBLICEER aan staan); bij --concept wordt schrijf niet aangeroepen.
head(pagina, cfg)      geeft canonical, Open Graph, Twitter, favicon en theme-color als HTML-regels,
                       voor in de <head> die build.py maakt.

lastmod verandert alleen als de inhoud van <main> van een pagina verandert (zoals Brocken): de hash per pagina
staat in _werk/.lastmod.json. Een nieuwe build zonder inhoudelijke wijziging laat de datums dus staan.
"""
import datetime
import hashlib
import json
import re
from pathlib import Path
from xml.dom import minidom

ROOT = Path(__file__).resolve().parent.parent
STAAT = Path(__file__).resolve().parent / ".lastmod.json"

# Rangorde uit sitemap/SITEMAP.md (v1.3). Google negeert priority; andere zoekmachines gebruiken het soms.
PRIORITEIT = {
    "/": "1.0",
    "/diensten/": "0.9",
    "/kosten/": "0.9",
    "/offerte/": "0.8",
    "/werkwijze/": "0.7",
    "/werkgebied/": "0.7",
    "/over-ons/": "0.6",
    "/contact/": "0.5",
    "/algemene-voorwaarden/": "0.2",
    "/privacyverklaring/": "0.2",
}
# Conceptpagina's (BOUWPLAN 12) die later live gaan: per map, de langste map wint
PRIORITEIT_MAP = [
    ("/diensten/internationale-verhuizingen/", "0.7"),   # landenpagina's
    ("/diensten/", "0.8"),                               # dienst- en doelgroeppagina's
    ("/werkgebied/", "0.7"),                             # plaatspagina's
]

# Mappen die niet online staan (.vercelignore); in robots.txt voor het geval ze toch ergens opduiken
NIET_PUBLIEK = ["/_werk/", "/website/", "/brandbook/", "/sitemap/", "/logo-opties/", "/_bron/", "/_ai-beelden/", "/_ontwerpen/",
                "/_voorbeeld/", "/_concept/"]


def _prioriteit(pad):
    if pad in PRIORITEIT:
        return PRIORITEIT[pad]
    for map_, waarde in PRIORITEIT_MAP:
        if pad.startswith(map_) and pad != map_:
            return waarde
    return "0.5"


def _domein(cfg):
    return (getattr(cfg, "DOMEIN", "https://www.verhuisbedrijfdereus.nl") or "").rstrip("/")


def _bestand(pad):
    return ROOT / "index.html" if pad == "/" else ROOT / pad.strip("/") / "index.html"


def _inhoudshash(pad):
    """Hash van <main>, zonder de cachebreker (?v=), zodat alleen echte wijzigingen tellen."""
    f = _bestand(pad)
    if not f.exists():
        return None
    html = f.read_text(encoding="utf-8")
    m = re.search(r"<main\b.*?</main>", html, re.S)
    stuk = re.sub(r"\?v=[0-9a-zA-Z]+", "", m.group(0) if m else html)
    return hashlib.sha1(stuk.encode("utf-8")).hexdigest()[:16]


def _lastmods(paden):
    vandaag = datetime.date.today().isoformat()
    try:
        staat = json.loads(STAAT.read_text(encoding="utf-8"))
    except Exception:
        staat = {}
    uit = {}
    for pad in paden:
        h = _inhoudshash(pad)
        oud = staat.get(pad, {})
        if h and oud.get("hash") == h:
            uit[pad] = oud["datum"]
        else:
            uit[pad] = vandaag
            staat[pad] = {"hash": h, "datum": vandaag}
    STAAT.write_text(json.dumps(staat, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return uit


def _live(p):
    """Gewone pagina's en aangezette concepten (kit.Pagina.live). Een concept dat uit staat komt nooit in de sitemap,
    ook niet als de build het ooit per ongeluk zou doorgeven."""
    return bool(getattr(p, "live", True))


def _in_sitemap(p):
    return getattr(p, "in_sitemap", True) and not getattr(p, "noindex", False) and _live(p)


def schrijf(paginas, cfg):
    d = _domein(cfg)
    paden = [p.pad for p in paginas if _in_sitemap(p)]
    paden.sort(key=lambda x: (-float(_prioriteit(x)), x))
    datums = _lastmods(paden)

    regels = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for pad in paden:
        regels.append(f"  <url><loc>{d}{pad}</loc><lastmod>{datums[pad]}</lastmod>"
                      f"<priority>{_prioriteit(pad)}</priority></url>")
    regels.append("</urlset>")
    xml = "\n".join(regels) + "\n"
    minidom.parseString(xml)                        # faalt hard als de XML niet klopt
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8", newline="\n")

    robots = ["User-agent: *", "Allow: /"] + [f"Disallow: {m}" for m in NIET_PUBLIEK] + ["", f"Sitemap: {d}/sitemap.xml", ""]
    (ROOT / "robots.txt").write_text("\n".join(robots), encoding="utf-8", newline="\n")
    return {"sitemap": len(paden), "uitgesloten": [p.pad for p in paginas if not _in_sitemap(p)]}


def _esc(t):
    return (t or "").replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def _meta(pagina):
    """titel, beschrijving en og-titel: de pagina gaat voor, anders de voorkant van het kopijbestand
    (dezelfde volgorde als meta_van in build.py)."""
    meta = {}
    if getattr(pagina, "kopij", None):
        try:
            import kopij
            meta = kopij.document(pagina.kopij).meta
        except Exception:
            meta = {}
    titel = getattr(pagina, "titel", None) or meta.get("titel") or "Verhuisbedrijf De Reus"
    beschrijving = getattr(pagina, "beschrijving", None) or meta.get("beschrijving") or ""
    return titel, beschrijving, meta.get("og-titel") or titel


def head(pagina, cfg):
    """Canonical of noindex, Open Graph, Twitter, theme-color en favicons. De build zet <title> en
    de description zelf en laat deze regels dan aan dit bestand over."""
    d = _domein(cfg)
    pad = getattr(pagina, "pad", "/")
    titel, beschrijving, og_titel = _meta(pagina)
    og_beeld = getattr(pagina, "og_beeld", None) or "/img/og.jpg"
    naam = getattr(cfg, "NAAM", "Verhuisbedrijf De Reus")
    r = []
    if getattr(pagina, "noindex", False):
        r.append('<meta name="robots" content="noindex, follow">')
    elif not _live(pagina):
        # alleen in de voorvertoning (_voorbeeld/): een concept dat uit staat
        r.append('<meta name="robots" content="noindex, nofollow">')
    else:
        r.append(f'<link rel="canonical" href="{d}{pad}">')
    r += [
        '<meta property="og:type" content="website">',
        f'<meta property="og:locale" content="{getattr(cfg, "LOCALE", "nl_NL")}">',
        f'<meta property="og:site_name" content="{_esc(naam)}">',
        f'<meta property="og:url" content="{d}{pad}">',
        f'<meta property="og:title" content="{_esc(og_titel)}">',
        f'<meta property="og:description" content="{_esc(beschrijving)}">',
        f'<meta property="og:image" content="{d}{og_beeld}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="Logo van {_esc(naam)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="theme-color" content="{getattr(cfg, "THEMA_KLEUR", "#1746A2")}">',
        '<meta name="format-detection" content="telephone=no">',
        '<link rel="icon" href="/img/logo/dereus-favicon.ico" sizes="any">',
        '<link rel="icon" href="/img/logo/dereus-favicon.svg" type="image/svg+xml">',
        '<link rel="icon" href="/img/logo/dereus-favicon-32.png" type="image/png" sizes="32x32">',
        '<link rel="apple-touch-icon" href="/img/logo/dereus-favicon-180.png">',
    ]
    return "\n".join(r)
