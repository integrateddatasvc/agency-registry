
'''
Registry reporting utilities
'''

import argparse
import logging
import os
from registry import *
import yaml

def report_default(catalog, agency):
    ids_file = get_agency_ids_file(catalog, agency)
    if os.path.isfile(ids_file):
        with open(ids_file) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            ids = []
            for key,value in data.items():
                ids.append(f"{key}={value}")
            print(f"ids({len(ids)}): "+' | '.join(ids))
    return

def main():
    for catalog in sorted(os.listdir(get_registry_dir())):
        if args.catalogs and catalog not in args.catalogs:
            continue
        catalog_dir = get_catalog_dir(catalog)
        print("="*20)
        print(catalog)
        for agency in sorted(os.listdir(catalog_dir)):
            if args.agencies and agency not in args.agencies:
                continue
            print("-"*20)
            print(agency)
            if not args.reports:
                report_default(catalog,agency)
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

