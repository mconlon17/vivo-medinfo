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

def improve_certification(cert):
    """
    Board certification information is provided by physicians in open text form.
    This function tkaes the variations supplied by the physicians and returns
    standard certification names.  Input is text.  Output is a list of certs.
    """
    cert = cert.title()
    certs = []
    if cert.find('Pediatric Dentistry') > -1:
        certs.append('Pediatric Dentistry')
        return certs
    if cert.find('Eligible') > -1:
        return certs
    if cert.find('Advanced Heart Failure And Transplant Cardiology') > -1:
        certs.append('Advanced Heart Failure')
        certs.append('Transplant Cardiology')
        return certs
    if cert.find('Anatomic And Clinical Pathology') > -1:
        certs.append('Anatomic Pathology')
        certs.append('Clinical Pathology')
        return certs
    if cert.find('Anatomic Pathology And Clinical Pathology') > -1:
        certs.append('Anatomic Pathology')
        certs.append('Clinical Pathology')
        return certs
    if cert.find('Radiation Oncology') > -1:
        certs.append('Radiation Oncology')
        return certs
    if cert.find('General Surgery') > -1:
        certs.append('General Surgery')
        return certs
    if cert.find('Neurotology/Otology') > -1:
        certs.append('Neurotology')
        certs.append('Otology')
        return certs
    if cert.find('Nrp Instructor') > -1:
        return certs
    if cert.find('Florida License 1998') > -1:
        return certs
    if cert.find('American Board Of Oral Medicine 1986 And American Board Of Oral And Maxillofacial Pathology') > -1:
        certs.append('Oral Medicine')
        certs.append('Oral and Maxillofacial Pathology')
        return certs
    if cert.find('Board Certified In Both General And Vascular Surgery By The American Board Of Surgery') > -1:
        certs.append('General Surgery')
        certs.append('Vascular Surgery')
        return certs
    if cert.find('Congenital Heart Surgery,') > -1:
        certs.append('Congenital Heart Surgery')
        return certs
    if cert.find('American Board Of Thoracic Surgery') > -1:
        certs.append('Thoracic Surgery')
        return certs
    if cert.find('American Board Of Surgery') > -1:
        certs.append('General Surgery')
        return certs
    if cert.find('Blood Banking And Transfusion Medicine Certification - American Board Of Pathology, 1993') > -1:
        certs.append('Blood Banking and Transfusion Medicine')
        return certs
    if cert.find('Medical Management') > -1:
        certs.append('Medical Management')
        return certs
    if cert.find('Double Boarded In Psychiatry And Addiction Medicine.') > -1:
        certs.append('Psychiatry')
        certs.append('Addiction Medicine')
        return certs
    if cert.find('-Forensic Pathology') > -1:
        certs.append('Forensic Pathology')
        return certs
    if cert.find(', Dermatopathology') > -1:
        certs.append('Dermatopathology')
        return certs
    if cert.find('American Board Of Dermatology') > -1:
        certs.append('Dermatology')
        return certs
    if cert.find('American Academy Of Dermatology') > -1:
        return certs
    if cert.find('American Board Of Oral And Maxillofacial Pathology') > -1:
        certs.append('Oral and Maxillofacial Pathology')
        return certs
    if cert.find('National Board Of Medical Examiners') > -1:
        certs.append('National Board of Medical Examiners')
        return certs
    if cert.find('General Psychiatry By The American') > -1:
        certs.append('General Psychiatry')
        return certs
    if cert.find('Abr Physics And') > -1:
        certs.append('Physics and Radiobiology')
        return certs
    if cert.find('Medical License') > -1:
        return certs
    if cert.find('Royal College Of Physicians And Surgeons Of Canada') > -1:
        return certs
    if cert.find('American Board Of Prosthodontics') > -1:
        certs.append('Prosthodontics')
        return certs
    if cert.find('American Board Of Neurological Surgery') > -1:
        certs.append('Neurological Surgery')
        return certs
    if cert.find('American Board Of Neurology And Psychiatry') > -1:
        certs.append('Neurology')
        certs.append('Psychiatry')
        return certs
    if cert.find('Pediatric Nurse Practitioner') > -1:
        certs.append('Pediatric Nursing')
        return certs
    if cert.find('Pediatric Primary Care Mental Health Specialist') > -1:
        certs.append('Pediatric Primary Care Mental Health')
        return certs
    if cert.find('American Board Of Pathology- Anatomic') > -1:
        certs.append('Anatomic Pathology')
        return certs
    if cert.find('American Board Of Pathology And Dermatology- Dermatopathology') > -1:
        certs.append('Dermatopathology')
        return certs
    if cert.find('Diplomate. American Board Of Forensic Toxicology') > -1:
        certs.append('Forensic Toxicology')
        return certs
    if cert.find('Clinical Laboratory Director') > -1:
        return certs
    if cert.find('Toxicological Chemist') > -1:
        return certs
    if cert.find('Orthodontics') > -1:
        certs.append('Orthodontics')
        return certs
    if cert.find('Therapeutic Radiology') > -1:
        certs.append('Therapeutic Radiology')
        return certs
    if cert.find('American Board Of Radiology 2009') > -1:
        certs.append('Radiology')
        return certs
    if cert.find('American Board Of Medical Specialties (Abms) Board Certified In:') > -1:
        return certs
    if cert.find('Diplomat, American Board Of Neurological Surgeons, 1992') > -1:
        certs.append('Neurological Surgery')
        return certs
    if cert.find('Fellow, American College Of Surgeons, 1993') > -1:
        return certs
    if cert.find('Diplomat, American Board Of Medical Examiners, 1984') > -1:
        certs.append('National Board of Medical Examiners')
        return certs
    if cert.find('American Board Of Obstetrics And Gynecology') > -1:
        certs.append('Obstetrics and Gyencology')
        return certs
    if cert.find('Maternal-Fetal Medicine') > -1:
        certs.append('Maternal-Fetal Medicine')
        return certs
    if cert.find('American Board Of Internal Medicine') > -1:
        certs.append('Internal Medicine')
        return certs
    if cert.find('American Board Of Psychiatry And Neurology') > -1:
        certs.append('Psychiatry')
        certs.append('Neurology')
        return certs
    if cert.find('Diplomat In Sleep Medicine American Board Of Internal Medicine') > -1:
        certs.append('Sleep Medicine')
        return certs
    if cert.find('Double Boarded In Adult Psychiatry And Geriatric Psychiatry') > -1:
        certs.append('Adult Psychiatry')
        certs.append('Geriatric Psychiatry')
        return certs
    if cert.find('Pediatric Surgery And Surgery (General)') > -1:
        certs.append('Pediatric Surgery')
        certs.append('General Surgery')
        return certs
    if cert.find('American Board Of Radiology, 1991') > -1:
        certs.append('Radiology')
        return certs
    if cert.find('Diplomate American Board Of Periodontology') > -1:
        certs.append('Periodontology')
        return certs
    if cert.find('Anesthesiology (Recertified 2010)') > -1:
        certs.append('Anesthesiology')
        return certs
    if cert.find('American Board Of Radiology (Therapeutic) 1985') > -1:
        certs.append('Therapeutic Radiology')
        return certs
    if cert.find('American Board Of Radiology (Therapeutic), 1983') > -1:
        certs.append('Therapeutic Radiology')
        return certs
    if cert.find('National Board Of Echocardiography') > -1:
        certs.append('Echocardiography')
        return certs
    if cert.find('Board Certified In Critical Care Surgery') > -1:
        certs.append('Critical Care Surgery')
        return certs
    if cert.find('Board Certified Periodontist (Abp)') > -1:
        certs.append('Periodontology')
        return certs
    if cert.find('American College Of Mohs Surgery, 2008') > -1:
        certs.append('Mohs Surgery')
        return certs
    if cert.find('American Society Of Dermatologic Surgery') > -1:
        return certs
    if cert.find('American Society For Laser Medicine And Surgery') > -1:
        return certs
    if cert.find('Vascukar And Interventional Radiology') > -1:
        certs.append('Vascular Radiology')
        certs.append('Interventional Rdiology')
        return certs
    if cert.find('Transthoracic Plus Transesophageal Certification, National Board Of Echocardiography') > -1:
        certs.append('Transthoracic Echocardiography')
        certs.append('Transesophageal Echocardiography')
        return certs
    if cert.find('Abim Board Certified, Cardiovascular Disease') > -1:
        certs.append('Cardiovascular Disease')
        return certs
    if cert.find('Diplomate, Internal Medicine') > -1:
        certs.append('Internal Medicine')
        return certs
    if cert.find('Medical Microbiology') > -1:
        certs.append('Medical Microbiology')
        return certs
    if cert.find('Hand Surgery') > -1:
        certs.append('Hand Surgery')
        return certs
    if cert.find('Anatomic Pathology') > -1:
        certs.append('Anatomic Pathology')
        return certs
    if cert.find('Neuropathology') > -1:
        certs.append('Neuropathology')
        return certs
    if cert.find('Member') > -1:
        return certs
    if cert.find('Course') > -1:
        return certs
    if cert.find('Aha Bls Recertification For Health Providers') > -1:
        certs.append('Basic Life Support')
        return certs
    if cert.find('Board Certified In Surgery') > -1:
        certs.append('Surgery')
        return certs
    if cert.find('Addiction Medicine') > -1:
        certs.append('Addiction Medicine')
        return certs
    if cert.find('Clinical Psychology') > -1:
        certs.append('Clinical Psychology')
        return certs
    if cert.find('Clinical Health Psychology') > -1:
        certs.append('Clinical Health Psychology')
        return certs
    certs.append(cert)
    return certs

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
                rawcerts = child.text.split('\n')
                for rawcert in rawcerts:
                    rawcert.strip()
                    if len(rawcert) > 0:
                        certs = improve_certification(rawcert)
                        for cert in certs:
                            if len(cert) > 0:
                                mperson['board_certifications'].append(cert)
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
    person_uri = find_vivo_uri('ufVivo:ufid', mperson['ufid'])
    if person_uri is not None:
        mperson['uri'] = person_uri
        found = found + 1
        if 'board_certifications' in mperson and \
            len(mperson['board_certifications']) > 0:
            k = k + 1
            print k, mperson['ufid']
            for cert in mperson['board_certifications']:
                print '\t\t',cert

    else:
        not_found = not_found + 1
        print >>exc_file, not_found, "Person Not Found", mperson['ufid']

adrf = ardf + rdf_footer()
srdf = srdf + rdf_footer()
add_file.write(ardf)
sub_file.write(srdf)
add_file.close()
sub_file.close()

print >>log_file, datetime.now(), "Found = ", found
print >>log_file, datetime.now(), "Fot found = ", not_found
print >>log_file, datetime.now(), "Finished"

