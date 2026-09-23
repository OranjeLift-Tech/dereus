"""Stappen na de aanvraag (/offerte/): wat er gebeurt nadat u het formulier verstuurt, plus de Google-pil.

Kopij: offerte.md, blok {#na-aanvraag}: intro, belregel en drie ###-items (titel + tekst).
De Google-pil gebruikt de score uit config.py ("4,9 uit 5 op Google", zonder aantal) en linkt naar
GOOGLE_PROFIEL, dezelfde bestemming als "Bekijk alle reviews op Google" in het blok reviews. Let op:
die constante is een Google-zoekopdracht en geen bedrijfsprofiel; zodra de klant de echte profiel-URL
aanlevert, is config.py de enige plek die verandert.

Vorm: drie stations op een goudgele lijn, elk met een 3D-voorwerp dat op het huis uit het logo staat,
en links daarvan een verhuizer op een blauw vlak. Gekozen uit ronde 1 (website/review/offerte-ronde-1/,
versie 6, "de tijdlijn met de verhuizer erbij"); de vijf versies en de meetcijfers staan daar.

Waarom deze vorm: de vorige had drie kaarten op een gestippelde route die op dezelfde hoogte lag als de
blauwe balk boven elke kaart, dus de route las als streepje, balk, streepje, balk, en hij liep uit op
een los beeldmerk in een vierde kolom. De stations met een voorwerp op het huis zijn dezelfde taal als
"Van aanvraag tot verhuisdag" op /werkwijze/, waar hetzelfde verhaal staat.

De voorwerpen staan hier vast, zoals in het blok tijdlijn: telefoon bij "wij bellen u", klembord bij het
gesprek, formulier bij de offerte. De figuur is een uitsnede van dereus-79 (23-09-2026, gegenereerd met
gemini-3-pro-image-preview, merk uit brandbook/assets/logo/ er later op gezet, geen stockfoto).
"""

NAAM = "stappen-na-aanvraag"
CSS = True
JS = False

# Per station een 3D-render: map, bestandsnaam, breedte en hoogte. Dezelfde reeks als op /contact/.
VOORWERPEN = [
    ("contact-3d", "telefoon", 208, 400),
    ("kaart-3d", "klembord", 600, 792),
    ("contact-3d", "formulier", 346, 400),
]

# De verhuizer links. Wit gerande dozen, dus het vlak eronder is blauw (zie de CSS).
FIGUUR = ("/img/verhuizer-steekwagen-uit.webp", 734, 1200)


def _station(ctx, it, nr):
    map_, naam, breedte, hoogte = VOORWERPEN[(nr - 1) % len(VOORWERPEN)]
    beeld = ctx.beeld(f"/img/{map_}/{naam}.webp", "", breedte, hoogte,
                      klasse=f"b-{NAAM}__obj b-{NAAM}__obj--{naam}")
    return f'''<li class="b-{NAAM}__stap">
              <span class="b-{NAAM}__ic" aria-hidden="true">{beeld}</span>
              <div class="b-{NAAM}__plaat">
                <p class="b-{NAAM}__nr" aria-hidden="true">0{nr}</p>
                <h3 class="b-{NAAM}__titel">{ctx.inline(it.kop)}</h3>
                {ctx.alineas(it.tekst, klasse=f"b-{NAAM}__regel")}
              </div>
            </li>'''


def html(ctx, kopij, **opties) -> str:
    k = kopij
    sid = opties.get("id", k.id)
    stations = "".join(_station(ctx, it, i) for i, it in enumerate(k.items, 1))
    src, breedte, hoogte = FIGUUR
    figuur = ctx.beeld(src, "", breedte, hoogte)
    belregel = k.veld("belregel")
    return f'''<section class="b-{NAAM} sectie sectie--wit" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap">
        {ctx.kopgroep(k, klasse=f"b-{NAAM}__kop")}
        <div class="b-{NAAM}__raam">
          <div class="b-{NAAM}__beeld" aria-hidden="true">{figuur}</div>
          <ol class="b-{NAAM}__rij" role="list" data-reveal-groep>{stations}</ol>
          <div class="b-{NAAM}__voet">
            {ctx.belregel(belregel, klasse=f"belregel b-{NAAM}__bel")}
            <a class="b-{NAAM}__google" href="{ctx.esc(ctx.cfg.GOOGLE_PROFIEL)}" rel="noopener" target="_blank">{ctx.icoon("google", klasse="ic b-" + NAAM + "__g")}{ctx.sterren(klasse="sterren b-" + NAAM + "__sterren")}<span><strong>{ctx.esc(ctx.cfg.GOOGLE_SCORE)}</strong> uit 5 op Google</span><span class="vh"> (opent Google in een nieuw tabblad)</span></a>
          </div>
        </div>
      </div>
    </section>'''
