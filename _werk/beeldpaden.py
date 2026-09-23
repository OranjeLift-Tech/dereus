"""Waar de beelden in deze repo vandaan verwezen worden, en in welke klasse ze daarmee vallen.

Dit is de gedeelde kern onder `opruimen-beelden.py` (wat mag weg) en `controle-beelden.py
--vangnet` (mist er na een verplaatsing iets). Beide moeten van precies dezelfde verzameling
"live bestanden" uitgaan, anders ruimt het een op wat het ander nog nodig heeft.

Drie klassen, en het verschil tussen de eerste twee is de hele reden dat dit bestand bestaat:

  in gebruik     verwezen vanuit de gebouwde site (html, css, js) of vanuit de bouwbron
                 (_werk/*.py, website/content/). Dit gaat nooit weg.
  bronmateriaal  alleen verwezen vanuit een generator (_ai-beelden/), een oude reviewronde
                 (website/review/), een ontwerpvariant (_ontwerpen/) of een keuzereeks
                 (beeld-opties/, logo-opties/). Dat is werkmateriaal, geen dood gewicht:
                 het gaat NIET mee in de opruiming, het wordt alleen gemeld.
  ongebruikt     nergens vandaan verwezen. Alleen dit komt in aanmerking.

DE VALKUIL, en waarom "grep de gebouwde pagina's" hier niet volstaat: de blokken zetten hun
beeldpaden met f-strings in elkaar.

    _werk/blokken/plaatskaart.py   beeld = f"/img/kaart-{slug}.svg"
    _werk/blokken/verhuisdag.py    pad   = f"/img/{naam}.webp"
    _werk/blokken/werkwijze.py     foto  = f"/img/{FOTOS[(i - 1) % len(FOTOS)]}"

De letterlijke naam `kaart-delft.svg` staat daardoor in geen enkel bronbestand, en in de
gebouwde site ook niet: van de pagina's die de build kan maken staan er op dit moment tien in
de wortel, en de plaatspagina's zitten daar niet bij. Op de letterlijke tekst afgaan zou alle
elf kaart-*.svg als ongebruikt aanmerken en de eerstvolgende volledige build breken.

Daarom worden die f-strings als patroon gelezen en andersom toegepast: niet elk patroon met
elk mogelijk woord invullen, maar per bestand kijken of het op een patroon past en of het
ingevulde stuk ook echt ergens in de bron of de kopij voorkomt. `img/kaart-delft.svg` past op
`img/kaart-[^/]+\\.svg` en `delft` staat in website/content/plaatsen/delft.md, dus: in gebruik.
Een `img/avatar-<naam>.webp` past op `img/[^/]+\\.webp`, maar komt `avatar-<naam>` nergens voor,
dan blijft dat bestand ongebruikt -- wel met de reden erbij, zodat een mens er nog naar kan kijken.

Een patroon wordt alleen herkend als het pad met een `/` begint of het letterlijke stuk met
`img/` begint. Dat scheelt de foutmeldingen: "{titel} verwijst naar img/{...}.webp" uit
bewakers.py is een zin en geen verwijzing, en zou als patroon elke webp in img/ levend houden.

Wat dit niet ziet, en dat is bewust: een beeld dat alleen via een naam in een database of een
losse json gebouwd wordt waarvan het woord nergens anders staat. Dat valt dan als ongebruikt
op, met de patroonregel erbij in `bijna`. Daarom is de opruiming omkeerbaar.
"""
import ast
import json
import re
from collections import defaultdict
from pathlib import Path

WORTEL = Path(__file__).resolve().parent.parent

BEELD_SUFFIX = (".webp", ".jpg", ".jpeg", ".png", ".avif", ".gif", ".svg", ".ico")
# Wat een verwijzing kan bevatten. Beeldbestanden zelf staan er niet in; svg wel, want een svg
# kan een ander bestand inladen.
LEES_SUFFIX = (".html", ".css", ".js", ".mjs", ".cjs", ".json", ".xml", ".txt", ".md", ".py",
               ".svg", ".webmanifest")

NOOIT = ("node_modules", "__pycache__", ".git", ".claude", ".codex", ".vercel")

