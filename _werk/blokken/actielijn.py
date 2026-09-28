"""Actielijn: een schuine blauwe streep met vier korte feiten, elk met een klei-icoon.
Gebruikt op de home (#cijfers, in plaats van de cijferband) en op /contact/ (#vertrouwen, in plaats van de
vertrouwensrij). Bron: section-library/slanted-action-line. De oude blokken cijfers.py en vertrouwensrij.py
staan er nog, maar geen pagina gebruikt ze.

Kopij: een ##-blok met een kop die alleen voor schermlezers is, en vier ###-items (titel + tekst:).
Het icoon volgt uit titel en tekst samen; zonder treffer het klembord.
Opties: id (standaard het id van het kopijblok); sectie=True maakt het een .sectie .sectie--wit. Dat telt dan mee
in de motieftellers van style.css (nth-child of .sectie), dus alleen waar het vorige blok er ook een was: /contact/.
Op de home was de cijferband geen .sectie; met de klasse erbij schuiven de motieven van alle secties eronder op.
"""

NAAM = "actielijn"
CSS = True
JS = False

# Het klei-icoon per feit (img/clay/<naam>-144/240.webp, vierkant). Sinds 28-09-2026 in plaats van de Solar-iconen in
# het goudgele huis: "add the r3 action line, but use the clay icons instead". Eerste treffer wint, gezocht in titel +
# tekst in kleine letters. De munten (voorrijkosten) en de vakman (verhuisadviseur) zijn later die dag gemaakt en
# goedgekeurd ("Goedgekeurd voor de site: icoon 2 en 4", website/review/clay-munt-persoon-20260928/); daarvoor stonden
# daar de verhuiswagen en de headset. Voor bereikbaar staat nog de telefoon.
ICOON = [("uit 5", "ster"), ("google", "ster"), ("verzeker", "schild"), ("adviseur", "vakman"),
         ("per week", "telefoon"), ("bereikbaar", "telefoon"), ("24 uur", "klok"), ("bellen", "klok"),
         ("voorrijkosten", "munten"), ("€", "munten")]


# Lange samenstellingen krijgen een zacht afbreekstreepje op de naad. Op 20% grotere maat past "verhuisadviseur" niet
# meer in een kolom van vier (1100 tot 1920) en niet naast het huis op een telefoon; zo breekt het als "verhuis-" en
# "adviseur" in plaats van over de rand te lopen. Werkt in elke browser, ook zonder woordenboek voor hyphens:auto.
AFBREEK = {"verhuisadviseur": "verhuis\u00adadviseur"}


def _kop(ctx, titel):
    tekst = ctx.inline(titel)
    for woord, gebroken in AFBREEK.items():
        tekst = tekst.replace(woord, gebroken)
    # data-afbreek: zo'n kop loopt gewoon door in plaats van gebalanceerd (zie actielijn.css)
    return f"<b data-afbreek>{tekst}</b>" if "\u00ad" in tekst else f"<b>{tekst}</b>"


def _icoon(tekst):
    t = tekst.lower()
    for sleutel, naam in ICOON:
        if sleutel in t:
            return naam
    return "klembord"


def _klei(naam):
    # 4 rem op het scherm, 3,12 rem op een telefoon (actielijn.css); 144 dekt 2x, 240 een telefoon op 3x
    return (f'<img src="/img/clay/{naam}-144.webp" srcset="/img/clay/{naam}-144.webp 144w, /img/clay/{naam}-240.webp 240w" '
            f'sizes="(max-width: 560px) 3.12rem, 4rem" alt="" width="144" height="144" loading="lazy" decoding="async">')


def html(ctx, kopij, **opties) -> str:
    k = kopij
    sid = ctx.esc(opties.get("id", k.id))
    feiten = "".join(f'''<li class="b-{NAAM}__feit">
            <span class="b-{NAAM}__ic" aria-hidden="true">{_klei(_icoon(it.titel + " " + it.veld("tekst")))}</span>
            <p>{_kop(ctx, it.titel)}{f"<span>{ctx.inline(it.veld('tekst'))}</span>" if it.veld("tekst") else ""}</p>
          </li>''' for it in k.items)
    klasse = f"b-{NAAM} sectie sectie--wit" if opties.get("sectie") else f"b-{NAAM}"
    return f'''<section class="{klasse}" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="b-{NAAM}__streep">
        <div class="wrap">
          <h2 class="vh" id="{sid}-kop">{ctx.inline(k.kop)}</h2>
          <ul class="b-{NAAM}__lijst" role="list" data-reveal-groep>{feiten}
          </ul>
        </div>
      </div>
    </section>'''
