#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include <NewPing.h>
#include <ESP32Servo.h>
#include "Adafruit_VL53L1X.h"
#include <Adafruit_FXAS21002C.h>
#include <Adafruit_FXOS8700.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <AccelStepper.h>

const int maxDistanceSonar = 400;  // in cm
int distanceSonarFront = 0;
int16_t lidarDistance;
float dataSend[12];
const unsigned long interval = 10;
unsigned long previousMillis = 0;
#define FULLSTEP 4
#define HALFSTEP 8
sensors_event_t event;
sensors_event_t aevent, mevent;

// Define acceleration and maximum speed values
const float acceleration = 250.0;
const float maxSpeed = 2000;
const float constSpeed = 1000;
const int STEPS_PER_REV = 2038;
const int STEPS_90_DEG = 1740;

// FrontUtlrasonic settings
#define trigPinFront 12
#define echoPinFront 14
NewPing frontUltrasonic(trigPinFront, echoPinFront, maxDistanceSonar);

// VL53L1X Lidar
#define IRQ_PIN 2
#define XSHUT_PIN 3
Adafruit_VL53L1X vl53 = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);
const int16_t minLidarDistance = 150;  // in mm 

// Servo settings
#define servoPin 16
Servo servo;
const int servoInitPos = 84;
int servoAngle = servoInitPos;
int direction = 1;

// Gyro Accel Mag (GAM)
#define SDA_2 26                                            // New I2C Data Pin
#define SCL_2 27                                            // New I2C Clock Pin
Adafruit_FXAS21002C gyro = Adafruit_FXAS21002C(0x0021002C); /* Assign a unique ID to the sensors at the same time */
Adafruit_FXOS8700 accelmag = Adafruit_FXOS8700(0x8700A, 0x8700B);

// Left Motor
#define lIN1 2
#define lIN2 0
#define lIN3 4
#define lIN4 16

// Right Motor
#define rIN1 17
#define rIN2 5
#define rIN3 18
#define rIN4 19

// Creates two instances of Stepper Motors
AccelStepper stepperLeft(FULLSTEP, lIN1, lIN3, lIN2, lIN4);
AccelStepper stepperRight(FULLSTEP, rIN1, rIN3, rIN2, rIN4);

// SSID and password of Wifi connection:
const char* password = "0123456789";
const char* ssid = "espWifi2";

// Port to send data
const uint16_t sendDataPort = 8888;
const uint16_t recieveDataPort = 8889;

//Open Wifi Port
WiFiServer sendServer(sendDataPort);
WiFiServer recieveServer(recieveDataPort);

//Open WifiClients
WiFiClient sendClient;
WiFiClient recieveClient;

int numberOfConnectionOld = 0;

// Configure IP addresses of the local access point
IPAddress local_IP(192, 168, 1, 22);
IPAddress user_IP(192, 168, 1, 23);

IPAddress gateway(192, 168, 1, 5);
IPAddress subnet(255, 255, 255, 0);

void setup() {
  Serial.begin(115200);

  // Access Point SetUp
  WiFi.softAPConfig(local_IP, gateway, subnet);
  WiFi.softAP(ssid, password);
  Serial.print("IP address = ");
  Serial.println(WiFi.softAPIP());

  // WifiServer Setup
  sendServer.begin();
  Serial.print("Sending Port is open at : ");
  Serial.println(sendDataPort);

  recieveServer.begin();
  Serial.print("Recieving Port is open at : ");
  Serial.println(recieveDataPort);

  // Servo Setup
  servo.attach(servoPin);
  servo.write(servoInitPos);  // Put servo to initial position (looking forward)

   // Gyro Accel Mag (GAM) Setup
  setupGAM();

  // Lidar Setup
  setupLidar();

  // Motors Setup
  stepperLeft.setMaxSpeed(maxSpeed);
  stepperLeft.setAcceleration(acceleration);
  stepperRight.setMaxSpeed(maxSpeed);
  stepperRight.setAcceleration(acceleration);

}

