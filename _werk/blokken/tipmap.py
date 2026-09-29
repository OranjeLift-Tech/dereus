"""Regel dit op tijd (/diensten/internationale-verhuizingen/ #op-tijd), sinds 29-09-2026 op de testlijn. Nieuw patroon
tip-sheets-pocket (/section, ../section-library/tip-sheets-pocket): vier tips als vellen papier in een map, de voorkant
van de map over hun onderrand met een zin en de offerteknop. Elk vel heeft een klei-icoon over de rechterbovenhoek.
Geclaimd als #8 in _werk/dienstsecties-register.md.

Kopij: dienstsecties-internationaal.md {#op-tijd}, via kopij_van (de pagina leest diensten.md): label, intro, de tips als
lijst ("**Titel.** tekst"), voet (de zin op de voorkant) en knop. De bron per zin staat in dat bestand.
Opties: kopij_van=(document, blok-id), href (de offerteknop, zoals die van het paneel).
"""
import re

NAAM = "tipmap"
CSS = True
JS = False

# klei-icoon per tip (img/clay/<naam>-144/240.webp), op de vetgedrukte titel zonder punt
KLEI = {"Uitschrijven bij uw gemeente": "zakelijk", "Inschrijven als u naar Nederland komt": "particulier",
        "Papieren bij de hand": "envelop", "Adres in het buitenland": "nationaal"}
TIP = re.compile(r"^\*\*(.+?)\.?\*\*\s*(.*)$", re.S)


def _klei(ctx, titel):
    n = KLEI.get(titel)
    if not n:
        raise ValueError(f"tipmap: geen klei-icoon voor tip {titel!r}, zet er een in KLEI")
    return ctx.beeld(f"/img/clay/{n}-144.webp", "", 144, 144, klasse="tm__klei",
                     srcset=f"/img/clay/{n}-144.webp 144w, /img/clay/{n}-240.webp 240w",
                     sizes="(max-width: 560px) 3.75rem, 4.25rem")


def html(ctx, kopij, kopij_van=("dienstsecties-internationaal", "op-tijd"), href="/offerte/?dienst=internationaal", **opties):
    k = ctx.kopij_van(kopij_van[0]).blok(kopij_van[1])
    tips = []
    for regel in k.lijst:
        m = TIP.match(regel)
        if not m:
            raise ValueError(f"tipmap: tip zonder vetgedrukte titel: {regel!r}")
        tips.append((m.group(1), m.group(2)))
    if len(tips) != 4:
        raise ValueError(f"tipmap: vier tips, niet {len(tips)} (de rijregels in tipmap.css gaan uit van vier)")
    vellen = "".join(f'''
        <li class="tm__vel"><div class="tm__blad">{_klei(ctx, titel)}<h3>{ctx.inline(titel)}</h3><p>{ctx.inline(tekst)}</p></div></li>'''
                     for titel, tekst in tips)
    return f'''<section class="sectie sectie--mist b-{NAAM}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    {ctx.kopgroep(k, klasse="tm__kop")}
    <div class="tm__map">
      <ul class="tm__vellen" role="list" data-reveal-groep>{vellen}
      </ul>
      <div class="tm__voor" data-reveal>
        <p>{ctx.inline(k.eis("voet"))}</p>
        {ctx.knop(k.eis("knop"), href)}
      </div>
    </div>
  </div>
</section>'''
