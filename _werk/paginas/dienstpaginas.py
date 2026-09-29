"""De acht diensten van /diensten/ als eigen pagina's. Alleen in de testlijn test/diensten-paginas (29-09-2026).

De gebruiker: "can you do a seperate line to test the website where all 8 diensten sections are their own pages.
dont change the current page, just need this new version prebuild and able to be worked on".

Elke pagina is een sectie van /diensten/: hetzelfde ##-blok uit website/content/diensten.md en hetzelfde patroon
(blok dienstenpanelen, data-vorm per dienst), met daaronder wat /diensten/ onder de acht secties heeft: de reviews,
de actielijn en het grote formulier. Er is geen tekst bij geschreven; alles bestond al op de site:
  kop           label en kop van het blok van de dienst. De H1 is dus de kop van het blok, en het paneel eronder
                herhaalt hem als H2.
  titel         de naam van de dienst in het menu (navigatie.DIENSTEN) met " | Verhuisbedrijf De Reus", zoals de
                andere titels eindigen. De kop van het blok is voor vier diensten langer dan de bewaker toestaat (60).
  beschrijving  de regel van de dienst in de dienstentegels van de home (home.md, #diensten). De eerste alinea van
                het blok is overal langer dan 158 tekens.
De body krijgt p-diensten, zodat de naden onder het paneel dezelfde zijn als op /diensten/.

Een pagina aanpassen: haar regel in PAGINAS_DIENST (adres) of haar blokken in _blokken(). De adressen staan ook in
_b4.DIENST_PAGINA, navigatie.DIENST_PAGINA en jsonld.DIENST_PAGINA; daardoor linken het menu, de footer, de koppen op
/diensten/ en de Service-knopen naar deze pagina's. De vier adressen die er al waren (particulier, zakelijk, opslag,
internationaal) waren conceptpagina's van dienstdetail.py; die regels staan daar nu als commentaar, hun kopij
(website/content/diensten-*.md) is niet gebruikt.
"""
import re
import sys

import kopij as _kopij
import navigatie
from kit import Pagina

# dienstsleutel (het ##-blok in diensten.md) en adres, in de volgorde van /diensten/
PAGINAS_DIENST = [
    ("particulier", "/diensten/particuliere-verhuizingen/"),
    ("zakelijk", "/diensten/zakelijke-verhuizingen/"),
    ("nationaal", "/diensten/nationale-verhuizingen/"),
    ("internationaal", "/diensten/internationale-verhuizingen/"),
    ("verhuislift", "/diensten/verhuislift/"),
    ("opslag", "/diensten/tijdelijke-opslag/"),
    ("montage", "/diensten/montage/"),
    ("woningontruiming", "/diensten/woningontruiming/"),
]


def _plat(t):
    """Opmaak uit de kopij weghalen voor titel en beschrijving: **vet**, ==markering== en [tekst](link)."""
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t.replace("**", "").replace("==", "").strip()


def _naadiconen(sleutel):
    """De klei-iconen die /diensten/ op dit paneel zet (NAADICONEN in paginas/diensten.py), zodat de sectie er
    hetzelfde uitziet. diensten.py laadt eerder: build.py laadt de paginamodules op alfabet."""
    diensten = sys.modules.get("paginas_diensten")
    return [p for p in getattr(diensten, "NAADICONEN", []) if p[0] == sleutel]


def _blokken(sleutel):
    plek = _naadiconen(sleutel)
    paneel = (("naadiconen", {"kopij": None, "blok": "dienstenpanelen", "opties": {"kopij_ids": [sleutel]}, "plek": plek})
              if plek else ("dienstenpanelen", {"kopij_ids": [sleutel]}))
    return [
        ("kop", {"kopij_id": sleutel, "id": "kop", "dienst": sleutel}),
        paneel,
        # zoals onder de acht secties van /diensten/ (paginas/diensten.py)
        ("reviews", {"sectie": "wit"}),
        ("actielijn", {"kopij": None, "kopij_van": ("home", "cijfers")}),
        ("naadiconen", {"kopij": None, "blok": "aanvraag", "opties": {"kopij": None},
                        "plek": ("aanvraag", [("klembord", "hoek", -14, -52)], "b-formulier__kaart")}),
    ]


def _pagina(sleutel, pad):
    naam = next(n for s, n, _ in navigatie.DIENSTEN if s == sleutel)
    tegel = next(it for it in _kopij.document("home").blok("diensten").items if it.id == sleutel)
    titel = f"{naam} | Verhuisbedrijf De Reus"
    return Pagina(pad=pad, kopij="diensten", header="transparant", body_klasse="p-diensten p-dienstpagina",
                  extra_css=("reviews-ster",), titel=titel, og_titel=titel,
                  beschrijving=_plat(tegel.veld("tekst")), blokken=_blokken(sleutel))


PAGINAS = [_pagina(*rij) for rij in PAGINAS_DIENST]
