import dataclasses
import json

from dataclasses import Field, dataclass
from enum import StrEnum

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlTime

import lxml.etree as ET


class Serializable:
    @classmethod
    def _ORI_A_ordered_fields(cls) -> tuple[Field]:
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
                elif isinstance(val, bool):
                    # micro-optim: create subelem and .text content in one go
                    ET.SubElement(root_elem, field_name).text = str(val).lower()
                else:
                    ET.SubElement(root_elem, field_name).text = str(val)
                    
        return root_elem

    # Think this maybe should be something done in (post)init? thay way you can make it a property
    def _ori_aliases(self) -> dict[str, str]:
        """Override this function when property names in ORI and ORI-A differ"""
        return {f.name: f.name for f in dataclasses.fields(self)}

    # note: the performance of all of this is not amazing. To fix this, we must precompute stuff
    def to_ori_json(self) -> str:
        strip_none = lambda d: {k: v for k, v in d if v is not None}
        # FIXME: asdict is not "recursive". Other Serializables/dataclasses are treated as dicts.
        # I think this causes self._ori_aliases() in subclasses to be ignored.
        d = dataclasses.asdict(self, dict_factory=strip_none)
        aliased = {self._ori_aliases()[k]: v for k, v in d.items()}
        return json.dumps(aliased)

    @classmethod
    def _from_elem(cls, elem: ET.Element):
        """Private helper method stub.

        Used within open() to construct a gegevensgroep from an ET.Element.
        This stub is dynamically implemented at runtime.
        """
        pass

# TODO: generate docstrings for these as well (just a list of options is good)
# TODO: maybe make the case match values? (or give options for both; and/or add a UPPER_CASE variant)
# TODO: maybe move these to their own submodule? ORI_A.enumerations.BesluitResultaat.verworpen may read better

@dataclass
class GremiumGegevens(Serializable):
    """{{docs.gremiumGegevens}}"""

    naam: str
    identificatie: str = None

    # instead of complex system with aliases and transformers, maybe just override a single method?
    def _ori_aliases(self):
        return {"naam": "gremiumnaam", "identificatie": "gremiumidentificatie"}


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
    def _ORI_A_ordered_fields(cls) -> tuple[Field]:
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
    def _ORI_A_ordered_fields(cls) -> tuple[Field]:
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

    def _ORI_A_ordered_fields(self) -> tuple(Field):
        fields = super()._ORI_A_ordered_fields()
        return fields[1:-1] + (fields[0],)

@dataclass
class StemGegevens(Serializable):
    """{{docs.stemGegevens}}"""

    keuzeStemming: KeuzeStemmingEnum
    gegevenOpStemming: VerwijzingGegevens
    ID: str | list[str] = None

    def _ORI_A_ordered_fields(self) -> tuple[Field]:
        fields = super()._ORI_A_ordered_fields()
        return (fields[2], fields[0], fields[1])


@dataclass
class StemresultaatPerFractieGegevens(Serializable):
    """{{docs.stemresultaatPerFractieGegevens}}"""

    fractieStemresultaat: FractieStemresultaatEnum
    verwijzingStemming: VerwijzingGegevens
    ID: str | list[str] = None

    def _ORI_A_ordered_fields(self) -> tuple[Field]:
        fields = super()._ORI_A_ordered_fields()
        return (fields[-1], fields[0], fields[1])

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
    neemtDeelAanStemming: (
        StemresultaatPerFractieGegevens | list[StemresultaatPerFractieGegevens]
    ) = None


@dataclass
class InformatieobjectGegevens(Serializable):
    """{{docs.informatieobjectGegevens}}"""

    verwijzingInformatieobject: VerwijzingGegevens
    informatieobjectType: BegripGegevens = None

    def _ORI_A_ordered_fields(self) -> tuple[Field]:
        return super()._ORI_A_ordered_fields()[::-1]


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
    stemmingOverPersonen: (
        StemmingOverPersonenGegevens | list[StemmingOverPersonenGegevens]
    ) = None
    leidtTotBesluit: VerwijzingGegevens = None
    heeftBetrekkingOpBesluitvormingsstuk: (
        InformatieobjectGegevens | list[InformatieobjectGegevens]
    ) = None

    def _ORI_A_ordered_fields(self) -> tuple[Field]:
        fields = super()._ORI_A_ordered_fields()
        return (fields[0], fields[2]) + fields[3:7] + (fields[1], fields[-1])


