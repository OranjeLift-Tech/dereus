"""Controle van de beelden in de gebouwde pagina's.

Gebruik: python _werk/controle-beelden.py [--streng]
         python _werk/controle-beelden.py --vangnet

--vangnet is het net onder de opruimronde: elk beeld-, svg- en lettertypepad dat een
geserveerd bestand opvraagt moet naar een bestaand bestand wijzen. Waar controle A alleen
naar src, srcset, link en og:image in de html kijkt, gaat het vangnet ook door de css en de
js, en door `url(...)` en inline styles. Dat is geen theorie: `css/blok/kaart.css` laadt
`/img/kaart-3d/kantoor.webp` uitsluitend via `url()`, en controle A ziet dat niet.

Het vangnet heeft een eigen afsluitcode 1, want dit is de enige controle die na een
verplaatsing meteen rood moet staan. De rest van dit bestand rapporteert en hangt niet aan
de build; dat blijft zo.

Vier controles:
  A  elk beeld waar de HTML om vraagt bestaat ook echt op schijf
  B  dezelfde bronfoto staat niet twee keer op een pagina, waarbij een uitsnede
     meetelt als de foto waar hij uit geknipt is
  C  de opgegeven maten kloppen met het bestand, en de pagina vraagt een beeld
     niet veel groter op dan het is
  D  elke uitsnede in _ai-beelden/uitstap.json heeft ook een webp

Staat los van bewakers.py omdat die de build laat vallen. Deze controle rapporteert
eerst, zodat hij te draaien is terwijl er nog aan de blokken gewerkt wordt. Zodra de
uitslag schoon is kan hij alsnog aan de build gehangen worden.
Met --streng is de afsluitcode 1 zodra er een fout is.

Controle B kijkt per sectie, want de regel gaat over dezelfde foto op twee plekken
op een pagina. Twee verwijzingen binnen een sectie zijn meestal een opbouw, zoals een
uitsnede over zijn eigen bronfoto in dezelfde tegel, of een mobiele en een brede variant
waarvan de CSS er altijd maar een toont. Die komen als waarschuwing naar boven, niet
als fout.

Wat controle B niet ziet, en dat is bewust zo opgeschreven: wij hebben geen manifest
dat een afgeleid beeld aan zijn origineel koppelt, zoals Brocken dat wel heeft. De
controle leunt daarom op de naamafspraak, "-uit" hoort bij de foto zonder "-uit" en
"-700" bij de naam zonder maat. Twee foto's uit dezelfde reeks onder verschillende
namen ziet hij dus niet, en een uitsnede waarvan de bron hernoemd is ook niet. Hij
leest ook geen CSS, dus of een van twee varianten werkelijk verborgen is kan hij niet
zien, alleen dat ze in dezelfde sectie staan.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

WORTEL = Path(__file__).resolve().parent.parent

# Mappen die geen gebouwde pagina's bevatten. _bron is de binnengehaalde Wix-pagina.
UITGESLOTEN_MAPPEN = ("_voorbeeld", "beeld-opties", "logo-opties", "brandbook", "website",
                      "_ai-beelden", "node_modules", "_bron")
BEELD_SUFFIX = (".webp", ".jpg", ".jpeg", ".png", ".avif", ".gif", ".svg", ".ico")
RASTER_SUFFIX = (".webp", ".jpg", ".jpeg", ".png", ".avif")
# Merkbeeld en pictogrammen horen vaker op een pagina, die vallen buiten controle B.
HERHAALBAAR = ("/img/logo/", "/img/icon/", "/img/favicon", "/img/og.")
ORIGINE_RE = re.compile(r"^https?://[^/]+")
UITSNEDE_RE = re.compile(r"-uit$")
MAAT_RE = re.compile(r"-\d{2,4}$")      # team-hero-700 hoort bij team-hero
OPBLAAS_GRENS = 1.3


def paginas():
    """Alle gebouwde pagina's in de wortel, zonder voorbeeld-, keuze- en bronmappen."""
    uit = []
    for pad in sorted(WORTEL.rglob("*.html")):
        rel = pad.relative_to(WORTEL).as_posix()
        if any(rel == m or rel.startswith(m + "/") for m in UITGESLOTEN_MAPPEN):
            continue
        uit.append(pad)
    return uit


