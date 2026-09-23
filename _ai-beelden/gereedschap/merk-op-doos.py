"""Zet het echte beeldmerk van De Reus op een onbedrukte verhuisdoos.

De dozen in deze ronde zijn met opzet effen bruin, dus er hoeft niets weggehaald te
worden. Wat er wel moet gebeuren: het merk in het perspectief van het dooszijvlak
leggen en het door de luminantie van het karton vermenigvuldigen, anders ligt het als
een sticker op de foto in plaats van erop gedrukt.

Eén beeld:

    python merk-op-doos.py versie-1.png --hoeken "663,331 866,297 861,441 669,452"

Een hele ronde, met de vlakken in een platte lijst ernaast, zoals de jobs.json van de
archiefreeksen:

    python merk-op-doos.py --vlakken vlakken.json --uit-map ../uit

    [
      {"bron": "versie-1.png",
       "hoeken": [[663,331],[866,297],[861,441],[669,452]]},
      {"bron": "versie-2.png", "breedte": 0.42, "variant": "beeldmerk",
       "hoeken": [[732,1002],[1505,984],[1502,1460],[745,1500]]}
    ]

Paden in het json staan relatief aan het json zelf. `variant`, `breedte`, `midden` en
`logo` horen bij het merk en niet bij de ronde: ze staan als standaard in dit script en
zijn per job te overschrijven, zodat ze niet in elk rondebestand uit elkaar gaan lopen.

De vier hoekpunten zijn van het zijvlak waar het merk op komt, met de klok mee vanaf
linksboven: linksboven, rechtsboven, rechtsonder, linksonder. Ze mogen best een paar
pixels mis zijn; het merk staat gecentreerd op het vlak en op de helft van de breedte,
dus het valt ruim binnen de randen.

Schrijft per beeld <naam>-merk.png en <naam>-merkcrop.png (het merkgebied op minimaal
3x, om te lezen of het merk klopt).
"""
import argparse
import json
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HIER = os.path.dirname(os.path.abspath(__file__))

# versie 2 (september 2026), blauw en geel, zonder tagline: het kleurenmerk hoort op
# bruin karton. De negatieve variant is voor koningsblauw en diepblauw.
VARIANT = {
    'logo': ('dereus-logo.png', 100),
    'beeldmerk': ('dereus-beeldmerk.png', 32),
}   # bestandsnaam plus de minimale breedte in pixels die het brandbook voorschrijft


def merkenmap():
    """Zoek brandbook/assets/logo omhoog vanaf het script en vanaf de werkmap.

    Niet uitrekenen met een vast aantal '..': dan verhuist het script niet meer.
    """
    for start in (HIER, os.path.abspath(os.curdir)):
        pad = start
        while True:
            kandidaat = os.path.join(pad, 'brandbook', 'assets', 'logo')
            if os.path.isdir(kandidaat):
                return kandidaat
            ouder = os.path.dirname(pad)
            if ouder == pad:
                break
            pad = ouder
    raise SystemExit('brandbook/assets/logo niet gevonden boven het script of de werkmap. '
                     'Geef het merkbestand met --logo.')

LUM = np.array([0.2126, 0.7152, 0.0722])


def lees_hoeken(tekst):
    """Acht getallen (vier punten) uit de tekst halen."""
    getallen = [float(g) for g in re.findall(r'-?\d+(?:\.\d+)?', tekst)]
    if len(getallen) != 8:
        raise SystemExit('--hoeken wil acht getallen (vier punten), kreeg er %d' % len(getallen))
    return np.array(getallen, float).reshape(4, 2)


def controleer_vlak(p):
    """Bolle vierhoek? Een geknikte volgorde geeft een omgeklapt merk, dus liever hier stuk."""
    def kruisproduct(a, b):     # np.cross doet sinds numpy 2 geen 2D-vectoren meer
        return a[0] * b[1] - a[1] * b[0]

    kruis = np.array([kruisproduct(p[(i + 1) % 4] - p[i], p[(i + 2) % 4] - p[(i + 1) % 4])
                      for i in range(4)])
    if np.any(np.abs(kruis) < 1.0) or not (np.all(kruis > 0) or np.all(kruis < 0)):
        raise SystemExit('De vier hoekpunten vormen geen bol vierhoek. Volgorde is met de klok '
                         'mee vanaf linksboven: linksboven, rechtsboven, rechtsonder, linksonder.')


