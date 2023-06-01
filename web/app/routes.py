
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

global togo
togoX = (0,0)




startTime= time.time()

espT = ESP32Connection(send_port=send_port,recv_port=recv_port)
espT.start_thread() # Always on
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
    direction = request.form.get('direction')
    repCode = 0
    print("moving")
    print(direction)

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
    list_of_obs = espT.slam_data.list_of_100_orr


    # Create multiple arrays
    result = [[t[i] for t in list_of_obs] for i in range(4)]

    # Print the result
    for sub_arr in result:
        print(sub_arr) 
        
    response_data = {
        'mag': result[0],
        'gyro': result[1],
        'kalman': result[2],
        'time': result[3]
    }


    return jsonify(data=json.dumps(response_data))


@main.route('/get-graph-com', methods=['GET'])
def get_graph_com():
    print(" COM ")
    if espT.connected:
            # Retrieve the time data for 'Sent' and 'Received' traces
        sent_data = espT.send_stat
        received_data =espT.recv_stat
        obs_data= espT.obs_stat
        
        # Create a dictionary with the time data
        chart_data = {
            'sent': sent_data,
            'received': received_data,
            'obs': obs_data
        }
        
        # Return the data as JSON
        return jsonify(data=json.dumps(chart_data))
    
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
    #slist_of_obs = espT.slam_data._filter_obstacles(number_min_of_obstacle, in_radius)
    x_obs = [coord[0] for coord in espT.slam_data.list_of_obs]
    y_obs = [coord[1] for coord in espT.slam_data.list_of_obs]
    response_data = {
        'x_car': espT.slam_data.curr_x_car,
        'y_car': espT.slam_data.curr_y_car,
        'x_obs': x_obs,
        'y_obs': y_obs
    }

    return jsonify(data=json.dumps(response_data))
@main.route('/get-graph-kmeans', methods=['GET'])
def get_graph_kmeans():
    global cluster_chart, togo
    mapJson, togo, rectangle = cluster_chart.generate_chart_json(espT.slam_data.list_of_obs)

  # Generate the list of occupied cells
    cells = []
    for rec in rectangle:
        print(rec)
        min_x_grid, min_y_grid =  espT.path_finder.car_to_grid((rec[0], rec[2]))
        max_x_grid, max_y_grid =  espT.path_finder.car_to_grid((rec[1],rec[3]))
        for x in range(min_x_grid,max_x_grid+ 1):
            for y in range(min_y_grid, max_y_grid + 1):
                cells.append((x, y))
    
        espT.path_finder.fill_grid(cells)
        espT.path_finder.togo_position = espT.path_finder.car_to_grid(togo)
    print("Data calculated")
    print(espT.path_finder.togo_position)
    print(cells)
    return jsonify(mapJson)

@main.route('/get-graph-movement', methods=['POST'])
def get_graph_movement():
        if 'togo' in request.form:
            togo_coordinates = json.loads(request.form['togo'])
            print(f"togo fro web:{togo_coordinates}")
            espT.path_finder.setTarget_xy_in_website( togo_coordinates)
            espT.map_all()
            
        x_route = [coord[0] for coord in espT.path_finder.path]
        y_route = [coord[1] for coord in espT.path_finder.path]

        print(espT.path_finder.generate_list_of_obstacles_for_website())
        response_data = {   
        'gridData': espT.path_finder.generate_list_of_obstacles_for_website(),  
        'pathX': x_route,
        'pathY': y_route,
        'angle' : espT.slam_data.list_of_100_orr.at(-1)
        }

        return jsonify(data=json.dumps(response_data))

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
    print("updating")
    if not settingConnection and sSettingConnection == "true":
        espT.start_thread()
        print("launching")

    if sSettingConnection == "false" and settingConnection:
        espT.stop_thread()
        print("stopping")
       
    settingConnection = (sSettingConnection == "true")

    return jsonify({'success': True})
