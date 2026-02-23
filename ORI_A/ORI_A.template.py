import dataclasses

from dataclasses import Field, dataclass
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlTime

class Serializable:
    @classmethod
    def _ORI_A_ordered_fields(cls) -> list[Field]:
        """Return dataclass fields by their order in the ORI-A XSD.

        This method should be overridden when the order of fields in
        a dataclass does not match the order required by the ORI-A XSD.

        Such mismatches occur because Python only allows optional arguments
        at the _end_ of a function's signature, while schemas such as the
        ORI-A XSD allow optional attributes to appear anywhere.
        """
        return dataclasses.fields(cls)


@dataclass
class GremiumGegevens(Serializable):
    """{{docs.gremiumGegevens}}"""

    naam: str
    identificatie: str = None


@dataclass
class NaamGegevens(Serializable):
    """{{docs.naamGegevens}}"""

    achternaam: str
    tussenvoegsel: str = None
    voorletters: str = None
    voornamen: str = None
    volledigeNaam: str = None


@dataclass
class NevenfunctieGegevens(Serializable):
    """{{docs.nevenfunctieGegevens}}"""

    omschrijving: str
    naamOrganisatie: str = None
    aantalUrenPerMaand: int = None
    indicatieBezoldigd: bool = None
    indicatieFunctieVanwegeLidmaatschap: bool = None
    datumMelding: XmlDate = None
    datumAanvang: XmlDate = None
    datumEinde: XmlDate = None


@dataclass
class StemmingOverPersonenGegevens(Serializable):
    """{{docs.stemmingOverPersonenGegevens}}"""

    naamKandidaat: str
    aantalUitgebrachteStemmen: int = None


@dataclass
class VerwijzingGegevens(Serializable):
    """{{docs.verwijzingGegevens}}"""

    verwijzingID: str
    verwijzingNaam: str = None


@dataclass
class BegripGegevens(Serializable):
    """{{docs.begripGegevens}}"""

    begripLabel: str
    verwijzingBegrippenlijst: VerwijzingGegevens
    begripCode: str = None

    @classmethod
    def _ORI_A_ordered_fields(cls) -> list[Field]:
        """Sort dataclass fields by their order in the ORI-A XSD."""
        fields = super()._ORI_A_ordered_fields()
        # swap order of begripBegrippenlijst and begripCode
        return (fields[0], fields[2], fields[1])


@dataclass
class BesluitGegevens(Serializable):
    """{{docs.besluitGegevens}}"""

    ID: str | list[str]
    resultaat: BesluitResultaatEnum
    toelichting: str = None
    toezegging: str = None


@dataclass
class DagelijksBestuurLidmaatschapGegevens(Serializable):
    """{{docs.dagelijksBestuurLidmaatschapGegevens}}"""

    verwijzingDagelijksBestuur: VerwijzingGegevens
    ID: str | list[str] = None
    datumBeginDagelijksBestuurLidmaatschap: XmlDate = None
    datumEindeDagelijksBestuurLidmaatschap: XmlDate = None

    @classmethod
    def _ORI_A_ordered_fields(cls) -> list[Field]:
        """Sort dataclass fields by their order in the ORI-A XSD."""
        fields = super()._ORI_A_ordered_fields()
        # move first field to the back
        return fields[1:] + fields[:1]

@dataclass
class FractielidmaatschapGegevens(Serializable):
    """{{docs.fractielidmaatschapGegevens}}"""

    verwijzingFractie: VerwijzingGegevens
    ID: str | list[str] = None
    datumBeginFractielidmaatschap: XmlDate = None
    datumEindeFractielidmaatschap: XmlDate = None
    indicatieVoorzitter: bool = None


@dataclass
class StemGegevens(Serializable):
    """{{docs.stemGegevens}}"""

    keuzeStemming: KeuzeStemmingEnum
    gegevenOpStemming: VerwijzingGegevens
    ID: str | list[str] = None


@dataclass
class StemresultaatPerFractieGegevens(Serializable):
    """{{docs.stemresultaatPerFractieGegevens}}"""

    fractieStemresultaat: FractieStemresultaatEnum
    verwijzingStemming: VerwijzingGegevens
    ID: str | list[str] = None


