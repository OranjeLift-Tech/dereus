"""/diensten/: kop met ankerchips, de acht diensten met ankernavigatie, reviews (compact) en de offertepil."""
import kopij as _kopij
from kit import Pagina

DIENSTEN = ["particulier", "zakelijk", "nationaal", "internationaal", "verhuislift", "opslag", "montage", "woningontruiming"]


def _chips():
    """De chiptekst is het veld label van elk dienstblok (anders de kop)."""
    doc = _kopij.document("diensten")
    return [(doc.blok(d).veld("label") or doc.blok(d).kop, f"#{d}") for d in DIENSTEN if doc.heeft(d)]


PAGINA = Pagina(
    pad="/diensten/",
    kopij="diensten",
    header="transparant",
    body_klasse="p-diensten",
    blokken=[
        ("kop", {"chips": _chips()}),
        ("dienstenpanelen", {"kopij_ids": DIENSTEN}),
        ("reviews", {"variant": "compact"}),
        ("offertepil", {"variant": "los"}),
    ],
)
