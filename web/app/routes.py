from flask import render_template, jsonify, request
from flask import Blueprint
import time
import json

from app.models.esp32 import ESP32Connection
from app.models.mapK import ClusterChart

main = Blueprint('main', __name__)

ip="168.20.13.1"
recv_port = 8888
send_port = 8889

espT = ESP32Connection(send_port=send_port,recv_port=recv_port)
startTime = time.time()

# Initial robot position and obstacle data
global togo
togo = (0,0)

global cluster_chart
cluster_chart  =  ClusterChart()

espT.start_thread()

# Know if you are connected or not
global settingConnection
settingConnection = False

@main.route('/')
def index():
    """
    Route handler for the root URL ("/").
    Renders the "index.html" template and passes the 'ip' variable to it.
    """
    return render_template('index.html', ip=ip)


############ MOVEMENT API ############
@main.route('/post-move', methods=['POST'])
def post_move():
    """
    Route handler for the "/post-move" endpoint with the POST method.
    Receives the 'direction' parameter from the request form and sends
    corresponding commands to the ESP32 based on the direction.
    Returns a JSON response indicating the command status.
    """
    direction = request.form.get('direction')
    repCode = 0

    if direction == 'forward':
        repCode = espT.sendMove_Forward()
        pass
    elif direction == 'stop':
        repCode = espT.sendStop()
        pass
    elif direction == 'right':
        repCode = espT.sendMove_Right()
        pass
    elif direction == 'left':
        repCode = espT.sendMove_Left()
        pass
    elif direction == 'backward':
        repCode = espT.sendMove_Backward()
        pass
    else:
        repCode = 404
    if repCode == 404:
         return jsonify({'message': 'Unable to send Command', 'espStatus' : repCode })
    return jsonify({'message': 'Command received', 'espStatus' : repCode })


############ GRAPH API ############ 
@main.route('/get-graph-distance', methods=['GET'])
def get_graph_distance():
    """
    Route handler for the "/get-graph-distance" endpoint with the GET method.
    Retrieves the orientation from espT.slam_data and returns it as a JSON response.
    """
    list_of_obs = espT.slam_data.list_of_temp_orr

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
    """
    Route handler for the "/get-graph-com" endpoint with the GET method.
    Retrieves the number of data packages transfer from espT and returns it as a JSON response.
    """
    print(" COM ")
    if espT.connected:
            # Retrieve the time data for 'Sent' and 'Received' traces
        sent_data = espT.send_stat
        received_data = espT.recv_stat
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
    """
    Route handler for the "/get-graph-obs-raw" endpoint with the GET method.
    Retrieves the raw list of obstacles with from espT.slam_data and returns it as a JSON response.
    """
    response_data = {
        'x_car': espT.slam_data.curr_x_car,
        'y_car': espT.slam_data.curr_y_car,
        'x_obs': espT.slam_data.list_of_temp_x_obs.copy(),
        'y_obs': espT.slam_data.list_of_temp_y_obs.copy()
    }
    return jsonify(data=json.dumps(response_data))

@main.route('/get-graph-redundancy', methods=['GET'])
def get_graph_redundancy():
    """
    Route handler for the "/get-graph-redundancy" endpoint with the GET method.
    Retrieves filter list of data from espT.slam_data and returns it as a JSON response.
    """
    list_of_obs = espT.slam_data.filter_obstacles()
    x_obs = [coord[0] for coord in list_of_obs]
    y_obs = [coord[1] for coord in list_of_obs]
    response_data = {
        'x_car': espT.slam_data.curr_x_car,
        'y_car': espT.slam_data.curr_y_car,
        'x_obs': x_obs,
        'y_obs': y_obs
    }

    return jsonify(data=json.dumps(response_data))