# TODO: move to a helpers file
def _integer_to_timestamp(secs: int) -> str:
    hours, remainder = divmod(secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

@dataclass
class TijdsaanduidingGegevens(Serializable):
    """{{docs.tijdsaanduidingGegevens}}"""

    aanvang: int | XmlTime
    einde: int | XmlTime = None
    isRelatiefTot: InformatieobjectGegevens = None

    def integers_to_timestamps(self) -> None:
        """Convert integer values in `aanvang` and `einde` to hh:mm:ss timestamps."""

        if not isinstance(self.aanvang, int):
            raise TypeError("TijdsaanduidingGegevens.aanvang is not an integer")

        if self.einde is not None and not isinstance(self.einde, int):
            raise TypeError("TijdsaanduidingGegevens.einde is not an integer")

        self.aanvang = _integer_to_timestamp(self.aanvang)

        if self.einde is not None:
            self.einde = _integer_to_timestamp(self.einde)



    def timestamps_to_integers(self) -> None:
        """Convert hh:mm:ss timestamps in `aanvang` and `einde` to integers."""
        pass

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
    isVastgelegdMiddels: InformatieobjectGegevens | list[InformatieobjectGegevens] = (
        None
    )
    isGenotuleerdIn: InformatieobjectGegevens = None
    heeftAlsBijlage: InformatieobjectGegevens | list[InformatieobjectGegevens] = None
    heeftAlsDeelvergadering: VergaderingGegevens | list[VergaderingGegevens] = None

    def _ORI_A_ordered_fields(self) -> tuple[Field]:
        f = super()._ORI_A_ordered_fields()
        return (f[2], f[0], f[3], f[1], f[4]) + f[5:]


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
    tijdsaanduidingMediabron: (
        TijdsaanduidingGegevens | list[TijdsaanduidingGegevens]
    ) = None
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
    tijdsaanduidingMediabron: (
        TijdsaanduidingGegevens | list[TijdsaanduidingGegevens]
    ) = None

    def _ORI_A_ordered_fields(self) -> tuple[Field]:
        fields = super()._ORI_A_ordered_fields()
        return (fields[1],) + fields[2:] + (fields[0],)


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
    spreektTijdensSpreekfragment: (
        SpreekfragmentGegevens | list[SpreekfragmentGegevens]
    ) = None

    def _ORI_A_ordered_fields(self) -> tuple[Field]:
        fields = super()._ORI_A_ordered_fields()
        return (fields[1],) + fields[2:8] + (fields[0],) + fields[8:]

@dataclass
class ORI_A(Serializable):
    """{{docs.ORI_A}}"""

    # todo: pluralize?
    vergadering: VergaderingGegevens
    agendapunt: AgendapuntGegevens | list[AgendapuntGegevens]
    stemming: StemmingGegevens | list[StemmingGegevens] = None
    besluit: BesluitGegevens | list[BesluitGegevens] = None
    fractie: FractieGegevens | list[FractieGegevens] = None
    dagelijksBestuur: DagelijksBestuurGegevens | list[DagelijksBestuurGegevens] = None
    persoonBuitenVergadering: (
        NatuurlijkPersoonGegevens | list[NatuurlijkPersoonGegevens]
    ) = None
    aanwezigeDeelnemer: (
        AanwezigeDeelnemerGegevens | list[AanwezigeDeelnemerGegevens]
    ) = None

    def to_xml(self, root: str) -> ET.Element:
        """Transform ORI-A object into an XML tree with the following structure:

        ```xml
        <ORI-A xmlns=…>
            …
        </ORI-A>
        ```

        Note:
           There is rarely a real reason to use this directly. If you want to
           write ORI-A XML to a file, see the `.save()` method.

        Returns:
            ET.Element: XML seralization of the object
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

    def to_html(self, outfile, jinja_template="template.html"):
        # is this import worth it? probably is okay if we make this optional deps
        import mdto
        from jinja2 import Template

        with open(jinja_template) as f:
            template = Template(f.read())

        # todo: ensure nothing modifies properties of `self`
        # fixme: idk if any of this media extraction logic works
        media_id = self.vergadering.isVastgelegdMiddels.verwijzingInformatieobject.verwijzingID
        media_path = list(Path(".").rglob(f"**/*{media_id}*xml"))[0]
        media = mdto.Informatieobject.open(media_path)
        src = media_path.parent / media.heeftRepresentatie.verwijzingNaam

        agendapunt_spreekfragmenten = defaultdict(list)
        for deelnemer in self.aanwezigeDeelnemer:
            # listify
            if not isinstance(deelnemer.spreektTijdensSpreekfragment, list):
                deelnemer.spreektTijdensSpreekfragment = [deelnemer.spreektTijdensSpreekfragment]

            for fragment in deelnemer.spreektTijdensSpreekfragment:
                if not fragment.tijdsaanduidingMediabron:
                    continue

                agendapunt_id = fragment.gedurendeAgendapunt.verwijzingID
                h, m, s = map(int, fragment.tijdsaanduidingMediabron.aanvang.split(":"))
                fragment_info = {
                    "aanvang_integer": h * 3600 + m * 60 + round(s),
                    "aanvang": fragment.tijdsaanduidingMediabron.aanvang,
                    "einde": fragment.tijdsaanduidingMediabron.einde,
                    "deelnemer": deelnemer
                }

                if deelnemer.isNatuurlijkPersoon.isLidVanFractie:
                    fractie_ref = deelnemer.isNatuurlijkPersoon.isLidVanFractie.verwijzingFractie.verwijzingID
                    fractie = next(f for f in self.fractie if f.ID == fractie_ref)
                    fragment_info["fractie"] = fractie

                agendapunt_spreekfragmenten[agendapunt_id].append(fragment_info)
            
        # temporal sort
        for agendapunt_id in agendapunt_spreekfragmenten:
            agendapunt_spreekfragmenten[agendapunt_id].sort(key=lambda x: x["aanvang_integer"])

        # todo: ensure that everything listable is a list
        ori_a_dict = self.__dict__
        ori_a_dict["src"] = src
        ori_a_dict["ori_a_xml"] = self._srcfile
        ori_a_dict["agendapunt_spreekfragmenten"] = agendapunt_spreekfragmenten
        html = template.render(ori_a_dict)

        with open(outfile, "w") as f:
            f.write(html)

        

# TODO: generate docstrings for these as well (just a list of options is good)
# TODO: maybe make the case match values? (or give options for both; and/or add a UPPER_CASE variant)
class BesluitResultaatEnum(StrEnum):
    """{{docs.besluitResultaatEnum}}"""

    unaniem_aangenomen = "Unaniem aangenomen"
    aangenomen = "Aangenomen"
    geamendeerd_aangenomen = "Geamendeerd aangenomen"
    onder_voorbehoud_aangenomen = "Onder voorbehoud aangenomen"
    verworpen = "Verworpen"
    aangehouden = "Aangehouden"


class GeslachtsaanduidingEnum(StrEnum):
    """{{docs.geslachtsaanduidingEnum}}"""

    man = "Man"
    vrouw = "Vrouw"
    anders = "Anders"
    onbekend = "Onbekend"


class KeuzeStemmingEnum(StrEnum):
    """{{docs.keuzeStemmingEnum}}"""

    tegen = "Tegen"
    afwezig = "Afwezig"
    onthouden = "Onthouden"


class ResultaatMondelingeStemmingEnum(StrEnum):
    """{{docs.resultaatMondelingeStemmingEnum}}"""

    voor = "Voor"
    tegen = "Tegen"
    gelijk = "Gelijk"


class StemmingTypeEnum(StrEnum):
    """{{docs.stemmingTypeEnum}}"""

    hoofdelijk = "Hoofdelijk"
    regulier = "Regulier"
    schriftelijk = "Schriftelijk"


class FractieStemresultaatEnum(StrEnum):
    """{{docs.fractieStemresultaatEnum}}"""

    aangenomen = "Aangenomen"
    verworpen = "Verworpen"
    verdeeld = "Verdeeld"


class VergaderingStatusEnum(StrEnum):
    """{{docs.vergaderingStatusEnum}}"""

    gepland = "Gepland"
    gehouden = "Gehouden"
    geannuleerd = "Geannuleerd"


def _construct_deserialization_classmethods():
    """
    Construct the private `_from_elem()` classmethod on all subclasses
    of `Serializable`.

    This constructor executes on module import, and creates helpers
    for the public `open()` classmethods of Informatieobject and
    Bestand.
    """

    def resolve_type(field_type: type):
        """Resolve a type from typing annotations. If Union[...] is
        detected, return the type of the first item."""

        origin = get_origin(field_type)
        if origin is Union:
            args = get_args(field_type)
            return args[0]  # assume first type is what we care about
        # VergaderingGegevens has a reference to itself
        elif isinstance(field_type, ForwardRef):
            return VergaderingGegevens
        else:
            return field_type

    def parse_text(elem: ET.Element) -> str:
        return elem.text

    def parse_int(elem: ET.Element) -> int:
        # fixme: ugly hack to support both ints and timestamps
        try:
            return int(elem.text)
        except:
            return elem.text

    def parse_bool(elem: ET.Element) -> bool:
        return bool(elem.text)

    # fixme: parsing specific dates _formats_ kinda violates the whole
    # "accept everything" premise
    def parse_date(elem: ET.Element) -> datetime:
        return datetime.strptime(elem.text, "%Y-%m-%d")

    def parse_datetime(elem: ET.Element) -> datetime:
        return datetime.strptime(elem.text, "%Y-%m-%dT%H:%M:%S")

    def from_elem_factory(ori_a_xml_parsers: dict) -> classmethod:
        """Create initialized from_elem functions."""

        def from_elem(cls, elem: ET.Element):
            """Convert XML elements (`elem`) to ORI-A classes (`cls`)"""

            # it may seem like pre computing this is faster, but it is not
            constructor_args = {field: [] for field in ori_a_xml_parsers}
            for child in elem:
                ori_a_field = child.tag.removeprefix(
                    "{https://ori-a.nl}"
                )
                parser = ori_a_xml_parsers[ori_a_field]
                constructor_args[ori_a_field].append(parser(child))

            # cleanup class constructor arguments
            for argname, value in constructor_args.items():
                # Replace empty argument lists by None
                if len(value) == 0:
                    constructor_args[argname] = None
                # Replace one-itemed argument lists by their respective item
                elif len(value) == 1:
                    constructor_args[argname] = value[0]

            return cls(**constructor_args)

        return classmethod(from_elem)

    # This loop depends on the order of the gegevensgroep defintions in this file
    for cls in Serializable.__subclasses__():
        parsers = {}
        for field in dataclasses.fields(cls):
            field_name = field.name
            field_type = resolve_type(field.type)
            if field_type is str:
                parsers[field_name] = parse_text
            elif issubclass(field_type, Serializable):
                parsers[field_name] = field_type._from_elem
            elif field_type is int:
                parsers[field_name] = parse_int
            elif field_type is XmlDate:
                parsers[field_name] = parse_date
            elif field_type is XmlDateTime:
                parsers[field_name] = parse_datetime
            else:
                parsers[field_name] = parse_text

        cls._from_elem = from_elem_factory(parsers)


# construct all _from_elem() classmethods immediately on import
_construct_deserialization_classmethods()
