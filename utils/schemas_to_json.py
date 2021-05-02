'''
Utility that converts the YAML schemas to JSON
'''

import os.path
import json
from registry import *
import yaml

if __name__ ==  "__main__":
    schemas_dir = get_schemas_dir()
    for filename in os.listdir(schemas_dir):
        if filename.endswith(".yaml"):
            data = load_yaml(os.path.join(schemas_dir, filename))
            json_filename = os.path.join(schemas_dir, filename.replace('.yaml','.json'))
            with open(json_filename, 'w') as outfile:
                json.dump(data, outfile, indent=4)            
        else:
            continue    
