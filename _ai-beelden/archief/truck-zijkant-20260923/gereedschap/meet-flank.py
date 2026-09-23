#!/usr/bin/env python3
"""Meet wat de flank van versie-5 zelf aan sleet heeft, zodat de belettering die kan overnemen.

Meet binnen het vlak van ronde 2, in vlakcoordinaten (u,v van 0 tot 1), dus onafhankelijk
van het perspectief:
  - korrel: hoogfrequente ruis, per kanaal
  - vuilverloop: de luminantie per band van boven naar beneden
  - vlekken: middenfrequente variatie en op welke schaal
  - streekrichting: ligt de textuur horizontaal of verticaal
"""
import sys, pathlib
import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "_ai-beelden/gereedschap"))
from importlib import import_module
mod = import_module("merk-op-doos".replace("-", "_")) if False else None
import importlib.util
spec = importlib.util.spec_from_file_location(
    "mod", pathlib.Path(__file__).resolve().parents[3] / "_ai-beelden/gereedschap/merk-op-doos.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

HOEKEN = np.array([[1465,186],[2262,345],[2257,1043],[1480,1110]], float)
beeld = np.asarray(Image.open("versie-5.png").convert("RGB"), float) / 255.0

# de flank recht trekken: 800x800 in vlakcoordinaten
N = 800
H = mod.homografie(HOEKEN)
vv, uu = np.mgrid[0:N, 0:N].astype(float)
u = (uu + 0.5) / N; v = (vv + 0.5) / N
x = H[0,0]*u + H[0,1]*v + H[0,2]; y = H[1,0]*u + H[1,1]*v + H[1,2]; w = H[2,0]*u + H[2,1]*v + H[2,2]
x, y = x/w, y/w
recht = np.stack([ndimage.map_coordinates(beeld[...,k], [y, x], order=1, mode="nearest")
                  for k in range(3)], -1)
lum = recht @ mod.LUM

print("VLAK RECHTGETROKKEN NAAR %dx%d (u,v van 0 tot 1)" % (N, N))
print("luminantie      gemiddeld %.3f   min %.3f   max %.3f" % (lum.mean(), lum.min(), lum.max()))

# 1. korrel: hoogfrequent, per kanaal, in eenheden van 0-1
rest = recht - ndimage.gaussian_filter(recht, (1.6, 1.6, 0))
print("korrel (std)    r %.4f  g %.4f  b %.4f" % tuple(rest[...,k].std() for k in range(3)))

# 2. vuilverloop: luminantie per band van boven naar beneden, geijkt op de bovenste band
banden = [lum[int(i*N/10):int((i+1)*N/10)].mean() for i in range(10)]
print("verloop v       " + "  ".join("%.3f" % (b / banden[0]) for b in banden))
print("                (1.000 = zo licht als de bovenste band; lager is donkerder/viezer)")
banden_u = [lum[:, int(i*N/10):int((i+1)*N/10)].mean() for i in range(10)]
print("verloop u       " + "  ".join("%.3f" % (b / banden_u[0]) for b in banden_u))

# 3. vlekken: middenfrequent, op drie schalen
for maat in (6, 14, 30):
    band = ndimage.gaussian_filter(lum, maat/2) - ndimage.gaussian_filter(lum, maat*2)
    print("vlekken  schaal %2d px   std %.4f   p1 %.4f   p99 %.4f"
          % (maat, band.std(), np.percentile(band, 1), np.percentile(band, 99)))

# 4. streekrichting van de middenband
band = ndimage.gaussian_filter(lum, 3) - ndimage.gaussian_filter(lum, 24)
gx = np.abs(np.gradient(band, axis=1)).mean(); gy = np.abs(np.gradient(band, axis=0)).mean()
print("streek          |dx| %.5f   |dy| %.5f   ->  %s" %
      (gx, gy, "horizontaal gestreept" if gy > gx else "verticaal gestreept"))
Image.fromarray((np.clip(recht,0,1)*255).astype(np.uint8)).save("_controle/flank-recht.png")
print("geschreven: _controle/flank-recht.png")
