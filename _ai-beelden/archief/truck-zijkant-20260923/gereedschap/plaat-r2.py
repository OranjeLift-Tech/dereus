#!/usr/bin/env python3
"""Zet de twee maten van ronde 2 naast elkaar voor de reviewpagina.

Twee platen:
  versie-5-r2.png      A boven B, hele beelden, om de compositie te beoordelen
  versie-5-r2crop.png  ronde 1, A en B naast elkaar, hetzelfde stuk flank op 3x,
                       zodat de maten eerlijk te vergelijken zijn en de tekst leesbaar is
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

HIER = pathlib.Path(__file__).resolve().parent
FONT = HIER.parents[2] / "brandbook/assets/mockups/_bron/fonts/Archivo-VF.ttf"
VLAK = (1440, 160, 2290, 1140)      # het beletteringsvlak plus wat marge, in bronpixels
SCHAAL = 3
INKT, GROND = (18, 23, 38), (255, 255, 255)


def font(maat, gewicht="SemiBold"):
    f = ImageFont.truetype(str(FONT), maat)
    f.set_variation_by_name(gewicht)
    return f


def met_strook(im, tekst, maat=44):
    """Het beeld met een witte strook erboven waar het label in staat."""
    f = font(maat)
    hoog = maat + 26
    uit = Image.new("RGB", (im.width, im.height + hoog), GROND)
    d = ImageDraw.Draw(uit)
    d.text((14, (hoog - maat) / 2 - 6), tekst, font=f, fill=INKT)
    uit.paste(im.convert("RGB"), (0, hoog))
    return uit


def onder_elkaar(platen, gat=18):
    b = max(p.width for p in platen)
    h = sum(p.height for p in platen) + gat * (len(platen) - 1)
    uit = Image.new("RGB", (b, h), GROND)
    y = 0
    for p in platen:
        uit.paste(p, (0, y))
        y += p.height + gat
    return uit


def naast_elkaar(platen, gat=24):
    h = max(p.height for p in platen)
    b = sum(p.width for p in platen) + gat * (len(platen) - 1)
    uit = Image.new("RGB", (b, h), GROND)
    x = 0
    for p in platen:
        uit.paste(p, (x, 0))
        x += p.width + gat
    return uit


# 1. de hele beelden, A boven B
vol = [met_strook(Image.open(HIER / f"versie-5-{k}.png").resize((1600, 1073), Image.LANCZOS),
                  t, 40)
       for k, t in (("A", "A   belettering op 82% van de flank   nummer 614 px breed"),
                    ("B", "B   belettering op 94% van de flank   nummer 703 px breed"))]
onder_elkaar(vol).save(HIER / "versie-5-r2.png")

# 2. hetzelfde stuk flank uit drie bestanden, op 3x
snee = []
for bestand, label in (("versie-5-merk.png", "RONDE 1   nummer 449 px"),
                       ("versie-5-A.png", "A   nummer 614 px"),
                       ("versie-5-B.png", "B   nummer 703 px")):
    c = Image.open(HIER / bestand).crop(VLAK)
    c = c.resize((c.width * SCHAAL, c.height * SCHAAL), Image.LANCZOS)
    snee.append(met_strook(c, label, 72))
naast_elkaar(snee).save(HIER / "versie-5-r2crop.png")

for n in ("versie-5-r2.png", "versie-5-r2crop.png"):
    print(n, Image.open(HIER / n).size)
