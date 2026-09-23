#!/usr/bin/env python3
"""Ronde 3: het logo verplaatst en de belettering zo versleten als de flank zelf.

Het nummer blijft waar variant B het had: onderaan, 94 procent van de flankbreedte.
Twee lezingen van "gecentreerd", allebei op dezelfde hoekpunten als ronde 2:

  C  het logo in het hart van de flank
  D  het logo in het hart van de ruimte boven het nummer

De sleet is niet verzonnen maar overgenomen van de flank zelf (meet-flank.py):
  - korrel 0.0085 per kanaal
  - donkere plekken tot -0.04 luminantie op schalen van 6 tot 30 px, twee keer zo diep
    als de lichte; waar de flank zelf een veeg heeft, verliest de folie daar dekking
  - een vuilband onderin: de onderste tiende van het vlak is 6,2 procent donkerder
  - horizontaal gestreept (|dy| > |dx|), dus de krassen lopen met de flank mee
"""
import argparse
import importlib.util
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HIER = pathlib.Path(__file__).resolve().parent
WORTEL = HIER.parents[2]
spec = importlib.util.spec_from_file_location(
    "merkopdoos", WORTEL / "_ai-beelden/gereedschap/merk-op-doos.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

HOEKEN = np.array([[1465, 186], [2262, 345], [2257, 1043], [1480, 1110]], float)
BREEDTE = 0.94
BRON = HIER / "versie-5.png"
LOGO = WORTEL / "brandbook/assets/logo/dereus-logo-horizontaal.png"
FONT = WORTEL / "brandbook/assets/mockups/_bron/fonts/Archivo-VF.ttf"
BLAUW = (23, 70, 162, 255)
NUMMER = "085 000 5647"
LW, LH = 2048, 1700
SPATIE, DEEL = 16, 0.94


def nummerfont():
    f = ImageFont.truetype(str(FONT), 300)
    f.set_variation_by_name("ExtraBold")
    breed = sum(f.getlength(t) for t in NUMMER) + SPATIE * (len(NUMMER) - 1)
    f = ImageFont.truetype(str(FONT), round(300 * LW * DEEL / breed))
    f.set_variation_by_name("ExtraBold")
    return f


def paneel(logo_y):
    """Het schone paneel: logo op hoogte logo_y, grondlijn van het nummer op de onderrand."""
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.resize((LW, round(logo.height * LW / logo.width)), Image.LANCZOS)
    f = nummerfont()
    nb = sum(f.getlength(t) for t in NUMMER) + SPATIE * (len(NUMMER) - 1)
    vak = f.getbbox(NUMMER)
    nh = vak[3] - vak[1]

    p = Image.new("RGBA", (LW, LH), (0, 0, 0, 0))
    p.alpha_composite(logo, (0, round(logo_y)))
    d = ImageDraw.Draw(p)
    x, y = (LW - nb) / 2, LH - nh - vak[1]
    for teken in NUMMER:
        d.text((x, y), teken, font=f, fill=BLAUW)
        x += f.getlength(teken) + SPATIE
    return p, logo.height, LH - nh


def plek():
    """Waar het paneel op het vlak ligt; dezelfde rekensom als merk-op-doos."""
    vb, vh = mod.vlakmaten(HOEKEN)
    bw = BREEDTE
    bh = bw * (LH / LW) * (vb / vh)
    return bw, bh, 0.5 - bw / 2, 0.5 - bh / 2


def afwijkingskaart():
    """Waar de flank zelf donkerder is dan zijn omgeving: vegen, vuil, krassen.

    De brede vervaging eruit, want dat is het licht dat over de flank valt en dat neemt
    merk-op-doos al mee in zijn schaduwkaart.
    """
    beeld = np.asarray(Image.open(BRON).convert("RGB"), float) / 255.0
    lum = beeld @ mod.LUM
    return lum - ndimage.gaussian_filter(lum, 40)


def sleet(p, afwijking, bw, bh, u0, v0, seed=11):
    """Minder dekking waar de flank gehavend is, plus het eigen verval van de folie."""
    H = mod.homografie(HOEKEN)
    yy, xx = np.mgrid[0:LH, 0:LW].astype(float)
    u = u0 + (xx + 0.5) / LW * bw
    v = v0 + (yy + 0.5) / LH * bh
    w = H[2, 0] * u + H[2, 1] * v + H[2, 2]
    bx = (H[0, 0] * u + H[0, 1] * v + H[0, 2]) / w
    by = (H[1, 0] * u + H[1, 1] * v + H[1, 2]) / w
    onder = ndimage.map_coordinates(afwijking, [by, bx], order=1, mode="nearest")

    rng = np.random.default_rng(seed)
    # 1. de havens van de flank zelf; alleen de donkere kant telt, tot -0.04
    uit_flank = np.clip(-onder / 0.04, 0, 1) * 0.30
    # 2. eigen verval van de folie, grof gevlekt, donkere kant twee keer zo diep als de
    #    lichte, in dezelfde verhouding als de flank (p1 -0.037 tegen p99 +0.018)
    ruw = rng.normal(0, 1, (LH // 8 + 2, LW // 8 + 2))
    vlek = ndimage.zoom(ndimage.gaussian_filter(ruw, 3), 8, order=1)[:LH, :LW]
    vlek = vlek / (np.abs(vlek).max() + 1e-9)
    eigen = np.clip(np.where(vlek < 0, vlek * 2.0, vlek), -1, 1) * 0.10
    # 3. krassen die met de flank mee lopen: horizontaal gestreept
    lijn = rng.normal(0, 1, (LH, LW // 40 + 2))
    lijn = ndimage.zoom(lijn, (1, 40), order=1)[:LH, :LW]
    kras = np.clip(-np.clip(ndimage.gaussian_filter(lijn, (0.7, 26)) * 9, -1, 1), 0, 1) * 0.14
    # 4. de vuilband onderin, omgerekend van vlak-v naar paneel-v
    start = (0.90 - v0) / bh
    band = np.clip(((yy / LH) - start) / max(1e-6, 1 - start), 0, 1) ** 1.5 * 0.12
    # 5. de rand van oude folie is niet meer scherp
    a = np.asarray(p, float)[..., 3] / 255.0
    rand = np.clip(ndimage.gaussian_filter(a, 2.2) - ndimage.gaussian_filter(a, 0.6), 0, 1)
    randsleet = rand * np.clip(rng.normal(0.5, 0.5, a.shape), 0, 1) * 0.55

    verlies = np.clip(0.05 + uit_flank + np.clip(eigen, 0, None) + kras + band + randsleet
                      - np.clip(-eigen, 0, None) * 0.3, 0, 0.62)
    uit = np.asarray(p, float).copy()
    uit[..., 3] = a * (1 - verlies) * 255.0
    # verbleekte folie verliest ook verzadiging: een tik richting zijn eigen grijswaarde
    rgb = uit[..., :3] / 255.0
    grijs = (rgb @ mod.LUM)[..., None]
    uit[..., :3] = (rgb + (grijs - rgb) * (verlies * 0.45)[..., None]) * 255.0
    return Image.fromarray(np.clip(uit, 0, 255).astype(np.uint8)), verlies, a


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--schoon", action="store_true",
                    help="ook het paneel zonder sleet wegschrijven, om te vergelijken")
    arg = ap.parse_args()

    bw, bh, u0, v0 = plek()
    vb, vh = mod.vlakmaten(HOEKEN)
    afwijking = afwijkingskaart()
    _, logo_h, nummer_top = paneel(0)
    nummer_v = v0 + (nummer_top / LH) * bh
    logo_v = (logo_h / LH) * bh

    print("vlak %.0fx%.0f px   paneel %.3f bij %.3f van het vlak   v van %.3f tot %.3f"
          % (vb, vh, bw, bh, v0, v0 + bh))
    print("nummer op vlak-v %.3f tot %.3f   logohoogte %.3f van het vlak"
          % (nummer_v, v0 + bh, logo_v))

    for naam, midden, wat in (("C", 0.50, "logo in het hart van de flank"),
                              ("D", None, "logo in het hart van de ruimte boven het nummer")):
        v_mid = midden if midden is not None else nummer_v / 2
        logo_y = ((v_mid - logo_v / 2) - v0) / bh * LH
        p, _, _ = paneel(logo_y)
        versleten, verlies, alfa = sleet(p, afwijking, bw, bh, u0, v0)
        pad = HIER / ("zijkant-paneel-%s.png" % naam)
        versleten.save(pad)
        if arg.schoon:
            p.save(HIER / ("zijkant-paneel-%s-schoon.png" % naam))

        ink = alfa > 0.5
        print("\n%s  %s" % (naam, wat))
        print("   logo op vlak-v %.3f tot %.3f (midden %.3f)"
              % (v_mid - logo_v / 2, v_mid + logo_v / 2, v_mid))
        print("   dekkingsverlies op de inkt: gemiddeld %.1f%%, p99 %.1f%%, hoogste %.1f%%"
              % (verlies[ink].mean() * 100, np.percentile(verlies[ink], 99) * 100,
                 verlies[ink].max() * 100))
        subprocess.run(
            [sys.executable, str(WORTEL / "_ai-beelden/gereedschap/merk-op-doos.py"),
             str(BRON), "--hoeken", " ".join("%d,%d" % tuple(q) for q in HOEKEN.astype(int)),
             "--logo", str(pad), "--breedte", str(BREEDTE),
             "--uit", str(HIER / ("versie-5-%s.png" % naam)),
             "--crop", str(HIER / ("versie-5-%scrop.png" % naam))],
            check=True, capture_output=True)
        print("   geschreven: versie-5-%s.png" % naam)


if __name__ == "__main__":
    main()
