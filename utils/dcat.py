'''
Utility to retrieve/harvest DCAT content from catalog services identified in the registry
'''

import argparse
from registry import *
import requests


def harvest(catalog, agency): 
    services = get_agency_services(catalog, agency)
    if services:
        catalogs = services.get('catalogs')
        if catalogs:
            for entry in catalogs:
                if entry.get('platform') == 'ckan':
                    print(entry)

if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", help="Catalog")
    parser.add_argument("agency", help="Agency")
    parser.add_argument("-o","--output", help="Output directory", default=".")
    args = parser.parse_args()

    harvest(args.catalog, args.agency)