# Bestanden die over beeldpaden gaan in plaats van er een te gebruiken. Zouden ze wel meetellen,
# dan houdt de opruiming zichzelf in leven: de lijst van wat weg mag noemt elk pad dat weg mag.
NIET_ALS_BRON = ("_werk/beeldpaden.py", "_werk/opruimen-beelden.py",
                 "website/review/opruimen-beelden-20260922/")

# De bouwbron: hieruit verwijzen betekent dat het beeld na de eerstvolgende build op de site staat.
LIVE_MAPPEN = ("css", "js", "_werk")
# img/headers/manifest.json ligt in een assetmap maar is een bouwbron: kit.py:252 headerbeeld()
# leest hem per route en gooit een BouwFout als hij ontbreekt. Zonder deze regel telt hij als
# bron, en dan overleven de twintig headerbeelden alleen doordat hun naam toevallig ook in de
# gebouwde html of in _voorbeeld/ staat. Gevonden door dereus-49, 22-09-2026.
LIVE_PADEN = ("website/content/", "img/headers/manifest.json")
# Generatoren, reviewrondes, ontwerpvarianten, keuzereeksen, voorvertoning.
BRON_MAPPEN = ("_ai-beelden", "website", "beeld-opties", "logo-opties", "_ontwerpen",
               "_voorbeeld", "brandbook", "docs", "_bron", "sitemap")
# Assetmappen. Een svg daarin mag verwijzen, maar telt als bron: een ongebruikte svg moet geen
# ander beeld levend kunnen houden alsof de site het gebruikt.
ASSET_MAPPEN = ("img", "fonts")

PLAATSHOUDER_RE = re.compile(r"\{[^{}]*\}|%\([^)]*\)[sdr]|%[sdr]|\$\{[^{}]*\}")
MARKER = "\x00"
# Een pad dat met / begint of, in een los tekstfragment, met img/ aan het begin.
KERN_RE = re.compile(r"(?:^|/)((?:img|fonts)/[A-Za-z0-9_.\-/" + MARKER + r"]*)")
# Losse bestanden in de wortel: /favicon.ico, /og.jpg, /logo_try.jpeg.
WORTEL_RE = re.compile(
    r"""(?:^|["'(=\s,])/([A-Za-z0-9_.\-]+\.(?:webp|jpe?g|png|avif|gif|svg|ico|webmanifest))""",
    re.I)
WOORD_RE = re.compile(r"[a-z0-9][a-z0-9_-]{1,60}")
# Waar een echte verwijzing op eindigt. Zonder deze zeef levert `url(/img/${naam}.webp)` uit een
# generator de kern "img" op, en dat is een map en geen beeld.
ASSET_SUFFIX = BEELD_SUFFIX + (".woff2", ".woff", ".ttf", ".otf", ".webmanifest")
# Korter dan dit zegt een ingevuld stuk niets meer; dan telt het patroon niet als bewijs.
MIN_INGEVULD = 3


def rel(pad: Path) -> str:
    return pad.relative_to(WORTEL).as_posix()


def klasse_van_bron(relpad: str):
    """live, bron of None (doet niet mee) voor een bestand dat naar beelden kan verwijzen."""
    delen = relpad.split("/")
    if any(deel in NOOIT for deel in delen):
        return None
    if any(relpad == n or relpad.startswith(n) for n in NIET_ALS_BRON):
        return None
    if any(relpad.startswith(p) for p in LIVE_PADEN):
        return "live"
    eerste = delen[0]
    if eerste in ASSET_MAPPEN or eerste in BRON_MAPPEN:
        return "bron"
    if eerste in LIVE_MAPPEN:
        return "live"
    # Alles wat verder in de wortel staat is de deploy-root: index.html, contact/index.html,
    # 404.html, sitemap.xml, robots.txt.
    return "live"


def bronbestanden():
    """Elk bestand dat naar een beeld kan verwijzen, met zijn klasse."""
    uit = []
    for pad in WORTEL.rglob("*"):
        if not pad.is_file() or pad.suffix.lower() not in LEES_SUFFIX:
            continue
        r = rel(pad)
        klasse = klasse_van_bron(r)
        if klasse:
            uit.append((r, pad, klasse))
    return sorted(uit)


