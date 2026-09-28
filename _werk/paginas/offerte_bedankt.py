"""/offerte/bedankt/ (noindex): bevestiging na het versturen van het offerteformulier."""
import kopij
from kit import Pagina


def _kort(tekst, maximaal=158):
    """Description voor een noindex-pagina: de eerste zin, hoogstens 158 tekens (bewaker 3)."""
    eerste = tekst.split(". ")[0].rstrip(".") + "."
    if len(eerste) <= maximaal:
        return eerste
    return eerste[:maximaal - 3].rsplit(" ", 1)[0] + "..."


_B = kopij.document("systeem").blok_of_leeg("offerte-bedankt")

PAGINA = Pagina(
    pad="/offerte/bedankt/",
    kopij="systeem",
    header="transparant",
    noindex=True,
    in_sitemap=False,
    body_klasse="p-bedankt",
    titel=_B.velden.get("titel") or "Bedankt voor uw aanvraag | Verhuisbedrijf De Reus",
    beschrijving=_B.velden.get("beschrijving") or _kort(_B.veld("intro", "")),
    blokken=[
        ("kop", {"kopij_id": "offerte-bedankt"}),
        # Sinds 28-09-2026 de Diepblauwe band met foto van /contact/ ("5. What happens next: A: Navy band with
        # photo"), als plaat in de mist-sectie zodat er een lichte band voor de footer blijft. Hiervoor stond hier
        # ("bedankt", {"kopij_id": "offerte-bedankt", "beeld": ("/img/kosten-kalender/wand.webp", 363, 720)});
        # dat blok bestaat nog. Eén WhatsApp-knop per kaart: zie knoppen "bedankt" in na-bericht.py.
        ("na-bericht", {"kopij_id": "offerte-bedankt", "paneel": True, "grond": "mist", "kop": False,
                        "vink": True, "knoppen": "bedankt"}),
    ],
)