def naar_pad(url):
    """Een url uit de HTML naar een pad in de repo. Geeft None bij externe of data-urls."""
    url = url.strip()
    if not url or url.startswith(("data:", "mailto:", "tel:", "#")):
        return None
    url = ORIGINE_RE.sub("", url)
    url = url.split("?")[0].split("#")[0]
    if not url.startswith("/"):
        return None
    if not url.lower().endswith(BEELD_SUFFIX):
        return None
    return url


def uit_srcset(waarde):
    """Haal de urls uit een srcset of imagesrcset."""
    uit = []
    for deel in waarde.split(","):
        deel = deel.strip()
        if deel:
            uit.append(deel.split()[0])
    return uit


def verwijzingen(html):
    """Alle beeldverwijzingen op een pagina.

    Geeft (url, soort, element_id, attributen). Alles binnen een picture krijgt een
    en hetzelfde element_id, want een webp met een png ernaast is een beeld en geen twee.
    """
    # Eerst de picture-blokken, zodat source en img daarbinnen bij elkaar horen.
    blokken = [(m.start(), m.end(), "pic%d" % i)
               for i, m in enumerate(re.finditer(r"<picture\b.*?</picture>", html, re.S | re.I))]

    def element_id(pos, eigen):
        for start, eind, naam in blokken:
            if start <= pos < eind:
                return naam
        return eigen

    uit = []
    for m in re.finditer(r"<(img|source)\b([^>]*)>", html, re.I):
        attrs = m.group(2)
        eid = element_id(m.start(), "el%d" % m.start())
        for naam in ("src", "srcset", "imagesrcset"):
            a = re.search(r'\b%s="([^"]*)"' % naam, attrs, re.I)
            if not a:
                continue
            urls = uit_srcset(a.group(1)) if "srcset" in naam.lower() else [a.group(1)]
            for u in urls:
                uit.append((u, m.group(1).lower(), eid, attrs, m.start()))

    for m in re.finditer(r"<link\b([^>]*)>", html, re.I):
        attrs = m.group(1)
        rel = (re.search(r'\brel="([^"]*)"', attrs, re.I) or [None, ""])[1].lower()
        alsdit = (re.search(r'\bas="([^"]*)"', attrs, re.I) or [None, ""])[1].lower()
        if "icon" not in rel and not (rel == "preload" and alsdit == "image"):
            continue
        for naam in ("href", "imagesrcset"):
            a = re.search(r'\b%s="([^"]*)"' % naam, attrs, re.I)
            if not a:
                continue
            urls = uit_srcset(a.group(1)) if naam == "imagesrcset" else [a.group(1)]
            for u in urls:
                uit.append((u, "link-" + (rel or alsdit), "link%d" % m.start(), attrs, m.start()))

    for m in re.finditer(r'<meta\b[^>]*(?:property|name)="(og:image|twitter:image)"[^>]*>', html, re.I):
        a = re.search(r'\bcontent="([^"]*)"', m.group(0), re.I)
        if a:
            uit.append((a.group(1), "meta", "meta%d" % m.start(), "", m.start()))
    return uit


def secties(html):
    """Begin en naam van elke sectie op de pagina, om verwijzingen aan toe te wijzen."""
    uit = []
    for m in re.finditer(r"<section\b([^>]*)>", html, re.I):
        naam = re.search(r'\bid="([^"]*)"', m.group(1)) or re.search(r'\bclass="([^"]*)"', m.group(1))
        uit.append((m.start(), (naam.group(1).split()[0] if naam else "sectie") ))
    return uit


def sectie_van(pos, lijst):
    """De laatste sectie die voor deze positie begint."""
    label = "(buiten een sectie)"
    for start, naam in lijst:
        if start <= pos:
            label = naam
        else:
            break
    return label


def bronsleutel(pad):
    """Herleid een bestandspad naar de bronfoto, volgens de naamafspraak in deze repo.

    dienst-opslag-uit.webp  ->  img/dienst-opslag
    team/team-hero-700.webp ->  img/team/team-hero
    """
    p = pad.rsplit(".", 1)[0]
    vorig = None
    while p != vorig:
        vorig = p
        p = UITSNEDE_RE.sub("", p)
        p = MAAT_RE.sub("", p)
    return p


