"""Bewakers: de build faalt als een regel uit website/BOUWPLAN.md (hoofdstuk 9) geschonden wordt."""
import html as _html
import re
from pathlib import Path

DASHES = ("\u2013", "\u2014")   # en-dash en em-dash, als escape zodat dit bestand zelf schoon blijft

# Hele woorden of vaste woordgroepen, hoofdletterongevoelig. Controle op de zichtbare tekst.
VERBODEN = [
    r"zonder verrassingen",
    r"volledig verzekerd",
    r"alles is mogelijk",
    r"garantie\w*",
    r"4,9/5", r"4\.9",
    r"kvk",
    r"gecertificeerd\w*",
    r"erkend\w*",
    r"sinds (?:19|20)\d\d",
]
VERBODEN_RE = re.compile(r"(?<![\w-])(?:" + "|".join(VERBODEN) + r")(?![\w])", re.I)


def verboden_re():
    """Zodra de klant een feit bevestigt (config.FEITEN), mag het bijbehorende woord wel."""
    try:
        import config
        feiten = getattr(config, "FEITEN", {})
    except ImportError:
        feiten = {}
    lijst = [v for v in VERBODEN
             if not (v == r"kvk" and feiten.get("KVK"))
             and not (v.startswith("sinds") and feiten.get("OPRICHTINGSJAAR"))]
    return re.compile(r"(?<![\w-])(?:" + "|".join(lijst) + r")(?![\w])", re.I)


# Resten van onbekende feiten of sjablonen mogen nooit zichtbaar worden
RESTEN_RE = re.compile(r"\[\s*(?:\.\.\.|\u2026)\s*\]|\bNone\b|\{[A-Za-z_]+\}")

BRONMAPPEN = ["_werk", "website/content", "css", "js"]
BRON_UITSLUITEN = ("css/min/", "__pycache__", "css/hero.css", "css/3d.css", "css/rit.css", "css/werkwijze.css",
                   "js/3d.js", "js/hero.js", "js/rit.js", "js/main.js", "_werk/kaart/")


def zichtbare_tekst(html):
    t = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    # alt- en aria-label-teksten tellen mee als zichtbaar voor wie ze hoort
    extra = " ".join(re.findall(r'(?:alt|aria-label|title)="([^"]*)"', t))
    t = re.sub(r"<[^>]+>", " ", t)
    return _html.unescape(t + " " + extra)


def _ids(html):
    return set(re.findall(r'\sid="([^"]+)"', html))



def verhuisdagbeelden(wortel):
    """Half ingevulde beeldvelden in een verhuisdagblok.

    verhuisdag.py gaat pas naar de kaderindeling als elk moment een veld `beeld` heeft en dat
    bestand ook bestaat. Ontbreekt er een, dan blijft de route staan en gebeurt er verder niets:
    geen fout, geen verschil, geen melding. Wie net twee van de drie regels heeft toegevoegd,
    ziet dus niets veranderen en weet niet waarom. Deze bewaker sluit dat gat.

    Het blijft een waarschuwing: alles of niets is het juiste gedrag en een halve invulling is
    geen reden om een build te stoppen, zeker niet terwijl er aan de kopij gewerkt wordt.
    """
    uit = []
    map_ = wortel / "website" / "content"
    if not map_.exists():
        return uit
    for bestand in sorted(map_.glob("*.md")):
        tekst = bestand.read_text(encoding="utf-8", errors="ignore")
        blok = re.search(r"^##\s+.*\{#verhuisdag\}\s*$(.*?)(?=^##\s|\Z)", tekst, re.S | re.M)
        if not blok:
            continue
        rel = bestand.relative_to(wortel).as_posix()
        momenten = re.findall(r"^###\s+(.+?)\s*$(.*?)(?=^###\s|\Z)", blok.group(1), re.S | re.M)
        met, zonder, kwijt = [], [], []
        for titel, romp in momenten:
            m = re.search(r"^beeld:\s*(\S+)\s*$", romp, re.M)
            if not m:
                zonder.append(titel)
            elif not (wortel / "img" / f"{m.group(1)}.webp").exists():
                kwijt.append(f"{titel} verwijst naar img/{m.group(1)}.webp")
            else:
                met.append(titel)
        if met and zonder:
            uit.append(f"{rel}: verhuisdag heeft een veld beeld bij {', '.join(met)} maar niet bij "
                       f"{', '.join(zonder)}. Het blok gaat pas naar de kaderindeling als elk moment "
                       f"er een heeft; tot die tijd blijft de route staan en verandert er niets.")
        if kwijt:
            uit.append(f"{rel}: verhuisdag wijst naar een bestand dat niet in img/ staat: "
                       f"{'; '.join(kwijt)}. Het blok blijft daardoor op de route staan.")
    return uit

