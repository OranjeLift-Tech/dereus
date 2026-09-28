"""/contact/, opgezet zoals de contactpagina van referentie A (website/referentie):
kop met offertepil over de rand, vertrouwensrij, adres met kaart, persoonlijk contact met kanaalkaarten,
het contactformulier (dereus-b4) als tweekoloms kaart, de Diepblauwe band "na uw bericht" en de vragen.
Weggelaten ten opzichte van referentie A: bedrijfsgegevens (KvK en keurmerk onbekend, open vragen 1.1 en 1.5),
WhatsApp en "kom langs" (niet bevestigd) en foto's van medewerkers (er zijn nog geen eigen foto's).
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
        ("kaart", {"grond": "blauw"}),                                    # de ene Koningsblauwe band van deze pagina
        # figuur: een verhuizer in het lege vak tussen de kop en de belkaart, in lagen: plaat en huis
        # erachter, dozen ervoor (gevraagd 23-09-2026). verhuizer-doos-deken-uit.webp heeft geen
        # doorzichtige rand (alfa-bbox is het hele bestand, 698x1200); bij een wissel opnieuw meten.
        ("contactkaarten", {"figuur": ("/img/verhuizer-doos-deken-uit.webp", 698, 1200, 0, 0, 698, 1200),
                            "voorgrond": ("/img/verhuisdozen-uit.webp", 562, 522)}),
        # figuur: sinds 28-09-2026 de opzet van het offerteblok op de contactpagina van referentie B
        # (gevraagd: "in de stijl van dat formulier, passend bij het merkboek van De Reus"): drie verhuizers
        # steken boven de kaart uit, een Koningsblauw paneel met schuine bovenkant valt over hun
        # onderlichaam. Tot dan team: het kantoor (img/helpen-kantoor.webp) onderaan een blauw-50 zijkolom.
        # helpen-drie-uit.webp: de adviseur met het echte borstmerk vooraan, twee mannen uit team-hero
        # erachter (bron en scripts: _ai-beelden/helpen-drie/). Maat meegeven, PIL staat niet overal.
        # grond: lucht komt van de bandenronde en blijft staan.
        ("formulier", {"variant": "contact", "figuur": ("/img/helpen-drie-uit.webp", 685, 591), "grond": "lucht"}),
        ("na-bericht", {}),
        # Goudgele band met foto-afdruk (ontwerp 07, 28-09-2026), net als /werkwijze/; de home en /kosten/ houden het
        # blauwe paneel. Afdruk zakelijk: de klantenservice staat al in na-bericht en de adviseur in het formulier.
        ("vragen", {"stijl": "geel", "afdruk": "zakelijk"}),
    ],
)
