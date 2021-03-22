import argparse
import logging
import json
from registry import *
import requests
import os
from xml.etree import ElementTree
import yaml

#
# ENVIRONMENT
#
def get_registry_root():
    # returns the registry root directory
    global args
    return args.registry_root

def get_targets():
    # returns the list of targets to process
    global args
    return args.targets

#
# AGENCY
#
def get_agency_ids(agency):
    # returns the agency known identifiers as key/value or key/array pairs
    if os.path.isfile(get_agency_ids_file(agency)):
        with open(get_agency_ids_file(agency)) as f:
            data = yaml.load(f, Loader=yaml.FullLoader) 
            return data
    else:
        return {}

def get_agency_ids_file(agency):
    file = os.path.join(get_agency_dir(agency),'ids.yaml')
    return file

def get_agency_dir(agency):
    # returns the agency's directory
    return os.path.join(get_registry_root(),agency)

def get_agency_external_dir(agency):
    # returns the agency's external data directory
    dir = os.path.join(get_agency_dir(agency),'external')
    if not os.path.isdir(dir):
        os.mkdir(dir)
    return dir

def reset_agency(agency):
    # USE WITH CARE!
    # removes harvested/generated metadata from an agency
    logging.info(f"Resetting agency {agency}")
    try:
        os.remove(get_ror_file(agency))
    except OSError:
        pass
    try:
        os.remove(get_isni_file(agency))
    except OSError:
        pass
    return

def save_agency_ids(agency, data):
    with open(get_agency_ids_file(agency), 'w') as f:
        yaml.dump(data, f)

#
# CrossRef
#

def delete_crossref(agency):
    file = get_crossref_file()
    if os.path.isfile(ror_file):
        logging.info(f"Deleting CrossRef file {file}")
        try:
            os.remove(ror_file)
        except OSError:
            pass    

def get_crossref(agency):
    file = get_crossref_file(agency)
    if not os.path.isfile(file):
        harvest_crossref(agency)
    with open(file, 'r') as f:
        data = json.load(f)
        return data

def get_crossref_file(agency):
    file = os.path.join(get_agency_external_dir(agency),'crossref.json')
    return file

def harvest_crossref(agency):
    # harvest the agency metadata from the CrossRef registry
    # returns JSON string
    id = get_agency_ids(agency).get('crossref')
    if id:
        url = f"https://api.crossref.org/funders/{id}"
        response = requests.get(url)
        return response.json()

def save_crossref(agency, data):
    # save the CrossRef metadata
    with open(get_crossref_file(agency), 'w') as f:
        json.dump(data, f, indent=4)

#
# ISNI REGISTRY
#

def get_isni_file(agency):
    file = os.path.join(get_agency_external_dir(agency),'isni.xml')
    return file

def harvest_isni(agency):
    # harvest the agency metadata from the ISNI registry
    # returns XML string
    id = get_agency_ids(agency).get('isni')
    if id:
        print(f"ISNI:{id}")
        url = f"http://isni.oclc.org/sru/?query=pica.isn+%3D+%22{id}%22&operation=searchRetrieve&recordSchema=isni-b"
        print(f"ISNI url {url}")
        response = requests.get(url)
        searchRetrieveResponse = ElementTree.fromstring(response.content)
        isni = searchRetrieveResponse.find('.//ISNIAssigned')
        return isni

def save_isni(agency, xml):
    # save the ISNI metadata
    xml = ElementTree.tostring(xml, encoding='utf8')
    with open(get_isni_file(agency), 'wb') as f:
        f.write(xml) 
    return

#
# ROR REGISTRY
#
def add_agency_ids_from_ror(agency):
    # Adds the ROR external identifiers to the agency ids if missing
    logging.debug(f"add_agency_ids_from_ror({agency})")
    agency_ids = get_agency_ids(agency)
    ror = get_ror(agency)
    ror_external_ids = ror.get("external_ids")
    for (external_id_key, external_id_value) in ror_external_ids.items():
        logging.debug(external_id_key)
        agency_id_key = external_id_key.lower()
        if not agency_ids.get(agency_id_key): # add ID only if missing
            id = external_id_value.get("preferred")
            if not id:
                id = external_id_value.get("all")[0]
                id = id.strip().replace(" ","") # remove white space
                logging.debug(f"Adding {external_id_key} {id} to {agency}")
            agency_ids[agency_id_key]=id
    return agency_ids

def delete_ror(agency):
    ror_file = get_ror_file()
    if os.path.isfile(ror_file):
        logging.info(f"Deleting ROR file {ror_file}")
        try:
            os.remove(ror_file)
        except OSError:
            pass    

def get_ror(agency):
    ror_file = get_ror_file(agency)
    if not os.path.isfile(ror_file):
        harvest_ror(agency)
    with open(ror_file, 'r') as f:
        data = json.load(f)
        return data

def get_ror_file(agency):
    ror_file = os.path.join(get_agency_external_dir(agency),'ror.json')
    return ror_file

def harvest_ror(agency):
    # harvest the agency metadata from the ROR registry
    # returns JSON string
    ror_id = get_agency_ids(agency).get('ror')
    if ror_id:
        url = 'http://api.ror.org/organizations/https://ror.org/'+ror_id
        response = requests.get(url)
        return response.json()

def save_ror(agency, data):
    # save the ROR metadata
    with open(get_ror_file(agency), 'w') as f:
        json.dump(data, f, indent=4)

#
# PROCESSING
#
def process_agency(agency):
    logging.info("Processing "+agency)
    agency_dir = get_agency_dir(agency)
    # reset
    if args.reset:
        reset_agency(agency)
    # ROR (must be first as it adds identifers)
    ror_file = get_ror_file(agency)
    if not os.path.isfile(ror_file):
        data = harvest_ror(agency)
        if (data):
            save_ror(agency, data)
            ids = add_agency_ids_from_ror(agency)
            logging.debug(ids)
            save_agency_ids(agency, ids)
    # Crossref
    crossref_file = get_crossref_file(agency)
    if not os.path.isfile(crossref_file):
        data = harvest_crossref(agency)
        if (data):
            save_crossref(agency, data)
    # ISNI
    isni_file = get_isni_file(agency)
    if not os.path.isfile(isni_file):
        data = harvest_isni(agency)
        if data:
            save_isni(agency, data)
    return

def process_target(target):
    if target == 'ALL':
        groups = [f.path for f in os.scandir(get_registry_root()) if f.is_dir()]
        for group in groups:
            agencies =  [f.path for f in os.scandir(group) if f.is_dir()]
            for agency in agencies:
                process_agency(agency)
    else:
        process_agency(target)
    return

#
# MAIN
#
def main():
    for target in get_targets():
        process_target(target)
    return

if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("targets",nargs='+', help="The agency names to harvest or ALL")
    parser.add_argument("-r", "--registry", help="The registry or source to harvest")
    parser.add_argument("--registry-root", help="The root diretcoty of the registry", default=get_registry_dir())
    parser.add_argument("-ll","--loglevel", help="Python logging level", default="INFO")
    parser.add_argument("--reset", action='store_true', help="Reset agency metadata (USE WITH CARE)")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    if args.loglevel:
        logging.getLogger().setLevel(args.loglevel.upper())

    logging.info(args)
    main()

