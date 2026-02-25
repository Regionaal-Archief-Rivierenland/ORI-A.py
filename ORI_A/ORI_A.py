from __future__ import annotations
import dataclasses

from dataclasses import Field, dataclass
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlTime

import lxml.etree as ET

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

    def to_xml(self, root: str) -> ET.Element:
        """Serialize ORI-A object to XML.

        Args:
            root (str): name of the new root tag

        Returns:
            ET.Element: XML serialization of object with new root tag
        """

        root_elem = ET.Element(root)
        # get dataclass fields, but in the order required by the ORI-A XSD
        fields = self._ORI_A_ordered_fields()

        for field in fields:
            field_name = field.name
            field_value = getattr(self, field_name)

            # skip empty fields
            if field_value is None:
                continue

            # listify
            if not isinstance(field_value, (list, tuple, set)):
                field_value = (field_value,)

            # serialize sequence of primitives and *Gegevens objects
            for val in field_value:
                if isinstance(val, Serializable):
                    root_elem.append(val.to_xml(field_name))
                else:
                    # micro-optim: create subelem and .text content in one go
                    ET.SubElement(root_elem, field_name).text = str(val)
                    
        return root_elem


@dataclass
class GremiumGegevens(Serializable):
    """Gegevens over een gremium.

    Attributes:
        naam (str[1..1]): Naam van het gremium, zoals 'Commissie Samenleving'.
        identificatie (str[0..1]): Uniek identificatiekenmerk van het gremium.
    """

    naam: str
    identificatie: str = None


@dataclass
class NaamGegevens(Serializable):
    """Gegevens over de naam van een persoon, zoals diens voor- en achternaam.

    Attributes:
        achternaam (str[1..1]): De achternaam van de persoon, zoals `Mierlo`.
        tussenvoegsel (str[0..1]): Het tussenvoegsel in de naam van de persoon, zoals
          `van der`.
        voorletters (str[0..1]): De voorletters van de persoon, zoals `J.P.` of `K.`.
        voornamen (str[0..1]): De voornaam of voornamen van de persoon, zoals `Anna
          Maria Sophia` of `Jan`.
        volledigeNaam (str[0..1]): De volledige naam van de persoon, zoals `Piet van
          der Berg`.
    """

    achternaam: str
    tussenvoegsel: str = None
    voorletters: str = None
    voornamen: str = None
    volledigeNaam: str = None


