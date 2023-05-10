import socket
import time
import struct
import threading
import math
import random



class ESP32Connection():
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
        self.start_thread()
    
######## Thread Looping #############

    def stop_thread(self):
        self.running = False

    def start_thread(self):
        self.running = True
        connectLoop = threading.Thread(target=self.thread_connect) 
        listenLoop = threading.Thread(target=self._listen)
        connectLoop.start()
        listenLoop.start()

    def thread_connect(self):
        while self.running:
            if not self._is_socket_alive():
                print("Thread reconnecting......")
                self._connect()
            time.sleep(1)
        print("Thread stopped")



############ COMUNICATION METHOD #############

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

    def _listen(self):
        if self.connected:
            # Receive data from the client socket
            data = self.recv_socket.recv(48)
            data_decoded = struct.unpack('ffffffffffff', data)
            print(data)

            if data:
                self.recv_socket.send("200".encode())
                self.recv_stat.append([1, time.time()-self.time])
                # Print the received data
                print(f"Received data: {data_decoded}")
 
    def _send_actionNumber(self, actionNumber):
        try:
            # Send the packed angles over the socket
            packed_angles = struct.pack('f', actionNumber)
            self.send_socket.sendall(packed_angles)
            print("Message sent")

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

        except Exception as e:
            print("Connection error :", e)
            
        timeav =  time.time()-self.time
        print(timeav)
        self.send_stat.append([1,timeav]) # To make a graph about the number of packet send


############ Moving METHOD ########

    def _sendStop(self):
        self._send_actionNumber(0)
    
    def _sendMove_Forward(self):
        self._send_actionNumber(1)
    
    def _sendMove_Backward(self):
        self._send_actionNumber(2)

    def _sendMove_Right(self):
        self._send_actionNumber(3)

    def _sendMove_Left(self):
        self._send_actionNumber(4)



############ HELPER METHOD ########

    def _is_socket_alive(self):
        if self.send_socket is None: 
            return False
        err = self.send_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        return err == 0