def homografie(p):
    """Projectieve afbeelding van het eenheidsvierkant naar de vier hoekpunten."""
    src = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
    A = np.zeros((8, 8))
    b = np.zeros(8)
    for i in range(4):
        u, v = src[i]
        x, y = p[i]
        A[2 * i] = [u, v, 1, 0, 0, 0, -u * x, -v * x]
        b[2 * i] = x
        A[2 * i + 1] = [0, 0, 0, u, v, 1, -u * y, -v * y]
        b[2 * i + 1] = y
    return np.append(np.linalg.solve(A, b), 1.0).reshape(3, 3)


def vlakmaten(p):
    """Breedte en hoogte van het vlak in pixels, gemiddeld over beide zijden."""
    breed = (np.linalg.norm(p[1] - p[0]) + np.linalg.norm(p[2] - p[3])) / 2
    hoog = (np.linalg.norm(p[3] - p[0]) + np.linalg.norm(p[2] - p[1])) / 2
    return breed, hoog


def vlakcoordinaten(Hinv, vorm, oorsprong, ss):
    """Per (sub)pixel de plek op het dooszijvlak: u en v lopen van 0 tot 1 binnen het vlak."""
    h, w = vorm
    yy, xx = np.mgrid[0:h * ss, 0:w * ss].astype(float)
    xx = oorsprong[0] + (xx + 0.5) / ss - 0.5
    yy = oorsprong[1] + (yy + 0.5) / ss - 0.5
    een = np.ones_like(xx)
    u = Hinv[0, 0] * xx + Hinv[0, 1] * yy + Hinv[0, 2] * een
    v = Hinv[1, 0] * xx + Hinv[1, 1] * yy + Hinv[1, 2] * een
    wgt = Hinv[2, 0] * xx + Hinv[2, 1] * yy + Hinv[2, 2] * een
    veilig = np.where(np.abs(wgt) < 1e-9, 1e-9, wgt)
    return u / veilig, v / veilig, wgt


def logo_lagen(pad):
    """Het logo als voorvermenigvuldigde RGB plus alfa; zo bloedt de rand niet uit."""
    im = np.asarray(Image.open(pad).convert('RGBA'), float) / 255.0
    alfa = im[..., 3]
    return im[..., :3] * alfa[..., None], alfa


def kartonmasker(a255):
    """Warm maar niet knalgeel: karton. Handen en blauwe polo's vallen erbuiten."""
    som = a255.sum(-1) + 1e-6
    d = (a255[..., 0] - a255[..., 2]) / som
    return (d > 0.06) & (d < 0.32) & (som > 60)


