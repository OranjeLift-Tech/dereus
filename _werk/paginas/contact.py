"""/contact/, opgezet zoals de contactpagina van referentie A (website/referentie):
kop met offertepil over de rand, vertrouwensrij, adres met kaart, persoonlijk contact met kanaalkaarten,
het contactformulier (dereus-b4) als tweekoloms kaart, de Diepblauwe band "na uw bericht" en de vragen.
Weggelaten ten opzichte van referentie A: bedrijfsgegevens (KvK en keurmerk onbekend, open vragen 1.1 en 1.5),
WhatsApp en "kom langs" (niet bevestigd) en foto's van medewerkers (er zijn nog geen eigen foto's).

29-09-2026: terug naar de versie van Tugche (origin/main 9dbb9a8, 28-09-2026): "revert changes to werkwijze and
contact to be the latest tugche changes". Haar blokken, haar volgorde en haar opties; vertrouwensrij.css,
contactkaarten.py en contactkaarten.css zijn weer haar bestanden, en haar kaart staat als eigen blok kaart-tugche.
Onze versie van 28-09-2026 (commit 98f7e0e) staat per blok als commentaar eronder.

29-09-2026, samengevoegd met origin/main 8971f9e ("add all the changes to it except to the homepage, diensten,
over-ons pages"): waar Tugche een sectie opnieuw deed, staat nu die van haar: de kaart met punaise en wekker in de
gele tegels en de groene offerteknop (kaart.py), de kanaalkaarten met echte foto's (contactkaarten.py/.css), de
adviseur in de witte boog (na-bericht) en de Koningsblauwe kaart met de collega (vragen). Vertrouwensrij en het
formulier met de drie verhuizers raakte haar commit niet: die blijven zoals hierboven.
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
        # Sinds de samenvoeging met 8971f9e (29-09-2026) weer kaart.py: Diepblauw, drie gebiedsrijen en een hoge kaart
        # ("7. Map and service area: A: Navy, three area rows and a tall map"), met de punaise en de wekker van Tugche
        # in de gele tegels en de offerteknop groen, net als in de header.
        ("kaart", {}),
        # Haar kaart van 9dbb9a8 als eigen blok (kaart-tugche.py), met haar kopij #kaart, van de ochtend van
        # 29-09-2026 tot de samenvoeging, aan door deze regel te wisselen met de regel erboven:
        # ("kaart-tugche", {"kopij_id": "kaart", "grond": "blauw"}),
        # figuur: een verhuizer in het lege vak tussen de kop en de belkaart, in lagen: plaat en huis
        # erachter, dozen ervoor (gevraagd 23-09-2026). verhuizer-doos-deken-uit.webp heeft geen
        # doorzichtige rand (alfa-bbox is het hele bestand, 698x1200); bij een wissel opnieuw meten.
        ("contactkaarten", {"figuur": ("/img/verhuizer-doos-deken-uit.webp", 698, 1200, 0, 0, 698, 1200),
                            "voorgrond": ("/img/verhuisdozen-uit.webp", 562, 522)}),
        # Sinds de samenvoeging met 8971f9e (29-09-2026) contactkaarten.py/.css van Tugche: echte foto's
        # (img/contact-echt/) op een goudgele schijf, de groene rand altijd aan. Daarvoor haar 3D-beelden uit
        # img/contact-3d/ (9dbb9a8), en in 98f7e0e klei-iconen op vlakke kaarten.
        # figuur: sinds 28-09-2026 de opzet van het offerteblok op de contactpagina van referentie B
        # (gevraagd: "in de stijl van dat formulier, passend bij het merkboek van De Reus"): drie verhuizers
        # steken boven de kaart uit, een Koningsblauw paneel met schuine bovenkant valt over hun
        # onderlichaam. helpen-drie-uit.webp: de adviseur met het echte borstmerk vooraan, twee mannen uit
        # team-hero erachter (bron en scripts: _ai-beelden/helpen-drie/). grond: lucht komt van de bandenronde.
        ("formulier", {"variant": "contact", "figuur": ("/img/helpen-drie-uit.webp", 685, 591), "grond": "lucht"}),
        # Onze versie: de opmaak van het formulier op de home ("9. Form: A: Light panel with mover"):
        # ("formulier", {"variant": "contact", "beeld": "/img/verhuizer-doos-zijgreep-uit.webp", "grond": "lucht"}),
        # Sinds 29-09-2026 de adviseur zonder kamer in een witte boog, als "Na uw aanvraag" bij referentie A
        # (de gebruiker: haar achtergrond weg en iets wits erachter, zoals daar; optie beeld in na-bericht.py).
        # Tugche, 8971f9e.
        ("na-bericht", {"beeld": "boog"}),
        # beeld bureau: haar versie van 9dbb9a8, de adviseur aan haar bureau met de Goudgele duim, aan door deze regel
        # te wisselen met de regel erboven:
        # ("na-bericht", {"beeld": "bureau"}),
        # Onze versie: ("na-bericht", {}),
        # Sinds 29-09-2026 de Koningsblauwe kaart met de collega die erboven uitsteekt (ontwerp 03 uit
        # _ontwerpen/vragen-contact-ronde3.html, Tugche, 8971f9e). Het paneel stond te druk, "gesprek" was te sober.
        ("vragen", {"stijl": "kaart", "sectie": "wit"}),
        # Een paar uur op 29-09-2026: dezelfde opzet zonder kaart en zonder collega, aan door deze regel te wisselen met de regel erboven:
        # ("vragen", {"stijl": "gesprek"}),
        # Goudgele band met foto-afdruk (ontwerp 07, 28-09-2026), net als /werkwijze/. Afdruk zakelijk: de
        # klantenservice staat al in na-bericht en de adviseur in het formulier:
        # ("vragen", {"stijl": "geel", "afdruk": "zakelijk"}),
        # Onze versie: hetzelfde blauwe paneel als op de home en /kosten/ (23-09-2026):
        # ("vragen", {"sectie": "wit", "beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),
    ],
)
