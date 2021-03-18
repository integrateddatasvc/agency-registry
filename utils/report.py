'''
Registry reporting utilities
'''

import argparse
import json
import jsonschema
import logging
import os
from registry import *
import requests
import yaml


def ckan(catalog, agency):
    services = get_agency_services(catalog, agency)
    catalogs = services.get('catalogs')
    if catalogs:
        for entry in catalogs:
            if entry.get('platform') == 'ckan':
                catalog_url = entry.get('endpoint')
                api_endpoint = entry.get('api_endpoint')
                if api_endpoint:
                    api_url = api_endpoint
                else:
                    api_url = f"{entry.get('endpoint')}/api"
                # get package count (using v1)
                package_count = None
                url = f"{api_url}/search/package?limit=0"
                result = requests.get(url)
                if result.status_code == 200:
                    json = result.json()
                    package_count = json.get('count')
                # get resources count 9using v1)
                resource_count = None
                url = f"{api_url}/search/resource?limit=0"
                result = requests.get(url)
                if result.status_code == 200:
                    json = result.json()
                    package_count = json.get('count')
                # DCAT
                resource_count = None
                url = f"{catalog_url}/catalog.jsonld"
                result = requests.get(url)
                if result.status_code == 200:
                    json = result.json()
                    is_dcat_catalog_found = True
                else:
                    is_dcat_catalog_found = False

                # report
                print("-"*20)
                print(f"{catalog}/{agency} | {entry.get('name')}")
                print(f"{catalog}/{agency} | {catalog_url}")
                print(f"{catalog}/{agency} | {api_url}")
                print(f"{catalog}/{agency} | packages: {package_count} | resources: {resource_count} | DCAT Catalog: {is_dcat_catalog_found}")
    return

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
    for (type, services) in data.items():
        for service in services:
            service_key = f"{type}/{service.get('client')}"
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

            if "default" in args.reports:
                print("-"*20)
                print(agency)
                report_default(catalog,agency)
            if "ckan" in args.reports:
                ckan(catalog, agency)
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
    parser.add_argument("-r","--reports", nargs="*", help="Reports to run: default | ckan | validation)", default='default')
    parser.add_argument("-ll","--loglevel", help="Python logging level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    if args.loglevel:
        logging.getLogger().setLevel(args.loglevel.upper())

    logging.info(args)
    main()

