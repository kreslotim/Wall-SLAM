
import threading
from flask import Response, render_template, jsonify, request
from flask import Blueprint
import time
import json
import random
import math
import numpy as np

from app.models.esp32 import ESP32Connection

from app.models.dummyData import DummyData
from app.models.mapK import ClusterChart

main = Blueprint('main', __name__)

ip="168.20.13.1"
recv_port = 8888
send_port = 8889

# Initial robot position and obstacle data

global togoX 
togoX = 1
global togoY
togoY = 0


startTime= time.time()

espT = ESP32Connection(send_port=send_port,recv_port=recv_port)
global cluster_chart
cluster_chart  =  ClusterChart()
dataD = DummyData(10)

#TODO to delete later
number_min_of_obstacle = 2
in_radius = 30

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


############ MOVEMENT API ############
@main.route('/post-move', methods=['POST'])
def post_move():
    direction = request.args.get('direction')
    repCode = 0

    if direction == 'forward':
        repCode = espT._sendMove_Forward()
        pass
    elif direction == 'stop':
        repCode = espT._sendStop()
        pass
    elif direction == 'right':
        repCode = espT._sendMove_Right()
        pass
    elif direction == 'left':
        repCode = espT._sendMove_Left()
        pass
    elif direction == 'backward':
        repCode = espT._sendMove_Backward()
        pass
    else:
        repCode = 404
    
    if repCode == 404:
         return jsonify({'message': 'Unable to send Command', 'espStatus' : repCode })
    return jsonify({'message': 'Command received', 'espStatus' : repCode })


############ GRAPH API ############ 
@main.route('/get-graph-distance', methods=['GET'])
def get_graph_distance():
    print(" distance ")
    return jsonify({'message': 'Command received'}, 200)
@main.route('/get-graph-orientation', methods=['GET'])
def get_graph_orientation():
    print(" orientation ")
    return jsonify({'message': 'Command received'}, 200)
@main.route('/get-graph-com', methods=['GET'])
def get_graph_com():
    print(" COM ")
    return jsonify({'message': 'Command received'}, 200)
@main.route('/get-graph-obs-raw', methods=['GET'])
def get_graph_obs_raw():
    print(" obs-raw ")
    return jsonify({'message': 'Command received'}, 200)
@main.route('/get-graph-redundancy', methods=['GET'])
def get_graph_redundancy():
    print(" redundancy ")
    return jsonify({'message': 'Command received'}, 200)
@main.route('/get-graph-kmeans', methods=['GET'])
def get_graph_kmeans():
    print(" kmeans ")
    return jsonify({'message': 'Command received'}, 200)
@main.route('/get-graph-movement', methods=['GET'])
def get_graph_movement():
    print(" movement ")
    return jsonify({'message': 'Command received'}, 200)

############ Decrepitated API ############
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

@main.route('/get-graph-data-slam', methods=['GET'])
def get_graph_data_slam():
    list_of_obs = espT.slam_data._filter_obstacles(number_min_of_obstacle, in_radius)
    x_obs = [point[0] for point in list_of_obs]
    y_obs = [point[1] for point in list_of_obs]
   
    response_data = {
        'x_car': espT.slam_data.curr_x_car,
        'y_car': espT.slam_data.curr_y_car,
        'x_obs': x_obs,
        'y_obs': y_obs
    }

    return jsonify(data=json.dumps(response_data))

@main.route('/update_kmean_slider', methods=['POST'])
def update_kmean_slider():
    global cluster_chart
    filter_value = int(request.form.get('filter'))
    max_k_value = int(request.form.get('max_k'))
    split_value = float(request.form.get('split'))
    threshold_value = float(request.form.get('threshold'))
    
    cluster_chart  =  ClusterChart(split_value,threshold_value,max_k_value,filter_value)
    return 'Slider values received successfully'

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
            time.sleep(0.1)
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
            time.sleep(0.1)
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
            time.sleep(0.1)
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
            time.sleep(0.1)
           
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
            # Wait for a new error to be added
            if espT.connected:
                if espT.slam_data._is_ready_to_go():
                    yield 'data: {}\n\n'.format(json.dumps((espT.curr_x_car, espT.curr_y_car, espT.list_of_100_x_obs, espT.list_of_100_y_obs)))
                    espT._clear_temp_list()
            
            elif settingDataSIM:
                print("Adding data")
                new_info = dataD._randomlyFill()
                timeOfObs = new_info[0]
                x_car = new_info[1]
                y_car = new_info[2]
                distance = new_info[3]
                orientation = new_info[4]
                x_obs,y_obs = _dataToObstacle(x_car,y_car,distance,orientation)
                if not (distance == -1):
                    yield 'data: {}\n\n'.format(json.dumps((x_car, y_car, x_obs, y_obs)))
                

    # Return the SSE response
    return Response(event_stream(), mimetype='text/event-stream')

#TODO TO DELETE 
def _dataToObstacle(x_car,y_car, distance,orientation):    
    # Calculate the x and y coordinates of the obstacle
    orientation = math.radians(orientation)
    point_x = x_car + distance * math.cos(orientation)
    point_y = y_car + distance * math.sin(orientation)

    return(point_x,point_y)

@main.route('/refresh_map', methods=['GET'])
def refresh_map():
    global cluster_chart

    mapJson = cluster_chart.generate_chart_json(espT.slam_data.list_of_obs)
               
               
    return jsonify(mapJson)

@main.route('/get_new_trace_data', methods=['GET'])
def get_new_trace_data():
    num_points = 3
    points = [(random.random(), random.random()) for _ in range(num_points)]
    print(f"sending togo {togoX}")
    return jsonify({'points': points, 'robot' : (2,1), 'togo' : (togoX,togoY)})

@main.route('/process_coordinates', methods=['POST'])
def process_coordinates():
    global togoX,togoY
    togoX = request.form.get('x')
    togoY = request.form.get('y')
    print(togoX,togoY)

    # Process the received coordinates
    # ... Your code to handle the coordinates ...

    # Return a response to the AJAX request if needed
    return 'Coordinates processed successfully'
