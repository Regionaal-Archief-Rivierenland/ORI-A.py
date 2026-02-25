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
    status: VergaderingStatusEnum = None
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
