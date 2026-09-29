"""Op de verhuisdag: de Koningsblauwe band met dakrand van /werkwijze/. De momenten van de dag als een korte,
liggende route met goudgele stippen. Geen tijden of aantallen: die staan niet vast.

Kopij: ## ... {#verhuisdag} met label, intro, slot en per moment een ###-item met tekst.
De dakrand hoort bij .sectie--blauw; zet dit blok daarom direct onder een witte sectie.

Twee indelingen, en welke het wordt hangt aan de kopij en niet aan een optie:

  route    De liggende stippenroute met de uitgesneden verhuizers naast het slot. Dit is wat er
           staat zolang niet elk moment een eigen beeld heeft.
  kaders   Elk moment krijgt een groot rechthoekig beeld, en de bovenranden van die kaders volgen
           de helling van de dakrand: het middelste kader staat op de nok, de buitenste zakken mee.
           Gekozen ronde 4, website/review/verhuisdag-ronde-4/.

De omslag is alles of niets: pas als *elk* moment een veld `beeld:` heeft en dat bestand bestaat,
gaat het blok naar kaders. Met twee beelden werkt het ontwerp niet, want bij twee kaders is de
zakking links en rechts gelijk en is er geen daklijn meer te zien; met één beeld is het een ander
ontwerp. Beter de route houden tot de serie compleet is dan een halve versie tonen.

Kopij met beeld ziet er zo uit:

    ### Aankomst
    beeld: verhuisdag-aankomst
    Onze verhuizers staan ...

Het pad wordt /img/<beeld>.webp. Maat: 4:3, 1400 bij 1050, en de drie opnames moeten onderling
gelijk uitgekaderd zijn (onderwerp ongeveer driekwart van de kaderhoogte, dezelfde ooghoogte,
hetzelfde licht), anders valt de rij uit elkaar.

Uit de foto (28-09-2026, gekozen ontwerp 09 "Rondom uit het kader" uit
_ontwerpen/verhuisdag-uit-de-foto.html). Heeft elk beeld een uitsnede in UITSNEDE, dan wordt het kader
een venster in de foto: de foto staat groter dan het kader en wordt erop geknipt, en de uitsnede
(zelfde maat en plek als de foto, img/verhuisdag-uit/) staat er los overheen maar is alleen BUITEN
het venster te zien. Hoofden steken boven het kader uit, voeten eronder, armen en bank opzij.
Waar het beeld komt te liggen rekent _venster() uit, uit de plaats van de mensen in de foto.

Het slot is dan geen losse regel meer maar een blok: elke afspraak een eigen helft met een
3D-voorwerp dat boven het blok uitkomt, en de verwijzing naar de voorwaarden als voet. De tekst
komt ongewijzigd uit de kopij; _afspraken() deelt hem alleen op in zinnen.

Optie grond (29-09-2026): "blauw" (standaard) of "geel". Geel is het Goudgeel van het logo, voor een
pagina die anders te blauw wordt; de dakrand blijft die van .sectie--blauw, alleen de kleuren wisselen
(blok "Goudgele band" onderaan css/blok/verhuisdag.css).
"""
import re

from kit import WORTEL

NAAM = "verhuisdag"
CSS = True
JS = False

# de uitgesneden verhuizers naast het slot; op blauw mag een uitsnede met slagschaduw (STIJLANALYSE 2.3)
FOTO = ("/img/verhuisdag-verhuizers.webp", 709, 787)
# de kaders in de indeling met beeld: 4:3, groot genoeg voor 3x op een kader van 465 px
KADERMAAT = (1400, 1050)
# De rij kaders loopt breder dan de tekstkolom. Dezelfde waarde staat in de CSS; hier gaat hij
# mee als --detail-inhoud, zodat de achtergrondlaag in css/style.css zijn vrije midden op de
# breedste inhoud van de sectie berekent en niet op de tekstkolom.
KADERBREEDTE = "1440px"

# Uit de foto: per beeld (naam uit de kopij) de uitsnede, de echte maat van de foto en waar de
# mensen staan, als deel van het beeld: kruin, voeten, links, rechts en midden.
UITSNEDE = {
    "dienst-particulier": ("/img/verhuisdag-uit/aankomst.webp", (720, 540), (1080, 810),
                           dict(top=0.338, bot=0.954, l=0.2, rgt=0.821, cx=0.51)),
    "dienst-internationaal": ("/img/verhuisdag-uit/inladen.webp", (720, 540), (1080, 810),
                              dict(top=0.214, bot=0.85, l=0.43, rgt=0.70, cx=0.56)),
    "stap-5-bank-voordeur": ("/img/verhuisdag-uit/uitladen.webp", (1120, 760), (1120, 760),
                             dict(top=0.134, bot=0.993, l=0.114, rgt=0.502, cx=0.36)),
}
# het venster: breedte/hoogte, en hoe ver kruin (boven) en voeten (onder) erbuiten staan, als deel
# van de vensterhoogte. Dezelfde drie getallen staan in de CSS (--ar, --u, --f).
VENSTER, BOVEN, ONDER = 1.6, 0.2, 0.1
# de voorwerpen bij de afspraken, in volgorde: betalen op de dag, schade
VOORWERPEN = [("/img/kosten-kalender/blok.webp", 449, 720), ("/img/contact-3d/schild.webp", 251, 320)]


