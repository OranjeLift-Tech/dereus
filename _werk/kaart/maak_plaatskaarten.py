"""Statische routekaarten voor de plaatspagina's /werkgebied/<slug>/ (blok plaatskaart van dereus-b4).

Per plaats één SVG, img/kaart-<slug>.svg, 1400 x 933 zoals img/kaart-den-haag.svg: de gemeente uitgelicht, Den Haag
ernaast, de route vanaf het hoofdkantoor aan de Lau Mazirellaan 336 en een speld op de plaats (naar het idee van de
Tilburg-pagina van Brocken). Alleen OpenStreetMap-data (ODbL): gemeentegrenzen, grote wegen en water via Overpass,
de route via OSRM (ook OpenStreetMap). De bronvermelding staat als bijschrift in het blok, niet in het beeld.
Het middelpunt van een woonplaats komt van de PDOK Locatieserver.

Draaien: python _werk/kaart/maak_plaatskaarten.py [slug ...]
De data (Overpass, tientallen MB) en de routes worden in de tijdelijke map van het systeem bewaard, niet in de repo.
Een slug moet gelijk zijn aan het kopijbestand website/content/plaatsen/<slug>.md.
Kleuren alleen uit brandbook/tokens.css, zoals in maak_kaart.py.
"""
import json
import math
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TMP = Path(tempfile.gettempdir())
BRON = TMP / "dereus-osm-regio.json"
MLAT, MLON = 52.0596297, 4.29913794          # PDOK: Lau Mazirellaan 336, Den Haag
BR, HO = 1400, 933

# slug, naam op de kaart, gemeente zoals in OpenStreetMap, woonplaats waar de route naartoe gaat (de grootste kern)
PLAATSEN = [
    ("rijswijk", "Rijswijk", "Rijswijk", "Rijswijk"),
    ("delft", "Delft", "Delft", "Delft"),
    ("zoetermeer", "Zoetermeer", "Zoetermeer", "Zoetermeer"),
    ("leidschendam-voorburg", "Voorburg", "Leidschendam-Voorburg", "Voorburg"),
    ("westland", "Naaldwijk", "Westland", "Naaldwijk"),
    ("wassenaar", "Wassenaar", "Wassenaar", "Wassenaar"),
    ("pijnacker-nootdorp", "Pijnacker", "Pijnacker-Nootdorp", "Pijnacker"),
    ("leiden", "Leiden", "Leiden", "Leiden"),
    ("lansingerland", "Berkel en Rodenrijs", "Lansingerland", "Berkel en Rodenrijs"),
    ("voorschoten", "Voorschoten", "Voorschoten", "Voorschoten"),
]
DEN_HAAG = ("Den Haag", "'s-Gravenhage")

S, W, N, E = 51.90, 4.00, 52.27, 4.70         # alles wat een van de kaarten kan raken
VRAAG = (f"[out:json][timeout:240][maxsize:1073741824];("
         f'way["highway"~"^(motorway|trunk|primary|secondary)$"]({S},{W},{N},{E});'
         f'way["natural"="water"]({S},{W},{N},{E});'
         f'relation["natural"="water"]({S},{W},{N},{E});'
         f'way["waterway"~"^(river|canal)$"]({S},{W},{N},{E});'
         f'relation["boundary"="administrative"]["admin_level"="8"]({S},{W},{N},{E});'
         f'node["place"~"^(city|town|village)$"]({S},{W},{N},{E});'
         f");out geom;")

# tokens.css
MIST, ZILVER, B50, B100, B200 = "#F6F7F9", "#D3D7DE", "#F3F7FE", "#E6EFFF", "#CDDFFF"
KONINGSBLAUW, DIEPBLAUW, GOUD, LEISTEEN, WIT = "#1746A2", "#0B2352", "#FFCC33", "#5E6675", "#FFFFFF"
HUIS = "M267.6 7.8L320.9 53.2V0H356.8V83.9L535.3 236.2H457.6V509.8H326.2V384.1H209.1V509.8H77.7V236.2H0Z"
LETTER = "Inter,Segoe UI,Arial,sans-serif"


