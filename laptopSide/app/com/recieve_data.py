import socket

# IP address and port number of the WiFi access point
HOST = "192.168.210.79"
print(HOST)
PORT = 8888

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a specific IP address and port number
s.bind((HOST, PORT))

# listen for incoming connections
s.listen()

while True:
    # accept incoming connection
    conn, addr = s.accept()
    # Receive data from the client
    data = conn.recv(1024)
    # Print the received data
    print(data.decode())
    print("test2")

# Close the connection
conn.close()
