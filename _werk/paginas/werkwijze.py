"""/werkwijze/: kop, de vijf stappen als tijdlijn, de voorbereiding, de verhuisdag (de ene blauwe band met dakrand),
na de verhuizing, vragen over de werkwijze en de offertepil."""
from kit import Pagina

PAGINA = Pagina(
    pad="/werkwijze/",
    kopij="werkwijze",
    header="transparant",
    body_klasse="p-werkwijze",
    blokken=[
        ("kop", {}),
        ("stappenlang", {"kopij_id": "stappen"}),
        ("checklist", {"kopij_id": "voorbereiding", "grond": "wit"}),     # wit, zodat de dakrand erboven schoon aansluit
        ("verhuisdag", {}),
        ("checklist", {"kopij_id": "na-de-verhuizing", "grond": "mist"}),
        ("vragen", {"kopij_id": "vragen"}),
        ("offertepil", {"variant": "los"}),
    ],
)
