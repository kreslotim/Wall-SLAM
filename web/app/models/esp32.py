import socket
import time
import struct
import threading
import math
import random



class ESP32Connection:
    def __init__(self, send_port, recv_port):
        print("Establishing Connection")

        # INPUT
        self.send_port = send_port
        self.recv_port = recv_port

        # Connection variable
        self.espIP = None
        self.hostName = socket.gethostname()
        self.hostIp = socket.gethostbyname(self.hostName) 
        self.connected = False
        self.send_socket = None
        self.recv_socket = None
        self.running = False

        # Logging
        self.errors = []
        self.info=[]
        self.output = []
        self.input = []

        # OUTPUT
        self.obstacle = []

        # Statistic variable
        self.recv_stat = []
        self.send_stat = []
        self.time = time.time()

        self.list_of_obs = []
        self.list_of_100_x_obs = []
        self.list_of_100_y_obs = []
        self.numberOfObsInOneGo = 50
        self.delete_distance_if_no_distance = 30
        self.delete_distance_linear_equation = 10
        self.max_distance_detection = 2000
        self.number_min_of_obstacle = 1
        self.in_radius = 10

        self.curr_x_car = 0
        self.curr_y_car = 0
    
######## Thread Looping #############

    def stop_thread(self):
        timeOfRep = round( time.time() - self.time, 2)
        self.info.append((timeOfRep, "Stopping threads ..."))
        self.running = False

    def start_thread(self):
        timeOfRep = round( time.time() - self.time, 2)
        self.info.append((timeOfRep, "Starting threads ..."))
        self.running = True
        connectLoop = threading.Thread(target=self.thread_connect) 
        listenLoop = threading.Thread(target=self._listen)
        connectLoop.start()
        listenLoop.start()

    def thread_connect(self):
        while self.running:
            if not self._is_socket_alive() or not self.connected :
                timeOfRep = round( time.time() - self.time, 2)
                self.info.append((timeOfRep, "Connection Thread Reconnecting ..."))
                self.connected = False
                self._connect()
            time.sleep(1)
        timeOfRep = round( time.time() - self.time, 2)
        self.info.append((timeOfRep, "Connection Thread Stopped"))

    def _listen(self):
        while self.running:
            if self.connected:
                # Receive data from the client socket
                data = self.recv_socket.recv(48)
                data_decoded = struct.unpack('ffffffffffff', data)

                if data:
                    self.recv_socket.send("200".encode())

                    # TODO INACURATE. ESP OUTPUT UNCLEAR.
                    distanceBack = data_decoded[3]
                    distanceFront = data_decoded[2]

                    if (distanceFront == -1) :
                        distanceFront = 0
                    else :
                        distanceFront += 20

                    if (distanceBack == -1) :
                        distanceBack = 0
                    else :
                        distanceBack = -distanceBack-20
                    orientation= data_decoded[4]

                    x_car = data_decoded[5]
                    y_car= data_decoded[6]
                    timeOfReading= data_decoded[7]

                   
                   
                    self.obstacle.append((timeOfReading,x_car,y_car,distanceFront,orientation))
                    self.obstacle.append((timeOfReading,x_car,y_car,distanceBack,orientation))
                    self.output.append((timeOfReading, 'Position ', x_car, y_car))  
                    self.output.append((timeOfReading, 'Obstacle found at ', distanceFront, ' mm, looking at ', orientation)) 
                    # Log it
                    timeOfRep = round( time.time() - self.time, 2)
        
                    #self.recv_stat.append([1, timeOfRep])



        timeOfRep = round( time.time() - self.time, 2)
        self.info.append((timeOfRep, "Listen Thread stopped"))           

############ COMMUNICATION METHOD #############

    def _connect(self):
        try:
            # create a socket object for receiving data from the client
            recv_socket = socket.socket()
            recv_socket.bind(('0.0.0.0', self.recv_port))  # bind to a local address and port
            recv_socket.listen(0)  # start listening for incoming connections
            recv_socket.settimeout(5.0)  # set a timeout of 10 seconds

            # wait for a client to connect
            self.recv_socket, client_address = recv_socket.accept()

            timeOfRep = round( time.time() - self.time, 2)
            self.info.append((timeOfRep, 'Recv established successfully by', client_address))   

            recv_socket.close()
            self.espIP = client_address[0]

            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.send_socket.settimeout(5)  # set a timeout of 2 seconds
            self.send_socket.connect((self.espIP, self.send_port))
            
            timeOfRep = round( time.time() - self.time, 2)
            self.info.append((timeOfRep, 'Send established successfully, connection established successfully')) 
    
            
            self.connected = True

        except Exception as e:
            print("Connection error :", e)
            print("Reconnecting ...")
            timeOfRep = round( time.time() - self.time, 2)
            self.errors.append((timeOfRep, e))

            self.connected = False
            time.sleep(1)
    


    def _send_actionNumber(self, actionNumber):
        if self.connected:
            try:
                # Send the packed angles over the socket
                packed_angles = struct.pack('f', actionNumber)
                self.send_socket.sendall(packed_angles)

                # Wait for a response from the ESP32
                response = 0

                while (self._is_socket_alive() and not response == "200") :
                    
                    response = self.send_socket.recv(1024).decode()   
                    print("Received response from ESP32:", response)

                if not self._is_socket_alive() :  
                    print("Invalid response from ESP32, reconnecting...")
                    self.recv_socket.close()
                    self.send_socket.close()
                    self._connect() 
                    self._send_actionNumber(actionNumber)
                    return 410
               
            except Exception as e:
                print("Connection error :", e)
                timeOfRep = round( time.time() - self.time, 2)
                self.errors.append((timeOfRep, e))
                return 400
                

            timeOfRep = round( time.time() - self.time, 2)
            self.send_stat.append([1,timeOfRep]) # To make a graph about the number of packet send
            return 200
        return 400


