"""/werkwijze/: kop, de vijf stappen als tijdlijn, de voorbereiding, de verhuisdag (de ene blauwe band met dakrand),
na de verhuizing, reviews, vragen over de werkwijze en de offertepil."""
from kit import Pagina

PAGINA = Pagina(
    pad="/werkwijze/",
    kopij="werkwijze",
    header="transparant",
    body_klasse="p-werkwijze",
    extra_css=("uitsnede",),                  # de gedeelde uitsnede-plaat, zie css/blok/uitsnede.css
    blokken=[
        ("kop", {}),
        ("tijdlijn", {"kopij_id": "stappen"}),
        ("lijstplaat", {"kopij_id": "voorbereiding", "grond": "wit"}),    # wit, zodat de dakrand erboven schoon aansluit
        ("verhuisdag", {}),
        ("naplaten", {"kopij_id": "na-de-verhuizing", "grond": "mist",
                      "beeld": ("/img/dienst-nationaal-uit.webp", 1080, 810, 470, 100, 394, 710)}),  # slotplaten + foto
        ("reviews", {"variant": "compact"}),                              # wit, tussen twee Mist-secties
        # kopkaart: de sectiekop hoort hier in de belkaart, niet erboven. foto: de verhuizer
        # rechts in die kaart. Beide opties staan alleen op deze pagina aan.
        ("vragen", {"kopij_id": "vragen", "beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),   # hetzelfde blauwe paneel als op de home, /kosten/ en /contact/ (23-09-2026)
        ("offertepil", {"variant": "los"}),
    ],
)
