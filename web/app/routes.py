
import threading
from flask import Response, render_template, jsonify, request
from flask import Blueprint
import time
import json
import random
import math

from app.models.esp32 import ESP32Connection
from app.models.esp32Bluetooth import ESP32ConnectionBluetooth

from app.models.dummyData import DummyData
from app.models.mapK import ClusterChart

main = Blueprint('main', __name__)

ip="168.20.13.1"
recv_port = 8888
send_port = 8889

# Initial robot position and obstacle data
robotX = 0
robotY = 0
global togoX 
togoX = 1
global togoY
togoY = 0
obstacles = []


startTime= time.time()
#espT = ESP32ConnectionBluetooth(com_port=com_port,baud_port=baud_port)
espT = ESP32Connection(send_port=send_port,recv_port=recv_port)
global cluster_chart
cluster_chart  =  ClusterChart()
dataD = DummyData(10)

list_of_100_x_obs = []
list_of_100_y_obs = []
numberOfObsInOneGo = 50
delete_distance = 30
max_distance_detection = 2000
number_min_of_obstacle = 1
in_radius = 10



global settingConnection
settingConnection = False

global settingChewbaccaAuto
settingChewbaccaAuto = False

global settingDataESP
settingDataESP = False

global settingDataSIM
settingDataSIM = False



global list_of_obs
list_of_obs = []

global curr_x_car
curr_x_car = 0

global curr_y_car
curr_y_car = 0


# Create a lock to synchronize access to the computation
computation_lock = threading.Lock()

@main.route('/')
def index():
    return render_template('index.html', ip=ip)



@main.route('/update_kmean_slider', methods=['POST'])
def update_kmean_slider():
    global cluster_chart
    filter_value = int(request.form.get('filter'))
    max_k_value = int(request.form.get('max_k'))
    split_value = float(request.form.get('split'))
    threshold_value = float(request.form.get('threshold'))
    
    cluster_chart  =  ClusterChart(split_value,threshold_value,max_k_value,filter_value)
    return 'Slider values received successfully'

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
        espT.listening_lock.acquire()
        rec =espT.recv_stat
        send=  espT.send_stat
        espT.listening_lock.release()
            
        x_sent =[pair[0] for pair in rec]
        x_received =[pair[1] for pair in rec]
        y_sent = [pair[0] for pair in send]
        y_received =[pair[1] for pair in send]
        

    
        return jsonify(x_sent=x_sent, y_sent=y_sent, x_received=x_received,y_received=y_received)
    
    return jsonify()

@main.route('/get-graph-data-slam', methods=['GET'])
def get_graph_data_slam():
    global list_of_obs
   
    x_obs = [point[0] for point in list_of_obs]
    y_obs = [point[1] for point in list_of_obs]
   
    response_data = {
        'x_car': curr_x_car,
        'y_car': curr_y_car,
        'x_obs': x_obs,
        'y_obs': y_obs
    }

    return jsonify(data=json.dumps(response_data))


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
            time.sleep(1)
            # Wait for a new error to be added
            espT.listening_lock.acquire()
            if len(espT.errors) != 0:
                new_error = espT.errors[0]
                espT.errors.pop(0)
                # If a new error is available, send it to the client as an SSE event
                error_time = new_error[0]
                error_message = str(new_error[1])
                yield 'data: {}\n\n'.format(json.dumps((error_time, error_message)))
            espT.listening_lock.release()


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
            espT.listening_lock.acquire()
            while len(espT.info) != 0:
                new_info = espT.info[0]
                espT.info.pop(0)
                # If a new error is available, send it to the client as an SSE event
                error_time = new_info[0]
                error_message = str(new_info[1])
                yield 'data: {}\n\n'.format(json.dumps((error_time, error_message)))
            espT.listening_lock.release()


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
            espT.listening_lock.acquire()
            while len(espT.output) != 0:
                new_info = espT.output[0]
                espT.output.pop(0)
                # If a new error is available, send it to the client as an SSE event
                error_time = new_info[0]
                error_message = str(new_info[1])
                yield 'data: {}\n\n'.format(json.dumps((error_time, error_message)))
            espT.listening_lock.release()


    # Return the SSE response
    return Response(event_stream(), mimetype='text/event-stream')

