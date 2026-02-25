default: build

build:
    touch ORI_A/ORI_A.py
    # make file temporarily writeable
    chmod u+w ORI_A/ORI_A.py
    ./generate_docstrings.py "ORI-A.xsd" "ORI_A/ORI_A.template.py"
    chmod u-w ORI_A/ORI_A.py

test:
    pytest

clean:
    # noop
