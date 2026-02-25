import dataclasses
from enum import Enum
from typing import Union, get_args, get_origin, get_type_hints
from uuid import uuid4

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlTime

from ORI_A.ORI_A import ORI_A, AgendapuntGegevens, Serializable, VergaderingGegevens

# TODO: ORI-A has legit instances where a field can take on muliple values 

class_dummy_map = {
    int: 1,
    str: "test",
    bool: True,
    XmlDate: "22-05-2017",
    XmlDateTime: "22-05-2017T03:02:01",
    XmlTime: "03:02:01",
    # these exists to halt infinite recursion
    VergaderingGegevens: VergaderingGegevens(naam="test", datum="22-05-2017"),
    AgendapuntGegevens: AgendapuntGegevens("test", "test"),
}

def _init_obj(cls: Serializable) -> Serializable:
    """init an object with dummy values"""
    class_args = {}
    hints = get_type_hints(cls)

    for field in dataclasses.fields(cls):
        field_type = hints[field.name]
        
        # get field's expected type
        if get_origin(field_type) is Union:
            repeatable = True
            field_type = get_args(field_type)[0]
        else:
            repeatable = False

        # avoid recursing infinitely if parent' and child' types are the same
        if field_type is cls:
            class_args[field.name] = class_dummy_map[field_type]
        elif issubclass(field_type, Serializable):
            class_args[field.name] = _init_obj(field_type)
        elif issubclass(field_type, Enum):
            class_args[field.name] = next(iter(field_type)).value
        elif field.name == "ID":
            # IDs must be unique
            class_args[field.name] = uuid4()
        else:
            dummy_val = class_dummy_map[field_type]
            class_args[field.name] = [dummy_val] * 2 if repeatable else dummy_val

    return cls(**class_args)

def test_dataclass_definitions_match_XSD_rules():
    """Test if dataclass field definitions match the rules in the XSD"""
    # do not use getattr and dir: use the ORI-A dataclass itself instead!

    obj = _init_obj(ORI_A)
    obj.to_xml("ORI_A")
    assert True
    
