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
#include <WiFiUdp.h>


TaskHandle_t Task1;

sensors_event_t event;
sensors_event_t aevent, mevent;
int distanceSonarFront = 0;
int16_t lidarDistanceFront;
int16_t lidarDistanceBack;
const short POINTS_PER_PACKET = 20;
short point = 0;
float dataSend[12 * POINTS_PER_PACKET];
int servoAngle=1;
int numberOfConnectionOld = 0;
float actionNumber = 0;
float orientation = 0;
int goToOrientation = 0;

float curr_x = 0;
float curr_y = 0;

float prev_x = 0;
float prev_y = 0;

unsigned long startTime; // Variable to store the start time
unsigned long elapsedTime;
int direction = 1;

const float ACCELERATION_STEPPER = 250.0;
const float MAX_SPEED_STEPPER = 2000;
const float CONST_SPEED_STEPPER = 500;
const int STEPS_PER_REV = 2038;
const int STEPS_90_DEG = 1740;
const int16_t MIN_LIDAR_DISTANCE = 150;  // in mm
const int16_t MIN_SONAR_DISTANCE = 40;  // in mm (in cm but we x10 the distance)
const int SERVO_INIT_POS = 84;
const int MAX_DISTANCE_SONAR = 400;
const float DIST_PER_STEP = 0.06;  // in mm per step

const float STM_Err = 0.0000612825;


#define FULLSTEP 4
#define HALFSTEP 8

// FrontUtlrasonic settings
#define TRIG_PIN 12
#define ECHO_PIN 14

// VL53L1X Lidar
#define IRQ_PIN 2
#define XSHUT_PIN 3

// Servo settings
#define servoPin 15

// Pins for Front lidar
#define SDA_1 26
#define SCL_1 27

// Pins for left motor
#define L_IN1 2
#define L_IN2 23
#define L_IN3 4
#define L_IN4 16

// Pins for right motor
#define R_IN1 17
#define R_IN2 5
#define R_IN3 18
#define R_IN4 19

// Create instance of Servo
Servo servo;

// Create instance of Lidar
Adafruit_VL53L1X vl53Front = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);
Adafruit_VL53L1X vl53Back = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);

// Create intance of Gyro, Accel and Mag
Adafruit_FXAS21002C gyro = Adafruit_FXAS21002C(0x0021002C);
Adafruit_FXOS8700 accelmag = Adafruit_FXOS8700(0x8700A, 0x8700B);

// Create instance of ultrasonic
NewPing frontUltrasonic(TRIG_PIN, ECHO_PIN, MAX_DISTANCE_SONAR);

// Create instances of stepper motors
AccelStepper stepperLeft(FULLSTEP, L_IN1, L_IN3, L_IN2, L_IN4);
AccelStepper stepperRight(FULLSTEP, R_IN1, R_IN3, R_IN2, R_IN4);

// SSID and password of Wifi connection:
const char* password = "0123456789A";
const char* ssid = "espWifi2";

// Port to send data
const uint16_t SEND_DATA_PORT = 8888;
const uint16_t RECIEVE_DATA_PORT = 8889;

//Open Wifi Port
WiFiServer sendServer(SEND_DATA_PORT);
WiFiServer recieveServer(RECIEVE_DATA_PORT);

//Open WifiClients
WiFiClient sendClient;
WiFiClient recieveClient;

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
  Serial.println(SEND_DATA_PORT);

  recieveServer.begin();
  Serial.print("Recieving Port is open at : ");
  Serial.println(RECIEVE_DATA_PORT);

  // Servo Setup
  servo.attach(servoPin);
  servo.write(SERVO_INIT_POS);  // Put servo to initial position (looking forward)

  // Setup Front/Back lidars and IMU
  setupLidarsAndIMU();

  // Motors Setup
  stepperLeft.setMaxSpeed(MAX_SPEED_STEPPER);
  stepperLeft.setAcceleration(ACCELERATION_STEPPER);
  stepperRight.setMaxSpeed(MAX_SPEED_STEPPER);
  stepperRight.setAcceleration(ACCELERATION_STEPPER);

  // Setup core to Move
  xTaskCreatePinnedToCore(
    Task1code, /* Task function. */
    "Task1",   /* name of task. */
    10000,     /* Stack size of task */
    NULL,      /* parameter of the task */
    1,         /* priority of the task */
    &Task1,    /* Task handle to keep track of created task */
    1);        /* pin task to core 0 */
  delay(500);

  // Setup Timer
  startTime = millis(); // Record the start time
}

