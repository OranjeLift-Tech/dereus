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
"""
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


def html(ctx, kopij, **opties) -> str:
    k = kopij
    beelden = _kaders(k)

    if beelden:
        aantal = len(k.items)
        momenten = "".join(
            f'<li class="b-{NAAM}__moment" style="--zak:{_zak(i, aantal)};--i:{i}">'
            f'<span class="b-{NAAM}__kader" aria-hidden="true">'
            f'{ctx.beeld(beelden[i], "", *KADERMAAT)}</span>'
            f'<h3 class="b-{NAAM}__titel">{ctx.inline(it.titel)}</h3>{ctx.alineas(it.tekst)}</li>'
            for i, it in enumerate(k.items))
        slot = f'<p class="b-{NAAM}__slot">{ctx.inline(k.veld("slot"))}</p>' if k.veld("slot") else ""
        return f'''<section class="b-{NAAM} b-{NAAM}--kaders sectie sectie--blauw" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}" style="--detail-inhoud:{KADERBREEDTE}">
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
    return f'''<section class="b-{NAAM} sectie sectie--blauw" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        {ctx.kopgroep(k, "kopgroep--midden")}
        {ctx.alineas(k.tekst, "b-" + NAAM + "__tekst")}
        <ol class="b-{NAAM}__dag" role="list" style="--aantal:{max(1, len(k.items))}" data-reveal-groep>{momenten}</ol>
        {slot}
      </div>
    </section>'''