def haal_json(url, data=None, cache=None):
    if cache and cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    verzoek = urllib.request.Request(url, data=data, headers={"User-Agent": "dereus-plaatskaart/1.0"})
    tekst = urllib.request.urlopen(verzoek, timeout=300).read().decode("utf-8")
    if cache:
        cache.write_text(tekst, encoding="utf-8")
    return json.loads(tekst)


def middelpunt(woonplaats):
    q = urllib.parse.urlencode({"q": woonplaats, "fq": "type:woonplaats", "rows": 1, "fl": "weergavenaam,centroide_ll"})
    d = haal_json(f"https://api.pdok.nl/bzk/locatieserver/search/v3_1/free?{q}",
                  cache=TMP / f"dereus-pdok-{woonplaats.lower().replace(' ', '-')}.json")
    lon, lat = map(float, d["response"]["docs"][0]["centroide_ll"].replace("POINT(", "").replace(")", "").split())
    return lat, lon


def route(lat, lon, slug):
    d = haal_json(f"https://router.project-osrm.org/route/v1/driving/{MLON},{MLAT};{lon},{lat}"
                  f"?overview=full&geometries=geojson", cache=TMP / f"dereus-route-{slug}.json")
    r = d["routes"][0]
    return [(la, lo) for lo, la in r["geometry"]["coordinates"]], r["distance"] / 1000, r["duration"] / 60


def ringen(leden):
    """Buitenringen van een relatie: losse wegstukken aan elkaar rijgen tot gesloten ringen."""
    stukken = [[(p["lat"], p["lon"]) for p in m["geometry"]] for m in leden
               if m.get("type") == "way" and m.get("role", "outer") in ("outer", "") and m.get("geometry")]
    uit = []
    while stukken:
        ring = stukken.pop(0)
        verder = True
        while verder and ring[0] != ring[-1]:
            verder = False
            for i, st in enumerate(stukken):
                if st[0] == ring[-1]:
                    ring += st[1:]
                elif st[-1] == ring[-1]:
                    ring += st[::-1][1:]
                elif st[-1] == ring[0]:
                    ring = st[:-1] + ring
                elif st[0] == ring[0]:
                    ring = st[::-1][:-1] + ring
                else:
                    continue
                stukken.pop(i)
                verder = True
                break
        if len(ring) > 3:
            uit.append(ring)
    return uit


merc = lambda lat: math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


class Beeld:
    """Projectie (Web Mercator) van een lat/lon-venster naar 1400 x 933."""

    def __init__(self, punten, marge=0.12):
        ys = [merc(la) for la, _ in punten]
        xs = [math.radians(lo) for _, lo in punten]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        bx, by = (x1 - x0) or 1e-4, (y1 - y0) or 1e-4
        x0, x1, y0, y1 = x0 - bx * marge, x1 + bx * marge, y0 - by * marge, y1 + by * marge
        # naar 3:2 verbreden, gecentreerd
        doel = BR / HO
        if (x1 - x0) / (y1 - y0) < doel:
            extra = (y1 - y0) * doel - (x1 - x0)
            x0, x1 = x0 - extra / 2, x1 + extra / 2
        else:
            extra = (x1 - x0) / doel - (y1 - y0)
            y0, y1 = y0 - extra / 2, y1 + extra / 2
        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1
        self.km = (x1 - x0) * 6371 * math.cos(math.radians(MLAT))   # breedte van het beeld in km

    def xy(self, lat, lon):
        return ((math.radians(lon) - self.x0) / (self.x1 - self.x0) * BR,
                (self.y1 - merc(lat)) / (self.y1 - self.y0) * HO)

    def raakt(self, pts, rand=60):
        xs = [x for x, _ in pts]
        ys = [y for _, y in pts]
        return max(xs) > -rand and min(xs) < BR + rand and max(ys) > -rand and min(ys) < HO + rand


def vereenvoudig(pts, tol=1.6):
    uit = [pts[0]]
    for p in pts[1:-1]:
        if abs(p[0] - uit[-1][0]) + abs(p[1] - uit[-1][1]) > tol:
            uit.append(p)
    if len(pts) > 1:
        uit.append(pts[-1])
    return uit


RAND = 24                                     # knippen net buiten het beeld: kleinere bestanden, zelfde beeld
X0, Y0, X1, Y1 = -RAND, -RAND, BR + RAND, HO + RAND


