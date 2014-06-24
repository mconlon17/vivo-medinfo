# Consume Medinfo data

Medinfo is a long running directory system of the University of Florida College of Medicine Office of Medical Informatics that tracks some data elements of interest to VIVO.  The software here reads Medinfo data and updates VIVO accordingly.

## Data Elements updated from Medinfo

1. Photo
2. Education
3. Medical speciality
4. Awards and honors

Other data elements are considered to authoritative from other source.  Home Department, for example comes to UF VIVO from the UF HR System.

## Technique

Medinfo data is formatted in XML.  We use elementree to read and navigate the resulting DOM.
