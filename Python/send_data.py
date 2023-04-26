import socket

HOST = "192.168.137.200"  # The server's hostname or IP address
PORT = 8888  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    #data = s.recv(1024)

#print(f"Received {data!r}")
