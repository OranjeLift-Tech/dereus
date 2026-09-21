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
        # breed: kop op het midden, punten eronder in twee kolommen. De koppen hier zijn kort en de lijsten lang,
        # in de indeling ernaast bleef links de onderste helft leeg.
        ("checklist", {"kopij_id": "voorbereiding", "grond": "wit", "indeling": "breed"}),   # wit, zodat de dakrand erboven schoon aansluit
        ("verhuisdag", {}),
        ("checklist", {"kopij_id": "na-de-verhuizing", "grond": "mist", "indeling": "breed"}),
        ("vragen", {"kopij_id": "vragen"}),
        ("offertepil", {"variant": "los"}),
    ],
)
