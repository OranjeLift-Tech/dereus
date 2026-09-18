"""404.html (noindex): Vercel toont dit bestand bij elk onbekend adres."""
import kopij
from kit import Pagina


def _kort(tekst, maximaal=158):
    """Description voor een noindex-pagina: de eerste zin, hoogstens 158 tekens (bewaker 3)."""
    eerste = tekst.split(". ")[0].rstrip(".") + "."
    if len(eerste) <= maximaal:
        return eerste
    return eerste[:maximaal - 3].rsplit(" ", 1)[0] + "..."


_B = kopij.document("systeem").blok_of_leeg("niet-gevonden")

PAGINA = Pagina(
    pad="/404.html",
    kopij="systeem",
    header="transparant",
    noindex=True,
    in_sitemap=False,
    body_klasse="p-niet-gevonden",
    titel=_B.velden.get("titel") or "Pagina niet gevonden | Verhuisbedrijf De Reus",
    beschrijving=_B.velden.get("beschrijving") or _kort(_B.veld("intro", "")),
    blokken=[
        ("kop", {"kopij_id": "niet-gevonden"}),
        ("niet-gevonden", {"kopij_id": "niet-gevonden"}),
    ],
)
