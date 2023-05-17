
from flask import Response, render_template, jsonify, request
from flask import Blueprint
import time
import json
import random
import math

from app.models.esp32 import ESP32Connection
from app.models.dummyData import DummyData

main = Blueprint('main', __name__)

ip="168.20.13.1"
recv_port = 8888
send_port = 8889

startTime= time.time()
espT = ESP32Connection(send_port=send_port,recv_port=recv_port)
dataD = DummyData(10)

global settingConnection
settingConnection = False

global settingChewbaccaAuto
settingChewbaccaAuto = False

global settingDataESP
settingDataESP = False

global settingDataSIM
settingDataSIM = False


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
    print( "GRAPH " + str(espT.connected))
    if espT.connected:
        rec =espT.recv_stat
        send=  espT.send_stat
            
        x_sent =[pair[0] for pair in rec]
        x_received =[pair[1] for pair in rec]
        y_sent = [pair[0] for pair in send]
        y_received =[pair[1] for pair in send]

    
        return jsonify(x_sent=x_sent, y_sent=y_sent, x_received=x_received,y_received=y_received)
    
    return jsonify()

@main.route('/get-status-value', methods=['GET'])
def get_status_value():
    return jsonify({'setting' : settingConnection, 'status': espT.connected, 'hostIP' : espT.hostIp, 'hostName' : espT.hostName})

@main.route('/update-switch-state-setting', methods=['POST'])
def update_switch_state_data():
    global settingConnection, settingChewbaccaAuto, settingDataESP, settingDataSIM

    sSettingConnection = request.form.get('connection')
    sSettingChewbaccaAuto = request.form.get('auto')
    sSettingDataESP = request.form.get('dataESP')
    sSettingDataSIM = request.form.get('dataSIM')

    settingChewbaccaAuto = (sSettingChewbaccaAuto == "true")
    settingDataESP = (sSettingDataESP == "true")
    settingDataSIM = (sSettingDataSIM == "true")

    if not settingConnection and sSettingConnection == "true":
        espT.start_thread()

    if sSettingConnection == "false" and settingConnection:
        espT.stop_thread()
       
    settingConnection = (sSettingConnection == "true")

    return jsonify({'success': True})


# This route generates a stream of SSE events
@main.route('/stream-errors')
def stream_errors():
    def event_stream():
        error = []
        # Loop indefinitely
        while True:
            
            # Wait for a new error to be added
            if len(espT.errors) != 0:
                new_error = espT.errors[0]
                espT.errors.pop(0)
                # If a new error is available, send it to the client as an SSE event
                error_time = new_error[0]
                error_message = str(new_error[1])
                yield 'data: {}\n\n'.format(json.dumps((error_time, error_message)))


    # Return the SSE response
    return Response(event_stream(), mimetype='text/event-stream')

# This route generates a stream of SSE events
@main.route('/stream-info')
def stream_info():
    def event_stream():
        error = []
        # Loop indefinitely
        while True:
            time.sleep(1)
            # Wait for a new error to be added
            if len(espT.info) != 0:
                new_info = espT.info[0]
                espT.info.pop(0)
                # If a new error is available, send it to the client as an SSE event
                error_time = new_info[0]
                error_message = str(new_info[1])
                yield 'data: {}\n\n'.format(json.dumps((error_time, error_message)))


    # Return the SSE response
    return Response(event_stream(), mimetype='text/event-stream')

# This route generates a stream of SSE events
@main.route('/stream-output')
def stream_output():
    def event_stream():
        # Loop indefinitely
        while True:
            time.sleep(1)
            # Wait for a new error to be added
            if len(espT.output) != 0:
                new_info = espT.output[0]
                espT.output.pop(0)
                # If a new error is available, send it to the client as an SSE event
                error_time = new_info[0]
                error_message = str(new_info[1])
                yield 'data: {}\n\n'.format(json.dumps((error_time, error_message)))


    # Return the SSE response
    return Response(event_stream(), mimetype='text/event-stream')

# This route generates a stream of SSE events
@main.route('/stream-input')
def stream_input():
    def event_stream():
        # Loop indefinitely
        while True:
            time.sleep(1)
            # Wait for a new error to be added
            if len(espT.input) != 0:
                new_info = espT.input[0]
                espT.input.pop(0)
                # If a new error is available, send it to the client as an SSE event
                error_time = new_info[0]
                error_message = str(new_info[1])
                yield 'data: {}\n\n'.format(json.dumps((error_time, error_message)))


    # Return the SSE response
    return Response(event_stream(), mimetype='text/event-stream')


# This route generates a stream of SSE events
@main.route('/stream-noisy-obstacle')
def stream_noisy_obstacle():
    def event_stream():
        # Loop indefinitely
        while True:
            time.sleep(1)
            # Wait for a new error to be added
            if espT.connected:
                if len(espT.obstacle) != 0:
                    new_info = espT.obstacle[0]
                    espT.obstacle.pop(0)
                    # If a new error is available, send it to the client as an SSE event
                    timeOfObs = new_info[0]
                    x_car = new_info[1]
                    y_car = new_info[2]
                    distance = new_info[3]
                    orientation = new_info[4]
                    x_obs,y_obs = _dataToObstacle(x_car,y_car,distance,orientation)
                    if not (distance == -1):
                        yield 'data: {}\n\n'.format(json.dumps((x_car, y_car,x_obs,y_obs)))
    

                

    # Return the SSE response
    return Response(event_stream(), mimetype='text/event-stream')


def _dataToObstacle(x_car,y_car, distance,orientation):    
    # Calculate the x and y coordinates of the obstacle
    orientation = math.radians(orientation)
    point_x = x_car + distance * math.cos(orientation)
    point_y = y_car + distance * math.sin(orientation)
    return(point_x,point_y)