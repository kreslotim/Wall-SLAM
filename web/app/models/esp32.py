import socket
import time
import struct
import threading
from app.models.slamData import SlamData
from app.models.pathFindingAlgo import PathFinder


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
        self.info = []
        self.output = []
        self.input = []

        # OUTPUT
        self.obstacle = []

        # Statistic variable
        self.recv_stat = []
        self.send_stat = []
        self.time = time.time()

        # Data variable
        self.slam_data = SlamData()
        self.path_finder = PathFinder()
        self.action_instruction_list = []
        

    
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

                    # Use the data 
                    distanceFront = data_decoded[2]
                    distanceBack = data_decoded[3]
                    orientation = data_decoded[4]
                    self.slam_data.curr_x_car = data_decoded[5]
                    self.slam_data.curr_y_car = data_decoded[6]
                    timeOfReading = data_decoded[7]
                    self.slam_data.perfect_orientation = data_decoded[8]

                    # Filter invalid distances to 0, to allow negative distances
                    if (distanceFront == -1) :
                        distanceFront = 0
                    else :
                        distanceFront += 20

                    if (distanceBack == -1) :
                        distanceBack = 0
                    else :
                        distanceBack = -distanceBack - 20

              
                    # Adding obstacles with Front Lidar
                    self.slam_data._add_and_delete_obstacle(self.slam_data.curr_x_car,  self.slam_data.curr_y_car, distanceFront, orientation)

                    # Adding obstacles with Back Lidar
                    self.slam_data._add_and_delete_obstacle(self.slam_data.curr_x_car,  self.slam_data.curr_y_car, distanceBack, orientation)

                    #TODO Flo do you still want this ??

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
        return repStatut
 
    def _sendMove_Forward(self):
        repStatut = self._send_actionNumber(1)
        timeOfRep = round( time.time() - self.time, 2)
        if repStatut == 200 :
            self.output.append((timeOfRep, 'Sent Move Forward successful :' + str(repStatut))) 
        else :
            self.output.append((timeOfRep, 'Sent Move Forward fail : ' + str(repStatut))) 
        return repStatut
    
    def _sendMove_Backward(self):
        repStatut = self._send_actionNumber(2)
        timeOfRep = round( time.time() - self.time, 2)
        if repStatut == 200 :
            self.output.append((timeOfRep, 'Sent Move Forward successful :' + str(repStatut))) 
        else :
            self.output.append((timeOfRep, 'Sent Move Forward fail  : ' + str(repStatut))) 
        return repStatut

    def _sendMove_Right(self):
        repStatut = self._send_actionNumber(3)
        timeOfRep = round( time.time() - self.time, 2)
        if repStatut == 200 :
            self.output.append((timeOfRep, 'Sent Move Forward successful :' + str(repStatut))) 
        else :
            self.output.append((timeOfRep, 'Sent Move Forward fail  : ' + str(repStatut))) 
        return repStatut

    def _sendMove_Left(self):
        repStatut = self._send_actionNumber(4)
        timeOfRep = round( time.time() - self.time, 2)
        if repStatut == 200 :
            self.output.append((timeOfRep, 'Sent Move Forward successful : ' + str(repStatut))) 
        else :
            self.output.append((timeOfRep, 'Sent Move Forward fail  : ' +str(repStatut))) 
        return repStatut
    
############ PATH FINDING ############
    def _sendPath_Instruction(self):
        pos_car = (self.slam_data.curr_x_car, self.slam_data.curr_y_car)
        
        # Calculate the best path and send the instrucitions
        #TODO for now instructions_to_go_x_y sends an Array but needs to be modified to only send the first instruction of the list
        self._send_actionNumber(self.path_finder.instructions_to_go_x_y(pos_car, self.slam_data.perfect_orientation, self.slam_data.list_of_obs))

############ HELPER METHOD ############

    def _is_socket_alive(self):
        if self.send_socket is None: 
            return False
        err = self.send_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        return err == 0
    
