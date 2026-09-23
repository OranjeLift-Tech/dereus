"""Over De Reus: tekst links, rechts een huisvenster in Koningsblauw met het negatieve beeldmerk en het motto
"Geen verhuizing te groot!" (config.MOTTO). Het motto staat nooit in hetzelfde blok als de pay-off.

Twee plekken:
  home #over-ons     korte teaser met knop en de link "Meer over De Reus" (velden knop, linktekst, link)
  /over-ons/ #verhaal  het verhaal; met optie feiten=True komen de bevestigde feiten eronder
                       (OPRICHTINGSJAAR, EIGENAAR, TEAM, RECHTSVORM, KVK uit config.FEITEN; onbekend = geen rij)
Huisvenster: staat FEITEN["TEAM_BEELD"] op een pad, dan toont het venster dat beeld, met
FEITEN["TEAM_BEELD_ALT"] als alt-tekst. Die twee horen bij elkaar en moeten samen vervangen worden:
het bijschrift beschrijft wat er in beeld is en claimt niet wie het zijn. Er staat nu een gegenereerd
beeld van fictieve verhuizers, geen foto van de echte ploeg.
De home gebruikt anders de bestaande illustratieve uitsnede, zonder een teamidentiteit te claimen.
Opties: feiten (False), motto (True), sectie ("wit").
"""
NAAM = "over-ons"
CSS = True
JS = False

FEITRIJEN = [
    ("OPRICHTINGSJAAR", "Opgericht in", "kalender"),
    ("EIGENAAR", "Eigenaar", "persoon"),
    ("TEAM", "Team", "doos"),
    ("RECHTSVORM", "Rechtsvorm", "document"),
    ("KVK", "KvK-nummer", "document"),
]


def feitenlijst(ctx):
    rijen = [(label, ctx.feit(naam), icoon) for naam, label, icoon in FEITRIJEN if ctx.feit(naam) is not None]
    if not rijen:
        return ""
    li = "".join(f'<li>{ctx.icoon(icoon)}<span>{ctx.esc(label)}</span><b>{ctx.esc(str(w))}</b></li>' for label, w, icoon in rijen)
    return f'<ul class="over__feiten" role="list">{li}</ul>'


def html(ctx, kopij, feiten=False, motto=True, sectie="wit", kopij_van=None, **opties):
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
    b, h = cfg.LOGO_MATEN["beeldmerk"]
    knoppen = []
    if k.veld("knop"):
        knoppen.append(ctx.knop(k.veld("knop"), "/offerte/"))
    if k.veld("linktekst") and ctx.live(k.veld("link", "/over-ons/")):
        knoppen.append(ctx.knop(k.veld("linktekst"), k.veld("link", "/over-ons/"), soort="licht"))
    elif knoppen:
        knoppen.append(ctx.belknop("licht"))
    tekst_motto = getattr(cfg, "MOTTO", "") if motto else ""
    foto = ctx.feit("TEAM_BEELD")
    if foto:
        # De alt-tekst komt uit de config, naast het beeld zelf, want alleen daar is bekend wat er te zien is.
        # Zonder alt-tekst laten we hem leeg: liever niets zeggen dan iets beweren wat het beeld niet waarmaakt.
        venster = (f'<div class="huisvenster over__foto">{ctx.beeld(foto, ctx.feit("TEAM_BEELD_ALT") or "", 1200, 1140)}</div>')
    else:
        venster = f'''<div class="over__huis">
        <img class="over__merk" src="{ctx.logo("beeldmerk-negatief")}" alt="Het beeldmerk van De Reus: een huis met twee sterke armen" width="{b}" height="{h}" loading="lazy" decoding="async">
        {f'<p class="over__motto">{ctx.esc(tekst_motto)}</p>' if tekst_motto else ""}
      </div>'''
    return f'''<section class="sectie sectie--{sectie} b-over" id="{ctx.esc(anker)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap over">
    <div class="over__tekst" data-reveal>
      {ctx.kopgroep(k)}
      <div class="over__alineas">{ctx.alineas(k.tekst)}</div>
      {feitenlijst(ctx) if feiten else ""}
      {f'<div class="knoppen">{"".join(knoppen)}</div>' if knoppen else ""}
    </div>
    <figure class="over__beeld" data-reveal>
      {venster}
      <figcaption class="over__adres">{ctx.icoon("pin")}<span>Hoofdkantoor: {ctx.esc(cfg.STRAAT)}, {ctx.esc(cfg.PLAATS)}</span></figcaption>
    </figure>
  </div>
</section>'''
