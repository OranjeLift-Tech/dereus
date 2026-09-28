"""/werkwijze/: kop, de vijf stappen als tijdlijn, de voorbereiding, de verhuisdag (de ene blauwe band met dakrand),
na de verhuizing, reviews, vragen over de werkwijze en de offertepil."""
from kit import Pagina

PAGINA = Pagina(
    pad="/werkwijze/",
    kopij="werkwijze",
    header="transparant",
    body_klasse="p-werkwijze",
    extra_css=("logomotief",),                # het logo in de zijmarge in plaats van de randmotieven (28-09-2026)
    blokken=[
        ("kop", {}),
        ("tijdlijn", {"kopij_id": "stappen"}),
        ("lijstplaat", {"kopij_id": "voorbereiding", "grond": "wit"}),    # wit, zodat de dakrand erboven schoon aansluit
        ("verhuisdag", {}),
        # Diepblauwe kaart op een schuine gele band, nummer 03 uit _ontwerpen/na-de-verhuizing-varianten.html
        # (28-09-2026); verving het mozaiek (blok namozaiek, dat blijft bestaan)
        ("naband", {"kopij_id": "na-de-verhuizing"}),
        # het reviewblok van referentie B (scorepodium + rail) in onze stijl (28-09-2026); verving reviews compact
        # met de 3D-ster (extra_css reviews-ster-werkwijze, dat bestand blijft bestaan). Wit, tussen twee Mist-secties.
        ("reviewrail", {"kopij_id": "reviews", "accent": "in de praktijk"}),
        # Goudgele band met foto-afdruk (ontwerp 07 uit _ontwerpen/vragen-referentie-ronde1.html, 28-09-2026), net als
        # /contact/. Afdruk woningontruiming: de bankscène staat al twee keer op deze pagina (verhuisdag).
        ("vragen", {"kopij_id": "vragen", "stijl": "geel", "afdruk": "woningontruiming"}),
        ("offertepil", {"variant": "los"}),
    ],
)
