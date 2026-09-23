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
    extra_css=("uitsnede",),                  # het vak van de adviseur in "Zo bereikt u ons", zie css/blok/uitsnede.css
    blokken=[
        ("kop", {}),
        ("offertepil", {"variant": "los", "over_kop": True}),
        ("vertrouwensrij", {"kopij_id": "vertrouwen", "grond": "wit"}),   # wit, zodat de dakrand erboven schoon aansluit
        ("kaart", {"grond": "blauw"}),                                    # de ene Koningsblauwe band van deze pagina
        # figuur: een verhuizer in het lege vak tussen de kop en de belkaart, in lagen: plaat en huis
        # erachter, dozen ervoor (gevraagd 23-09-2026). verhuizer-doos-deken-uit.webp heeft geen
        # doorzichtige rand (alfa-bbox is het hele bestand, 698x1200); bij een wissel opnieuw meten.
        ("contactkaarten", {"figuur": ("/img/verhuizer-doos-deken-uit.webp", 698, 1200, 0, 0, 698, 1200),
                            "voorgrond": ("/img/verhuisdozen-uit.webp", 562, 522)}),
        # team: de groepsfoto onderaan de zijkolom, tegen de onderrand (commit 7fe41fb, "Teamfoto terug
        # bij Zo helpen wij u snel"). Stond tot 22-09-2026 alleen in de gebouwde HTML en niet hier, dus
        # elke build draaide hem terug naar de uitsnede van de adviseur; die staat nu in de bron.
        # grond: lucht komt van de bandenronde en blijft staan.
        ("formulier", {"variant": "contact", "team": "/img/helpen-kantoor.webp", "grond": "lucht"}),
        ("na-bericht", {}),
        ("vragen", {"sectie": "wit", "beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),   # hetzelfde blauwe paneel als op de home, /werkwijze/ en /kosten/ (23-09-2026)
    ],
)
