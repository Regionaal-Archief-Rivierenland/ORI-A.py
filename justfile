default: build

build:
    touch ORI_A/ORI_A.py
    # ensure file is syntactically correct before rendering
    python -m py_compile templates/ORI_A.py.j2
    # make file temporarily writeable
    chmod u+w ORI_A/ORI_A.py
    ./generate_docstrings.py ORI-A-XSD/ORI-A.xsd templates/ORI_A.py.j2
    chmod u-w ORI_A/ORI_A.py

    touch ORI_A/begrippenlijsten.py
    chmod u+w ORI_A/begrippenlijsten.py
    ./generate_begrippenlijsten.py
    chmod u-w ORI_A/begrippenlijsten.py

test:
    pytest

clean:
    # noop
