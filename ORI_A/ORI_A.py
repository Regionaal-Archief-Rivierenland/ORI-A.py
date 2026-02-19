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
    """Gegevens over een gremium.

    Attributes:
        naam: Naam van het gremium, zoals 'Commissie Samenleving'.
        identificatie: Uniek identificatiekenmerk van het gremium.
    """

    naam: str
    identificatie: str = None


@dataclass
class NaamGegevens(Serializable):
    """Gegevens over de naam van een persoon, zoals diens voor- en achternaam.

    Attributes:
        achternaam: De achternaam van de persoon, zoals `Mierlo`.
        tussenvoegsel: Het tussenvoegsel in de naam van de persoon, zoals `van
          der`.
        voorletters: De voorletters van de persoon, zoals `J.P.` of `K.`.
        voornamen: De voornaam of voornamen van de persoon, zoals `Anna Maria
          Sophia` of `Jan`.
        volledigeNaam: De volledige naam van de persoon, zoals `Piet van der
          Berg`.
    """

    achternaam: str
    tussenvoegsel: str = None
    voorletters: str = None
    voornamen: str = None
    volledigeNaam: str = None


@dataclass
class NevenfunctieGegevens(Serializable):
    """Gegevens over een nevenfunctie van een persoon, zoals of het om een betaalde
    functie gaat.

    Attributes:
        omschrijving: Informatie over de inhoud van iemands nevenfunctie, zoals de
          officiële functietitel of een korte beschrijving.
        naamOrganisatie: De naam van de organisatie waarbinnen de nevenfunctie
          wordt uitgevoerd.
        aantalUrenPerMaand: Aantal uren per maand dat besteed wordt aan de
          nevenfunctie.
        indicatieBezoldigd: Geeft aan of de nevenfunctie wordt uitgevoerd tegen
          betaling.
        indicatieFunctieVanwegeLidmaatschap: Geeft aan of de nevenfunctie wordt
          vervuld vanwege iemands lidmaatschap aan het betreffende
          overheidsorgaan.
        datumMelding: Datum waarop de nevenfunctie gemeld is bij de griffie.
        datumAanvang: Datum waarop iemand met de nevenfunctie begon.
        datumEinde: Datum waarop iemands nevenfunctie wordt/is beëindigd.
    """

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
    """Gegevens die een stemming over personen beschrijven, zoals het aantal stemmen dat
    een kandidaat haalde.

    Attributes:
        naamKandidaat: Naam van de kandidaat waarover gestemd werd.
        aantalUitgebrachteStemmen: Aantal stemmen dat de kandidaat gehaald heeft.
    """

    naamKandidaat: str
    aantalUitgebrachteStemmen: None | int = None


@dataclass
class VerwijzingGegevens(Serializable):
    """Gegevens om vanuit een entiteit naar een ander te verwijzen.

    Attributes:
        verwijzingID: Het ID van de entiteit waarnaar verwezen wordt.
        verwijzingNaam: Een voor menselijke lezers bedoelde naam van de entiteit
          waarnaar verwezen wordt.
    """

    verwijzingID: str
    verwijzingNaam: str = None


@dataclass
class BegripGegevens(Serializable):
    """Gegevens over een begrip, zoals de locatie van de begrippenlijst waar het begrip
    verklaard wordt.

    Attributes:
        begripLabel: Het label dat aan het begrip is toegekend in de
          begrippenlijst.
        verwijzingBegrippenlijst: Een verwijzing naar de begrippenlijst waarin het
          begrip beschreven wordt. Het ID van de begrippenlijst waarnaar verwezen
          wordt is meestal een URL, en de gewenste naam de titel van de
          begrippenlijst (bijvoorbeeld 'ORI-A vergaderstuktypes').
        begripCode: De code die aan het begrip is toegekend in de begrippenlijst.
    """

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
    """Gegevens over een besluit, zoals of het unaniem aangenomen of verworpen is. Een
    besluit volgt in de regel op een `stemming`.

    Attributes:
        ID: Uniek identificatiekenmerk van het besluit.
        resultaat: Het resultaat van het besluit.
        toelichting: Een toelichting op het besluit.
        toezegging: Een toezegging die bij het besluit gedaan is.
    """

    ID: str | list[str]
    resultaat: BesluitResultaatEnum
    toelichting: str = None
    toezegging: str = None


