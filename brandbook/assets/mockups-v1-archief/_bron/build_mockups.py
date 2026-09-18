#!/usr/bin/env python3
"""Toepassingsmockups voor het merkboek van Verhuisbedrijf De Reus.

Draaien:  python brandbook/assets/mockups/_bron/build_mockups.py
Nodig:    pip install uharfbuzz fonttools
Uitvoer:  brandbook/assets/mockups/*.svg

Elke SVG is zelfstandig: het logo staat er inline in (uit ../logo/*.svg) en alle
tekst is omgezet naar outlines in Archivo Condensed en Inter (fonts in _bron/fonts,
SIL Open Font License). De bestanden werken dus ook in een <img>-tag, zonder
externe verzoeken. Kleuren en maten staan alleen in het blok TOKENS; na een
wijziging van het logo of de tokens draai je het script opnieuw.
"""
import html
import os
import re

from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path

try:
    import uharfbuzz as hb
    from fontTools.pens.svgPathPen import SVGPathPen
    OUTLINES = True
except ImportError:  # noodgreep: gewone <text> met een systeemfontstack
    OUTLINES = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
LOGO_DIR = os.path.join(os.path.dirname(OUT), "logo")
FONT_DIR = os.path.join(HERE, "fonts")

# ---------------------------------------------------------------------------
# TOKENS  (bron: brandbook/research/color-type-system.md, versie 1.0)
# ---------------------------------------------------------------------------
KONINGSBLAUW = "#1746A2"    # --brand-primary
DIEPBLAUW = "#0B2352"       # --brand-secondary
GOUDGEEL = "#FFCC33"        # --brand-accent
INKT = "#0E1A33"            # --ink
GRAFIET = "#2E3647"         # --graphite
LEISTEEN = "#5E6675"        # --grey-600
STAALGRIJS = "#838996"      # --grey-400
ZILVERGRIJS = "#D3D7DE"     # --grey-300
MIST = "#F6F7F9"            # --off-white
WIT = "#FFFFFF"
BLAUW_50 = "#F3F7FE"
BLAUW_600 = "#123780"
CTA = GOUDGEEL              # --color-cta
CTA_TEXT = DIEPBLAUW        # --color-cta-text

# Illustratiekleuren (geen merkkleuren): banden, glas, metaal, karton
BAND = "#1C222E"
METAAL = "#262D3B"
CHROOM = "#C3CAD4"
KARTON = "#CFA36C"

FONT_DISPLAY = ("Archivo-VF.ttf", {"wdth": 75})   # Archivo Condensed
FONT_SANS = ("Inter-VF.ttf", {})
STACK = {"d": "Archivo,'Arial Narrow',Arial,sans-serif",
         "s": "Inter,'Segoe UI',Roboto,Arial,sans-serif"}

# Contactgegevens (bron: verhuisbedrijfdereus.nl, september 2026)
PHONE = "085 000 5647"
EMAIL = "info@verhuisbedrijfdereus.nl"
WEB = "www.verhuisbedrijfdereus.nl"
WEB_SHORT = "verhuisbedrijfdereus.nl"
STREET = "Lau Mazirellaan 336"
CITY = "2525 ZJ Den Haag"
NAME = "Naam Achternaam"     # plaatshouder, bewust geen echte naam
ROLE = "Verhuisadviseur"
PAYOFF = "Sterk in verhuizen. Zorgeloos geregeld."   # alleen waar het logo zonder tagline staat

LOGO_FILES = {
    "logo": ("dereus-logo.svg", None),
    "negatief": ("dereus-logo-negatief.svg", None),
    "compact": ("dereus-logo-zonder-tagline.svg", None),
    "compact-negatief": ("dereus-logo-zonder-tagline-negatief.svg", None),
    "1kleur": ("dereus-logo-1kleur-blauw.svg", None),                  # eenkleurendruk in koningsblauw
    "horizontaal": ("dereus-logo-horizontaal.svg", None),              # alleen waar de hoogte beperkt is
    "beeldmerk": ("dereus-beeldmerk.svg", None),
    "beeldmerk-negatief": ("dereus-beeldmerk-negatief.svg", None),
    "favicon": ("dereus-favicon.svg", None),
}


# ---------------------------------------------------------------------------
# Tekst als outlines
# ---------------------------------------------------------------------------
_fonts = {}


def _font(kind, weight, opsz):
    file, fixed = FONT_DISPLAY if kind == "d" else FONT_SANS
    key = (file, weight, opsz)
    if key not in _fonts:
        face = hb.Face(hb.Blob.from_file_path(os.path.join(FONT_DIR, file)))
        font = hb.Font(face)
        axes = dict(fixed, wght=weight)
        if kind == "s":
            axes["opsz"] = opsz
        font.set_variations(axes)
        _fonts[key] = (font, face.upem)
    return _fonts[key]


_glyphs = {}        # (font, gewicht, opsz, glyph) -> (id, pad), per document


def _glyph(font, key, gid):
    k = key + (gid,)
    if k not in _glyphs:
        pen = SVGPathPen(None, ntos=lambda v: "%d" % round(v))
        font.draw_glyph_with_pen(gid, pen)
        _glyphs[k] = (f"g{len(_glyphs)}", pen.getCommands())
    return _glyphs[k][0] if _glyphs[k][1] else None


def _shape(s, size, kind, weight, ls, opsz, draw=True):
    opsz = round(opsz or max(14, min(32, size)))
    font, upem = _font(kind, weight, opsz)
    buf = hb.Buffer()
    buf.add_str(s)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    k = size / upem
    extra = ls / k
    uses = []
    x = 0
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        if draw:
            gid = _glyph(font, (kind, weight, opsz), info.codepoint)
            if gid:
                uses.append(f'<use href="#{gid}" x="{round(x + pos.x_offset)}"/>')
        x += pos.x_advance + (extra if i < n - 1 else 0)
    return "".join(uses), x * k, k


def measure(s, size, font="s", weight=400, ls=0, opsz=None):
    if not OUTLINES:
        return len(s) * size * (0.46 if font == "d" else 0.55)
    return _shape(s, size, font, weight, ls, opsz, draw=False)[1]


_texts = []        # alle geprinte regels van het huidige document, voor de tekstlijst in README.md


def text(x, y, s, size, fill=INKT, font="s", weight=400, anchor="start", ls=0, opsz=None, extra=""):
    """Tekstregel op basislijn y. ls = letterspatiering in dezelfde eenheid als size."""
    _texts.append(s)
    if not OUTLINES:
        a = {"start": "start", "middle": "middle", "end": "end"}[anchor]
        return (f'<text x="{x}" y="{y}" font-family="{STACK[font]}" font-size="{size}" font-weight="{weight}" '
                f'fill="{fill}" text-anchor="{a}" letter-spacing="{ls}"{extra}>{esc(s)}</text>')
    uses, w, k = _shape(s, size, font, weight, ls, opsz)
    x0 = x - w * {"start": 0, "middle": 0.5, "end": 1}[anchor]
    return (f'<g transform="translate({x0:.2f} {y:.2f}) scale({k:.6g} {-k:.6g})" '
            f'fill="{fill}"{extra}>{uses}</g>')


def wrap(s, width, size, font="s", weight=400, opsz=None):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if cur and measure(trial, size, font, weight, 0, opsz) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


# ---------------------------------------------------------------------------
# Logo inline als <symbol>
# ---------------------------------------------------------------------------
_logo_cache = {}
_used = set()


def _load_logo(kind):
    if kind not in _logo_cache:
        file, recolor = LOGO_FILES[kind]
        path = os.path.join(LOGO_DIR, file)
        if not os.path.exists(path):
            raise SystemExit(f"Logobestand ontbreekt: {path}")
        src = open(path, encoding="utf-8").read()
        vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).split()]
        inner = re.search(r"<svg[^>]*>(.*)</svg>", src, re.S).group(1)
        inner = re.sub(r"<title[^>]*>.*?</title>|<desc[^>]*>.*?</desc>", "", inner, flags=re.S)
        inner = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{kind}_{m.group(1)}"', inner)
        inner = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{kind}_{m.group(1)})", inner)
        inner = re.sub(r"\s+", " ", inner).strip()
        for old, new in (recolor or {}).items():
            inner = re.sub(re.escape(old), new, inner, flags=re.I)
        _logo_cache[kind] = (vb, inner)
    return _logo_cache[kind]


def logo_ratio(kind):
    vb = _load_logo(kind)[0]
    return vb[2] / vb[3]


