import socket
import time
import struct
import math


def encode_angles(angle1, angle2, angle3):

    # Combine the scaled angles into a 24-bit integer
    encoded = (angle1 << 16) | (angle2 << 8) | angle3

    return encoded


# IP address and port number of the ESP32
host = '192.168.210.79'
port = 8888

# Create a TCP client socket and connect to the ESP32
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

while True:
    # Send a message to the ESP32
    # Encode the angles as floats and pack them into a binary format
    angle1 = 45.9  # in degrees
    angle2 = 90.5  # in degrees
    angle3 = 180.2  # in degrees

    packed_angles = struct.pack('fff', angle1, angle2,angle3)

    # Send the packed angles over the socket
    client.sendall(packed_angles)


    # Wait for a response from the ESP32
    response = client.recv(1024).decode()
    print("Received response from ESP32:", response)

    time.sleep(1)



