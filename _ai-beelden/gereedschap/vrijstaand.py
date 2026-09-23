"""Snijdt een figuur los van een effen studiodoek en schrijft een vrijstaande webp.

Zelfde route als de hero-trio: rembg met isnet-general-use op het bronbeeld op volle
resolutie. Daar komt een masker uit dat de haarrand goed pakt, maar de halfdoorzichtige
randpixels dragen nog de grijze doek in zich. Op een donkere sectieachtergrond wordt dat
een lichte zoom om de hele figuur, en dat is precies waar een uitsnede op afstand aan te
zien is. Dus na rembg nog drie dingen: losse snippers weg, de rand ontgrijzen, en pas dan
bijsnijden op wat er overblijft.

    python vrijstaand.py <bron.png> <doel.webp> [--hoog 1200] [--kwaliteit 82]

Schrijft het bestand en print één regel met de maten en het alfakader, in de vorm die de
plaatsing verderop nodig heeft: pad, bestandsbreedte, bestandshoogte, x, y, w, h.
"""
import argparse
import os

import numpy as np
from PIL import Image
from scipy import ndimage


def masker(bron):
    """rembg, met het model dat de rest van de site ook gebruikt."""
    from rembg import new_session, remove
    im = Image.open(bron).convert('RGB')
    uit = remove(im, session=new_session('isnet-general-use'))
    return np.asarray(im, float), np.asarray(uit, float)[..., 3] / 255.0


def grootste_blok(a, drempel=0.5):
    """Alleen de figuur houden. rembg laat soms een snipper doek of een schaduwvlek staan."""
    vast = a > drempel
    lab, n = ndimage.label(vast)
    if n <= 1:
        return a
    maten = ndimage.sum(vast, lab, range(1, n + 1))
    houd = lab == 1 + int(np.argmax(maten))
    # wat aan de figuur vastzit via halfdoorzichtige pixels hoort er ook bij
    houd = ndimage.binary_propagation(houd, mask=a > 0.05)
    return a * houd


def ontgrijs(rgb, alfa, straal=60):
    """Haalt het doek uit de halfdoorzichtige randpixels.

    De waargenomen kleur is C = a*F + (1-a)*B. B schatten we lokaal uit de pixels die
    volledig doek zijn, glad gemaakt over een grote straal, zodat een verloop in het doek
    meegaat. Daarna F terugrekenen. Zonder deze stap houdt elke randpixel een beetje grijs
    vast en krijgt de figuur op een donkere achtergrond een lichte zoom.
    """
    doek = (alfa < 0.05).astype(float)
    som = ndimage.gaussian_filter(rgb * doek[..., None], (straal, straal, 0))
    tel = ndimage.gaussian_filter(doek, straal)[..., None]
    B = som / np.maximum(tel, 1e-6)
    rand = (alfa > 0.02) & (alfa < 0.98)
    a = alfa[..., None]
    F = np.where(rand[..., None], (rgb - (1 - a) * B) / np.maximum(a, 0.02), rgb)
    return np.clip(F, 0, 255)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('bron')
    p.add_argument('doel')
    p.add_argument('--hoog', type=int, default=1200,
                   help='hoogte van het doelbestand; 0 laat de bronresolutie staan')
    p.add_argument('--kwaliteit', type=int, default=82)
    p.add_argument('--krimp', type=float, default=0.6,
                   help='px waarmee de rand strakker wordt getrokken')
    p.add_argument('--vast', action='append', default=[],
                   help='masker (wit = dekkend) dat sowieso ondoorzichtig moet worden; '
                        'voor vlakken die rembg niet van het doek kan houden, zoals een '
                        'witte doos tegen een lichtgrijze achtergrond')
    arg = p.parse_args()

    rgb, alfa = masker(arg.bron)
    alfa = grootste_blok(alfa)
    # Wit karton tegen een lichtgrijs doek is te weinig contrast: rembg geeft zo'n vlak
    # een halve alfa en de doos wordt doorschijnend op een donkere sectie. Waar we zelf
    # precies weten dat er doos zit, zetten we de alfa hard op 1.
    for pad in arg.vast:
        v = np.asarray(Image.open(pad).convert('L'), float) / 255.0
        if v.shape != alfa.shape:
            raise SystemExit(f'{pad} is {v.shape}, het beeld is {alfa.shape}')
        alfa = np.maximum(alfa, (v > 0.5).astype(float))
    # de rand een halve pixel strakker: rembg zit er eerder een tikje buiten dan binnen
    if arg.krimp:
        alfa = np.clip((alfa - arg.krimp * 0.5) / max(1 - arg.krimp * 0.5, 1e-6), 0, 1)
        alfa = ndimage.gaussian_filter(alfa, 0.4)
    rgb = ontgrijs(rgb, alfa)

    ys, xs = np.nonzero(alfa > 0.02)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    uit = np.dstack([rgb[y0:y1, x0:x1], alfa[y0:y1, x0:x1] * 255])
    im = Image.fromarray(np.clip(uit, 0, 255).round().astype('uint8'), 'RGBA')
    if arg.hoog and im.height != arg.hoog:
        im = im.resize((max(round(im.width * arg.hoog / im.height), 1), arg.hoog), Image.LANCZOS)
    os.makedirs(os.path.dirname(os.path.abspath(arg.doel)), exist_ok=True)
    # Het doelformaat volgt de extensie. Een png is de bron voor een verdere export
    # (export-teambeeld.cjs wil een master met alfa), een webp is het eindbestand.
    if arg.doel.lower().endswith('.png'):
        im.save(arg.doel, 'PNG', compress_level=6)
    else:
        im.save(arg.doel, 'WEBP', quality=arg.kwaliteit, method=6)

    a = np.asarray(im, float)[..., 3]
    ys, xs = np.nonzero(a > 2)
    print(f"{arg.doel}  {im.width}x{im.height}  alfakader {xs.min()},{ys.min()},"
          f"{xs.max() - xs.min() + 1},{ys.max() - ys.min() + 1}  "
          f"{os.path.getsize(arg.doel) / 1024:.1f} kB")


if __name__ == '__main__':
    main()
