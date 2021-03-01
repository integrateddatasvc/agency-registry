'''
Registry reporting utilities
'''

import argparse
import json
import jsonschema
import logging
import os
from registry import *
import yaml

def report_default(catalog, agency):
    report_ids(catalog, agency)
    report_services(catalog, agency)
    return

def report_ids(catalog, agency):
    data = get_agency_ids(catalog, agency)
    ids = []
    for key,value in data.items():
        ids.append(f"{key}={value}")
    print(f"ids({len(ids)}): "+' | '.join(ids))
    return

def report_services(catalog, agency, platform=None, protocol=None):
    data = get_agency_services(catalog, agency)
    service_stats = {}
    for key, value in data.items():
        service_key = f"{value.get('type')}/{value.get('protocol')}"
        if service_key in service_stats:
            service_stats[service_key] += 1
        else:
            service_stats[service_key] = 1
    services = []
    for service_key, service_count in service_stats.items():
        services.append(f"{service_key}[{service_count}]")
    print("services: "+' | '.join(sorted(services)))
    return

def validate(catalog, agency, schema):
    # load schema
    schema_data = get_schema(schema)
    # validate file if exists
    agency_file = os.path.join(get_agency_dir(catalog, agency), f"{schema}.yaml")
    if os.path.isfile(agency_file):
        agency_data = load_yaml(agency_file)
        try:
            validation = jsonschema.validate(agency_data, schema_data)
        except jsonschema.exceptions.ValidationError as e:
            print(f"{catalog}/{agency} {schema} ValidationError: {e.message}")
        except jsonschema.exceptions.SchemaError as e:
            print(f"{catalog}/{agency} {schema} SchemaError: {e.message}")
    return

def main():
    for catalog in sorted(os.listdir(get_registry_dir())):
        if args.catalogs and catalog not in args.catalogs:
            continue
        catalog_dir = get_catalog_dir(catalog)
        if not os.path.isdir(catalog_dir):
            continue
        for agency in sorted(os.listdir(catalog_dir)):
            if args.agencies and agency not in args.agencies:
                continue
            if not args.reports:
                print("-"*20)
                print(agency)
                report_default(catalog,agency)
            if "validate" in args.reports:
                validate(catalog, agency, 'ids')
                validate(catalog, agency, 'geo')
                validate(catalog, agency, 'social')
                validate(catalog, agency, 'services')
    return

if __name__ ==  "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    registry_dir = os.path.abspath(script_dir+"/../registry")
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--agencies", nargs="*", help="Agencies to include")
    parser.add_argument("-c","--catalogs", nargs="*", help="Catalogs to include")
    parser.add_argument("-r","--reports", nargs="*", help="Reports to run")
    parser.add_argument("-ll","--loglevel", help="Python logging level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    if args.loglevel:
        logging.getLogger().setLevel(args.loglevel.upper())

    logging.info(args)
    main()

