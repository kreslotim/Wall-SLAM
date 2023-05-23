import socket
import time
import struct
import threading
import math
import random
import serial



class ESP32ConnectionBluetooth:
    def __init__(self, com_port, baud_port):
        print("Establishing Connection")

        self.serialBT = serial.Serial(com_port, baud_port, timeout=1)

        
        # Connection variable
        self.espIP = None
        self.hostName = socket.gethostname()
        self.hostIp = socket.gethostbyname(self.hostName) 
        self.connected = False
        self.send_socket = None
        self.recv_socket = None
        self.running = False

        self.actionNumber = 200

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
                self.serialBT.send(self.actionNumber.encode())
                self.actionNumber = 200

                # Receive data from the client socket
                data = self.serialBT.readline().decode().strip()
                if (data==200 or data==0 or data==1 or data==2 or data==3 or data==4):
                    return  
                
                data_decoded = struct.unpack('ffffffffffff', data)
                if data:

                    # TODO INACURATE. ESP OUTPUT UNCLEAR.
                    distanceFront = -data_decoded[2]
                    distanceBack = data_decoded[3]
                    orientation= data_decoded[4]
                    x_car = data_decoded[5]
                    y_car= data_decoded[6]
                    timeOfReading= data_decoded[7]
                   
                    print(data_decoded)
                    self.obstacle.append((timeOfReading,x_car,y_car,distanceFront,orientation))
                    self.obstacle.append((timeOfReading,x_car,y_car,distanceBack,orientation))
                    self.output.append((timeOfReading, 'Position ', x_car, y_car))  
                    self.output.append((timeOfReading, 'Obstacle found at ', distanceBack, ' mm, looking at ', orientation)) 
                    # Log it
                    timeOfRep = round(time.time() - self.time, 2)
        
                    #self.recv_stat.append([1, timeOfRep])

                    # Print the received data
                    print(f"Received data: {data_decoded}")

        timeOfRep = round( time.time() - self.time, 2)
        self.info.append((timeOfRep, "Listen Thread stopped"))           

############ COMMUNICATION METHOD #############

    def _connect(self):
        try:
            if self.serialBT.is_open:
                print("Serial port is connected")
                self.connected = True
            else:
                raise Exception("Serial port is not connected")



        except Exception as e:
            print("Connection error :", e)
            print("Reconnecting ...")
            timeOfRep = round( time.time() - self.time, 2)
            self.errors.append((timeOfRep, e))

            self.connected = False
            time.sleep(1)

############ ESP DIRECT COMMAND METHOD ############

    def _sendStop(self):
        self.actionNumber = 0

    def _sendMove_Forward(self):
        self.actionNumber = 1
 
    def _sendMove_Backward(self):
        self.actionNumber = 2

    def _sendMove_Right(self):
        self.actionNumber = 3

    def _sendMove_Left(self):
        self.actionNumber = 4

############ HELPER METHOD ############

    def _is_socket_alive(self):
        if self.send_socket is None: 
            return False
        err = self.send_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        return err == 0
    

