"""/contact/, opgezet zoals de contactpagina van referentie A (website/referentie):
kop met offertepil over de rand, vertrouwensrij, adres met kaart, persoonlijk contact met kanaalkaarten,
het contactformulier (dereus-b4) als tweekoloms kaart, de Diepblauwe band "na uw bericht" en de vragen.
Weggelaten ten opzichte van referentie A: bedrijfsgegevens (KvK en keurmerk onbekend, open vragen 1.1 en 1.5),
WhatsApp en "kom langs" (niet bevestigd) en foto's van medewerkers (er zijn nog geen eigen foto's).

29-09-2026: terug naar de versie van Tugche (origin/main 9dbb9a8, 28-09-2026): "revert changes to werkwijze and
contact to be the latest tugche changes". Haar blokken, haar volgorde en haar opties; vertrouwensrij.css,
contactkaarten.py en contactkaarten.css zijn weer haar bestanden, en haar kaart staat als eigen blok kaart-tugche.
Onze versie van 28-09-2026 (commit 98f7e0e) staat per blok als commentaar eronder.
"""
from kit import Pagina

PAGINA = Pagina(
    pad="/contact/",
    kopij="contact",
    header="transparant",
    body_klasse="p-contact",
    extra_css=("uitsnede",                    # het vak van de adviseur in "Zo bereikt u ons", zie css/blok/uitsnede.css
               "logomotief"),                 # het logo in de zijmarge in plaats van de randmotieven (28-09-2026)
    blokken=[
        ("kop", {}),
        ("offertepil", {"variant": "los", "over_kop": True}),
        ("vertrouwensrij", {"kopij_id": "vertrouwen", "grond": "wit"}),   # wit, zodat de dakrand erboven schoon aansluit
        # Onze versie had hier geen vertrouwensrij maar, na de kanaalkaarten, de schuine actielijn met klei ("add the r3
        # action line, but use the clay icons instead", "add it but move to middle of page", 28-09-2026):
        # ("actielijn", {"kopij_id": "vertrouwen", "sectie": True}),
        # Haar kaart.py als eigen blok (kaart-tugche.py), met haar kopij #kaart. kaart.py zelf is sinds 28-09-2026
        # de vorm van het werkgebied op de home en blijft dat voor de andere pagina's.
        ("kaart-tugche", {"kopij_id": "kaart", "grond": "blauw"}),
        # Onze versie: Diepblauw, drie gebiedsrijen en een hoge kaart ("7. Map and service area: A: Navy, three
        # area rows and a tall map"): ("kaart", {}),
        # figuur: een verhuizer in het lege vak tussen de kop en de belkaart, in lagen: plaat en huis
        # erachter, dozen ervoor (gevraagd 23-09-2026). verhuizer-doos-deken-uit.webp heeft geen
        # doorzichtige rand (alfa-bbox is het hele bestand, 698x1200); bij een wissel opnieuw meten.
        ("contactkaarten", {"figuur": ("/img/verhuizer-doos-deken-uit.webp", 698, 1200, 0, 0, 698, 1200),
                            "voorgrond": ("/img/verhuisdozen-uit.webp", 562, 522)}),
        # Onze versie: dezelfde opties, maar contactkaarten.py/.css van 98f7e0e: klei-iconen op vlakke kaarten,
        # zonder de 3D-beelden uit img/contact-3d/ en zonder de groene hover.
        # figuur: sinds 28-09-2026 de opzet van het offerteblok op de contactpagina van referentie B
        # (gevraagd: "in de stijl van dat formulier, passend bij het merkboek van De Reus"): drie verhuizers
        # steken boven de kaart uit, een Koningsblauw paneel met schuine bovenkant valt over hun
        # onderlichaam. helpen-drie-uit.webp: de adviseur met het echte borstmerk vooraan, twee mannen uit
        # team-hero erachter (bron en scripts: _ai-beelden/helpen-drie/). grond: lucht komt van de bandenronde.
        ("formulier", {"variant": "contact", "figuur": ("/img/helpen-drie-uit.webp", 685, 591), "grond": "lucht"}),
        # Onze versie: de opmaak van het formulier op de home ("9. Form: A: Light panel with mover"):
        # ("formulier", {"variant": "contact", "beeld": "/img/verhuizer-doos-zijgreep-uit.webp", "grond": "lucht"}),
        # beeld bureau: haar versie van dit blok, de adviseur aan haar bureau met de Goudgele duim. In haar
        # na-bericht.py was dat de enige vorm; hier is het een optie naast de foto met huisvlak.
        ("na-bericht", {"beeld": "bureau"}),
        # Onze versie: ("na-bericht", {}),
        # Goudgele band met foto-afdruk (ontwerp 07, 28-09-2026), net als /werkwijze/. Afdruk zakelijk: de
        # klantenservice staat al in na-bericht en de adviseur in het formulier.
        ("vragen", {"stijl": "geel", "afdruk": "zakelijk"}),
        # Onze versie: hetzelfde blauwe paneel als op de home en /kosten/ (23-09-2026):
        # ("vragen", {"sectie": "wit", "beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),
    ],
)
