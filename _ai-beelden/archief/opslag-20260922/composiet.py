"""Vervang de drie verzonnen De Reus-prints in de opslagfoto door het echte merk.

Werkt op de bronfoto (1200x896), niet op de webp van 720x540: compositen op vol formaat
en daarna verkleinen geeft veel schonere randen.

Per print: oude inkt maskeren op kleur, weghalen door vanuit de omgeving te vullen,
de luminantie van die vulling als schaduwkaart bewaren, het officiele logo erin passen
met een IoU-fit op het oude merk, en het merk vermenigvuldigen met die schaduwkaart.

  python composiet.py [--debug]
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = 'C:/users/arnas/git_repos/dereus'
BRON = ROOT + '/_ai-beelden/foto/Onze diensten/Tijdelijke opslag.jpg'
WERK = ROOT + '/website/review/beeld-opslag-ronde-1'
LOGO = {
    'kleur': ROOT + '/brandbook/assets/logo/dereus-logo.png',
    'negatief': ROOT + '/brandbook/assets/logo/dereus-logo-negatief.png',
}
DEBUG = '--debug' in sys.argv

# merkkleuren uit het brandbook
BLAUW = np.array([23, 70, 162], float)
GEEL = np.array([255, 204, 51], float)
WIT = np.array([255, 255, 255], float)

JOBS = [
    dict(naam='doos-groot', vak=(832, 470, 1158, 768), grond='karton', versie='kleur',
         tekst=True, hoek=-14.0, zacht=1.2, bereik=40, minmaat=25, halo=14, inpassen=True, korrel=0.55),
    dict(naam='doos-links', vak=(228, 698, 400, 896), grond='karton', versie='kleur',
         tekst=False, hoek=-19.0, zacht=1.6, bereik=30, minmaat=8, halo=14, inpassen=True,
         korrel=0.5, oude_tekst_weg=True),
    dict(naam='borst', vak=(630, 492, 742, 582), grond='polo', versie='negatief',
         tekst=False, hoek=-8.0, zacht=1.0, bereik=14, minmaat=4, halo=16, inpassen=True, korrel=0.25,
         oude_tekst_weg=True, snede=(722, 0.30, 500)),
]


def kanalen(a):
    return a[..., 0], a[..., 1], a[..., 2]


def kleurzweem(a):
    """Chromaticiteit: rood-aandeel min blauw-aandeel, plus de helderheid.

    Ongevoelig voor licht en schaduw, en dat is nodig: de rechterkant van de doos
    ligt in de schaduw, waar vaste drempels op R en B het karton en de inkt missen.
    """
    som = a.sum(-1) + 1e-6
    return (a[..., 0] - a[..., 2]) / som, som


def printmasker(a, grond):
    """Pixels die inkt zijn: wit of geel op de polo, blauw of geel op karton."""
    d, som = kleurzweem(a)
    if grond == 'polo':
        # het merk op de polo is bleekwit tot geel; alles wat niet blauwe stof is,
        # binnen het vak dat de doos en de hand al wegsnijdt, is print
        return (d > -0.25) & (som > 120) & ~kartonweren(a)
    geel = (d > 0.30) & (som > 220)
    blauw = (d < -0.15) & (som > 20)
    return blauw | geel


def grondmasker(a, grond):
    """Waar mag er geschilderd worden: alleen op de stof of op het karton."""
    d, som = kleurzweem(a)
    if grond == 'polo':
        return (d < -0.25) & (som > 45)
    return (d > 0.08) & (d < 0.35) & (som > 40)


def grootste_component(m):
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    if n == 0:
        return m
    maten = ndimage.sum(m, lab, range(1, n + 1))
    return lab == (1 + int(np.argmax(maten)))


def print_componenten(m, bereik=45, minmaat=25):
    """Het grootste blok (armen en huis) plus alles wat er vlakbij ligt: de tekstregels."""
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    if n == 0:
        return m
    maten = ndimage.sum(m, lab, range(1, n + 1))
    kern = 1 + int(np.argmax(maten))
    rand = np.zeros_like(m)
    rand[0], rand[-1], rand[:, 0], rand[:, -1] = True, True, True, True
    houd = lab == kern
    for _ in range(6):
        buurt = ndimage.binary_dilation(houd, schijf(bereik))
        groei = False
        for i in range(1, n + 1):
            if i == kern:
                continue
            deel = lab == i
            if (deel & rand).any():
                continue        # loopt het vak uit: een doos erachter, niet deze print
            if maten[i - 1] >= minmaat and not (deel & houd).any() and (deel & buurt).any():
                houd |= deel
                groei = True
        if not groei:
            break
    return houd


def schijf(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def vullen(beeld, weg, bron_ok=None):
    """Vul de gemaskeerde pixels vanuit de dichtstbijzijnde bruikbare pixel en maak het glad.

    bron_ok begrenst waar de vulling vandaan mag komen: zonder die grens haalt de
    borstprint karton van de doos ernaast naar binnen en krijgt de polo een bruine veeg.
    """
    niet = weg if bron_ok is None else (weg | ~bron_ok)
    idx = ndimage.distance_transform_edt(niet, return_distances=False, return_indices=True)
    gevuld = beeld[idx[0], idx[1]]
    glad = np.stack([ndimage.gaussian_filter(gevuld[..., k], 8) for k in range(3)], -1)
    # binnen het masker de gladde vulling, met een zachte overgang aan de rand
    w = np.clip(ndimage.gaussian_filter(weg.astype(float), 1.2), 0, 1)[..., None]
    return beeld * (1 - w) + glad * w


def logo_frames(pad):
    """Het logo als array plus de rij waar het beeldmerk ophoudt en de tekst begint."""
    im = np.asarray(Image.open(pad).convert('RGBA'), float) / 255.0
    alfa = im[..., 3]
    rij = alfa.max(1) > 0.02
    # de eerste lege rij onder het beeldmerk
    grens = im.shape[0]
    aan = False
    for y in range(im.shape[0]):
        if rij[y]:
            aan = True
        elif aan:
            grens = y
            break
    return im, grens


def warp(bron, par, vorm, mid_bron, ss=1):
    """Het logo in beeldcoordinaten leggen. par = tx, ty, log sx, log sy, hoek."""
    tx, ty, lsx, lsy, th = par
    sx, sy = np.exp(lsx), np.exp(lsy)
    h, w = vorm
    yy, xx = np.mgrid[0:h * ss, 0:w * ss].astype(float) / ss
    dx, dy = xx - tx, yy - ty
    c, s = np.cos(-th), np.sin(-th)
    u = (c * dx - s * dy) / sx + mid_bron[1]
    v = (s * dx + c * dy) / sy + mid_bron[0]
    uit = np.stack([ndimage.map_coordinates(bron[..., k], [v, u], order=1, mode='constant')
                    for k in range(bron.shape[2])], -1)
    if ss > 1:
        uit = uit.reshape(h, ss, w, ss, bron.shape[2]).mean((1, 3))
    return uit


def pas_in(alfa_bron, mid_bron, oud, mag, hoek0):
    """Zoek de affiene ligging waarbij het logo het oude merk het beste dekt."""
    ys, xs = np.nonzero(oud)
    mid = np.array([ys.mean(), xs.mean()])
    opp_oud, opp_bron = oud.sum(), (alfa_bron > 0.5).sum()
    schaal = np.sqrt(opp_oud / max(opp_bron, 1))
    start = np.array([mid[1], mid[0], np.log(schaal), np.log(schaal), np.deg2rad(hoek0)])

    def kosten(p):
        if abs(p[2] - start[2]) > 0.45 or abs(p[3] - start[3]) > 0.45:
            return 1.0
        if abs(p[3] - p[2]) > 0.34 or abs(p[4] - start[4]) > np.deg2rad(6):
            return 1.0
        a = warp(alfa_bron[..., None], p, oud.shape, mid_bron)[..., 0] > 0.5
        doorsnee = (a & oud & mag).sum()
        vereniging = ((a | oud) & mag).sum()
        return 1.0 - doorsnee / max(vereniging, 1)

    beste, bkosten = start, kosten(start)
    for dh in np.deg2rad(np.arange(-5, 5.1, 2.5)):
        for ds in (-0.12, 0.0, 0.12):
            p = start + np.array([0, 0, ds, ds, dh])
            k = kosten(p)
            if k < bkosten:
                beste, bkosten = p, k
    # patroonzoek: scipy.optimize laadt hier niet (Application Control), dit is genoeg
    stap = np.array([2.0, 2.0, 0.06, 0.06, np.deg2rad(2.0)])
    for _ in range(8):
        verbeterd = True
        while verbeterd:
            verbeterd = False
            for i in range(5):
                for teken in (1, -1):
                    p = beste.copy()
                    p[i] += teken * stap[i]
                    k = kosten(p)
                    if k < bkosten - 1e-5:
                        beste, bkosten, verbeterd = p, k, True
        stap *= 0.5
    return beste, bkosten


def inkt_winst(a, oud, grond):
    """Hoe de echte inktkleuren er in dit licht uitzien: per kleur een factor."""
    d, som = kleurzweem(a)
    geel = oud & (d > 0.30)
    winst = {}
    if grond == 'polo':
        wit = oud & (d > -0.12) & (d < 0.08)
        # hoogste waarden, niet het gemiddelde: de randpixels lopen in de stof over
        winst['wit'] = (np.percentile(a[wit], 82, axis=0) / WIT) if wit.sum() > 20 else np.ones(3)
    else:
        blauw = oud & (d < -0.15)
        winst['blauw'] = a[blauw].mean(0) / BLAUW if blauw.sum() > 20 else np.ones(3)
    winst['geel'] = a[geel].mean(0) / GEEL if geel.sum() > 20 else np.ones(3)
    return winst


def kleur_ijken(rgb, alfa, winst):
    """Elke logopixel krijgt de winst van de kleur waar hij het dichtst bij ligt."""
    uit = rgb.copy()
    ref = {'geel': GEEL / 255.0, 'blauw': BLAUW / 255.0, 'wit': WIT / 255.0}
    namen = [n for n in winst]
    afst = np.stack([np.linalg.norm(rgb - ref[n], axis=-1) for n in namen], -1)
    keuze = afst.argmin(-1)
    for i, n in enumerate(namen):
        m = (keuze == i) & (alfa > 0.02)
        uit[m] = np.clip(rgb[m] * winst[n], 0, 1)
    return uit


def verschuif(par, d):
    """Dezelfde ligging, maar gemeten vanaf een ander punt in het bronbeeld."""
    uit = par.copy()
    c, s = np.cos(par[4]), np.sin(par[4])
    sx, sy = np.exp(par[2]), np.exp(par[3])
    uit[0] += c * (d[1] * sx) - s * (d[0] * sy)
    uit[1] += s * (d[1] * sx) + c * (d[0] * sy)
    return uit


def snede_masker(vorm, snede, t, l):
    """Half vlak dat de doos en de hand grofweg buiten het werkgebied houdt.

    De fijne afwerking doet kartonweren in printmasker: de lijn loopt bewust een paar
    pixels voorbij de doosrand, anders blijft daar een reepje oude inkt op de stof staan.
    """
    if not snede:
        return np.ones(vorm, bool)
    x0, k, y0 = snede
    yy, xx = np.mgrid[0:vorm[0], 0:vorm[1]]
    return (xx + l) < x0 - k * ((yy + t) - y0)


def kartonweren(a255):
    """Kartonkleur: warm maar niet zo warm als de gele inkt."""
    d, som = kleurzweem(a255)
    return (d > 0.08) & (d < 0.28) & (som > 120)


def doe_job(vol, job):
    l, t, r, b = job['vak']
    a = vol[t:b, l:r].astype(float)
    a255 = a * 255.0
    grond = job['grond']
    binnen = snede_masker(a.shape[:2], job.get('snede'), t, l)

    # geen opening: de tweede tekstregel is maar 2 px dik en verdwijnt daar helemaal door
    oud = printmasker(a255, grond) & binnen
    oud = print_componenten(ndimage.binary_closing(oud, schijf(2)), job['bereik'], job['minmaat'])
    oud = ndimage.binary_closing(oud, schijf(2))

    vlak = (grondmasker(a255, grond) & binnen) | oud
    vlak = ndimage.binary_closing(vlak, schijf(4))
    vlak = ndimage.binary_fill_holes(vlak)
    vlak = grootste_component(vlak)
    # ruim vak voor de fit, daarna wordt het strak om oude print plus nieuw logo gelegd
    mag = vlak & ndimage.binary_dilation(oud, schijf(30))

    bron, grens = logo_frames(LOGO[job['versie']])
    if not job['tekst']:
        bron = bron.copy()
        bron[grens:, :, 3] = 0.0
    ys, xs = np.nonzero(bron[..., 3] > 0.5)
    mid_bron = np.array([ys.mean(), xs.mean()])

    # de fit gebruikt altijd het hele logo, ook als alleen het beeldmerk geplaatst wordt:
    # het oude merk heeft immers ook een tekstregel eronder
    vol_bron, vgrens = logo_frames(LOGO[job['versie']])
    ysf, xsf = np.nonzero(vol_bron[..., 3] > 0.5)
    mid_fit = np.array([ysf.mean(), xsf.mean()])
    par, kost = pas_in(vol_bron[..., 3], mid_fit, oud, mag, job['hoek'])

    # tweede slag op alleen het beeldmerk: de verzonnen tekstregels hebben andere
    # verhoudingen dan VERHUISBEDRIJF / DE REUS en trekken de fit anders scheef
    zone = np.zeros_like(vol_bron[..., 3])
    zone[:vgrens] = 1.0
    in_merk = ndimage.binary_dilation(warp(zone[..., None], par, oud.shape, mid_fit)[..., 0] > 0.5,
                                      schijf(6))
    merk_alfa = vol_bron[..., 3] * zone
    ysm, xsm = np.nonzero(merk_alfa > 0.5)
    mid_merk = np.array([ysm.mean(), xsm.mean()])
    par2, kost2 = pas_in(merk_alfa, mid_merk, oud & in_merk, mag & in_merk, np.rad2deg(par[4]))
    if kost2 < 0.62:
        par = verschuif(par2, mid_fit - mid_merk)
        kost = kost2
    # dezelfde ligging, maar gemeten vanaf het zwaartepunt van wat we echt tekenen
    par = verschuif(par, mid_bron - mid_fit)

    # weghalen: de omhullende van de oude print, en het tekstvlak eronder. Dat laatste
    # moet erbij omdat de vage tweede regel op de kleine doos te weinig kleur heeft om
    # op inkt te maskeren; het vak komt uit de ligging van het logo zelf.
    romp_print = ndimage.binary_fill_holes(ndimage.binary_closing(oud, schijf(18)))
    weg = ndimage.binary_dilation(romp_print, schijf(3))
    if job.get('oude_tekst_weg'):
        # anderhalve loghoogte: de verzonnen naamregel loopt verder door dan het
        # echte tekstblok, en blijft anders als blauwe veeg onder het merk staan
        hoog = int(vol_bron.shape[0] * 1.9)
        tekstzone = np.zeros((hoog, vol_bron.shape[1]), float)
        tekstzone[vgrens:] = 1.0
        vak = warp(tekstzone[..., None], verschuif(par, mid_fit - mid_bron), oud.shape,
                   mid_fit)[..., 0] > 0.5
        weg = weg | (ndimage.binary_dilation(vak, schijf(10)) & vlak)
    if grond == 'polo':
        # rond de borstprint is alles wat geen stof is oude inkt of de bleke rand ervan
        weg = weg | (ndimage.binary_dilation(romp_print, schijf(30)) & binnen
                     & ~grondmasker(a255, grond) & ~kartonweren(a255))
    basis = vullen(a, weg, vlak)
    rand = ndimage.binary_dilation(weg, schijf(14)) & ~weg
    halo = rand & vlak & (np.linalg.norm(a - basis, axis=-1) * 255 > job['halo'])
    weg = weg | ndimage.binary_dilation(halo, schijf(1))
    basis = vullen(a, weg, vlak)

    lum = basis @ np.array([0.2126, 0.7152, 0.0722])
    schaduw = ndimage.gaussian_filter(lum, 5)
    ijk = np.median(schaduw[oud]) if oud.sum() else schaduw.mean()
    schaduw = np.clip(schaduw / max(ijk, 1e-6), 0.55, 1.45)

    if job.get('inpassen'):
        mid_oud = np.array([np.nonzero(oud)[0].mean(), np.nonzero(oud)[1].mean()])
        for _ in range(14):
            a4 = warp(bron[..., 3:], par, oud.shape, mid_bron)[..., 0] > 0.15
            if a4.sum() and (a4 & ~vlak).sum() / a4.sum() < 0.005:
                break
            par[2] -= 0.02
            par[3] -= 0.02
            par[0] += (mid_oud[1] - par[0]) * 0.02
            par[1] += (mid_oud[0] - par[1]) * 0.02

    nieuw = warp(bron, par, oud.shape, mid_bron, ss=3)
    rgb = kleur_ijken(nieuw[..., :3], nieuw[..., 3], inkt_winst(a255, oud, grond))
    rgb = np.clip(rgb * schaduw[..., None], 0, 1)

    schilder = vlak & ndimage.binary_dilation(oud | (nieuw[..., 3] > 0.02), schijf(6))
    alfa = nieuw[..., 3] * ndimage.gaussian_filter(schilder.astype(float), 1.0)
    z = job['zacht']
    alfa = ndimage.gaussian_filter(alfa, z)
    rgb = np.stack([ndimage.gaussian_filter(rgb[..., k], z) for k in range(3)], -1)

    uit = basis * (1 - alfa[..., None]) + rgb * alfa[..., None]

    rest = a - ndimage.gaussian_filter(a, (2, 2, 0))
    ruis = np.random.default_rng(7).normal(0, max(rest[~weg].std(), 0.004), uit.shape)
    korrelvak = ((alfa > 0.15) | weg)[..., None]
    uit = np.clip(uit + ruis * korrelvak * job['korrel'], 0, 1)

    if DEBUG:
        overlay = (a * 255).astype(np.uint8).copy()
        overlay[..., 0] = np.where(oud, 255, overlay[..., 0])
        overlay[..., 1] = np.where(nieuw[..., 3] > 0.5, 255, overlay[..., 1])
        overlay[..., 2] = np.where(weg, np.minimum(overlay[..., 2] + 90, 255), overlay[..., 2] // 2)
        Image.fromarray(overlay).resize((overlay.shape[1] * 3, overlay.shape[0] * 3),
                                        Image.NEAREST).save(f'{WERK}/crops/fit-{job["naam"]}.png')
        Image.fromarray((basis * 255).astype(np.uint8)).save(f'{WERK}/crops/basis-{job["naam"]}.png')
    print(f'{job["naam"]:12s} IoU {1 - kost:.3f} (heel {1 - kost2:.3f})  hoek {np.rad2deg(par[4]):6.1f}  '
          f'schaal {np.exp(par[2]):.4f}/{np.exp(par[3]):.4f}  inkt {oud.sum()} px  weg {weg.sum()} px')
    return (t, b, l, r), uit


def main():
    vol = np.asarray(Image.open(BRON).convert('RGB'), float) / 255.0
    uit = vol.copy()
    for job in JOBS:
        (t, b, l, r), stuk = doe_job(vol, job)
        uit[t:b, l:r] = stuk
    beeld = Image.fromarray((np.clip(uit, 0, 1) * 255).round().astype(np.uint8))
    beeld.save(f'{WERK}/pogingen/opslag-gecorrigeerd.png')
    print('geschreven:', f'{WERK}/pogingen/opslag-gecorrigeerd.png')


if __name__ == '__main__':
    main()