def _venster(p, verhouding):
    """Schaal en plaats van het beeld achter het venster (breedte = 1, hoogte = 1).

    Het beeld wordt zo groot dat de kruin BOVEN en de voeten ONDER buiten het venster vallen en de
    foto het venster toch helemaal vult; opzij ligt het midden van de mensen in het midden.
    Terug: s (beeldbreedte), x, y (linksboven) en de vloerschaduw (links, breedte, hoogte voeten).
    """
    k = VENSTER / verhouding
    s = max(1.0, (1.012 + BOVEN) / (k * (1 - p["top"])), (1 + ONDER + BOVEN) / (k * (p["bot"] - p["top"])))
    y = -BOVEN - p["top"] * k * s
    start = min(max(p["cx"] - 0.5 / s, 0.0), 1 - 1 / s)
    voet = y + p["bot"] * k * s
    return s, -start * s, y, ((p["l"] - start) * s, (p["rgt"] - p["l"]) * s, voet)


def _uitsnedes(k):
    """Per moment de uitsnede, of None zodra er één ontbreekt (alles of niets, net als de kaders)."""
    uit = []
    for it in k.items:
        rij = UITSNEDE.get(it.veld("beeld").strip())
        if not rij or not (WORTEL / rij[0].lstrip("/")).exists():
            return None
        uit.append(rij)
    return uit


def _afspraken(ctx, tekst):
    """Het slot als blok. De zinnen blijven woord voor woord staan; een vraag hoort bij het antwoord
    erna, de laatste zin met een link wordt de voet, en het begin van elke afspraak (tot de eerste
    komma of het vraagteken) wordt vet."""
    zinnen = re.split(r"(?<=[.?!])\s+(?=[A-Z])", tekst.strip())
    voet = zinnen.pop() if len(zinnen) > 1 and "](" in zinnen[-1] else ""
    groepen = []
    for z in zinnen:
        if groepen and groepen[-1].endswith("?"):
            groepen[-1] += " " + z
        else:
            groepen.append(z)
    delen = []
    for i, g in enumerate(groepen):
        m = re.match(r"([^,?]{8,70}[,?])\s+(.*)", g)
        zin = f"<b>{ctx.inline(m.group(1))}</b> {ctx.inline(m.group(2))}" if m else ctx.inline(g)
        vw = ctx.beeld(*VOORWERPEN[i][:1], "", *VOORWERPEN[i][1:], klasse=f"b-{NAAM}__voorwerp") if i < len(VOORWERPEN) else ""
        delen.append(f'<div class="b-{NAAM}__afspraak">{vw}<p>{zin}</p></div>')
    voet = f'<p class="b-{NAAM}__voorwaarden">{ctx.icoon("check")}<span>{ctx.inline(voet)}</span></p>' if voet else ""
    return f'<div class="b-{NAAM}__afspraken"><div class="b-{NAAM}__afspraken-rij">{"".join(delen)}</div>{voet}</div>'


def _kaders(k):
    """De beelden per moment, of None zodra er één ontbreekt.

    Alles of niets: de daklijn is het middel van deze indeling en die vraagt drie kaders.
    """
    uit = []
    for it in k.items:
        naam = it.veld("beeld").strip()
        if not naam:
            return None
        pad = f"/img/{naam}.webp"
        if not (WORTEL / "img" / f"{naam}.webp").exists():
            return None
        uit.append(pad)
    return uit if len(uit) >= 3 else None


def _zak(i, aantal):
    """Hoe ver de bovenrand van kader i onder de nok zakt, als deel van de dakhoogte.

    De nok ligt op 50 procent van de breedte en de dakrand is aan beide randen --dak hoog, dus
    op positie x zakt de daklijn |x - 50| / 50. Het getal wordt hier uitgerekend en als
    --zak meegegeven, zodat de tekening van het dak en de plaatsing van de kaders uit hetzelfde
    getal komen en niet uit elkaar lopen bij een andere breedte of een ander aantal momenten.
    """
    midden = (i + 0.5) * 100 / aantal
    return f"{abs(midden - 50) / 50:.4f}"