def afmetingen(pad, buffer={}):
    """Werkelijke afmetingen van een beeldbestand, of None als het niet te lezen is."""
    if pad.suffix.lower() == ".svg":
        return None
    sleutel = str(pad)
    if sleutel in buffer:
        return buffer[sleutel]
    maat = None
    try:
        from PIL import Image
        with Image.open(pad) as im:
            maat = im.size
    except Exception:
        maat = None
    buffer[sleutel] = maat
    return maat


def controleer():
    fouten, waarsch = [], []
    gemeld = set()

    for pagina in paginas():
        rel_pagina = "/" + pagina.relative_to(WORTEL).as_posix()
        html = pagina.read_text(encoding="utf-8", errors="replace")
        sectielijst = secties(html)
        per_bron = defaultdict(set)
        bron_urls = defaultdict(set)

        for url, soort, eid, attrs, pos in verwijzingen(html):
            pad_url = naar_pad(url)
            if pad_url is None:
                continue
            bestand = WORTEL / pad_url.lstrip("/")

            # A: bestaat het bestand
            if not bestand.exists():
                sleutel = (rel_pagina, pad_url)
                if sleutel not in gemeld:
                    gemeld.add(sleutel)
                    fouten.append("A  %s  ontbreekt op schijf, gevraagd via %s: %s"
                                  % (rel_pagina, soort, pad_url))
                continue

            # B: alleen echte foto's, geen merkbeeld, pictogram of metadata
            if soort in ("img", "source") and pad_url.lower().endswith(RASTER_SUFFIX) \
                    and not any(h in pad_url.lower() for h in HERHAALBAAR):
                sleutel = bronsleutel(pad_url.lstrip("/"))
                per_bron[sleutel].add((sectie_van(pos, sectielijst), eid))
                bron_urls[sleutel].add(pad_url)

            # C: kloppen de opgegeven maten met het bestand
            if soort == "img":
                echt = afmetingen(bestand)
                b = re.search(r'\bwidth="(\d+)"', attrs)
                h = re.search(r'\bheight="(\d+)"', attrs)
                if echt and b and h:
                    opgegeven = (int(b.group(1)), int(h.group(1)))
                    if opgegeven != echt:
                        factor = max(opgegeven[0] / echt[0], opgegeven[1] / echt[1])
                        regel = "%s  %s  opgegeven %dx%d, bestand %dx%d" % (
                            rel_pagina, pad_url, opgegeven[0], opgegeven[1], echt[0], echt[1])
                        sleutel = ("C", rel_pagina, pad_url)
                        if sleutel in gemeld:
                            continue
                        gemeld.add(sleutel)
                        if factor > OPBLAAS_GRENS:
                            fouten.append("C  " + regel + "  (%.2fx opgeblazen)" % factor)
                        else:
                            waarsch.append("C  " + regel)

        for sleutel, plekken in sorted(per_bron.items()):
            urls = ", ".join(sorted(bron_urls[sleutel]))
            secs = {sec for sec, _ in plekken}
            elems = {eid for _, eid in plekken}
            if len(secs) > 1:
                fouten.append("B  %s  bronfoto %s in %d secties (%s): %s" % (
                    rel_pagina, sleutel, len(secs), ", ".join(sorted(secs)), urls))
            elif len(elems) > 1:
                # Binnen een sectie is dit vrijwel altijd opbouw of een responsieve variant.
                waarsch.append("B  %s  bronfoto %s in %d elementen binnen sectie %s: %s" % (
                    rel_pagina, sleutel, len(elems), "".join(secs), urls))

    return fouten, waarsch


def uitsnedes_zonder_bestand():
    """Losse controle op _ai-beelden/uitstap.json: staat er een uitsnede in zonder webp."""
    bron = WORTEL / "_ai-beelden" / "uitstap.json"
    if not bron.exists():
        return []
    try:
        data = json.loads(bron.read_text(encoding="utf-8"))
    except ValueError:
        return ["D  _ai-beelden/uitstap.json is geen geldige json"]
    uit = []
    for naam in sorted(data):
        kandidaten = [WORTEL / "img" / ("dienst-%s-uit.webp" % naam),
                      WORTEL / "img" / ("%s-uit.webp" % naam)]
        if not any(k.exists() for k in kandidaten):
            uit.append("D  uitstap.json noemt '%s' maar er is geen %s" % (
                naam, " of ".join(k.relative_to(WORTEL).as_posix() for k in kandidaten)))
    return uit


