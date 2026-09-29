"""/over-ons/: kop met de offertepil over de onderrand (zoals Brocken en referentie A), het verhaal met de
verhuizers op twee platen en drie feitenkaarten (about-address-team, sinds 28-09-2026), de actielijn van de home
(sinds 29-09-2026), de kernwaarden als
gedrag (Koningsblauw met dakrand: een uitgelichte waarde met de verhuizers die uit de foto stappen, de
overige als rijen ernaast), reviews, Den Haag met de kaart (Diepblauw met dakrand) en het grote offerteformulier
van de home (blok aanvraag, sinds 28-09-2026; daarvoor de offertekaart "Kennismaken?").

Feiten (config.FEITEN): OPRICHTINGSJAAR, EIGENAAR, TEAM, RECHTSVORM en KVK verschijnen onder het verhaal zodra
ze bekend zijn. Tot die tijd blijven ze weg. TEAM_BEELD leest het verhaal sinds 28-09-2026 niet meer.
"""
from kit import Pagina

PAGINA = Pagina(
    pad="/over-ons/",
    kopij="over-ons",
    header="transparant",
    body_klasse="p-over-ons",
    feiten=("OPRICHTINGSJAAR", "EIGENAAR", "TEAM", "RECHTSVORM", "KVK"),
    # over-naden: de schuine overgangen tussen de secties van deze pagina (29-09-2026), alleen hier geladen.
    # "reviews-ster" (de 3D-ster op de uitgelichte review) hoort bij het reviewblok "reviews"; zet hem terug als dat
    # blok hieronder weer aan gaat.
    extra_css=("over-naden",),
    blokken=[
        ("kop", {}),
        ("offertepil", {"variant": "los", "over_kop": True, "kopij": None}),
        # feiten: False sinds 28-09-2026, toen het KvK-nummer in config.FEITEN kwam: "Sterk waar het zwaar is" blijft zoals
        # goedgekeurd, zonder feitenrijen. Het KvK-nummer staat in de footer, op /contact/ en in de JSON-LD.
        ("over-ons", {"kopij_id": "verhaal", "feiten": False, "motto": False}),
        # De actielijn van de home, met dezelfde kopij (home.md, #cijfers): "add action line to the diensten and over-ons
        # pages". Plek A gekozen op 29-09-2026 (website/review/actielijn-over-ons-20260929/): na het verhaal, voor het
        # blad. Geen .sectie, dus de motieftellers blijven gelijk; de lichtblauwe grond eronder regelt actielijn.css.
        ("actielijn", {"kopij": None, "kopij_van": ("home", "cijfers")}),
        # Sinds 28-09-2026 het blad met de vakman en vijf kaarten: versie 5 uit website/review/zowerkenwij-20260928/,
        # met ronde 2 en 3 ("Take r3 onto /over-ons/"). Hiervoor stond hier
        # ("kernwaarden", {"kopij_id": "zo-werken-wij", "foto": "particulier-v2", "compact": "krap"}); dat blok bestaat nog.
        # voorwerpen="echt": de echte voorwerpen van Tugche (8971f9e) in gele tegels in plaats van de klei-iconen
        ("waardenblad", {"kopij_id": "zo-werken-wij", "voorwerpen": "echt"}),
        # Wit sinds 29-09-2026: tussen het lichtblauwe blad (#F3F7FE) en de grijze Mist (#F6F7F9) was de naad niet te zien
        # (hooguit 5 punten verschil per kleurkanaal). Op wit wordt de schuine rand eronder een echte overgang. Zie over-naden.css.
        # het reviewblok van /werkwijze/ (scorepodium + rail, referentie B) sinds 29-09-2026: de klant wilde het in
        # alle reviewsecties (Tugche, 8971f9e; na de samenvoeging van 29-09-2026 teruggezet).
        ("reviewrail", {"kopij_id": "reviews", "sectie": "wit", "accent": "over ons zeggen"}),
        # variant A, aan door deze regel te wisselen met de regel erboven (en "reviews-ster" terug in extra_css):
        # ("reviews", {"sectie": "wit"}),
        # keuze A (28-09-2026): de drie regels van de home. Van werkgebied r2 alleen de routelijn: het adres staat in de
        # intro en de routeknop eronder, en het grote formulier volgt direct, dus geen adresplaat en geen knoppen.
        ("werkgebied", {"kopij_id": "den-haag", "regels_van": ("home", "werkgebied"), "alineas": False,
                        "adresplaat": False, "acties": False, "voorwerpen": "echt"}),
        # Sinds 28-09-2026 het grote formulier van de home, zoals home.py het aanroept. De gebruiker: "replace the small
        # form in /over-ons/ with the big one from homepage". Hiervoor stond hier ("offertepil", {"variant": "los",
        # "kopij_id": "contact"}), "Kennismaken?"; die kopij in over-ons.md blijft staan, ongebruikt.
        # Met het klembord van de home op de kaart (29-09-2026): "Vertel ons over uw verhuizing section - homepage version
        # has list clay icon, it should always be 100% opacity [...] also add it to diensten en over-ons pages too."
        ("naadiconen", {"kopij": None, "blok": "aanvraag", "opties": {"kopij": None},
                        "plek": ("aanvraag", [("klembord", "hoek", -14, -52)], "b-formulier__kaart")}),
    ],
)