def geserveerd():
    """Alleen wat de bezoeker echt opvraagt: de gebouwde pagina's, de css, de js, de svg's.

    Scheelt van `bronbestanden()` dat _werk/ en website/content/ er niet in zitten. Die tellen
    wel mee om een beeld levend te verklaren, maar niet om te controleren of een pad bestaat:
    een docstring of een zelftest mag een pad noemen dat er niet is, een gebouwde pagina niet.
    """
    uit = []
    for pad in WORTEL.rglob("*"):
        if not pad.is_file() or pad.suffix.lower() not in LEES_SUFFIX:
            continue
        r = rel(pad)
        delen = r.split("/")
        if any(deel in NOOIT for deel in delen):
            continue
        if delen[0] in BRON_MAPPEN or delen[0] == "_werk":
            continue
        uit.append((r, pad))
    return sorted(uit)


def _letterlijken_python(tekst):
    """Alle stringwaarden uit een python-bestand, met f-strings als `{}`-patroon.

    Via ast en niet via een regex op aanhalingstekens, want de meeste beeldpaden in _werk
    staan in een f-string die zelf weer aanhalingstekens bevat.
    """
    try:
        boom = ast.parse(tekst)
    except SyntaxError:
        return []
    uit = []
    for knoop in ast.walk(boom):
        if isinstance(knoop, ast.Constant) and isinstance(knoop.value, str):
            uit.append(knoop.value)
        elif isinstance(knoop, ast.JoinedStr):
            stukken = []
            for deel in knoop.values:
                if isinstance(deel, ast.Constant) and isinstance(deel.value, str):
                    stukken.append(deel.value)
                else:
                    stukken.append("{}")
            uit.append("".join(stukken))
    return uit


def _kernen(tekst, maskeer=False):
    """De beeldpaden in een stuk tekst, als {(kern, is_patroon)}.

    kern is repo-relatief zonder leidende slash: img/foo.webp, fonts/inter-latin.woff2.

    Maskeren is alleen voor python. In een f-string is `{...}` een plaatshouder, maar in css is
    het een regelblok en in html een style-blok: daar de plaatshouders wegstrepen wist het halve
    bestand. Dat kostte een ronde: `url(/img/kaart-3d/kantoor.webp)` zit midden in een regel
    `.b-kaart__kantoor{...}`, en die hele regel verdween onder een marker.
    """
    gemaskeerd = PLAATSHOUDER_RE.sub(MARKER, tekst) if maskeer else tekst
    uit = set()
    for m in KERN_RE.finditer(gemaskeerd):
        kern = m.group(1).rstrip("/.")
        if not kern or " " in kern:
            continue
        is_patroon = MARKER in kern
        if not is_patroon and not kern.lower().endswith(ASSET_SUFFIX):
            continue
        uit.add((kern, is_patroon))
    for m in WORTEL_RE.finditer(gemaskeerd):
        naam = m.group(1)
        if MARKER not in naam:
            uit.add((naam, False))
    return uit


def verwijzingen(tekst, is_python=False):
    """Alle beeldverwijzingen in een bestand, als {(kern, is_patroon)}."""
    if not is_python:
        return _kernen(tekst)
    uit = set()
    for letterlijk in _letterlijken_python(tekst):
        uit |= _kernen(letterlijk, maskeer=True)
    # Ook buiten de stringwaarden kijken: commentaar en docstrings noemen vaak een pad, en dat
    # is voor het levend houden van een beeld net zo goed bewijs als de code zelf. Patronen uit
    # commentaar tellen niet mee; die zijn bijna altijd een zin en geen verwijzing.
    uit |= {(k, p) for k, p in _kernen(tekst, maskeer=True) if not p}
    return uit


