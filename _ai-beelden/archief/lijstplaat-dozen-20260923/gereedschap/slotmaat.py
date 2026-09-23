#!/usr/bin/env python3
"""Wat de belettering op de doos werkelijk wordt zodra de plaat hem toont.

De keten: het gegenereerde beeld (2752 breed) gaat als 720x405 naar img/, de plaat snijdt
daar met object-fit cover een vak van 535.3/509.8 uit op object-position 25% (425 bronpixels
breed), en toont dat op ten hoogste 240 css-pixels. Dit script loopt die keten echt af in
plaats van hem uit te rekenen, en schrijft de uitkomst op ware grootte weg.
"""
import pathlib
import sys

import numpy as np
from PIL import Image, ImageDraw

HIER = pathlib.Path(__file__).resolve().parent
EXPORT, VERHOUDING, POSITIE, PLAAT = 720, 535.3 / 509.8, 0.25, 240
HUIS = [(50, 1.5), (59.9, 10.4), (59.9, 0), (66.7, 0), (66.7, 16.5), (100, 46.3),
        (85.5, 46.3), (85.5, 100), (14.5, 100), (14.5, 46.3), (0, 46.3)]


def keten(bron, breedte=PLAAT):
    """Van bronbeeld naar het huisje zoals de plaat het toont."""
    im = Image.open(bron).convert("RGB")
    im = im.resize((EXPORT, round(EXPORT * im.height / im.width)), Image.LANCZOS)
    vak_b = im.height * VERHOUDING
    x = (im.width - vak_b) * POSITIE
    im = im.crop((round(x), 0, round(x + vak_b), im.height))
    return im.resize((breedte, round(breedte / VERHOUDING)), Image.LANCZOS)


def geknipt(im):
    pts = [(a / 100 * im.width, b / 100 * im.height) for a, b in HUIS]
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    doek = Image.new("RGB", im.size, (239, 240, 244))
    doek.paste(im, (0, 0), m)
    return doek


def wcag(a, b):
    hoog, laag = max(a, b), min(a, b)
    return (hoog + 0.05) / (laag + 0.05)


def relatief(rgb):
    c = np.asarray(rgb, float) / 255.0
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722


bron = sys.argv[1] if len(sys.argv) > 1 else "versie-2-r2.png"
schoon = sys.argv[2] if len(sys.argv) > 2 else "versie-2-r2bron.png"

# het merkvlak in bronpixels vinden door het met en zonder belettering te vergelijken
a = np.asarray(Image.open(bron).convert("RGB"), float)
b = np.asarray(Image.open(schoon).convert("RGB"), float)
verschil = np.abs(a - b).max(2) > 18
ys, xs = np.nonzero(verschil)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
breed_bron = x1 - x0 + 1
print("belettering in de bron: %d x %d px, vak (%d,%d)-(%d,%d)"
      % (breed_bron, y1 - y0 + 1, x0, y0, x1, y1))

f = (EXPORT / a.shape[1]) * (PLAAT / (Image.open(bron).height * EXPORT / Image.open(bron).width * VERHOUDING))
print("bronpixel -> schermpixel: %.4f" % f)
print("  logo met naam:  %.1f px breed op het scherm   (brandbook wil 100)" % (breed_bron * f))
# de cijfers zijn de onderste 190/737 van het paneel
print("  cijferhoogte:   %.1f px" % (190 / 737 * (y1 - y0 + 1) * f))

for maat, naam in ((PLAAT, "de plaat op zijn breedst, 240 px"),
                   (176, "de plaat op 1000 px venster, 13rem"),
                   (144, "de plaat op een telefoon, 9rem")):
    im = geknipt(keten(bron, maat))
    im.resize((im.width * 4, im.height * 4), Image.NEAREST).save(
        HIER / "_controle" / ("slotmaat-%d.png" % maat))
    print("  %-36s huisje %dx%d px" % (naam, im.width, im.height))

# contrast van de cijfers tegen het karton, op de maat van de plaat
klein = keten(bron, PLAAT)
groot = keten(bron, PLAAT * 6)          # zelfde uitsnede, groot genoeg om het vak te vinden
arr = np.asarray(klein.convert("RGB"), float)
L = relatief(arr)
# het cijfervak: de onderste helft van de belettering, geschat op het huisje
vak = arr[int(klein.height * 0.62):int(klein.height * 0.78), int(klein.width * 0.18):int(klein.width * 0.72)]
Lv = relatief(vak)
inkt, karton = np.percentile(Lv, 6), np.percentile(Lv, 92)
print("  cijfers tegen karton op 240 px: inkt %.3f  karton %.3f  contrast %.1f:1"
      % (inkt, karton, wcag(karton, inkt)))
