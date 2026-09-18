"""/algemene-voorwaarden/: de voorwaarden letterlijk (Versie 2025), met inhoudsopgave en de pdf.

letterlijk=True: de juridische tekst mag niet worden herschreven, dus de controle op verboden woorden
(zoals "garantie" in artikel 15, Nakomingsgarantie) slaat deze pagina over. Dashes en links blijven gecontroleerd.
"""
from kit import Pagina

PAGINA = Pagina(
    pad="/algemene-voorwaarden/",
    kopij="algemene-voorwaarden",
    header="transparant",
    body_klasse="p-juridisch",
    letterlijk=True,
    blokken=[
        ("kop", {}),
        ("juridisch", {"kopij": None, "pdf": "/docs/algemene-voorwaarden-verhuisbedrijf-de-reus-2025.pdf"}),
    ],
)
