import esp32Connection as esp


 # IP address and port number of the ESP32
host = '192.168.28.79'
recv_port = 8090
send_port = 8091

esp = esp.ESP32Connection(host,send_port,recv_port)
esp.send_hello()
esp.listen()




