#!/usr/bin/env python3
"""Drukklare vector-PDF's van het logo van Verhuisbedrijf De Reus, in CMYK.

Draaien:  python brandbook/assets/logo/druk/_bron/maak_pdf.py
Nodig:    alleen Python 3 (geen extra pakketten)
Uitvoer:  brandbook/assets/logo/druk/*.pdf

Het script leest de paden uit ../../*.svg (alleen M, L, H, V, C, Q en Z, absolute
coordinaten, vlakke vullingen) en schrijft ze een op een als PDF-paden. Er wordt
niets gerasterd. De RGB-kleuren uit de SVG worden vervangen door de vaste
CMYK-waarden uit het blok KLEUREN (DeviceCMYK). 1000 eenheden in de SVG worden
100 mm in de PDF, dus het beeldmerk is in elk bestand 100 mm breed.
"""
import os
import re
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
LOGO_DIR = os.path.dirname(OUT)

# ---------------------------------------------------------------------------
# KLEUREN  (bron: brandbook/research/color-type-system.md, Coated FOGRA39)
# ---------------------------------------------------------------------------
KLEUREN = {
    "#1746A2": (0.97, 0.77, 0.00, 0.00),   # Koningsblauw, 97 77 0 0
    "#FFCC33": (0.00, 0.20, 0.85, 0.00),   # Goudgeel, 0 20 85 0
    "#FFFFFF": (0.00, 0.00, 0.00, 0.00),   # wit: geen inkt
    "#000000": (0.00, 0.00, 0.00, 1.00),   # zwart: alleen K, geen rijk zwart
}

BESTANDEN = [
    "dereus-logo",
    "dereus-logo-negatief",
    "dereus-logo-1kleur",
    "dereus-logo-1kleur-blauw",
    "dereus-logo-zonder-tagline",
    "dereus-logo-zonder-tagline-negatief",
    "dereus-logo-horizontaal",
    "dereus-logo-horizontaal-negatief",
    "dereus-beeldmerk",
]

MM = 72 / 25.4
SCHAAL = 0.1 * MM          # 1 eenheid = 0,1 mm


def n(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def pad_naar_pdf(d, hoogte):
    """SVG-pad (absoluut) naar PDF-operatoren. De y-as wordt omgeklapt."""
    tokens = re.findall(r"[MLHVCQZ]|-?\d*\.?\d+(?:e-?\d+)?", d)
    onbekend = set(re.findall(r"[a-zA-Z]", d)) - set("MLHVCQZe")
    assert not onbekend, f"niet ondersteund in pad: {onbekend}"
    out, i, cmd = [], 0, None
    x = y = sx = sy = 0.0

    def P(px, py):
        return f"{n(px * SCHAAL)} {n((hoogte - py) * SCHAAL)}"

    def take(k):
        nonlocal i
        vals = [float(t) for t in tokens[i:i + k]]
        i += k
        return vals

    while i < len(tokens):
        if tokens[i] in "MLHVCQZ":
            cmd = tokens[i]
            i += 1
            if cmd == "Z":
                out.append("h")
                x, y = sx, sy
                continue
        if cmd == "M":
            x, y = take(2)
            sx, sy = x, y
            out.append(f"{P(x, y)} m")
            cmd = "L"                          # volgende paren zijn lijnen
        elif cmd == "L":
            x, y = take(2)
            out.append(f"{P(x, y)} l")
        elif cmd == "H":
            (x,) = take(1)
            out.append(f"{P(x, y)} l")
        elif cmd == "V":
            (y,) = take(1)
            out.append(f"{P(x, y)} l")
        elif cmd == "C":
            x1, y1, x2, y2, x3, y3 = take(6)
            out.append(f"{P(x1, y1)} {P(x2, y2)} {P(x3, y3)} c")
            x, y = x3, y3
        elif cmd == "Q":                       # kwadratisch naar kubisch, exact
            qx, qy, x3, y3 = take(4)
            c1 = (x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y))
            c2 = (x3 + 2 / 3 * (qx - x3), y3 + 2 / 3 * (qy - y3))
            out.append(f"{P(*c1)} {P(*c2)} {P(x3, y3)} c")
            x, y = x3, y3
    return "\n".join(out)


def maak(naam):
    src = open(os.path.join(LOGO_DIR, naam + ".svg"), encoding="utf-8").read()
    assert "transform=" not in src and "fill-rule" not in src and "<use" not in src
    _, _, w, h = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).split()]
    titel = re.search(r"<title[^>]*>(.*?)</title>", src, re.S).group(1).strip()
    paden = re.findall(r'<path\b[^>]*?\sfill="([^"]+)"[^>]*?\sd="([^"]+)"', src)
    assert len(paden) == src.count("<path"), f"{naam}: niet elk pad heeft fill voor d"

    stream, kleur = [], None
    for fill, d in paden:
        cmyk = KLEUREN[fill.upper()]
        if cmyk != kleur:
            stream.append(" ".join(n(c) for c in cmyk) + " k")
            kleur = cmyk
        stream.append(pad_naar_pdf(d, h))
        stream.append("f")                     # nonzero, net als de SVG
    data = zlib.compress("\n".join(stream).encode("ascii"), 9)

    box = f"[0 0 {n(w * SCHAAL)} {n(h * SCHAAL)}]"
    info = titel.encode("utf-16-be").hex().upper()
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (f"<< /Type /Page /Parent 2 0 R /MediaBox {box} /TrimBox {box} "
         f"/Resources << >> /Contents 4 0 R >>").encode(),
        b"<< /Length %d /Filter /FlateDecode >>\nstream\n" % len(data) + data + b"\nendstream",
        (f"<< /Title <FEFF{info}> /Author (Verhuisbedrijf De Reus) "
         f"/Creator (maak_pdf.py, DeviceCMYK) >>").encode(),
    ]
    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for k, body in enumerate(objs, 1):
        offsets.append(len(pdf))
        pdf += b"%d 0 obj\n" % k + body + b"\nendobj\n"
    xref = len(pdf)
    pdf += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for off in offsets:
        pdf += b"%010d 00000 n \n" % off
    pdf += b"trailer\n<< /Size %d /Root 1 0 R /Info 5 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    with open(os.path.join(OUT, naam + ".pdf"), "wb") as f:
        f.write(pdf)
    print(f"   {naam + '.pdf':40s} {w / 10:6.1f} x {h / 10:5.1f} mm  {len(paden):3d} paden  {len(pdf) // 1024:3d} kB")


if __name__ == "__main__":
    print("Druk-PDF's naar", OUT)
    for naam in BESTANDEN:
        maak(naam)