@main.route('/get-graph-kmeans', methods=['GET'])
def get_graph_kmeans():
    """
    Route handler for the "/get-graph-kmeans" endpoint with the GET method.
    Generates a chart JSON using cluster_chart with K-means and returns it as a JSON response.
    """
    global cluster_chart
    mapJson, togo, rectangle = cluster_chart.generate_chart_json(espT.slam_data.list_of_obs)

    # Generate the list of occupied cells
    cells = []
    for rec in rectangle:
        min_x_grid, min_y_grid =  espT.path_finder.car_to_grid((rec[0], rec[2]))
        max_x_grid, max_y_grid =  espT.path_finder.car_to_grid((rec[1],rec[3]))
        for x in range(min_x_grid,max_x_grid + 1):
            for y in range(min_y_grid, max_y_grid + 1):
                cells.append((x, y))

    espT.path_finder.fill_grid(cells)
    print(togo , espT.path_finder.car_to_grid(togo))
    if (espT.path_finder.togo_position != espT.path_finder.car_to_grid(togo) and espT.path_finder.togo_position and len(espT.path_finder.path)<2) or espT.path_finder.togo_position is None:
        espT.path_finder.togo_position = espT.path_finder.car_to_grid(togo)
    espT.map_all()
    x_route = [coord[0] for coord in espT.path_finder.path]
    y_route = [coord[1] for coord in espT.path_finder.path]

    response_data = {   
    'map': mapJson,
    'pathX': x_route,
    'pathY': y_route,
    'angle' : espT.slam_data.list_of_temp_orr[-1][2] if len(espT.slam_data.list_of_temp_orr) != 0 else []
    }
    return jsonify(data=json.dumps(response_data))

@main.route('/get-graph-movement', methods=['POST'])
def get_graph_movement():
    """
    Route handler for the "/get-graph-movement" endpoint with the POST method.
    Receives targeted coordinates from the mouse-click on the map, sets the target in espT.path_finder and forces espT.path_finder to run Dijkstra, and returns a JSON response with grid data, path coordinates, and angle.
    """
    if 'togo' in request.form:
        togo_coordinates = json.loads(request.form['togo'])
        if len(togo_coordinates) != 0 :
            print(f"togo_coordinates : {togo_coordinates}")
            espT.path_finder.setTarget_xy_in_website( togo_coordinates)
            espT.map_all()

            
    x_route = [coord[0] for coord in espT.path_finder.path]
    y_route = [coord[1] for coord in espT.path_finder.path]

    response_data = {   
    'gridData': espT.path_finder.generate_list_of_obstacles_for_website(),  
    'pathX': x_route,
    'pathY': y_route,
    'angle' : espT.slam_data.list_of_temp_orr[-1][2] if len(espT.slam_data.list_of_temp_orr) != 0 else []
    }

    return jsonify(data=json.dumps(response_data))

############ SETTING API ############
@main.route('/update_kmean_slider', methods=['POST'])
def update_kmean_slider():
    """
    Route handler for the "/update_kmean_slider" endpoint with the POST method.
    Updates the values of chart based on the received slider values.
    Returns a success message.
    """
    global cluster_chart
    filter_value = int(request.form.get('filter'))
    max_k_value = int(request.form.get('max_k'))
    split_value = float(request.form.get('split'))
    threshold_value = float(request.form.get('threshold'))
    
    cluster_chart  =  ClusterChart(split_value,threshold_value,max_k_value,filter_value)
    return 'Slider values received successfully'

@main.route('/get-status-value', methods=['GET'])
def get_status_value():
    """
    Route handler for the "/get-status-value" endpoint with the GET method.
    Returns a JSON response with the status values including the connection status,
    ESP32 status, host IP, and host name.
    """
    return jsonify({'setting' : settingConnection, 'status': espT.connected, 'hostIP' : espT.hostIp, 'hostName' : espT.hostName})

@main.route('/update-switch-state-setting', methods=['POST'])
def update_switch_state_data():
    """
    Route handler for the "/update-switch-state-setting" endpoint with the POST method. Updates the switch state value and starts or stops the ESP32 thread accordingly. Returns a JSON response indicating the success status.
    """
    global settingConnection

    sSettingConnection = request.form.get('connection')

    print("updating")
    if not settingConnection and sSettingConnection == "true":
        espT.start_thread()
        print("launching")

    if sSettingConnection == "false" and settingConnection:
        espT.stop_thread()
        print("stopping")
       
    settingConnection = (sSettingConnection == "true")

    return jsonify({'success': True})