def knip_vlak(pts):
    """Sutherland-Hodgman: een vlak knippen op de rechthoek rond het beeld."""
    def snij(a, b, as_, grens):
        (xa, ya), (xb, yb) = a, b
        if as_ == "x":
            t = (grens - xa) / (xb - xa)
            return grens, ya + t * (yb - ya)
        t = (grens - ya) / (yb - ya)
        return xa + t * (xb - xa), grens
    for as_, grens, binnen in (("x", X0, lambda p: p[0] >= X0), ("x", X1, lambda p: p[0] <= X1),
                               ("y", Y0, lambda p: p[1] >= Y0), ("y", Y1, lambda p: p[1] <= Y1)):
        if not pts:
            return []
        uit = []
        for i, cur in enumerate(pts):
            vor = pts[i - 1]
            if binnen(cur):
                if not binnen(vor):
                    uit.append(snij(vor, cur, as_, grens))
                uit.append(cur)
            elif binnen(vor):
                uit.append(snij(vor, cur, as_, grens))
        pts = uit
    return pts


def knip_lijn(pts):
    """Een lijn opdelen in de stukken die het beeld raken."""
    stukken, huidig = [], []
    for a, b in zip(pts, pts[1:]):
        raakt = not (max(a[0], b[0]) < X0 or min(a[0], b[0]) > X1 or max(a[1], b[1]) < Y0 or min(a[1], b[1]) > Y1)
        if raakt:
            if not huidig:
                huidig = [a]
            huidig.append(b)
        elif huidig:
            stukken.append(huidig)
            huidig = []
    if huidig:
        stukken.append(huidig)
    return stukken


def oppervlak(pts):
    return abs(sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts)))) / 2


def pad(pts, dicht=False):
    return " ".join(f"{'M' if i == 0 else 'L'}{x:.0f},{y:.0f}" for i, (x, y) in enumerate(pts)) + (" Z" if dicht else "")


def zwaartepunt(pts):
    return sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)


def tekst(x, y, inhoud, grootte=22, gewicht=600, kleur=LEISTEEN, halo=MIST, extra=""):
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-family="{LETTER}" font-weight="{gewicht}" '
            f'font-size="{grootte}" fill="{kleur}" stroke="{halo}" stroke-width="{max(5, grootte // 3)}" '
            f'paint-order="stroke"{extra}>{inhoud}</text>')


def laad():
    if not BRON.exists():
        print("Overpass ophalen (kan een paar minuten duren) ...")
        data = urllib.parse.urlencode({"data": VRAAG}).encode()
        haal_json("https://overpass-api.de/api/interpreter", data=data, cache=BRON)
    d = json.loads(BRON.read_text(encoding="utf-8"))
    gemeenten, wegen, water, kanalen, plaatsnamen = {}, [], [], [], []
    for e in d["elements"]:
        t = e.get("tags", {})
        if e["type"] == "node":
            if t.get("name"):
                plaatsnamen.append((t["name"], t.get("place"), e["lat"], e["lon"]))
        elif e["type"] == "relation":
            if t.get("boundary") == "administrative" and t.get("admin_level") == "8" and t.get("name"):
                gemeenten[t["name"]] = ringen(e.get("members", []))
            elif t.get("natural") == "water":
                water += ringen(e.get("members", []))
        else:
            g = [(p["lat"], p["lon"]) for p in e.get("geometry") or []]
            if len(g) < 2:
                continue
            if t.get("highway"):
                wegen.append((t["highway"], g))
            elif t.get("natural") == "water":
                water.append(g)
            elif t.get("waterway"):
                kanalen.append((t["waterway"], g))
    return gemeenten, wegen, water, kanalen, plaatsnamen


def speld_de_reus(x, y):
    schaal = 26 / 535.3
    return (f'<g transform="translate({x:.0f},{y:.0f})" filter="url(#k-schaduw)">'
            f'<path d="M0,10 C0,10 -32,-24 -32,-46 A32,32 0 1 1 32,-46 C32,-24 0,10 0,10 Z" fill="{KONINGSBLAUW}" '
            f'stroke="{WIT}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="{HUIS}" fill="{GOUD}" transform="translate(-13,-58.5) scale({schaal:.5f})"/></g>')