def logo(kind, x, y, w=None, h=None, ax=0.5, ay=0.5, extra=""):
    """Past het logo in het vak (x, y, w, h), met behoud van verhouding. ax/ay: 0 links/boven, 1 rechts/onder."""
    r = logo_ratio(kind)
    if w is None:
        w = h * r
    if h is None:
        h = w / r
    ww, hh = (h * r, h) if w / h > r else (w, w / r)
    _used.add(kind)
    return (f'<use href="#logo-{kind}" xlink:href="#logo-{kind}" x="{x + (w - ww) * ax:.2f}" '
            f'y="{y + (h - hh) * ay:.2f}" width="{ww:.2f}" height="{hh:.2f}"{extra}/>')


_last_logos = []


def _symbols():
    global _last_logos
    _last_logos = sorted(_used)
    out = "".join(f'<path id="{gid}" d="{d}"/>' for gid, d in _glyphs.values() if d) + "\n"
    _glyphs.clear()
    for kind in sorted(_used):
        vb, inner = _load_logo(kind)
        out += f'<symbol id="logo-{kind}" viewBox="{" ".join("%g" % v for v in vb)}">{inner}</symbol>\n'
    _used.clear()
    return out


# Het huis uit het logo, als los grafisch element
def _house():
    src = open(os.path.join(LOGO_DIR, "dereus-logo.svg"), encoding="utf-8").read()
    d = re.search(r'id="huis"[^>]*\sd="([^"]+)"', src).group(1)
    pen = BoundsPen(None)
    parse_path(d, pen)
    return d, pen.bounds


def house(x, y, w, fill):
    d, (x0, y0, x1, y1) = _house()
    k = w / (x1 - x0)
    return f'<path transform="translate({x:.2f} {y:.2f}) scale({k:.5f}) translate({-x0:.2f} {-y0:.2f})" fill="{fill}" d="{d}"/>'


def house_height(w):
    _, (x0, y0, x1, y1) = _house()
    return w * (y1 - y0) / (x1 - x0)


# ---------------------------------------------------------------------------
# Algemeen
# ---------------------------------------------------------------------------
def esc(s):
    return html.escape(s, quote=True)


def doc(w, h, title, desc, body, defs=""):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title>
<desc id="desc">{esc(desc)}</desc>
<defs>
<linearGradient id="decor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{MIST}"/><stop offset="1" stop-color="#E4E8EE"/></linearGradient>
<filter id="schaduw" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="{INKT}" flood-opacity=".16"/></filter>
<filter id="zacht" x="-10%" y="-300%" width="120%" height="700%"><feGaussianBlur stdDeviation="9"/></filter>
{_symbols()}{defs}
</defs>
{body}
</svg>
"""


# Lijniconen, 24x24 raster (Lucide, ISC-licentie)
ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "back": '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
    "reload": '<path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/>',
    "up": '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
}
STAR = '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'


def icon(name, x, y, size, color, sw=2):
    return (f'<g transform="translate({x:.2f} {y:.2f}) scale({size / 24:.4f})" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def stars(x, y, size, n=5, gap=2, color=GOUDGEEL):
    return "".join(f'<g transform="translate({x + i * (size + gap):.2f} {y:.2f}) scale({size / 24:.4f})" '
                   f'fill="{color}">{STAR}</g>' for i in range(n))


def button(x, y, label, kind, h=56, size=17, icon_name=None, icon_left=False):
    """Pilvormige knop. kind: 'cta' (goudgeel), 'blauw' (op licht), 'wit' (op blauw). Geeft (svg, breedte)."""
    fill, color = {"cta": (CTA, CTA_TEXT), "blauw": (KONINGSBLAUW, WIT), "wit": (WIT, KONINGSBLAUW)}[kind]
    pad = h * 0.5
    tw = measure(label, size, "s", 700)
    isz = size * 1.2
    gap = size * 0.5
    w = pad * 2 + tw + (isz + gap if icon_name else 0)
    base = y + h / 2 + size * 0.36
    out = f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h}" rx="{h / 2}" fill="{fill}"/>'
    if icon_name and icon_left:
        out += icon(icon_name, x + pad, y + (h - isz) / 2, isz, color, 2.2)
        out += text(x + pad + isz + gap, base, label, size, color, "s", 700)
    else:
        out += text(x + pad, base, label, size, color, "s", 700)
        if icon_name:
            out += icon(icon_name, x + pad + tw + gap, y + (h - isz) / 2, isz, color, 2.4)
    return out, w


TEXTS = {}


def write(name, content):
    for ch in (chr(0x2014), chr(0x2013)):
        assert ch not in content, f"{name} bevat een lang streepje"
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    seen = []
    for t in _texts:
        if t not in seen:
            seen.append(t)
    TEXTS[name] = (seen, list(_last_logos))
    _texts.clear()
    print(f"   {name:34s} {len(content) // 1024:5d} kB")


# ---------------------------------------------------------------------------
# 1. Verhuiswagen: bakwagen in zijaanzicht (21:9)
#    Eigen assenstelsel: grond op y = 800, wagen van x = 136 tot 1514.
# ---------------------------------------------------------------------------
TRUCK_BOX = (136, 165, 1514, 800)


def truck(uid="wagen"):
    cab = ("M492,296 L492,736 L374,736 L374,730 A84,84 0 0 0 206,730 L206,736 L158,736 Q150,736 150,728 "
           "L150,560 L156,520 L196,322 Q202,298 230,296 Z")
    bx, by, bw, bh = 504, 165, 996, 455          # opbouw
    stripe_y, band_y = 508, 520                   # gele bies en blauwe band

    def wheel(cx, cy):
        bolts = "".join(f'<circle cx="{cx + 26 * c:.1f}" cy="{cy + 26 * s:.1f}" r="3.6" fill="#6B7382"/>'
                        for c, s in ((1, 0), (.5, .866), (-.5, .866), (-1, 0), (-.5, -.866), (.5, -.866)))
        return (f'<circle cx="{cx}" cy="{cy}" r="70" fill="{BAND}"/>'
                f'<circle cx="{cx}" cy="{cy}" r="60" fill="none" stroke="#2C3444" stroke-width="3"/>'
                f'<circle cx="{cx}" cy="{cy}" r="42" fill="url(#{uid}-velg)"/>'
                f'<circle cx="{cx}" cy="{cy}" r="42" fill="none" stroke="#8A93A1" stroke-width="2"/>'
                f'<circle cx="{cx}" cy="{cy}" r="15" fill="{STAALGRIJS}"/>'
                f'<circle cx="{cx}" cy="{cy}" r="7" fill="#6B7382"/>{bolts}')

    defs = f"""
<clipPath id="{uid}-romp"><path d="{cab}"/><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6"/></clipPath>
<clipPath id="{uid}-bak"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6"/></clipPath>
<linearGradient id="{uid}-glas" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#94ABC9"/><stop offset=".55" stop-color="#4E6789"/><stop offset="1" stop-color="#2A3F62"/></linearGradient>
<linearGradient id="{uid}-wit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WIT}"/><stop offset="1" stop-color="#EEF1F5"/></linearGradient>
<linearGradient id="{uid}-spoiler" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#D9DEE6"/><stop offset="1" stop-color="#F7F8FA"/></linearGradient>
<linearGradient id="{uid}-tank" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E3E7ED"/><stop offset="1" stop-color="#A9B2BF"/></linearGradient>
<radialGradient id="{uid}-velg" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="#EEF1F5"/><stop offset="1" stop-color="#A3ACB9"/></radialGradient>
"""
    # Belettering: logo met tagline groot links, telefoon en website rechts. Verder niets.
    white_h = stripe_y - by                        # wit vlak boven de bies
    logo_h = 272
    logo_w = logo_h * logo_ratio("logo")
    clear = 0.117 * logo_w
    lx = bx + 58
    ly = by + (white_h - logo_h) / 2
    tx = lx + logo_w + 2.2 * clear
    avail = (bx + bw - 16) - 56 - tx
    ph_size = min(104, avail / measure(PHONE, 1, "s", 700))
    web_size = min(46, avail / measure(WEB_SHORT, 1, "s", 700))
    ph_base = by + white_h / 2 + 0.36 * ph_size
    web_base = band_y + (620 - band_y) / 2 + 0.36 * web_size

    g = f"""
