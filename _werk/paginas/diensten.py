"""/diensten/: kop met ankerchips, acht diensten, reviews (variant A, zoals de home) en het grote offerteformulier
van de home (blok aanvraag)."""
import kopij as _kopij
from kit import Pagina

DIENSTEN = ["particulier", "zakelijk", "nationaal", "internationaal", "verhuislift", "opslag", "montage", "woningontruiming"]


def _chips():
    """De chiptekst is het veld label van elk dienstblok (anders de kop). Het derde deel is de dienstsleutel: elke
    chip krijgt het Solar-ikoon van zijn dienst (28-09-2026, de gebruiker: "nav in diensten, use different icons for
    each section, use the small icons, not the clay ones.")."""
    doc = _kopij.document("diensten")
    return [(doc.blok(d).veld("label") or doc.blok(d).kop, f"#{d}", d) for d in DIENSTEN if doc.heeft(d)]


# Klei-iconen in twee dienstsecties, alleen vanaf 1100 px (blok naadiconen, zoals op de home). De gebruiker plaatste
# ze zelf met de artifact placer op 1440 (export 29-09-2026). Per icoon (naam, kant, x, y, dekking): x in px vanaf die
# kant van de pagina, y vanaf de bovenkant van de sectie, beide omgerekend uit de procenten van de export op 1440
# (secties 835, 939 en 707 hoog). De dekking is die uit de export; zonder vijfde veld wordt het .5, de vaste regel
# voor placer-iconen ("on the added artifacts from the artifact-placer, make them all 50% opacity").
# Het formulier boven #zakelijk ("formulier", links, 63, -12, .48) is weg sinds 29-09-2026, de gebruiker: "remove the
# clipboard icon"; het hield de ruimte boven die kaart groot (dienstenpanelen.css, "ruimte rond 02, 04 en 06").
NAADICONEN = [
    ("nationaal", [("dozen", "links", 55, 33, .61)]),
    ("internationaal", [("vakman", "rechts", 60, 41, .55)]),
]


PAGINA = Pagina(
    pad="/diensten/",
    kopij="diensten",
    header="transparant",
    body_klasse="p-diensten",
    extra_css=("reviews-ster",),   # de 3D-ster op de uitgelichte review
    blokken=[
        ("kop", {"chips": _chips()}),
        ("naadiconen", {"kopij": None, "blok": "dienstenpanelen", "opties": {"kopij_ids": DIENSTEN}, "plek": NAADICONEN}),
        ("reviews", {"sectie": "wit"}),                   # variant A met de ploeg achter het scorepaneel (28-09-2026)
        # De actielijn van de home, met dezelfde kopij (home.md, #cijfers): plek 2 gekozen op 29-09-2026
        # (website/review/opslag-naad-20260929/, item 4). De grond eromheen staat in dienstenpanelen.css en actielijn.css.
        ("actielijn", {"kopij": None, "kopij_van": ("home", "cijfers")}),
        # Sinds 28-09-2026 het grote formulier van de home, zoals home.py het aanroept. De gebruiker: "Welke dienst u
        # ook kiest, één aanspreekpunt in diensten - replace it with the big one in homepage - "Vertel ons over uw
        # verhuizing"". Hiervoor stond hier ("offertepil", {"variant": "los"}); de kopij daarvan (diensten.md,
        # #offertepil) blijft staan, ongebruikt.
        # Met het klembord van de home op de kaart (29-09-2026): "Vertel ons over uw verhuizing section - homepage version
        # has list clay icon, it should always be 100% opacity [...] also add it to diensten en over-ons pages too."
        ("naadiconen", {"kopij": None, "blok": "aanvraag", "opties": {"kopij": None},
                        "plek": ("aanvraag", [("klembord", "hoek", -14, -52)], "b-formulier__kaart")}),
    ],
)
