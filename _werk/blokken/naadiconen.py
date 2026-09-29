"""Naadiconen: klei-iconen op de naad tussen twee secties, als laatste kind van een sectie.

De gebruiker plaatste ze zelf met de artifact placer op 1440 (28-09-2026, ronde 3 van de tussenicoontjes, versie 2:
"dont add them yourself use the artifact placer skill and let me do it. dont show these in mobile, just for desktop
for styling. i only need the artifacts, not text"). Alleen decoratie: alt="", geen tekst, geen klikvlak.

Geen eigen sectie: de pagina zet een van haar blokken in dit blok, als
("naadiconen", {"kopij": None, "blok": naam, "opties": opties, "plek": (sectie-id, [(icoon, kant, x, y), ...])}).
html() rendert dat blok via ctx.blok en zet de iconen vlak voor de sluittag van de sectie met dat id. Noemt plek een
derde veld, een klasse, dan komen ze als eerste kind in het eerste element met die klasse binnen die sectie
(kant "hoek": vast aan dat element, zie naadiconen.css). Zo blijven de
bestanden van de andere blokken onaangeroerd. De plaats per icoon staat in de pagina (home.py), de opmaak in
css/blok/naadiconen.css.

Sinds 29-09-2026 (/diensten/): plek mag ook een lijst van zulke tuples zijn, als een blok meer secties rendert
(dienstenpanelen geeft alle acht diensten), en een icoon mag een vijfde veld hebben, zijn dekking (anders .5).
Sinds 29-09-2026 (home, #waarom) ook een zesde, vanaf: de breedte in px vanaf waar het icoon er staat (anders 1100, zoals
alle naadiconen). Alleen breedtes uit VANAF, want elk heeft een eigen regel in naadiconen.css.
"""
import re

from kit import BouwFout

NAAM = "naadiconen"
CSS = True
JS = False

VANAF = (1160,)   # breedtes met een regel .naadicoon--vanaf-<n> in naadiconen.css


def _icoon(naam, kant, x, y, dekking=None, vanaf=None):
    b = f"/img/clay/{naam}"
    stijl = f"--ni-x:{x}px;--ni-y:{y}px" + (f";--ni-o:{dekking:g}" if dekking is not None else "")
    if vanaf is not None and vanaf not in VANAF:
        raise BouwFout(f"naadiconen: {naam} vanaf {vanaf} heeft geen regel in css/blok/naadiconen.css (wel: {VANAF})")
    extra = f" naadicoon--vanaf-{vanaf}" if vanaf is not None else ""
    return (f'<img class="naadicoon naadicoon--{kant}{extra}" src="{b}-240.webp" srcset="{b}-240.webp 240w, {b}-480.webp 480w" '
            f'sizes="120px" width="120" height="120" alt="" loading="lazy" decoding="async" style="{stijl}">')


def html(ctx, kopij, blok, opties, plek, **_):
    binnen = ctx.blok(blok, **opties)
    for p in plek if isinstance(plek, list) else [plek]:
        binnen = _plaats(ctx, binnen, blok, *p)
    return binnen


def _plaats(ctx, binnen, blok, sid, iconen, *anker):
    begin = re.search(r'<section\b[^>]*\bid="%s"' % re.escape(sid), binnen)
    if not begin:
        raise BouwFout(f"{ctx.pagina.pad}: naadiconen vindt geen <section id=\"{sid}\"> in blok '{blok}'")
    diepte = 0
    for tag in re.finditer(r"<(/?)section\b", binnen[begin.start():]):
        diepte += -1 if tag.group(1) else 1
        if diepte == 0:
            eind = begin.start() + tag.start()
            break
    else:
        raise BouwFout(f"{ctx.pagina.pad}: de sectie #{sid} in blok '{blok}' wordt niet gesloten")
    if anker:
        m = re.compile(r'<[a-z]+\b[^>]*\bclass="(?:[^"]*\s)?%s[\s"][^>]*>' % re.escape(anker[0])).search(binnen, begin.start(), eind)
        if not m:
            raise BouwFout(f"{ctx.pagina.pad}: naadiconen vindt geen .{anker[0]} in #{sid} (blok '{blok}')")
        eind = m.end()
    return binnen[:eind] + "".join(_icoon(*i) for i in iconen) + binnen[eind:]
