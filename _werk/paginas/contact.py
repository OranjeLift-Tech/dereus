"""/contact/, opgezet zoals de contactpagina van De Kievit (website/referentie, de-kievit.nl/contact/):
kop met offertepil over de rand, vertrouwensrij, adres met kaart, persoonlijk contact met kanaalkaarten,
het contactformulier (dereus-b4) als tweekoloms kaart, de Diepblauwe band "na uw bericht" en de vragen.
Weggelaten ten opzichte van De Kievit: bedrijfsgegevens (KvK en keurmerk onbekend, open vragen 1.1 en 1.5),
WhatsApp en "kom langs" (niet bevestigd) en foto's van medewerkers (er zijn nog geen eigen foto's).
"""
from kit import Pagina

PAGINA = Pagina(
    pad="/contact/",
    kopij="contact",
    header="transparant",
    body_klasse="p-contact",
    blokken=[
        ("kop", {}),
        ("offertepil", {"variant": "los", "over_kop": True}),
        ("vertrouwensrij", {"kopij_id": "vertrouwen", "grond": "wit"}),   # wit, zodat de dakrand erboven schoon aansluit
        ("kaart", {"grond": "blauw"}),                                    # de ene Koningsblauwe band van deze pagina
        ("contactkaarten", {}),
        # beeld: de uitsnede van de verhuisadviseur in de zijkolom, genormaliseerd op 640x954.
        # grond: lucht komt van de bandenronde en blijft staan.
        ("formulier", {"variant": "contact", "beeld": "/img/contact-adviseur-uit.webp", "grond": "lucht"}),
        ("na-bericht", {}),
        ("vragen", {"sectie": "wit", "beeld": "headset"}),   # servicebalie: het paneel met de headset erboven
    ],
)
