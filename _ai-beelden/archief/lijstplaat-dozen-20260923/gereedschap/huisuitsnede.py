#!/usr/bin/env python3
"""Toont wat de plaat op /werkwijze/ werkelijk van een foto laat zien.

De foto gaat in de huisvorm uit het logo: object-fit cover in een vak van 535.3/509.8,
object-position 25% center, daarna geknipt met de clip-path uit css/blok/lijstplaat.css.
Zonder deze stap beoordeel je een 16:9-foto terwijl de bezoeker een bijna vierkant huisje ziet.

    python huisuitsnede.py versie-1.png versie-2.png ...   -> huisuitsnede.png
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

HIER = pathlib.Path(__file__).resolve().parent
FONT = HIER.parents[2] / "brandbook/assets/mockups/_bron/fonts/Archivo-VF.ttf"
VERHOUDING = 535.3 / 509.8
POSITIE = 0.25
GEEL, BLAUW, GROND = (255, 204, 51), (23, 70, 162), (239, 240, 244)
# de huisvorm uit de CSS, in procenten van het vak
HUIS = [(50, 1.5), (59.9, 10.4), (59.9, 0), (66.7, 0), (66.7, 16.5), (100, 46.3),
        (85.5, 46.3), (85.5, 100), (14.5, 100), (14.5, 46.3), (0, 46.3)]
MAAT = 560


def huisje(bron):
    im = Image.open(bron).convert("RGB")
    # cover: het vak vullen en de overmaat aan de zijkant weghalen op 25 procent
    vak_b = im.height * VERHOUDING
    if vak_b <= im.width:
        x = (im.width - vak_b) * POSITIE
        im = im.crop((round(x), 0, round(x + vak_b), im.height))
    else:
        vak_h = im.width / VERHOUDING
        y = (im.height - vak_h) / 2
        im = im.crop((0, round(y), im.width, round(y + vak_h)))
    im = im.resize((MAAT, round(MAAT / VERHOUDING)), Image.LANCZOS)

    punten = [(x / 100 * im.width, y / 100 * im.height) for x, y in HUIS]
    masker = Image.new("L", im.size, 0)
    ImageDraw.Draw(masker).polygon(punten, fill=255)
    # het goudgele huis er net iets omheen, zoals de ::before in de CSS (scale 1.06)
    doek = Image.new("RGB", (im.width + 40, im.height + 40), GROND)
    groot = [(x * 1.06 + 20 - im.width * 0.03, y * 1.06 + 20 - im.height * 0.03)
             for x, y in punten]
    ImageDraw.Draw(doek).polygon(groot, fill=GEEL)
    doek.paste(im, (20, 20), masker)
    return doek


def strook(im, tekst, maat=30):
    f = ImageFont.truetype(str(FONT), maat)
    f.set_variation_by_name("SemiBold")
    hoog = maat + 20
    uit = Image.new("RGB", (im.width, im.height + hoog), (255, 255, 255))
    d = ImageDraw.Draw(uit)
    d.text((10, (hoog - maat) / 2 - 5), tekst, font=f, fill=(18, 23, 38))
    uit.paste(im, (0, hoog))
    return uit


bronnen = sys.argv[1:] or sorted(str(p.name) for p in HIER.glob("versie-?.png"))
platen = [strook(huisje(HIER / b), b.replace(".png", "")) for b in bronnen]
b = sum(p.width for p in platen) + 16 * (len(platen) - 1)
blad = Image.new("RGB", (b, max(p.height for p in platen)), (255, 255, 255))
x = 0
for p in platen:
    blad.paste(p, (x, 0))
    x += p.width + 16
blad.save(HIER / "huisuitsnede.png")
print("huisuitsnede.png", blad.size, "uit", len(bronnen), "beelden")