@dataclass
class DagelijksBestuurLidmaatschapGegevens(Serializable):
    """Gegevens over wanneer iemand lid is geworden van een bepaald dagelijks bestuur.

    Attributes:
        verwijzingDagelijksBestuur: Verwijzing naar het dagelijks bestuur waar het
          lidmaatschap betrekking op heeft.
        ID: Uniek identificatiekenmerk van het dagelijks bestuur lidmaatschap.
        datumBeginDagelijksBestuurLidmaatschap: Datum waarop iemands lidmaatschap
          van het dagelijks bestuur begon.
        datumEindeDagelijksBestuurLidmaatschap: Datum waarop iemands lidmaatschap
          van het dagelijks bestuur eindigde.
    """

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
    """Gegevens over iemands fractielidmaatschap.

    Attributes:
        verwijzingFractie: Verwijzing naar de fractie waar het lidmaatschap
          betrekking op heeft.
        ID: Uniek identificatiekenmerk van het fractielidmaatschap.
        datumBeginFractielidmaatschap: Datum waarop iemands fractielidmaatschap
          begon.
        datumEindeFractielidmaatschap: Datum waarop iemands fractielidmaatschap
          eindigde.
        indicatieVoorzitter: Geeft aan of iemand fractievoorzitter is.
    """

    verwijzingFractie: VerwijzingGegevens
    ID: str | list[str] = None
    datumBeginFractielidmaatschap: XmlDate = None
    datumEindeFractielidmaatschap: XmlDate = None
    indicatieVoorzitter: bool = None


@dataclass
class StemGegevens(Serializable):
    """Gegevens over een stem die iemand heeft uitgebracht, zoals diens stemkeuze en de
    stemming waarop deze keuze betrekking heeft.

    Attributes:
        keuzeStemming: De keuze op de stemming.
        gegevenOpStemming: Verwijzing naar de stemming waar de stem betrekking op
          heeft.
        ID: Uniek identificatiekenmerk van de stem.
    """

    keuzeStemming: KeuzeStemmingEnum
    gegevenOpStemming: VerwijzingGegevens
    ID: str | list[str] = None


@dataclass
class StemresultaatPerFractieGegevens(Serializable):
    """Gegevens over hoe een fractie als geheel tegenover een stemming stond, zoals of de
    aanwezigen leden unaniem voor, unaniem tegen, of juist verdeeld hebben
    gestemd.

    Attributes:
        fractieStemresultaat: Geeft aan hoe de fractie als geheel tegenover een
          stemming stond.
        verwijzingStemming: Verwijzing naar de stemming waar de fractie aan heeft
          deelgenomen.
        ID: Uniek identificatiekenmerk van het stemresultaat per fractie.
    """

    fractieStemresultaat: FractieStemresultaatEnum
    verwijzingStemming: VerwijzingGegevens
    ID: str | list[str] = None


@dataclass
class DagelijksBestuurGegevens(Serializable):
    """Gegevens over een dagelijks bestuur, zoals de naam van het bestuur.

    Attributes:
        ID: Uniek identificatiekenmerk van het dagelijks bestuur.
        naam: Naam van het dagelijks bestuur.
        overheidsorgaan: Het overheidsorgaan waarbinnen dit dagelijks bestuur
          opereert.
        type: Het soort dagelijks bestuur.
    """

    ID: str | list[str]
    naam: str
    overheidsorgaan: BegripGegevens
    type: BegripGegevens = None


@dataclass
class FractieGegevens(Serializable):
    """Gegevens over een fractie, zoals de naam en het stemgedrag van de fractie.

    Attributes:
        ID: Uniek identificatiekenmerk van de fractie.
        naam: De naam van de fractie, zoals `D66` of `VVD`.
        overheidsorgaan: Het overheidsorgaan waarbinnen de fractie opereert.
        neemtDeelAanStemming: Gegevens over hoe de fractie als geheel tegenover
          een stemming stond, zoals of de aanwezigen leden unaniem voor, unaniem
          tegen, of juist verdeeld hebben gestemd.
    """

    ID: str | list[str]
    naam: str
    overheidsorgaan: BegripGegevens = None
    neemtDeelAanStemming: list[StemresultaatPerFractieGegevens] = None