def html(ctx, kopij, grond="blauw", **opties) -> str:
    k = kopij
    geel = f" b-{NAAM}--geel" if grond == "geel" else ""
    beelden = _kaders(k)

    uitsnedes = _uitsnedes(k) if beelden else None
    if uitsnedes:
        aantal = len(k.items)
        li = []
        for i, it in enumerate(k.items):
            uit_src, (fb, fh), (ub, uh), p = uitsnedes[i]
            s, x, y, (vl, vb, voet) = _venster(p, fb / fh)
            foto = ctx.beeld(beelden[i], "", fb, fh, klasse=f"b-{NAAM}__foto-in")
            uit = ctx.beeld(uit_src, "", ub, uh, klasse=f"b-{NAAM}__uit")
            li.append(
                f'<li class="b-{NAAM}__moment" style="--zak:{_zak(i, aantal)};--i:{i}">'
                f'<span class="b-{NAAM}__kader" aria-hidden="true" style="--s:{s:.4f};--x:{x:.4f};--y:{y:.4f}">'
                f'<span class="b-{NAAM}__raam">{foto}</span>'
                f'<span class="b-{NAAM}__vloer" style="left:{vl * 100:.2f}%;width:{vb * 100:.2f}%;top:{(voet - 0.05) * 100:.2f}%"></span>'
                f'<span class="b-{NAAM}__buiten">{uit}</span></span>'
                f'<h3 class="b-{NAAM}__titel">{ctx.inline(it.titel)}</h3>{ctx.alineas(it.tekst)}</li>')
        slot = _afspraken(ctx, k.veld("slot")) if k.veld("slot") else ""
        return f'''<section class="b-{NAAM} b-{NAAM}--kaders b-{NAAM}--uit sectie sectie--blauw{geel}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}" style="--detail-inhoud:{KADERBREEDTE}">
      <div class="wrap">
        {ctx.kopgroep(k, "kopgroep--midden")}
        {ctx.alineas(k.tekst, "b-" + NAAM + "__tekst")}
        <ol class="b-{NAAM}__dag" role="list" style="--aantal:{max(1, aantal)}" data-reveal-groep>{"".join(li)}</ol>
        {slot}
      </div>
    </section>'''

    if beelden:
        aantal = len(k.items)
        momenten = "".join(
            f'<li class="b-{NAAM}__moment" style="--zak:{_zak(i, aantal)};--i:{i}">'
            f'<span class="b-{NAAM}__kader" aria-hidden="true">'
            f'{ctx.beeld(beelden[i], "", *KADERMAAT)}</span>'
            f'<h3 class="b-{NAAM}__titel">{ctx.inline(it.titel)}</h3>{ctx.alineas(it.tekst)}</li>'
            for i, it in enumerate(k.items))
        slot = f'<p class="b-{NAAM}__slot">{ctx.inline(k.veld("slot"))}</p>' if k.veld("slot") else ""
        return f'''<section class="b-{NAAM} b-{NAAM}--kaders sectie sectie--blauw{geel}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}" style="--detail-inhoud:{KADERBREEDTE}">
      <div class="wrap">
        {ctx.kopgroep(k, "kopgroep--midden")}
        {ctx.alineas(k.tekst, "b-" + NAAM + "__tekst")}
        <ol class="b-{NAAM}__dag" role="list" style="--aantal:{max(1, aantal)}" data-reveal-groep>{momenten}</ol>
        {slot}
      </div>
    </section>'''

    momenten = "".join(
        f'<li class="b-{NAAM}__moment"><span class="b-{NAAM}__stip" aria-hidden="true"></span>'
        f'<h3 class="b-{NAAM}__titel">{ctx.inline(it.titel)}</h3>{ctx.alineas(it.tekst)}</li>'
        for it in k.items)
    slot = f'<p class="b-{NAAM}__slot">{ctx.inline(k.veld("slot"))}</p>' if k.veld("slot") else ""
    if slot:
        src, breedte, hoogte = FOTO
        beeld = ctx.beeld(src, "", breedte, hoogte)      # sier: alles wat telt staat in de tekst ernaast
        slot = f'<div class="b-{NAAM}__afsluiter"><span class="b-{NAAM}__foto">{beeld}</span>{slot}</div>'
    return f'''<section class="b-{NAAM} sectie sectie--blauw{geel}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        {ctx.kopgroep(k, "kopgroep--midden")}
        {ctx.alineas(k.tekst, "b-" + NAAM + "__tekst")}
        <ol class="b-{NAAM}__dag" role="list" style="--aantal:{max(1, len(k.items))}" data-reveal-groep>{momenten}</ol>
        {slot}
      </div>
    </section>'''
