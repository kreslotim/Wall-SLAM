from flask import render_template, jsonify,request
from app.main import bp
from datetime import datetime, timedelta
import time
import random
from .esp32Connection import ESP32Connection

ip="168.20.13.1"
startTime= time.time()

host = '192.168.28.79'
recv_port = 8090
send_port = 8091
esp = ESP32Connection(send_port,recv_port)

@bp.route('/')
def index():
    # Make connection to ESP here

    #Dummy data
    connected = True
    

    return render_template('index.html', ip=ip)

@bp.route('/run-python-function', methods=['POST'])
def run_python_function():
    # Get the value of the slider from the AJAX request
    slider_value = request.form.get('value')

    # Call your Python function here, passing the slider value as a parameter
    result = my_python_function(slider_value)
    return jsonify(result=result)


@bp.route('/reset-connection', methods=['POST'])
def init_connection():
    result = reset_esp_connection()
    return jsonify(result=result)


def reset_esp_connection():
    print("RESETTTT")

def my_python_function(slider):  
    print("hello from web")
    print(slider)
   

@bp.route('/get-graph-data', methods=['POST'])
def get_graph_data():
    esp.send_hello()
    
    x_sent = [row[1] for row in esp.send_stat]
    x_received = [row[1] for row in esp.recv_stat]
    y_sent = [row[0] for row in esp.send_stat]
    y_received = [row[0] for row in esp.recv_stat]
    print(x_sent)
    #
    #for i in range(10):
    #    x_sent.append(time.time()-startTime)
    #    y_sent.append(random.randint(0, 10))
    #    x_received.append(time.time()-startTime)
    #    y_received.append(random.randint(0, 10))
  
    return jsonify(x_sent=x_sent, y_sent=y_sent, x_received=x_received,y_received=y_received)