@dataclass
class InformatieobjectGegevens(Serializable):
    """Gegevens die worden gebruikt om te **verwijzen** naar een elders gedefinieerd
    informatieobject.

    Attributes:
        verwijzingInformatieobject: Verwijzing naar een elders gedefinieerd
          informatieobject.
        informatieobjectType: Het soort informatieobject waarnaar verwezen wordt.
    """

    verwijzingInformatieobject: VerwijzingGegevens
    informatieobjectType: BegripGegevens = None


@dataclass
class NatuurlijkPersoonGegevens(Serializable):
    """Gegevens over een natuurlijk persoon. Dit datatype komt voor onder de top-level
    elementen `<aanwezigeDeelnemer>` en `<persoonBuitenVergadering>`.

    Attributes:
        ID: Uniek identificatiekenmerk van de persoon.
        naam: Gegevens over de naam van de persoon, zoals diens voor- en
          achternaam.
        geslachtsaanduiding: Geslachtsaanduiding van de persoon.
        functie: De functie of het ambt van de persoon.
        nevenfunctie: Gegevens over een nevenfunctie van de persoon, zoals of het
          om een betaalde functie gaat.
        isLidVanFractie: Gegevens over iemands fractielidmaatschap.
        isLidVanDagelijksBestuur: Gegevens over iemands lidmaatschap van een
          dagelijks bestuur.
    """

    ID: str | list[str]
    naam: NaamGegevens
    geslachtsaanduiding: GeslachtsaanduidingEnum = None
    functie: BegripGegevens = None
    nevenfunctie: list[NevenfunctieGegevens] = None
    isLidVanFractie: FractielidmaatschapGegevens = None
    isLidVanDagelijksBestuur: DagelijksBestuurLidmaatschapGegevens = None


@dataclass
class StemmingGegevens(Serializable):
    """Gegevens over een stemming, zoals het agendapunt of de persoon waarover gestemd
    is. Iemands stemkeuze op een stemming hoort onder `aanwezigeDeelnemer`.

    Attributes:
        ID: Uniek identificatiekenmerk van de stemming.
        heeftBetrekkingOpAgendapunt: Verwijzing naar het agendapunt waarover
          gestemd werd.
        type: De wijze waarop gestemd is.
        resultaatMondelingeStemming: Het resultaat van een mondelinge stemming.
        resultaatStemmingOverPersonen: Beschrijving van het resultaat van een
          stemming over een of meerdere personen.
        stemmingOverPersonen: Gegevens die een stemming over personen beschrijven,
          zoals het aantal stemmen dat een kandidaat haalde.
        leidtTotBesluit: Verwijzing naar het besluit waartoe de stemming heeft
          geleid.
        heeftBetrekkingOpBesluitvormingsstuk: Gegevens over een
          besluitvormingsstuk waarover gestemd werd. Dit besluitvormingsstuk kan
          bijvoorbeeld een motie, voorstel, of (sub)amendement zijn.
    """

    ID: str | list[str]
    heeftBetrekkingOpAgendapunt: VerwijzingGegevens
    type: StemmingTypeEnum = None
    resultaatMondelingeStemming: ResultaatMondelingeStemmingEnum = None
    resultaatStemmingOverPersonen: str = None
    stemmingOverPersonen: list[StemmingOverPersonenGegevens] = None
    leidtTotBesluit: VerwijzingGegevens = None
    heeftBetrekkingOpBesluitvormingsstuk: list[InformatieobjectGegevens] = None