ZELFTEST = """<html><body>
<section id="een">
  <img src="/img/proef-foto.webp" alt="" width="10" height="10">
</section>
<section id="twee">
  <img src="/img/proef-foto-uit.webp" alt="" width="10" height="10">
</section>
<section id="drie">
  <picture><source srcset="/img/ander-700.webp 700w"><img src="/img/ander-700.png" alt=""></picture>
</section>
</body></html>"""


def zelftest():
    """Controleer dat B een echte dubbele bronfoto ziet en een picture met rust laat."""
    html = ZELFTEST
    lijst = secties(html)
    per_bron = {}
    for url, soort, eid, attrs, pos in verwijzingen(html):
        pad_url = naar_pad(url)
        if pad_url is None or soort not in ("img", "source"):
            continue
        sleutel = bronsleutel(pad_url.lstrip("/"))
        per_bron.setdefault(sleutel, set()).add((sectie_van(pos, lijst), eid))
    proef = per_bron.get("img/proef-foto", set())
    ander = per_bron.get("img/ander", set())
    goed = True
    if len({s for s, _ in proef}) != 2:
        print("  ZELFTEST FAALT: uitsnede en bronfoto in twee secties niet herkend:", proef)
        goed = False
    if len({s for s, _ in ander}) != 1 or len({e for _, e in ander}) != 1:
        print("  ZELFTEST FAALT: picture telt als meer dan een element:", ander)
        goed = False
    if goed:
        print("  zelftest in orde: kruist secties wordt gezien, picture telt als een beeld")
    return goed


def vangnet():
    """Elk pad dat een geserveerd bestand opvraagt moet bestaan.

    Patronen (`/img/kaart-{slug}.svg`) blijven buiten beschouwing: die staan in de bouwbron en
    niet in een geserveerd bestand, en of ze ergens op uitkomen is de vraag van beeldpaden.py.
    """
    import beeldpaden

    ontbreekt, gekeken, bestanden = [], 0, 0
    for rel_bron, pad in beeldpaden.geserveerd():
        try:
            tekst = pad.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        bestanden += 1
        for kern, is_patroon in sorted(beeldpaden.verwijzingen(tekst)):
            if is_patroon:
                continue
            gekeken += 1
            if not (beeldpaden.WORTEL / kern).exists():
                ontbreekt.append((rel_bron, kern))

    print("Vangnet: %d verwijzingen in %d geserveerde bestanden" % (gekeken, bestanden))
    if not ontbreekt:
        print("GOED  elk pad komt uit op een bestaand bestand")
        return 0
    print("FOUT  %d %s naar een bestand dat er niet is:"
          % (len(ontbreekt),
             "verwijzing wijst" if len(ontbreekt) == 1 else "verwijzingen wijzen"))
    for bron, kern in ontbreekt:
        print("  %s  vraagt om /%s" % (bron, kern))
    print("\nTerugzetten: python _werk/opruimen-beelden.py --terug")
    return 1


def main():
    if "--zelftest" in sys.argv:
        return 0 if zelftest() else 1
    if "--vangnet" in sys.argv:
        return vangnet()
    fouten, waarsch = controleer()
    los = uitsnedes_zonder_bestand()
    aantal = len(paginas())

    print("Beeldcontrole over %d gebouwde pagina's" % aantal)
    print()
    if fouten:
        print("FOUTEN (%d)" % len(fouten))
        for f in fouten:
            print("  " + f)
        print()
    if los:
        print("LOSSE EINDJES in uitstap.json (%d)" % len(los))
        for f in los:
            print("  " + f)
        print()
    if waarsch:
        print("WAARSCHUWINGEN (%d), nakijken maar vrijwel altijd bedoeld" % len(waarsch))
        for w in waarsch:
            print("  " + w)
        print()
    if not (fouten or waarsch or los):
        print("Niets gevonden.")

    print("A ontbrekend: %d   B dubbele bronfoto: %d   C opgeblazen: %d   D uitstap.json: %d" % (
        sum(1 for f in fouten if f.startswith("A")),
        sum(1 for f in fouten if f.startswith("B")),
        sum(1 for f in fouten if f.startswith("C")),
        len(los)))

    if "--streng" in sys.argv and (fouten or los):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
