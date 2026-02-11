docstring_old := 'ORI_A:\n    """\n    Attributes'
docstring_new := 'ORI_A:\n    """\n    Gegevens die onder het _root_-element `<ORI-A>` komen.\n\n    Attributes'

default: build

fetch_xsd:
    rm -f ORI-A.xsd
    wget -q https://github.com/Regionaal-Archief-Rivierenland/ORI-A-XSD/releases/latest/download/ORI-A.xsd

build: && monkeypatch
    xsdata generate -c .xsdata.xml ORI-A.xsd

monkeypatch:
    sd -f mc '{{docstring_old}}' '{{docstring_new}}' generated/ORI_A.py
    sd '\s+"namespace": "https://ori-a.nl",' '' generated/ORI_A.py

clean:
    rm -rf generated/
