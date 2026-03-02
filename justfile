default: build

build:
    touch ORI_A/ORI_A.py
    # ensure file is syntactically correct before rendering
    python ORI_A/ORI_A.template.py || exit 1
    # make file temporarily writeable
    chmod u+w ORI_A/ORI_A.py
    ./generate_docstrings.py "ORI_A/ORI_A.xsd" "ORI_A/ORI_A.template.py"
    chmod u-w ORI_A/ORI_A.py

test:
    pytest

clean:
    # noop