@dataclass
class TijdsaanduidingGegevens(Serializable):
    """Gegevens om het begin- en eindpunt van een gebeurtenis in een mediabron aan te
    geven, zoals de aanvang van een spreekfragment in een video-opname.

    Attributes:
        aanvang: Het beginpunt van de gebeurtenis in de mediabron, vanaf het begin
          van de mediabron gerekend. Dit is óf een tijdcode (hh:mm:ss), óf een
          positief getal dat het aantal seconden aangeeft waarna de gebeurtenis
          begint.
        einde: Het eindpunt van de gebeurtenis in de mediabron, vanaf het begin
          van de mediabron gerekend. Dit is óf een tijdcode (hh:mm:ss), óf een
          positief getal dat het aantal seconden aangeeft waarna de gebeurtenis
          eindigt.
        isRelatiefTot: Gegevens over de mediabron waar deze tijdsaanduiding
          betrekking op heeft, zoals het identificatiekenmerk van een video-
          opname. Dit element is alleen nodig wanneer er meer dan een mediabron
          aan een vergadering is gerelateerd. Als dit element ontbreekt, moet
          worden verondersteld dat de tijdsaanduiding relatief is tot de mediabron
          die is vastgelegd onder het top-level element `vergadering`.
    """

    aanvang: int | XmlTime
    einde: None | XmlTime = None
    isRelatiefTot: InformatieobjectGegevens = None


@dataclass
class VergaderingGegevens(Serializable):
    """Gegevens over een (deel)vergadering, zoals de startdatum en locatie.

    Attributes:
        naam: De naam van de vergadering, zoals 'Commissie Onderwijs en
          Samenleving'.
        datum: De datum waarop de vergadering daadwerkelijk gehouden werd.
        ID: Uniek identificatiekenmerk van de vergadering.
        geplandeDatum: Geplande aanvangsdatum van de vergadering.
        geplandeAanvang: Het geplande moment (datum en tijdstip) waarop de
          vergadering zou beginnen.
        geplandEinde: Het geplande moment (datum en tijdstip) waarop de
          vergadering beëindigd zou worden.
        aanvang: Daadwerkelijke datum en tijdstip waarop de vergadering begon.
        einde: Daadwerkelijke datum en tijdstip waarop de vergadering eindigde.
        publicatiedatum: Datum en tijdstip waarop de vergadering voor het laatst
          gepubliceerd of gewijzigd is.
        type: Het soort vergadering.
        toelichting: Toelichting of nadere omschrijving van de vergadering.
        georganiseerdDoorGremium: Gegevens over het gremium dat de vergadering
          georganiseerd heeft, zoals de naam van het gremium.
        locatie: Locatie (bijvoorbeeld gebouw of plaats) waar de vergadering
          gehouden is.
        weblocatie: Actuele link naar een online raadpleeglocatie waar de
          vergadering in zijn geheel wordt getoond, zoals de publicatieomgeving
          van een e-depot of raadsinformatiesysteem.
        status: De status van de vergadering.
        overheidsorgaan: Het overheidsorgaan dat de vergadering heeft gehouden.
        isVastgelegdMiddels: Gegevens over een informatieobject waarin de
          (deel)vergadering is opgenomen. Deze opname kan een audiotuul, videotuul
          of transcriptie zijn.
        isGenotuleerdIn: Gegevens over het informatieobject waarin de notulen van
          de vergadering zijn vastgelegd.
        heeftAlsBijlage: Gegevens over een informatieobject dat als bijlage bij de
          algehele (deel)vergadering diende.
        heeftAlsDeelvergadering: Gegevens over een vergadering die als
          afzonderlijk onderdeel functioneert binnen een grotere vergadering.
    """

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
    isVastgelegdMiddels: list[InformatieobjectGegevens] = None
    isGenotuleerdIn: InformatieobjectGegevens = None
    heeftAlsBijlage: list[InformatieobjectGegevens] = None
    heeftAlsDeelvergadering: list[VergaderingGegevens] = None


