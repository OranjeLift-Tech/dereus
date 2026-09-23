#!/usr/bin/env python3
"""Bouwt het beletteringspaneel dat op de blanke flank van elke wagen komt.

Eén paneel voor alle vijf de versies: de keuze gaat over de wagen, niet over de belettering.

Inhoud, van boven naar beneden:
  1. het echte horizontale logo uit brandbook/assets/logo (armen, huis, VERHUISBEDRIJF DE REUS)
  2. het telefoonnummer 085 000 5647

De naam wordt NOOIT opnieuw gezet: die zit als outline in het logobestand (brandbook README:
"Zet de naam nooit zelf opnieuw in een lettertype"). Alleen het nummer is echte tekst, in
Archivo ExtraBold, dezelfde familie als het woordmerk.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

WORTEL = pathlib.Path(__file__).resolve().parents[3]
LOGO = WORTEL / "brandbook/assets/logo/dereus-logo-horizontaal.png"
FONT = WORTEL / "brandbook/assets/mockups/_bron/fonts/Archivo-VF.ttf"
BLAUW = (23, 70, 162, 255)          # koningsblauw #1746A2
NUMMER = "085 000 5647"

logo = Image.open(LOGO).convert("RGBA")
breed = 2048
logo = logo.resize((breed, round(logo.height * breed / logo.width)), Image.LANCZOS)

font = ImageFont.truetype(str(FONT), 300)
font.set_variation_by_name("ExtraBold")
spatie = 14                          # iets uit elkaar: op een flank leest dat van verder weg

def nummerbreedte(f):
    return sum(f.getlength(t) for t in NUMMER) + spatie * (len(NUMMER) - 1)

# het nummer op 78 procent van de logobreedte
doel = breed * 0.78
maat = round(300 * doel / nummerbreedte(font))
font = ImageFont.truetype(str(FONT), maat)
font.set_variation_by_name("ExtraBold")
hoog = font.getbbox(NUMMER)
nb, nh = nummerbreedte(font), hoog[3] - hoog[1]

gat = round(logo.height * 0.42)
paneel = Image.new("RGBA", (breed, logo.height + gat + nh), (0, 0, 0, 0))
paneel.alpha_composite(logo, (0, 0))

d = ImageDraw.Draw(paneel)
x, y = (breed - nb) / 2, logo.height + gat - hoog[1]
for teken in NUMMER:                 # teken voor teken, anders werkt de letterspatiering niet
    d.text((x, y), teken, font=font, fill=BLAUW)
    x += font.getlength(teken) + spatie

uit = pathlib.Path(__file__).with_name("zijkant-paneel.png")
paneel.save(uit)
print(f"{uit.name}  {paneel.width}x{paneel.height}  verhouding {paneel.width/paneel.height:.2f}:1")
