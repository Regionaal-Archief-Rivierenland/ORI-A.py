from ORI_A import BegripGegevens as _BegripGegevens
from ORI_A import VerwijzingGegevens as _VerwijzingGegevens

class _Begrippenlijst(type):
    # For some reason, we need a metaclass to do this
    """Implements iteration through all posible values in a enumeration, as well
    as containment checking (the `in` operator)."""
    def __iter__(begrippenlijst_cls):
        # we need if isinstance(...) because vars() returns a bunch of stuff
        return (v for v in vars(begrippenlijst_cls).values() if isinstance(v, _BegripGegevens))

    # TODO: maybe something like `"video" in Mediabrontypes` should also work?
    def __contains__(begrippenlijst_cls, begrip: _BegripGegevens):
        label_normalized = begrippenlijst_cls._alt_labels.get(
            begrip.begripLabel, begrip.begripLabel
        )

        # as long as there is no canonical code, or at least one implemented by
        # this module, checking the value of begripCode will only create problems
        # TODO: add code check logic when codes are canonicalized
        soft_equiv = lambda b1, b2: (
            label_normalized == b2.begripLabel
            and b1.verwijzingBegrippenlijst.verwijzingID == b2.verwijzingBegrippenlijst.verwijzingID
        )
        return any(soft_equiv(begrip, b) for b in begrippenlijst_cls)

    # TODO: during validation, maybe add check that returns close matches on error? 


class BetrokkeneVergaderstukRelaties(metaclass=_Begrippenlijst):
    """
    Relaties tussen een persoon en een vergaderstuk.

    Attributes:
        indiener: Indiener van een vergaderstuk.
        ondertekenaar: Ondertekenaar van een vergaderstuk.
        portefeuillehouder: De portefeuillehouder van een voorstel.
    """
    indiener = _BegripGegevens(
        "Indiener",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#betrokkene-vergaderstuk-relaties", "ORI-A Betrokkene-vergaderstuk relaties")
    )
    """Indiener van een vergaderstuk."""
    ondertekenaar = _BegripGegevens(
        "Ondertekenaar",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#betrokkene-vergaderstuk-relaties", "ORI-A Betrokkene-vergaderstuk relaties")
    )
    """Ondertekenaar van een vergaderstuk."""
    portefeuillehouder = _BegripGegevens(
        "Portefeuillehouder",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#betrokkene-vergaderstuk-relaties", "ORI-A Betrokkene-vergaderstuk relaties")
    )
    """De portefeuillehouder van een voorstel."""
    
    _alt_labels = {}


class DagelijksBestuurTypes(metaclass=_Begrippenlijst):
    """
    Soorten dagelijks bestuur.

    Attributes:
        college_van_burgemeester_en_wethouders: Dagelijks bestuur van een gemeente.
        college_van_gedeputeerde_staten: Dagelijks bestuur van een provincie.
        college_van_dijkgraaf_en_heemraden: Dagelijks bestuur van een waterschap. Ook van
         toepassing op hoogheemraden.
        dagelijks_bestuur: Dagelijks bestuur van een overheidsorgaan.
    """
    college_van_burgemeester_en_wethouders = _BegripGegevens(
        "College van burgemeester en wethouders",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#dagelijks-bestuur-types", "ORI-A Dagelijks bestuur types")
    )
    """Dagelijks bestuur van een gemeente."""
    college_van_gedeputeerde_staten = _BegripGegevens(
        "College van Gedeputeerde Staten",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#dagelijks-bestuur-types", "ORI-A Dagelijks bestuur types")
    )
    """Dagelijks bestuur van een provincie."""
    college_van_dijkgraaf_en_heemraden = _BegripGegevens(
        "College van dijkgraaf en heemraden",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#dagelijks-bestuur-types", "ORI-A Dagelijks bestuur types")
    )
    """Dagelijks bestuur van een waterschap. Ook van toepassing op hoogheemraden."""
    dagelijks_bestuur = _BegripGegevens(
        "Dagelijks bestuur",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#dagelijks-bestuur-types", "ORI-A Dagelijks bestuur types")
    )
    """Dagelijks bestuur van een overheidsorgaan."""
    
    _alt_labels = {'College van B&W': 'College van burgemeester en wethouders'}