@dataclass
class NevenfunctieGegevens(Serializable):
    """Gegevens over een nevenfunctie van een persoon, zoals of het om een betaalde functie
    gaat.

    Attributes:
        omschrijving (str[1..1]): Informatie over de inhoud van iemands nevenfunctie,
          zoals de officiële functietitel of een korte beschrijving.
        naamOrganisatie (str[0..1]): De naam van de organisatie waarbinnen de
          nevenfunctie wordt uitgevoerd.
        aantalUrenPerMaand (int[0..1]): Aantal uren per maand dat besteed wordt aan de
          nevenfunctie.
        indicatieBezoldigd (bool[0..1]): Geeft aan of de nevenfunctie wordt uitgevoerd
          tegen betaling.
        indicatieFunctieVanwegeLidmaatschap (bool[0..1]): Geeft aan of de nevenfunctie
          wordt vervuld vanwege iemands lidmaatschap aan het betreffende
          overheidsorgaan.
        datumMelding (XmlDate[0..1]): Datum waarop de nevenfunctie gemeld is bij de
          griffie.
        datumAanvang (XmlDate[0..1]): Datum waarop iemand met de nevenfunctie begon.
        datumEinde (XmlDate[0..1]): Datum waarop iemands nevenfunctie wordt/is
          beëindigd.
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
    """Gegevens die een stemming over personen beschrijven, zoals het aantal stemmen dat een
    kandidaat haalde.

    Attributes:
        naamKandidaat (str[1..1]): Naam van de kandidaat waarover gestemd werd.
        aantalUitgebrachteStemmen (int[0..1]): Aantal stemmen dat de kandidaat gehaald
          heeft.
    """

    naamKandidaat: str
    aantalUitgebrachteStemmen: int = None


@dataclass
class VerwijzingGegevens(Serializable):
    """Gegevens om vanuit een entiteit naar een ander te verwijzen.

    Attributes:
        verwijzingID (str[1..1]): Het ID van de entiteit waarnaar verwezen wordt.
        verwijzingNaam (str[0..1]): Een voor menselijke lezers bedoelde naam van de
          entiteit waarnaar verwezen wordt.
    """

    verwijzingID: str
    verwijzingNaam: str = None


@dataclass
class BegripGegevens(Serializable):
    """Gegevens over een begrip, zoals de locatie van de begrippenlijst waar het begrip
    verklaard wordt.

    Attributes:
        begripLabel (str[1..1]): Het label dat aan het begrip is toegekend in de
          begrippenlijst.
        verwijzingBegrippenlijst (VerwijzingGegevens[1..1]): Een verwijzing naar de
          begrippenlijst waarin het begrip beschreven wordt. Het ID van de
          begrippenlijst waarnaar verwezen wordt is meestal een URL, en de gewenste
          naam de titel van de begrippenlijst (bijvoorbeeld 'ORI-A vergaderstuktypes').
        begripCode (str[0..1]): De code die aan het begrip is toegekend in de
          begrippenlijst.
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
    """Gegevens over een besluit, zoals of het unaniem aangenomen of verworpen is. Een besluit
    volgt in de regel op een `stemming`.

    Attributes:
        ID (str[1..*]): Uniek identificatiekenmerk van het besluit.
        resultaat (BesluitResultaatEnum[1..1]): Het resultaat van het besluit.
        toelichting (str[0..1]): Een toelichting op het besluit.
        toezegging (str[0..1]): Een toezegging die bij het besluit gedaan is.
    """

    ID: str | list[str]
    resultaat: BesluitResultaatEnum
    toelichting: str = None
    toezegging: str = None


@dataclass
class DagelijksBestuurLidmaatschapGegevens(Serializable):
    """Gegevens over wanneer iemand lid is geworden van een bepaald dagelijks bestuur.

    Attributes:
        verwijzingDagelijksBestuur (VerwijzingGegevens[1..1]): Verwijzing naar het
          dagelijks bestuur waar het lidmaatschap betrekking op heeft.
        ID (str[0..*]): Uniek identificatiekenmerk van het dagelijks bestuur
          lidmaatschap.
        datumBeginDagelijksBestuurLidmaatschap (XmlDate[0..1]): Datum waarop iemands
          lidmaatschap van het dagelijks bestuur begon.
        datumEindeDagelijksBestuurLidmaatschap (XmlDate[0..1]): Datum waarop iemands
          lidmaatschap van het dagelijks bestuur eindigde.
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
        verwijzingFractie (VerwijzingGegevens[1..1]): Verwijzing naar de fractie waar
          het lidmaatschap betrekking op heeft.
        ID (str[0..*]): Uniek identificatiekenmerk van het fractielidmaatschap.
        datumBeginFractielidmaatschap (XmlDate[0..1]): Datum waarop iemands
          fractielidmaatschap begon.
        datumEindeFractielidmaatschap (XmlDate[0..1]): Datum waarop iemands
          fractielidmaatschap eindigde.
        indicatieVoorzitter (bool[0..1]): Geeft aan of iemand fractievoorzitter is.
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
        keuzeStemming (KeuzeStemmingEnum[1..1]): De keuze op de stemming.
        gegevenOpStemming (VerwijzingGegevens[1..1]): Verwijzing naar de stemming waar
          de stem betrekking op heeft.
        ID (str[0..*]): Uniek identificatiekenmerk van de stem.
    """

    keuzeStemming: KeuzeStemmingEnum
    gegevenOpStemming: VerwijzingGegevens
    ID: str | list[str] = None


