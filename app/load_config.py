import os
import json
from json import JSONEncoder
import mysql.connector

#load the configurations from json file
def load_cfg(path):
    jsonres = {}
    try:
        with open(os.path.abspath(os.path.realpath(path)), 'r') as f:
            jsonres = json.load(f)
    except Exception as e:
        print("Exception: ", e)
    return jsonres
    
def db_cursor():
    main_cfg = load_cfg('./main_cfg.json')
    
      db = mysql.connector.connect (
        host=main_cfg['dbHost'],
        port=main_cfg['port'],
        user=main_cfg['sqlUser'],
        password=main_cfg['sqlPass'],
        database=main_cfg['db']
      )
      
      mycursor = db.cursor()
    
    return mycursor