@dataclass
class DagelijksBestuurGegevens(Serializable):
    """{{docs.dagelijksBestuurGegevens}}"""

    ID: str | list[str]
    naam: str
    overheidsorgaan: BegripGegevens
    type: BegripGegevens = None


@dataclass
class FractieGegevens(Serializable):
    """{{docs.fractieGegevens}}"""

    ID: str | list[str]
    naam: str
    overheidsorgaan: BegripGegevens = None
    neemtDeelAanStemming: StemresultaatPerFractieGegevens | list[StemresultaatPerFractieGegevens] = None


@dataclass
class InformatieobjectGegevens(Serializable):
    """{{docs.informatieobjectGegevens}}"""

    verwijzingInformatieobject: VerwijzingGegevens
    informatieobjectType: BegripGegevens = None


@dataclass
class NatuurlijkPersoonGegevens(Serializable):
    """{{docs.natuurlijkPersoonGegevens}}"""

    ID: str | list[str]
    naam: NaamGegevens
    geslachtsaanduiding: GeslachtsaanduidingEnum = None
    functie: BegripGegevens = None
    nevenfunctie: NevenfunctieGegevens | list[NevenfunctieGegevens] = None
    isLidVanFractie: FractielidmaatschapGegevens = None
    isLidVanDagelijksBestuur: DagelijksBestuurLidmaatschapGegevens = None


@dataclass
class StemmingGegevens(Serializable):
    """{{docs.stemmingGegevens}}"""

    ID: str | list[str]
    heeftBetrekkingOpAgendapunt: VerwijzingGegevens
    type: StemmingTypeEnum = None
    resultaatMondelingeStemming: ResultaatMondelingeStemmingEnum = None
    resultaatStemmingOverPersonen: str = None
    stemmingOverPersonen: StemmingOverPersonenGegevens | list[StemmingOverPersonenGegevens] = None
    leidtTotBesluit: VerwijzingGegevens = None
    heeftBetrekkingOpBesluitvormingsstuk: InformatieobjectGegevens | list[InformatieobjectGegevens] = None


@dataclass
class TijdsaanduidingGegevens(Serializable):
    """{{docs.tijdsaanduidingGegevens}}"""

    aanvang: int | XmlTime
    einde: int | XmlTime = None
    isRelatiefTot: InformatieobjectGegevens = None


@dataclass
class VergaderingGegevens(Serializable):
    """{{docs.vergaderingGegevens}}"""

    naam: str
    datum: XmlDate
    ID: str | list[str] = None
    geplandeDatum: XmlDate = None
    geplandeAanvang: XmlDateTime = None
    geplandEinde: XmlDateTime = None
    aanvang: XmlDateTime = None
    einde: XmlDateTime = None
    publicatiedatum: XmlDateTime = None
    type: BegripGegevens = None
    toelichting: str = None
    georganiseerdDoorGremium: GremiumGegevens = None
    locatie: str = None
    weblocatie: str = None
    status: VergaderingGegevensStatus = None
    overheidsorgaan: BegripGegevens = None
    isVastgelegdMiddels: InformatieobjectGegevens | list[InformatieobjectGegevens] = None
    isGenotuleerdIn: InformatieobjectGegevens = None
    heeftAlsBijlage: InformatieobjectGegevens | list[InformatieobjectGegevens] = None
    heeftAlsDeelvergadering: VergaderingGegevens | list[VergaderingGegevens] = None


@dataclass
class AgendapuntGegevens(Serializable):
    """{{docs.agendapuntGegevens}}"""

    ID: str | list[str]
    naam: str
    # TODO: check for "pattern": r"\d+.*",
    geplandVolgnummer: str = None
    # TODO: check for "pattern": r"\d+.*",
    volgnummer: str = None
    volgnummerWeergave: str = None
    omschrijving: str = None
    geplandeStarttijd: XmlDateTime = None
    geplandeEindtijd: XmlDateTime = None
    starttijd: XmlDateTime = None
    eindtijd: XmlDateTime = None
    tijdsaanduidingMediabron: TijdsaanduidingGegevens | list[TijdsaanduidingGegevens] = None
    locatie: str = None
    indicatieHamerstuk: bool = None
    indicatieBehandeld: bool = None
    indicatieBesloten: bool = None
    overheidsorgaan: BegripGegevens = None
    wordtBehandeldTijdens: VerwijzingGegevens = None
    heeftBehandelendAmbtenaar: VerwijzingGegevens | list[VerwijzingGegevens] = None
    heeftAlsBijlage: InformatieobjectGegevens | list[InformatieobjectGegevens] = None
    heeftAlsSubagendapunt: AgendapuntGegevens | list[AgendapuntGegevens] = None