def controleer(uitvoer, paginas, wortel, volledig=True, verborgen=()):
    """uitvoer: {pad: html}. verborgen: paden van conceptpagina's die in deze build uit staan.
    Geeft (fouten, waarschuwingen)."""
    fouten, waarsch = [], []
    verboden = verboden_re()
    per_pad = {p.pad: p for p in paginas}
    ids_per_pad = {pad: _ids(h) for pad, h in uitvoer.items()}
    bekende_paden = {p.pad for p in paginas}

    for pad, html in uitvoer.items():
        pagina = per_pad[pad]
        naam = f"{pad}"
        # 1. dashes
        for d in DASHES:
            if d in html:
                fouten.append(f"{naam}: bevat een {'en' if d == DASHES[0] else 'em'}-dash")
        # 2. skiplink, main, één h1
        if 'class="skiplink"' not in html:
            fouten.append(f"{naam}: geen skiplink")
        if '<main id="inhoud" tabindex="-1">' not in html:
            fouten.append(f"{naam}: geen <main id=\"inhoud\" tabindex=\"-1\">")
        n_h1 = len(re.findall(r"<h1[\s>]", html))
        if n_h1 != 1:
            fouten.append(f"{naam}: {n_h1} keer <h1> (moet 1 zijn)")
        # 3. titel en beschrijving
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        titel = _html.unescape(m.group(1)) if m else ""
        if not titel:
            fouten.append(f"{naam}: geen <title>")
        elif len(titel) > 60:
            fouten.append(f"{naam}: titel is {len(titel)} tekens (max 60)")
        m = re.search(r'<meta name="description" content="([^"]*)"', html)
        beschr = _html.unescape(m.group(1)) if m else ""
        if not beschr:
            waarsch.append(f"{naam}: geen meta description")
        elif len(beschr) > 158:
            fouten.append(f"{naam}: beschrijving is {len(beschr)} tekens (max 158)")
        # 4. interne links en ankers
        for href in re.findall(r'href="([^"]+)"', html):
            if not href.startswith("/") or href.startswith("//"):
                continue
            pad_deel, _, anker = href.partition("#")
            pad_deel = pad_deel.split("?")[0]
            if pad_deel == "/_concept/":
                continue                      # het lokale overzicht van --concept (alleen in _voorbeeld/)
            if pad_deel.startswith(("/css/", "/js/", "/fonts/", "/img/", "/docs/", "/favicon")):
                if not (wortel / pad_deel.lstrip("/")).exists():
                    fouten.append(f"{naam}: bestand bestaat niet: {href}")
                continue
            doel = pad_deel or pad
            if doel in verborgen:
                fouten.append(f"{naam}: link naar conceptpagina {href}, die staat nog uit (gebruik ctx.live of ctx.href)")
                continue
            if doel not in bekende_paden:
                if volledig:
                    fouten.append(f"{naam}: link naar onbekende pagina {href}")
                continue
            if anker and doel in ids_per_pad and anker not in ids_per_pad[doel]:
                fouten.append(f"{naam}: anker bestaat niet: {href}")
        # 5. beelden
        for img in re.findall(r"<img\b[^>]*>", html):
            for attr in ("width=", "height=", "alt="):
                if attr not in img:
                    fouten.append(f"{naam}: <img> zonder {attr[:-1]}: {img[:90]}")
            src = re.search(r'src="([^"]+)"', img)
            if src and src.group(1).startswith("/"):
                if not (wortel / src.group(1).split("?")[0].lstrip("/")).exists():
                    fouten.append(f"{naam}: beeld bestaat niet: {src.group(1)}")
        # 6. verboden woorden
        zichtbaar = zichtbare_tekst(html)
        if not pagina.letterlijk:
            for m in verboden.finditer(zichtbaar):
                fouten.append(f"{naam}: verboden woord '{m.group(0)}'")
        for m in RESTEN_RE.finditer(zichtbaar):
            fouten.append(f"{naam}: onbekend feit of sjabloonrest zichtbaar: '{m.group(0)}'")
        # 7. Google Fonts, avatars
        if "fonts.googleapis.com" in html or "fonts.gstatic.com" in html:
            fouten.append(f"{naam}: Google Fonts-link")
        if "img/avatar-" in html:
            fouten.append(f"{naam}: reviewfoto (img/avatar-) gebruikt; gebruik initialen")
        # 8. Web3Forms-key: alleen de placeholder
        for key in re.findall(r'name="access_key" value="([^"]*)"', html):
            if key and not key.startswith("VUL-HIER"):
                fouten.append(f"{naam}: een echte Web3Forms-key staat in de HTML; overleg met dereus-28")
        # waarschuwing: meer dan één CTA-knop per sectie
        for sectie in re.findall(r"<section\b.*?</section>", html, re.S):
            n = len(re.findall(r'class="[^"]*\bknop--cta\b', sectie))
            if n > 1:
                sid = re.search(r'id="([^"]+)"', sectie)
                waarsch.append(f"{naam}: {n} CTA-knoppen in sectie #{sid.group(1) if sid else '?'}")

    # 1b. dashes in de bronbestanden
    if volledig:
        for map_ in BRONMAPPEN:
            for pad in (wortel / map_).rglob("*"):
                if not pad.is_file() or pad.suffix not in (".py", ".md", ".css", ".js", ".json"):
                    continue
                rel = pad.relative_to(wortel).as_posix()
                if any(u in rel for u in BRON_UITSLUITEN):
                    continue
                tekst = pad.read_text(encoding="utf-8", errors="ignore")
                for d in DASHES:
                    if d in tekst:
                        fouten.append(f"{rel}: bevat een {'en' if d == DASHES[0] else 'em'}-dash")
        # hex-waarden in blok-CSS (waarschuwing)
        for pad in (wortel / "css" / "blok").glob("*.css") if (wortel / "css" / "blok").exists() else []:
            tekst = re.sub(r"/\*.*?\*/", "", pad.read_text(encoding="utf-8"), flags=re.S)
            hexen = set(re.findall(r"#[0-9a-fA-F]{3,8}\b", tekst))
            if hexen:
                waarsch.append(f"css/blok/{pad.name}: losse kleurwaarden {', '.join(sorted(hexen))} (gebruik tokens)")
        # verhuisdag: half ingevulde beeldvelden, want de omslag is stil
        waarsch += verhuisdagbeelden(wortel)
        # grote beelden
        for pad in (wortel / "img").rglob("*"):
            if pad.is_file() and pad.suffix in (".jpg", ".jpeg", ".png", ".webp") and pad.stat().st_size > 250_000:
                waarsch.append(f"{pad.relative_to(wortel).as_posix()}: {pad.stat().st_size // 1024} KB (groter dan 250 KB)")
    return fouten, waarsch