class Deelnemerrollen(metaclass=_Begrippenlijst):
    """
    Rollen waarin een deelnemer in een vergadering aanwezig kan zijn.

    Attributes:
        voorzitter: De voorzitter van de vergadering.
        vice_voorzitter: De vice-voorzitter van de vergadering.
        portefeuillehouder: Ambtenaar die de verantwoordelijkheid draagt over
         een besproken onderwerp.
        griffier: Hoofd van de griffie.
        raadslid: Gekozen volksvertegenwoordiger binnen een
         gemeente.
        statenlid: Gekozen volksvertegenwoordiger binnen een
         provincie.
        kamerlid: Gekozen volksvertegenwoordiger binnen de Eerste of
         Tweede Kamer.
        dagelijks_bestuurslid: Lid van een dagelijks bestuur.
        algemeen_bestuurslid: Lid van een algemeen bestuur.
        inspreker: Niet-lid dat inspreekt tijdens de vergadering.
    """
    voorzitter = _BegripGegevens(
        "Voorzitter",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#deelnemerrollen", "ORI-A Deelnemerrollen")
    )
    """De voorzitter van de vergadering."""
    vice_voorzitter = _BegripGegevens(
        "Vice-voorzitter",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#deelnemerrollen", "ORI-A Deelnemerrollen")
    )
    """De vice-voorzitter van de vergadering."""
    portefeuillehouder = _BegripGegevens(
        "Portefeuillehouder",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#deelnemerrollen", "ORI-A Deelnemerrollen")
    )
    """Ambtenaar die de verantwoordelijkheid draagt over een besproken onderwerp."""
    griffier = _BegripGegevens(
        "Griffier",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#deelnemerrollen", "ORI-A Deelnemerrollen")
    )
    """Hoofd van de griffie."""
    raadslid = _BegripGegevens(
        "Raadslid",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#deelnemerrollen", "ORI-A Deelnemerrollen")
    )
    """Gekozen volksvertegenwoordiger binnen een gemeente."""
    statenlid = _BegripGegevens(
        "Statenlid",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#deelnemerrollen", "ORI-A Deelnemerrollen")
    )
    """Gekozen volksvertegenwoordiger binnen een provincie."""
    kamerlid = _BegripGegevens(
        "Kamerlid",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#deelnemerrollen", "ORI-A Deelnemerrollen")
    )
    """Gekozen volksvertegenwoordiger binnen de Eerste of Tweede Kamer."""
    dagelijks_bestuurslid = _BegripGegevens(
        "Dagelijks bestuurslid",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#deelnemerrollen", "ORI-A Deelnemerrollen")
    )
    """Lid van een dagelijks bestuur."""
    algemeen_bestuurslid = _BegripGegevens(
        "Algemeen bestuurslid",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#deelnemerrollen", "ORI-A Deelnemerrollen")
    )
    """Lid van een algemeen bestuur."""
    inspreker = _BegripGegevens(
        "Inspreker",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#deelnemerrollen", "ORI-A Deelnemerrollen")
    )
    """Niet-lid dat inspreekt tijdens de vergadering."""
    
    _alt_labels = {}


class Mediabrontypes(metaclass=_Begrippenlijst):
    """
    Gangbare mediaformaten waarin vergaderingen worden vastgesteld.

    Attributes:
        video: Een audiovisuele opname van een vergadering.
        audio: Een geluidsopname van een vergadering.
        transcriptie: Een schriftelijke uitwerking van de gesproken
         inhoud van een vergadering.
    """
    video = _BegripGegevens(
        "Video",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#mediabrontypes", "ORI-A Mediabrontypes")
    )
    """Een audiovisuele opname van een vergadering."""
    audio = _BegripGegevens(
        "Audio",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#mediabrontypes", "ORI-A Mediabrontypes")
    )
    """Een geluidsopname van een vergadering."""
    transcriptie = _BegripGegevens(
        "Transcriptie",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#mediabrontypes", "ORI-A Mediabrontypes")
    )
    """Een schriftelijke uitwerking van de gesproken inhoud van een vergadering."""
    
    _alt_labels = {'Videotuul': 'Video', 'Audiotuul': 'Audio'}


