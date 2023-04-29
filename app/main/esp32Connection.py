import socket
import time
import struct

class ESP32Connection:
    def __init__(self, send_port,recv_port):
        print("Establishing Connection")
        self.host = None
        self.send_port = send_port
        self.recv_port=recv_port
        self.send_socket  = None
        self.recv_socket = None
        self.connect()
        self.recv_stat = []
        self.send_stat = []
        self.time = time.time()

    def connect(self):
        try:

            # create a socket object for receiving data from the client
            recv_socket = socket.socket()
            recv_socket.bind(('0.0.0.0', 8090 ))  # bind to a local address and port
            recv_socket.listen(0)  # start listening for incoming connections
            
            #wait for a client to connect
            self.recv_socket, client_address = recv_socket.accept()
            print('Recv established successfully by', client_address)
            recv_socket.close()
            self.host = client_address[0]

            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.send_socket.connect((self.host, self.send_port))
            print("Send established successfully")
        

            print("Connection established successfully")
            return
        except Exception as e:
            print("Connection error :", e)
            print(" Reconnecting ...")
            time.sleep(1)
            self.connect()

    def listen(self):
        # Receive data from the client socket
        data = self.recv_socket.recv(1024)
        if data:
            self.recv_socket.send("200".encode())
            self.recv_stat.append([1,time.time()-self.time])
            # Print the received data
            print(f"Received data: {data}")

    def send_hello(self):
        try:
            # Send the packed angles over the socket
            self.send_socket.sendall("hello".encode())

            # Wait for a response from the ESP32
            response = self.send_socket.recv(1024).decode()            
            if response == "200":
                print("Received response from ESP32:", response)
                timeav =  time.time()-self.time
                print(timeav)
                self.send_stat.append([1,timeav]) # To make a graph about the number of packet send
            else:
                print("Invalid response from ESP32, reconnecting...")
                    
                self.send_socket.close()
                self.recv_socket.close()
                self.connect()
                self.send_hello()

        except Exception as e:
            print("Connection error :", e)
            self.connect()

    
    def send_angles(self, angle1, angle2, angle3):
        # Encode the angles as floats and pack them into a binary format
        packed_angles = struct.pack('fff', angle1, angle2, angle3)

    
        try:
            # Send the packed angles over the socket
            self.client.sendall(packed_angles)

            # Wait for a response from the ESP32
            response = self.client.recv(1024).decode()
            
            if response == "200":
                print("Received response from ESP32:", response)
                self.send_stat.append([1, time.time()-self.time]) # To make a graph about the number of packet send
            else:
                print("Invalid response from ESP32, reconnecting...")
                self.connect()
                self.send_angles(angle1,angle2,angle3)

        except Exception as e:
            print("Connection error :", e)
            self.connect()

    def setting(self, speed1, speed2):
        # Encode the angles as floats and pack them into a binary format
        packed_setting = struct.pack('fff', speed1, speed2)

        try:
            # Send the packed angles over the socket
            self.client.sendall(packed_setting)

            # Wait for a response from the ESP32
            response = self.client.recv(1024).decode()

            if response == "200":
                print("Received response from ESP32:", response)
      
            else:
                print("Invalid response from ESP32, reconnecting...")
                self.connect()
                self.setting(self,speed1,speed2)

        except Exception as e:
            print("Connection error :", e)
            self.connect()
