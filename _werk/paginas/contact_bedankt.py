"""/contact/bedankt/ (noindex): bevestiging na het versturen van het contactformulier."""
import kopij
from kit import Pagina


def _kort(tekst, maximaal=158):
    """Description voor een noindex-pagina: de eerste zin, hoogstens 158 tekens (bewaker 3)."""
    eerste = tekst.split(". ")[0].rstrip(".") + "."
    if len(eerste) <= maximaal:
        return eerste
    return eerste[:maximaal - 3].rsplit(" ", 1)[0] + "..."


_B = kopij.document("systeem").blok_of_leeg("contact-bedankt")

PAGINA = Pagina(
    pad="/contact/bedankt/",
    kopij="systeem",
    header="transparant",
    noindex=True,
    in_sitemap=False,
    body_klasse="p-bedankt",
    titel=_B.velden.get("titel") or "Bedankt voor uw bericht | Verhuisbedrijf De Reus",
    beschrijving=_B.velden.get("beschrijving") or _kort(_B.veld("intro", "")),
    blokken=[
        ("kop", {"kopij_id": "contact-bedankt"}),
        ("bedankt", {"kopij_id": "contact-bedankt"}),
    ],
)