@dataclass
class AgendapuntGegevens(Serializable):
    """Gegevens over een agendapunt, zoals het volgnummer en bijbehorende stukken. Bij
    het ontbreken van volgnummers, moet de volgorde van agendapunt-elementen
    aangeven in welke volgorde ze behandeld zijn.

    Attributes:
        ID: Uniek identificatiekenmerk van het agendapunt.
        naam: Naam of onderwerp van het agendapunt.
        geplandVolgnummer: Het geplande agendapunt volgnummer. Begint met een of
          meer cijfers, maar mag gevolgd worden door andere karakters.
        volgnummer: Het agendapunt volgnummer. Begint met een of meer cijfers,
          maar mag gevolgd worden door andere karakters.
        volgnummerWeergave: De naar buiten gepresenteerde weergave van het
          volgnummer op de agenda, zoals `10a.`.
        omschrijving: Toelichting of nadere omschrijving van het agendapunt.
        geplandeStarttijd: Het geplande moment (datum en tijdstip) waarop het
          agendapunt in behandeling zou worden genomen.
        geplandeEindtijd: Het geplande moment (datum en tijdstip) waarop het
          agendapunt zou worden afgesloten.
        starttijd: Datum en tijdstip waarop het agendapunt daadwerkelijk in
          behandeling werd genomen.
        eindtijd: Datum en tijdstip waarop het agendapunt daadwerkelijk werd
          afgesloten.
        tijdsaanduidingMediabron: Gegevens over wanneer het agendapunt begint en
          eindigt in een bepaalde mediabron, zoals een video- of audio-opname van
          de vergadering.
        locatie: Locatie (bijvoorbeeld gebouw of plaats) waar het agendapunt werd
          behandeld.
        indicatieHamerstuk: Geeft aan of het agendapunt een hamerstuk was.
        indicatieBehandeld: Geeft aan of het agendapunt is behandeld tijdens de
          vergadering.
        indicatieBesloten: Geeft aan of het agendapunt besloten werd behandeld.
        overheidsorgaan: Het overheidsorgaan dat het agendapunt heeft behandeld.
        wordtBehandeldTijdens: Verwijzing naar de vergadering waarin het
          agendapunt behandeld werd.
        heeftBehandelendAmbtenaar: Verwijzing naar een natuurlijk persoon die de
          behandelend ambtenaar van het agendapunt was.
        heeftAlsBijlage: Gegevens over een informatieobject dat als bijlage bij
          dit agendapunt diende.
        heeftAlsSubagendapunt: Gegevens over een agendapunt dat als afzonderlijk
          onderdeel functioneert binnen een groter agendapunt.
    """

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
    tijdsaanduidingMediabron: list[TijdsaanduidingGegevens] = None
    locatie: str = None
    indicatieHamerstuk: bool = None
    indicatieBehandeld: bool = None
    indicatieBesloten: bool = None
    overheidsorgaan: BegripGegevens = None
    wordtBehandeldTijdens: VerwijzingGegevens = None
    heeftBehandelendAmbtenaar: list[VerwijzingGegevens] = None
    heeftAlsBijlage: list[InformatieobjectGegevens] = None
    heeftAlsSubagendapunt: list[AgendapuntGegevens] = None


@dataclass
class SpreekfragmentGegevens(Serializable):
    """Gegevens over een spreekfragment waarin een deelnemer sprak, zoals het moment
    waarop dit fragment begon en eindigde.

    Attributes:
        gedurendeAgendapunt: Verwijzing naar het agendapunt waar tijdens gesproken
          wordt.
        ID: Uniek identificatiekenmerk van het spreekfragment.
        naam: De naam van het spreekfragment, of een benaming voor de discussie
          die tijdens dit fragment plaatsvindt.
        aanvang: Datum en tijdstip waarop het spreekfragment begon.
        einde: Datum en tijdstip waarop het spreekfragment eindigde.
        taal: De taal van het spreekfragment.
        tekst: De uitgeschreven tekst van het spreekfragment.
        positieNotulen: De positie van het spreekfragment in de notulen,
          bijvoorbeeld `pagina 8`.
        tijdsaanduidingMediabron: Gegevens over wanneer het spreekfragment begint
          en eindigt in een bepaalde mediabron, zoals een video- of audio-opname
          van de vergadering.
    """

    gedurendeAgendapunt: list[VerwijzingGegevens]
    ID: str | list[str] = None
    naam: str = None
    aanvang: XmlDateTime = None
    einde: XmlDateTime = None
    taal: str = None
    tekst: str = None
    positieNotulen: str = None
    tijdsaanduidingMediabron: list[TijdsaanduidingGegevens] = None