def bruikbaar_patroon(kern):
    """Of dit patroon een pad beschrijft of alleen over paden praat.

    De grens ligt bij de extensie. `img/kaart-{slug}.svg` eindigt op een echte extensie en
    `/img/{FOTOS[i]}` vult de hele bestandsnaam in; beide bouwen een pad. Maar
    `img/{...}-{...}.{...}` uit een notitie over naamgeving zet een plaatshouder op de plek van
    de extensie, en dat is geen verwijzing maar een beschrijving. Zonder deze grens houdt een
    zin als "de foto's heten img/<onderwerp>-<variant>.<ext>" elke webp in de repo levend.
    """
    if kern.lower().endswith(BEELD_SUFFIX):
        return True
    kop = kern[:-len(MARKER)] if kern.endswith(MARKER) else None
    return bool(kop) and kop.endswith("/")


def naar_patroon(kern):
    """Van `img/kaart-<marker>.svg` naar een regex die op een repo-pad past."""
    stukken = kern.split(MARKER)
    patroon = "[^/]+".join(re.escape(s) for s in stukken)
    return re.compile("^" + patroon + "$")


def ingevuld(kern, pad):
    """Wat het patroon op deze plek heeft ingevuld, zonder extensie. None als het niet past."""
    stukken = kern.split(MARKER)
    patroon = "([^/]+)".join(re.escape(s) for s in stukken)
    m = re.match("^" + patroon + "$", pad)
    if not m:
        return None
    return [re.sub(r"\.(webp|jpe?g|png|avif|gif|svg|ico)$", "", g, flags=re.I)
            for g in m.groups()]


def kopijwoorden(bestanden):
    """Elk woord uit de kopij. Dat is de ene plek buiten de code waar een beeldnaam vandaan komt.

    Bewust NIET alle woorden uit de hele bouwbron. Die eerste versie liet een woord uit het ene
    bestand een patroon in het andere goedkeuren: `img/{map_}/{naam}.webp` uit tijdlijn.py werd
    gedekt door het woord 'doos' uit contactkaarten.py, en zo gold `img/kaart-3d/doos.webp` als
    in gebruik terwijl de tabel in tijdlijn.py dat bestand helemaal niet kent. Zie `gedekt()`.
    """
    woorden = set()
    for r, pad, klasse in bestanden:
        if klasse != "live" or not any(r.startswith(p) for p in LIVE_PADEN):
            continue
        # Dezelfde uitzondering als _b4.kopijbestanden(): die globt *.md en laat alles met
        # -feiten en alles met _ ervoor liggen, dus zo'n bestand levert nooit een slug op. Zonder
        # deze regel houdt een los feitenbestand (zoals lansingerland-feiten.md) een kaart-*.svg in
        # leven terwijl er geen plaatspagina is die die kaart ooit opvraagt.
        kaal = pad.stem
        if kaal.endswith("-feiten") or kaal.startswith("_"):
            continue
        try:
            tekst = pad.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            continue
        woorden.update(WOORD_RE.findall(tekst))
    # De kopij noemt beelden zonder extensie ("beeld: verhuisdag-aankomst"); die staan er dus al
    # in. De uitsnedelijst is geen live bestand maar wel een bouwbron.
    uitstap = WORTEL / "_ai-beelden" / "uitstap.json"
    if uitstap.exists():
        try:
            woorden.update(k.lower() for k in json.loads(uitstap.read_text(encoding="utf-8")))
        except ValueError:
            pass
    return woorden


def gedekt(delen, woorden_hier, regels_hier, kopij):
    """Of het ingevulde stuk van een patroon ergens op steunt.

    De bron moet die van het patroon zelf zijn: het bestand waarin de f-string staat, of de
    kopij. Bij twee of meer plaatshouders moeten alle stukken op dezelfde REGEL staan, want zo
    staan de tabellen erin:

        VOORWERPEN = [("contact-3d", "telefoon", 208, 400), ...]

    Daardoor geldt `img/contact-3d/telefoon.webp` als in gebruik en `img/kaart-3d/telefoon.webp`
    niet: er is geen regel met allebei die woorden. Zonder die eis dekt elk woord elk ander.
    """
    if not delen or any(len(d) < MIN_INGEVULD for d in delen):
        return False
    klein = [d.lower() for d in delen]
    if len(klein) == 1:
        return klein[0] in woorden_hier or klein[0] in kopij
    if all(d in kopij for d in klein):
        return True
    return any(all(d in regel for d in klein) for regel in regels_hier)