void setupLidarsAndIMU() {
  while (!Serial) delay(10);

  Wire.begin();

  Wire1.begin(SDA_1,SCL_1);

  /* Initialise the sensor */
  if (!gyro.begin(0x21, &Wire)) {
    /* There was a problem detecting the FXAS21002C ... check your connections
     */
    Serial.println("Ooops, no FXAS21002C detected ... Check your wiring!");
    while (1)
      ;
  }
  if (!accelmag.begin(0x1F, &Wire)) {
    /* There was a problem detecting the FXOS8700 ... check your connections */
    Serial.println("Ooops, no FXOS8700 detected ... Check your wiring!");
    while (1)
      ;
  }

  if (! vl53Front.begin(0x29, &Wire1)) {
    Serial.print(F("Error on init of Front VL sensor: "));
    Serial.println(vl53Front.vl_status);
    while (1)       delay(10);
  }
  if (! vl53Back.begin(0x29, &Wire)) {
    Serial.print(F("Error on init of Back VL sensor: "));
    Serial.println(vl53Back.vl_status);
    while (1)       delay(10);
  }
  Serial.println(F("VL53L1X sensor OK!"));

  Serial.print(F("Sensor ID: 0x"));
  Serial.println(vl53Front.sensorID(), HEX);

  if (! vl53Front.startRanging()) {
    Serial.print(F("Front lidar Couldn't start ranging: "));
    Serial.println(vl53Front.vl_status);
    while (1)       delay(10);
  }
  if (! vl53Back.startRanging()) {
    Serial.print(F("Back lidar Couldn't start ranging: "));
    Serial.println(vl53Back.vl_status);
    while (1)       delay(10);
  }
  Serial.println(F("Ranging started"));

  // Valid timing budgets: 15, 20, 33, 50, 100, 200 and 500ms!
  vl53Front.setTimingBudget(50);
  Serial.print(F("Timing budget (ms): "));
  Serial.println(vl53Front.getTimingBudget());
}


void readLidar() {
  if (vl53Front.dataReady()) {
    lidarDistanceFront = vl53Front.distance();
  } else {
    lidarDistanceFront = -1;
  }

  if (vl53Back.dataReady()) {
    lidarDistanceBack = vl53Back.distance();
  } else {
    lidarDistanceBack = -1;
  }
}

void readData() {
  if (!recieveClient.connected()) {
    Serial.println("No client connected (Recieve)");
    recieveClient = recieveServer.available();
  } else {
    Serial.println("New client connected (Recieve)");
    if (recieveClient.connected() && recieveClient.available()) {
      // Read the packed dataRecieved from the socket
      float dataRecieved[1];
      recieveClient.read((byte*)dataRecieved, sizeof(dataRecieved));

      // Unpack the dataRecieved
      actionNumber = dataRecieved[0];

      // Do something with the decoded angles
      Serial.print("Action recieved: ");
      Serial.print(actionNumber);

      //action(actionNumber);
      // Send "200" back to the client
      recieveClient.write("200");
    }
  }
}

void sendData() {
  if (!sendClient.connected()){
    if(sendClient.connect(user_IP, SEND_DATA_PORT)) {
      Serial.println("Connected to server");
    } else{
      Serial.println("Non connection");
    }
  } else {
    sendClient.flush();
    sendClient.write((byte*)dataSend, sizeof(dataSend));
    Serial.println("Data Sent");
    point = 0;
  }
}

void handleOutgoingData(){
  if(point != POINTS_PER_PACKET){
    packData();
    return;
  }else{
    sendData();
  }
}

void updateSensors() {
  // Ultrasonic Update
  distanceSonarFront = frontUltrasonic.ping_cm() * 10;

  // Lidar Update
  rotateServo();
  readLidar();

  // IMU Update
  gyro.getEvent(&event);
  accelmag.getEvent(&aevent, &mevent);

  // Orientation Update
  orientation = atan2(mevent.magnetic.y, mevent.magnetic.x) * 180 / PI;

  //Update Timer
  elapsedTime = (float)(millis() - startTime);
}

void updatePosition(){
  float distance =  0.001* STM_Err * stepperRight.currentPosition();
  float rad_orient = PI * 0.00555555555 * orientation;
  curr_x = prev_x + cos(rad_orient) * distance;
  curr_y = prev_y + sin(rad_orient) * distance;
}

