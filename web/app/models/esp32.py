import socket
import time
import struct
import threading
from app.models.slamData import SlamData
import pywifi
import time
from app.models.pathfinder import PathFinder



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
        self.obs_stat = []
        self.time = time.time()

        # Data variable
        self.slam_data = SlamData()
        self.path_finder = PathFinder()
        self.action_instruction_list = []

        self.ssid = "espWifi2"
        self.password = "0123456789A"




 
    def connect_to_wifi(self):
        ssid = self.ssid
        password = self.password
        wifi = pywifi.PyWiFi()  # Create a PyWiFi object
        iface = wifi.interfaces()[0]  # Get the first available network interface

        iface.disconnect()  # Disconnect from any existing Wi-Fi connection
        time.sleep(1)

        profile = pywifi.Profile()  # Create a new Wi-Fi profile
        profile.ssid = ssid  # Set the SSID (Wi-Fi network name)
        profile.auth = pywifi.const.AUTH_ALG_OPEN  # Set the authentication algorithm

        # Set the encryption type and password (comment out if the network is not password-protected)
        profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
        profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
        profile.key = password

        iface.remove_all_network_profiles()  # Remove all existing profiles
        temp_profile = iface.add_network_profile(profile)  # Add the new profile

        iface.connect(temp_profile)  # Connect to the network
        time.sleep(5)  # Wait for the connection to establish

        return iface.status() == pywifi.const.IFACE_CONNECTED

    def check_wifi_connection(self):
        wifi = pywifi.PyWiFi()  # Create a PyWiFi object
        iface = wifi.interfaces()[0]  # Get the first available network interface
        print(f" checking status  : { iface.status() == pywifi.const.IFACE_CONNECTED}")
        return iface.status() == pywifi.const.IFACE_CONNECTED
        
######## Thread Looping #############

    def stop_thread(self):
        timeOfRep = round( time.time() - self.time, 2)
        self.info.append((timeOfRep, "Stopping threads ..."))
        self.running = False

    def start_thread(self):

        connected = False
        while not connected:
            connected = self.connect_to_wifi()
            print("trying to connect to the Wifi...")
       
        print("Connected to the Esp Wifi")
                    # create a socket object for receiving data from the
            # wait for a client to connect
        while self.espIP is None:
            try:
                self.get_info= socket.socket()
                self.get_info.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.get_info.bind(('0.0.0.0', self.recv_port))  # bind to a local address and port
                self.get_info.settimeout(3.0)  # set a timeout of 10 seconds
                self.get_info.listen(0)  # start listening for incoming connections
                self.recv_socket, client_address = self.get_info.accept()
                self.get_info.close()
                self.espIP = client_address[0]
            except Exception as e:
                print(f"No information was sent by ESP, retrying... {e}")
                self.start_thread()


        print(f"Got a first answer from the ESP, ip :{self.espIP}")

        timeOfRep = round( time.time() - self.time, 2)
        self.info.append((timeOfRep, "Starting threads ..."))
        self.running = True
        connectLoop = threading.Thread(target=self.thread_connect) 
        listenLoop = threading.Thread(target=self._listen)
        pathLoop = threading.Thread(target=self._sendPath_Instruction)

        pathLoop.start()
        connectLoop.start()
        listenLoop.start()

    def thread_connect(self):
        while self.running:
            
            if not self.connected :
                timeOfRep = round( time.time() - self.time, 2)
                self.info.append((timeOfRep, "Connection Thread Reconnecting ..."))
                self.connected = False
                self._connect()
            threading.Event().wait(1)  # Wait for 1 seconds
        timeOfRep = round( time.time() - self.time, 2)
        self.info.append((timeOfRep, "Connection Thread Stopped"))

    def _listen(self):
        while self.running:
            if self.connected:
                try:
                    # Receive data from the client socket
                    data = self.recv_socket.recv(48)

                

                    if data:
                      
                        try :
                            data_decoded = struct.unpack('ffffffffffff', data)
                        except Exception as e:
                            print("Connection error :", e)
                            print(len(data))
                        # Use the data 
                        distanceFront = data_decoded[2]
                        distanceBack = data_decoded[3]
                        orientation = data_decoded[4]
                        self.slam_data.curr_x_car = data_decoded[5]
                        self.slam_data.curr_y_car = data_decoded[6]
                        timeOfReading = data_decoded[7]/10000
                        angleMap = data_decoded[8]
                        angleGyro = data_decoded[9]
                        angleKalman = data_decoded[10]
                        self.slam_data.perfect_orientation = data_decoded[11]

                        self.slam_data.add_orr(angleMap,angleGyro,angleKalman, timeOfReading)
                        timeOfRep = round( time.time() - self.time, 2)
                        self.recv_stat.append(timeOfRep)

                        # Filter invalid distances to 0, to allow negative distances
                        if (distanceFront == -1) :
                            distanceFront = 0
                        else :
                            distanceFront += 20
                            self.obs_stat.append(timeOfRep)

                        if (distanceBack == -1) :
                            distanceBack = 0
                        else :
                            distanceBack = -distanceBack - 20
                            self.obs_stat.append(timeOfRep)

                        # Adding obstacles with Front Lidar
                        self.slam_data.add_and_delete_obstacle(self.slam_data.curr_x_car,  self.slam_data.curr_y_car, distanceFront, orientation)

                        # Adding obstacles with Back Lidar
                        self.slam_data.add_and_delete_obstacle(self.slam_data.curr_x_car,  self.slam_data.curr_y_car, distanceBack, orientation)
                        

                
                       

                except Exception as e:
                         print("Connection error :", e)




        timeOfRep = round( time.time() - self.time, 2)
        self.info.append((timeOfRep, "Listen Thread stopped"))           

