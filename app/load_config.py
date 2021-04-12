import os
import json
from json import JSONEncoder

#load the configurations from json file
def load_cfg(path):
    jsonres = {}
    try:
        with open(os.path.abspath(os.path.realpath(path)), 'r') as f:
            jsonres = json.load(f)
    except Exception as e:
        print("Exception: ", e)
    return jsonres