class Vergaderstuktypes(metaclass=_Begrippenlijst):
    """
    Vergaderstuktypes die binnen het ORI-A project worden gedefinieerd en beheerd.

    Attributes:
        voorstel: Plan waarover een besluit genomen kan worden.
        motie: Gemotiveerde verklaring waardoor een mening of
         verzoek wordt uitgesproken.
        motie_voorstel: Motie met een voorstel tot handelen.
        motie_wantrouwen: Motie van wantrouwen.
        motie_treurnis: Motie van treurnis.
        motie_afkeuring: Motie van afkeuring.
        motie_vreemd: Motie over een onderwerp dat niet op de agenda
         staat.
        amendement: Voorstel om een bestaand voorstel te wijzigen.
        toezegging: Toezegging van een gedeputeerde of raadslid.
        vraag: Vraag aan een overheidsorgaan.
        vraag_technische_vraag: Vraag naar feitelijke informatie.
        vraag_schriftelijke_politieke_vraag: Schriftelijk ingediende vraag over een politiek
         standpunt.
        vraag_mondelinge_politieke_vraag: Mondelinge vraag over een politiek standpunt.
        antwoord: Antwoord op een vraag.
        ingekomen_stuk: Een stuk gericht aan de raad.
        mededeling: Een mededeling.
    """
    voorstel = _BegripGegevens(
        "Voorstel",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Plan waarover een besluit genomen kan worden."""
    motie = _BegripGegevens(
        "Motie",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Gemotiveerde verklaring waardoor een mening of verzoek wordt uitgesproken."""
    motie_voorstel = _BegripGegevens(
        "Motie | Voorstel",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Motie met een voorstel tot handelen."""
    motie_wantrouwen = _BegripGegevens(
        "Motie | Wantrouwen",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Motie van wantrouwen."""
    motie_treurnis = _BegripGegevens(
        "Motie | Treurnis",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Motie van treurnis."""
    motie_afkeuring = _BegripGegevens(
        "Motie | Afkeuring",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Motie van afkeuring."""
    motie_vreemd = _BegripGegevens(
        "Motie | Vreemd",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Motie over een onderwerp dat niet op de agenda staat."""
    amendement = _BegripGegevens(
        "Amendement",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Voorstel om een bestaand voorstel te wijzigen."""
    toezegging = _BegripGegevens(
        "Toezegging",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Toezegging van een gedeputeerde of raadslid."""
    vraag = _BegripGegevens(
        "Vraag",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Vraag aan een overheidsorgaan."""
    vraag_technische_vraag = _BegripGegevens(
        "Vraag | Technische vraag",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Vraag naar feitelijke informatie."""
    vraag_schriftelijke_politieke_vraag = _BegripGegevens(
        "Vraag | Schriftelijke politieke vraag",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Schriftelijk ingediende vraag over een politiek standpunt."""
    vraag_mondelinge_politieke_vraag = _BegripGegevens(
        "Vraag | Mondelinge politieke vraag",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Mondelinge vraag over een politiek standpunt."""
    antwoord = _BegripGegevens(
        "Antwoord",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Antwoord op een vraag."""
    ingekomen_stuk = _BegripGegevens(
        "Ingekomen stuk",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Een stuk gericht aan de raad."""
    mededeling = _BegripGegevens(
        "Mededeling",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderstuktypes", "ORI-A Vergaderstuktypes")
    )
    """Een mededeling."""
    
    _alt_labels = {}


class Functies(metaclass=_Begrippenlijst):
    """
    Begrippen om de functie of ambt van een persoon mee vast te leggen.

    Attributes:
        commissaris_van_de_koning: Voorzitter van het algemeen en dagelijks bestuur
         van een provincie.
        burgemeester: Voorzitter van het algemeen en dagelijks bestuur
         van een gemeente.
        dijkgraaf: Voorzitter van het algemeen en dagelijks bestuur
         van een waterschap.
        statenlid: Lid van het algemeen bestuur van een provincie.
        raadslid: Lid van het algemeen bestuur van een gemeente.
        algemeen_bestuurslid: Lid van een algemeen bestuur.
        gedeputeerde: Lid van het dagelijks bestuur van een provincie.
        wethouder: Lid van het dagelijks bestuur van een gemeente.
        heemraad: Lid van het dagelijks bestuur van een waterschap.
        dagelijks_bestuurslid: Lid van een dagelijks bestuur.
        griffier: Secretaris van het algemeen bestuur van een
         gemeente of provincie.
        secretaris_directeur: Secretaris van het algemeen en dagelijks bestuur
         van een waterschap.
        provinciesecretaris: Secretaris van het dagelijks bestuur van een
         provincie.
        gemeentesecretaris: Secretaris van het dagelijks bestuur van een
         gemeente.
        commissielid: Door het algemeen bestuur van een overheidsorgaan
         benoemd lid van een commissie of werkgroep.
        commissielid_burgerlid: Een niet-verkozen lid van een commissie of
         werkgroep.
        commissielid_commissievoorzitter: Voorzitter van een commissie of werkgroep.
        ambtenaar_of_medewerker: Een overheidsmedewerker.
        adviseur_of_deskundige: Een door de overheid ingehuurde adviseur of
         deskundige.
    """
    commissaris_van_de_koning = _BegripGegevens(
        "Commissaris van de Koning",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Voorzitter van het algemeen en dagelijks bestuur van een provincie."""
    burgemeester = _BegripGegevens(
        "Burgemeester",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Voorzitter van het algemeen en dagelijks bestuur van een gemeente."""
    dijkgraaf = _BegripGegevens(
        "Dijkgraaf",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Voorzitter van het algemeen en dagelijks bestuur van een waterschap."""
    statenlid = _BegripGegevens(
        "Statenlid",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Lid van het algemeen bestuur van een provincie."""
    raadslid = _BegripGegevens(
        "Raadslid",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Lid van het algemeen bestuur van een gemeente."""
    algemeen_bestuurslid = _BegripGegevens(
        "Algemeen bestuurslid",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Lid van een algemeen bestuur."""
    gedeputeerde = _BegripGegevens(
        "Gedeputeerde",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Lid van het dagelijks bestuur van een provincie."""
    wethouder = _BegripGegevens(
        "Wethouder",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Lid van het dagelijks bestuur van een gemeente."""
    heemraad = _BegripGegevens(
        "Heemraad",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Lid van het dagelijks bestuur van een waterschap."""
    dagelijks_bestuurslid = _BegripGegevens(
        "Dagelijks bestuurslid",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Lid van een dagelijks bestuur."""
    griffier = _BegripGegevens(
        "Griffier",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Secretaris van het algemeen bestuur van een gemeente of provincie."""
    secretaris_directeur = _BegripGegevens(
        "Secretaris-directeur",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Secretaris van het algemeen en dagelijks bestuur van een waterschap."""
    provinciesecretaris = _BegripGegevens(
        "Provinciesecretaris",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Secretaris van het dagelijks bestuur van een provincie."""
    gemeentesecretaris = _BegripGegevens(
        "Gemeentesecretaris",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Secretaris van het dagelijks bestuur van een gemeente."""
    commissielid = _BegripGegevens(
        "Commissielid",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Door het algemeen bestuur van een overheidsorgaan benoemd lid van een commissie of werkgroep."""
    commissielid_burgerlid = _BegripGegevens(
        "Commissielid | Burgerlid",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Een niet-verkozen lid van een commissie of werkgroep."""
    commissielid_commissievoorzitter = _BegripGegevens(
        "Commissielid | Commissievoorzitter",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Voorzitter van een commissie of werkgroep."""
    ambtenaar_of_medewerker = _BegripGegevens(
        "Ambtenaar of medewerker",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Een overheidsmedewerker."""
    adviseur_of_deskundige = _BegripGegevens(
        "Adviseur of deskundige",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#functies", "ORI-A Functies")
    )
    """Een door de overheid ingehuurde adviseur of deskundige."""
    
    _alt_labels = {'Commissaris van de Koningin': 'Commissaris van de Koning', 'Gouverneur van Limburg': 'Commissaris van de Koning', 'Watergraaf': 'Dijkgraaf', 'Hoogheemraad': 'Heemraad'}


class Vergaderingstypes(metaclass=_Begrippenlijst):
    """
    Soorten vergaderingen.

    Attributes:
        raadsvergadering: Vergadering van een gemeenteraad.
        commissievergadering: Vergadering van een commissie.
        collegevergadering: Vergadering van een college.
        statenvergadering: Vergadering van Provinciale Staten.
        algemene_bestuursvergadering: Vergadering van een algemeen bestuur.
        dagelijks_bestuursvergadering: Vergadering van een dagelijks bestuur.
        presidium: Vergadering van een presidium.
    """
    raadsvergadering = _BegripGegevens(
        "Raadsvergadering",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderingstypes", "ORI-A Vergaderingstypes")
    )
    """Vergadering van een gemeenteraad."""
    commissievergadering = _BegripGegevens(
        "Commissievergadering",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderingstypes", "ORI-A Vergaderingstypes")
    )
    """Vergadering van een commissie."""
    collegevergadering = _BegripGegevens(
        "Collegevergadering",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderingstypes", "ORI-A Vergaderingstypes")
    )
    """Vergadering van een college."""
    statenvergadering = _BegripGegevens(
        "Statenvergadering",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderingstypes", "ORI-A Vergaderingstypes")
    )
    """Vergadering van Provinciale Staten."""
    algemene_bestuursvergadering = _BegripGegevens(
        "Algemene bestuursvergadering",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderingstypes", "ORI-A Vergaderingstypes")
    )
    """Vergadering van een algemeen bestuur."""
    dagelijks_bestuursvergadering = _BegripGegevens(
        "Dagelijks bestuursvergadering",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderingstypes", "ORI-A Vergaderingstypes")
    )
    """Vergadering van een dagelijks bestuur."""
    presidium = _BegripGegevens(
        "Presidium",
        _VerwijzingGegevens("https://ori-a.nl/begrippenlijsten#vergaderingstypes", "ORI-A Vergaderingstypes")
    )
    """Vergadering van een presidium."""
    
    _alt_labels = {'Algemeen bestuursvergadering': 'Algemene bestuursvergadering'}

