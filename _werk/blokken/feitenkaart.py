"""Een kaart met lokale feiten: rijen "sleutel: waarde" en daaronder links (bijvoorbeeld naar de gemeente).

Sjablonen plaats (#lokaal) en land (#reis). Opties: kopij_id, grond ("wit" of "mist").
Kopij: label, intro, lijst. Een regel "- Parkeren: uitleg" wordt een rij; een regel die alleen een link is
("- [Verhuizing doorgeven](https://...)") komt in de linklijst. Regels met een onbekend feit heeft de kopijlezer
al weggelaten. Blijft er niets over, dan vervalt het hele blok: er staat nooit een lege kaart.
De feiten komen uit het onderzoek van dereus-e7; dit blok verzint niets.
"""
import re

NAAM = "feitenkaart"
CSS = True
JS = False

_LINK = re.compile(r"^\[[^\]]+\]\([^)\s]+\)\.?$")
_RIJ = re.compile(r"^(?:\*\*)?([^:*\[\]]{2,40}?)(?:\*\*)?:\s+(.+)$")


def html(ctx, kopij, **opties) -> str:
    k = kopij
    rijen, links, los = "", "", ""
    for regel in k.lijst:
        regel = regel.strip()
        m = _RIJ.match(regel)
        if _LINK.match(regel):
            links += f"<li>{ctx.inline(regel)}</li>"
        elif m:
            rijen += f'<div class="b-{NAAM}__rij"><dt>{ctx.inline(m.group(1))}</dt><dd>{ctx.inline(m.group(2))}</dd></div>'
        else:
            los += f"<li>{ctx.inline(regel)}</li>"
    if not (rijen or links or los or k.tekst):
        return ""
    grond = "mist" if opties.get("grond") == "mist" else "wit"
    rijen = f'<dl class="b-{NAAM}__rijen">{rijen}</dl>' if rijen else ""
    los = f'<ul class="b-{NAAM}__los">{los}</ul>' if los else ""
    linkkop = f'<h3 class="b-{NAAM}__linkkop">{ctx.inline(k.veld("linkkop"))}</h3>' if k.veld("linkkop") and links else ""
    links = f'{linkkop}<ul class="b-{NAAM}__links">{links}</ul>' if links else ""
    bron = f'<p class="b-{NAAM}__bron">{ctx.inline(k.veld("bron"))}</p>' if k.veld("bron") else ""
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap b-{NAAM}__in">
        <div class="b-{NAAM}__kop" data-reveal>{ctx.kopgroep(k)}{ctx.alineas(k.tekst)}</div>
        <div class="b-{NAAM}__kaart" data-reveal>{rijen}{los}{links}{bron}</div>
      </div>
    </section>'''
