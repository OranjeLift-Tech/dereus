"""/ (home): hero met offertepil, diensten, waarom, werkwijze, reviews, over ons, werkgebied en vragen.

Banden (review dereus-70, D3): Mist, Wit, Koningsblauw met dakrand (werkwijze), Mist, Wit,
Diepblauw met dakrand (werkgebied), Mist. Nooit twee donkere banden naast elkaar, en licht voor de footer.
De beeldblokken, cijfers, aanvraag en contact uit main zijn opgenomen in de gedeelde bouwstraat.
"""
import config as cfg
import kit
from kit import Pagina


def _preload():
    """Het teambeeld is de LCP: preload de webp in de juiste maat (zelfde sizes als het blok hero)."""
    if not getattr(cfg, "HERO_TEAM", None):
        return None
    r = kit.responsief(cfg.HERO_TEAM)
    return {"href": r["webp"], "imagesrcset": r["srcset"], "imagesizes": kit.HERO_SIZES, "type": "image/webp"}

PAGINA = Pagina(
    pad="/",
    kopij="home",
    header="transparant",
    body_klasse="p-home",
    preload_beeld=_preload(),
    blokken=[
        ("hero", {"kopij_id": "offerte"}),
        ("diensten", {}),
        ("waarom", {}),
        ("cijfers", {}),
        ("werkwijze", {}),
        ("reviews", {}),
        ("over-ons", {}),
        ("werkgebied", {}),
        ("vragen", {"beeld": "headset-huis"}),
        ("aanvraag", {"kopij": None}),
        ("homecontact", {"kopij_id": "contact"}),
    ],
)
