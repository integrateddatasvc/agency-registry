'''
Utility functions for the agency-registry
'''

import os
import json
import yaml

def get_catalog_dir(catalog):
    return os.path.join(get_registry_dir(), catalog)

def get_agency_dir(catalog, agency):
    return os.path.join(get_registry_dir(), catalog, agency)

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
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__))+'/../_registry')

def get_schema(schema):
    schema_file = get_schema_file(schema, format='yaml')
    return load_yaml(schema_file)

def get_schema_file(schema, format='yaml'):
    return os.path.join(get_schemas_dir(),f"{schema}.{format}")

def get_schemas_dir():
    return os.path.join(get_script_dir(),'../schemas')

def get_script_dir():
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def load_yaml(file):
    if os.path.isfile(file):
        with open(file) as f:
            data = yaml.load(f, Loader=yaml.FullLoader) 
            return data
    return {}