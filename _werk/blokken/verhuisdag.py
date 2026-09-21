"""Op de verhuisdag: de Koningsblauwe band met dakrand van /werkwijze/. De momenten van de dag als een korte,
liggende route met goudgele stippen. Geen tijden of aantallen: die staan niet vast.

Kopij: ## ... {#verhuisdag} met label, intro, slot en per moment een ###-item met tekst.
De dakrand hoort bij .sectie--blauw; zet dit blok daarom direct onder een witte sectie.
"""

NAAM = "verhuisdag"
CSS = True
JS = False

# de uitgesneden verhuizers naast het slot; op blauw mag een uitsnede met slagschaduw (STIJLANALYSE 2.3)
FOTO = ("/img/verhuisdag-verhuizers.webp", 709, 787)


def html(ctx, kopij, **opties) -> str:
    k = kopij
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