@dataclass
class AanwezigeDeelnemerGegevens(Serializable):
    """Gegevens over een persoon die bij de vergadering aanwezig was, zoals diens
    stemgedrag, inspreekmomenten, en meer algemene persoonsgegevens.

    Attributes:
        isNatuurlijkPersoon: Gegevens over de persoon die als deelnemer optreedt,
          zoals diens naam en fractielidmaatschap.
        ID: Uniek identificatiekenmerk van de deelnemer.
        rolnaam: De rol waarin iemand bij de vergadering aanwezig was.
        organisatie: De naam van de organisatie die wordt vertegenwoordigd door de
          deelnemer.
        deelnemerspositie: Beschrijving van de plek waar de deelnemer in de zaal
          zat.
        aanvangAanwezigheid: Datum en tijdstip vanaf wanneer de deelnemer bij de
          vergadering aanwezig was.
        eindeAanwezigheid: Datum en tijdstip waarna de deelnemer de vergadering
          verliet.
        neemtDeelAanVergadering: Verwijzing naar de vergadering of
          deelvergaderingen waar de deelnemer aanwezig was.
        neemtDeelAanStemming: Gegevens over een stem die de deelnemer heeft
          uitbracht, zoals de stemkeuze en de stemming waarop deze keuze
          betrekking heeft.
        spreektTijdensSpreekfragment: Gegevens over een spreekfragment waarin de
          deelnemer sprak, zoals het moment waarop dit fragment begon en eindigde.
    """

    isNatuurlijkPersoon: NatuurlijkPersoonGegevens
    ID: str | list[str] = None
    rolnaam: BegripGegevens = None
    organisatie: str = None
    deelnemerspositie: str = None
    aanvangAanwezigheid: XmlDateTime = None
    eindeAanwezigheid: XmlDateTime = None
    neemtDeelAanVergadering: list[VerwijzingGegevens] = None
    neemtDeelAanStemming: list[StemGegevens] = None
    spreektTijdensSpreekfragment: list[SpreekfragmentGegevens] = None


# TODO: insert your monkeypatch here
@dataclass
class ORI_A(Serializable):
    """"""

    vergadering: VergaderingGegevens
    agendapunt: list[AgendapuntGegevens]
    stemming: list[StemmingGegevens] = None
    besluit: list[BesluitGegevens] = None
    fractie: list[FractieGegevens] = None
    dagelijksBestuur: list[DagelijksBestuurGegevens] = None
    persoonBuitenVergadering: list[NatuurlijkPersoonGegevens] = None
    aanwezigeDeelnemer: list[AanwezigeDeelnemerGegevens] = None


# TODO: generate docstrings for these as well (just a list of options is good)
# TODO: maybe make the case match values? (or give options for both; and/or add a UPPER_CASE variant)
class BesluitResultaatEnum(Enum):
    """"""

    unaniem_aangenomen = "Unaniem aangenomen"
    aangenomen = "Aangenomen"
    geamendeerd_aangenomen = "Geamendeerd aangenomen"
    onder_voorbehoud_aangenomen = "Onder voorbehoud aangenomen"
    verworpen = "Verworpen"
    aangehouden = "Aangehouden"


class GeslachtsaanduidingEnum(Enum):
    """"""

    man = "Man"
    vrouw = "Vrouw"
    anders = "Anders"
    onbekend = "Onbekend"


class KeuzeStemmingEnum(Enum):
    """"""

    tegen = "Tegen"
    afwezig = "Afwezig"
    onthouden = "Onthouden"


class ResultaatMondelingeStemmingEnum(Enum):
    """"""

    voor = "Voor"
    tegen = "Tegen"
    gelijk = "Gelijk"


class StemmingTypeEnum(Enum):
    """"""

    hoofdelijk = "Hoofdelijk"
    regulier = "Regulier"
    schriftelijk = "Schriftelijk"


class FractieStemresultaatEnum(Enum):
    """"""

    aangenomen = "Aangenomen"
    verworpen = "Verworpen"
    verdeeld = "Verdeeld"


class VergaderingStatusEnum(Enum):
    """"""

    gepland = "Gepland"
    gehouden = "Gehouden"
    geannuleerd = "Geannuleerd"