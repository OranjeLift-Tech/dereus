#!/usr/bin/env python3
"""Bouwt de site van Verhuisbedrijf De Reus (alleen standaardbibliotheek).

    python _werk/build.py                bouw alles en draai de bewakers
    python _werk/build.py --alleen /     bouw één pagina (plus de gedeelde bestanden)
    python _werk/build.py --serve        bouw en start http://127.0.0.1:8000
    python _werk/build.py --streng       ontbrekende kopijvelden zijn ook een fout
    python _werk/build.py --concept      ook alle conceptpagina's, in _voorbeeld/ (overzicht op /_concept/)
    python _werk/build.py --serve --poort 8001   andere poort

Zie website/BOUWPLAN.md voor de API van pagina's en blokken.
"""
import hashlib
import importlib
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
WORTEL = HIER.parent
sys.path.insert(0, str(HIER))

import config as cfg          # noqa: E402
import kit                    # noqa: E402
import navigatie              # noqa: E402
import bewakers               # noqa: E402
from kopij import BouwFout    # noqa: E402

CSS_KERN = ["css/tokens.css", "css/style.css"]


# ---------------------------------------------------------------------------
# Verkleinen
# ---------------------------------------------------------------------------
_STRING = re.compile(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')')


def css_verklein(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    delen = _STRING.split(css)
    uit = []
    for i, d in enumerate(delen):
        if i % 2:                      # een string: ongemoeid laten
            uit.append(d)
            continue
        d = re.sub(r"\s+", " ", d)
        d = re.sub(r"\s*([{};,>])\s*", r"\1", d)
        d = re.sub(r":\s+", ":", d)      # alleen na de dubbele punt: "a :hover" (spatie ervoor) is een andere selector
        d = d.replace(";}", "}")
        uit.append(d)
    css = "".join(uit).strip()
    return css


def hash_van(*teksten):
    h = hashlib.sha1()
    for t in teksten:
        h.update(t.encode("utf-8"))
    return h.hexdigest()[:10]


# ---------------------------------------------------------------------------
# Laden van blokken en pagina's
# ---------------------------------------------------------------------------
def laad_modules(map_naam):
    map_ = HIER / map_naam
    mods = []
    if not map_.exists():
        return mods
    # De map staat op het pad voor hulpmodules met een _ ervoor (zoals _e7.py). De bestanden zelf laden we
    # onder een unieke naam, zodat blok diensten.py en pagina diensten.py elkaar niet overschrijven.
    if str(map_) not in sys.path:
        sys.path.insert(0, str(map_))
    for pad in sorted(map_.glob("*.py")):
        if pad.name.startswith("_"):
            continue
        naam = f"{map_naam}_{pad.stem.replace('-', '_')}"
        spec = importlib.util.spec_from_file_location(naam, pad)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[naam] = mod
        spec.loader.exec_module(mod)
        mod.BESTAND = pad
        mods.append(mod)
    return mods


def blokken_register():
    reg = {}
    for mod in laad_modules("blokken"):
        naam = getattr(mod, "NAAM", mod.BESTAND.stem)
        if not hasattr(mod, "html"):
            raise BouwFout(f"blok {mod.BESTAND.name} heeft geen html(ctx, kopij, **opties)")
        if naam in reg:
            raise BouwFout(f"bloknaam '{naam}' komt twee keer voor ({reg[naam].BESTAND.name} en {mod.BESTAND.name})")
        reg[naam] = mod
    return reg


def paginas_lijst():
    uit = []
    for mod in laad_modules("paginas"):
        if not hasattr(mod, "PAGINA") and not hasattr(mod, "PAGINAS"):
            raise BouwFout(f"paginas/{mod.BESTAND.name} heeft geen PAGINA = Pagina(...)")
        if hasattr(mod, "PAGINA"):
            uit.append(mod.PAGINA)
        for p in getattr(mod, "PAGINAS", []):
            uit.append(p)
    uit.sort(key=lambda p: (p.pad != "/", p.pad))
    return uit


# ---------------------------------------------------------------------------
# Kopiëren van merkbestanden
# ---------------------------------------------------------------------------
def kopieer_merk():
    bron = WORTEL / cfg.LOGO_BRON
    doel = WORTEL / "img" / "logo"
    doel.mkdir(parents=True, exist_ok=True)
    for f in bron.glob("dereus-*"):
        if f.suffix in (".svg", ".ico", ".png") and (f.suffix == ".svg" or "favicon" in f.name):
            shutil.copy2(f, doel / f.name)
    fav = bron / "dereus-favicon.ico"
    if fav.exists():
        shutil.copy2(fav, WORTEL / "favicon.ico")      # browsers vragen /favicon.ico
    icdoel = WORTEL / "img" / "iconen"
    icdoel.mkdir(parents=True, exist_ok=True)
    for f in (WORTEL / "brandbook" / "assets" / "imagery").glob("icoon-*.svg"):
        shutil.copy2(f, icdoel / f.name)


# ---------------------------------------------------------------------------
# CSS en JS per pagina
# ---------------------------------------------------------------------------
class Bestanden:
    """Houdt de verkleinde CSS bij (één keer schrijven) en geeft de URL met ?v=."""

    def __init__(self):
        self.css_urls = {}
        self.js_urls = {}
        (WORTEL / "css" / "min").mkdir(parents=True, exist_ok=True)
        kern = "\n".join((WORTEL / p).read_text(encoding="utf-8") for p in CSS_KERN)
        mini = css_verklein(kern)
        (WORTEL / "css" / "min" / "site.min.css").write_text(mini, encoding="utf-8")
        self.kern_css = f"/css/min/site.min.css?v={hash_van(mini)}"
        js = (WORTEL / "js" / "site.js").read_text(encoding="utf-8")
        self.kern_js = f"/js/site.js?v={hash_van(js)}"

    def blok_css(self, naam):
        if naam in self.css_urls:
            return self.css_urls[naam]
        bron = WORTEL / "css" / "blok" / f"{naam}.css"
        url = None
        if bron.exists():
            mini = css_verklein(bron.read_text(encoding="utf-8"))
            (WORTEL / "css" / "min" / f"{naam}.min.css").write_text(mini, encoding="utf-8")
            url = f"/css/min/{naam}.min.css?v={hash_van(mini)}"
        self.css_urls[naam] = url
        return url

    def blok_js(self, naam):
        if naam in self.js_urls:
            return self.js_urls[naam]
        bron = WORTEL / "js" / "blok" / f"{naam}.js"
        url = f"/js/blok/{naam}.js?v={hash_van(bron.read_text(encoding='utf-8'))}" if bron.exists() else None
        self.js_urls[naam] = url
        return url


# ---------------------------------------------------------------------------
# Pagina bouwen
# ---------------------------------------------------------------------------
def meta_van(pagina, ctx):
    titel = pagina.titel or ctx.kopij.titel or cfg.NAAM
    beschrijving = pagina.beschrijving or ctx.kopij.beschrijving or ""
    og_titel = ctx.kopij.meta.get("og-titel", titel)
    return titel, beschrijving, og_titel


def kop_html(pagina, ctx, css, js, jsonld_html):
    titel, beschrijving, og_titel = meta_van(pagina, ctx)
    e = kit.esc
    regels = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<script>document.documentElement.className+=' js'</script>",
        f"<title>{e(titel)}</title>",
        f'<meta name="description" content="{e(beschrijving)}">',
    ]
    seo_head = None
    try:
        import seo  # dereus-e7: canonical of noindex, OG, Twitter, theme-color en favicons op één plek
        if hasattr(seo, "head"):
            seo_head = seo.head(pagina, cfg)
    except ImportError:
        pass
    if seo_head:
        regels.append(seo_head)
    elif pagina.noindex:
        regels.append('<meta name="robots" content="noindex">')
    else:
        regels.append(f'<link rel="canonical" href="{e(pagina.url)}">')
    regels += [] if seo_head else [
        f'<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{e(cfg.NAAM)}">',
        f'<meta property="og:locale" content="{cfg.LOCALE}">',
        f'<meta property="og:title" content="{e(og_titel)}">',
        f'<meta property="og:description" content="{e(beschrijving)}">',
        f'<meta property="og:url" content="{e(pagina.url)}">',
        f'<meta property="og:image" content="{e(cfg.DOMEIN + pagina.og_beeld)}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="theme-color" content="{cfg.THEMA_KLEUR}">',
        '<meta name="format-detection" content="telephone=no">',
        '<link rel="icon" href="/img/logo/dereus-favicon.ico" sizes="any">',
        '<link rel="icon" href="/img/logo/dereus-favicon-32.png" type="image/png" sizes="32x32">',
        '<link rel="apple-touch-icon" href="/img/logo/dereus-favicon-180.png">',
    ]
    regels += [
        '<link rel="preload" href="/fonts/archivo-condensed-latin.woff2" as="font" type="font/woff2" crossorigin>',
        '<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>',
    ]
    if pagina.preload_beeld:
        pb = pagina.preload_beeld
        a = " ".join(f'{k}="{e(v)}"' for k, v in pb.items())
        regels.append(f'<link rel="preload" as="image" fetchpriority="high" {a}>')
    for url in css:
        regels.append(f'<link rel="stylesheet" href="{url}">')
    for url in js:
        regels.append(f'<script src="{url}" defer></script>')
    if jsonld_html:
        regels.append(jsonld_html)
    return "\n".join(regels)


