"""Zet een raster met coordinaten over een uitsnede, om de vier hoekpunten af te lezen.

    python hoekraster.py versie-1.png --vak "620,260 900,500"

Schrijft versie-1-raster.png: het vak vergroot, met rode lijnen (x) en groene lijnen (y)
in de coordinaten van het originele beeld. Lees de vier hoeken van het dooszijvlak af en
geef ze met de klok mee vanaf linksboven aan merk-op-doos.py.
"""
import argparse
import os
import re

from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('bron')
    ap.add_argument('--vak', required=True, help='"links,boven rechts,onder" in beeldpixels')
    ap.add_argument('--stap', type=int, default=20, help='afstand tussen de rasterlijnen')
    ap.add_argument('--schaal', type=int, default=0, help='vergroting; 0 = automatisch')
    ap.add_argument('--uit')
    arg = ap.parse_args()

    g = [int(float(n)) for n in re.findall(r'-?\d+(?:\.\d+)?', arg.vak)]
    if len(g) != 4:
        raise SystemExit('--vak wil vier getallen: "links,boven rechts,onder"')
    l, t, r, b = g

    im = Image.open(arg.bron).convert('RGB')
    l, t = max(l, 0), max(t, 0)
    r, b = min(r, im.width), min(b, im.height)
    if r - l < 4 or b - t < 4:
        raise SystemExit('Het vak valt (bijna) buiten het beeld.')

    f = arg.schaal or max(2, int(1200 / max(r - l, 1)))
    uit = im.crop((l, t, r, b)).resize(((r - l) * f, (b - t) * f), Image.LANCZOS)
    d = ImageDraw.Draw(uit)
    for x in range(l - l % arg.stap + arg.stap, r, arg.stap):
        d.line([((x - l) * f, 0), ((x - l) * f, uit.height)], fill=(255, 0, 0))
        d.text(((x - l) * f + 2, 2), str(x), fill=(255, 0, 0))
    for y in range(t - t % arg.stap + arg.stap, b, arg.stap):
        d.line([(0, (y - t) * f), (uit.width, (y - t) * f)], fill=(0, 220, 0))
        d.text((2, (y - t) * f + 2), str(y), fill=(0, 150, 0))

    pad = arg.uit or os.path.splitext(arg.bron)[0] + '-raster.png'
    uit.save(pad)
    print('geschreven: %s (%dx, raster elke %d px)' % (pad, f, arg.stap))


if __name__ == '__main__':
    main()
