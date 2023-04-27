import esp32Connection as esp


 # IP address and port number of the ESP32
host = '192.168.210.79'
port = 8888

esp = esp.ESP32Connection(host,port)
esp.send_angles(20.4,10.2,10)



