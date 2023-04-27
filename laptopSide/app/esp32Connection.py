import socket
import time
import struct

class ESP32Connection:
    def __init__(self, host, port):
        print("Establishing Connection")
        self.host = host
        self.port = port

        # IP address and port number of the ESP32
        host = '192.168.210.79'
        port = 8888

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        print("Connection successfully")
        
    def send_angles(self, angle1, angle2, angle3):
        # Encode the angles as floats and pack them into a binary format
        packed_angles = struct.pack('fff', angle1, angle2, angle3)

        # Send the packed angles over the socket
        self.client.sendall(packed_angles)

        # Wait for a response from the ESP32
        response = self.client.recv(1024).decode()
        print("Received response from ESP32:", response)


