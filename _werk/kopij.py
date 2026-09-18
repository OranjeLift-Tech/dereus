"""Leest de teksten uit website/content/*.md (formaat: website/BOUWPLAN.md, hoofdstuk 7).

Een bestand:
    ---
    titel: ...
    beschrijving: ...
    ---
    # Kop van de pagina {#id}        blok met de H1
    ## Kop {#id}                     blok, de kop wordt een H2
    ### Titel {#id}                  item binnen het laatste blok
    sleutel: waarde                  veld (kleine letters, koppeltekens)
    gewone regels                    alinea's van het veld "tekst"
    - regel                          het veld "lijst"
    Notitie: ...                     genegeerd, net als <!-- commentaar -->

Feiten van de klant (config.FEITEN, BOUWPLAN 12):
    {NAAM}                           in tekst, veldwaarde of lijstregel: wordt ingevuld; is het feit
                                     onbekend (None/False/leeg), dan valt die alinea, dat veld of die regel weg
    als: NAAM                        de volgende alinea of lijstregel alleen als het feit bekend of waar is
    tenzij: NAAM                     de volgende alinea of lijstregel alleen als het feit onbekend of onwaar is
    alleen-als: NAAM                 op een ## blok of ### item: het hele blok of item alleen als het feit er is
"""
import re
from pathlib import Path

WORTEL = Path(__file__).resolve().parent.parent
MAP = WORTEL / "website" / "content"

FEIT = re.compile(r"\{([A-Z][A-Z0-9_]*)\}")


def _feiten():
    import config
    return getattr(config, "FEITEN", {})


def _bekend(naam, bestand):
    alle = _feiten()
    if naam not in alle:
        raise BouwFout(f"{bestand}: onbekend feit '{naam}' (voeg het toe aan config.FEITEN)")
    w = alle[naam]
    return w not in (None, False, "") and not (isinstance(w, (list, tuple)) and not w)


def vul(tekst, bestand="?"):
    """Vul {NAAM} in uit config.FEITEN. Geeft None als een van de feiten onbekend is."""
    ontbreekt = False

    def zet(m):
        nonlocal ontbreekt
        naam = m.group(1)
        if not _bekend(naam, bestand):
            ontbreekt = True
            return ""
        w = _feiten()[naam]
        if isinstance(w, (list, tuple)):
            w = [str(x) for x in w]
            return w[0] if len(w) == 1 else ", ".join(w[:-1]) + " en " + w[-1]
        return str(w)

    uit = FEIT.sub(zet, tekst)
    return None if ontbreekt else uit


KOP = re.compile(r"^(#{1,3})\s+(.*?)\s*(?:\{#([a-z0-9][a-z0-9-]*)\})?\s*$")
VELD = re.compile(r"^([a-z][a-z0-9-]*):\s*(.*)$")


class BouwFout(Exception):
    pass


class Blok:
    """Een blok (## of #) of een item (###)."""

    def __init__(self, bestand, niveau, kop, id_):
        self.bestand = bestand
        self.niveau = niveau          # 1 = H1-blok, 2 = blok, 3 = item
        self.kop = kop                # tekst van de kopregel
        self.id = id_
        self.velden = {}
        self.tekst = []               # alinea's
        self.lijst = []
        self.items = []
        self._alinea = []
        self._voorwaarde = None       # (als|tenzij, NAAM) voor de alinea die nu loopt
        self.alleen_als = None        # NAAM: blok of item alleen tonen als het feit bekend is

    # ---- lezen --------------------------------------------------------
    def veld(self, naam, standaard=""):
        if naam == "titel" and "titel" not in self.velden:
            return self.kop or standaard
        if naam == "tekst" and "tekst" not in self.velden:
            # tekst: komt als alinea in .tekst terecht; veld("tekst") geeft die alinea's als één regel
            return " ".join(self.tekst) or standaard
        return self.velden.get(naam, standaard)

    def eis(self, naam):
        waarde = self.veld(naam, None)
        if waarde in (None, ""):
            raise BouwFout(f"{self.bestand}: blok #{self.id} mist het veld '{naam}'")
        return waarde

    def heeft(self, naam):
        return bool(self.velden.get(naam))

    def item(self, id_):
        for it in self.items:
            if it.id == id_:
                return it
        raise BouwFout(f"{self.bestand}: blok #{self.id} heeft geen item #{id_}")

    @property
    def titel(self):
        return self.veld("titel")

    def __repr__(self):
        return f"<Blok #{self.id} '{self.kop}' velden={list(self.velden)} items={len(self.items)}>"

    # ---- opbouwen -----------------------------------------------------
    def _sluit_alinea(self):
        if self._alinea:
            tekst = " ".join(self._alinea)
            if _mag(self._voorwaarde, self.bestand):
                tekst = vul(tekst, self.bestand)
                if tekst is not None:
                    self.tekst.append(tekst)
            self._alinea = []
            self._voorwaarde = None


def _mag(voorwaarde, bestand):
    if not voorwaarde:
        return True
    soort, naam = voorwaarde
    bekend = _bekend(naam, bestand)
    return bekend if soort == "als" else not bekend


class Leeg(Blok):
    """Staat in voor een blok dat (nog) niet in de kopij staat. Velden geven de standaardwaarde."""

    def __init__(self, bestand, id_):
        super().__init__(bestand, 2, "", id_)


