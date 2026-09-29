"""Lichtere beelden voor telefoons, sinds 29-09-2026. Opdracht via dereus-2f, in de woorden van de gebruiker:
"optimize for mobile". Metingen en de vergelijking oud tegen nieuw: website/review/mobiel-beelden-20260929/.

BEELDEN staat op het pad zoals een blok het aan ctx.beeld geeft (kit.py; reviews.py gebruikt kies() zelf). Het
origineel blijft staan: het is de bron van de lichtere bestanden en de grootste kandidaat in een srcset.

  licht      hetzelfde beeld op dezelfde maat, zuiniger gecodeerd. ctx.beeld zet dat bestand in src, op elke
             pagina, lui of niet.
  varianten  kleinere breedtes voor een srcset, alleen bij luie beelden, met sizes="auto, <terugval>". Chromium
             kiest dan op de breedte die het beeld werkelijk krijgt (sizes="auto" werkt alleen bij loading="lazy",
             dus een niet-lui beeld krijgt hier geen srcset). Andere browsers kiezen op de terugval: per band de
             grootste breedte die het beeld op een van zijn pagina's krijgt, gemeten van 320 tot 1920 px op 29-09-2026,
             zodat geen browser een te klein bestand kiest. Staat een beeld later ergens breder, pas dan de terugval aan.
  paginas    alleen daar krijgt het beeld de varianten; elke andere pagina houdt het origineel. Een pagina staat
             erin als het beeld er op precies een plek staat en de telefoon er minder door laadt. Staat hetzelfde
             beeld twee keer op een pagina, dan kiest elke plek een eigen breedte en laadt de pagina twee bestanden
             waar het eerst een was. Zo liep het op 29-09-2026 op de home (verhuizer-doos-deken-uit in de stapkaarten
             en het werkgebied) en op /werkwijze/ (de tijdlijn koos de 480 van het trio, de naband laadt de 700 al).
             Een nieuwe pagina krijgt dus pas varianten als iemand dat daar gemeten heeft.

Waarom niet overal een srcset: een beeld dat op de telefoon breder staat dan zijn bestand bij 1,75x vraagt (de
koppen, de collage, de dienstpanelen van /diensten/) wint er niets bij. Die zijn hooguit lichter gecodeerd.

LOS zijn bestanden die elders bij naam staan (img/headers/manifest.json), met hoe ze gemaakt zijn.

De bestanden maakt dit script, en nooit over een bestaand bestand heen:
    python _werk/beeldvarianten.py
Pillow: verkleinen met Lanczos (RGBA met voorvermenigvuldigde alfa), WebP methode 6, alfa-kwaliteit 90. Kwaliteit
per bestand gekozen op SSIM tegen het origineel (verkleind, ongecodeerd) en op het oog in de reviewpagina: q80 voor
de kleinere breedtes (SSIM 0,978 tot 0,991), q70 voor de dienstfoto's (0,972 tot 0,978 tegen het huidige bestand),
q60 voor de kop van /diensten/ onder de verdonkering. De build leest alleen de tabel en blijft standaardbibliotheek.
"""
from pathlib import Path

WORTEL = Path(__file__).resolve().parent.parent

