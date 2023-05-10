
from flask import render_template, jsonify, request
from flask import Blueprint
import time

from app.models.esp32 import ESP32Connection
from app.models.dummyData import DummyData

main = Blueprint('main', __name__)

ip="168.20.13.1"
recv_port = 8888
send_port = 8889

startTime= time.time()
espT = ESP32Connection(send_port=send_port,recv_port=recv_port)
dataD = DummyData(10)


@main.route('/')
def index():
    return render_template('index.html', ip=ip)

@main.route('/run-python-function', methods=['POST'])
def run_python_function():
    # Get the value of the slider from the AJAX request
    slider_value = request.form.get('value')

    # Call your Python function here, passing the slider value as a parameter
    result = my_python_function(slider_value)
    return jsonify(result=result)


@main.route('/map-kmean', methods=['POST'])
def map_kmean():
    print("generate Kmean")
    
    

@main.route('/move-forward', methods=['POST'])
def move_forward():
    print("FORWARDDDD")
    espT._sendMove_Forward()
    return jsonify()

@main.route('/move-backward', methods=['POST'])
def move_backward():
    print("BACKWARRRDDD")
    espT._sendMove_Backward()
    return jsonify()

@main.route('/move-left', methods=['POST'])
def move_left():
    print("LEFTTT")
    espT._sendMove_Left()
    return jsonify()

@main.route('/move-right', methods=['POST'])
def move_right():
    print("RIGGHHH")
    espT._sendMove_Right()
    
    return jsonify()

@main.route('/move-stop', methods=['POST'])
def move_stop():
    print("STOPPPPP")
    espT._sendStop()
    return jsonify()

    
def reset_esp_connection():
    print("RESETTTT")

def my_python_function(slider):  
    print("SPED SET TO")
    print(slider)
   

@main.route('/get-graph-data-com', methods=['POST'])
def get_graph_data_com():
    if espT.connected:
        rec =espT.recv_stat
        send=  espT.send_stat
            
        x_sent =[pair[0] for pair in rec]
        x_received =[pair[1] for pair in rec]
        y_sent = [pair[0] for pair in send]
        y_received =[pair[1] for pair in send]

    
        return jsonify(x_sent=x_sent, y_sent=y_sent, x_received=x_received,y_received=y_received)
    
    return jsonify()
@main.route('/get-graph-data-obstacle', methods=['POST'])
def get_graph_data_obstacle():
    data = {}
    return jsonify(data)

@main.route('/get-status-value', methods=['GET'])
def get_status_value():
    return jsonify({'status': espT.connected, 'hostIP' : espT.hostIp, 'hostName' : espT.hostName})

