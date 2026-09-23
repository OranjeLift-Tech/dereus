#!/usr/bin/env python3
"""Het beletteringspaneel voor ronde 2: nummer onderaan en groter.

Verschil met ronde 1 (zijkantpaneel.py):
  - het paneel is bijna zo hoog als de flank zelf, met het logo bovenaan en het nummer
    helemaal onderaan, in plaats van beide dicht op elkaar in het midden
  - het nummer is 94 procent van de logobreedte in plaats van 78

De naam wordt nog steeds NOOIT opnieuw gezet: die zit als outline in het logobestand.
Alleen het nummer is echte tekst, Archivo ExtraBold in koningsblauw.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

WORTEL = pathlib.Path(__file__).resolve().parents[3]
LOGO = WORTEL / "brandbook/assets/logo/dereus-logo-horizontaal.png"
FONT = WORTEL / "brandbook/assets/mockups/_bron/fonts/Archivo-VF.ttf"
BLAUW = (23, 70, 162, 255)
NUMMER = "085 000 5647"
HOOG = 1700                          # totale paneelhoogte; bepaalt hoe laag het nummer komt
DEEL = 0.94                          # breedte van het nummer als deel van de logobreedte

logo = Image.open(LOGO).convert("RGBA")
breed = 2048
logo = logo.resize((breed, round(logo.height * breed / logo.width)), Image.LANCZOS)

spatie = 16

def zet(maat):
    f = ImageFont.truetype(str(FONT), maat)
    f.set_variation_by_name("ExtraBold")
    return f

def nummerbreedte(f):
    return sum(f.getlength(t) for t in NUMMER) + spatie * (len(NUMMER) - 1)

proef = zet(300)
maat = round(300 * breed * DEEL / nummerbreedte(proef))
font = zet(maat)
vak = font.getbbox(NUMMER)
nb, nh = nummerbreedte(font), vak[3] - vak[1]

paneel = Image.new("RGBA", (breed, HOOG), (0, 0, 0, 0))
paneel.alpha_composite(logo, (0, 0))

d = ImageDraw.Draw(paneel)
x, y = (breed - nb) / 2, HOOG - nh - vak[1]      # grondlijn op de onderrand van het paneel
for teken in NUMMER:
    d.text((x, y), teken, font=font, fill=BLAUW)
    x += font.getlength(teken) + spatie

uit = pathlib.Path(__file__).with_name("zijkant-paneel-r2.png")
paneel.save(uit)
print(f"{uit.name}  {paneel.width}x{paneel.height}  logo 0-{logo.height}, "
      f"nummer {nb:.0f}x{nh} op y={y + vak[1]:.0f}, gat {HOOG - logo.height - nh:.0f} px")
