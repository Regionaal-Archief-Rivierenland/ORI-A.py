import dataclasses
import xml.etree.ElementTree as ET
import ORI_A
import textwrap

from jinja2 import Template

ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
root = ET.parse("ORI-A.xsd").getroot()
MAX_WIDTH = 82
INDENT = 4

with open('ORI_A/ORI_A.template.py') as f:
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
        field_docstring = elem.find("./xs:annotation/xs:documentation", namespaces=ns).text
        field_docstring = textwrap.fill(
            f"{field.name}: {field_docstring}",
            width=MAX_WIDTH,
            initial_indent=" "*(2*INDENT),
            subsequent_indent=" "*(2*INDENT+2),
        )
        class_docstring += field_docstring + "\n"

    class_docstring += " "*INDENT
    # print(class_docstring)
    docs[class_name[0].lower() + class_name[1:]] = class_docstring

with open("ORI_A/ORI_A.py", "w") as f:
    f.write(template.render(docs=docs))