@dataclass
class StemresultaatPerFractieGegevens(Serializable):
    """Gegevens over hoe een fractie als geheel tegenover een stemming stond, zoals of de
    aanwezigen leden unaniem voor, unaniem tegen, of juist verdeeld hebben gestemd.

    Attributes:
        fractieStemresultaat (FractieStemresultaatEnum[1..1]): Geeft aan hoe de fractie
          als geheel tegenover een stemming stond.
        verwijzingStemming (VerwijzingGegevens[1..1]): Verwijzing naar de stemming waar
          de fractie aan heeft deelgenomen.
        ID (str[0..*]): Uniek identificatiekenmerk van het stemresultaat per fractie.
    """

    fractieStemresultaat: FractieStemresultaatEnum
    verwijzingStemming: VerwijzingGegevens
    ID: str | list[str] = None


@dataclass
class DagelijksBestuurGegevens(Serializable):
    """Gegevens over een dagelijks bestuur, zoals de naam van het bestuur.

    Attributes:
        ID (str[1..*]): Uniek identificatiekenmerk van het dagelijks bestuur.
        naam (str[1..1]): Naam van het dagelijks bestuur.
        overheidsorgaan (BegripGegevens[1..1]): Het overheidsorgaan waarbinnen dit
          dagelijks bestuur opereert.
        type (BegripGegevens[0..1]): Het soort dagelijks bestuur.
    """

    ID: str | list[str]
    naam: str
    overheidsorgaan: BegripGegevens
    type: BegripGegevens = None


@dataclass
class FractieGegevens(Serializable):
    """Gegevens over een fractie, zoals de naam en het stemgedrag van de fractie.

    Attributes:
        ID (str[1..*]): Uniek identificatiekenmerk van de fractie.
        naam (str[1..1]): De naam van de fractie, zoals `D66` of `VVD`.
        overheidsorgaan (BegripGegevens[0..1]): Het overheidsorgaan waarbinnen de
          fractie opereert.
        neemtDeelAanStemming (StemresultaatPerFractieGegevens[0..*]): Gegevens over hoe
          de fractie als geheel tegenover een stemming stond, zoals of de aanwezigen
          leden unaniem voor, unaniem tegen, of juist verdeeld hebben gestemd.
    """

    ID: str | list[str]
    naam: str
    overheidsorgaan: BegripGegevens = None
    neemtDeelAanStemming: StemresultaatPerFractieGegevens | list[StemresultaatPerFractieGegevens] = None


@dataclass
class InformatieobjectGegevens(Serializable):
    """Gegevens die worden gebruikt om te **verwijzen** naar een elders gedefinieerd
    informatieobject.

    Attributes:
        verwijzingInformatieobject (VerwijzingGegevens[1..1]): Verwijzing naar een
          elders gedefinieerd informatieobject.
        informatieobjectType (BegripGegevens[0..1]): Het soort informatieobject
          waarnaar verwezen wordt.
    """

    verwijzingInformatieobject: VerwijzingGegevens
    informatieobjectType: BegripGegevens = None


@dataclass
class NatuurlijkPersoonGegevens(Serializable):
    """Gegevens over een natuurlijk persoon. Dit datatype komt voor onder de top-level
    elementen `<aanwezigeDeelnemer>` en `<persoonBuitenVergadering>`.

    Attributes:
        ID (str[1..*]): Uniek identificatiekenmerk van de persoon.
        naam (NaamGegevens[1..1]): Gegevens over de naam van de persoon, zoals diens
          voor- en achternaam.
        geslachtsaanduiding (GeslachtsaanduidingEnum[0..1]): Geslachtsaanduiding van de
          persoon.
        functie (BegripGegevens[0..1]): De functie of het ambt van de persoon.
        nevenfunctie (NevenfunctieGegevens[0..*]): Gegevens over een nevenfunctie van
          de persoon, zoals of het om een betaalde functie gaat.
        isLidVanFractie (FractielidmaatschapGegevens[0..1]): Gegevens over iemands
          fractielidmaatschap.
        isLidVanDagelijksBestuur (DagelijksBestuurLidmaatschapGegevens[0..1]): Gegevens
          over iemands lidmaatschap van een dagelijks bestuur.
    """

    ID: str | list[str]
    naam: NaamGegevens
    geslachtsaanduiding: GeslachtsaanduidingEnum = None
    functie: BegripGegevens = None
    nevenfunctie: NevenfunctieGegevens | list[NevenfunctieGegevens] = None
    isLidVanFractie: FractielidmaatschapGegevens = None
    isLidVanDagelijksBestuur: DagelijksBestuurLidmaatschapGegevens = None