# pad in de html: {"breedte": breedte van het origineel,
#                  "licht": (pad, kwaliteit),
#                  "varianten": {breedte: (pad, kwaliteit[, bron als dat niet het origineel is])},
#                  "terugval": sizes voor browsers zonder sizes="auto",
#                  "paginas": de pagina's (pad) waar de varianten gelden}
BEELDEN = {
    # dienstfoto's (home, /diensten/): op de telefoon 328 tot 964 px breed, dus geen kleinere breedte
    "/img/dienst-nationaal-v2.webp": {"breedte": 720, "licht": ("/img/dienst-nationaal-v2-licht.webp", 70)},
    "/img/dienst-verhuislift.webp": {"breedte": 720, "licht": ("/img/dienst-verhuislift-licht.webp", 70)},
    "/img/dienst-particulier-v2.webp": {"breedte": 720, "licht": ("/img/dienst-particulier-v2-licht.webp", 70)},
    # waarom (home): foto en uitsnede hebben dezelfde maat en kader, dus dezelfde breedtes
    "/img/verhuisdag-dragen-stoep.webp": {
        "breedte": 1400, "varianten": {900: ("/img/verhuisdag-dragen-stoep-900.webp", 80)}, "paginas": {"/"},
        "terugval": "(max-width: 400px) 436px, (max-width: 480px) 533px, (max-width: 767px) 860px, (max-width: 1100px) 1033px, 895px"},
    "/img/verhuisdag-dragen-stoep-uit.webp": {
        "breedte": 1400, "varianten": {900: ("/img/verhuisdag-dragen-stoep-uit-900.webp", 80)}, "paginas": {"/"},
        "terugval": "(max-width: 400px) 436px, (max-width: 480px) 533px, (max-width: 767px) 860px, (max-width: 1100px) 1033px, 895px"},
    # waardenblad (/over-ons/). De dienstenpanelen van /diensten/ kiezen altijd de 1080, en de dtegel op de home staat
    # alleen op het scherm, waar Chromium bij 768 px en 2x de 720 koos voor 812 px beeld.
    "/img/dienst-montage-v2-uit.webp": {
        "breedte": 1080, "varianten": {560: ("/img/dienst-montage-v2-uit-560.webp", 80), 720: ("/img/dienst-montage-v2-uit-720.webp", 80)},
        "paginas": {"/over-ons/"},
        "terugval": "(max-width: 400px) 400px, (max-width: 480px) 480px, (max-width: 767px) 773px, (max-width: 1100px) 1005px, 924px"},
    # stapkaarten (home), na-bericht (/offerte/ en de bedanktpagina's)
    "/img/contact-klantenservice-uit.webp": {
        "breedte": 1200, "varianten": {680: ("/img/contact-klantenservice-uit-680.webp", 80), 900: ("/img/contact-klantenservice-uit-900.webp", 80)},
        "terugval": "(max-width: 480px) 434px, (max-width: 767px) 503px, 594px", "paginas": {"/", "/offerte/bedankt/", "/contact/bedankt/"}},
    # werkgebied (/over-ons/). Op de home staat hij ook in de stapkaarten (twee plekken), op /contact/ alleen op het scherm.
    "/img/verhuizer-doos-deken-uit.webp": {
        "breedte": 698, "varianten": {320: ("/img/verhuizer-doos-deken-uit-320.webp", 80), 480: ("/img/verhuizer-doos-deken-uit-480.webp", 80)},
        "terugval": "(max-width: 400px) 243px, 283px", "paginas": {"/over-ons/"}},
    # stapkaarten (home). Niet in de tijdlijn van /werkwijze/: daar laadt de naband de 700 al. Uit de 1600 van
    # _werk/teambeeld.py, zoals de 700 zelf.
    "/img/team/team-hero-dozen-700.webp": {
        "breedte": 700, "varianten": {480: ("/img/team/team-hero-dozen-480.webp", 80, "/img/team/team-hero-dozen-1600.webp")},
        "terugval": "(max-width: 400px) 227px, 264px", "paginas": {"/"}},
    # reviews (home, /over-ons/; reviews.py)
    "/img/review-verhuizers.webp": {
        "breedte": 760, "varianten": {400: ("/img/review-verhuizers-400.webp", 80)},
        "terugval": "(max-width: 767px) 193px, (max-width: 1100px) 230px, 314px", "paginas": {"/", "/over-ons/"}},
    # over ons (home, /over-ons/), reviews op /diensten/ (reviews.py)
    "/img/review-verhuizers-lachend-breed.webp": {
        "breedte": 914, "varianten": {480: ("/img/review-verhuizers-lachend-breed-480.webp", 80),
                                      720: ("/img/review-verhuizers-lachend-breed-720.webp", 80)},
        "terugval": "(max-width: 400px) 342px, (max-width: 480px) 417px, (max-width: 767px) 546px, (max-width: 1100px) 559px, 664px",
        "paginas": {"/", "/over-ons/", "/diensten/"}},
}

# pad: (bron, (breedte, hoogte), kwaliteit). De bron wordt eerst in het midden op die verhouding bijgesneden,
# zoals img/headers/maak.cjs doet. De bron staat in _ai-beelden/ en gaat niet mee in git.
LOS = {
    # kop van /diensten/ (manifest), sinds 29-09-2026; was headers/diensten.webp, q84 en 176 KB
    "/img/headers/diensten-licht.webp": ("/_ai-beelden/foto/header-achtergronden/werk-straat.png", (1600, 900), 60),
}


def kies(src, lui=True, pagina=None):
    """(src, srcset, sizes) voor een img op pagina (pad, zoals "/over-ons/"). Zonder regel in de tabel: (src, None, None)."""
    regel = BEELDEN.get(src)
    if not regel:
        return src, None, None
    nieuw = regel["licht"][0] if "licht" in regel else src
    if not lui or "varianten" not in regel or pagina not in regel["paginas"]:
        return nieuw, None, None
    kandidaten = sorted([(b, v[0]) for b, v in regel["varianten"].items()] + [(regel["breedte"], nieuw)])
    return nieuw, ", ".join(f"{pad} {b}w" for b, pad in kandidaten), f"auto, {regel['terugval']}"


def _maak():
    from PIL import Image

    def schrijf(bron, doel, maat, kwaliteit, bijsnijden=False):
        uit = WORTEL / doel.lstrip("/")
        if uit.exists():
            print(f"bestaat al, overgeslagen: {doel}")
            return
        im = Image.open(WORTEL / bron.lstrip("/"))
        im.load()
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
        breedte, hoogte = maat if bijsnijden else (maat, round(im.height * maat / im.width))
        if bijsnijden:
            if im.width * hoogte > im.height * breedte:
                w = round(im.height * breedte / hoogte)
                im = im.crop(((im.width - w) // 2, 0, (im.width - w) // 2 + w, im.height))
            else:
                h = round(im.width * hoogte / breedte)
                im = im.crop((0, (im.height - h) // 2, im.width, (im.height - h) // 2 + h))
        if im.size != (breedte, hoogte):
            im = im.resize((breedte, hoogte), Image.LANCZOS)
        kw = {"quality": kwaliteit, "method": 6}
        if im.mode == "RGBA":
            kw["alpha_quality"] = 90
        im.save(uit, "WEBP", **kw)
        print(f"{doel}  {im.width}x{im.height}  {uit.stat().st_size} bytes  (q{kwaliteit}, uit {bron})")

    for src, regel in BEELDEN.items():
        if "licht" in regel:
            schrijf(src, regel["licht"][0], regel["breedte"], regel["licht"][1])
        for breedte, (pad, kwaliteit, *bron) in regel.get("varianten", {}).items():
            schrijf(bron[0] if bron else src, pad, breedte, kwaliteit)
    for doel, (bron, maat, kwaliteit) in LOS.items():
        schrijf(bron, doel, maat, kwaliteit, bijsnijden=True)


if __name__ == "__main__":
    _maak()
