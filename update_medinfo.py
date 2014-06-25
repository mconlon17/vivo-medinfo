#!/usr/bin/env/python
"""
    update_medinfo.py -- Reaad medinfo XML data and update corresponding
    information in VIVO

    Version 0.0 MC 2014-06-24
    --  just starting
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.0"

__harvest_text__ = "Python Medinfo " + __version__

from vivotools import rdf_header
from vivotools import rdf_footer
from vivotools import get_person
from vivotools import find_vivo_uri
import vivotools as vt

from datetime import datetime
import xml.etree.ElementTree as ET
import json
import sys
import os
import codecs

def prepare_medinfo(input_file_name):
    """
    Given a file name with medinfo data, use element tree to parse the
    XML found in the file and return a list of VIVO person data structures
    """
    tree = ET.parse(input_file_name)
    root = tree.getroot()
    channel = root[0]
    medinfo = []
    for item in channel.findall('item'):
        for provider in item.findall('provider'):
            mperson = {}
            for child in provider.findall('ufid'):
                mperson['ufid'] = child.text
            for child in provider.findall('photo'):
                mperson['photo_url'] = child.text
            for child in provider.findall('honors'):
                mperson['honors'] = child.text
            mperson['degrees'] = []
            for child in provider.findall('education'):
                for p in child.findall('p'):
                    mperson['degrees'].append(p.text)
            mperson['board_certifications'] = []
            for child in provider.findall('boardcertification'):
                for p in child.findall('p'):
                    mperson['board_certifications'].append(p.text)
            medinfo.append(mperson)
    return medinfo

def update_person(vperson, sperson):
    """
    Given a VIVO person object and a source person object, generate the RDF
    necessary to update the data for the person in VIVO so as to match the
    source
    """
    ardf = ""
    srdf = ""
    return [ardf, srdf]

# Start here

if len(sys.argv) > 1:
    input_file_name = str(sys.argv[1])
else:
    input_file_name = "medinfo2.txt"
file_name, file_extension = os.path.splitext(input_file_name)

add_file = codecs.open(file_name+"_add.rdf", mode='w', encoding='ascii',
                       errors='xmlcharrefreplace')
sub_file = codecs.open(file_name+"_sub.rdf", mode='w', encoding='ascii',
                       errors='xmlcharrefreplace')
log_file = sys.stdout
##log_file = codecs.open(file_name+"_log.txt", mode='w', encoding='ascii',
##                       errors='xmlcharrefreplace')
exc_file = codecs.open(file_name+"_exc.txt", mode='w', encoding='ascii',
                       errors='xmlcharrefreplace')

ardf = rdf_header()
srdf = rdf_header()

print >>log_file, datetime.now(), "Start"
print >>log_file, datetime.now(), "Update Medinfo Version", __version__
print >>log_file, datetime.now(), "VIVO Tools Version", vt.__version__
print >>log_file, datetime.now(), "Read Medinfo Data"
medinfo = prepare_medinfo(input_file_name)

print >>log_file, datetime.now(), "Medinfo Data has", len(medinfo), "people"
found = 0
not_found = 0
k = 0
for mperson in medinfo:
    k = k + 1
    print mperson
    if k > 10:
        break
    person_uri = find_vivo_uri('ufVivo:ufid', mperson['ufid'])
    if person_uri is not None:
        mperson['uri'] = person_uri
        found = found + 1
        print >>log_file, found, "Updating Person at", mperson['uri']

    else:
        not_found = not_found + 1
        print >>log_file, not_found, "Person Not Found", mperson['ufid']

adrf = ardf + rdf_footer()
srdf = srdf + rdf_footer()
print >>add_file, adrf
print >>sub_file, srdf
add_file.close()
sub_file.close()

print >>log_file, datetime.now(), "Found = ", found
print >>log_file, datetime.now(), "Fot found = ", not_found
print >>log_file, datetime.now(), "Finished"

