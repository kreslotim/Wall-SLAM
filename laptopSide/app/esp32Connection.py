import socket
import time
import struct

class ESP32Connection:
    def __init__(self, host, port):
        print("Establishing Connection")
        self.host = host
        self.port = port
        self.client = None
        self.connect()

    def connect(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
            print("Connection established successfully")
            return
        except Exception as e:
            print("Connection error :", e)
            print(" Reconnecting ...")
            time.sleep(1)
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
            else:
                print("Invalid response from ESP32, reconnecting...")
                self.connect()

        except Exception as e:
            print("Connection error :", e)
            self.connect()

    def setting(self, speed1, speed2, angle3):
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

        except Exception as e:
            print("Connection error :", e)
            self.connect()