def jsonld_voor(pagina, ctx):
    try:
        import jsonld  # dereus-e7
    except ImportError:
        return ""
    graaf = jsonld.voor(pagina, ctx)
    if not graaf:
        return ""
    if hasattr(jsonld, "als_script"):
        return jsonld.als_script(graaf)
    data = json.dumps(graaf, ensure_ascii=False, separators=(",", ":")).replace("</", r"<\/")
    return f'<script type="application/ld+json">{data}</script>'


def bouw_pagina(pagina, register, bestanden, streng):
    ctx = kit.Ctx(pagina)
    ctx.register = register
    delen = []
    gebruikt = ctx.gebruikt
    for naam, opties in pagina.blokken:
        if naam not in register:
            raise BouwFout(f"{pagina.pad}: onbekend blok '{naam}' (bestaat _werk/blokken/{naam}.py?)")
        mod = register[naam]
        if "kopij_ids" in opties or ("kopij" in opties and opties["kopij"] is None):
            k = None
        else:
            kid = opties.get("kopij_id") or naam
            if kid in ctx.kopij.verborgen:
                continue                      # alleen-als: het feit is nog onbekend, het blok valt weg
            if ctx.kopij.heeft(kid):
                k = ctx.kopij.blok(kid)
            else:
                k = kit._kopij.Leeg(pagina.kopij or "", kid)
                ctx.waarschuw(f"{pagina.pad}: blok '{naam}' vindt #{kid} niet in {pagina.kopij}.md")
        schone = {k_: v for k_, v in opties.items() if k_ not in ("kopij",)}
        delen.append(mod.html(ctx, k, **schone))
        for dep in [naam] + list(getattr(mod, "AFHANKELIJK", [])):
            if dep not in gebruikt:
                gebruikt.append(dep)
    gebruikt += [d for d in ctx.extra_css if d not in gebruikt]

    # gedeelde onderdelen (na de blokken, zodat alle iconen geteld zijn)
    hdr = navigatie.header(ctx)
    ld = navigatie.lade(ctx)
    ft = navigatie.footer(ctx)
    bb = navigatie.belbalk(ctx)

    css = [bestanden.kern_css] + [u for u in (bestanden.blok_css(n) for n in gebruikt) if u]
    js = [bestanden.kern_js] + [u for u in (bestanden.blok_js(n) for n in gebruikt) if u]
    head = kop_html(pagina, ctx, css, js, jsonld_voor(pagina, ctx))
    klasse = " ".join(k for k in ["p", pagina.body_klasse, f"header-{pagina.header}"] if k)
    html = f'''<!doctype html>
<html lang="{cfg.TAAL}">
<head>
{head}
</head>
<body class="{klasse}">
<a class="skiplink" href="#inhoud">Naar de inhoud</a>
{kit.sprite(ctx.iconen)}
{hdr}
{ld}
<main id="inhoud" tabindex="-1">
{"".join(delen)}
</main>
{ft}
{bb}
</body>
</html>
'''
    if streng and ctx.waarschuwingen:
        raise BouwFout("\n".join(ctx.waarschuwingen))
    return re.sub(r"(?m)^[ \t]+$", "", html), ctx


