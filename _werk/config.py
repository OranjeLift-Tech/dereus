"""Vaste gegevens en schakelaars van de site. Eén plek: wijzig het hier, niet in de HTML.

Alle tekst voor bezoekers staat in website/content/*.md. Hier staan alleen gegevens die op
meer plekken terugkomen (telefoon, adres, tijden) en de schakelaars voor de build.
"""

# Voorkeursdomein, met www (sitemap 3). Canonical, og:url, sitemap.xml en JSON-LD gebruiken dit.
DOMEIN = "https://www.verhuisbedrijfdereus.nl"
NAAM = "Verhuisbedrijf De Reus"
KORTE_NAAM = "De Reus"

TEL = "085 000 5647"
TELHREF = "tel:+31850005647"
# Hetzelfde bedrijfsnummer; de link bevestigt niet dat het account actief is.
WHATSAPP = "https://wa.me/" + "".join(c for c in TELHREF if c.isdigit())
MAIL = "info@verhuisbedrijfdereus.nl"

STRAAT = "Lau Mazirellaan 336"
POSTCODE = "2525 ZJ"
PLAATS = "Den Haag"
ADRES = f"{STRAAT}, {POSTCODE} {PLAATS}"
# Routeplanner naar het hoofdkantoor (OpenStreetMap, geen trackers).
ROUTE = "https://www.openstreetmap.org/directions?to=52.05963%2C4.29914#map=17/52.05963/4.29914"
# Coordinaten van PDOK Locatieserver voor Lau Mazirellaan 336 (ook in de kaart en de JSON-LD)
GEO = (52.0596297, 4.29913794)

# Openingstijden in Nederlandse tijd. De bereikbaarheidsstatus in js/site.js leest ze uit data-attributen.
# (dagnummers 0 = zondag ... 6 = zaterdag, tijden in minuten na middernacht)
TIJDEN = [
    {"dagen": "maandag tot en met zaterdag", "kort": "ma t/m za", "van": "08.00", "tot": "20.00", "nummers": [1, 2, 3, 4, 5, 6]},
    {"dagen": "zondag", "kort": "zo", "van": "09.00", "tot": "17.00", "nummers": [0]},
]

# Google: altijd als "4,9 uit 5 op Google", zonder aantal (open vraag 1.4).
GOOGLE_SCORE = "4,9"
GOOGLE_PROFIEL = "https://www.google.com/search?q=reviews+voor+verhuisbedrijf+de+reus"

# Web3Forms: nog geen key. Zolang dit de placeholder is, toont het formulier een nette melding met
# telefoon en e-mail in plaats van te versturen. Zet hier NOOIT een echte key als de repo publiek is
# zonder overleg met dereus-28: een Web3Forms-key is bedoeld voor de voorkant, maar hoort bij de klant.
WEB3FORMS_KEY = "VUL-HIER-DE-WEB3FORMS-KEY-IN"

# Logo: één regel om te wisselen. De build kopieert de bestanden naar img/logo/.
# Logo v2 (goedgekeurd): grotere biceps, zonder tagline. Terug naar het oude logo: "brandbook/assets/logo".
LOGO_BRON = "brandbook/assets/logo-v2"
# Welk logo in de header: "horizontaal" (zoals De Kievit en Brocken, minimaal 28 px hoog) of "staand".
HEADER_LOGO = "horizontaal"
# Afmetingen (viewBox) van de logo's, voor width en height op <img>
LOGO_MATEN = {"horizontaal": (2444, 509), "staand": (1000, 828), "beeldmerk": (1000, 509)}
# "Geen verhuizing te groot!" is sinds logo v2 een los motto: één keer op de home, nooit naast de pay-off.
MOTTO = "Geen verhuizing te groot!"

# De teamfoto in de hero, vrijstaand, met de rechte onderrand achter de offertekaart (zoals Brocken).
# Pad zonder maat en extensie; _werk/teambeeld.py maakt -700, -1100 en -1600.webp, een png-terugval en
# een .json met de maten. None = het beeldmerk.
HERO_TEAM = "/img/team/team-hero-dozen"
HERO_TEAM_ALT = "Drie verhuizers van Verhuisbedrijf De Reus in uniform"
# Achtergrondfoto van de hero. None = grafische hero (Diepblauw naar Koningsblauw, huismotief).
# Komt er een eigen foto van De Reus, zet dan het pad hier, bijvoorbeeld "/img/hero-de-reus.webp"
# (1920 x 1120, webp, onder 250 KB). De waas en de korrel liggen er al klaar voor.
# Geen stockfoto's van de oude Wix-site: die licentie geldt alleen op Wix.
HERO_BEELD = None

