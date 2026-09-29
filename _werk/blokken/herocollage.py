"""Bewegende collage achter de hero van de home, sinds 28-09-2026. Wens van de gebruiker: "i need a collage of
images with more clear movement to replicate a video feel, but without video as we dont have one", en na de mock
(website/review/hero-collage-20260928/mock/): "add the hero collage video". Goedgekeurd: beeld 2, 4, 5 en 6 van de
lijst, hier in die volgorde.

Vier beelden na elkaar, elk STAP seconden met een eigen camerabeweging; de overgang is een schuine veeg van WIS
seconden waarin het oude en het nieuwe beeld het scherm delen. De rondgang is 20 s (css/blok/herocollage.css).
De laag ligt onder .hero__waas, dus dezelfde verdonkering en hetzelfde ovaal achter de tekst als de foto ervoor.

Beeld 1 is de foto uit de headerbeeldenlijst (img/headers/manifest.json, "/"), als gewone img met dezelfde
attributen als de stilstaande foto ervoor: de LCP-kandidaten blijven dezelfde. Beeld 2 tot 4 staan in een
<template> (niet geladen, geen img in document.images); js/blok/herocollage.js zet ze pas na het load-event in de
pagina en start de beweging als alle vier gedecodeerd zijn. Tot 28-09-2026 17:30 was dat een img met alleen
data-src, maar een img zonder src is ongeldig en controle-layout.cjs zag hem als kapot beeld. Met prefers-reduced-motion of Save-Data blijft beeld 1 stil staan en worden de andere nooit opgehaald.
Alle vier hebben fetchpriority="low". Zonder die hint krijgen beeld 2 tot 4 na het inzetten prioriteit High, want ze
liggen in beeld, en rekent de gesimuleerde LCP van Lighthouse ze mee als beelden waar de LCP op wacht: mobiel 8,0 s
in plaats van 5,05 s (gemeten 29-09-2026).
De beelden maakt img/headers/maak-collage.cjs.

In hero.py: ctx.blok("herocollage", kopij=None, foto=<manifestregel>) geeft de fotolaag,
ctx.blok("herocollage", kopij=None, deel="knop") de pauzeknop. Die staat apart, want de fotolaag zit in de
aria-hidden grond van de hero en een knop moet bereikbaar zijn.
"""

NAAM = "herocollage"
CSS = True
JS = True

# Moeten gelijk blijven aan de keyframes in herocollage.css (20 s rondgang, 4 x 5 s, veeg 0,9 s).
STAP, WIS = 5, 0.9

# Per beeld: uitsnede (object-position) op het scherm en op de telefoon, het punt waar omheen geschaald wordt, en
# de camera: x en y in % van het beeld, s de schaal; a aan het begin van zijn beurt, b aan het eind.
# Beeld 1 neemt src, maten en uitsnede uit het manifest.
BEELDEN = [
    # twee verhuizers met de bank op de stoep: mee naar rechts en iets inzoomen
    {"mobiel": "42% 50%", "oorsprong": "50% 50%", "a": (2.5, 0, 1.08), "b": (-2.5, -1, 1.16)},
    # langs de verhuislift omhoog naar het open raam
    {"src": "/img/headers/home-collage-2-verhuislift.webp", "maat": (720, 540), "pos": "60% 50%", "mobiel": "68% 40%",
     "oorsprong": "50% 50%", "a": (0, -7, 1.2), "b": (-1, 7, 1.2)},
    # snel mee met de verhuiswagen
    {"src": "/img/headers/home-collage-3-wagen.webp", "maat": (1200, 847), "pos": "50% 60%", "mobiel": "28% 55%",
     "oorsprong": "50% 50%", "a": (-7, 0, 1.18), "b": (7, 0, 1.18)},
    # inzoomen op de verhuizer die met een doos naar buiten loopt
    {"src": "/img/headers/home-collage-4-uitladen.webp", "maat": (1280, 960), "pos": "60% 50%", "mobiel": "64% 50%",
     "oorsprong": "66% 58%", "a": (0, 0, 1.02), "b": (0, 0, 1.24)},
]


def _getal(v):
    return f"{round(v, 4):g}"


def _stijl(n, b, pos):
    # Beeld 1 staat bij het laden al zover in zijn beweging als de rondgang hem oppakt (WIS van STAP + WIS),
    # dus bij de start springt er niets. De andere beelden zijn dan nog onzichtbaar.
    stand = [a + (z - a) * (WIS / (STAP + WIS)) for a, z in zip(b["a"], b["b"])] if n == 0 else b["a"]
    x0, y0, s0 = b["a"]
    x1, y1, s1 = b["b"]
    xp, yp, sp = stand
    return (f"--start:{_getal(n * STAP - WIS)}s;--pos:{pos};--pos-m:{b['mobiel']};--oorsprong:{b['oorsprong']};"
            f"--x0:{_getal(x0)}%;--y0:{_getal(y0)}%;--s0:{_getal(s0)};--x1:{_getal(x1)}%;--y1:{_getal(y1)}%;--s1:{_getal(s1)};"
            f"--xp:{_getal(xp)}%;--yp:{_getal(yp)}%;--sp:{_getal(sp)}")


def html(ctx, kopij, foto=None, deel="foto", **opties):
    if deel == "knop":
        # verborgen tot de beelden spelen; aria-pressed="true" is gepauzeerd
        return ('<button class="collage__knop" type="button" aria-pressed="false" hidden>'
                '<span class="vh">Beweging pauzeren</span></button>')
    ramen = []
    for n, b in enumerate(BEELDEN):
        if n == 0:
            src, (w, h), pos = foto["src"], (foto["width"], foto["height"]), foto.get("position", "50% 50%")
        else:
            src, (w, h), pos = b["src"], b["maat"], b["pos"]
        img = f'<img src="{ctx.esc(src)}" fetchpriority="low" alt="" width="{w}" height="{h}" decoding="async">'
        # beeld 2 tot 4 in een <template>: een img zonder src is ongeldig en telt in controle-layout als kapot beeld
        ramen.append(f'<div class="collage__raam" style="{_stijl(n, b, pos)}">'
                     f'{img if n == 0 else "<template>" + img + "</template>"}</div>')
    return f'<div class="hero__foto collage" data-collage>{"".join(ramen)}</div>'
