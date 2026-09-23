#!/usr/bin/env python3
"""Ronde 5: variant D, met de print op de achterste doos donkerder.

Ronde 3 en 4 ijkten de inkt per doos op het gemeten licht. De achterste doos vangt het
daglicht van de deur, dus die kreeg belichting 1,118 en daarmee lichtere, koelere inkt dan
de voorste (0,882). Dat is de meting; de gebruiker vraagt hem terug omlaag. Twee niveaus,
zodat hij kiest in plaats van dat ik gok:

  E  belichting 1,000 - de daglichtopslag eraf, de kleurzweem blijft
  F  belichting 0,882 - gelijk aan de voorste doos, dus even donkere inkt op beide

De voorste doos verandert niet. Het logo staat bij allebei waar variant D het had.
"""
import importlib.util
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image

HIER = pathlib.Path(__file__).resolve().parent
WORTEL = HIER.parents[2]


def laad(naam, bestand):
    spec = importlib.util.spec_from_file_location(naam, HIER / bestand)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


L = laad("licht", "licht.py")
R4 = laad("ronde4", "ronde4.py")

TOOL = WORTEL / "_ai-beelden/gereedschap/merk-op-doos.py"
BRON = HIER / "versie-2-r2bron.png"
NIVEAUS = {"E": 1.000, "F": 0.882}


def paneel_met_logo_op(y, winst):
    """Het paneel van ronde 4: logo op hoogte y, nummer op de onderrand, inkt getint."""
    p, _, nh = L.paneel_vol(R4.HOOG)
    leeg = Image.new("RGBA", (2048, R4.HOOG), (0, 0, 0, 0))
    logo = Image.open(L.LOGO).convert("RGBA")
    logo = logo.resize((2048, round(logo.height * 2048 / logo.width)), Image.LANCZOS)
    leeg.alpha_composite(logo, (0, round(y)))
    leeg.alpha_composite(p.crop((0, R4.HOOG - nh - 10, 2048, R4.HOOG)), (0, R4.HOOG - nh - 10))
    return L.tint(leeg, winst)


def main():
    beeld = np.asarray(Image.open(BRON).convert("RGB"), float) / 255.0
    gemeten = {n: L.meet(n, hk, beeld) for n, hk in L.VLAKKEN.items()}
    print()
    winst = L.lichtwinst(gemeten)
    print()

    kleur_achter = winst["achterste doos"][0]
    nu = winst["achterste doos"][2]
    print("achterste doos staat nu op R%.3f G%.3f B%.3f (belichting %.3f)"
          % (nu[0], nu[1], nu[2], winst["achterste doos"][1]))
    print()

    for niveau, belichting in NIVEAUS.items():
        nieuw = kleur_achter * belichting
        print("%s  belichting %.3f -> inkt R%.3f G%.3f B%.3f  (%.1f%% donkerder dan nu)"
              % (niveau, belichting, nieuw[0], nieuw[1], nieuw[2],
                 (1 - (nieuw.mean() / nu.mean())) * 100))
        bron = BRON
        for i, (naam, hoeken) in enumerate(L.VLAKKEN.items()):
            y, doel, logo_v, nt, vb, b, h = R4.logo_y(hoeken, "D")
            w = winst[naam][2] if i == 0 else nieuw
            pad = HIER / ("paneel-r5%s-%d.png" % (niveau, i + 1))
            paneel_met_logo_op(y, w).save(pad)
            uit = (HIER / ("versie-2-r5%s.png" % niveau)) if i else (HIER / ("_tussen-r5%s.png" % niveau))
            crop = HIER / ("versie-2-r5%scrop-%s.png" % (niveau, "achter" if i else "voor"))
            r = subprocess.run(
                [sys.executable, str(TOOL), str(bron),
                 "--hoeken", " ".join("%d,%d" % tuple(q) for q in hoeken.astype(int)),
                 "--logo", str(pad), "--breedte", str(R4.BREEDTE),
                 "--uit", str(uit), "--crop", str(crop)],
                capture_output=True, text=True)
            if r.returncode:
                print(r.stdout, r.stderr)
                raise SystemExit("merk-op-doos faalde")
            bron = uit
        print("   geschreven: versie-2-r5%s.png" % niveau)


if __name__ == "__main__":
    main()
