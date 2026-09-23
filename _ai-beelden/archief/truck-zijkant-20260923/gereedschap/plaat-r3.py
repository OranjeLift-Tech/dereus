#!/usr/bin/env python3
"""De twee lezingen van "gecentreerd" naast elkaar voor de reviewpagina.

  versie-5-r3.png      C boven D, hele beelden
  versie-5-r3crop.png  B, C en D naast elkaar, hetzelfde stuk flank op 3x, zodat de
                       plek van het logo en de sleet te vergelijken zijn en het nummer
                       te lezen is
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

HIER = pathlib.Path(__file__).resolve().parent
FONT = HIER.parents[2] / "brandbook/assets/mockups/_bron/fonts/Archivo-VF.ttf"
VLAK = (1440, 160, 2290, 1140)
SCHAAL = 3
INKT, GROND = (18, 23, 38), (255, 255, 255)


def font(maat, gewicht="SemiBold"):
    f = ImageFont.truetype(str(FONT), maat)
    f.set_variation_by_name(gewicht)
    return f


def met_strook(im, tekst, maat):
    f = font(maat)
    hoog = maat + 26
    uit = Image.new("RGB", (im.width, im.height + hoog), GROND)
    d = ImageDraw.Draw(uit)
    d.text((14, (hoog - maat) / 2 - 6), tekst, font=f, fill=INKT)
    uit.paste(im.convert("RGB"), (0, hoog))
    return uit


def stapel(platen, gat, horizontaal):
    if horizontaal:
        b = sum(p.width for p in platen) + gat * (len(platen) - 1)
        h = max(p.height for p in platen)
    else:
        b = max(p.width for p in platen)
        h = sum(p.height for p in platen) + gat * (len(platen) - 1)
    uit = Image.new("RGB", (b, h), GROND)
    k = 0
    for p in platen:
        uit.paste(p, (k, 0) if horizontaal else (0, k))
        k += (p.width if horizontaal else p.height) + gat
    return uit


vol = [met_strook(Image.open(HIER / ("versie-5-%s.png" % k)).resize((1600, 1073), Image.LANCZOS),
                  t, 40)
       for k, t in (("C", "C   logo in het hart van de flank"),
                    ("D", "D   logo in het hart van de ruimte boven het nummer"))]
stapel(vol, 18, False).save(HIER / "versie-5-r3.png")

snee = []
for bestand, label in (("versie-5-B.png", "B UIT RONDE 2   logo bovenaan, geen sleet"),
                       ("versie-5-C.png", "C   logo in het hart van de flank, met sleet"),
                       ("versie-5-D.png", "D   logo boven het nummer gecentreerd, met sleet")):
    c = Image.open(HIER / bestand).crop(VLAK)
    c = c.resize((c.width * SCHAAL, c.height * SCHAAL), Image.LANCZOS)
    snee.append(met_strook(c, label, 72))
stapel(snee, 24, True).save(HIER / "versie-5-r3crop.png")

for n in ("versie-5-r3.png", "versie-5-r3crop.png"):
    print(n, Image.open(HIER / n).size)
