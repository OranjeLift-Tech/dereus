"""/diensten/: kop met ankerchips, acht diensten, reviews (scorepodium + rail, zoals de home) en het grote offerteformulier
van de home (blok aanvraag)."""
import kopij as _kopij
from kit import Pagina

DIENSTEN = ["particulier", "zakelijk", "nationaal", "internationaal", "verhuislift", "opslag", "montage", "woningontruiming"]


def _chips():
    """De chiptekst is het veld label van elk dienstblok (anders de kop). Het derde deel is de dienstsleutel: elke
    chip krijgt het Solar-ikoon van zijn dienst (28-09-2026, de gebruiker: "nav in diensten, use different icons for
    each section, use the small icons, not the clay ones.")."""
    doc = _kopij.document("diensten")
    return [(doc.blok(d).veld("label") or doc.blok(d).kop, f"#{d}", d) for d in DIENSTEN if doc.heeft(d)]


PAGINA = Pagina(
    pad="/diensten/",
    kopij="diensten",
    header="transparant",
    body_klasse="p-diensten",
    # "reviews-ster" (de 3D-ster op de uitgelichte review) hoort bij het reviewblok "reviews"; zet hem terug als dat
    # blok hieronder weer aan gaat.
    blokken=[
        ("kop", {"chips": _chips()}),
        ("dienstenpanelen", {"kopij_ids": DIENSTEN}),
        # het reviewblok van /werkwijze/ (scorepodium + rail, referentie B) sinds 29-09-2026: de klant wilde het in
        # alle reviewsecties
        ("reviewrail", {"kopij_id": "reviews", "sectie": "wit", "accent": "klanten zeggen"}),
        # variant A met de ploeg achter het scorepaneel (28-09-2026), aan door deze regel te wisselen met de regel
        # erboven (en "reviews-ster" terug in extra_css):
        # ("reviews", {"sectie": "wit"}),
        # Sinds 28-09-2026 het grote formulier van de home, zoals home.py het aanroept. De gebruiker: "Welke dienst u
        # ook kiest, één aanspreekpunt in diensten - replace it with the big one in homepage - "Vertel ons over uw
        # verhuizing"". Hiervoor stond hier ("offertepil", {"variant": "los"}); de kopij daarvan (diensten.md,
        # #offertepil) blijft staan, ongebruikt.
        ("aanvraag", {"kopij": None}),
    ],
)