# This route generates a stream of SSE events
@main.route('/stream-input')
def stream_input():
    def event_stream():
        # Loop indefinitely
        while True:
            time.sleep(1)
            espT.listening_lock.acquire()
            # Wait for a new error to be added
            while len(espT.input) != 0:
                new_info = espT.input[0]
                espT.input.pop(0)
                # If a new error is available, send it to the client as an SSE event
                error_time = new_info[0]
                error_message = str(new_info[1])
                yield 'data: {}\n\n'.format(json.dumps((error_time, error_message)))
            espT.listening_lock.release()


    # Return the SSE response
    return Response(event_stream(), mimetype='text/event-stream')

# This route generates a stream of SSE events
@main.route('/stream-noisy-obstacle')
def stream_noisy_obstacle():
    global curr_x_car, curr_y_car
    def event_stream():
        # Loop indefinitely
        while True:
            # Wait for a new error to be added
            if espT.connected:
                time.sleep(0.1)
                espT.listening_lock.acquire()
                while len(espT.obstacle) != 0:
                    new_info = espT.obstacle[0]
                    espT.obstacle.pop(0)
                    # If a new error is available, send it to the client as an SSE event
                    timeOfObs = new_info[0]
                    curr_x_car = new_info[1]
                    curr_y_car = new_info[2]
                    distance = new_info[3]
                    orientation = new_info[4]
                    
                    _add_and_delete_obstacle(curr_x_car, curr_y_car, distance, orientation)

                    if len(list_of_100_x_obs) > numberOfObsInOneGo :
                        yield 'data: {}\n\n'.format(json.dumps((curr_x_car, curr_y_car, list_of_100_x_obs,list_of_100_y_obs)))
                        list_of_100_x_obs.clear()
                        list_of_100_y_obs.clear()
                espT.listening_lock.release()


    
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

def _dataToObstacle(x_car,y_car, distance,orientation):    
    # Calculate the x and y coordinates of the obstacle
    orientation = math.radians(orientation)
    point_x = x_car + distance * math.cos(orientation)
    point_y = y_car + distance * math.sin(orientation)

    return(point_x,point_y)



@main.route('/refresh_map', methods=['GET'])
def refresh_map():
    global list_of_obs, cluster_chart

    mapJson = cluster_chart.generate_chart_json(list_of_obs)
               
               
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

def _add_and_delete_obstacle(x_car, y_car, obs_distance, orientation):
    global list_of_obs
    # Convert the orientation from degrees to radians
    angle_rad = math.radians(orientation)

    if obs_distance != 0 and obs_distance < max_distance_detection and obs_distance > -max_distance_detection: 
        x_new, y_new = _dataToObstacle(x_car,y_car, obs_distance,orientation)   
        list_of_obs.append([x_new,y_new])
        list_of_100_x_obs.append(x_new)
        list_of_100_y_obs.append(y_new)
        x_new -= x_car
        y_new -= y_car
    else :
        obs_distance = delete_distance
        x_new = obs_distance * math.cos(angle_rad)
        y_new = obs_distance * math.sin(angle_rad)

    # Calculate the slope of the line with the given orientation
    slope = math.tan(angle_rad)

    # Find the obstacles that lie on the linear equation between the new obstacle and the origin
    obstacles_to_delete = []

    for obstacle in list_of_obs:
        x_obs, y_obs = obstacle

        # Check if the obstacle lies on the linear equation
        if math.isclose(y_obs, slope * x_obs, abs_tol = 10):
            # Check if the obstacle lies between the new obstacle and the origin
            if 0 < x_obs < x_new-10 or 0 > x_obs > x_new-10:
                obstacles_to_delete.append(obstacle)

    # Remove the obstacles that lie on the linear equation between the new obstacle and the origin
    for obstacle in obstacles_to_delete:
        list_of_obs.remove(obstacle)
        
    return list_of_obs

def _filter_obstacles(number_min_of_obstacle, radius):
    global list_of_obs

    filtered_obs = []

    for obstacle in list_of_obs:
        count = 0

        # Check the distance between each point and the obstacle
        for point in list_of_obs:
            if obstacle != point:
                distance = math.sqrt((obstacle[0] - point[0])**2 + (obstacle[1] - point[1])**2)
                if distance <= radius:
                    count += 1

        # If the count is greater than or equal to n, keep the obstacle
        if count >= number_min_of_obstacle:
            filtered_obs.append(obstacle)

    list_of_obs = filtered_obs.copy()

    return list_of_obs

