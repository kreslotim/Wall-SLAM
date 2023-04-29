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
  connect();
  recv();
  delay(500);
}

void recv(){
  if(recieve_client.available()){
    Serial.println(recieve_client.readString());
    recieve_client.print("200");
  }
}
void send(){
  while(send_client.connect(host, send_port)){
  send_client.print("Hello from ESP32!");
  if(send_client.readString() == "200") {
    Serial.println(" Got 200 back");
    break;
  }
  }
}

void connect(){
  if(!recieve_client.connected() ){
    disconnect();

    

    if (!send_client.connect(host, send_port)) {
          Serial.println("Send Socket failed !");
          return;
      }

    Serial.println("Send Socket connected !");
    
    delay(200);

    recieve_client = wifiServer.available();

    if (recieve_client.connected()) {

      Serial.print("Recieve Socket from IP:");
      Serial.println(recieve_client.remoteIP());
      
    
    } else {
      Serial.println("Recieve Socket fail!");

  }
  }
}


void disconnect(){

  Serial.println("Connection fail...");

  send_client.stop();
  recieve_client.stop();
  delay(2000);

}
