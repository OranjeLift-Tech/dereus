"""Over De Reus, "Sterk waar het zwaar is": het patroon about-address-team uit ../section-library, de
hergebruikskandidaat die de gebruiker op 28-09-2026 hield (Reuse 2 in
website/review/sterk-waar-het-zwaar-is-20260928/, oorspronkelijk solargreen-www section.sgoo-team).

Sinds de tweede ronde van 28-09-2026 twee kolommen. Links bovenaan drie verhuizers als uitsnede op twee
platen (TEAM), daaronder de kop, de alinea's en de adresregel "Hoofdkantoor: ...". Rechts een feitenkaart
per ### item van het blok, met een icoon uit het veld "icoon"; de kaarten rekken over de hoogte van beeld
plus tekst. Ze dragen alleen feiten die al op de site staan (zie de notities in over-ons.md). Sinds
28-09-2026 is het icoon een klei-icoon ("Sterk waar het zwaar is - add clay icons to this"), zie KLEI. Gestapeld
(onder 900 px) volgen beeld, tekst en kaarten elkaar in die volgorde op.

Twee plekken:
  /over-ons/ #verhaal  het verhaal; met optie feiten=True komen de bevestigde feiten onder de adresregel
                       (OPRICHTINGSJAAR, EIGENAAR, TEAM, RECHTSVORM, KVK uit config.FEITEN; onbekend = geen rij)
  home #over-ons       sinds 23-09-2026 letterlijk dezelfde sectie, via kopij_van=("over-ons", "verhaal")
Knoppen alleen als het blok de velden knop of linktekst (met link) heeft; #verhaal heeft ze nu niet.

Het beeld: dezelfde uitsnede als op de reviewkaart van /diensten/, drie verhuizers met een rechte snede
door de heupen, precies wat het patroon verwacht. Gegenereerd, geen foto van de echte ploeg. Sinds 29-09-2026
(SEO-ronde) beschrijft de alt wat er te zien is, zonder te zeggen wie het zijn; tot dan was hij leeg.
config.FEITEN["TEAM_BEELD"] (het oude huisvenster) leest dit blok niet
meer; een echte teamfoto hoort hier pas als hij ook als uitsnede bestaat.
Opties: feiten (False), sectie ("wit").
"""
NAAM = "over-ons"
CSS = True
JS = False

# pad, breedte, hoogte en alt. De alt zegt niet wie het zijn: het beeld is gegenereerd. Zelfde opbouw als
# TEAM_BEELD_ALT in config.py.
TEAM = ("/img/review-verhuizers-lachend-breed.webp", 914, 504,
        "Illustratief beeld van drie lachende verhuizers in blauwe polo's met het logo van De Reus")

FEITRIJEN = [
    ("OPRICHTINGSJAAR", "Opgericht in", "kalender"),
    ("EIGENAAR", "Eigenaar", "persoon"),
    ("TEAM", "Team", "doos"),
    ("RECHTSVORM", "Rechtsvorm", "document"),
    ("KVK", "KvK-nummer", "document"),
]


# Het klei-icoon bij het veld icoon: van de 19 goedgekeurde (img/clay/<naam>-144/240.webp, vierkant;
# website/review/clay-iconen-20260928/). Bij de vakmensen de vakman met de doos en bij geen voorrijkosten de
# munten, goedgekeurd op 28-09-2026 (website/review/clay-munt-persoon-20260928/, "icoon 2 en 4"); daarvoor
# stonden daar het gereedschap (montage) en de verhuiswagen (nationaal). Een icoon zonder klei-tweeling houdt
# het lijnicoon.
KLEI = {"persoon": "vakman", "schild": "schild", "telefoon": "telefoon", "euro": "munten", "klok": "klok"}


def _icoon(ctx, naam):
    klei = KLEI.get(naam)
    if not klei:
        return f'<span class="over__icoon">{ctx.icoon(naam)}</span>'
    return (f'<span class="over__icoon over__icoon--klei"><img class="over__klei" src="/img/clay/{klei}-144.webp" '
            f'srcset="/img/clay/{klei}-144.webp 144w, /img/clay/{klei}-240.webp 240w" sizes="4.25rem" alt="" '
            f'width="144" height="144" loading="lazy" decoding="async"></span>')


def feitenlijst(ctx):
    rijen = [(label, ctx.feit(naam), icoon) for naam, label, icoon in FEITRIJEN if ctx.feit(naam) is not None]
    if not rijen:
        return ""
    li = "".join(f'<li>{ctx.icoon(icoon)}<span>{ctx.esc(label)}</span><b>{ctx.esc(str(w))}</b></li>' for label, w, icoon in rijen)
    return f'<ul class="over__feiten" role="list">{li}</ul>'


def kaarten(ctx, k):
    if not k.items:
        return ""
    li = "".join(f'''<li class="over__kaart">{_icoon(ctx, it.eis("icoon"))}
          <div><h3>{ctx.inline(it.titel)}</h3><p>{ctx.inline(it.eis("tekst"))}</p></div></li>''' for it in k.items)
    return f'<ul class="over__kaarten" role="list" data-reveal-groep>{li}</ul>'


def html(ctx, kopij, feiten=False, sectie="wit", kopij_van=None, team=TEAM, **opties):
    k = kopij
    anker = k.id
    if kopij_van:
        # Sinds 23-09-2026 toont de home letterlijk de sectie van /over-ons/: "Sterk waar het zwaar is in
        # homepage should be copy of Sterk waar het zwaar is in /over-ons/". De tekst komt dan uit dat
        # blok, zodat hij op één plek staat en de twee niet uit elkaar lopen. Het anker blijft dat van de
        # eigen pagina (#over-ons op de home), de kop houdt het id uit de bron.
        pagina, kid = kopij_van
        k = ctx.kopij_van(pagina).blok(kid)
    cfg = ctx.cfg
    knoppen = []
    if k.veld("knop"):
        knoppen.append(ctx.knop(k.veld("knop"), "/offerte/"))
    if k.veld("linktekst") and ctx.live(k.veld("link", "/over-ons/")):
        knoppen.append(ctx.knop(k.veld("linktekst"), k.veld("link", "/over-ons/"), soort="licht"))
    elif knoppen:
        knoppen.append(ctx.belknop("licht"))
    src, b, h, alt = team
    return f'''<section class="sectie sectie--{sectie} b-over" id="{ctx.esc(anker)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    <div class="over__rij">
      <div class="over__links">
        <div class="over__podium" data-reveal>
          <span class="over__platen" aria-hidden="true"></span>
          {ctx.beeld(src, alt, b, h, klasse="over__team")}
        </div>
        <div class="over__kop" data-reveal>
          {ctx.kopgroep(k)}
          <div class="over__alineas">{ctx.alineas(k.tekst)}</div>
          <p class="over__adres">{ctx.icoon("pin")}<span>Hoofdkantoor: {ctx.esc(cfg.STRAAT)}, {ctx.esc(cfg.PLAATS)}</span></p>
          {feitenlijst(ctx) if feiten else ""}
          {f'<div class="knoppen">{"".join(knoppen)}</div>' if knoppen else ""}
        </div>
      </div>
      {kaarten(ctx, k)}
    </div>
  </div>
</section>'''
