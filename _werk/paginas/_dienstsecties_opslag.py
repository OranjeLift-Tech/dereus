"""De twee extra secties van /diensten/tijdelijke-opslag/ (testlijn test/diensten-paginas). Bouwt: dereus-3e.

Alleen dereus-3e bewerkt dit bestand; elke dienstpagina heeft een eigen bestand, zodat de vier sessies die de
secties bouwen elkaars regels niet raken. dienstpaginas.py zet SECTIES tussen het paneel van de dienst en de reviews,
in deze volgorde. Een regel is (blok, opties), net als in dienstpaginas._blokken(). Hooguit twee regels.

Patroon eerst laten vastleggen in _werk/dienstsecties-register.md (bijgehouden door dereus-37), dan pas bouwen.
Kopij: de pagina leest website/content/diensten.md; een blok met eigen kopij neemt {"kopij": None, "kopij_van":
(document, blok-id)} en leest die zelf via ctx.kopij_van(document).blok(blok-id), zoals blok actielijn.
"""
SECTIES = [
    # 11: zo werkt opslag, drie stappen naast een opslagdeur met de adviseur (section-library/door-shutter-steps, nieuw via /section)
    ("rolluik", {"kopij": None, "kopij_van": ("dienstsecties-opslag", "zo-werkt-opslag")}),
    # 12: goed om te weten voor u opslaat, vier kaarten met klei-iconen (section-library/vision-goals)
    ("tipraster", {"kopij": None, "kopij_van": ("dienstsecties-opslag", "voor-u-opslaat")}),
]
