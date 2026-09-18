#!/usr/bin/env python3
"""Maakt de vrijstaande teamfoto voor de hero uit een groepsfoto op een effen achtergrond.

Hulpmiddel naast de build, niet ervan (de build blijft standaardbibliotheek). Nodig: Pillow, numpy en scipy,
plus een masker (grijswaarden, wit = persoon), bijvoorbeeld van rembg (model isnet-general-use).

    python _werk/teambeeld.py <foto.jpg> <masker.png> [<grensmasker.png>]

Het optionele grensmasker (zelfde maat) begrenst het eerste: waar het grensmasker duidelijk achtergrond zegt
(meer dan 3 px van de persoon), wordt het beeld doorzichtig. Zo combineert u de fijne haarrand van rembg met
een strak masker dat ingesloten achtergrond wel herkent. De pixels komen altijd uit <foto.jpg>.

Stappen:
1. achtergrond schatten: een glad vlak (tweedegraads per kleurkanaal) door de pixels buiten het masker;
2. ingesloten achtergrond weghalen: vlakken die de kleur van de achtergrond hebben en groter zijn dan
   een logo (bijvoorbeeld tussen een arm en een schouder) worden doorzichtig;
3. rand opschonen: het masker iets strakker (geen lichte zoom) en de randkleur terugrekenen zonder
   de grijze achtergrond (ontkleuren van de rand, dus geen lichte rand rond het haar op Diepblauw);
4. bijsnijden op de personen, met een rechte onderrand (valt in de hero achter de offertekaart);
5. schrijven naar img/team/: team-hero-700.webp, -1100.webp, -1600.webp en team-hero-700.png als
   terugval, plus img/team/team-hero.json met de maten voor width en height in de HTML.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

WORTEL = Path(__file__).resolve().parent.parent
UIT = WORTEL / "img" / "team"
BREEDTES = (700, 1100, 1600)
NAAM = "team-hero"


def achtergrond(rgb, a):
    """Glad achtergrondvlak per kanaal, gefit op pixels die zeker achtergrond zijn."""
    h, w, _ = rgb.shape
    ys, xs = np.nonzero(a < 0.02)
    kies = np.random.default_rng(1).choice(len(ys), size=min(60000, len(ys)), replace=False)
    ys, xs = ys[kies], xs[kies]
    xn, yn = xs / w, ys / h
    A = np.stack([np.ones_like(xn), xn, yn, xn * xn, yn * yn, xn * yn], 1)
    Y, X = np.mgrid[0:h, 0:w]
    Xn, Yn = X / w, Y / h
    vlak = np.empty_like(rgb)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, rgb[ys, xs, c], rcond=None)
        vlak[..., c] = coef[0] + coef[1] * Xn + coef[2] * Yn + coef[3] * Xn ** 2 + coef[4] * Yn ** 2 + coef[5] * Xn * Yn
    return vlak


def maak(foto, masker, grens=None):
    rgb = np.asarray(Image.open(foto).convert("RGB")).astype(np.float32) / 255
    a = np.asarray(Image.open(masker).convert("L")).astype(np.float32) / 255
    if a.shape != rgb.shape[:2]:
        raise SystemExit("masker en foto hebben niet dezelfde maat")
    if grens:
        g = np.asarray(Image.open(grens).convert("L")).astype(np.float32) / 255
        g = ndimage.maximum_filter(g, size=7)                    # 3 px ruimte rond de persoon
        g = ndimage.gaussian_filter(g, 1.2)                      # zachte overgang
        a = np.minimum(a, g)
    B = achtergrond(rgb, a)
    # ingesloten achtergrond: kleur binnen 0,05 van het vlak, samenhangend en groter dan een logo
    lijkt = np.abs(rgb - B).max(2) < 0.05
    labels, n = ndimage.label(lijkt & (a > 0.02))
    if n:
        maten = ndimage.sum(np.ones_like(a), labels, index=np.arange(1, n + 1))
        groot = np.zeros(n + 1, bool)
        groot[1:] = maten > 4000
        gat = groot[labels]
        gat = ndimage.binary_dilation(gat, iterations=2)          # de overgang naar de persoon mee
        a = np.where(gat, np.minimum(a, np.clip(np.abs(rgb - B).max(2) / 0.10, 0, 1)), a)
    # strakker masker: de buitenste zachte zoom weg, harde kern blijft
    a = np.clip((a - 0.12) / 0.80, 0, 1)
    # randkleur zonder achtergrond: F = (C - (1 - a) B) / a
    rand = (a > 0.02) & (a < 0.98)
    F = rgb.copy()
    veilig = np.maximum(a, 0.05)[..., None]
    F[rand] = np.clip((rgb[rand] - (1 - a[rand])[:, None] * B[rand]) / veilig[rand], 0, 1)
    # heel lichte randpixels iets donkerder, tegen een lichte zoom op Diepblauw
    licht = rand & (F.mean(2) > B.mean(2) - 0.04)
    F[licht] *= 0.85
    rgba = np.dstack([F, a])
    img = Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), "RGBA")
    # bijsnijden: links, rechts en boven op de personen met wat lucht, onder recht op de fotorand
    x0, y0, x1, _ = img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    marge = 24
    img = img.crop((max(0, x0 - marge), max(0, y0 - marge), min(img.width, x1 + marge), img.height))
    return img


def schrijf(img):
    UIT.mkdir(parents=True, exist_ok=True)
    maten = {}
    for b in BREEDTES:
        h = round(img.height * b / img.width)
        klein = img.resize((b, h), Image.LANCZOS)
        pad = UIT / f"{NAAM}-{b}.webp"
        klein.save(pad, "WEBP", quality=80 if b <= 1100 else 70, method=6, alpha_quality=90)
        maten[b] = [b, h, pad.stat().st_size]
        print(f"  {pad.relative_to(WORTEL).as_posix():32} {b}x{h}  {pad.stat().st_size // 1024} KB")
    # terugval voor browsers zonder webp (vrijwel geen): klein en met 256 kleuren, dus licht
    b = BREEDTES[0]
    h = round(img.height * b / img.width)
    png = UIT / f"{NAAM}-{b}.png"
    img.resize((b, h), Image.LANCZOS).quantize(256, method=Image.Quantize.FASTOCTREE).save(png, optimize=True)
    print(f"  {png.relative_to(WORTEL).as_posix():32} {b}x{h}  {png.stat().st_size // 1024} KB (terugval)")
    (UIT / f"{NAAM}.json").write_text(json.dumps({"naam": NAAM, "verhouding": [img.width, img.height],
                                                  "breedtes": list(BREEDTES), "png": b}, indent=2) + "\n",
                                      encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    schrijf(maak(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None))