class Document:
    def __init__(self, naam, pad):
        self.naam = naam
        self.pad = pad
        self.meta = {}
        self.blokken = []
        self.verborgen = set()        # ids van blokken die door alleen-als wegvallen

    def heeft(self, id_):
        return any(b.id == id_ for b in self.blokken)

    def blok(self, id_):
        for b in self.blokken:
            if b.id == id_:
                return b
        raise BouwFout(f"{self.pad.name}: geen blok met id #{id_} (wel: {', '.join(b.id for b in self.blokken)})")

    def blok_of_leeg(self, id_):
        return self.blok(id_) if self.heeft(id_) else Leeg(self.pad.name, id_)

    @property
    def h1(self):
        for b in self.blokken:
            if b.niveau == 1:
                return b
        return None

    @property
    def titel(self):
        return self.meta.get("titel", "")

    @property
    def beschrijving(self):
        return self.meta.get("beschrijving", "")


def lees(naam):
    """Lees website/content/<naam>.md. Bestaat het bestand niet, dan een leeg document."""
    pad = MAP / f"{naam}.md"
    doc = Document(naam, pad)
    if not pad.exists():
        return doc
    tekst = pad.read_text(encoding="utf-8")
    tekst = re.sub(r"<!--.*?-->", "", tekst, flags=re.S)
    regels = tekst.splitlines()

    i = 0
    # voorkant
    while i < len(regels) and not regels[i].strip():
        i += 1
    if i < len(regels) and regels[i].strip() == "---":
        i += 1
        while i < len(regels) and regels[i].strip() != "---":
            m = VELD.match(regels[i].strip())
            if m:
                waarde = vul(m.group(2).strip(), pad.name)
                if waarde is not None:
                    doc.meta[m.group(1)] = waarde
            i += 1
        i += 1

    huidig_blok = None
    huidig = None          # het blok of item dat nu gevuld wordt
    teller = {}
    voorwaarde = None      # na "als: NAAM" of "tenzij: NAAM": geldt voor de volgende alinea of lijstregel
    for ruw in regels[i:]:
        regel = ruw.rstrip()
        kaal = regel.strip()
        if kaal.startswith("Notitie:"):
            continue
        m = KOP.match(kaal)
        if m and not kaal.startswith("####"):
            niveau = len(m.group(1))
            kop, id_ = m.group(2).strip(), m.group(3)
            if huidig:
                huidig._sluit_alinea()
            voorwaarde = None
            if niveau in (1, 2):
                if not id_:
                    raise BouwFout(f"{pad.name}: kop '{kaal}' heeft geen {{#id}}")
                huidig_blok = Blok(pad.name, niveau, kop, id_)
                doc.blokken.append(huidig_blok)
                huidig = huidig_blok
            else:
                if huidig_blok is None:
                    raise BouwFout(f"{pad.name}: item '{kaal}' staat buiten een blok")
                if not id_:
                    teller[huidig_blok.id] = teller.get(huidig_blok.id, 0) + 1
                    id_ = f"item-{teller[huidig_blok.id]}"
                item = Blok(pad.name, 3, kop, id_)
                huidig_blok.items.append(item)
                huidig = item
            continue
        if huidig is None:
            continue
        if not kaal:
            huidig._sluit_alinea()
            continue
        mv = VELD.match(kaal)
        if mv and not huidig._alinea:
            sleutel, waarde = mv.group(1), mv.group(2).strip()
            if sleutel in ("als", "tenzij"):
                _bekend(waarde, pad.name)          # controleert de naam
                voorwaarde = (sleutel, waarde)
                continue
            if sleutel == "alleen-als":
                _bekend(waarde, pad.name)
                huidig.alleen_als = waarde
                continue
            if sleutel == "tekst":
                huidig._sluit_alinea()
                if _mag(voorwaarde, pad.name):
                    waarde = vul(waarde, pad.name)
                    if waarde is not None:
                        huidig.tekst.append(waarde)
                voorwaarde = None
            else:
                waarde = vul(waarde, pad.name)
                if waarde is not None:
                    huidig.velden[sleutel] = waarde
            continue
        if kaal.startswith("- "):
            huidig._sluit_alinea()
            if _mag(voorwaarde, pad.name):
                regel = vul(kaal[2:].strip(), pad.name)
                if regel is not None:
                    huidig.lijst.append(regel)
            voorwaarde = None
            continue
        if not huidig._alinea:
            huidig._voorwaarde = voorwaarde
            voorwaarde = None
        huidig._alinea.append(kaal)
    if huidig:
        huidig._sluit_alinea()
    # alleen-als: blokken en items waarvan het feit onbekend is, vallen weg
    for b in list(doc.blokken):
        if b.alleen_als and not _bekend(b.alleen_als, pad.name):
            doc.blokken.remove(b)
            doc.verborgen.add(b.id)
            continue
        b.items = [it for it in b.items if not (it.alleen_als and not _bekend(it.alleen_als, pad.name))]
    return doc


_CACHE = {}


def document(naam):
    if naam not in _CACHE:
        _CACHE[naam] = lees(naam)
    return _CACHE[naam]


if __name__ == "__main__":
    import sys
    for naam in sys.argv[1:] or ["home"]:
        d = lees(naam)
        print(naam, d.meta)
        for b in d.blokken:
            print(" ", b, b.tekst[:1], b.lijst[:3])
            for it in b.items:
                print("    ", it, (it.tekst[:1] or [""])[0][:60])