@dataclass
class StemmingGegevens(Serializable):
    """Gegevens over een stemming, zoals het agendapunt of de persoon waarover gestemd is.
    Iemands stemkeuze op een stemming hoort onder `aanwezigeDeelnemer`.

    Attributes:
        ID (str[1..*]): Uniek identificatiekenmerk van de stemming.
        heeftBetrekkingOpAgendapunt (VerwijzingGegevens[1..1]): Verwijzing naar het
          agendapunt waarover gestemd werd.
        type (StemmingTypeEnum[0..1]): De wijze waarop gestemd is.
        resultaatMondelingeStemming (ResultaatMondelingeStemmingEnum[0..1]): Het
          resultaat van een mondelinge stemming.
        resultaatStemmingOverPersonen (str[0..1]): Beschrijving van het resultaat van
          een stemming over een of meerdere personen.
        stemmingOverPersonen (StemmingOverPersonenGegevens[0..*]): Gegevens die een
          stemming over personen beschrijven, zoals het aantal stemmen dat een
          kandidaat haalde.
        leidtTotBesluit (VerwijzingGegevens[0..1]): Verwijzing naar het besluit waartoe
          de stemming heeft geleid.
        heeftBetrekkingOpBesluitvormingsstuk (InformatieobjectGegevens[0..*]): Gegevens
          over een besluitvormingsstuk waarover gestemd werd. Dit besluitvormingsstuk
          kan bijvoorbeeld een motie, voorstel, of (sub)amendement zijn.
    """

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
    """Gegevens om het begin- en eindpunt van een gebeurtenis in een mediabron aan te geven,
    zoals de aanvang van een spreekfragment in een video-opname.

    Attributes:
        aanvang (int[1..1]): Het beginpunt van de gebeurtenis in de mediabron, vanaf
          het begin van de mediabron gerekend. Dit is óf een tijdcode (hh:mm:ss), óf
          een positief getal dat het aantal seconden aangeeft waarna de gebeurtenis
          begint.
        einde (int[0..1]): Het eindpunt van de gebeurtenis in de mediabron, vanaf het
          begin van de mediabron gerekend. Dit is óf een tijdcode (hh:mm:ss), óf een
          positief getal dat het aantal seconden aangeeft waarna de gebeurtenis
          eindigt.
        isRelatiefTot (InformatieobjectGegevens[0..1]): Gegevens over de mediabron waar
          deze tijdsaanduiding betrekking op heeft, zoals het identificatiekenmerk van
          een video-opname. Dit element is alleen nodig wanneer er meer dan een
          mediabron aan een vergadering is gerelateerd. Als dit element ontbreekt, moet
          worden verondersteld dat de tijdsaanduiding relatief is tot de mediabron die
          is vastgelegd onder het top-level element `vergadering`.
    """

    aanvang: int | XmlTime
    einde: int | XmlTime = None
    isRelatiefTot: InformatieobjectGegevens = None


