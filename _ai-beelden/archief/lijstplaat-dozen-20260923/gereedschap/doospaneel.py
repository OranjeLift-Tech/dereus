#!/usr/bin/env python3
"""Het beletteringspaneel voor de verhuisdoos: logo, naam en nummer op de voorkant.

Zelfde opbouw als het truckpaneel van ronde 1 (logo boven, nummer eronder), maar compacter,
want een doosvlak is minder hoog dan een wagenflank. De naam wordt nooit opnieuw gezet: die
zit als outline in het logobestand. Alleen het nummer is echte tekst, Archivo ExtraBold.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

HIER = pathlib.Path(__file__).resolve().parent
WORTEL = HIER.parents[2]
LOGO = WORTEL / "brandbook/assets/logo/dereus-logo-horizontaal.png"
FONT = WORTEL / "brandbook/assets/mockups/_bron/fonts/Archivo-VF.ttf"
BLAUW = (23, 70, 162, 255)
NUMMER = "085 000 5647"
BREED, SPATIE, DEEL = 2048, 16, 0.94

logo = Image.open(LOGO).convert("RGBA")
logo = logo.resize((BREED, round(logo.height * BREED / logo.width)), Image.LANCZOS)

f = ImageFont.truetype(str(FONT), 300)
f.set_variation_by_name("ExtraBold")
breed = lambda g: sum(g.getlength(t) for t in NUMMER) + SPATIE * (len(NUMMER) - 1)
f = ImageFont.truetype(str(FONT), round(300 * BREED * DEEL / breed(f)))
f.set_variation_by_name("ExtraBold")
vak = f.getbbox(NUMMER)
nb, nh = breed(f), vak[3] - vak[1]

gat = round(logo.height * 0.28)
paneel = Image.new("RGBA", (BREED, logo.height + gat + nh), (0, 0, 0, 0))
paneel.alpha_composite(logo, (0, 0))
d = ImageDraw.Draw(paneel)
x, y = (BREED - nb) / 2, logo.height + gat - vak[1]
for teken in NUMMER:
    d.text((x, y), teken, font=f, fill=BLAUW)
    x += f.getlength(teken) + SPATIE

uit = HIER / "doos-paneel.png"
paneel.save(uit)
print("%s  %dx%d   logo %d hoog, nummer %.0fx%d, cijferhoogte %d van %d paneelhoogte"
      % (uit.name, paneel.width, paneel.height, logo.height, nb, nh, nh, paneel.height))
