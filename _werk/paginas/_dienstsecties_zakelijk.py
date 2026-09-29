"""De twee extra secties van /diensten/zakelijke-verhuizingen/ (testlijn test/diensten-paginas). Bouwt: dereus-28.

Alleen dereus-28 bewerkt dit bestand; elke dienstpagina heeft een eigen bestand, zodat de vier sessies die de
secties bouwen elkaars regels niet raken. dienstpaginas.py zet SECTIES tussen het paneel van de dienst en de reviews,
in deze volgorde. Een regel is (blok, opties), net als in dienstpaginas._blokken(). Hooguit twee regels.

Patroon eerst laten vastleggen in _werk/dienstsecties-register.md (bijgehouden door dereus-37), dan pas bouwen.
Kopij: de pagina leest website/content/diensten.md; een blok met eigen kopij neemt {"kopij": None, "kopij_van":
(document, blok-id)} en leest die zelf via ctx.kopij_van(document).blok(blok-id), zoals blok actielijn.
"""
SECTIES = [
    # 3 in het register: branch-route-stops (De Bresser), de werkwijze als haltes op een route
    ("routestops", {"kopij": None, "kopij_van": ("diensten-zakelijk", "hoe"), "offerte": "/offerte/?dienst=zakelijk"}),
    # 4 in het register: text-benefit-cards (Solar Green), de tips als kaarten met de vraag over grote kantoren
    ("tipkaarten", {"kopij": None, "kopij_van": ("diensten-zakelijk", "tips")}),
]