############ ESP DIRECT COMMAND METHOD ############

    def _sendStop(self):
        repStatut = self._send_actionNumber(0)
        timeOfRep = round( time.time() - self.time, 2)
        if repStatut == 200 :
            self.output.append((timeOfRep, 'Sent stop successful :' + str(repStatut))) 
        else :
            self.output.append((timeOfRep, 'Sent Move fail : ' + str(repStatut))) 
 
    def _sendMove_Forward(self):
        repStatut = self._send_actionNumber(1)
        timeOfRep = round( time.time() - self.time, 2)
        if repStatut == 200 :
            self.output.append((timeOfRep, 'Sent Move Forward successful :' + str(repStatut))) 
        else :
            self.output.append((timeOfRep, 'Sent Move Forward fail : ' + str(repStatut))) 
 
    
    
    def _sendMove_Backward(self):
        repStatut = self._send_actionNumber(2)
        timeOfRep = round( time.time() - self.time, 2)
        if repStatut == 200 :
            self.output.append((timeOfRep, 'Sent Move Forward successful :' + str(repStatut))) 
        else :
            self.output.append((timeOfRep, 'Sent Move Forward fail  : ' + str(repStatut))) 
 

    def _sendMove_Right(self):
        repStatut = self._send_actionNumber(3)
        timeOfRep = round( time.time() - self.time, 2)
        if repStatut == 200 :
            self.output.append((timeOfRep, 'Sent Move Forward successful :' + str(repStatut))) 
        else :
            self.output.append((timeOfRep, 'Sent Move Forward fail  : ' + str(repStatut))) 
 

    def _sendMove_Left(self):
        repStatut = self._send_actionNumber(4)
        timeOfRep = round( time.time() - self.time, 2)
        if repStatut == 200 :
            self.output.append((timeOfRep, 'Sent Move Forward successful : ' + str(repStatut))) 
        else :
            self.output.append((timeOfRep, 'Sent Move Forward fail  : ' +str(repStatut))) 

############ OBSTACLE METHODS ############

    def _add_and_delete_obstacle(self, x_car, y_car, obs_distance, orientation):

        if obs_distance != 0 and obs_distance < self.max_distance_detection and obs_distance > -self.max_distance_detection:
            x_new, y_new = self._dataToObstacle(x_car,y_car, obs_distance,orientation)   
            self.list_of_obs.append([x_new,y_new])
            self.list_of_100_x_obs.append(x_new)
            self.list_of_100_y_obs.append(y_new)
        else :
            x_new, y_new = self._dataToObstacle(x_car,y_car, obs_distance,orientation)   
            obs_distance = self.delete_distance_if_no_distance

        # Calculate the linear equation between the car and new obstacle
        m = (y_new - y_car)/(x_new - y_car ) if (x_new - y_car) != 0 else 0
        b = -m*x_car + y_car

        # Find the obstacles that lie on the linear equation between the new obstacle and the origin
        obstacles_to_delete = []

        for obstacle in self.list_of_obs:
            x_obs, y_obs = obstacle

            # Check if the obstacle lies on the linear equation
            distance = abs(y_obs - m * x_obs - b) / math.sqrt(1 + m**2)

            # Check if the obstacle lies between the new obstacle and the origin
            if (x_car < x_obs < x_new - 10 or x_car > x_obs > x_new + 10) and self.delete_distance_linear_equation > distance:
                    obstacles_to_delete.append(obstacle)

        # Remove the obstacles that lie on the linear equation between the new obstacle and the origin
        for obstacle in obstacles_to_delete:
            self.list_of_obs.remove(obstacle)
            
        return self.list_of_obs

    def _filter_obstacles(self, number_min_of_obstacle, radius):
        filtered_obs = []

        for obstacle in self.list_of_obs:
            count = 0

            # Check the distance between each point and the obstacle
            for point in self.list_of_obs:
                if obstacle != point:
                    distance = math.sqrt((obstacle[0] - point[0])**2 + (obstacle[1] - point[1])**2)
                    if distance <= radius:
                        count += 1

            # If the count is greater than or equal to n, keep the obstacle
            if count >= number_min_of_obstacle:
                filtered_obs.append(obstacle)

        self.list_of_obs = filtered_obs.copy()

        return self.list_of_obs

    def _is_ready_to_go(self):
        return len(self.list_of_100_x_obs) > self.numberOfObsInOneGo 

    def _clear_temp_list(self):
        self.list_of_100_x_obs.clear()
        self.list_of_100_y_obs.clear()


############ HELPER METHOD ############

    def _dataToObstacle(self, x_car,y_car, distance,orientation):    
        # Calculate the x and y coordinates of the obstacle
        orientation = math.radians(orientation)
        point_x = x_car + distance * math.cos(orientation)
        point_y = y_car + distance * math.sin(orientation)

        return(point_x,point_y)

    def _is_socket_alive(self):
        if self.send_socket is None: 
            return False
        err = self.send_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        return err == 0
    