############ COMMUNICATION METHOD #############

    
    def _connect(self):
        try:
            # create a socket object for receiving data from the
            # wait for a client to connect

            timeOfRep = round( time.time() - self.time, 2)
        


            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.send_socket.settimeout(5)  # set a timeout of 2 seconds
            self.send_socket.connect((self.espIP, self.send_port))
            
            timeOfRep = round( time.time() - self.time, 2)
            self.info.append((timeOfRep, 'Send established successfully, connection established successfully')) 
    
            
            self.connected = True

        except Exception as e:
            print("Connection error :", e)
            print("Reconnecting ...")
            # Check connection status
            while not self.check_wifi_connection():
                self.connect_to_wifi()
                print("reconnecting to wifi")

            timeOfRep = round( time.time() - self.time, 2)
            self.errors.append((timeOfRep, e))
            threading.Event().wait(5)  

            self.connected = False
            

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
                self.connected =False
                self.errors.append((timeOfRep, e))
                return 400
                

            timeOfRep = round( time.time() - self.time, 2)
            self.send_stat.append(timeOfRep) # To make a graph about the number of packet send
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
        while self.running:
            if  self.connected :
                actionNumber = self.map_all()
                print(f"actionNumber : {actionNumber}")

                if actionNumber != -1 :
                    self._send_actionNumber(actionNumber[0])

            threading.Event().wait(5)  

        timeOfRep = round( time.time() - self.time, 2)
        self.info.append((timeOfRep, "Listen Thread stopped")) 
        


############ HELPER METHOD ############

    def _is_socket_alive(self):
        if self.send_socket is None: 
            return False
        err = self.send_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        return err == 0
    
    def map_all(self) :
            point_car = self.path_finder.car_to_grid((self.slam_data.curr_x_car, self.slam_data.curr_y_car))
            self.path_finder.generateGrid(self.slam_data.list_of_obs)
            self.path_finder.dijkstra_shortest_path(point_car)
            actionNumber = self.path_finder.path_to_actionNumber(int(self.slam_data.perfect_orientation))
            return actionNumber
    
