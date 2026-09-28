"""/werkwijze/: kop, de vijf stappen als kaarten met een verhuizer, de voorbereiding, de verhuisdag (de ene blauwe band met dakrand),
na de verhuizing, reviews, vragen over de werkwijze en de offertepil."""
from kit import Pagina

PAGINA = Pagina(
    pad="/werkwijze/",
    kopij="werkwijze",
    header="transparant",
    body_klasse="p-werkwijze",
    extra_css=("reviews-ster",                # de 3D-ster op de uitgelichte review
               "logomotief"),                 # het logo in de zijmarge in plaats van de randmotieven (Tugche, 28-09-2026)
    blokken=[
        ("kop", {}),
        # De vijf stappen als kaarten met een verhuizer die er bovenuit komt: steps-four-green uit ../section-library,
        # optie A uit website/review/zowerkthet-bibliotheek-20260928/ (28-09-2026). Hiervoor de tijdlijn.
        ("stapkaarten", {"kopij_id": "stappen"}),
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # de tijdlijn als trap (css/blok/tijdlijn.css)
        # ("tijdlijn", {"kopij_id": "stappen"}),
        ("lijstplaat", {"kopij_id": "voorbereiding", "grond": "wit"}),    # wit, zodat de dakrand erboven schoon aansluit
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # de Goudgele plaat waar de verhuizer uit leunt (ontwerp 09 "Diepe plaat"), met de klei-iconen van hier
        # ("lijstplaat-geel", {"kopij_id": "voorbereiding", "grond": "wit"}),
        ("verhuisdag", {}),
        # mozaiek van vier tegels, versie 3 uit ronde 7 (23-09-2026); de foto is nationaal r4 versie 2
        ("namozaiek", {"kopij_id": "na-de-verhuizing",
                       "foto": ("/img/dienst-nationaal-v2-groot.webp", 1440, 1080),
                       "foto_srcset": "/img/dienst-nationaal-v2.webp 720w, /img/dienst-nationaal-v2-groot.webp 1440w"}),
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # Diepblauwe kaart op een schuine gele band, nummer 03 uit _ontwerpen/na-de-verhuizing-varianten.html
        # ("naband", {"kopij_id": "na-de-verhuizing"}),
        ("reviews", {"sectie": "wit"}),              # variant A zoals de home (28-09-2026); wit, tussen twee Mist-secties
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # het reviewblok van referentie B (scorepodium + rail) in onze stijl
        # ("reviewrail", {"kopij_id": "reviews", "accent": "in de praktijk"}),
        # kopkaart: de sectiekop hoort hier in de belkaart, niet erboven. foto: de verhuizer
        # rechts in die kaart. Beide opties staan alleen op deze pagina aan.
        ("vragen", {"kopij_id": "vragen", "beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),   # hetzelfde blauwe paneel als op de home, /kosten/ en /contact/ (23-09-2026)
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # Goudgele band met foto-afdruk (ontwerp 07 uit _ontwerpen/vragen-referentie-ronde1.html). Afdruk
        # woningontruiming: de bankscene staat al twee keer op deze pagina (verhuisdag).
        # ("vragen", {"kopij_id": "vragen", "stijl": "geel", "afdruk": "woningontruiming"}),
        ("offertepil", {"variant": "los"}),
    ],
)