def leg_merk(beeld, p, logo_pad, breedte, midden, schaduw_maat, zacht, korrel, ss, seed):
    """Geeft het bewerkte beeld terug plus een verslag van wat er gebeurd is."""
    H, W = beeld.shape[:2]
    Hm = homografie(p)
    Hinv = np.linalg.inv(Hm)

    lx0 = max(int(np.floor(p[:, 0].min())) - 2, 0)
    ly0 = max(int(np.floor(p[:, 1].min())) - 2, 0)
    lx1 = min(int(np.ceil(p[:, 0].max())) + 3, W)
    ly1 = min(int(np.ceil(p[:, 1].max())) + 3, H)
    if lx1 - lx0 < 8 or ly1 - ly0 < 8:
        raise SystemExit('Het dooszijvlak valt (bijna) buiten het beeld.')
    a = beeld[ly0:ly1, lx0:lx1]
    vorm = a.shape[:2]

    # maat van het merk: een deel van de doosbreedte, met de verhouding van het logo
    # gecorrigeerd voor de verhouding van het vlak zelf
    vlak_b, vlak_h = vlakmaten(p)
    bron_rgb, bron_alfa = logo_lagen(logo_pad)
    Lh, Lw = bron_alfa.shape
    bw = float(breedte)
    bh = bw * (Lh / Lw) * (vlak_b / vlak_h)
    if bh > 0.80:                       # laag vlak: liever smaller dan over de rand
        bw *= 0.80 / bh
        bh = 0.80
    u0, v0 = midden[0] - bw / 2, midden[1] - bh / 2
    if not (0 <= u0 and u0 + bw <= 1 and 0 <= v0 and v0 + bh <= 1):
        raise SystemExit('Het merk valt buiten het vlak (u %.2f-%.2f, v %.2f-%.2f). '
                         'Verklein --breedte of verschuif --midden.'
                         % (u0, u0 + bw, v0, v0 + bh))

    u, v, wgt = vlakcoordinaten(Hinv, vorm, (lx0, ly0), ss)
    voor = wgt * np.sign(wgt.reshape(-1)[wgt.size // 2]) > 0
    in_vlak_ss = (u >= 0) & (u <= 1) & (v >= 0) & (v <= 1) & voor

    # het logo bemonsteren in vlakcoordinaten: dat is de perspectiefafbeelding
    ly = (v - v0) / bh * Lh - 0.5
    lxx = (u - u0) / bw * Lw - 0.5
    binnen = in_vlak_ss & (lxx > -1) & (lxx < Lw) & (ly > -1) & (ly < Lh)
    coords = [np.where(binnen, ly, -5), np.where(binnen, lxx, -5)]
    lagen = [ndimage.map_coordinates(bron_rgb[..., k], coords, order=1, mode='constant')
             for k in range(3)]
    lagen.append(ndimage.map_coordinates(bron_alfa, coords, order=1, mode='constant'))
    ss_uit = np.stack(lagen, -1) * binnen[..., None]
    if ss > 1:                          # supersampling terugvouwen: zachte, rechte randen
        ss_uit = ss_uit.reshape(vorm[0], ss, vorm[1], ss, 4).mean((1, 3))
    merk_rgb_v, alfa = ss_uit[..., :3], ss_uit[..., 3]
    merk_rgb = np.where(alfa[..., None] > 1e-4, merk_rgb_v / np.maximum(alfa[..., None], 1e-4), 0.0)

    in_vlak = in_vlak_ss.reshape(vorm[0], ss, vorm[1], ss).mean((1, 3)) > 0.5

    # schaduw: de luminantie van het karton zelf, 5x5 gladgestreken en geijkt op de
    # mediaan onder het merk. Zo houdt het merk zijn eigen helderheid maar neemt het
    # het verloop en de ribbels van de doos over.
    lum = a @ LUM
    kaart = ndimage.uniform_filter(lum, schaduw_maat)
    voet = alfa > 0.02
    if voet.sum() < 25:
        raise SystemExit('Er komt bijna geen merk in beeld; controleer de hoekpunten.')
    ijk = float(np.median(kaart[voet]))
    schaduw = np.clip(kaart / max(ijk, 1e-6), 0.55, 1.45)
    rgb = np.clip(merk_rgb * schaduw[..., None], 0, 1)

    # geen harde randen: de alfa een halve pixel zachter, en de korrel van het karton
    # er overheen, anders blijft het merk te schoon voor de foto eromheen
    alfa = ndimage.gaussian_filter(alfa, zacht) * in_vlak
    rgb = np.stack([ndimage.gaussian_filter(rgb[..., k], zacht) for k in range(3)], -1)
    uit = a * (1 - alfa[..., None]) + rgb * alfa[..., None]
    if korrel > 0:
        rest = a - ndimage.gaussian_filter(a, (2, 2, 0))
        schoon = in_vlak & ~voet
        ruisbreedte = rest[schoon].std() if schoon.sum() > 50 else 0.006
        ruis = np.random.default_rng(seed).normal(0, max(ruisbreedte, 0.004), uit.shape)
        # met de alfa meewegen, niet met een drempel: anders krijgt de korrel zelf een rand
        uit = np.clip(uit + ruis * alfa[..., None] * korrel, 0, 1)

    vol = beeld.copy()
    vol[ly0:ly1, lx0:lx1] = uit

    karton = kartonmasker(a * 255.0)
    verslag = dict(
        vlak=(vlak_b, vlak_h),
        merk_px=(bw * vlak_b, bh * vlak_h),
        breedte=bw,
        op_karton=float(karton[voet].mean()),
        binnen_vlak=float(in_vlak[voet].mean()),
        schaduw=(float(schaduw[voet].min()), float(schaduw[voet].max())),
        vak=(lx0, ly0, lx1, ly1),
        voet=voet,
    )
    return vol, verslag


def schrijf_crop(beeld, verslag, pad, schaal):
    """Het merkgebied uitsnijden en opschalen, zodat je kunt lezen of het merk klopt."""
    lx0, ly0, lx1, ly1 = verslag['vak']
    ys, xs = np.nonzero(verslag['voet'])
    marge = 0.18
    bx = xs.max() - xs.min() + 1
    by = ys.max() - ys.min() + 1
    x0 = max(int(lx0 + xs.min() - marge * bx), 0)
    x1 = min(int(lx0 + xs.max() + marge * bx) + 1, beeld.shape[1])
    y0 = max(int(ly0 + ys.min() - marge * by), 0)
    y1 = min(int(ly0 + ys.max() + marge * by) + 1, beeld.shape[0])
    crop = Image.fromarray((np.clip(beeld[y0:y1, x0:x1], 0, 1) * 255).round().astype(np.uint8))
    f = max(schaal, int(np.ceil(900 / max(crop.width, 1))))
    crop.resize((crop.width * f, crop.height * f), Image.LANCZOS).save(pad)
    return f, (x0, y0, x1, y1)


def schrijf_debug(beeld, p, pad):
    """Het opgegeven vlak als rode vierhoek over het resultaat, om de hoekpunten na te lopen."""
    im = Image.fromarray((np.clip(beeld, 0, 1) * 255).round().astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.polygon([tuple(q) for q in p], outline=(255, 0, 0))
    for i, q in enumerate(p):
        d.text((q[0] + 3, q[1] + 3), '1234'[i], fill=(255, 0, 0))
    im.save(pad)


def lees_midden(tekst):
    m = [float(g) for g in re.findall(r'-?\d+(?:\.\d+)?', str(tekst))]
    if len(m) != 2:
        raise SystemExit('midden wil twee getallen, bijvoorbeeld 0.5,0.45')
    return m


def doe_beeld(taak, arg, uit_map):
    """Eén bronbeeld met één vlak. taak overschrijft de standaarden van de commandoregel."""
    bron = taak['bron']
    if not os.path.isabs(bron):
        bron = os.path.join(taak.get('bron_map', ''), bron) if taak.get('bron_map') else bron
    hoeken = taak['hoeken']
    p = lees_hoeken(hoeken) if isinstance(hoeken, str) else np.array(hoeken, float).reshape(4, 2)
    controleer_vlak(p)

    variant = taak.get('variant', arg.variant)
    if variant not in VARIANT:
        raise SystemExit('onbekende variant %r; kies uit %s' % (variant, ', '.join(VARIANT)))
    breedte = float(taak.get('breedte', arg.breedte))
    midden = lees_midden(taak.get('midden', arg.midden))
    if not 0.45 <= breedte <= 0.55:
        print('let op: breedte %.2f valt buiten de afgesproken 0.45-0.55' % breedte,
              file=sys.stderr)

    merk = taak.get('logo', arg.logo)
    if merk:
        merk_pad, minimaal = merk, 0
    else:
        naam, minimaal = VARIANT[variant]
        merk_pad = os.path.join(merkenmap(), naam)

    stam = os.path.join(uit_map, os.path.splitext(os.path.basename(bron))[0])
    uit_pad = taak.get('uit', arg.uit) or stam + '-merk.png'
    crop_pad = taak.get('crop', arg.crop) or stam + '-merkcrop.png'

    beeld = np.asarray(Image.open(bron).convert('RGB'), float) / 255.0
    vol, verslag = leg_merk(beeld, p, merk_pad, breedte, midden, arg.schaduw,
                            arg.zacht, arg.korrel, arg.ss, arg.seed)
    Image.fromarray((np.clip(vol, 0, 1) * 255).round().astype(np.uint8)).save(uit_pad)
    f, _ = schrijf_crop(vol, verslag, crop_pad, arg.crop_schaal)
    if arg.debug:
        schrijf_debug(vol, p, stam + '-merkvlak.png')

    vb, vh = verslag['vlak']
    mb, mh = verslag['merk_px']
    print('%s  vlak %.0fx%.0f px   merk %.0fx%.0f px (%.0f%% van de doosbreedte)'
          % (os.path.basename(bron), vb, vh, mb, mh, verslag['breedte'] * 100))
    print('   merk op karton %.1f%%   binnen het vlak %.1f%%   schaduw %.2f-%.2fx'
          % (verslag['op_karton'] * 100, verslag['binnen_vlak'] * 100,
             verslag['schaduw'][0], verslag['schaduw'][1]))
    if verslag['op_karton'] < 0.90:
        print('let op (%s): een deel van het merk ligt niet op karton (hand, band of rand). '
              'Verklein breedte of verschuif midden.' % os.path.basename(bron), file=sys.stderr)
    if minimaal and round(mb) < minimaal:
        # het brandbook: logo vanaf 100 px breed, beeldmerk vanaf 32 px. Daaronder loopt
        # de naam dicht en dat is precies wat de merkcrop moet laten zien.
        raad = ' Neem variant beeldmerk.' if variant == 'logo' else ''
        print('let op (%s): het merk wordt %.0f px breed, onder de %d px die het brandbook '
              'voor het %s vraagt.%s' % (os.path.basename(bron), mb, minimaal, variant, raad),
              file=sys.stderr)
    print('   geschreven:', uit_pad)
    print('   geschreven:', crop_pad, '(%dx)' % f)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('bron', nargs='?', help='het bronbeeld; laat weg bij --vlakken')
    ap.add_argument('--hoeken',
                    help='vier hoekpunten van het dooszijvlak, met de klok mee vanaf '
                         'linksboven: "x,y x,y x,y x,y"')
    ap.add_argument('--vlakken',
                    help='json met de vlakken van een hele ronde, in plaats van bron en '
                         '--hoeken')
    ap.add_argument('--uit-map', help='map voor de uitvoer; standaard naast het bronbeeld')
    ap.add_argument('--variant', choices=sorted(VARIANT), default='logo',
                    help='logo = armen, huis en naam; beeldmerk = alleen armen en huis, '
                         'voor een klein dooszijvlak waar de naam toch dichtloopt')
    ap.add_argument('--logo', help='een eigen merkbestand in plaats van --variant')
    ap.add_argument('--uit', help='standaard <bron>-merk.png; alleen bij één beeld')
    ap.add_argument('--crop', help='standaard <bron>-merkcrop.png; alleen bij één beeld')
    ap.add_argument('--breedte', type=float, default=0.50,
                    help='breedte van het merk als deel van de doosbreedte (0.45-0.55)')
    ap.add_argument('--midden', default='0.5,0.5',
                    help='middelpunt op het vlak, 0-1 in u,v; 0.5,0.5 is het hart')
    ap.add_argument('--schaduw', type=int, default=5, help='venster van de luminantiekaart')
    ap.add_argument('--zacht', type=float, default=0.8, help='verzachting van de merkrand')
    ap.add_argument('--korrel', type=float, default=0.3, help='hoeveel kartonkorrel erover')
    ap.add_argument('--crop-schaal', type=int, default=3, help='minimale vergroting van de crop')
    ap.add_argument('--ss', type=int, default=3, help='supersampling')
    ap.add_argument('--seed', type=int, default=7)
    ap.add_argument('--debug', action='store_true', help='schrijft ook <bron>-merkvlak.png')
    arg = ap.parse_args()

    if arg.vlakken:
        if arg.bron or arg.hoeken:
            raise SystemExit('--vlakken gaat over de hele ronde; laat bron en --hoeken weg.')
        with open(arg.vlakken, encoding='utf-8') as fh:
            banen = json.load(fh)
        # platte lijst van jobs, zoals jobs.json in de archiefreeksen. Geen wikkelobject:
        # variant, breedte en logo horen bij het merk en staan hieronder als standaard,
        # per job te overschrijven.
        if not isinstance(banen, list):
            raise SystemExit('%s moet een platte lijst van jobs zijn: '
                             '[{"bron": ..., "hoeken": [[x,y] x4]}, ...]' % arg.vlakken)
        if not banen:
            raise SystemExit('%s is leeg.' % arg.vlakken)
        # de paden in het json staan relatief aan het json zelf, niet aan de werkmap
        basis = os.path.dirname(os.path.abspath(arg.vlakken))
        uit_map = arg.uit_map or basis
        if not os.path.isabs(uit_map):
            uit_map = os.path.join(basis, uit_map)
        os.makedirs(uit_map, exist_ok=True)
        taken = []
        for i, t in enumerate(banen):
            if 'bron' not in t or 'hoeken' not in t:
                raise SystemExit('job %d in %s mist "bron" of "hoeken".' % (i + 1, arg.vlakken))
            taken.append(dict(t, bron_map=t.get('bron_map', basis)))
    else:
        if not arg.bron or not arg.hoeken:
            raise SystemExit('geef een bronbeeld met --hoeken, of een ronde met --vlakken.')
        uit_map = arg.uit_map or os.path.dirname(os.path.abspath(arg.bron))
        os.makedirs(uit_map, exist_ok=True)
        taken = [dict(bron=arg.bron, hoeken=arg.hoeken)]

    if len(taken) > 1 and (arg.uit or arg.crop):
        raise SystemExit('--uit en --crop gaan over één beeld; gebruik --uit-map.')
    for taak in taken:
        doe_beeld(taak, arg, uit_map)


if __name__ == '__main__':
    main()
