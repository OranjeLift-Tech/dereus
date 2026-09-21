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
        ("vertrouwensrij", {"kopij_id": "vertrouwen"}),
        ("kaart", {}),
        ("contactkaarten", {}),
        # merk: het beeldmerk in de zijkolom. Zodra De Reus een eigen foto kiest wordt dit "beeld": "/img/...".
        ("formulier", {"variant": "contact", "merk": "beeldmerk"}),
        ("na-bericht", {}),
        ("vragen", {}),
    ],
)
