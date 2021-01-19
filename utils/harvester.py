import argparse
import json
import requests
import os
import yaml


def get_registry_root():
    global args
    return args.registry_root

def get_targets():
    global args
    return args.targets

def get_agency_ids(agency):
    with open(os.path.join(get_agency_dir(agency),'ids.yaml')) as f:
        data = yaml.load(f, Loader=yaml.FullLoader) 
        return data

def get_agency_dir(agency):
    return os.path.join(get_registry_root(),agency)

def harvest_ror(agency):
    ror_id = get_agency_ids(agency).get('ror')
    url = 'http://api.ror.org/organizations/https://ror.org/'+ror_id
    r = requests.get(url)
    return r.json()

def process_agency(agency):
    print("Processing "+agency)
    agency_dir = get_agency_dir(agency)
    ror_file = os.path.join(agency_dir,'ror.json')
    if not os.path.isfile(ror_file):
        data = harvest_ror(agency)
        with open(ror_file, 'w') as f:
            json.dump(data, f, indent=4)
    return

def process_target(target):
    if "*":
        groups = [f.path for f in os.scandir(get_registry_root()) if f.is_dir()]
        for group in groups:
            agencies =  [f.path for f in os.scandir(group) if f.is_dir()]
            for agency in agencies:
                process_agency(agency)
    else:
        process_agency(target)
    return

def main():
    for target in get_targets():
        process_target(target)
    return

if __name__ ==  "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    registry_dir = os.path.abspath(script_dir+"/../registry")
    parser = argparse.ArgumentParser()
    parser.add_argument("targets",nargs='+', help="The agency names to harvest (use * for all)")
    parser.add_argument("-r", "--registry", help="The registry or source to harvest")
    parser.add_argument("--registry-root", help="The root diretcoty of the registry", default=registry_dir)
    args = parser.parse_args()
    print(args)
    main()

