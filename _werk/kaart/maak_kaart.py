"""Statische kaart voor de contactpagina van Verhuisbedrijf De Reus.

Eigen SVG op OpenStreetMap-data (ODbL), naar het voorbeeld van De Kievit (_werk/paginabeeld/maak_kaart.py).
Geen Google-kaart en geen embed: de kaart laadt niets van buiten, staat in de huisstijl en is meteen scherp.
Attributie (ODbL) staat als zichtbaar bijschrift onder de kaart, in het blok kaart: "Kaartgegevens © OpenStreetMap-bijdragers".

Draaien: python _werk/kaart/maak_kaart.py
De OSM-data (Overpass, "out geom", ongeveer 3 MB) wordt opgehaald naar de tijdelijke map van het systeem
en niet in de repo bewaard. Uitvoer: img/kaart-den-haag.svg.
Locatie volgens PDOK Locatieserver: 52.0596297, 4.29913794 (buurt Groente- en Fruitmarkt).
Kleuren alleen uit brandbook/tokens.css (Mist, Zilvergrijs, blauw 50 tot 200, Koningsblauw, Diepblauw, Goudgeel, Leisteen).
"""
import json
import math
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UIT = ROOT / "img" / "kaart-den-haag.svg"
BRON = Path(tempfile.gettempdir()) / "dereus-osm-den-haag.json"
MLAT, MLON = 52.0596297, 4.29913794
S, W, N, E = 52.0476, 4.2721, 52.0716, 4.3261
VRAAG = (f"[out:json][timeout:60];("
         f'way["highway"~"^(motorway|trunk|primary|secondary|tertiary)$"]({S},{W},{N},{E});'
         f'way["landuse"~"^(residential|industrial|retail|commercial)$"]({S},{W},{N},{E});'
         f'way["leisure"="park"]({S},{W},{N},{E});'
         f'way["landuse"~"^(forest|recreation_ground|grass)$"]({S},{W},{N},{E});'
         f'way["natural"="water"]({S},{W},{N},{E});'
         f'way["waterway"~"^(canal|river)$"]({S},{W},{N},{E});'
         f'way["railway"="rail"]({S},{W},{N},{E});'
         f'node["place"~"^(suburb|quarter|neighbourhood)$"]({S},{W},{N},{E});'
         f");out geom;")

if not BRON.exists():
    data = urllib.parse.urlencode({"data": VRAAG}).encode()
    verzoek = urllib.request.Request("https://overpass-api.de/api/interpreter", data=data,
                                     headers={"User-Agent": "dereus-contactkaart/1.0"})
    BRON.write_bytes(urllib.request.urlopen(verzoek, timeout=120).read())
BR, HO = 1400, 933

merc = lambda lat: math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
MS, MN = merc(S), merc(N)


def xy(lat, lon):
    return ((lon - W) / (E - W) * BR, (MN - merc(lat)) / (MN - MS) * HO)


def vereenvoudig(pts, tol=1.8):
    uit = [pts[0]]
    for p in pts[1:-1]:
        if abs(p[0] - uit[-1][0]) + abs(p[1] - uit[-1][1]) > tol:
            uit.append(p)
    if len(pts) > 1:
        uit.append(pts[-1])
    return uit


def oppervlak(pts):
    return abs(sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts)))) / 2


def pad(pts, dicht=False):
    return " ".join(f"{'M' if i == 0 else 'L'}{x:.0f},{y:.0f}" for i, (x, y) in enumerate(pts)) + (" Z" if dicht else "")


d = json.loads(BRON.read_text(encoding="utf-8"))
bebouwd, groen, water, kanaal, spoor, wegen, namen, parken = [], [], [], [], [], [], [], []
for e in d["elements"]:
    t = e.get("tags", {})
    if e["type"] == "node":
        if t.get("place") == "quarter" and t.get("name"):
            namen.append((t["name"], e["lat"], e["lon"]))
        continue
    g = e.get("geometry")
    if not g or len(g) < 2:
        continue
    pts = vereenvoudig([xy(p["lat"], p["lon"]) for p in g])
    lu, hw = t.get("landuse"), t.get("highway")
    if lu in ("residential", "industrial", "retail", "commercial"):
        if oppervlak(pts) > 700:
            bebouwd.append(pad(pts, True))
    elif lu in ("forest", "grass", "recreation_ground") or t.get("leisure") == "park":
        opp = oppervlak(pts)
        if opp > 1500:
            groen.append(pad(pts, True))
        if t.get("leisure") == "park" and t.get("name") and opp > 60000:
            cx = sum(x for x, _ in pts) / len(pts); cy = sum(y for _, y in pts) / len(pts)
            parken.append((t["name"], cx, cy))
    elif t.get("natural") == "water":
        if oppervlak(pts) > 250:
            water.append(pad(pts, True))
    elif t.get("waterway") in ("canal", "river"):
        kanaal.append(pad(pts))
    elif t.get("railway") == "rail":
        spoor.append(pad(pts))
    elif hw:
        wegen.append((hw, pad(pts)))

