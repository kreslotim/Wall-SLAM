#include <WiFi.h>

const char* ssid = "OccuPi";
const char* password = "rkuf4617Qwe12$ReD";

const uint16_t send_port = 8090;
const uint16_t recv_port = 8091;
const char * host = "192.168.28.39";
WiFiServer wifiServer(recv_port);

WiFiClient recieve_client;
WiFiClient send_client;

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP: ");
  Serial.println(WiFi.localIP());
  wifiServer.begin();


}


void loop() {
  recv();
  send();


  delay(1000);
}

void recv(){
  recieve_client = wifiServer.available();

  if (recieve_client) {

    Serial.print("Client connected with IP:");
    Serial.println(recieve_client.remoteIP());
    Serial.println("Recv Disconnecting...");
    recieve_client.stop();
  }
}

void send(){
  if (!send_client.connect(host, send_port)) {

        Serial.println("Connection to host failed");

        delay(1000);
        return;
    }

  Serial.println("Connected to server successful!");

  send_client.print("Hello from ESP32!");

  Serial.println("Sent Disconnecting...");
  send_client.stop();
}

void loop1() {
     /*
  if (send_socket.connected()) {
    if (send_socket.available()) {

   
      // Read the packed angles from the socket
      float answer[4];
      send_socket.readBytes((char*)answer, sizeof(answer));
      
      switch(answer[0]){

        case 0: // Set up phase
          break;
        case 1:  // Motors Angle
          motorCom()
          break;
        case 2:
          break;  // Motors Speed
      }

      // Send "200" back to the client
      send_socket.println("200");
      

    }

    String message = Serial.readStringUntil('\n');
    Serial.print("Sending message to Python: ");
    Serial.println(message);

    // Send the message to Python
    send_socket.println(message);

  }
  else {
    send_socket = server.available();
  }
  delay(100);
  */
}

void motorCom(){

  /*
  // Unpack the angles
  float angle1_deg = answer[0];
  float angle2_deg = answer[1];
  float angle3_deg = answer[2];

  // Do something with the decoded angles
  Serial.print("Received angles: ");
  Serial.print(angle1_deg);
  Serial.print(", ");
  Serial.print(angle2_deg);
  Serial.print(", ");
  Serial.println(angle3_deg);
  */


}