void setupLidar() {
  //Serial.begin(115200);
  while (!Serial) delay(10);

  Serial.println(F("Adafruit VL53L1X sensor demo"));

  Wire.begin();
  if (!vl53.begin(0x29, &Wire)) {
    Serial.print(F("Error on init of VL sensor: "));
    Serial.println(vl53.vl_status);
    while (1) delay(10);
  }
  Serial.println(F("VL53L1X sensor OK!"));

  Serial.print(F("Sensor ID: 0x"));
  Serial.println(vl53.sensorID(), HEX);

  if (!vl53.startRanging()) {
    Serial.print(F("Couldn't start ranging: "));
    Serial.println(vl53.vl_status);
    while (1) delay(10);
  }
  Serial.println(F("Ranging started"));

  // Valid timing budgets: 15, 20, 33, 50, 100, 200 and 500ms!
  vl53.setTimingBudget(50);
  Serial.print(F("Timing budget (ms): "));
  Serial.println(vl53.getTimingBudget());

  /*
  vl.VL53L1X_SetDistanceThreshold(100, 300, 3, 1);
  vl.VL53L1X_SetInterruptPolarity(0);
  */
}

void setupGAM() {
  Wire1.begin(SDA_2, SCL_2);

  Serial.println("Gyroscope Accel Mag Test");
  Serial.println("");

  /* Initialise the sensor */
  if (!gyro.begin(0x21, &Wire1)) {
    /* There was a problem detecting the FXAS21002C ... check your connections
     */
    Serial.println("Ooops, no FXAS21002C detected ... Check your wiring!");
    while (1)
      ;
  }

  if (!accelmag.begin(0x1F, &Wire1)) {
    /* There was a problem detecting the FXOS8700 ... check your connections */
    Serial.println("Ooops, no FXOS8700 detected ... Check your wiring!");
    while (1)
      ;
  }
}

void readLidar() {
  if (vl53.dataReady()) {
    // new measurement for the taking!
    lidarDistance = vl53.distance();
  }
}

void readData() {
  if(!recieveClient.connected()){
    Serial.println("No client connected (Recieve)");
    recieveClient = recieveServer.available();
  } else {
      Serial.println("New client connected (Recieve)");
    if (recieveClient.connected() && recieveClient.available()) {
      // Read the packed dataRecievd from the socket
      float dataRecievd[3];
      recieveClient.read((byte*)dataRecievd, sizeof(dataRecievd));

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
      recieveClient.flush();
      recieveClient.write("200");
    }
  } 
}

void sendData() { 
  packData();

  if (!sendClient.connected() && sendClient.connect(user_IP, sendDataPort)) {
    Serial.println("Connected to server");
  } 

  if (sendClient.connected()) {
    sendClient.flush();
    sendClient.write((byte*)dataSend, sizeof(dataSend));
  }
}

void action(int actionNumber) { 
  
}

void updateSensors() {
  // Ultrasonic Update
  distanceSonarFront = frontUltrasonic.ping_cm();

  // Lidar Update
  readLidar();

  // IMU Update
  gyro.getEvent(&event);
  accelmag.getEvent(&aevent, &mevent);
}

void packData(){
  updateSensors();
  dataSend[0] = servo.read();
  dataSend[1] = distanceSonarFront;
  dataSend[2] = lidarDistance;
  dataSend[3] = event.gyro.x;
  dataSend[4] = event.gyro.y;
  dataSend[5] = event.gyro.z;
  dataSend[6] = aevent.acceleration.x;
  dataSend[7] = aevent.acceleration.y;
  dataSend[8] = aevent.acceleration.z;
  dataSend[9] = mevent.magnetic.x;
  dataSend[10] = mevent.magnetic.y;
  dataSend[11] = mevent.magnetic.z;
}

void numberConnected() {
  int numberOfConnection = WiFi.softAPgetStationNum();
  if (numberOfConnectionOld != numberOfConnection) {
    Serial.print("Stations connected: ");
    Serial.println(numberOfConnection);
    numberOfConnectionOld = numberOfConnection;
  }
}

void loop() {
  // WifiServers
  sendData();
  readData();

  // Updates everytime someone connects or disconnects from WiFi
  numberConnected();

  delay(10);
}
