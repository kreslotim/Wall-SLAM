import socket
import time
import struct

class ESP32Connection:
    def __init__(self, send_port, recv_port):
        print("Establishing Connection")
        self.host = None
        self.send_port = send_port
        self.recv_port = recv_port
        self.send_socket = None
        self.recv_socket = None
        self.time = time.time()
        self._connect()

############ COMUNICATION METHOD #############
                
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
            
        except Exception as e:
            print("Connection error :", e)
            print("Reconnecting ...")
            time.sleep(1)


    def _listen(self):
        # Receive data from the client socket
        data = self.recv_socket.recv(48)
        data_decoded = struct.unpack('ffffffffffff', data)

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

            while (_is_socket_alive(self) and not response == "200") :
                response = self.send_socket.recv(1024).decode()   
                print("Received response from ESP32:", response)

            if not _is_socket_alive(self) :  
                print("Invalid response from ESP32, reconnecting...")
                self.recv_socket.close()
                self.send_socket.close()
                self._connect() 
                self._send_actionNumber(actionNumber)

        except Exception as e:
            print("Connection error :", e)


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
        err = self.send_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        return err == 0