<ellipse cx="825" cy="801" rx="720" ry="15" fill="{INKT}" opacity=".22" filter="url(#zacht)"/>
<ellipse cx="290" cy="800" rx="86" ry="7" fill="{INKT}" opacity=".35"/>
<ellipse cx="1150" cy="800" rx="86" ry="7" fill="{INKT}" opacity=".35"/>
<rect x="470" y="618" width="1032" height="30" fill="{METAAL}"/>
<rect x="516" y="648" width="146" height="62" rx="14" fill="url(#{uid}-tank)" stroke="{STAALGRIJS}" stroke-width="2"/>
<line x1="530" y1="668" x2="648" y2="668" stroke="{STAALGRIJS}" stroke-width="1.5" opacity=".6"/>
<rect x="676" y="660" width="378" height="9" rx="3" fill="{STAALGRIJS}"/>
<rect x="676" y="688" width="378" height="9" rx="3" fill="{STAALGRIJS}"/>
<rect x="702" y="648" width="8" height="50" fill="{LEISTEEN}"/><rect x="870" y="648" width="8" height="50" fill="{LEISTEEN}"/><rect x="1032" y="648" width="8" height="50" fill="{LEISTEEN}"/>
<rect x="720" y="628" width="12" height="7" rx="1.5" fill="#F5A623"/><rect x="980" y="628" width="12" height="7" rx="1.5" fill="#F5A623"/><rect x="1330" y="628" width="12" height="7" rx="1.5" fill="#F5A623"/>
<rect x="1486" y="626" width="16" height="16" rx="2" fill="#D64545"/>
<path d="M1066,730 A84,84 0 0 1 1234,730" fill="none" stroke="{METAAL}" stroke-width="14"/>
{wheel(1150, 730)}
<rect x="1392" y="646" width="104" height="30" rx="4" fill="#394152"/>
<rect x="1446" y="676" width="8" height="18" fill="{METAAL}"/>
<rect x="1420" y="692" width="84" height="11" rx="3" fill="{METAAL}"/>
<rect x="488" y="172" width="18" height="452" fill="{METAAL}"/>
<!-- opbouw -->
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6" fill="url(#{uid}-wit)"/>
<g clip-path="url(#{uid}-bak)">
  <rect x="{bx}" y="{by}" width="{bw}" height="12" fill="#E7EAEF"/>
  <rect x="{bx + bw - 16}" y="{by}" width="16" height="{bh}" fill="#E7EAEF"/>
  <rect x="{bx}" y="{by}" width="10" height="{bh}" fill="#EEF1F4"/>
</g>
<path d="M250,297 C350,294 440,252 492,176 L492,297 Z" fill="url(#{uid}-spoiler)"/>
<path d="M206,730 A84,84 0 0 1 374,730 Z" fill="{BAND}"/>
{wheel(290, 730)}
<!-- cabine -->
<path d="{cab}" fill="url(#{uid}-wit)"/>
<g clip-path="url(#{uid}-romp)">
  <rect x="120" y="{stripe_y}" width="1400" height="{band_y - stripe_y}" fill="{GOUDGEEL}"/>
  <rect x="120" y="{band_y}" width="1400" height="230" fill="{KONINGSBLAUW}"/>
</g>
<path d="{cab}" fill="none" stroke="{INKT}" stroke-opacity=".16" stroke-width="2"/>
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6" fill="none" stroke="{INKT}" stroke-opacity=".14" stroke-width="2"/>
<path d="M250,297 C350,294 440,252 492,176" fill="none" stroke="{INKT}" stroke-opacity=".14" stroke-width="2"/>
<line x1="{bx + bw - 16}" y1="{by}" x2="{bx + bw - 16}" y2="{by + bh}" stroke="{INKT}" stroke-opacity=".10" stroke-width="2"/>
<path d="M206,730 A84,84 0 0 1 374,730" fill="none" stroke="{METAAL}" stroke-width="7"/>
<!-- deur, raam, spiegel, lamp, bumper, treden -->
<path d="M220,318 L462,318 Q470,318 470,326 L470,632 Q470,640 462,640 L198,640 Q190,640 190,632 L190,466 Z" fill="none" stroke="{INKT}" stroke-opacity=".22" stroke-width="2"/>
<path d="M228,332 L450,332 Q456,332 456,338 L456,462 Q456,468 450,468 L201,468 Z" fill="url(#{uid}-glas)"/>
<path d="M262,332 L310,332 L284,468 L236,468 Z" fill="{WIT}" opacity=".13"/>
<rect x="428" y="484" width="28" height="7" rx="3.5" fill="{STAALGRIJS}"/>
{logo("beeldmerk-negatief", 330 - 60, 551, 120, 58)}
<line x1="200" y1="386" x2="158" y2="382" stroke="{METAAL}" stroke-width="6" stroke-linecap="round"/>
<rect x="136" y="346" width="24" height="98" rx="9" fill="{METAAL}"/>
<line x1="192" y1="472" x2="158" y2="468" stroke="{METAAL}" stroke-width="5" stroke-linecap="round"/>
<rect x="140" y="452" width="20" height="32" rx="7" fill="{METAAL}"/>
<path d="M150,650 L178,650 Q183,650 183,655 L183,675 Q183,680 178,680 L150,680 Z" fill="#EEF2F7" stroke="{STAALGRIJS}" stroke-width="1.5"/>
<rect x="188" y="661" width="14" height="8" rx="2" fill="#F5A623"/>
<path d="M150,698 L214,698 L206,722 L206,736 L158,736 Q150,736 150,728 Z" fill="{METAAL}"/>
<rect x="392" y="652" width="72" height="9" rx="3" fill="{METAAL}"/>
<rect x="392" y="690" width="72" height="9" rx="3" fill="{METAAL}"/>
<!-- belettering opbouw -->
{logo("logo", lx, ly, logo_w, logo_h)}
{text(tx, ph_base, PHONE, ph_size, KONINGSBLAUW, "s", 700)}
{text(tx, web_base, WEB_SHORT, web_size, WIT, "s", 700)}
"""
    return defs, g


def build_truck():
    W, H = 1750, 750
    defs, g = truck()
    x0, y0, x1, y1 = TRUCK_BOX
    s = 1.0
    tx = W / 2 - s * (x0 + x1) / 2
    ty = H / 2 - s * (y0 + y1 + 16) / 2
    body = f"""
<rect width="{W}" height="{H}" fill="url(#decor)"/>
<rect y="{ty + s * 800:.1f}" width="{W}" height="{H - ty - s * 800:.1f}" fill="#E1E5EC"/>
<g transform="translate({tx:.1f} {ty:.1f}) scale({s})">{g}</g>
"""
    write("verhuiswagen.svg", doc(
        W, H, "Verhuiswagen De Reus",
        "Zijaanzicht van een witte bakwagen. Op de opbouw het logo met tagline, het telefoonnummer "
        f"{PHONE} en de website {WEB_SHORT} in een koningsblauwe band met een goudgele bies. "
        "Op het portier het negatieve beeldmerk.", body, defs))


# ---------------------------------------------------------------------------
# 1b. Verhuiswagen, achterkant (16:10). Voor de signmaker: horizontaal logo en telefoonnummer.
#     Roldeur zonder middennaad, zodat het logo niet door een naad wordt gesneden.
# ---------------------------------------------------------------------------
def build_truck_rear():
    W, H = 1600, 1000
    ground = 900
    bx, by, bw, bh = 460, 110, 680, 650            # opbouw, zelfde verhouding band en bies als de zijkant
    post, head = 22, 28                             # hoekstijlen en bovenregel
    stripe_y = by + round(bh * 0.754)
    stripe_h = 17
    band_y = stripe_y + stripe_h
    dx0, dx1 = bx + post, bx + bw - post            # roldeur
    # belettering: horizontaal logo, daaronder het telefoonnummer op dezelfde breedte
    lw = 520
    lh = lw / logo_ratio("horizontaal")
    clear = 0.217 * lh                              # vrije ruimte horizontaal logo: 21,7 % van de hoogte
    ph_size = lw / measure(PHONE, 1, "s", 700)
    cap = 0.727 * ph_size                           # kapitaalhoogte Inter
    block = lh + 2.4 * clear + cap
    ly = by + head + ((stripe_y - by - head) - block) / 2
    lx = (dx0 + dx1 - lw) / 2
    slats = "".join(f'<line x1="{dx0}" y1="{yy}" x2="{dx1}" y2="{yy}" stroke="{INKT}" stroke-opacity=".07" stroke-width="2"/>'
                    for yy in range(by + head + 54, by + bh, 54))

    def tyre(x):
        return (f'<rect x="{x}" y="{ground - 150}" width="118" height="150" rx="22" fill="{BAND}"/>'
                + "".join(f'<line x1="{x + 10}" y1="{yy}" x2="{x + 108}" y2="{yy}" stroke="#2C3444" stroke-width="3"/>'
                          for yy in range(ground - 128, ground - 8, 20)))

    def lamp(x):
        return (f'<rect x="{x}" y="{by + bh + 22}" width="92" height="34" rx="6" fill="{METAAL}"/>'
                f'<rect x="{x + 5}" y="{by + bh + 27}" width="38" height="24" rx="3" fill="#D64545"/>'
                f'<rect x="{x + 47}" y="{by + bh + 27}" width="20" height="24" rx="3" fill="#F5A623"/>'
                f'<rect x="{x + 71}" y="{by + bh + 27}" width="16" height="24" rx="3" fill="#EEF2F7"/>')

    defs = f"""
<clipPath id="achter-bak"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8"/></clipPath>
<linearGradient id="achter-wit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WIT}"/><stop offset="1" stop-color="#EEF1F5"/></linearGradient>
"""
    body = f"""
<rect width="{W}" height="{H}" fill="url(#decor)"/>
<rect y="{ground}" width="{W}" height="{H - ground}" fill="#E1E5EC"/>
<ellipse cx="{W / 2}" cy="{ground + 2}" rx="430" ry="16" fill="{INKT}" opacity=".24" filter="url(#zacht)"/>
<!-- spiegels van de cabine, banden, chassis -->
<rect x="{bx - 58}" y="330" width="30" height="104" rx="10" fill="{METAAL}"/><rect x="{bx - 30}" y="372" width="34" height="8" fill="{METAAL}"/>
<rect x="{bx + bw + 28}" y="330" width="30" height="104" rx="10" fill="{METAAL}"/><rect x="{bx + bw - 4}" y="372" width="34" height="8" fill="{METAAL}"/>
{tyre(bx + 26)}{tyre(bx + 150)}{tyre(bx + bw - 268)}{tyre(bx + bw - 144)}
<rect x="{bx + 286}" y="{ground - 118}" width="{bw - 572}" height="64" rx="10" fill="#394152"/>
<rect x="{bx + 10}" y="{by + bh}" width="{bw - 20}" height="18" fill="{METAAL}"/>
{lamp(bx + 16)}{lamp(bx + bw - 108)}
<rect x="{bx + 6}" y="{by + bh + 62}" width="{bw - 12}" height="16" rx="4" fill="{CHROOM}" stroke="{STAALGRIJS}" stroke-width="1.5"/>
<rect x="{W / 2 - 78}" y="{by + bh + 24}" width="156" height="32" rx="4" fill="#EEF2F7" stroke="{METAAL}" stroke-width="2"/>
<rect x="{bx + 40}" y="{by + bh + 78}" width="96" height="46" fill="{METAAL}"/><rect x="{bx + bw - 136}" y="{by + bh + 78}" width="96" height="46" fill="{METAAL}"/>
<!-- opbouw met roldeur -->
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="url(#achter-wit)"/>
<g clip-path="url(#achter-bak)">
  {slats}
  <rect x="{bx}" y="{stripe_y}" width="{bw}" height="{stripe_h}" fill="{GOUDGEEL}"/>
  <rect x="{bx}" y="{band_y}" width="{bw}" height="{by + bh - band_y}" fill="{KONINGSBLAUW}"/>
  <rect x="{bx}" y="{by}" width="{post}" height="{bh}" fill="{INKT}" opacity=".06"/>
  <rect x="{dx1}" y="{by}" width="{post}" height="{bh}" fill="{INKT}" opacity=".06"/>
  <rect x="{bx}" y="{by}" width="{bw}" height="{head}" fill="{INKT}" opacity=".06"/>
</g>
<line x1="{dx0}" y1="{by + head}" x2="{dx0}" y2="{by + bh}" stroke="{INKT}" stroke-opacity=".16" stroke-width="2"/>
<line x1="{dx1}" y1="{by + head}" x2="{dx1}" y2="{by + bh}" stroke="{INKT}" stroke-opacity=".16" stroke-width="2"/>
<line x1="{dx0}" y1="{by + head}" x2="{dx1}" y2="{by + head}" stroke="{INKT}" stroke-opacity=".16" stroke-width="2"/>
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="none" stroke="{INKT}" stroke-opacity=".16" stroke-width="2"/>
<rect x="{bx + 60}" y="{by + 8}" width="26" height="12" rx="3" fill="#D64545"/><rect x="{bx + bw - 86}" y="{by + 8}" width="26" height="12" rx="3" fill="#D64545"/>
<rect x="{W / 2 - 70}" y="{by + bh - 44}" width="140" height="14" rx="7" fill="{CHROOM}" stroke="{DIEPBLAUW}" stroke-opacity=".5" stroke-width="1.5"/>
<!-- belettering -->
{logo("horizontaal", lx, ly, lw, lh)}
{text(W / 2, ly + lh + 2.4 * clear + cap, PHONE, ph_size, KONINGSBLAUW, "s", 700, "middle")}
"""
    write("verhuiswagen-achterkant.svg", doc(
        W, H, "Verhuiswagen De Reus, achterkant",
        "Achteraanzicht van de witte bakwagen met een roldeur. Op de deur het horizontale logo en daaronder, even "
        f"breed, het telefoonnummer {PHONE} in koningsblauw. Onderaan dezelfde koningsblauwe band met goudgele bies "
        "als op de zijkant.", body, defs))


# ---------------------------------------------------------------------------
# 2. Visitekaartje, 85 x 55 mm per kant (1 eenheid = 0,1 mm)
# ---------------------------------------------------------------------------
def card_front():
    lw = 420                                       # 42 mm, minimum met tagline is 40 mm
    lh = lw / logo_ratio("negatief")
    return f"""
<rect width="850" height="550" fill="{KONINGSBLAUW}"/>
{logo("negatief", (850 - lw) / 2, (528 - lh) / 2, lw, lh)}
<rect y="528" width="850" height="22" fill="{GOUDGEEL}"/>
"""


def card_back():
    rows = [("phone", PHONE, 600), ("mail", EMAIL, 400), ("globe", WEB, 400), ("pin", f"{STREET}, {CITY}", 400)]
    lines = ""
    for i, (ic, val, wt) in enumerate(rows):
        y = 262 + i * 50
        lines += icon(ic, 64, y - 21, 26, KONINGSBLAUW, 2) + text(108, y, val, 25, INKT, "s", wt, opsz=14)
    return f"""
<rect width="850" height="550" fill="{WIT}"/>
{text(62, 118, NAME, 46, KONINGSBLAUW, "d", 800)}
{text(64, 158, ROLE, 25, LEISTEEN, "s", 400, opsz=14)}
{lines}
<rect y="484" width="850" height="10" fill="{GOUDGEEL}"/>
<rect y="494" width="850" height="56" fill="{KONINGSBLAUW}"/>
<rect x="1" y="1" width="848" height="548" fill="none" stroke="{ZILVERGRIJS}" stroke-width="2"/>
"""


def build_cards():
    write("visitekaartje.svg", doc(
        1760, 550, "Visitekaartje De Reus",
        "Visitekaartje van 85 x 55 mm, voor- en achterkant naast elkaar. Voorkant: het negatieve logo op "
        "koningsblauw met een goudgele rand. Achterkant: naam, functie en contactgegevens op wit.",
        f'<g>{card_front()}</g><g transform="translate(910 0)">{card_back()}</g>'))
    write("visitekaartje-voorkant.svg", doc(
        850, 550, "Visitekaartje voorkant",
        "Voorkant van het visitekaartje (85 x 55 mm): het negatieve logo op koningsblauw.", card_front()))
    write("visitekaartje-achterkant.svg", doc(
        850, 550, "Visitekaartje achterkant",
        "Achterkant van het visitekaartje (85 x 55 mm): naam, functie en contactgegevens.", card_back()))


# ---------------------------------------------------------------------------
# 3. Briefpapier A4 (eenheden in mm) en envelop DL
# ---------------------------------------------------------------------------
PT = 0.3528
LETTER = [
    "Hartelijk dank voor uw aanvraag. Zoals besproken in ons telefoongesprek sturen wij u hierbij onze "
    "offerte voor de verhuizing van uw woning in Den Haag naar uw nieuwe woning in Delft.",
    "Wij verzorgen de complete verhuizing: het inpakken van breekbare spullen, het demonteren en monteren "
    "van meubels en het transport naar uw nieuwe adres. Waar nodig zetten wij een verhuislift in, zodat ook "
    "grote kasten via het raam naar binnen kunnen.",
    "In de bijlage vindt u de volledige offerte met een overzicht van alle werkzaamheden. Heeft u vragen of "
    f"wilt u iets aanpassen? Bel ons gerust op {PHONE} of stuur een e-mail naar {EMAIL}.",
    "Wij kijken ernaar uit om uw verhuizing zorgeloos te regelen.",
]


def letter():
    fs, lh = 10 * PT, 5.2
    small = 7.5 * PT
    o = dict(opsz=14)
    out = f'<rect width="210" height="297" fill="{WIT}"/>'
    out += logo("compact", 20, 14, 40, None, 0, 0)                  # zonder tagline: de pay-off staat in de voet
    for i, s in enumerate(["Familie De Vries", "Voorbeeldlaan 12", "2500 AA Den Haag"]):
        out += text(20, 66 + i * lh, s, fs, INKT, **o)
    for x, lab, val in ((20, "Datum", "18 september 2026"), (72, "Betreft", "Offerte voor uw verhuizing"),
                        (150, "Offertenummer", "2026 0918")):
        out += text(x, 100, lab.upper(), small, LEISTEEN, "s", 700, ls=0.08 * small, **o)
        out += text(x, 105.6, val, fs, INKT, **o)
    y = 124
    out += text(20, y, "Beste familie De Vries,", fs, INKT, **o)
    y += lh * 1.8
    for para in LETTER:
        for line in wrap(para, 168, fs, **o):
            out += text(20, y, line, fs, INKT, **o)
            y += lh
        y += lh * 0.7
    y += lh * 0.5
    out += text(20, y, "Met vriendelijke groet,", fs, INKT, **o)
    out += text(20, y + 17, NAME, fs, INKT, "s", 600, **o)
    out += text(20, y + 17 + lh, ROLE + ", Verhuisbedrijf De Reus", fs, LEISTEEN, **o)
    return out + paper_footer()


def paper_footer():
    """Voet van briefpapier en offerte: gegevens in drie kolommen, daaronder de band met de pay-off."""
    o = dict(opsz=14)
    out = ""
    cols = [[("Verhuisbedrijf De Reus", KONINGSBLAUW, 700), (STREET, GRAFIET, 400), (CITY, GRAFIET, 400)],
            [(PHONE, GRAFIET, 600), (EMAIL, GRAFIET, 400), (WEB, GRAFIET, 400)],
            [("Ma t/m za 08.00 tot 20.00 uur", GRAFIET, 400), ("Zo 09.00 tot 17.00 uur", GRAFIET, 400), ("4,9 uit 5 op Google", GRAFIET, 400)]]
    out += f'<line x1="20" y1="264" x2="190" y2="264" stroke="{ZILVERGRIJS}" stroke-width=".3"/>'
    for c, col in enumerate(cols):
        for i, (s, colr, wt) in enumerate(col):
            out += text(20 + c * 60, 270.5 + i * 3.9, s, 7.5 * PT, colr, "s", wt, **o)
    out += f'<rect y="285" width="210" height="1.2" fill="{GOUDGEEL}"/><rect y="286.2" width="210" height="10.8" fill="{KONINGSBLAUW}"/>'
    out += text(105, 292.6, PAYOFF, 8 * PT, WIT, "s", 600, "middle", **o)
    return out


def quote():
    """Offerte op A4. Voorbeeldregels zonder bedragen: de mockup doet geen prijs- of verzekeringsbeloftes."""
    fs, lh = 10 * PT, 5.2
    small = 7.5 * PT
    o = dict(opsz=14)
    out = f'<rect width="210" height="297" fill="{WIT}"/>'
    out += logo("compact", 20, 14, 40, None, 0, 0)                  # zonder tagline: de pay-off staat in de voet
    out += text(190, 30, "OFFERTE", 30 * PT, KONINGSBLAUW, "d", 800, "end", ls=0.02 * 30 * PT)
    for i, s in enumerate(["Familie De Vries", "Voorbeeldlaan 12", "2500 AA Den Haag"]):
        out += text(20, 66 + i * lh, s, fs, INKT, **o)
    for x, lab, val in ((20, "Datum", "18 september 2026"), (72, "Betreft", "Uw verhuizing"),
                        (150, "Offertenummer", "2026 0918")):
        out += text(x, 100, lab.upper(), small, LEISTEEN, "s", 700, ls=0.08 * small, **o)
        out += text(x, 105.6, val, fs, INKT, **o)
    # geen aanhef of ondertekening: de offerte is de bijlage bij de brief op het briefpapier
    # tabel: omschrijving links, bedrag rechts
    y = 120
    rh = 9
    out += f'<rect x="20" y="{y}" width="170" height="{rh}" fill="{KONINGSBLAUW}"/>'
    out += text(24, y + 5.8, "OMSCHRIJVING", small, WIT, "s", 700, ls=0.08 * small, **o)
    out += text(186, y + 5.8, "BEDRAG", small, WIT, "s", 700, "end", ls=0.08 * small, **o)
    y += rh
    rows = ["Verhuizing van adres A naar adres B", "Verhuislift", "Inpakmaterialen"]
    for i, row in enumerate(rows):
        if i % 2:
            out += f'<rect x="20" y="{y}" width="170" height="{rh}" fill="{BLAUW_50}"/>'
        out += text(24, y + 5.8, row, fs, INKT, **o) + text(186, y + 5.8, "€ 0,00", fs, INKT, "s", 400, "end", **o)
        y += rh
        out += f'<line x1="20" y1="{y}" x2="190" y2="{y}" stroke="{ZILVERGRIJS}" stroke-width=".25"/>'
    y += 3
    for lab, wt in (("Subtotaal", 400), ("Btw", 400)):
        y += 6.4
        out += text(150, y, lab, fs, GRAFIET, "s", wt, "end", **o) + text(186, y, "€ 0,00", fs, INKT, "s", wt, "end", **o)
    y += 4
    out += f'<rect x="120" y="{y}" width="70" height="10" fill="{GOUDGEEL}"/>'
    out += text(150, y + 6.4, "Totaal", fs, DIEPBLAUW, "s", 700, "end", **o)
    out += text(186, y + 6.4, "€ 0,00", fs, DIEPBLAUW, "s", 700, "end", **o)
    y += 10 + lh * 2.2
    out += text(20, y, "Deze offerte is vrijblijvend.", fs, INKT, "s", 600, **o)
    y += lh * 1.5
    for line in wrap(f"Heeft u vragen of wilt u iets aanpassen? Bel ons gerust op {PHONE} of stuur een e-mail naar {EMAIL}.", 170, fs, **o):
        out += text(20, y, line, fs, INKT, **o)
        y += lh
    # akkoordvak
    y += lh * 2.4
    out += text(20, y, "VOOR AKKOORD", small, LEISTEEN, "s", 700, ls=0.08 * small, **o)
    for i, lab in enumerate(("Naam", "Datum", "Handtekening")):
        ly = y + 9 + i * 9
        out += text(20, ly, lab, small, LEISTEEN, **o)
        out += f'<line x1="44" y1="{ly + .6}" x2="110" y2="{ly + .6}" stroke="{STAALGRIJS}" stroke-width=".25"/>'
    assert ly < 256, "offerte: akkoordvak loopt in de voet"
    return out + paper_footer()


def envelope():
    o = dict(opsz=14)
    out = f'<rect width="220" height="110" fill="{WIT}"/>'
    out += logo("compact", 14, 10, 28, None, 0, 0)                  # zonder tagline, 28 mm (minimum 25 mm)
    for i, (s, c, w) in enumerate([("Verhuisbedrijf De Reus", KONINGSBLAUW, 700), (STREET, GRAFIET, 400), (CITY, GRAFIET, 400)]):
        out += text(50, 16 + i * 3.9, s, 7.5 * PT, c, "s", w, **o)
    out += f'<rect x="20" y="50" width="90" height="38" rx="2.5" fill="#F3F5F8" stroke="{ZILVERGRIJS}" stroke-width=".4"/>'
    for i, s in enumerate(["Familie De Vries", "Voorbeeldlaan 12", "2500 AA Den Haag"]):
        out += text(27, 63 + i * 5.2, s, 10 * PT, INKT, **o)
    out += f'<rect y="101.5" width="220" height="1.2" fill="{GOUDGEEL}"/><rect y="102.7" width="220" height="7.3" fill="{KONINGSBLAUW}"/>'
    out += text(206, 107.4, WEB_SHORT, 7 * PT, WIT, "s", 600, "end", **o)
    out += f'<rect x=".15" y=".15" width="219.7" height="109.7" fill="none" stroke="{ZILVERGRIJS}" stroke-width=".3"/>'
    return out


def build_letter():
    write("briefpapier.svg", doc(
        210, 297, "Briefpapier De Reus",
        "A4-briefpapier: het logo zonder tagline linksboven, een adresvak voor een vensterenvelop, een "
        "voorbeeldofferte en in de voet de contactgegevens, openingstijden en de Google-score, met een "
        "koningsblauwe band en de pay-off.", letter()))
    write("offerte.svg", doc(
        210, 297, "Offerte De Reus",
        "Offerte op A4: het logo zonder tagline linksboven, het woord Offerte, een adresvak, een tabel met "
        "voorbeeldregels waarvan de bedragen op nul staan, de regel 'Deze offerte is vrijblijvend', een vak "
        "voor akkoord met naam, datum en handtekening, en in de voet de contactgegevens met de pay-off.", quote()))
    write("envelop.svg", doc(
        220, 110, "Envelop De Reus",
        "DL-vensterenvelop: logo zonder tagline en afzender linksboven, venster voor het adres en een "
        "koningsblauwe band met de website.", envelope()))


# ---------------------------------------------------------------------------
# 4. E-mailhandtekening (16:7)
# ---------------------------------------------------------------------------
def build_email():
    W, H = 1600, 700
    ww, wh = 1200, 580
    wx, wy = (W - ww) / 2, (H - wh) / 2
    L = wx + 56
    fs = 17
    out = f'<rect width="{W}" height="{H}" fill="url(#decor)"/>'
    out += f'<g filter="url(#schaduw)"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="16" fill="{WIT}"/></g>'
    out += f'<clipPath id="venster"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="16"/></clipPath>'
    out += (f'<g clip-path="url(#venster)"><rect x="{wx}" y="{wy}" width="{ww}" height="46" fill="#EEF1F5"/>'
            f'<line x1="{wx}" y1="{wy + 46}" x2="{wx + ww}" y2="{wy + 46}" stroke="{ZILVERGRIJS}"/></g>')
    out += "".join(f'<circle cx="{wx + 28 + i * 22}" cy="{wy + 23}" r="6.5" fill="{ZILVERGRIJS}"/>' for i in range(3))
    out += text(W / 2, wy + 29, "Bevestiging verhuisdatum", 14, LEISTEEN, "s", 500, "middle")
    y = wy + 82
    for lab, val in (("Van", f"{NAME}  <{EMAIL}>"), ("Aan", "Familie De Vries"),
                     ("Onderwerp", "Bevestiging verhuisdatum zaterdag 3 oktober")):
        out += text(L, y, lab, 15, LEISTEEN) + text(L + 104, y, val, 15, INKT, "s", 600 if lab == "Onderwerp" else 400)
        y += 26
    out += f'<line x1="{L}" y1="{y - 8}" x2="{wx + ww - 56}" y2="{y - 8}" stroke="{ZILVERGRIJS}"/>'
    y += 30
    mail = [("Beste familie De Vries,", 1.5),
            ("Hierbij bevestigen wij uw verhuizing op zaterdag 3 oktober. Ons team staat om 08.00 uur bij u voor "
             "de deur en de verhuislift is gereserveerd.", 1.5),
            ("Heeft u nog vragen? Bel of mail ons gerust.", 1.5),
            ("Met vriendelijke groet,", 1.6)]
    for para, gap in mail:
        for line in wrap(para, 840, fs):
            out += text(L, y, line, fs, INKT)
            y += 26
        y += 26 * (gap - 1)
    # handtekening
    sy = y
    lh_ = 104                                               # zonder tagline: 118 px breed (minimum 100 px)
    out += logo("compact", L, sy, None, lh_, 0, 0)
    cx = L + lh_ * logo_ratio("compact") + 30
    out += f'<rect x="{cx - 16}" y="{sy + 2}" width="2" height="{lh_ - 4}" fill="{ZILVERGRIJS}"/>'
    out += text(cx, sy + 26, NAME, 26, KONINGSBLAUW, "d", 800)
    out += text(cx, sy + 50, f"{ROLE}, Verhuisbedrijf De Reus", 15, LEISTEEN)

    def pair(x, yy, lab, val, wt=400):
        return text(x, yy, lab, 15, KONINGSBLAUW, "s", 700) + text(x + 22, yy, val, 15, INKT, "s", wt)
    col2 = cx + 250
    out += pair(cx, sy + 80, "T", PHONE, 600) + pair(col2, sy + 80, "E", EMAIL)
    out += pair(cx, sy + 102, "W", WEB) + pair(col2, sy + 102, "A", f"{STREET}, {CITY}")
    out += text(L, sy + lh_ + 34, PAYOFF, 14, KONINGSBLAUW, "s", 600)
    write("e-mailhandtekening.svg", doc(
        W, H, "E-mailhandtekening De Reus",
        "Een e-mail aan een klant met onderaan de handtekening: het logo zonder tagline, naam, functie, "
        "telefoonnummer, e-mailadres, website en adres, en als slotregel de pay-off.", out))


# ---------------------------------------------------------------------------
# 5. Websiteheader (16:7): servicebalk, header en hero met twee knoppen
# ---------------------------------------------------------------------------
# Hoofdmenu volgens sitemap/SITEMAP.md versie 1.2, hoofdstuk 6: (label, heeft een uitklapmenu)
MENU = (("Diensten", True), ("Kosten", False), ("Werkwijze", False), ("Over ons", True), ("Contact", False))
EYEBROW = "Verhuisbedrijf in Den Haag"          # de H1 van de home in de sitemap; de kop eronder is de visuele kop


def build_web():
    W, H = 1600, 700
    bx, by, bw = 48, 28, 1504
    L, R = 120, 1480
    tdefs, tg = truck("webwagen")
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="url(#decor)"/>')
    o.append(f'<g filter="url(#schaduw)"><rect x="{bx}" y="{by}" width="{bw}" height="{H}" rx="14" fill="{WIT}"/></g>')
    o.append(f'<clipPath id="venster"><rect x="{bx}" y="{by}" width="{bw}" height="{H}" rx="14"/></clipPath><g clip-path="url(#venster)">')
    # browserbalk
    o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="40" fill="#E6E9EE"/>')
    o.append("".join(f'<circle cx="{bx + 28 + i * 22}" cy="{by + 20}" r="6" fill="#C5CCD6"/>' for i in range(3)))
    o.append(f'<path d="M148,{by + 40} L148,{by + 16} Q148,{by + 8} 156,{by + 8} L422,{by + 8} Q430,{by + 8} 430,{by + 16} L430,{by + 40} Z" fill="{WIT}"/>')
    o.append(logo("favicon", 164, by + 15, 18, 18))
    o.append(text(192, by + 29, "Verhuisbedrijf De Reus", 13, INKT, "s", 500))
    o.append(f'<rect x="{bx}" y="{by + 40}" width="{bw}" height="40" fill="{WIT}"/>')
    o.append(icon("back", 70, by + 50, 20, LEISTEEN) + icon("arrow", 100, by + 50, 20, ZILVERGRIJS) + icon("reload", 132, by + 51, 18, LEISTEEN))
    o.append(f'<rect x="170" y="{by + 46}" width="720" height="28" rx="14" fill="#F0F2F5"/>')
    o.append(icon("lock", 184, by + 53, 14, LEISTEEN) + text(206, by + 65, WEB_SHORT, 14, GRAFIET))
    o.append(f'<line x1="{bx}" y1="{by + 80}" x2="{bx + bw}" y2="{by + 80}" stroke="{ZILVERGRIJS}"/>')
    # topbalk: telefoon, e-mail en Google-score (sitemap/SITEMAP.md versie 1.2, hoofdstuk 6)
    y = by + 80
    o.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="34" fill="{DIEPBLAUW}"/>')
    o.append(icon("phone", L, y + 9, 16, GOUDGEEL) + text(L + 24, y + 22, PHONE, 14, WIT, "s", 600))
    mx = L + 24 + measure(PHONE, 14, "s", 600) + 32
    o.append(icon("mail", mx, y + 9, 16, GOUDGEEL) + text(mx + 24, y + 22, EMAIL, 14, WIT))
    score = "4,9 uit 5 op Google"
    sw = measure(score, 14, "s", 600)
    o.append(stars(R - sw - 10 - 5 * 16, y + 9, 14) + text(R, y + 22, score, 14, WIT, "s", 600, "end"))
    # header (logo zonder tagline, 102 px breed)
    y += 34
    hh = 116
    o.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{hh}" fill="{WIT}"/>')
    o.append(f'<line x1="{bx}" y1="{y + hh}" x2="{bx + bw}" y2="{y + hh}" stroke="{ZILVERGRIJS}"/>')
    o.append(logo("compact", L, y + 13, None, 90, 0, 0.5))
    # hoofdmenu: alleen het hoogste niveau; een pijltje bij de items met een uitklapmenu
    _, cw = button(0, 0, "Offerte aanvragen", "cta", h=46, size=15)
    hb, _ = button(R - cw, y + (hh - 46) / 2, "Offerte aanvragen", "cta", h=46, size=15)
    o.append(hb)
    gap, chev = 34, 20
    widths = [measure(lab, 16, "s", 600) + (chev if drop else 0) for lab, drop in MENU]
    nx = R - cw - 48 - sum(widths) - gap * (len(MENU) - 1)
    for (lab, drop), mw in zip(MENU, widths):
        o.append(text(nx, y + hh / 2 + 6, lab, 16, INKT, "s", 600))
        if drop:
            o.append(icon("chevron", nx + mw - 16, y + hh / 2 - 8, 16, LEISTEEN, 2.4))
        nx += mw + gap
    # hero
    y += hh
    o.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{H - y}" fill="{KONINGSBLAUW}"/>')
    hw = 560
    o.append(house(1210 - hw / 2, y + 44, hw, BLAUW_600))
    s = 0.42
    o.append(f'<g transform="translate({1236 - s * 825:.1f} {688 - s * 800:.1f}) scale({s})">{tg}</g>')
    o.append(text(L, y + 50, EYEBROW, 17, GOUDGEEL, "s", 700, ls=0.2))
    o.append(text(L - 2, y + 112, "De betrouwbare keuze voor", 56, WIT, "d", 800))
    o.append(text(L - 2, y + 171, "een zorgeloze verhuizing", 56, WIT, "d", 800))
    ly = y + 218
    for line in wrap("Particulier of zakelijk, binnen Nederland of naar het buitenland: wij verhuizen het.", 600, 20):
        o.append(text(L, ly, line, 20, WIT, extra=' opacity=".92"'))
        ly += 30
    b1, w1 = button(L, ly + 14, "Offerte aanvragen", "cta", icon_name="arrow")
    b2, _ = button(L + w1 + 16, ly + 14, "Bel ons", "wit", icon_name="phone", icon_left=True)
    o.append(b1 + b2)
    cx = L
    for lab in ("Vrijblijvende offerte", "Particulier en zakelijk", "7 dagen per week bereikbaar"):
        cy = ly + 124
        o.append(f'<circle cx="{cx + 11}" cy="{cy - 5}" r="11" fill="{GOUDGEEL}"/>' + icon("check", cx + 4, cy - 12, 14, DIEPBLAUW, 3))
        o.append(text(cx + 30, cy, lab, 16, WIT, "s", 600))
        cx += 30 + measure(lab, 16, "s", 600) + 36
    o.append("</g>")
    write("website-header.svg", doc(
        W, H, "Websiteheader De Reus",
        "Bovenkant van de nieuwe website in een browservenster: een diepblauwe topbalk met telefoonnummer, e-mailadres en "
        "de Google-score, een witte header met logo, het menu Diensten, Kosten, Werkwijze, Over ons en Contact "
        "en de knop 'Offerte aanvragen', en een koningsblauwe hero met de regel 'Verhuisbedrijf in Den Haag' en de kop "
        "'De betrouwbare keuze voor een zorgeloze verhuizing', een goudgele primaire knop 'Offerte aanvragen' "
        "en een witte secundaire knop 'Bel ons'.", "".join(o), tdefs))


# ---------------------------------------------------------------------------
# 6. Social media: post en avatar (1:1)
# ---------------------------------------------------------------------------
def build_social():
    S = 1080
    o = [f'<rect width="{S}" height="{S}" fill="{KONINGSBLAUW}"/>']
    hw = 600
    o.append(house(S - hw + 70, S - house_height(hw) + 60, hw, DIEPBLAUW))
    # campagneregel A uit content/copy.md; daarom het logo zonder tagline (een slogan per vlak)
    o.append(logo("compact-negatief", 80, 80, 200, None, 0, 0))
    y = 432
    for i, (line, col) in enumerate((("Het zware", WIT), ("werk,", WIT), ("met zorg", GOUDGEEL), ("gedaan.", GOUDGEEL))):
        o.append(text(76, y + i * 116, line, 124, col, "d", 800))
    b, _ = button(80, 870, "Offerte aanvragen", "cta", h=76, size=28, icon_name="arrow")
    o.append(b)
    o.append(text(80, 1016, f"{WEB_SHORT}  ·  {PHONE}", 24, WIT, "s", 600))
    write("social-post.svg", doc(
        S, S, "Social media post De Reus",
        "Vierkante post van 1080 x 1080 pixels op koningsblauw: het negatieve logo zonder tagline, de campagneregel "
        "'Het zware werk, met zorg gedaan.' in wit en goudgeel, een goudgele knop 'Offerte aanvragen' en de website en het "
        "telefoonnummer. Rechtsonder het huis uit het logo in diepblauw.", "".join(o)))
    mw = 700                                               # beeldmerk past ruim binnen de ronde uitsnede
    mh = mw / logo_ratio("beeldmerk-negatief")
    av = f'<rect width="{S}" height="{S}" fill="{KONINGSBLAUW}"/>' + logo("beeldmerk-negatief", (S - mw) / 2, (S - mh) / 2 + 10, mw, mh)
    write("avatar.svg", doc(
        S, S, "Profielfoto De Reus",
        "Profielfoto van 1080 x 1080 pixels: het negatieve beeldmerk, witte armen en een goudgeel huis, op "
        "koningsblauw. Past binnen een ronde uitsnede.", av))


# ---------------------------------------------------------------------------
# 7. Verhuisdoos: karton, eenkleurig bedrukt in koningsblauw
# ---------------------------------------------------------------------------
def mix(c1, t, c2):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] * t + b[i] * (1 - t)) for i in range(3))


def moving_box(x0, y0, w, h, depth, s=1.0):
    dx, dy = depth * 0.74, -depth * 0.44
    x1, y1 = x0 + w, y0 + h
    front = f"M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} Z"
    side = f"M{x1},{y0} L{x1 + dx},{y0 + dy} L{x1 + dx},{y1 + dy} L{x1},{y1} Z"
    top = f"M{x0},{y0} L{x1},{y0} L{x1 + dx},{y0 + dy} L{x0 + dx},{y0 + dy} Z"
    a, b = (x0 + 0.43 * dx, y0 + 0.43 * dy), (x0 + 0.57 * dx, y0 + 0.57 * dy)
    tape_top = f"M{a[0]},{a[1]} L{a[0] + w},{a[1]} L{b[0] + w},{b[1]} L{b[0]},{b[1]} Z"
    seam = (x0 + 0.5 * dx, y0 + 0.5 * dy)
    m = f"matrix({dx / depth:.4f} {dy / depth:.4f} 0 1 {x1} {y0})"   # zijvlak: u = diepte, v = hoogte
    fs = 19 * s
    u0 = depth * 0.12
    lab = dict(font="s", weight=700, ls=0.08 * fs, opsz=14)
    fields = (
        icon("up", u0 - 4 * s, h * 0.21, 34 * s, KONINGSBLAUW, 2.8) + icon("up", u0 + 24 * s, h * 0.21, 34 * s, KONINGSBLAUW, 2.8)
        + text(u0, h * 0.21 + 64 * s, "DEZE KANT BOVEN", fs, KONINGSBLAUW, **lab)
        + text(u0, h * 0.49, "KAMER", fs, KONINGSBLAUW, **lab)
        + f'<line x1="{u0}" y1="{h * 0.49 + 36 * s}" x2="{depth * 0.9}" y2="{h * 0.49 + 36 * s}" stroke="{KONINGSBLAUW}" stroke-width="{2 * s}"/>'
        + text(u0, h * 0.67, "INHOUD", fs, KONINGSBLAUW, **lab)
        + f'<line x1="{u0}" y1="{h * 0.67 + 36 * s}" x2="{depth * 0.9}" y2="{h * 0.67 + 36 * s}" stroke="{KONINGSBLAUW}" stroke-width="{2 * s}"/>'
        + f'<rect x="{u0}" y="{h * 0.86}" width="{22 * s}" height="{22 * s}" fill="none" stroke="{KONINGSBLAUW}" stroke-width="{2.4 * s}"/>'
        + text(u0 + 34 * s, h * 0.86 + 19 * s, "BREEKBAAR", fs, KONINGSBLAUW, **lab))
    k_top, k_side = mix(KARTON, 0.78, WIT), mix(KARTON, 0.8, INKT)
    lw = w * 0.52
    # telefoonnummer minstens 1,2x vrije ruimte (11,7 % van de logobreedte) onder het logo
    ph = 40 * s
    ph_base = max(h * 0.86, h * 0.08 + lw / logo_ratio("1kleur") + 1.2 * 0.117 * lw + 0.727 * ph)
    return f"""
<ellipse cx="{x0 + w / 2 + dx / 2}" cy="{y1 + 2}" rx="{w / 2 + dx / 2 + 30}" ry="{13 * s}" fill="{INKT}" opacity=".24" filter="url(#zacht)"/>
<path d="{front}" fill="{KARTON}"/>
<path d="{side}" fill="{k_side}"/>
<path d="{top}" fill="{k_top}"/>
<line x1="{seam[0]}" y1="{seam[1]}" x2="{seam[0] + w}" y2="{seam[1]}" stroke="{k_side}" stroke-width="{2 * s}"/>
<path d="{tape_top}" fill="{GOUDGEEL}"/>
<g transform="{m}"><rect x="{depth * 0.43}" y="0" width="{depth * 0.14}" height="{h * 0.2}" fill="{GOUDGEEL}"/>
<g opacity=".94">{fields}</g></g>
<g opacity=".94">
{logo("1kleur", x0 + (w - lw) / 2, y0 + h * 0.08, lw, None, 0.5, 0)}
{text(x0 + w / 2, y0 + ph_base, PHONE, ph, KONINGSBLAUW, "s", 700, "middle")}
</g>
<path d="{front}" fill="none" stroke="{k_side}" stroke-width="1.5"/>
"""


def build_box():
    body = (f'<rect width="1600" height="1000" fill="url(#decor)"/>'
            + moving_box(190, 330, 560, 460, 310) + moving_box(1000, 546, 380, 300, 210, 0.68))
    write("verhuisdoos.svg", doc(
        1600, 1000, "Verhuisdoos De Reus",
        "Twee kartonnen verhuisdozen, eenkleurig bedrukt in koningsblauw: op de voorkant het logo en het "
        "telefoonnummer, op de zijkant 'Deze kant boven' en invulvakken voor kamer en inhoud. Dichtgeplakt met "
        "goudgele tape.", body))


# ---------------------------------------------------------------------------
# 8. Werkkleding: polo voor- en achterkant
# ---------------------------------------------------------------------------
def polo(cx, top, sc, back, uid):
    def P(x, y):
        return f"{cx + x * sc:.1f},{top + y * sc:.1f}"
    shade = mix(KONINGSBLAUW, 0.78, INKT)
    body = (f"M{P(-74, 0)} L{P(-206, 40)} Q{P(-262, 70)} {P(-318, 190)} L{P(-262, 230)} L{P(-196, 196)} "
            f"L{P(-204, 636)} Q{P(0, 652)} {P(204, 636)} L{P(196, 196)} L{P(262, 230)} L{P(318, 190)} "
            f"Q{P(262, 70)} {P(206, 40)} L{P(74, 0)} Q{P(0, 20)} {P(-74, 0)} Z")
    cuffs = "".join(f'<path d="M{P(f * 318, 190)} L{P(f * 262, 230)} L{P(f * 255, 219)} L{P(f * 311, 179)} Z" fill="{GOUDGEEL}"/>' for f in (-1, 1))
    seams = (f'<path d="M{P(-196, 196)} Q{P(-214, 110)} {P(-206, 40)} M{P(196, 196)} Q{P(214, 110)} {P(206, 40)}" '
             f'fill="none" stroke="{shade}" stroke-width="{2 * sc}" opacity=".8"/>'
             f'<path d="M{P(-200, 604)} Q{P(0, 620)} {P(200, 604)}" fill="none" stroke="{shade}" '
             f'stroke-width="{2 * sc}" stroke-dasharray="{6 * sc} {5 * sc}" opacity=".8"/>')
    if back:
        collar = (f'<path d="M{P(-80, -2)} Q{P(0, 24)} {P(80, -2)} L{P(86, 28)} Q{P(0, 60)} {P(-86, 28)} Z" fill="{KONINGSBLAUW}" stroke="{shade}" stroke-width="{1.5 * sc}"/>'
                  f'<path d="M{P(-85, 24)} Q{P(0, 55)} {P(85, 24)}" fill="none" stroke="{GOUDGEEL}" stroke-width="{5 * sc}"/>'
                  f'<path d="M{P(-206, 40)} Q{P(0, 100)} {P(206, 40)}" fill="none" stroke="{shade}" stroke-width="{2 * sc}" opacity=".6"/>')
        detail = logo("negatief", cx - 150 * sc, top + 112 * sc, 300 * sc, None, 0.5, 0)
    else:
        collar = (f'<path d="M{P(-72, 4)} Q{P(0, -16)} {P(72, 4)} L{P(64, 16)} Q{P(0, 0)} {P(-64, 16)} Z" fill="{shade}"/>'
                  f'<path d="M{P(-64, 16)} Q{P(0, 0)} {P(64, 16)} L{P(0, 64)} Z" fill="{mix(KONINGSBLAUW, 0.55, INKT)}"/>'
                  + "".join(f'<path d="M{P(f * 74, 0)} L{P(f * 104, 94)} Q{P(f * 60, 92)} {P(f * 20, 76)} L{P(0, 62)} Z" fill="{KONINGSBLAUW}" stroke="{shade}" stroke-width="{1.5 * sc}"/>'
                            f'<path d="M{P(f * 100, 87)} Q{P(f * 60, 85)} {P(f * 24, 71)}" fill="none" stroke="{GOUDGEEL}" stroke-width="{4 * sc}"/>' for f in (-1, 1)))
        detail = (f'<rect x="{cx - 17 * sc:.1f}" y="{top + 66 * sc:.1f}" width="{34 * sc:.1f}" height="{130 * sc:.1f}" fill="none" stroke="{shade}" stroke-width="{2 * sc}"/>'
                  + "".join(f'<circle cx="{cx}" cy="{top + yy * sc:.1f}" r="{5 * sc:.1f}" fill="{WIT}" opacity=".9"/>' for yy in (98, 140, 178))
                  + logo("negatief", cx + 78 * sc, top + 150 * sc, 80 * sc, None))      # borstlogo 80 mm
    grad = (f'<linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{shade}"/>'
            f'<stop offset=".2" stop-color="{KONINGSBLAUW}"/><stop offset=".8" stop-color="{KONINGSBLAUW}"/>'
            f'<stop offset="1" stop-color="{shade}"/></linearGradient>')
    return grad, f'<g filter="url(#schaduw)"><path d="{body}" fill="url(#{uid})"/></g>{cuffs}{seams}{collar}{detail}'


def build_polo():
    g1, front = polo(390, 190, 0.8, False, "polo-voor")
    g2, back = polo(930, 190, 0.8, True, "polo-achter")
    cx, cy, r = 1370, 460, 160
    lw = 196
    detail = (f'<clipPath id="zoom"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
              f'<g filter="url(#schaduw)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="{KONINGSBLAUW}"/></g>'
              f'<g clip-path="url(#zoom)">{logo("negatief", cx - lw / 2, cy - lw / 2 / logo_ratio("negatief"), lw)}</g>'
              f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{WIT}" stroke-width="6"/>')
    lab = ""
    for x, t1, t2, y in ((390, "Voorkant", "Borstlogo links, 80 mm breed", 790),
                         (930, "Achterkant", "Rugprint, 280 mm breed", 790),
                         (cx, "Detail borstlogo", "Negatief logo op koningsblauw", 690)):
        lab += text(x, y, t1, 22, INKT, "s", 700, "middle") + text(x, y + 30, t2, 17, LEISTEEN, "s", 400, "middle")
    body = f'<rect width="1600" height="1000" fill="url(#decor)"/>' + front + back + detail + lab
    write("werkkleding.svg", doc(
        1600, 1000, "Werkkleding De Reus",
        "Poloshirt in koningsblauw met goudgele kraagbies en mouwboorden. Voorkant met het negatieve logo op de "
        "linkerborst, achterkant met een grote rugprint en een uitvergroting van het borstlogo.", body, g1 + g2))


LOGO_LABEL = {
    "logo": "dereus-logo (met tagline)",
    "negatief": "dereus-logo-negatief (met tagline)",
    "compact": "dereus-logo-zonder-tagline",
    "compact-negatief": "dereus-logo-zonder-tagline-negatief",
    "1kleur": "dereus-logo-1kleur-blauw (met tagline)",
    "horizontaal": "dereus-logo-horizontaal",
    "beeldmerk": "dereus-beeldmerk",
    "beeldmerk-negatief": "dereus-beeldmerk-negatief",
    "favicon": "dereus-favicon",
}


def update_readme():
    """Schrijft de lijst met alle geprinte teksten per mockup in README.md, tussen de markeringen."""
    path = os.path.join(OUT, "README.md")
    lines = ["<!-- teksten:start (gegenereerd door _bron/build_mockups.py, niet met de hand aanpassen) -->", ""]
    for name, (texts, logos) in TEXTS.items():
        lines.append(f"**{name}**  ")
        lines.append("Logo: " + (", ".join(LOGO_LABEL[k] for k in logos) if logos else "geen"))
        lines.append("")
        lines += [f"- {t.strip()}" for t in texts]
        lines.append("")
    lines.append("<!-- teksten:end -->")
    src = open(path, encoding="utf-8").read()
    src = re.sub(r"<!-- teksten:start.*?<!-- teksten:end -->", lambda m: "\n".join(lines), src, flags=re.S)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(src)


if __name__ == "__main__":
    print("Mockups naar", OUT, "" if OUTLINES else "(LET OP: tekst niet als outlines, uharfbuzz ontbreekt)")
    build_truck()
    build_truck_rear()
    build_cards()
    build_letter()
    build_email()
    build_web()
    build_social()
    build_box()
    build_polo()
    update_readme()
