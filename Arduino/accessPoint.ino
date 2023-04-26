#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

// SSID and password of Wifi connection:
const char* password = "0123456789";
const char* ssid = "test";

// Port to send data
const uint16_t sendDataPort = 8888;

// Configure IP addresses of the local access point
IPAddress local_IP(192, 168, 1, 22);
IPAddress gateway(192, 168, 1, 5);
IPAddress subnet(255, 255, 255, 0);

String webpage = "<!DOCTYPE html><html><head><title>Test</title></head></html>";

const char* htmlWeb = R"html(
  <!DOCTYPE html>
  <html>
  <head>
  <title>Slider Control</title>
  <style>
      .slider1 {
        -webkit-appearance: none;
        width: 200px;
        height: 20px;
        border-radius: 10px;
        background-color: #ddd;
        margin: 100px;
        outline: none;
      }
      .slider2 {
        -webkit-appearance: none;
        width: 200px;
        height: 20px;
        border-radius: 10px;
        background-color: #ddd;
        margin: 100px;
        outline: none;
        transform: rotate(-90deg);
      }

      .slider1-horizontal::-webkit-slider-thumb {
        -webkit-appearance: none;
        width: 30px;
        height: 30px;
        background-color: #fff;
        border-radius: 50%;
        border: 3px solid #000;
        box-shadow: 0px 0px 8px 1px rgba(0, 0, 0, 0.5);
        margin-top: -5px;
      }


      .slider2-vertical::-webkit-slider-thumb {
        -webkit-appearance: none;
        width: 30px;
        height: 30px;
        background-color: #fff;
        border-radius: 50%;
        border: 3px solid #000;
        box-shadow: 0px 0px 8px 1px rgba(0, 0, 0, 0.5);
        margin-top: -5px;
      }

        .reset-button {
        background-color: red;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 15px;
        font-size: 16px;
        margin: auto;
        margin-left: 40px;
        cursor: pointer;
      }
        .auto-button {
        background-color: blue;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 15px;
        font-size: 16px;
        margin: auto;
        margin-left: 40px;
        cursor: pointer;
      }
    </style>
  </head>
  <body>
    <div style="display: flex">
      <h1 style="margin: 30px">Car Control</h1>
      <button  class="reset-button" id="reset-button">RESET</button>
      <button  class="auto-button" id="auto-button">Auto</button>
    </div>
    <div style="display: flex;">
      <div >
        <input type="range" min="-100" max="100" step="25" value="0" class="slider1 slider-horizontal" id="slider1">
        <p style="text-align: center">Servo Control Value: <span id="value1">0</span>%</p>
      </div>
    <div>
      <input type="range" min="-100" max="100" step="25" value="0" class="slider2 slider-vertical" id="slider2">
      <p style="text-align: center">Speed Slider Value: <span id="value2">0</span>%</p>
    </div>
  </div>
  <script>
    var slider1 = document.getElementById("slider1");
    var value1 = document.getElementById("value1");
    var slider2 = document.getElementById("slider2");
    var value2 = document.getElementById("value2");
    var resetButton = document.getElementById("reset-button");
   var autoButton = document.getElementById("auto-button");
 

slider1.oninput = function() {
  value1.innerHTML = this.value;
  fetch("/moveServo?val=" + slider1.value);

};

slider2.oninput = function() {
  value2.innerHTML = this.value;
  fetch("/moveStepper?val=" + slider2.value);
};

resetButton.onclick = function() {
  slider1.value = 0;
  slider2.value = 0;
  value1.innerHTML = 0;
  value2.innerHTML = 0;
  fetch("/reset");
};
autoButton.onclick = function() {
  slider1.value = 0;
  slider2.value = 0;
  value1.innerHTML = 0;
  value2.innerHTML = 0;
  fetch("/auto");
};
</script>
</body>
</html>)html";

WiFiServer sendServer(sendDataPort);
WebServer server(80);
//WebSocketsServer webSocket = WebSocketsServer(81);

void setup() {
  Serial.begin(115200);

  WiFi.softAPConfig(local_IP, gateway, subnet);
  WiFi.softAP(ssid, password);

  Serial.print("IP address = ");
  Serial.println(WiFi.softAPIP());

  server.on("/", HTTP_GET,  []() {
    server.send(200, "text/html", htmlWeb);
  });
  server.begin();
}

void loop() {
  server.handleClient();

  WiFiClient client = sendServer.available();
  if (client) {
    client.write("Hello, world!");
    //client.stop();
  }
      
}
