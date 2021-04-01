from flask import Flask, render_template, request, make_response, jsonify
import json
from json import JSONEncoder

keylog = []

#start flask app
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/something', methods=['POST'])
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


if __name__ == "__main__":
  app.run()