void packData() {
  updateSensors();
  updatePosition();

  short pos = point * 12;

  dataSend[pos + 0] = servo.read();
  dataSend[pos + 1] = distanceSonarFront;
  dataSend[pos + 2] = lidarDistanceFront;
  dataSend[pos + 3] = lidarDistanceBack;
  dataSend[pos + 4] = servo.read() + goToOrientation;
  dataSend[pos + 5] = x;
  dataSend[pos + 6] = y;
  dataSend[pos + 7] = elapsedTime;
  dataSend[pos + 8] = aevent.acceleration.y;
  dataSend[pos + 9] = aevent.acceleration.z;
  dataSend[pos + 10] = mevent.magnetic.x;
  dataSend[pos + 11] = mevent.magnetic.y;

  point++;
}

void rotateServo() {
  if (servoAngle >= 180 || servoAngle <= 0) direction = -direction;
  servoAngle += direction;
  servo.write(servoAngle);

}

void action(float actionNumber) {

  if (distanceSonarFront < MIN_SONAR_DISTANCE && actionNumber == 1) {
    stopMotors();
  }

  switch ((int)actionNumber) {
    case -1:
      dumbMapping();
      break;
    case 0:
      stopMotors();
      break;
    case 1:
      moveForward();
      break;

    case 2:
      moveBackward();
      break;

    case 3:
      moveRight();
      break;

    case 4:
      moveLeft();
      break;

    default:
      Serial.println("No output for the actionNumber");
      break;
  }
}

void dumbMapping(){
  moveForward();
  if (distanceSonarFront < MIN_SONAR_DISTANCE) {
      moveLeft();
  }
}

void stopMotors() {
  stepperLeft.setSpeed(0);
  stepperRight.setSpeed(0);
  stepperLeft.runSpeed();
  stepperRight.runSpeed();
}

void moveForward() {
  stepperLeft.setSpeed(-CONST_SPEED_STEPPER);
  stepperRight.setSpeed(CONST_SPEED_STEPPER);
  if(stepperLeft.runSpeed()){
    if (goToOrientation == 0) {
        curr_y += DIST_PER_STEP;  // move north
    } else if (goToOrientation == 90) {
        curr_x += DIST_PER_STEP;  // move west
    } else if (goToOrientation == 180) {
        curr_y -= DIST_PER_STEP;  // move south
    } else if (goToOrientation == 270) {
        curr_x -= DIST_PER_STEP;  // move east
    }
  }
  stepperRight.runSpeed();
}

void moveBackward() {
  stepperLeft.setSpeed(CONST_SPEED_STEPPER);
  stepperRight.setSpeed(-CONST_SPEED_STEPPER);
  if(stepperLeft.runSpeed()){
    if (goToOrientation == 0) {
        curr_y -= DIST_PER_STEP;  // move north
    } else if (goToOrientation == 90) {
        curr_x -= DIST_PER_STEP;  // move west
    } else if (goToOrientation == 180) {
        curr_y += DIST_PER_STEP;  // move south
    } else if (goToOrientation == 270) {
        curr_x += DIST_PER_STEP;  // move east
    }
  }
  stepperRight.runSpeed();
}

void moveRight() {
  goToOrientation = (int)(goToOrientation + 90) % 360;
  stepperLeft.setCurrentPosition(0);
  stepperRight.setCurrentPosition(0);
  stepperLeft.move(-STEPS_90_DEG);  // turn right 90 degrees
  stepperRight.move(-STEPS_90_DEG);
  prev_x = curr_x;
  prev_y = curr_y;
  while (stepperLeft.distanceToGo() != 0 || stepperRight.distanceToGo() != 0) {
    stepperLeft.run();
    stepperRight.run();
  }
  stepperRight.setCurrentPosition(0);
  actionNumber = 0;
}

void moveLeft() {
  goToOrientation = (int)(goToOrientation - 90) % 360;
  goToOrientation = goToOrientation < 0 ? goToOrientation + 360 : goToOrientation;
  stepperLeft.setCurrentPosition(0);
  stepperRight.setCurrentPosition(0);
  stepperLeft.move(STEPS_90_DEG);  // turn right 90 degrees
  stepperRight.move(STEPS_90_DEG);
  prev_x = curr_x;
  prev_y = curr_y;
  while (stepperLeft.distanceToGo() != 0 || stepperRight.distanceToGo() != 0) {
    stepperLeft.run();
    stepperRight.run();
  }
  stepperRight.setCurrentPosition(0);
  actionNumber = 0;
}


void Task1code(void* pvParameters) {
  for (;;) {
    action(actionNumber);
  }
}

void loop() {
  if(WiFi.softAPgetStationNum() == 1){
    handleOutgoingData();
    readData();
    delay(10);
  } 
}
