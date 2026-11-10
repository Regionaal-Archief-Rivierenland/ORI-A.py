#!/bin/python

from pathlib import Path
from jinja2 import FileSystemLoader, Environment
from rdflib import Graph, SKOS, RDF, OWL, DCTERMS

def build_label(concept, g):
    """Recursively prepend broader concept labels, e.g. 'A | B | C'."""
    label = g.value(concept, SKOS.prefLabel)

    if broader := g.value(concept, SKOS.broader):
        return f"{build_label(broader, g)} | {label}"
    else:
        return label

env = Environment(loader=FileSystemLoader(["templates"]))
template = env.get_template("begrippenlijsten.py.j2")

begrippenlijsten = []
for ttl in Path("ori-a-begrippenlijsten").glob("*.ttl"):
    g = Graph()
    g.parse(ttl)
    begrippen = []
    alt_labels = {}

    for concept in g.subjects(RDF.type, SKOS.Concept):
        label = build_label(concept, g)
        naam = label.lower().replace(" | ", "_").replace(" ", "_").replace("-", "_")
        begrippen.append(
            {
                "naam": naam,
                "label": label,
                "definitie": g.value(concept, SKOS.definition) or "",
                "deprecated": bool(g.value(concept, OWL.deprecated)),
            }
        )
        alt_labels.update({str(alt): str(label) for alt in list(g.objects(concept, SKOS.altLabel))})

    begrippenlijst = next(g.subjects(RDF.type, SKOS.ConceptScheme))
    naam = g.value(begrippenlijst, DCTERMS.title)
    # not sure if CamelCase is the way here
    cls_naam = naam.title().replace(" ", "").replace("-", "")
    begrippenlijsten.append(
        {
            "naam": naam,
            "cls_naam": cls_naam,
            "url": str(begrippenlijst),
            "omschrijving": g.value(begrippenlijst, DCTERMS.description),
            "alt_labels": alt_labels,
            "begrippen": begrippen,
        }
    )

with open("ORI_A/begrippenlijsten.py", "w+") as f:
    f.write(template.render(begrippenlijsten=begrippenlijsten))
