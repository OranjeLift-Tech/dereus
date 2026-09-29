"""Tips voor een soepele kantoorverhuizing (/diensten/zakelijke-verhuizingen/ #tips), sinds 29-09-2026 op de testlijn.
Naar het patroon text-benefit-cards (Solar Green) uit ../section-library: een crème band met de kop naast een witte
tekstkaart, daaronder de tips als kaarten met een klei-icoon dat linksboven uit de kaart steekt; de laatste kaart is
goud. Geclaimd als #4 in _werk/dienstsecties-register.md.

Kopij: diensten-zakelijk.md, via kopij_van, want de pagina leest diensten.md. {#tips}: label, intro en de tips als
lijst ("**Titel.** tekst"). De tekstkaart is een vraag uit {#vragen} (optie vraag, op titel), met de belknop eronder.
Opties: kopij_van=(document, blok-id), vraag (de ###-titel in {#vragen}).
"""
import re

NAAM = "tipkaarten"
CSS = True
JS = False

# klei-icoon per tip (img/clay/<naam>-144/240.webp), op de vetgedrukte titel zonder punt
KLEI = {"Wijs een vast aanspreekpunt aan": "headset", "Geef elke doos een plek": "dozen", "Ruim vooraf op": "woningontruiming",
        "Laat uw medewerkers hun bureau leegmaken": "envelop"}
TIP = re.compile(r"^\*\*(.+?)\.?\*\*\s*(.*)$", re.S)


def _klei(ctx, titel):
    n = KLEI.get(titel)
    if not n:
        raise ValueError(f"tipkaarten: geen klei-icoon voor tip {titel!r}, zet er een in KLEI")
    return ctx.beeld(f"/img/clay/{n}-144.webp", "", 144, 144, klasse="tipk__klei",
                     srcset=f"/img/clay/{n}-144.webp 144w, /img/clay/{n}-240.webp 240w",
                     sizes="(max-width: 560px) 3.75rem, 5.25rem")


def html(ctx, kopij, kopij_van=("diensten-zakelijk", "tips"), vraag="Verhuizen jullie ook grote kantoren?", **opties):
    doc = ctx.kopij_van(kopij_van[0])
    k = doc.blok(kopij_van[1])
    tips = []
    for regel in k.lijst:
        m = TIP.match(regel)
        if not m:
            raise ValueError(f"tipkaarten: tip zonder vetgedrukte titel: {regel!r}")
        tips.append((m.group(1), m.group(2)))
    if not 3 <= len(tips) <= 6:
        raise ValueError(f"tipkaarten: 3 tot 6 tips, niet {len(tips)}")
    v = next((it for it in doc.blok("vragen").items if it.titel == vraag), None)
    if v is None:
        raise ValueError(f"tipkaarten: vraag {vraag!r} staat niet in {kopij_van[0]}.md #vragen")
    kaarten = "".join(f'''
      <li class="tipk__item"><div class="tipk__kaart">{_klei(ctx, titel)}<h3>{ctx.inline(titel)}</h3><p>{ctx.inline(tekst)}</p></div></li>'''
                      for titel, tekst in tips)
    return f'''<section class="sectie sectie--wit b-{NAAM}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    <div class="tipk__rij">
      <div class="tipk__kop" data-reveal>{ctx.label(k.veld("label"))}<h2 id="{ctx.esc(k.id)}-kop">{ctx.inline(k.kop)}</h2>{f'<p class="intro">{ctx.inline(k.veld("intro"))}</p>' if k.veld("intro") else ""}</div>
      <div class="tipk__vraag" data-reveal><h3>{ctx.inline(v.titel)}</h3>{ctx.alineas(v.tekst)}{ctx.belknop(soort="link")}</div>
    </div>
    <ul class="tipk__kaarten" role="list" data-reveal-groep>{kaarten}
    </ul>
  </div>
</section>'''
