"""
Agency Registry DynamoDB integration

References

"""
import argparse
import boto3
from boto3.dynamodb.conditions import *
from decimal import Decimal
import logging
import os
from registry import *

def get_table():
    global args
    session = boto3.Session(profile_name='idms')
    dynamodb = session.resource('dynamodb',region_name='us-east-1')
    table = dynamodb.Table(args.table)
    return table

def reload():
    global args
    # iterate catalogs
    table = get_table()
    catalogs = [f.path for f in os.scandir(get_registry_dir()) if f.is_dir()]
    count = 0
    for catalog_dir in catalogs:
        agencies =  [f.path for f in os.scandir(catalog_dir) if f.is_dir()]
        # iterate agencies
        for agency_dir in agencies:
            count += 1
            catalog = os.path.basename(catalog_dir)
            agency = os.path.basename(agency_dir)
            wikidata_id = get_agency_id(catalog, agency, 'wikidata')
            if wikidata_id:
                logging.info(f"{catalog}/{agency} {wikidata_id}")
                metadata = get_agency_json(catalog, agency)
                metadata['id']=wikidata_id
                metadata2 = json.loads(json.dumps(metadata), parse_float=Decimal)
                # put in DB
                table.put_item(TableName='agency-registry', Item=metadata2)

def scan():
    table = get_table()
    # prepare
    scan_kwargs = {
        'ProjectionExpression': "id, ids",
    }
    filter = Attr('ids.wikidata').eq('Q5938294')
    filter = Attr('ids.isni').exists()
    print(filter)
    if len(args.params) > 0:
        scan_kwargs['FilterExpression'] = filter
    # scan
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        print(response.get('Items', []))
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None    
    return

def main():
    global args
    command = args.command.lower()
    if  command == 'reload':
        reload()
    elif command == 'scan':
        scan()
    return


if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("params",nargs='*')
    parser.add_argument("--registry-root", help="The root diretcoty of the registry", default=get_registry_dir())
    parser.add_argument("-ll","--loglevel", help="Python logging level", default="INFO")
    parser.add_argument("-t","--table", help="DynamoDB Table", default="agency-registry")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    if args.loglevel:
        logging.getLogger().setLevel(args.loglevel.upper())

    logging.info(args)
    main()