VOORBEELD = WORTEL / "_voorbeeld"      # --concept schrijft hierheen; nooit in de deploy (.vercelignore)


def concept_balk(p):
    """Een opvallende balk bovenaan een conceptpagina, alleen in _voorbeeld/."""
    status = "staat AAN in config.PUBLICEER" if p.live else "staat UIT, niet in de deploy"
    wacht = f" Wacht op: {kit.esc(p.wacht_op)}." if p.wacht_op else ""
    return (f'<div style="position:sticky;top:0;z-index:100;background:#FFCC33;color:#0B2352;'
            f'font:700 14px/1.4 Inter,Arial,sans-serif;padding:8px 16px;text-align:center">'
            f'Concept, {status}.{wacht} <a href="/_concept/" style="color:#0B2352">Overzicht</a></div>')


def concept_overzicht(paginas):
    rijen = []
    for p in sorted((p for p in paginas if p.concept), key=lambda p: p.pad):
        feiten = ", ".join(f'{n} {"&#10003;" if kit.feit(n) not in (None, "") else "(onbekend)"}' for n in p.feiten) or "geen"
        rijen.append(f'<tr><td><a href="{p.pad}">{kit.esc(p.pad)}</a></td><td>{"aan" if p.live else "uit"}</td>'
                     f'<td>{kit.esc(p.wacht_op) or "&nbsp;"}</td><td>{feiten}</td></tr>')
    feitrijen = "".join(f'<tr><td>{kit.esc(n)}</td><td>{kit.esc(str(v)) if v not in (None, "") else "<em>onbekend</em>"}</td></tr>'
                        for n, v in getattr(cfg, "FEITEN", {}).items())
    stijl = ("body{font:16px/1.5 Inter,Arial,sans-serif;margin:40px auto;max-width:1100px;padding:0 16px;color:#0E1A33}"
             "table{border-collapse:collapse;width:100%;margin:12px 0 40px}td,th{border:1px solid #D3D7DE;padding:8px 10px;text-align:left;vertical-align:top}"
             "th{background:#F6F7F9}h1,h2{color:#1746A2}")
    return f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<title>Conceptpagina's</title><style>{stijl}</style></head><body>
