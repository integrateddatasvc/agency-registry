import argparse
import logging
import os
from registry import *

def main():
    all = []
    catalogs = [f.path for f in os.scandir(get_registry_dir()) if f.is_dir()]
    for catalog_dir in catalogs:
        agencies =  [f.path for f in os.scandir(catalog_dir) if f.is_dir()]
        for agency_dir in agencies:
            catalog = os.path.basename(catalog_dir)
            agency = os.path.basename(agency_dir)
            logging.info(f"{catalog}/{agency}")
            metadata = get_agency_json(catalog, agency)
            all.append(metadata)
    filename = os.path.join(get_registry_dir(),'all.json')
    with open(filename,'w') as f:
        json.dump(all,f,indent=4)

if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-root", help="The root diretcoty of the registry", default=get_registry_dir())
    parser.add_argument("-ll","--loglevel", help="Python logging level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    if args.loglevel:
        logging.getLogger().setLevel(args.loglevel.upper())

    logging.info(args)
    main()