# ---------------------------------------------------------------------------
# Conceptpagina's (BOUWPLAN 12). Een pagina met Pagina(concept=True) wordt pas live als ze hier op
# True staat. Uit: niet in de deploy, niet in sitemap.xml, niet in menu, megamenu of footer, en geen
# enkele live pagina linkt ernaar. Lokaal bekijken: python _werk/build.py --concept --serve
# (alles in _voorbeeld/, met een overzicht op /_concept/).
# Aanzetten = één regel hier; menu, footer, hubblokken en sitemap volgen vanzelf.
PUBLICEER = {
    # "/diensten/tijdelijke-opslag/": False,
}

# Feiten van de klant die pagina's gebruiken. None = nog onbekend: de zin of rij valt dan weg,
# er verschijnt nooit "[...]" of "None". Lijsten als ["Spanje", "Frankrijk"].
# In de kopij: {NAAM}, "als: NAAM", "tenzij: NAAM" en "alleen-als: NAAM" (BOUWPLAN 12).
# Tussen haakjes het nummer van de open vraag aan de klant.
FEITEN = {
    # bedrijf (1.1, 1.2)
    "RECHTSVORM": None,             # bijvoorbeeld "eenmanszaak"
    "KVK": None,                    # KvK-nummer als tekst; maakt het woord KvK toegestaan
    "OPRICHTINGSJAAR": None,        # jaartal; maakt "sinds 2015" toegestaan
    "EIGENAAR": None,               # naam van de eigenaar (/over-ons/)
    "TEAM": None,                   # korte omschrijving van het team (/over-ons/)
    # Het beeld in het huisvenster op /over-ons/. Let op: dit is nu GEEN foto van de echte ploeg, maar een
    # gegenereerd beeld van fictieve verhuizers (beeld-opties/over-ons-20260921, kandidaat 02-wagen-laden).
    # Daarom beschrijft de alt-tekst hieronder wat er te zien is en zegt hij niet wie het zijn.
    # Komt er een echte foto, vervang dan allebei de regels, niet alleen het pad.
    "TEAM_BEELD": "/img/team-de-reus.webp",
    "TEAM_BEELD_ALT": "Illustratief beeld van drie verhuizers die dozen en verhuisdekens in een gesloten verhuiswagen laden",
    # reviews en werkgebied (1.4, 1.3)
    "AANTAL_REVIEWS": None,         # aantal Google-reviews
    "WERKGEBIED_PLAATSEN": None,    # bevestigde plaatsen, lijst
    # materieel (1.6)
    "EIGEN_BUSSEN": None,           # True/False
    "EIGEN_VERHUISLIFT": None,      # True/False
    "LIFT_MAX_VERDIEPING": None,    # getal of tekst
    # opslag (1.6, 2.4)
    "OPSLAG_LOCATIE": None,
    "OPSLAG_TERMIJN": None,
    "OPSLAG_OPZEGTERMIJN": None,
    "OPSLAG_VERZEKERING": None,
    "OPSLAG_LOS_TE_BOEKEN": None,   # True/False
    # internationaal en prijs (5.1, 5.2)
    "LANDEN": None,                 # lijst
    "PRIJS_INDICATIE": None,
    # voorwaarden en diensten (2.1, 2.5, 2.6, 5.4, 2.4)
    "KOSTELOOS_WIJZIGEN": None,     # True/False
    "ZAKELIJK_AVOND_WEEKEND": None, # True/False
    "ZAKELIJK_IT": None,            # True/False
    "MEERWERK_VOORAF": None,
    "HANDYMAN_KLUSSEN": None,       # lijst
    "ONTRUIMING_BEZEMSCHOON": None, # True/False
    "ONTRUIMING_AFVOER": None,      # True/False
    # doelgroepdiensten (5.6); de pagina's hebben daarnaast hun eigen regel in PUBLICEER
    "STUDENTEN_DIENST": None,
    "SENIOREN_DIENST": None,
    "SPOED_DIENST": None,
}

# Taal en regio
TAAL = "nl"
LOCALE = "nl_NL"
THEMA_KLEUR = "#1746A2"
