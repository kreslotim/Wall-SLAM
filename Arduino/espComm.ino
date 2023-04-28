#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

// SSID and password of Wifi connection:
const char* password = "0123456789";
const char* ssid = "espWifi2";

// Port to send data
const uint16_t sendDataPort = 8888;
const uint16_t recieveDataPort = 8889;

int numberOfConnectionOld = 0;

// Configure IP addresses of the local access point
IPAddress local_IP(192, 168, 1, 23);
IPAddress gateway(192, 168, 1, 5);
IPAddress subnet(255, 255, 255, 0);

//Open Wifi Port
WiFiServer sendServer(sendDataPort);
WiFiServer recieveServer(recieveDataPort);

//Open WifiClients
WiFiClient sendClient;
WiFiClient recieveClient;

void setup() {
  Serial.begin(115200);

  //SetUp Access Point
  WiFi.softAPConfig(local_IP, gateway, subnet);
  WiFi.softAP(ssid, password);
  Serial.print("IP address = ");
  Serial.println(WiFi.softAPIP());

  //Setup WifiServer
  sendServer.begin();
  recieveServer.begin();
}

void readData() {
  recieveClient = recieveServer.available();

  if (recieveClient) {
    Serial.println("New client connected (Recieve)");

    if (recieveClient.connected() && recieveClient.available()) {
      // Read the packed dataRecievd from the socket
      float dataRecievd[2];
      recieveClient.readBytes((char*)dataRecievd, sizeof(dataRecievd));

      // Unpack the dataRecievd
      float servoAngle = dataRecievd[0];
      float leftStepperMotor = dataRecievd[1];
      float rightStepperMotor = dataRecievd[2];

      // Do something with the decoded angles
      Serial.print("Received angles: ");
      Serial.print(servoAngle);
      Serial.print(", ");
      Serial.print(leftStepperMotor);
      Serial.print(", ");
      Serial.println(rightStepperMotor);

      // Send "200" back to the client
      recieveClient.println("200");
    }
  }
}

void sendData() {
  //if (sendClient.connect(local_IP, sendDataPort)) {
    Serial.print("Sending message");
    String message = "200";
    sendServer.println(message);
  //}
}

void numberConnected(){
  int numberOfConnection = WiFi.softAPgetStationNum();
  if(numberOfConnectionOld != numberOfConnection){
    Serial.print("Stations connected: ");
    Serial.println(numberOfConnection);
    numberOfConnectionOld =numberOfConnection;
  }
}

void loop() {

  //WifiServers and Client
  readData();
  sendData();
  numberConnected();

  delay(100);
}