def speld_plaats(x, y):
    return (f'<g transform="translate({x:.0f},{y:.0f})" filter="url(#k-schaduw)">'
            f'<path d="M0,10 C0,10 -32,-24 -32,-46 A32,32 0 1 1 32,-46 C32,-24 0,10 0,10 Z" fill="{DIEPBLAUW}" '
            f'stroke="{WIT}" stroke-width="5" stroke-linejoin="round"/>'
            f'<circle cx="0" cy="-46" r="11" fill="{GOUD}"/></g>')


def kaart(slug, label, gemeente, woonplaats, bron):
    gemeenten, wegen, water, kanalen, plaatsnamen = bron
    if gemeente not in gemeenten:
        raise SystemExit(f"{slug}: gemeente '{gemeente}' niet in de OSM-data (wel: {', '.join(sorted(gemeenten))})")
    lat, lon = middelpunt(woonplaats)
    lijn, km, minuten = route(lat, lon, slug)
    doelring = max(gemeenten[gemeente], key=len)
    beeld = Beeld([(MLAT, MLON), (lat, lon)] + doelring[::5])
    xy = beeld.xy
    detail = beeld.km < 16                  # kleine kaart: ook provinciale wegen en kleinere dorpen

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BR} {HO}" width="{BR}" height="{HO}" role="img" '
         f'aria-label="Kaart met de route van het hoofdkantoor van Verhuisbedrijf De Reus aan de Lau Mazirellaan 336 '
         f'in Den Haag naar {label} ({gemeente}), ongeveer {km:.0f} kilometer over de weg">',
         '<defs><filter id="k-schaduw" x="-40%" y="-40%" width="180%" height="180%">'
         f'<feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="{DIEPBLAUW}" flood-opacity=".35"/></filter></defs>',
         # ondergrond Blauw 100: wat buiten de gemeenten valt is zee of groot water
         f'<rect width="{BR}" height="{HO}" fill="{B100}"/>']

    # Gemeenten: wit, Den Haag Mist, de plaats zelf Blauw 50 met een Koningsblauwe rand
    vlakken = {"gewoon": [], "haag": [], "doel": []}
    haag_pts = []
    for naam, rs in gemeenten.items():
        soort = "doel" if naam == gemeente else ("haag" if naam in DEN_HAAG else "gewoon")
        for r in rs:
            pts = knip_vlak(vereenvoudig([xy(*p) for p in r]))
            if len(pts) > 3 and oppervlak(pts) > 50:
                vlakken[soort].append(pad(pts, True))
                if soort == "haag":
                    haag_pts.extend(p for p in pts if 0 < p[0] < BR and 0 < p[1] < HO)
    s.append(f'<g fill="{WIT}" stroke="{ZILVER}" stroke-width="2" stroke-linejoin="round">'
             + "".join(f'<path d="{p}"/>' for p in vlakken["gewoon"]) + "</g>")
    s.append(f'<g fill="{MIST}" stroke="{ZILVER}" stroke-width="2" stroke-linejoin="round">'
             + "".join(f'<path d="{p}"/>' for p in vlakken["haag"]) + "</g>")

    # Water
    min_opp = 900 if detail else 1400
    plassen = []
    for r in water:
        pts = knip_vlak(vereenvoudig([xy(*p) for p in r]))
        if len(pts) > 3 and oppervlak(pts) > min_opp:
            plassen.append(pad(pts, True))
    if plassen:
        s.append(f'<g fill="{B200}">' + "".join(f'<path d="{p}"/>' for p in plassen) + "</g>")
    lopen = []
    for soort, g in kanalen:
        if soort == "river" or detail:
            for stuk in knip_lijn(vereenvoudig([xy(*p) for p in g], 2.5)):
                if len(stuk) > 2:
                    lopen.append(pad(stuk))
    if lopen:
        s.append(f'<g fill="none" stroke="{B200}" stroke-width="{5 if detail else 4}" stroke-linecap="round" '
                 'stroke-linejoin="round" opacity=".85">' + "".join(f'<path d="{p}"/>' for p in lopen) + "</g>")

    # De uitgelichte gemeente boven het water, half doorzichtig, zodat plassen erin blauw blijven
    s.append(f'<g fill="{B50}" fill-opacity=".55" stroke="{KONINGSBLAUW}" stroke-width="3.5" stroke-linejoin="round" '
             'stroke-dasharray="10 7">' + "".join(f'<path d="{p}"/>' for p in vlakken["doel"]) + "</g>")

    # Wegen: rand Zilvergrijs, kern wit
    soorten = ["secondary", "primary", "trunk", "motorway"] if detail else ["primary", "trunk", "motorway"]
    breed = {"motorway": (11, 7), "trunk": (10, 6.2), "primary": (7.5, 4.6), "secondary": (5.5, 3.2)}
    weg_paden = {}
    for soort, g in wegen:
        if soort in soorten:
            for stuk in knip_lijn(vereenvoudig([xy(*p) for p in g])):
                weg_paden.setdefault(soort, []).append(pad(stuk))
    for laag in (0, 1):
        for soort in soorten:
            if weg_paden.get(soort):
                s.append(f'<g fill="none" stroke="{ZILVER if laag == 0 else WIT}" stroke-width="{breed[soort][laag]}" '
                         'stroke-linecap="round" stroke-linejoin="round">'
                         + "".join(f'<path d="{p}"/>' for p in weg_paden[soort]) + "</g>")

    # De route: witte rand, Koningsblauwe lijn
    rpts = " ".join(pad(stuk) for stuk in knip_lijn(vereenvoudig([xy(*p) for p in lijn], 1.2)))
    s.append(f'<path d="{rpts}" fill="none" stroke="{WIT}" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<path d="{rpts}" fill="none" stroke="{KONINGSBLAUW}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')

    # Plaatsnamen, weg van de spelden
    mx, my = xy(MLAT, MLON)
    px, py = xy(lat, lon)
    bezet = [(mx, my), (px, py)]
    for naam, soort, la, lo in sorted(plaatsnamen, key=lambda r: {"city": 0, "town": 1}.get(r[1], 2)):
        if soort == "village" and not detail:
            continue
        if naam in (label, woonplaats) or naam in DEN_HAAG:
            continue
        x, y = xy(la, lo)
        if not (80 < x < BR - 80 and 40 < y < HO - 30) or any(math.hypot(x - bx, y - by) < 150 for bx, by in bezet):
            continue
        bezet.append((x, y))
        s.append(tekst(x, y, naam, 22 if soort != "village" else 19, 600, LEISTEEN, WIT, ' opacity=".85"'))
    # Den Haag: op het plaatsknooppunt als dat in beeld is, anders midden in het zichtbare deel van de gemeente
    kandidaten = [xy(la, lo) for naam, soort, la, lo in plaatsnamen if naam in DEN_HAAG and soort == "city"]
    if haag_pts:
        kandidaten.append(zwaartepunt(haag_pts))
    for x, y in kandidaten:
        if 110 < x < BR - 110 and 50 < y < HO - 40 and all(math.hypot(x - bx, y - by) > 160 for bx, by in bezet):
            s.append(tekst(x, y, "Den Haag", 28, 700, DIEPBLAUW, WIT, ' opacity=".75"'))
            break

    # Spelden en namen
    s += [f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="44" fill="{KONINGSBLAUW}" opacity=".12"/>',
          speld_de_reus(mx, my), tekst(mx, my + 50, "De Reus", 28, 700, DIEPBLAUW, WIT),
          f'<circle cx="{px:.0f}" cy="{py:.0f}" r="44" fill="{DIEPBLAUW}" opacity=".10"/>',
          speld_plaats(px, py), tekst(px, py + 50, label, 30, 700, DIEPBLAUW, WIT),
          "</svg>"]
    uit = "\n".join(s)
    doel = ROOT / "img" / f"kaart-{slug}.svg"
    doel.write_bytes(uit.encode("utf-8"))
    print(f"{doel.name:34} {len(uit) // 1024:4} kB | beeld {beeld.km:4.1f} km breed | route {km:.1f} km, {minuten:.0f} min")


if __name__ == "__main__":
    kies = sys.argv[1:]
    bron = laad()
    for rij in PLAATSEN:
        if not kies or rij[0] in kies:
            kaart(*rij, bron)
