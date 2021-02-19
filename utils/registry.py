import os

def get_registry_dir():
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__))+'/../registry')

def get_catalog_dir(catalog):
    return os.path.join(get_registry_dir(), catalog)

def get_agency_dir(catalog, agency):
    return os.path.join(get_registry_dir(), catalog, agency)

def get_agency_ids(catalog, agency):
    # returns the agency known identifiers as key/value or key/array pairs
    if os.path.isfile(get_agency_ids_file(catalog, agency)):
        with open(get_agency_ids_file(agency)) as f:
            data = yaml.load(f, Loader=yaml.FullLoader) 
            return data
    else:
        return {}

def get_agency_ids_file(catalog, agency):
    file = os.path.join(get_agency_dir(catalog, agency),'ids.yaml')
    return file