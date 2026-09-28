"""Naadiconen: klei-iconen op de naad tussen twee secties, als laatste kind van een sectie.

De gebruiker plaatste ze zelf met de artifact placer op 1440 (28-09-2026, ronde 3 van de tussenicoontjes, versie 2:
"dont add them yourself use the artifact placer skill and let me do it. dont show these in mobile, just for desktop
for styling. i only need the artifacts, not text"). Alleen decoratie: alt="", geen tekst, geen klikvlak.

Geen eigen sectie: de pagina zet een van haar blokken in dit blok, als
("naadiconen", {"kopij": None, "blok": naam, "opties": opties, "plek": (sectie-id, [(icoon, kant, x, y), ...])}).
html() rendert dat blok via ctx.blok en zet de iconen vlak voor de sluittag van de sectie met dat id. Zo blijven de
bestanden van de andere blokken onaangeroerd. De plaats per icoon staat in de pagina (home.py), de opmaak in
css/blok/naadiconen.css.
"""
import re

from kit import BouwFout

NAAM = "naadiconen"
CSS = True
JS = False


def _icoon(naam, kant, x, y):
    b = f"/img/clay/{naam}"
    return (f'<img class="naadicoon naadicoon--{kant}" src="{b}-240.webp" srcset="{b}-240.webp 240w, {b}-480.webp 480w" '
            f'sizes="120px" width="120" height="120" alt="" loading="lazy" decoding="async" style="--ni-x:{x}px;--ni-y:{y}px">')


def html(ctx, kopij, blok, opties, plek, **_):
    binnen = ctx.blok(blok, **opties)
    sid, iconen = plek
    begin = re.search(r'<section\b[^>]*\bid="%s"' % re.escape(sid), binnen)
    if not begin:
        raise BouwFout(f"{ctx.pagina.pad}: naadiconen vindt geen <section id=\"{sid}\"> in blok '{blok}'")
    diepte = 0
    for tag in re.finditer(r"<(/?)section\b", binnen[begin.start():]):
        diepte += -1 if tag.group(1) else 1
        if diepte == 0:
            eind = begin.start() + tag.start()
            return binnen[:eind] + "".join(_icoon(*i) for i in iconen) + binnen[eind:]
    raise BouwFout(f"{ctx.pagina.pad}: de sectie #{sid} in blok '{blok}' wordt niet gesloten")
