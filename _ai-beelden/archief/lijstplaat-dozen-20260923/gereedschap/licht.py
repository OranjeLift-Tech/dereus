#!/usr/bin/env python3
"""Meet het licht op elk doosvlak apart en kleurt de belettering daarnaar.

merk-op-doos.py neemt het VERLOOP van een vlak al over: het vermenigvuldigt het merk met de
luminantiekaart van het karton eronder. Wat het niet doet is de KLEUR van het licht. In deze
gang valt daglicht door de deur op kier: de twee dozen staan in een ander licht, de ene warmer
dan de andere. Zonder correctie krijgen ze allebei dezelfde koele inkt en ligt de belettering
er als een sticker op.

Dit script trekt elk vlak recht, meet mean RGB, het verloop en de kleurzweem, en schrijft per
vlak een paneel waarvan de inkt met die zweem vermenigvuldigd is.
"""
import importlib.util
import pathlib

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HIER = pathlib.Path(__file__).resolve().parent
WORTEL = HIER.parents[2]
spec = importlib.util.spec_from_file_location(
    "merkopdoos", WORTEL / "_ai-beelden/gereedschap/merk-op-doos.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

BRON = HIER / "versie-2-r2bron.png"
LOGO = WORTEL / "brandbook/assets/logo/dereus-logo-horizontaal.png"
MERK = WORTEL / "brandbook/assets/logo/dereus-beeldmerk.png"
FONT = WORTEL / "brandbook/assets/mockups/_bron/fonts/Archivo-VF.ttf"
BLAUW = np.array([23, 70, 162], float)
NUMMER = "085 000 5647"

VLAKKEN = {
    "voorste doos": np.array([[475, 754], [1493, 746], [1493, 1435], [475, 1399]], float),
    "achterste doos": np.array([[505, 155], [1240, 45], [1240, 725], [505, 700]], float),
}


def rechttrekken(beeld, hoeken, n=400):
    H = mod.homografie(hoeken)
    vv, uu = np.mgrid[0:n, 0:n].astype(float)
    u, v = (uu + .5) / n, (vv + .5) / n
    w = H[2, 0] * u + H[2, 1] * v + H[2, 2]
    x = (H[0, 0] * u + H[0, 1] * v + H[0, 2]) / w
    y = (H[1, 0] * u + H[1, 1] * v + H[1, 2]) / w
    return np.stack([ndimage.map_coordinates(beeld[..., k], [y, x], order=1, mode="nearest")
                     for k in range(3)], -1)


def meet(naam, hoeken, beeld):
    vlak = rechttrekken(beeld, hoeken)
    lum = vlak @ mod.LUM
    mid = vlak.reshape(-1, 3).mean(0)
    # zweem: de kleur van het licht, op luminantie 1 genormeerd
    zweem = mid / (mid @ mod.LUM)
    links, rechts = lum[:, :80].mean(), lum[:, -80:].mean()
    boven, onder = lum[:80].mean(), lum[-80:].mean()
    b, h = mod.vlakmaten(hoeken)
    print("%s  vlak %.0fx%.0f px" % (naam, b, h))
    print("   gemiddelde kleur  R%.0f G%.0f B%.0f   luminantie %.3f"
          % (mid[0]*255, mid[1]*255, mid[2]*255, lum.mean()))
    print("   kleurzweem        R%.3f G%.3f B%.3f  (1.000 = neutraal)" % tuple(zweem))
    print("   verloop overdwars links %.3f -> rechts %.3f  (%+.1f%%)"
          % (links, rechts, (rechts/links - 1) * 100))
    print("   verloop omlaag    boven %.3f -> onder  %.3f  (%+.1f%%)"
          % (boven, onder, (onder/boven - 1) * 100))
    print("   donkerste 2%% %.3f   lichtste 98%% %.3f" % (np.percentile(lum, 2), np.percentile(lum, 98)))
    return zweem, b, h, float(lum.mean())


def nummerfont(breed, deel=0.94, spatie=16):
    f = ImageFont.truetype(str(FONT), 300)
    f.set_variation_by_name("ExtraBold")
    br = lambda g: sum(g.getlength(t) for t in NUMMER) + spatie * (len(NUMMER) - 1)
    f = ImageFont.truetype(str(FONT), round(300 * breed * deel / br(f)))
    f.set_variation_by_name("ExtraBold")
    return f, br(f), spatie


def paneel_vol(hoog, breed=2048):
    """Logo bovenaan, nummer met zijn grondlijn op de onderrand: het nummer zo laag mogelijk."""
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.resize((breed, round(logo.height * breed / logo.width)), Image.LANCZOS)
    f, nb, spatie = nummerfont(breed)
    vak = f.getbbox(NUMMER)
    nh = vak[3] - vak[1]
    p = Image.new("RGBA", (breed, hoog), (0, 0, 0, 0))
    p.alpha_composite(logo, (0, 0))
    d = ImageDraw.Draw(p)
    x, y = (breed - nb) / 2, hoog - nh - vak[1]
    for teken in NUMMER:
        d.text((x, y), teken, font=f, fill=tuple(BLAUW.astype(int)) + (255,))
        x += f.getlength(teken) + spatie
    return p, logo.height, nh


def paneel_merk():
    return Image.open(MERK).convert("RGBA")


def tint(p, winst):
    """De inkt in het licht van dit vlak zetten."""
    a = np.asarray(p, float)
    rgb = a[..., :3] / 255.0
    a[..., :3] = np.clip(rgb * winst, 0, 1) * 255.0
    return Image.fromarray(a.astype(np.uint8))


def lichtwinst(gemeten):
    """De zweem die ik meet is die van het KARTON, niet van de lamp.

    Beide dozen zijn hetzelfde kraft, dus wat de twee metingen onderscheidt is het licht.
    Deel elke meting door het gemiddelde van de twee en je houdt over hoe deze doos verlicht
    is ten opzichte van de andere: kleur EN helderheid. Dat is wat de inkt moet overnemen.
    merk-op-doos ijkt zijn schaduwkaart op de mediaan onder het merk, dus het neemt alleen
    het verloop binnen een vlak mee en niet het verschil tussen de twee dozen; die helft
    komt hiervandaan.
    """
    namen = list(gemeten)
    zwemen = np.array([gemeten[n][0] for n in namen])
    lums = np.array([gemeten[n][3] for n in namen])
    ref_z = np.exp(np.log(zwemen).mean(0))
    ref_l = lums.mean()
    uit = {}
    for i, n in enumerate(namen):
        kleur = zwemen[i] / ref_z
        belichting = lums[i] / ref_l
        uit[n] = (kleur, belichting, kleur * belichting)
        print("%s: kleur t.o.v. de andere doos R%.3f G%.3f B%.3f, belichting %.3f"
              % (n, kleur[0], kleur[1], kleur[2], belichting))
        print("   inktwinst R%.3f G%.3f B%.3f" % tuple(kleur * belichting))
    return uit


if __name__ == "__main__":
    beeld = np.asarray(Image.open(BRON).convert("RGB"), float) / 255.0
    gemeten = {}
    for naam, hoeken in VLAKKEN.items():
        gemeten[naam] = meet(naam, hoeken, beeld)
        print()

    print("HET LICHT VAN DE EEN TEN OPZICHTE VAN DE ANDER")
    winst = lichtwinst(gemeten)
    print()

    p, logo_h, nh = paneel_vol(1260)
    tint(p, winst["voorste doos"][2]).save(HIER / "paneel-voor.png")
    print("paneel-voor.png   2048x1260, logo %d hoog bovenaan, cijfers %d hoog op de onderrand,"
          " gat %d px" % (logo_h, nh, 1260 - logo_h - nh))
    print("   inkt vermenigvuldigd met R%.3f G%.3f B%.3f" % tuple(winst["voorste doos"][2]))

    tint(paneel_merk(), winst["achterste doos"][2]).save(HIER / "paneel-achter.png")
    print("paneel-achter.png  alleen het beeldmerk, inkt maal R%.3f G%.3f B%.3f"
          % tuple(winst["achterste doos"][2]))
