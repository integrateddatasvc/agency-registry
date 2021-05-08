'''
Utility functions for the agency-registry
'''

import json
import logging
import os
import requests
from xml.etree import ElementTree
import yaml

def delete_agency_crossref_file(catalog, agency):
    file = get_agency_crossref_file(catalog, agency)
    if os.path.isfile(file):
        logging.info(f"Deleting CrossRef file {file}")
        try:
            os.remove(file)
        except OSError:
            pass    

def delete_agency_isni_file(catalog, agency):
    file = get_agency_isni_file(catalog, agency)
    if os.path.isfile(file):
        logging.info(f"Deleting ISNI file {file}")
        try:
            os.remove(file)
        except OSError:
            pass    

def delete_agency_ror_file(catalog, agency):
    ror_file = get_agency_ror_file()
    if os.path.isfile(ror_file):
        logging.info(f"Deleting ROR file {ror_file}")
        try:
            os.remove(ror_file)
        except OSError:
            pass    

def get_catalog_dir(catalog):
    return os.path.join(get_registry_dir(), catalog)

def get_agency_dir(catalog, agency):
    return os.path.join(get_registry_dir(), catalog, agency)

def get_agency_external_dir(catalog, agency):
    # returns the agency's external data directory
    dir = os.path.join(get_agency_dir(catalog, agency),'external')
    if not os.path.isdir(dir):
        os.mkdir(dir)
    return dir

def get_agency_geo(catalog, agency):
    data = load_yaml(get_agency_geo_file(catalog, agency))
    return data

def get_agency_geo_file(catalog, agency):
    file = os.path.join(get_agency_dir(catalog, agency),'geo.yaml')
    return file

def get_agency_ids(catalog, agency):
    data = load_yaml(get_agency_ids_file(catalog, agency))
    return data

def get_agency_ids_file(catalog, agency):
    file = os.path.join(get_agency_dir(catalog, agency),'ids.yaml')
    return file

def get_agency_info_name(catalog, agency):
    name = agency
    return name

def get_agency_info(catalog, agency):
    info = {}
    info['name'] = get_agency_info_name(catalog, agency)
    return 

def get_agency_crossref(catalog, agency):
    file = get_agency_crossref_file(catalog, agency)
    if not os.path.isfile(file):
        harvest_agency_crossref(catalog, agency)
    with open(file, 'r') as f:
        data = json.load(f)
        return data

def get_agency_crossref_file(catalog, agency):
    file = os.path.join(get_agency_external_dir(catalog, agency),'crossref.json')
    return file

def get_agency_isni_file(catalog, agency):
    file = os.path.join(get_agency_external_dir(catalog, agency),'isni.xml')
    return file

def get_agency_ror(catalog, agency):
    ror_file = get_agency_ror_file(catalog, agency)
    if not os.path.isfile(ror_file):
        harvest_agency_ror(catalog, agency)
    if os.path.isfile(ror_file):
        with open(ror_file, 'r') as f:
            data = json.load(f)
            return data

def get_agency_ror_file(catalog, agency):
    ror_file = os.path.join(get_agency_external_dir(catalog, agency),'ror.json')
    return ror_file

def get_agency_services(catalog, agency):
    data = load_yaml(get_agency_services_file(catalog, agency))
    return data

def get_agency_services_file(catalog, agency):
    file = os.path.join(get_agency_dir(catalog, agency),'services.yaml')
    return file

def get_agency_social(catalog, agency):
    data = load_yaml(get_agency_social_file(catalog, agency))
    return data

def get_agency_social_file(catalog, agency):
    file = os.path.join(get_agency_dir(catalog, agency),'social.yaml')
    return file

def get_registry_dir():
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__))+'/../_data')

def get_schema(schema):
    schema_file = get_schema_file(schema, format='yaml')
    return load_yaml(schema_file)

def get_schema_file(schema, format='yaml'):
    return os.path.join(get_schemas_dir(),f"{schema}.{format}")

def get_schemas_dir():
    return os.path.join(get_script_dir(),'../schemas')

def get_script_dir():
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def harvest_agency_crossref(catalog, agency):
    # harvest the agency metadata from the CrossRef registry
    # returns JSON string
    id = get_agency_ids(catalog, agency).get('crossref')
    if id:
        url = f"https://api.crossref.org/funders/{id}"
        response = requests.get(url)
        return response.json()

def harvest_agency_isni(catalog, agency):
    # harvest the agency metadata from the ISNI registry
    # returns XML string
    id = get_agency_ids(catalog, agency).get('isni')
    if id:
        print(f"ISNI:{id}")
        url = f"http://isni.oclc.org/sru/?query=pica.isn+%3D+%22{id}%22&operation=searchRetrieve&recordSchema=isni-b"
        print(f"ISNI url {url}")
        response = requests.get(url)
        searchRetrieveResponse = ElementTree.fromstring(response.content)
        isni = searchRetrieveResponse.find('.//ISNIAssigned')
        return isni

def harvest_agency_ror(catalog, agency):
    # harvest the agency metadata from the ROR registry
    # returns JSON string
    ror_id = get_agency_ids(catalog, agency).get('ror')
    if ror_id:
        url = 'http://api.ror.org/organizations/https://ror.org/'+ror_id
        response = requests.get(url)
        return response.json()

def load_yaml(file):
    if os.path.isfile(file):
        with open(file) as f:
            data = yaml.load(f, Loader=yaml.FullLoader) 
            return data
    return {}

def save_agency_crossref(catalog, agency, data):
    # save the CrossRef metadata
    with open(get_agency_crossref_file(catalog, agency), 'w') as f:
        json.dump(data, f, indent=4)

def save_agency_isni(catalog, agency, xml):
    # save the ISNI metadata
    xml = ElementTree.tostring(xml, encoding='utf8')
    with open(get_agency_isni_file(catalog, agency), 'wb') as f:
        f.write(xml) 
    return

def save_agency_ror(catalog, agency, data):
    # save the ROR metadata
    with open(get_agency_ror_file(catalog, agency), 'w') as f:
        json.dump(data, f, indent=4)

