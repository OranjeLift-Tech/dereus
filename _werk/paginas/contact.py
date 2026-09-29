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
        # Sinds 28-09-2026 de vorm van het werkgebied op de home, Diepblauw ("7. Map and service area: A: Navy, three
        # area rows and a tall map"). Hiervoor {"grond": "blauw"}, de enige Koningsblauwe band van deze pagina.
        ("kaart", {}),
        # figuur: een verhuizer in het lege vak tussen de kop en de belkaart, in lagen: plaat en huis
        # erachter, dozen ervoor (gevraagd 23-09-2026). verhuizer-doos-deken-uit.webp heeft geen
        # doorzichtige rand (alfa-bbox is het hele bestand, 698x1200); bij een wissel opnieuw meten.
        ("contactkaarten", {"figuur": ("/img/verhuizer-doos-deken-uit.webp", 698, 1200, 0, 0, 698, 1200),
                            "voorgrond": ("/img/verhuisdozen-uit.webp", 562, 522)}),
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # de kaarten met een plaatrand, de verhuizer groter (optie stijl in contactkaarten.py); de groene hover staat altijd aan
        # ("contactkaarten", {"figuur": ("/img/verhuizer-doos-deken-uit.webp", 698, 1200, 0, 0, 698, 1200), "voorgrond": ("/img/verhuisdozen-uit.webp", 562, 522), "stijl": "groen"}),
        # Sinds 28-09-2026 de schuine actielijn, hetzelfde blok als #cijfers op de home: "make it slanted", "a more
        # interesting background color", "a quick overview like some sort of action line". Hiervoor stond direct onder
        # de kop ("vertrouwensrij", {"kopij_id": "vertrouwen", "grond": "wit"}); dat blok bestaat nog.
        # Hier en niet onder de kop: "add it but move to middle of page" (28-09-2026). De naad tussen contactkaarten
        # en formulier ligt het dichtst bij de helft van de pagina (1440: 2760 van 5410px, 390: 4553 van 9286px).
        # sectie: True, dus hij telt mee in de motieftellers van style.css: contactkaarten is nu de eerste getelde
        # sectie (huis, klein, links) en de actielijn de tweede (doos, groot, rechts); formulier en vragen houden hun motief.
        ("actielijn", {"kopij_id": "vertrouwen", "sectie": True}),
        # Sinds 28-09-2026 de opmaak van het formulier op de home ("9. Form: A: Light panel with mover"):
        # dezelfde verhuizer, die boven de kaart uitsteekt. Hiervoor stond hier het kantoor
        # (team: /img/helpen-kantoor.webp, commit 7fe41fb). grond: lucht komt van de bandenronde en blijft staan.
        ("formulier", {"variant": "contact", "beeld": "/img/verhuizer-doos-zijgreep-uit.webp", "grond": "lucht"}),
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # de opzet van het offerteblok op de contactpagina van referentie B: drie verhuizers steken boven de kaart
        # uit, een Koningsblauw paneel met schuine bovenkant valt over hun onderlichaam. helpen-drie-uit.webp: de
        # adviseur met het echte borstmerk vooraan, twee mannen uit team-hero erachter (_ai-beelden/helpen-drie/).
        # ("formulier", {"variant": "contact", "figuur": ("/img/helpen-drie-uit.webp", 685, 591), "grond": "lucht"}),
        # Sinds 29-09-2026 de adviseur zonder kamer in een witte boog, als "Na uw aanvraag" bij referentie A
        # (de gebruiker: haar achtergrond weg en iets wits erachter, zoals daar; optie beeld in na-bericht.py).
        ("na-bericht", {"beeld": "boog"}),
        # Tot 29-09-2026 de foto in de lijst met het huisvlak erachter, aan door deze regel te wisselen met de regel erboven:
        # ("na-bericht", {}),
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de eerste regel hierboven:
        # de adviseur aan haar bureau met de Goudgele duim (optie beeld in na-bericht.py)
        # ("na-bericht", {"beeld": "bureau"}),
        # Sinds 29-09-2026 de Koningsblauwe kaart met de collega die erboven uitsteekt (ontwerp 03 uit
        # _ontwerpen/vragen-contact-ronde3.html). Het paneel hieronder stond te druk, "gesprek" was te sober.
        ("vragen", {"stijl": "kaart", "sectie": "wit"}),
        # Een paar uur op 29-09-2026: dezelfde opzet zonder kaart en zonder collega, aan door deze regel te wisselen met de regel erboven:
        # ("vragen", {"stijl": "gesprek"}),
        # Tot 29-09-2026 het blauwe paneel met headset, vraagtekens en verhuizer, aan door deze regel te wisselen met de regel erboven:
        # ("vragen", {"sectie": "wit", "beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),   # hetzelfde blauwe paneel als op de home, /werkwijze/ en /kosten/ (23-09-2026)
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # Goudgele band met foto-afdruk (ontwerp 07), net als /werkwijze/. Afdruk zakelijk: de klantenservice staat al
        # in na-bericht en de adviseur in het formulier.
        # ("vragen", {"stijl": "geel", "afdruk": "zakelijk"}),
    ],
)
