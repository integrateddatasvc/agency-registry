import argparse
import os
import re
import xml.etree.ElementTree as ET

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
    path = os.path.join(registry_dir,f"{group}/{id}")
    if not os.path.exists(path):
        print(f"Init {path}")
        os.makedirs(path)
    return

def init_ror(group,id,organization):
    return
#
# MAIN
#
def main():
    global args
    omad = get_xml(args.file)
    for action in args.actions:
        if action == "init":
            for organization in omad.findall("omad:Organization",NS):
                omad_id = organization.get("id")
                if args.tag and args.tag not in get_organization_tags(organization):
                    continue
                (group,id) = get_organization_group_and_id(organization)
                if group and id:
                    init_organization(group,id,organization)
                else:
                    print(f"SKIPPED {omad_id}: no group/id")
        else:
            print(f"ERROR: unknown command {action}")
    return

if __name__ ==  "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    registry_dir = os.path.abspath(script_dir+"/../registry")
    omad_dir = os.path.abspath(script_dir+"/../omad")

    parser = argparse.ArgumentParser()
    parser.add_argument("actions",nargs='+', help="actions")
    parser.add_argument("-f", "--file", default="omad.xml", help="OMAD file (default )")
    parser.add_argument("-t", "--tag", help="Filter by tag")
    args = parser.parse_args()

    main()

