#include <WiFi.h>

const char* ssid = "OccuPi";
const char* password = "rkuf4617Qwe12$ReD";

const uint16_t port = 8888;
const char * host = "192.168.210.39";
WiFiServer server(port);
WiFiClient client;

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

  server.begin();
  Serial.println("Server started");
}

void loop() {
  if (client.connected()) {
    if (client.available()) {
      // Read the packed angles from the socket
      float angles[3];
      client.readBytes((char*)angles, sizeof(angles));

      // Unpack the angles
      float angle1_deg = angles[0];
      float angle2_deg = angles[1];
      float angle3_deg = angles[2];

      // Do something with the decoded angles
      Serial.print("Received angles: ");
      Serial.print(angle1_deg);
      Serial.print(", ");
      Serial.println(angle2_deg);
      Serial.print(", ");
      Serial.print(angle3_deg);
    
    }
  }
  else {
    client = server.available();
  }

  if (Serial.available()) {
    String message = Serial.readStringUntil('\n');
    Serial.print("Sending message to Python: ");
    Serial.println(message);

    // Send the message to Python
    client.println(message);
  }
  delay(100);
}



