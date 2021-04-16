'''
Utility to retrieve/harvest DCAT content from catalog services identified in the registry
'''

import argparse
from registry import *
import requests

def parse_paged_collection(resource):
    print(resource)
    return

def harvest(catalog, agency):    
    services = get_agency_services(catalog, agency)
    print(services)
    if services:
        catalogs = services.get('catalogs')
        if catalogs:
            for entry in catalogs:
                if entry.get('platform') == 'ckan':
                    url = f"{entry.get('endpoint')}/catalog.jsonld"
                    print(url)
                    result = requests.get(url)
                    if result.status_code == 200:
                        counts = {}
                        json = result.json()
                        print(f"{len(json)}")
                        for resource in json:
                            resource_types = resource.get('@type')
                            resource_type = resource_types[0]
                            if 'http://www.w3.org/ns/hydra/core#PagedCollection' in resource_types:
                                parse_paged_collection(resource)
                            if resource_type not in counts:
                                counts[resource_type] = 0
                            counts[resource_type] += 1
                        for resource_type, count in counts.items():
                            print(f"{resource_type} {count}")
                            
                    else:
                        print("DCAT catalog not found")

if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", help="Catalog")
    parser.add_argument("agency", help="Agency")
    parser.add_argument("-o","--output", help="Output directory", default=".")
    args = parser.parse_args()

    harvest(args.catalog, args.agency)


