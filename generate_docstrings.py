#!/bin/python

import dataclasses
import xml.etree.ElementTree as ET
import sys
import ORI_A
import textwrap
import annotationlib
from typing import Union, get_origin, get_args

from jinja2 import Template

MAX_WIDTH = 87
INDENT = 4

xsdfile = sys.argv[1]
ori_a_template = sys.argv[2]

ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
root = ET.parse(xsdfile).getroot()

with open(ori_a_template) as f:
    template = Template(f.read())

# dict that stores full class docstrings by lower camelCase class name
docs = {}

for complex_type in root.findall(".//xs:complexType", namespaces=ns):
    type_name = complex_type.get("name")

    # FIXME: the complexType under ORI-A currently has no associated name
    if not type_name:
        print("skipping")
        continue

    # classes are UpperCamelCase
    class_name = type_name[0].upper() + type_name[1:]

    # get class from module
    cls = getattr(ORI_A, class_name)
    python_ordered_fields = dataclasses.fields(cls)

    class_docstring = textwrap.fill(
        complex_type.find("./xs:annotation/xs:documentation", namespaces=ns).text,
        width=MAX_WIDTH,
        subsequent_indent=" "*INDENT
    )
    class_docstring += f"\n\n{' '*INDENT}Attributes:\n"

    for field in python_ordered_fields:
        elem = complex_type.find(f"./xs:sequence/xs:element[@name='{field.name}']", namespaces=ns)
        optional = not int(elem.attrib["minOccurs"])
        repeatable = True if elem.attrib["maxOccurs"] == "unbounded" else False

        if isinstance(field.type, annotationlib.ForwardRef):
            # nested dataclasses need the replace, for some reason
            field_type_name = f"{field.type.__forward_arg__}".replace(
                " | __annotationlib_name_1__", ""
            )
        elif get_origin(field.type) is Union:
            field_type_name = get_args(field.type)[0].__name__
        else:
            field_type_name = field.type.__name__

        if repeatable and optional:
            cardinality = "[0..*]"
        elif not repeatable and optional:
            cardinality = "[0..1]"
        elif repeatable and not optional:
            cardinality = "[1..*]"
        elif not repeatable and not optional:
            cardinality = "[1..1]"

        field_docstring = elem.find("./xs:annotation/xs:documentation", namespaces=ns).text

        field_docstring = textwrap.fill(
            f"{field.name} ({field_type_name}{cardinality}): " \
            f"{field_docstring}",
            width=MAX_WIDTH,
            initial_indent=" "*(2*INDENT),
            subsequent_indent=" "*(2*INDENT+2),
        )

        class_docstring += field_docstring + "\n"

    class_docstring += " "*INDENT
    docs[class_name[0].lower() + class_name[1:]] = class_docstring

with open("ORI_A/ORI_A.py", "w+") as f:
    f.write(template.render(docs=docs))

