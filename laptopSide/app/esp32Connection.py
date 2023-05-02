import socket
import time
import struct
import threading
import math

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

                
    def _connect(self):
        print(" Connecting...")
        try:
            # create a socket object for receiving data from the client
            recv_socket = socket.socket()
            recv_socket.bind(('0.0.0.0', self.recv_port))  # bind to a local address and port
            recv_socket.listen()  # start listening for incoming connections

            # wait for a client to connect
            self.recv_socket, client_address = recv_socket.accept()


            print('Recv established successfully by', client_address)
            self.host = client_address[0]

            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.send_socket.connect((self.host, self.send_port))
            print("Connection established successfully")
            
            self.connected = True

        except Exception as e:
            print("Connection error :", e)
            print("Reconnecting ...")
            self.connected = False
            time.sleep(1)



############ COMUNICATION METHOD #############

    def _listen(self):
        # Receive data from the client socket
        data = self.recv_socket.recv(48)
        data_decoded = struct.unpack('ffffffffffff', data)

        if data:
            self.recv_socket.send("200".encode())
            self.recv_stat.append([1, time.time()-self.time])
            # Print the received data
            print(f"Received data: {data_decoded}")


    def _send_hello(self):
        try:
            # Send the packed angles over the socket
            packed_angles = struct.pack('fff', 2, 3, 4)
            self.send_socket.sendall(packed_angles)
            print("Send Message")

            # Wait for a response from the ESP32
            response = 0

            while (_is_socket_alive(self) and not response == "200") :
                response = self.send_socket.recv(1024).decode()   
                print("Received response from ESP32:", response)

            if not _is_socket_alive(self) :  
                print("Invalid response from ESP32, reconnecting...")
                self.recv_socket.close()
                self.send_socket.close()
                self._connect() 
                self._send_hello()

                

        except Exception as e:
            print("Connection error :", e)
            self.connected = False

############ HELPER METHOD ########

def _is_socket_alive(self):
        err = self.send_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        return err == 0
