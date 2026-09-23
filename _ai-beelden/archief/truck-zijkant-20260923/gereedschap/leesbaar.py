#!/usr/bin/env python3
"""Is het nummer nog leesbaar als de site het beeld klein toont?

Meet het contrast tussen de inkt van de cijfers en de flank eromheen, op ware grootte en
op de maten waarop de site zo'n beeld toont, en schrijft een strook met het nummer op die
maten zodat het ook met het oog te controleren is.
"""
import pathlib

import numpy as np
from PIL import Image

HIER = pathlib.Path(__file__).resolve().parent
SCHOON = np.asarray(Image.open(HIER / "versie-5.png").convert("RGB"), float)
BRON_BREED = SCHOON.shape[1]
# het nummer ligt op vlak-v 0.797 tot 0.883; dit vak sluit daar met marge omheen
VAK = (1500, 900, 2260, 1060)
MATEN = [("volledig", 1.0), ("1200 px breed (footer-wagen)", 1200 / BRON_BREED),
         ("720 px breed (lijstplaat)", 720 / BRON_BREED),
         ("390 px breed (telefoon)", 390 / BRON_BREED)]


def wcag(l1, l2):
    a, b = max(l1, l2), min(l1, l2)
    return (a + 0.05) / (b + 0.05)


def lineair(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def relatief(rgb):
    lin = lineair(rgb)
    return lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722


for naam in ("versie-5-B.png", "versie-5-C.png", "versie-5-D.png"):
    vol = Image.open(HIER / naam).convert("RGB")
    print("\n%s" % naam)
    stroken = []
    for label, f in MATEN:
        if f < 1.0:
            klein = vol.resize((round(vol.width * f), round(vol.height * f)), Image.LANCZOS)
            vak = [round(v * f) for v in VAK]
        else:
            klein, vak = vol, list(VAK)
        a = np.asarray(klein.crop(vak).convert("RGB"), float)
        L = relatief(a)
        # de inkt is het donkerste vijfde, de flank het lichtste vijfde van het vak
        inkt = np.percentile(L, 4)
        flank = np.percentile(L, 90)
        # hoeveel pixels zijn duidelijk inkt: maat voor of de cijfers nog dicht lopen
        deel = float((L < (inkt + flank) / 2).mean())
        print("   %-28s inkt %.3f  flank %.3f  contrast %4.1f:1   inktvlak %4.1f%%   cijferhoogte %.0f px"
              % (label, inkt, flank, wcag(flank, inkt), deel * 100, (VAK[3] - VAK[1]) * f * 0.42))
        s = klein.crop(vak)
        if f < 1.0:
            stroken.append(s)
    b = max(s.width for s in stroken)
    h = sum(s.height for s in stroken) + 8 * (len(stroken) - 1)
    blad = Image.new("RGB", (b, h), (255, 255, 255))
    y = 0
    for s in stroken:
        blad.paste(s, (0, y))
        y += s.height + 8
    blad.save(HIER / "_controle" / ("leesbaar-%s" % naam.replace("versie-5-", "")))
print("\nstroken geschreven in _controle/")
