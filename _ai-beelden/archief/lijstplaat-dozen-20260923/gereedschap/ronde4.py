#!/usr/bin/env python3
"""Ronde 4: dezelfde belettering op beide dozen, logo gecentreerd, nummer laag.

Twee lezingen van "gecentreerd", allebei met het nummer waar ronde 3 het had:

  C  het logo in het hart van het doosvlak
  D  het logo in het hart van de ruimte boven het nummer

C levert op beide dozen letterlijk hetzelfde paneel, want het paneel staat zelf gecentreerd
op het vlak. D moet het logo per doos op een andere hoogte zetten, omdat de twee vlakken een
andere verhouding hebben; de elementen en hun maten blijven gelijk.

De lichtijking uit ronde 3 blijft: de inkt van elke doos wordt vermenigvuldigd met het licht
van dat vlak ten opzichte van het andere. Zie licht.py voor de meting.
"""
import importlib.util
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image

HIER = pathlib.Path(__file__).resolve().parent
WORTEL = HIER.parents[2]
spec = importlib.util.spec_from_file_location("licht", HIER / "licht.py")
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)

TOOL = WORTEL / "_ai-beelden/gereedschap/merk-op-doos.py"
BRON = HIER / "versie-2-r2bron.png"
BREEDTE = 0.85
HOOG = 1260                     # paneelhoogte, gelijk aan ronde 3
LOGO_H = 427                    # hoogte van het horizontale logo op 2048 breed
NUMMER_H = 190


def plek(hoeken):
    """bw, bh, v0 van het paneel op dit vlak, met dezelfde rekensom als merk-op-doos."""
    b, h = L.mod.vlakmaten(hoeken)
    bw = BREEDTE
    bh = bw * (HOOG / 2048) * (b / h)
    return bw, bh, 0.5 - bh / 2, b, h


def logo_y(hoeken, lezing):
    """Waar het logo in het paneel moet staan om op dit vlak gecentreerd te lijken."""
    bw, bh, v0, b, h = plek(hoeken)
    logo_v = LOGO_H / HOOG * bh                      # logohoogte als deel van het VLAK
    nummer_top_v = v0 + (HOOG - NUMMER_H) / HOOG * bh
    doel = 0.5 if lezing == "C" else nummer_top_v / 2
    y = ((doel - logo_v / 2) - v0) / bh * HOOG
    return y, doel, logo_v, nummer_top_v, v0 + bh, b, h


def main():
    beeld = np.asarray(Image.open(BRON).convert("RGB"), float) / 255.0
    gemeten = {n: L.meet(n, hk, beeld) for n, hk in L.VLAKKEN.items()}
    print()
    winst = L.lichtwinst(gemeten)
    print()

    for lezing, wat in (("C", "logo in het hart van het doosvlak"),
                        ("D", "logo in het hart van de ruimte boven het nummer")):
        print("%s  %s" % (lezing, wat))
        tussen = HIER / ("_tussen-%s.png" % lezing)
        bron = BRON
        for i, (naam, hoeken) in enumerate(L.VLAKKEN.items()):
            y, doel, logo_v, nt, vb, b, h = logo_y(hoeken, lezing)
            p, _, nh = L.paneel_vol(HOOG)
            # het logo verplaatsen: opnieuw opbouwen met het logo op hoogte y
            leeg = Image.new("RGBA", (2048, HOOG), (0, 0, 0, 0))
            logo = Image.open(L.LOGO).convert("RGBA")
            logo = logo.resize((2048, round(logo.height * 2048 / logo.width)), Image.LANCZOS)
            leeg.alpha_composite(logo, (0, round(y)))
            # het nummer uit het volle paneel overnemen, dat staat al op de onderrand
            nummerstrook = p.crop((0, HOOG - nh - 10, 2048, HOOG))
            leeg.alpha_composite(nummerstrook, (0, HOOG - nh - 10))
            paneel = L.tint(leeg, winst[naam][2])
            pad = HIER / ("paneel-%s-%d.png" % (lezing, i + 1))
            paneel.save(pad)
            uit = HIER / ("versie-2-r4%s.png" % lezing) if i else tussen
            crop = HIER / ("versie-2-r4%scrop-%s.png" % (lezing, "achter" if i else "voor"))
            print("   %-15s vlak %.0fx%.0f, paneel %.0f px breed, logo op vlak-v %.3f-%.3f, "
                  "nummer %.3f-%.3f" % (naam, b, h, BREEDTE * b, doel - logo_v / 2,
                                        doel + logo_v / 2, nt, vb))
            r = subprocess.run(
                [sys.executable, str(TOOL), str(bron),
                 "--hoeken", " ".join("%d,%d" % tuple(q) for q in hoeken.astype(int)),
                 "--logo", str(pad), "--breedte", str(BREEDTE),
                 "--uit", str(uit), "--crop", str(crop)],
                capture_output=True, text=True)
            if r.returncode:
                print(r.stdout, r.stderr)
                raise SystemExit("merk-op-doos faalde")
            bron = uit
        print("   geschreven: versie-2-r4%s.png" % lezing)
        print()


if __name__ == "__main__":
    main()
