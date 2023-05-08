import esp32 as esp
import time


 # IP address and port number of the ESP32
recv_port = 8888
send_port = 8889

espPro = esp.ESP32Connection(send_port,recv_port)

espPro.start_thread()


    





