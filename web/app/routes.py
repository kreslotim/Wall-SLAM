
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
    if espT.connected:
        rec = espT.recv_stat
        send=  espT.send_stat
            
        x_sent =[pair[0] for pair in rec]
        x_received =[pair[1] for pair in rec]
        y_sent = [pair[0] for pair in send]
        y_received =[pair[1] for pair in send]
        
        return jsonify(x_sent=x_sent, y_sent=y_sent, x_received=x_received,y_received=y_received)
    
    return jsonify({'message': 'Command received'}, 200)

@main.route('/get-graph-obs-raw', methods=['GET'])
def get_graph_obs_raw():
    print(" obs-raw ")
    response_data = {
        'x_car': espT.slam_data.curr_x_car,
        'y_car': espT.slam_data.curr_y_car,
        'x_obs': espT.slam_data.list_of_100_x_obs.copy(),
        'y_obs': espT.slam_data.list_of_100_y_obs.copy()
    }
    espT.slam_data._clear_temp_list()
    return jsonify(data=json.dumps(response_data))

@main.route('/get-graph-redundancy', methods=['GET'])
def get_graph_redundancy():
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
@main.route('/get-graph-kmeans', methods=['GET'])
def get_graph_kmeans():
    global cluster_chart
    mapJson, togo = cluster_chart.generate_chart_json(espT.slam_data.list_of_obs)
    print(togo)
    return jsonify(mapJson)

@main.route('/get-graph-movement', methods=['POST'])
def get_graph_movement():
    print("run")
    togo = request.form.get('togo')
  
    if espT.connected:
        if togo:
            print("pass")
            togo_coordinates = json.loads(togo)
            espT.path_finder.setTarget_xy(togo_coordinates)
            
        espT._sendPath_Instruction()
        response_data = {
        'x_car': espT.slam_data.curr_x_car,
        'y_car': espT.slam_data.curr_y_car,
        'x_route': espT.path_finder.x_route,
        'y_route': espT.path_finder.y_route
         }
        print(espT.path_finder.x_route)
        print(espT.path_finder.y_route)
        return jsonify(data=json.dumps(response_data))
    
    return jsonify({'message': 'not connected'}, 200)

############ SETTING API ############
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