@dataclass
class VergaderingGegevens(Serializable):
    """Gegevens over een (deel)vergadering, zoals de startdatum en locatie.

    Attributes:
        naam (str[1..1]): De naam van de vergadering, zoals 'Commissie Onderwijs en
          Samenleving'.
        datum (XmlDate[1..1]): De datum waarop de vergadering daadwerkelijk gehouden
          werd.
        ID (str[0..*]): Uniek identificatiekenmerk van de vergadering.
        geplandeDatum (XmlDate[0..1]): Geplande aanvangsdatum van de vergadering.
        geplandeAanvang (XmlDateTime[0..1]): Het geplande moment (datum en tijdstip)
          waarop de vergadering zou beginnen.
        geplandEinde (XmlDateTime[0..1]): Het geplande moment (datum en tijdstip)
          waarop de vergadering beëindigd zou worden.
        aanvang (XmlDateTime[0..1]): Daadwerkelijke datum en tijdstip waarop de
          vergadering begon.
        einde (XmlDateTime[0..1]): Daadwerkelijke datum en tijdstip waarop de
          vergadering eindigde.
        publicatiedatum (XmlDateTime[0..1]): Datum en tijdstip waarop de vergadering
          voor het laatst gepubliceerd of gewijzigd is.
        type (BegripGegevens[0..1]): Het soort vergadering.
        toelichting (str[0..1]): Toelichting of nadere omschrijving van de vergadering.
        georganiseerdDoorGremium (GremiumGegevens[0..1]): Gegevens over het gremium dat
          de vergadering georganiseerd heeft, zoals de naam van het gremium.
        locatie (str[0..1]): Locatie (bijvoorbeeld gebouw of plaats) waar de
          vergadering gehouden is.
        weblocatie (str[0..*]): Actuele link naar een online raadpleeglocatie waar de
          vergadering in zijn geheel wordt getoond, zoals de publicatieomgeving van een
          e-depot of raadsinformatiesysteem.
        status (VergaderingStatusEnum[0..1]): De status van de vergadering.
        overheidsorgaan (BegripGegevens[0..1]): Het overheidsorgaan dat de vergadering
          heeft gehouden.
        isVastgelegdMiddels (InformatieobjectGegevens[0..*]): Gegevens over een
          informatieobject waarin de (deel)vergadering is opgenomen. Deze opname kan
          een audiotuul, videotuul of transcriptie zijn.
        isGenotuleerdIn (InformatieobjectGegevens[0..1]): Gegevens over het
          informatieobject waarin de notulen van de vergadering zijn vastgelegd.
        heeftAlsBijlage (InformatieobjectGegevens[0..*]): Gegevens over een
          informatieobject dat als bijlage bij de algehele (deel)vergadering diende.
        heeftAlsDeelvergadering (VergaderingGegevens[0..*]): Gegevens over een
          vergadering die als afzonderlijk onderdeel functioneert binnen een grotere
          vergadering.
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
    status: VergaderingStatusEnum = None
    overheidsorgaan: BegripGegevens = None
    isVastgelegdMiddels: InformatieobjectGegevens | list[InformatieobjectGegevens] = None
    isGenotuleerdIn: InformatieobjectGegevens = None
    heeftAlsBijlage: InformatieobjectGegevens | list[InformatieobjectGegevens] = None
    heeftAlsDeelvergadering: VergaderingGegevens | list[VergaderingGegevens] = None


@dataclass
class AgendapuntGegevens(Serializable):
    """Gegevens over een agendapunt, zoals het volgnummer en bijbehorende stukken. Bij het
    ontbreken van volgnummers, moet de volgorde van agendapunt-elementen aangeven in
    welke volgorde ze behandeld zijn.

    Attributes:
        ID (str[1..*]): Uniek identificatiekenmerk van het agendapunt.
        naam (str[1..1]): Naam of onderwerp van het agendapunt.
        geplandVolgnummer (str[0..1]): Het geplande agendapunt volgnummer. Begint met
          een of meer cijfers, maar mag gevolgd worden door andere karakters.
        volgnummer (str[0..1]): Het agendapunt volgnummer. Begint met een of meer
          cijfers, maar mag gevolgd worden door andere karakters.
        volgnummerWeergave (str[0..1]): De naar buiten gepresenteerde weergave van het
          volgnummer op de agenda, zoals `10a.`.
        omschrijving (str[0..1]): Toelichting of nadere omschrijving van het
          agendapunt.
        geplandeStarttijd (XmlDateTime[0..1]): Het geplande moment (datum en tijdstip)
          waarop het agendapunt in behandeling zou worden genomen.
        geplandeEindtijd (XmlDateTime[0..1]): Het geplande moment (datum en tijdstip)
          waarop het agendapunt zou worden afgesloten.
        starttijd (XmlDateTime[0..1]): Datum en tijdstip waarop het agendapunt
          daadwerkelijk in behandeling werd genomen.
        eindtijd (XmlDateTime[0..1]): Datum en tijdstip waarop het agendapunt
          daadwerkelijk werd afgesloten.
        tijdsaanduidingMediabron (TijdsaanduidingGegevens[0..*]): Gegevens over wanneer
          het agendapunt begint en eindigt in een bepaalde mediabron, zoals een video-
          of audio-opname van de vergadering.
        locatie (str[0..1]): Locatie (bijvoorbeeld gebouw of plaats) waar het
          agendapunt werd behandeld.
        indicatieHamerstuk (bool[0..1]): Geeft aan of het agendapunt een hamerstuk was.
        indicatieBehandeld (bool[0..1]): Geeft aan of het agendapunt is behandeld
          tijdens de vergadering.
        indicatieBesloten (bool[0..1]): Geeft aan of het agendapunt besloten werd
          behandeld.
        overheidsorgaan (BegripGegevens[0..1]): Het overheidsorgaan dat het agendapunt
          heeft behandeld.
        wordtBehandeldTijdens (VerwijzingGegevens[0..1]): Verwijzing naar de
          vergadering waarin het agendapunt behandeld werd.
        heeftBehandelendAmbtenaar (VerwijzingGegevens[0..*]): Verwijzing naar een
          natuurlijk persoon die de behandelend ambtenaar van het agendapunt was.
        heeftAlsBijlage (InformatieobjectGegevens[0..*]): Gegevens over een
          informatieobject dat als bijlage bij dit agendapunt diende.
        heeftAlsSubagendapunt (AgendapuntGegevens[0..*]): Gegevens over een agendapunt
          dat als afzonderlijk onderdeel functioneert binnen een groter agendapunt.
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
    """Gegevens over een spreekfragment waarin een deelnemer sprak, zoals het moment waarop
    dit fragment begon en eindigde.

    Attributes:
        gedurendeAgendapunt (VerwijzingGegevens[1..*]): Verwijzing naar het agendapunt
          waar tijdens gesproken wordt.
        ID (str[0..*]): Uniek identificatiekenmerk van het spreekfragment.
        naam (str[0..1]): De naam van het spreekfragment, of een benaming voor de
          discussie die tijdens dit fragment plaatsvindt.
        aanvang (XmlDateTime[0..1]): Datum en tijdstip waarop het spreekfragment begon.
        einde (XmlDateTime[0..1]): Datum en tijdstip waarop het spreekfragment
          eindigde.
        taal (str[0..1]): De taal van het spreekfragment.
        tekst (str[0..1]): De uitgeschreven tekst van het spreekfragment.
        positieNotulen (str[0..1]): De positie van het spreekfragment in de notulen,
          bijvoorbeeld `pagina 8`.
        tijdsaanduidingMediabron (TijdsaanduidingGegevens[0..*]): Gegevens over wanneer
          het spreekfragment begint en eindigt in een bepaalde mediabron, zoals een
          video- of audio-opname van de vergadering.
    """

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
    """Gegevens over een persoon die bij de vergadering aanwezig was, zoals diens stemgedrag,
    inspreekmomenten, en meer algemene persoonsgegevens.

    Attributes:
        isNatuurlijkPersoon (NatuurlijkPersoonGegevens[1..1]): Gegevens over de persoon
          die als deelnemer optreedt, zoals diens naam en fractielidmaatschap.
        ID (str[0..*]): Uniek identificatiekenmerk van de deelnemer.
        rolnaam (BegripGegevens[0..1]): De rol waarin iemand bij de vergadering
          aanwezig was.
        organisatie (str[0..1]): De naam van de organisatie die wordt vertegenwoordigd
          door de deelnemer.
        deelnemerspositie (str[0..1]): Beschrijving van de plek waar de deelnemer in de
          zaal zat.
        aanvangAanwezigheid (XmlDateTime[0..1]): Datum en tijdstip vanaf wanneer de
          deelnemer bij de vergadering aanwezig was.
        eindeAanwezigheid (XmlDateTime[0..1]): Datum en tijdstip waarna de deelnemer de
          vergadering verliet.
        neemtDeelAanVergadering (VerwijzingGegevens[0..*]): Verwijzing naar de
          vergadering of deelvergaderingen waar de deelnemer aanwezig was.
        neemtDeelAanStemming (StemGegevens[0..*]): Gegevens over een stem die de
          deelnemer heeft uitbracht, zoals de stemkeuze en de stemming waarop deze
          keuze betrekking heeft.
        spreektTijdensSpreekfragment (SpreekfragmentGegevens[0..*]): Gegevens over een
          spreekfragment waarin de deelnemer sprak, zoals het moment waarop dit
          fragment begon en eindigde.
    """

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
    """"""

    vergadering: VergaderingGegevens
    agendapunt: AgendapuntGegevens | list[AgendapuntGegevens]
    stemming: StemmingGegevens | list[StemmingGegevens] = None
    besluit: BesluitGegevens | list[BesluitGegevens] = None
    fractie: FractieGegevens | list[FractieGegevens] = None
    dagelijksBestuur: DagelijksBestuurGegevens | list[DagelijksBestuurGegevens] = None
    persoonBuitenVergadering: NatuurlijkPersoonGegevens | list[NatuurlijkPersoonGegevens] = None
    aanwezigeDeelnemer: AanwezigeDeelnemerGegevens | list[AanwezigeDeelnemerGegevens] = None

    def to_xml(self, root: str) -> ET.Element:
        """Transform ORI-A object into an XML tree with the following structure:

        ```xml
        <ORI-A xmlns=…>
            …
        </ORI-A>
        ```

        Note:
           There is rarely a real reason to use this directly. If you want to
           write ORI-A XML to a file, look into the `.save()` method.

        Returns:
            ET.ElementTree: XML seralization of the object
        """

        xsi_ns = "http://www.w3.org/2001/XMLSchema-instance"
        root_without_attribs = super().to_xml(root)

        # we have to jump through some weird lxml hoops to get xmlns="https://ori-a.nl" to be first attrib.
        # while cosmetic, this is obviously super important
        root_elem = ET.Element(root, nsmap={None: "https://ori-a.nl", "xsi": xsi_ns})
        root_elem.set(
            # avoid f-strings here since double '{' upsets jinja
            "{" + xsi_ns + "}schemaLocation",
            "https://ori-a.nl https://github.com/Regionaal-Archief-Rivierenland/ORI-A-XSD/releases/download/v1.0.0/ORI-A.xsd",
        )
        # copy over children
        root_elem.extend(root_without_attribs)

        return root_elem

    def save(
        self,
        file_or_filename: str | TextIO,
        minify: bool = False,
        lxml_kwargs: dict = {},
    ) -> None:
        """Save ORI-A object to a XML file.

        The XML is pretty printed by default; use `minify=True` to reverse this.

        Args:
            file_or_filename (str | TextIO): Path or file-like object to write
             object's XML representation to
            minify (Optional[bool]): the reverse of pretty printing; makes the XML
             as small as possible by removing the XML declaration and any optional
             whitespace
            lxml_kwargs (Optional[dict]): optional dict of keyword arguments that
             can be used to override the args passed to lxml's `write()`.

        Note:
            For a complete list of arguments of lxml's write method, see
            https://lxml.de/apidoc/lxml.etree.html#lxml.etree._ElementTree.write

        Raises:
            ValidationError: ~~Object voilates the ORI-A schema~~ NOT IMPLEMENTED YET 
        """
        # lxml wants files in binary mode, so pass along a file's raw byte stream
        if hasattr(file_or_filename, "write"):
            file_or_filename = file_or_filename.buffer.raw

        # self.validate()
        xml = self.to_xml("ORI-A")
        # lxml's .write wants an ElementTree object
        tree = ET.ElementTree(xml)

        if not minify:
            ET.indent(xml, space="    ")

        lxml_defaults = {
            "xml_declaration": not minify,
            "pretty_print": not minify,
            "encoding": "UTF-8",
        }

        # `|` is a union operator; it merges two dicts, with right-hand side taking precedence
        tree.write(file_or_filename, **(lxml_defaults | lxml_kwargs))



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