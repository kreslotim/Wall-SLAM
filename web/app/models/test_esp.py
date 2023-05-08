import socket
import time
import struct
import threading
import math
import random

class ESP32Connection:
    def __init__(self, send_port, recv_port):
        print("Establishing Connection")
        self.host = None
        self.connected = False
        self.send_port = send_port
        self.recv_port = recv_port
        self.send_socket = None
        self.recv_socket = None
        self.recv_stat = []
        self.send_stat = []
        self.obstacle = {}
        self.time = time.time()
        self.running = False
    
    def stop_thread(self):
        self.running = False

    def start_thread(self):
        self._connect()

        while not self.connected:
            time.sleep(1)
            print("waiting...")

        self.running = True
        connectLoop = threading.Thread(target=self.thread_connect)
        listenLoop = threading.Thread(target=self._listen)
        connectLoop.start()
        listenLoop.start()

    def thread_connect(self):
 
        while self.running:
            if not self._connected():
                print("Thread reconnecting......")
                self._connect()
            time.sleep(1)
        print("Thread stopped")

    def _connected(self):
        err1 = self.send_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        err2 = self.recv_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)

        if err1 == 0 and err2==0:
            self.connected=True
            return True
        else:
            return False
          
    def _connect(self):
        print(" Connecting...")
        try:
            # create a socket object for receiving data from the client
            recv_socket = socket.socket()
            recv_socket.bind(('0.0.0.0', self.recv_port))  # bind to a local address and port
            recv_socket.listen(0)  # start listening for incoming connections

            # wait for a client to connect
            self.recv_socket, client_address = recv_socket.accept()
            print('Recv established successfully by', client_address)
            recv_socket.close()
            self.host = client_address[0]

            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.send_socket.connect((self.host, self.send_port))
            print("Send established successfully")

            print("Connection established successfully")
            
            self.connected = True

        except Exception as e:
            print("Connection error :", e)
            print("Reconnecting ...")
            self.connected = False
            time.sleep(1)



############ COMUNICATION METHOD #############

    def _listen(self):
         while self.running :
            if self._connected():
                # Receive data from the client socket
                data = self.recv_socket.recv(48)
                if data:
                    self.recv_socket.send("200".encode())
                    self.recv_stat.append([1, time.time()-self.time])
                    # Print the received data

                    data_decoded = struct.unpack('ffffffffffff', data)
                    print(f"Received data: {data_decoded}")
            else :
                time.sleep(1)

    def _send_hello(self):
        try:
            # Send the packed angles over the socket
            self.send_socket.sendall("hello".encode())

            time.sleep(1)
            # Wait for a response from the ESP32
            response = self.send_socket.recv(1024).decode()   

            if response == "200" :
                print("Received response from ESP32:", response)
                timeav =  time.time()-self.time
                print(timeav)
                self.send_stat.append([1,timeav]) # To make a graph about the number of packet send
            else:
                print("Invalid response from ESP32, reconnecting...")
                    
                self.send_socket.close()
                self.recv_socket.close()
                self.connected= False
            

        except Exception as e:
            print("Connection error :", e)
            self.connected = False

############ HELPER METHOD ########

    def _dataToObstacle(self,x_car,y_car, distance,orientation):    
        # Calculate the x and y coordinates of the obstacle
        orientation = math.radians(orientation)
        point_x = x_car + distance * math.cos(orientation)
        point_y = y_car + distance * math.sin(orientation)
        obstacle_position = (point_x, point_y)
        
        # Check if the obstacle position is already in the dictionary
        if obstacle_position in self.obstacles:
            self.obstacles[obstacle_position].add((x_car, y_car))
        else:
            self.obstacles[obstacle_position] = {(x_car, y_car)}
    
    def _randomlyFill(self):
        # Generate random car position within range (-100, 100)
        x_car = random.uniform(-100, 100)
        y_car = random.uniform(-100, 100)
        num_obstacles = random.uniform(0,5)
        # Generate random obstacles and add them to the obstacle map
        for i in range(num_obstacles):
            # Generate random obstacle position within range (-100, 100)
            x_obstacle = random.uniform(-100, 100)
            y_obstacle = random.uniform(-100, 100)

            # Calculate distance and orientation between car position and obstacle position
            distance =  random.uniform(0, 3)
            orientation = random.uniform(0,180)

            # Add obstacle to the obstacle map
            self._dataToObstacle(x_car,y_car,distance,orientation)

