"""De twee extra secties van /diensten/internationale-verhuizingen/ (testlijn test/diensten-paginas). Bouwt: dereus-49.

Alleen dereus-49 bewerkt dit bestand; elke dienstpagina heeft een eigen bestand, zodat de vier sessies die de
secties bouwen elkaars regels niet raken. dienstpaginas.py zet SECTIES tussen het paneel van de dienst en de reviews,
in deze volgorde. Een regel is (blok, opties), net als in dienstpaginas._blokken(). Hooguit twee regels.

Patroon eerst laten vastleggen in _werk/dienstsecties-register.md (bijgehouden door dereus-37), dan pas bouwen.
Kopij: de pagina leest website/content/diensten.md; een blok met eigen kopij neemt {"kopij": None, "kopij_van":
(document, blok-id)} en leest die zelf via ctx.kopij_van(document).blok(blok-id), zoals blok actielijn.
"""
SECTIES = [
    # 7 in het register: locations-plate-truck (De Bresser), de vier stappen op een plaat over de wielen van de wagen
    ("grensplaat", {"kopij": None, "kopij_van": ("dienstsecties-internationaal", "over-de-grens")}),
    # 8 in het register: nieuw tip-sheets-pocket (/section), vier tips als vellen in een map
    ("tipmap", {"kopij": None, "kopij_van": ("dienstsecties-internationaal", "op-tijd")}),
]
