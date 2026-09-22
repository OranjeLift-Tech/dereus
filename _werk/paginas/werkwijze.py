"""/werkwijze/: kop, de vijf stappen als tijdlijn, de voorbereiding, de verhuisdag (de ene blauwe band met dakrand),
na de verhuizing, reviews, vragen over de werkwijze en de offertepil."""
from kit import Pagina

PAGINA = Pagina(
    pad="/werkwijze/",
    kopij="werkwijze",
    header="transparant",
    body_klasse="p-werkwijze",
    blokken=[
        ("kop", {}),
        ("tijdlijn", {"kopij_id": "stappen"}),
        ("lijstplaat", {"kopij_id": "voorbereiding", "grond": "wit"}),    # wit, zodat de dakrand erboven schoon aansluit
        ("verhuisdag", {}),
        ("naplaten", {"kopij_id": "na-de-verhuizing", "grond": "mist"}),   # twee brede slotplaten, ronde 6
        ("reviews", {"variant": "compact"}),                              # wit, tussen twee Mist-secties
        ("vragen", {"kopij_id": "vragen"}),
        ("offertepil", {"variant": "los"}),
    ],
)
