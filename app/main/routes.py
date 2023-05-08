
from flask import render_template, jsonify,request
from app.main import bp
from datetime import datetime, timedelta
import time
import random
import app.models.dummyData as dummy
import app.models.esp32Connection as esp

ip="168.20.13.1"
startTime= time.time()

 # IP address and port number of the ESP32
data = dummy.dummyData()

 




@bp.route('/')
def index():
    # Make connection to ESP here

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
    print("RESETTTT")
    return jsonify(result=result)

@bp.route('/move-forward', methods=['POST'])
def init_connection():
    result = reset_esp_connection()
    return jsonify(result=result)

@bp.route('/move-backward', methods=['POST'])
def init_connection():
    result = reset_esp_connection()
    return jsonify(result=result)

@bp.route('/move-left', methods=['POST'])
def init_connection():
    result = reset_esp_connection()
    return jsonify(result=result)

@bp.route('/move-right', methods=['POST'])
def init_connection():
    result = reset_esp_connection()
    return jsonify(result=result)

@bp.route('/move-stop', methods=['POST'])
def init_connection():
    result = reset_esp_connection()
    return jsonify(result=result)


def reset_esp_connection():
    print("RESETTTT")

def my_python_function(slider):  
    print("hello from web")
    print(slider)
   

@bp.route('/get-graph-data-com', methods=['POST'])
def get_graph_data_com():
    x_sent =[]
    x_received = []
    y_sent = []
    y_received =[]

    for i in range(10):
        x_sent.append(time.time()-startTime)
        x_received.append(time.time()-startTime)
        y_sent.append(2)
        y_received.append( 2)
        time.sleep(0.2)

   
    return jsonify(x_sent=x_sent, y_sent=y_sent, x_received=x_received,y_received=y_received)

@bp.route('/get-graph-data-obstacle', methods=['POST'])
def get_graph_data_obstacle():
    obstacles = []
    car_position = (random.uniform(-15, 15), random.uniform(-15, 15))
    distance = random.uniform(0,3)
    for i in range(4):
        x = random.uniform(car_position[0]-distance, car_position[0]+distance)
        y = random.uniform(car_position[1]-distance, car_position[1]+distance)
        radius = random.uniform(0.3, 1)
        obstacles.append((x, y, radius))

    data = {'obstacles': obstacles, 'carPosition': car_position}
    return jsonify(data)

