import argparse
import json
import os
import re
from registry import *
import requests
import xml.etree.ElementTree as ET
import xmltodict
import yaml

NS = {'omad':'openmetadata:omad:1_0'}

def get_xml(file):
    global omad_dir
    tree = ET.parse(os.path.join(omad_dir,"xml",file))
    root = tree.getroot()
    return root

def get_organization_group_and_id(organization):
    # generates the registry group/id for this organization
    omad_id = organization.get("id")
    group = None
    id = None
    if 'NSO' in get_organization_tags(organization):
        m = re.match("(..)-(.*)", omad_id)
        if m:
            #print(f"{omad_id} | {m.group(1)} | {m.group(2)}")
            group = m.group(1)
            id = group+"-nso-"+m.group(2)
    elif 'FedStats' in get_organization_tags(organization):
        m = re.match("(..)-(.*)", omad_id)
        if m:
            #print(f"{omad_id} | {m.group(1)} | {m.group(2)}")
            group = m.group(1)
            if group == "us":
                id = group+"-gov-"+m.group(2)
    if group and id:
        return (group,id)
    else:
        return (None,None)

def get_organization_tags(organization):
    # returns the organization's Tags as an array
    tags = []
    xml_tags = organization.find("omad:Tags",NS)
    if xml_tags:
        for tag in xml_tags.findall("omad:Tag",NS):
            tags.append(tag.text)
    return tags

def init_organization(group,id,organization):
    organization_dir = os.path.join(get_registry_dir(),f"{group}/{id}")
    if not os.path.exists(organization_dir):
        print(f"Init {organization_dir}")
        os.makedirs(organization_dir)
    omad_file = os.path.join(organization_dir,'omad.json')
    if not os.path.isfile(omad_file):
        omad_dict = xmltodict.parse(ET.tostring(organization), process_namespaces=True, namespaces={'openmetadata:omad:1_0':None,'http://www.w3.org/XML/1998/namespace':None})
        with open(omad_file, 'w') as outfile:
            json.dump(omad_dict,outfile, indent=4)
    standards_file = os.path.join(organization_dir,'standards.json')
    if not os.path.isfile(standards_file):
        pass
    return

def init_ror(group,id,organization):
    # ROR ID lookup
    # http://api.ror.org/organizations?filter=types:Government,country.country_code:US&query=%22census%20bureau%22
    print("-"*20)
    name = organization.find("omad:Name",NS).text
    print(f"{group} {id} {name}")
    country_code = group.upper()
    url = f"http://api.ror.org/organizations?filter=types:Government,country.country_code:{country_code}&query=%22{name}%22"
    print(f"{url}")
    # check current ids
    ids = None
    organization_dir = os.path.join(get_registry_dir(),group,id)
    ids_file = os.path.join(organization_dir,'ids.yaml')
    if os.path.isfile(ids_file):
        with open(ids_file) as f:
            ids = yaml.load(f, Loader=yaml.FullLoader) 
            if ids and "ror" in ids:
                print("ROR id already set")
                return
    # lookup 
    response = requests.get(url)
    ror_json = response.json()
    ror_results_count = ror_json['number_of_results']
    if ror_results_count == 1:
        print("Unique match found")
        # save id
        if not ids:
            ids = {}
        ror_id = ror_json['items'][0]['id'][16:]
        ids['ror']=ror_id
        with open(ids_file, 'w') as f:
            yaml.dump(ids, f)
            print("ROR id set")
    elif ror_results_count > 1:
        print(f"Too many matches ({ror_results_count})")
    else:
        print("No match found")
    return
#
# MAIN
#
def main():
    global args
    omad = get_xml(args.file)
    for action in args.actions:
        count = 0
        for organization in omad.findall("omad:Organization",NS):
            count += 1
            omad_id = organization.get("id")
            if args.tag and args.tag not in get_organization_tags(organization):
                continue
            (group,id) = get_organization_group_and_id(organization)
            if group and id:
                if action == "init":
                    init_organization(group,id,organization)
                elif action == "ror":
                    init_ror(group,id,organization)
                else:
                    print(f"ERROR: unknown command {action}")
                    break
            else:
                print(f"SKIPPED {omad_id}: no group/id")
    return

if __name__ ==  "__main__":
    omad_dir = os.path.abspath(get_script_dir()+"/../omad")

    parser = argparse.ArgumentParser()
    parser.add_argument("actions",nargs='+', help="actions")
    parser.add_argument("-f", "--file", default="omad.xml", help="OMAD file (default )")
    parser.add_argument("-t", "--tag", help="Filter by tag")
    args = parser.parse_args()

    main()

