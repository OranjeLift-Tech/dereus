"""Niet gevonden (404): drie grote links naar waar de meeste bezoekers heen willen, en de belregel.

Kopij: systeem.md, blok {#niet-gevonden}: lijst met regels "[tekst](/pad/)" en belregel.
De kop en de intro staan in het blok "kop" (zelfde kopij_id).
"""
import re

NAAM = "niet-gevonden"
CSS = True
JS = False

LINK = re.compile(r"^\[([^\]]+)\]\(([^)\s]+)\)\s*(.*)$")


def html(ctx, kopij, **opties) -> str:
    k = kopij
    kaarten = []
    for regel in k.lijst:
        m = LINK.match(regel)
        if not m:
            continue
        tekst, href, uitleg = m.groups()
        extra = " b-{0}__kaart--offerte".format(NAAM) if href.startswith("/offerte/") else ""
        kaarten.append(f'''<li><a class="b-{NAAM}__kaart{extra}" href="{ctx.esc(href)}">
              <span class="b-{NAAM}__tekst">{ctx.esc(tekst)}{f'<small>{ctx.inline(uitleg)}</small>' if uitleg else ""}</span>
              <span class="b-{NAAM}__pijl" aria-hidden="true">{ctx.icoon("pijl")}</span>
            </a></li>''')
    belregel = k.veld("belregel")
    return f'''<section class="b-{NAAM} sectie sectie--mist" aria-label="Verder op deze site">
      <div class="wrap">
        <ul class="b-{NAAM}__lijst" role="list" data-reveal-groep>{"".join(kaarten)}</ul>
        {ctx.belregel(belregel, klasse=f"belregel b-{NAAM}__bel")}
      </div>
    </section>'''
