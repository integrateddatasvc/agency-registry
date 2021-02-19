
'''
Registry reporting utilities
'''

import argparse
import logging
import os
from registry import *

def report_default(catalog, agency):
    agency_dir = os.path.join(get_registry_root(),catalog,agency)
    if os.path.isfile('identifiers.yaml'):
        with open(get_agency_ids_file(agency)) as f:
            ids = yaml.load(f, Loader=yaml.FullLoader)
            for id in data:

    return

def main():
    for catalog in sorted(os.listdir(get_registry_root())):
        if args.catalogs and catalog not in args.catalogs:
            continue
        catalog_dir = os.path.join(get_registry_root(), catalog)
        print(catalog)
        for agency in sorted(os.listdir(catalog_dir)):
            if args.agencies and agency not in args.agencies:
                continue
            print(agency)
            if "default" in reports:
                report_default
    return

if __name__ ==  "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    registry_dir = os.path.abspath(script_dir+"/../registry")
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--agencies", nargs="*", help="Agencies to include")
    parser.add_argument("-c","--catalogs", nargs="*", help="Catalogs to include")
    parser.add_argument("-r","--reports", nargs="*", help="Reports to run", default="default")
    parser.add_argument("-ll","--loglevel", help="Python logging level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    if args.loglevel:
        logging.getLogger().setLevel(args.loglevel.upper())

    logging.info(args)
    main()