<h1>Conceptpagina's</h1>
<p>Alleen lokaal (_voorbeeld/). Aanzetten: zet het pad op True in config.PUBLICEER en bouw opnieuw.</p>
<table><tr><th>Pagina</th><th>Status</th><th>Wacht op</th><th>Feiten</th></tr>{"".join(rijen) or '<tr><td colspan="4">Nog geen conceptpagina\'s.</td></tr>'}</table>
<h2>Feiten (config.FEITEN)</h2>
<table><tr><th>Naam</th><th>Waarde</th></tr>{feitrijen}</table>
<p><a href="/">Naar de home</a></p>
</body></html>'''


def bouw(alleen=None, streng=False, concept=False):
    kopieer_merk()
    register = blokken_register()
    paginas = paginas_lijst()
    if not paginas:
        raise BouwFout("geen pagina's gevonden in _werk/paginas/")
    # Welke pagina's zitten in deze build? Live: gewone pagina's en aangezette concepten. --concept: alles.
    kit.ALLE_PADEN = {p.pad for p in paginas}
    te_bouwen = paginas if concept else [p for p in paginas if p.live]
    kit.ZICHTBAAR = {p.pad for p in te_bouwen}
    uitroot = VOORBEELD if concept else WORTEL
    bestanden = Bestanden()
    uitvoer = {}
    waarschuwingen = []
    for p in te_bouwen:
        if alleen and p.pad != alleen:
            continue
        html, ctx = bouw_pagina(p, register, bestanden, streng)
        if concept and p.concept:
            html = html.replace('<a class="skiplink"', concept_balk(p) + '\n<a class="skiplink"', 1)
        doel = uitroot / p.bestand
        doel.parent.mkdir(parents=True, exist_ok=True)
        doel.write_text(html, encoding="utf-8")
        uitvoer[p.pad] = html
        waarschuwingen += ctx.waarschuwingen
        print(f"  gebouwd  {p.pad:28} -> {'_voorbeeld/' if concept else ''}{p.bestand}{'  (concept)' if p.concept else ''}")
    if concept:
        (VOORBEELD / "_concept").mkdir(parents=True, exist_ok=True)
        (VOORBEELD / "_concept" / "index.html").write_text(concept_overzicht(paginas), encoding="utf-8")
        print("  overzicht /_concept/ -> _voorbeeld/_concept/index.html")
    else:
        # Een concept dat (weer) uit staat mag geen oud bestand in de deploy-root achterlaten
        for p in paginas:
            oud = WORTEL / p.bestand
            if not p.live and oud.exists() and "data-header" in oud.read_text(encoding="utf-8", errors="ignore"):
                oud.unlink()
                print(f"  verwijderd {p.bestand} (concept staat uit)")
    if not alleen and not concept:
        try:
            import seo  # dereus-e7
            seo.schrijf(te_bouwen, cfg)
        except ImportError:
            waarschuwingen.append("seo.py ontbreekt nog: geen sitemap.xml en robots.txt")
    verborgen = kit.ALLE_PADEN - kit.ZICHTBAAR
    fouten, meer = bewakers.controleer(uitvoer, te_bouwen, WORTEL, volledig=not alleen, verborgen=verborgen)
    waarschuwingen += meer
    for w in waarschuwingen:
        print(f"  let op   {w}")
    if fouten:
        print("\nBEWAKERS: de build is afgekeurd")
        for f in fouten:
            print(f"  FOUT     {f}")
        return 1
    print(f"\nKlaar: {len(uitvoer)} pagina's, {len(waarschuwingen)} waarschuwingen.")
    return 0


def serve(poort=8000, concept=False):
    import http.server
    import functools
    root = VOORBEELD if concept else WORTEL

    class Handler(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            # --concept: eerst _voorbeeld/ (pagina's), anders de repo-root (css, js, img, fonts)
            eerst = super().translate_path(path)
            if concept and not Path(eerst).exists():
                return str(WORTEL / Path(eerst).relative_to(root))
            return eerst

        def send_error(self, code, message=None, explain=None):
            if code == 404 and (root / "404.html").exists():
                inhoud = (root / "404.html").read_bytes()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(inhoud)))
                self.end_headers()
                self.wfile.write(inhoud)
                return
            super().send_error(code, message, explain)

        def log_message(self, *a):
            pass

    handler = functools.partial(Handler, directory=str(root))
    print(f"Server op http://127.0.0.1:{poort}/{'  (concept, overzicht op /_concept/)' if concept else ''} (Ctrl+C stopt)")
    http.server.ThreadingHTTPServer(("127.0.0.1", poort), handler).serve_forever()


if __name__ == "__main__":
    args = sys.argv[1:]
    alleen = None
    if "--alleen" in args:
        alleen = args[args.index("--alleen") + 1]
    poort = int(args[args.index("--poort") + 1]) if "--poort" in args else 8000
    concept = "--concept" in args
    try:
        code = bouw(alleen=alleen, streng="--streng" in args, concept=concept)
    except BouwFout as fout:
        print(f"\nBOUWFOUT: {fout}")
        sys.exit(2)
    if "--serve" in args:
        serve(poort, concept=concept)
    sys.exit(code)