def inventaris(extra=()):
    """Elk beeldbestand in img/ en los in de wortel, plus wat er meegegeven wordt."""
    uit = set()
    for pad in (WORTEL / "img").rglob("*"):
        if pad.is_file() and pad.suffix.lower() in BEELD_SUFFIX:
            uit.add(rel(pad))
    for pad in WORTEL.glob("*"):
        if pad.is_file() and pad.suffix.lower() in BEELD_SUFFIX:
            uit.add(rel(pad))
    uit.update(extra)
    return sorted(uit)


def scan(extra=()):
    """De hele kaart: per beeld zijn klasse en het bewijs daarvoor.

    Geeft {pad: {"klasse": ..., "bewijs": [...], "bijna": [...]}}. `bijna` is de reden om nog
    even te kijken: het bestand past op een patroon uit de bouwbron, maar het ingevulde stuk
    komt nergens in de kopij voor.
    """
    bestanden = bronbestanden()
    kopij = kopijwoorden(bestanden)
    lijst = inventaris(extra)

    concreet = {"live": defaultdict(list), "bron": defaultdict(list)}
    patronen = {"live": [], "bron": []}
    # Alleen voor bestanden die echt een patroon bevatten; dat zijn er een stuk of tien.
    tekstbuffer = {}

    for r, pad, klasse in bestanden:
        try:
            tekst = pad.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for kern, is_patroon in verwijzingen(tekst, pad.suffix.lower() == ".py"):
            if is_patroon:
                if bruikbaar_patroon(kern):
                    if r not in tekstbuffer:
                        laag = tekst.lower()
                        tekstbuffer[r] = (set(WOORD_RE.findall(laag)),
                                          [set(WOORD_RE.findall(regel))
                                           for regel in laag.splitlines()])
                    patronen[klasse].append((kern, naar_patroon(kern), r))
            else:
                concreet[klasse][kern].append(r)

    uit = {}
    for pad in lijst:
        bewijs, bijna, klasse = [], [], "ongebruikt"
        for soort, naam in (("live", "in gebruik"), ("bron", "bronmateriaal")):
            for bron in concreet[soort].get(pad, []):
                bewijs.append(f"genoemd in {bron}")
            for kern, regex, bron in patronen[soort]:
                if not regex.match(pad):
                    continue
                delen = ingevuld(kern, pad) or []
                woorden_hier, regels_hier = tekstbuffer.get(bron, (set(), []))
                zichtbaar = kern.replace(MARKER, "{...}")
                if gedekt(delen, woorden_hier, regels_hier, kopij):
                    bewijs.append(f"{zichtbaar} uit {bron} met "
                                  f"{', '.join(repr(d) for d in delen)}")
                else:
                    bijna.append(f"past op {zichtbaar} uit {bron}, maar "
                                 f"{', '.join(repr(d) for d in delen)} staat niet in {bron} "
                                 f"en niet in de kopij")
            if bewijs:
                klasse = naam
                break
        uit[pad] = {"klasse": klasse, "bewijs": bewijs, "bijna": bijna}
    return uit


def leesbaar(bytes_):
    """Een bytegetal als leesbare maat."""
    maat = float(bytes_)
    for eenheid in ("B", "KB", "MB", "GB"):
        if maat < 1024 or eenheid == "GB":
            return f"{maat:.0f} {eenheid}" if eenheid == "B" else f"{maat:.1f} {eenheid}"
        maat /= 1024


if __name__ == "__main__":
    import sys
    kaart = scan()
    tel = defaultdict(int)
    for pad, gegevens in sorted(kaart.items()):
        tel[gegevens["klasse"]] += 1
    breed = "--breed" in sys.argv
    for pad, gegevens in sorted(kaart.items()):
        if breed or gegevens["klasse"] != "in gebruik":
            print(f"{gegevens['klasse']:<14} {pad}")
            for regel in gegevens["bewijs"][:2] + gegevens["bijna"][:2]:
                print(f"               {regel}")
    print()
    print("   ".join(f"{k}: {v}" for k, v in sorted(tel.items())))
