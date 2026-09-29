"""De twee extra secties van /diensten/woningontruiming/ (testlijn test/diensten-paginas). Bouwt: dereus-ce.

Alleen dereus-ce bewerkt dit bestand; elke dienstpagina heeft een eigen bestand, zodat de vier sessies die de
secties bouwen elkaars regels niet raken. dienstpaginas.py zet SECTIES tussen het paneel van de dienst en de reviews,
in deze volgorde. Een regel is (blok, opties), net als in dienstpaginas._blokken(). Hooguit twee regels.

Patroon eerst laten vastleggen in _werk/dienstsecties-register.md (bijgehouden door dereus-37), dan pas bouwen.
Kopij: de pagina leest website/content/diensten.md; een blok met eigen kopij neemt {"kopij": None, "kopij_van":
(document, blok-id)} en leest die zelf via ctx.kopij_van(document).blok(blok-id), zoals blok actielijn.
"""
SECTIES = [
    # 15: het eerste gesprek met de verhuisadviseur, met drie bestemmingen voor de spullen (section-library/reply-dial-choices)
    ("ontruimgesprek", {"kopij": None, "kopij_van": ("dienstsecties-woningontruiming", "gesprek")}),
]
