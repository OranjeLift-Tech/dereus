"""Wat u vooraf kunt regelen (/diensten/particuliere-verhuizingen/ #voorbereiding), sinds 29-09-2026 op de testlijn.
Naar het patroon vacancy-detail-card (Solar Green) uit ../section-library: een witte kaart met de kop, drie kolommen
met een klei-icoon en de punten, en een balk met de vraag en de belknop. Geclaimd als #2 in
_werk/dienstsecties-register.md.

Kopij: werkwijze.md {#voorbereiding} (live op /werkwijze/), via kopij_van: label, intro, slot en de zes punten als lijst
("**Titel.** tekst"). De balk is het slot: de eerste zin (tot en met het vraagteken) wordt de titel, de rest de alinea.
De drie kolomtitels zijn eigen tekst van dereus-28; ze groeperen de punten, twee per kolom (KOLOMMEN).
Opties: kopij_van=(document, blok-id).
"""
import re

NAAM = "voorbereidkaart"
CSS = True
JS = False

# (kolomtitel, klei-icoon, de vetgedrukte titels van de punten zonder punt), in deze volgorde
KOLOMMEN = [
    ("Vooraf melden", "formulier", ("Meld alles wat belangrijk is", "Gevaarlijke stoffen vooraf melden")),
    ("Zelf regelen", "vakman", ("Gas laten afkoppelen", "Opvang voor uw huisdieren")),
    ("Bij het inpakken", "dozen", ("Dozen met een kamernaam", "Belangrijke spullen bij u")),
]
PUNT = re.compile(r"^\*\*(.+?)\.?\*\*\s*(.*)$", re.S)


def _klei(ctx, n):
    return ctx.beeld(f"/img/clay/{n}-144.webp", "", 144, 144, klasse="vbk__klei",
                     srcset=f"/img/clay/{n}-144.webp 144w, /img/clay/{n}-240.webp 240w",
                     sizes="(max-width: 900px) 3.5rem, 4.25rem")


def html(ctx, kopij, kopij_van=("werkwijze", "voorbereiding"), **opties):
    k = ctx.kopij_van(kopij_van[0]).blok(kopij_van[1])
    punten = {}
    for regel in k.lijst:
        m = PUNT.match(regel)
        if not m:
            raise ValueError(f"voorbereidkaart: punt zonder vetgedrukte titel: {regel!r}")
        punten[m.group(1)] = m.group(2)
    over = set(punten) - {t for _, _, ts in KOLOMMEN for t in ts}
    if over:
        raise ValueError(f"voorbereidkaart: punten zonder kolom: {sorted(over)}; zet ze in KOLOMMEN")
    kolommen = []
    for titel, klei, ts in KOLOMMEN:
        li = "".join(f'<li>{ctx.icoon("check")}<span><strong>{ctx.inline(t)}</strong><span>{ctx.inline(punten[t])}</span></span></li>'
                     for t in ts if t in punten)
        kolommen.append(f'''
        <li class="vbk__kolom">{_klei(ctx, klei)}<h3>{ctx.esc(titel)}</h3><ul class="vbk__punten" role="list">{li}</ul></li>''')
    slot = k.veld("slot") or ""
    vraag, _, rest = slot.partition("?")
    balk = (f'<div><h3>{ctx.inline(vraag + "?")}</h3><p>{ctx.inline(rest.strip())}</p></div>' if rest
            else f'<div><p>{ctx.inline(slot)}</p></div>')
    return f'''<section class="sectie sectie--mist b-{NAAM}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    <div class="vbk__kaart" data-reveal>
      <div class="vbk__kop"><div>{ctx.label(k.veld("label"))}<h2 id="{ctx.esc(k.id)}-kop">{ctx.inline(k.kop)}</h2></div>{f'<p class="intro">{ctx.inline(k.veld("intro"))}</p>' if k.veld("intro") else ""}</div>
      <ul class="vbk__kolommen" role="list">{"".join(kolommen)}
      </ul>
      <div class="vbk__balk">{balk}<div class="vbk__knoppen">{ctx.belknop(soort="blauw")}</div></div>
    </div>
  </div>
</section>'''
