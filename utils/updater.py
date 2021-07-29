import argparse
import logging
import json
from registry import *
import requests
import os
from xml.etree import ElementTree
import yaml


#
# Markdown files for jekyll
#
def generate_jekyll_markdown(catalog, agency):
    collection_agency_dir = os.path.join(get_collections_dir(),catalog,agency)
    if not os.path.isdir(collection_agency_dir):
        os.makedirs(collection_agency_dir)
    md_file_path = os.path.join(collection_agency_dir,'html.md')
    with open(md_file_path, 'wt') as md_file:
        metadata = get_agency_json(catalog, agency)
        md_file.write("---\n")
        name = agency
        if metadata['external'].get('ror'):
            name = metadata['external']['ror']['name']
        md_file.write(f"name: {name}\n")
        # write
        md_file.write(yaml.dump(metadata))
        md_file.write("---\n")
    return
#
# ENVIRONMENT
#
def get_targets():
    # returns the list of targets to process
    global args
    return args.targets

#
# AGENCY
#
def add_agency_ids_from_ror(catalog, agency):
    # Adds the ROR external identifiers to the agency ids if missing
    logging.debug(f"add_agency_ids_from_ror({agency})")
    agency_ids = get_agency_ids(catalog, agency)
    ror = get_agency_ror(catalog, agency)
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


def reset_agency(catalog, agency):
    # USE WITH CARE!
    # removes harvested/generated metadata from an agency
    logging.info(f"Resetting agency {catalog}/{agency}")
    delete_agency_crossref_file(catalog, agency)
    delete_agency_isni_file(catalog, agency)
    delete_agency_ror_file(catalog, agency)
    return

def save_agency_ids(catalog, agency, data):
    with open(get_agency_ids_file(catalog, agency), 'w') as f:
        yaml.dump(data, f)
#
# PROCESSING
#
def process_agency(catalog, agency):
    logging.info("Processing "+agency)
    agency_dir = get_agency_dir(catalog, agency)
    # reset
    if args.reset:
        reset_agency(catalog, agency)
    # Wikidata
    wikidata_file = get_agency_wikidata_file(catalog, agency)
    if not os.path.isfile(wikidata_file):
        # RDF
        data = harvest_agency_wikidata(catalog, agency, format='rdf')
        if data is not None:
            save_agency_wikidata(catalog, agency, data, format='rdf')
            #ids = add_agency_ids_from_ror(catalog, agency)
            #logging.debug(ids)
            #save_agency_ids(catalog, agency, ids)
        # JSON
        data = harvest_agency_wikidata(catalog, agency, format='json')
        if data is not None:
            save_agency_wikidata(catalog, agency, data, format='json')
    # ROR
    ror_file = get_agency_ror_file(catalog, agency)
    if not os.path.isfile(ror_file):
        data = harvest_agency_ror(catalog, agency)
        if (data):
            save_agency_ror(catalog, agency, data)
            ids = add_agency_ids_from_ror(catalog, agency)
            logging.debug(ids)
            save_agency_ids(catalog, agency, ids)
    # Crossref
    crossref_file = get_agency_crossref_file(catalog, agency)
    if not os.path.isfile(crossref_file):
        data = harvest_agency_crossref(catalog, agency)
        if (data):
            save_agency_crossref(catalog, agency, data)
    # ISNI
    isni_file = get_agency_isni_file(catalog, agency)
    if not os.path.isfile(isni_file):
        data = harvest_agency_isni(catalog, agency)
        if data:
            save_agency_isni(catalog, agency, data)
    # markdown
    generate_jekyll_markdown(catalog, agency)
    return

def process_target(target):
    if target == 'ALL':
        catalogs = [f.path for f in os.scandir(get_registry_dir()) if f.is_dir()]
        for catalog in catalogs:
            agencies =  [f.path for f in os.scandir(catalog) if f.is_dir()]
            for agency in agencies:
                process_agency(os.path.basename(catalog), os.path.basename(agency))
    else:
        if "/" in target:
            (catalog,agency) = target.split('/',2)
            process_agency(catalog, agency)
        else:
            catalog = target
            agencies =  [f.path for f in os.scandir(get_catalog_dir(catalog)) if f.is_dir()]
            for agency in agencies:
                process_agency(catalog, os.path.basename(agency))
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

