"""
Agency Registry Elasticsearch integration

References
- https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-request-signing.html#es-request-signing-python
- https://elasticsearch-py.readthedocs.io/en/v7.13.4/
"""
import argparse
from elasticsearch import Elasticsearch
import logging
import os
from registry import *

def main():
    global args
    es = Elasticsearch([args.host], http_auth=(args.user, args.password))
    es.indices.delete('agency-registry')
    return
    es.indices.create('agency-registry')
    es.indices.put_settings('{"index.mapping.total_fields.limit": 5000}','agency-registry')
    catalogs = [f.path for f in os.scandir(get_registry_dir()) if f.is_dir()]
    count = 0
    for catalog_dir in catalogs:
        agencies =  [f.path for f in os.scandir(catalog_dir) if f.is_dir()]
        for agency_dir in agencies:
            count += 1
            catalog = os.path.basename(catalog_dir)
            agency = os.path.basename(agency_dir)
            wikidata_id = get_agency_id(catalog, agency, 'wikidata')
            if wikidata_id:
                logging.info(f"{catalog}/{agency} {wikidata_id}")
                metadata = get_agency_json(catalog, agency)
                metadata['external']['wikidata'].pop('claims')
                es.index(args.index, metadata, id=wikidata_id)

if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-root", help="The root diretcoty of the registry", default=get_registry_dir())
    parser.add_argument("-ll","--loglevel", help="Python logging level", default="INFO")
    parser.add_argument("--host", help="Elasticsearch endpoint", default="https://search-idms-dev-7yfr5utei6g2km5xes7ntph5pa.us-east-1.es.amazonaws.com")
    parser.add_argument("--user", help="Elasticsearch user")
    parser.add_argument("--password", help="Elasticsearch password")
    parser.add_argument("--index", help="Elasticsearch index", default="agency-registry")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    if args.loglevel:
        logging.getLogger().setLevel(args.loglevel.upper())

    logging.info(args)
    main()



