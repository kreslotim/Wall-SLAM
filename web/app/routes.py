
from flask import render_template, jsonify, request
from flask import Blueprint
import time
import random


from app.models.dummyData import DummyData
from app.models.esp32 import ESP32Connection


ip="168.20.13.1"

startTime= time.time()

 # IP address and port number of the ESP32
data = DummyData()


main = Blueprint('main', __name__)


@main.route('/')
def index():
    # Make connection to ESP here

    return render_template("index.html", ip=ip)

@main.route('/run-python-function', methods=['POST'])
def run_python_function():
    # Get the value of the slider from the AJAX request
    slider_value = request.form.get('value')

    # Call your Python function here, passing the slider value as a parameter
    result = my_python_function(slider_value)
    return jsonify(result=result)


@main.route('/move-forward', methods=['POST'])
def move_forward():
    print("FORWARDDDD")
    return jsonify()

@main.route('/move-backward', methods=['POST'])
def move_backward():
    print("BACKWARRRDDD")
    return jsonify()

@main.route('/move-left', methods=['POST'])
def move_left():
    print("LEFTTT")
    return jsonify()

@main.route('/move-right', methods=['POST'])
def move_right():
    print("RIGGHHH")
    
    return jsonify()

@main.route('/move-stop', methods=['POST'])
def move_stop():
    print("STOPPPPP")
    return jsonify()

    
def reset_esp_connection():
    print("RESETTTT")

def my_python_function(slider):  
    print("SPED SET TO")
    print(slider)
   

@main.route('/get-graph-data-com', methods=['POST'])
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

@main.route('/get-graph-data-obstacle', methods=['POST'])
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