# tokens.css: Mist #F6F7F9, Zilvergrijs #D3D7DE, blauw 50 #F3F7FE, blauw 100 #E6EFFF, blauw 200 #CDDFFF,
# Koningsblauw #1746A2, Diepblauw #0B2352, Goudgeel #FFCC33, Leisteen #5E6675, Wit #FFFFFF
MIST, ZILVER, B50, B100, B200 = "#F6F7F9", "#D3D7DE", "#F3F7FE", "#E6EFFF", "#CDDFFF"
KONINGSBLAUW, DIEPBLAUW, GOUD, LEISTEEN, WIT = "#1746A2", "#0B2352", "#FFCC33", "#5E6675", "#FFFFFF"
BREED = {"motorway": (13, 8.5), "trunk": (12, 7.5), "primary": (10, 6.4), "secondary": (8, 5), "tertiary": (5.2, 3.2)}
VOLG = ["tertiary", "secondary", "primary", "trunk", "motorway"]
HUIS = ("M267.6 7.8L320.9 53.2V0H356.8V83.9L535.3 236.2H457.6V509.8H326.2V384.1H209.1V509.8H77.7V236.2H0Z")

s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BR} {HO}" width="{BR}" height="{HO}" role="img" '
     'aria-label="Kaart van Den Haag met het hoofdkantoor van Verhuisbedrijf De Reus aan de Lau Mazirellaan 336, '
     'in de wijk Groente- en Fruitmarkt">',
     '<defs><filter id="k-schaduw" x="-40%" y="-40%" width="180%" height="180%">'
     f'<feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="{DIEPBLAUW}" flood-opacity=".35"/></filter></defs>',
     f'<rect width="{BR}" height="{HO}" fill="{MIST}"/>']
if bebouwd:
    s.append(f'<g fill="{ZILVER}" opacity=".42">' + "".join(f'<path d="{p}"/>' for p in bebouwd) + "</g>")
if groen:
    s.append(f'<g fill="{WIT}">' + "".join(f'<path d="{p}"/>' for p in groen) + "</g>")   # open ruimte: wit, zodat het niet op water lijkt
if water:
    s.append(f'<g fill="{B200}">' + "".join(f'<path d="{p}"/>' for p in water) + "</g>")
if kanaal:
    s.append(f'<g fill="none" stroke="{B200}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">'
             + "".join(f'<path d="{p}"/>' for p in kanaal) + "</g>")
if spoor:
    s.append(f'<g fill="none" stroke="{LEISTEEN}" stroke-width="2" stroke-dasharray="9 7" opacity=".45">'
             + "".join(f'<path d="{p}"/>' for p in spoor) + "</g>")
for laag in (0, 1):
    for soort in VOLG:
        paden = [p for st, p in wegen if st == soort]
        if paden:
            s.append(f'<g fill="none" stroke="{ZILVER if laag == 0 else WIT}" stroke-width="{BREED[soort][laag]}" '
                     'stroke-linecap="round" stroke-linejoin="round">' + "".join(f'<path d="{p}"/>' for p in paden) + "</g>")

mx, my = xy(MLAT, MLON)
# De kaart staat in het blok met object-fit: cover. Op 1440 is het venster staand (ongeveer 0,8), op mobiel 1:1 met
# 190 % zoom: zichtbaar blijft steeds ongeveer x 330 tot 1070 en y 100 tot 830. Labels alleen als ze daar helemaal in passen.
VEILIG = (350, 120, 1050, 815)


def past(x, y, naam, grootte):
    half = len(naam) * grootte * .3
    return VEILIG[0] < x - half and x + half < VEILIG[2] and VEILIG[1] < y < VEILIG[3]


for naam, la, lo in namen:
    x, y = xy(la, lo)
    if not past(x, y, naam, 24) or math.hypot(x - mx, y - my) < 170 or naam == "Groente- en Fruitmarkt":
        continue
    s.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-family="Inter,Segoe UI,Arial,sans-serif" '
             f'font-weight="600" font-size="24" fill="{LEISTEEN}" stroke="{MIST}" stroke-width="6" paint-order="stroke" '
             f'opacity=".85">{naam}</text>')

for naam, x, y in parken:
    if math.hypot(x - mx, y - my) > 170 and past(x, y, naam, 22):
        s.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-family="Inter,Segoe UI,Arial,sans-serif" '
                 f'font-weight="600" font-style="normal" font-size="22" fill="{LEISTEEN}" stroke="{WIT}" stroke-width="6" '
                 f'paint-order="stroke" opacity=".8">{naam}</text>')

# Marker: Koningsblauwe speld met het gele huis uit het logo, zachte ring eromheen
schaal = 26 / 535.3
s += [f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="86" fill="{KONINGSBLAUW}" opacity=".08"/>',
      f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="50" fill="{KONINGSBLAUW}" opacity=".14"/>',
      f'<g transform="translate({mx:.0f},{my:.0f})" filter="url(#k-schaduw)">'
      f'<path d="M0,10 C0,10 -32,-24 -32,-46 A32,32 0 1 1 32,-46 C32,-24 0,10 0,10 Z" fill="{KONINGSBLAUW}" '
      f'stroke="{WIT}" stroke-width="5" stroke-linejoin="round"/>'
      f'<path d="{HUIS}" fill="{GOUD}" transform="translate({-13:.1f},{-58.5:.1f}) scale({schaal:.5f})"/></g>',
      f'<text x="{mx:.0f}" y="{my + 50:.0f}" text-anchor="middle" font-family="Inter,Segoe UI,Arial,sans-serif" '
      f'font-weight="700" font-size="28" fill="{DIEPBLAUW}" stroke="{WIT}" stroke-width="8" paint-order="stroke">De Reus</text>',
      "</svg>"]
uit = "\n".join(s)
UIT.write_bytes(uit.encode("utf-8"))
print(f"{UIT.name} {len(uit)//1024} kB | wegen {len(wegen)} groen {len(groen)} water {len(water)} kanaal {len(kanaal)} "
      f"bebouwd {len(bebouwd)} spoor {len(spoor)} namen {len(namen)} | marker {mx:.0f},{my:.0f}")
