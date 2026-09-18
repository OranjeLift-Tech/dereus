"""/privacyverklaring/: hoe De Reus omgaat met de gegevens uit de formulieren (AVG), met inhoudsopgave.

letterlijk=True: juridische tekst, zoals op /algemene-voorwaarden/.
"""
from kit import Pagina

PAGINA = Pagina(
    pad="/privacyverklaring/",
    kopij="privacyverklaring",
    header="transparant",
    body_klasse="p-juridisch",
    letterlijk=True,
    blokken=[
        ("kop", {}),
        ("juridisch", {"kopij": None}),
    ],
)
