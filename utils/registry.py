'''
Utility functions for the agency-registry
'''

import json
import logging
import os
import requests
import lxml.etree 
from lxml import etree
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

def get_agency_id(catalog, agency, id):
    data = get_agency_ids(catalog, agency)
    if data:
        return data.get(id)

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
    if os.path.isfile(file):
        with open(file, 'r') as f:
            data = json.load(f)
            return data

def get_agency_crossref_file(catalog, agency):
    file = os.path.join(get_agency_external_dir(catalog, agency),'crossref.json')
    return file

def get_agency_isni(catalog, agency):
    file = get_agency_isni_file(catalog, agency)
    if not os.path.isfile(file):
        harvest_agency_isni(catalog, agency)
    if os.path.isfile(file):
        data = etree.parse(file)
        return data

def get_agency_isni_file(catalog, agency):
    file = os.path.join(get_agency_external_dir(catalog, agency),'isni.xml')
    return file

def get_agency_json(catalog, agency):
    "Returns all agency information in a single JSON object"
    crossref = get_agency_crossref(catalog, agency)
    geo = get_agency_geo(catalog, agency)
    ids = get_agency_ids(catalog, agency)
    isni = get_agency_isni(catalog, agency)
    ror = get_agency_ror(catalog, agency)
    services = get_agency_services(catalog, agency)
    social = get_agency_social(catalog, agency)
    wikidata = get_agency_wikidata(catalog, agency, format='json') 
    # generate metadata
    metadata = {}
    if ids:
        metadata['ids'] = ids
    # organization name
    name = agency
    if ror:
        name = ror['name']
    # metadata
    if geo:
        metadata['geo'] = geo
    if services:
        metadata['services'] = services
    if social:
        metadata['social'] = social
    # external metadata
    external = {}
    metadata['external'] = external
    if crossref:
        external['crossref'] = '@todo'
    if isni:
        external['isni'] = '@todo'
    if ror:
        external['ror'] = ror
    if wikidata:
        external['wikidata'] = wikidata
    return metadata


def get_agency_ror(catalog, agency):
    file = get_agency_ror_file(catalog, agency)
    if not os.path.isfile(file):
        harvest_agency_ror(catalog, agency)
    if os.path.isfile(file):
        with open(file, 'r') as f:
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

def get_agency_wikidata(catalog, agency, format='rdf'):
    file = get_agency_wikidata_file(catalog, agency, format)
    if not os.path.isfile(file):
        harvest_agency_wikidata(catalog, agency, format)
    if os.path.isfile(file):
        if format == 'rdf':
            data = etree.parse(file)
        elif format == 'json':
            with open(file, 'r') as f:
                data = json.load(f)
        return data

def get_agency_wikidata_file(catalog, agency, format="rdf"):
    file = os.path.join(get_agency_external_dir(catalog, agency),f"wikidata.{format}")
    return file

def get_catalog_dir(catalog):
    return os.path.join(get_registry_dir(), catalog)

def get_collections_dir():
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__))+'/../_registry')

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
    ids = get_agency_ids(catalog, agency)
    if ids:
        id = ids.get('crossref')
        if id:
            url = f"https://api.crossref.org/funders/{id}"
            response = requests.get(url)
            return response.json()

def harvest_agency_isni(catalog, agency):
    # harvest the agency metadata from the ISNI registry
    # returns XML string
    ids = get_agency_ids(catalog, agency)
    if ids:
        id = ids.get('isni')
        if id:
            url = f"http://isni.oclc.org/sru/?query=pica.isn+%3D+%22{id}%22&operation=searchRetrieve&recordSchema=isni-b"
            response = requests.get(url)
            searchRetrieveResponse = etree.fromstring(response.content)
            isni = searchRetrieveResponse.find('.//ISNIAssigned')
            return isni

def harvest_agency_ror(catalog, agency):
    # harvest the agency metadata from the ROR registry
    # returns JSON string
    ids = get_agency_ids(catalog, agency)
    if ids:
        id = ids.get('ror')
        if id:
            url = 'http://api.ror.org/organizations/https://ror.org/'+id
            response = requests.get(url)
            return response.json()

def harvest_agency_wikidata(catalog, agency, format='rdf'):
    # harvest the agency metadata from Wikidata
    # returns JSON string
    ids = get_agency_ids(catalog, agency)
    if ids:
        id = ids.get('wikidata')
        if id:
            url = f"https://www.wikidata.org/wiki/Special:EntityData/{id}.{format}"
            if format == 'rdf':
                response = requests.get(url)
                isni_rdf = etree.fromstring(response.content)
                return isni_rdf
            elif format == 'json':
                response = requests.get(url)
                return response.json()
            else:
                logging.error(f"Unknow Wikidata format {format}")

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
    xml = etree.tostring(xml, encoding='unicode')
    with open(get_agency_isni_file(catalog, agency), 'w') as f:
        f.write(xml) 
    return

def save_agency_ror(catalog, agency, data):
    # save the ROR metadata
    with open(get_agency_ror_file(catalog, agency), 'w') as f:
        json.dump(data, f, indent=4)

def save_agency_wikidata(catalog, agency, data, format='rdf'):
    # save the Wikidata metadata
    with open(get_agency_wikidata_file(catalog, agency, format), 'w') as f:
        if format == 'rdf':
            xml = etree.tostring(data, encoding='unicode')
            f.write(xml) 
        elif format == 'json':
            json.dump(data, f, indent=4)