@dataclass
class SpreekfragmentGegevens(Serializable):
    """{{docs.spreekfragmentGegevens}}"""

    gedurendeAgendapunt: VerwijzingGegevens | list[VerwijzingGegevens]
    ID: str | list[str] = None
    naam: str = None
    aanvang: XmlDateTime = None
    einde: XmlDateTime = None
    taal: str = None
    tekst: str = None
    positieNotulen: str = None
    tijdsaanduidingMediabron: TijdsaanduidingGegevens | list[TijdsaanduidingGegevens] = None


@dataclass
class AanwezigeDeelnemerGegevens(Serializable):
    """{{docs.aanwezigeDeelnemerGegevens}}"""

    isNatuurlijkPersoon: NatuurlijkPersoonGegevens
    ID: str | list[str] = None
    rolnaam: BegripGegevens = None
    organisatie: str = None
    deelnemerspositie: str = None
    aanvangAanwezigheid: XmlDateTime = None
    eindeAanwezigheid: XmlDateTime = None
    neemtDeelAanVergadering: VerwijzingGegevens | list[VerwijzingGegevens] = None
    neemtDeelAanStemming: StemGegevens | list[StemGegevens] = None
    spreektTijdensSpreekfragment: SpreekfragmentGegevens | list[SpreekfragmentGegevens] = None


# TODO: insert your monkeypatch here
@dataclass
class ORI_A(Serializable):
    """{{docs.ORI_A}}"""

    vergadering: VergaderingGegevens
    agendapunt: AgendapuntGegevens | list[AgendapuntGegevens]
    stemming: StemmingGegevens | list[StemmingGegevens] = None
    besluit: BesluitGegevens | list[BesluitGegevens] = None
    fractie: FractieGegevens | list[FractieGegevens] = None
    dagelijksBestuur: list[DagelijksBestuurGegevens] = None
    persoonBuitenVergadering: NatuurlijkPersoonGegevens | list[NatuurlijkPersoonGegevens] = None
    aanwezigeDeelnemer: AanwezigeDeelnemerGegevens | list[AanwezigeDeelnemerGegevens] = None


# TODO: generate docstrings for these as well (just a list of options is good)
# TODO: maybe make the case match values? (or give options for both; and/or add a UPPER_CASE variant)
class BesluitResultaatEnum(Enum):
    """{{docs.besluitResultaatEnum}}"""

    unaniem_aangenomen = "Unaniem aangenomen"
    aangenomen = "Aangenomen"
    geamendeerd_aangenomen = "Geamendeerd aangenomen"
    onder_voorbehoud_aangenomen = "Onder voorbehoud aangenomen"
    verworpen = "Verworpen"
    aangehouden = "Aangehouden"


class GeslachtsaanduidingEnum(Enum):
    """{{docs.geslachtsaanduidingEnum}}"""

    man = "Man"
    vrouw = "Vrouw"
    anders = "Anders"
    onbekend = "Onbekend"


class KeuzeStemmingEnum(Enum):
    """{{docs.keuzeStemmingEnum}}"""

    tegen = "Tegen"
    afwezig = "Afwezig"
    onthouden = "Onthouden"


class ResultaatMondelingeStemmingEnum(Enum):
    """{{docs.resultaatMondelingeStemmingEnum}}"""

    voor = "Voor"
    tegen = "Tegen"
    gelijk = "Gelijk"


class StemmingTypeEnum(Enum):
    """{{docs.stemmingTypeEnum}}"""

    hoofdelijk = "Hoofdelijk"
    regulier = "Regulier"
    schriftelijk = "Schriftelijk"


class FractieStemresultaatEnum(Enum):
    """{{docs.fractieStemresultaatEnum}}"""

    aangenomen = "Aangenomen"
    verworpen = "Verworpen"
    verdeeld = "Verdeeld"


class VergaderingStatusEnum(Enum):
    """{{docs.vergaderingStatusEnum}}"""

    gepland = "Gepland"
    gehouden = "Gehouden"
    geannuleerd = "Geannuleerd"
