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

TaskHandle_t Task1;

sensors_event_t event;
sensors_event_t aevent, mevent;
int distanceSonarFront = 0;
int16_t lidarDistanceFront;
int16_t lidarDistanceBack;
float dataSend[12];
int servoAngle;
int numberOfConnectionOld = 0;
float actionNumber = 0;
float orientation = 0;
int goToOrientation = 0;
float x = 0;
float y = 0;
unsigned long startTime; // Variable to store the start time
unsigned long elapsedTime;

const float ACCELERATION_STEPPER = 250.0;
const float MAX_SPEED_STEPPER = 2000;
const float CONST_SPEED_STEPPER = 500;
const int STEPS_PER_REV = 2038;
const int STEPS_90_DEG = 1740;
const int16_t MIN_LIDAR_DISTANCE = 150;  // in mm
const int SERVO_INIT_POS = 84;
const int MAX_DISTANCE_SONAR = 400;
const float DIST_PER_STEP = 0.06;  // in mm per step

#define FULLSTEP 4
#define HALFSTEP 8

// FrontUtlrasonic settings
#define TRIG_PIN 12
#define ECHO_PIN 14

// VL53L1X Lidar
#define IRQ_PIN 2
#define XSHUT_PIN 3

#define SDA 26  // New I2C Data Pin
#define SCL 27  // New I2C Clock Pin

// Servo settings
#define servoPin 15

// Gyro Accel Mag (GAM)
#define SDA_2 33  // New I2C Data Pin
#define SCL_2 25  // New I2C Clock Pin

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
TwoWire wireOne = TwoWire(0);
TwoWire wireTwo = TwoWire(1);
TwoWire wireThree = TwoWire(2);


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
  WiFi.softAP(ssid, password, 1);  //limit connection to 1 user
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

  // Gyro Accel Mag (GAM) Setup
  setupGAM();

  // Lidar Setup
  setupLidar();

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

void setupLidar() {
  //Serial.begin(115200);
  while (!Serial) delay(10);

  Serial.println(F("Adafruit VL53L1X sensor demo"));

  Wire.begin();

  if (!vl53Front.begin(0x29, &Wire)) {
    Serial.print(F("Error on init of Front VL sensor: "));
    Serial.println(vl53Front.vl_status);
    while (1) delay(10);
  }

  Serial.println(F("VL53L1X sensor OK!"));

  Serial.print(F("Left Sensor ID: 0x"));
  Serial.println(vl53Front.sensorID(), HEX);

  if (!vl53Front.startRanging()) {
    Serial.print(F("Left Couldn't start ranging: "));
    Serial.println(vl53Front.vl_status);
    while (1) delay(10);
  }

  Serial.println(F("Ranging started"));

  // Valid timing budgets: 15, 20, 33, 50, 100, 200 and 500ms!
  vl53Front.setTimingBudget(50);
  Serial.print(F("Timing budget (ms): "));
  Serial.println(vl53Front.getTimingBudget());
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
    while (1);
  }

  if (!accelmag.begin(0x1F, &Wire1)) {
    /* There was a problem detecting the FXOS8700 ... check your connections */
    Serial.println("Ooops, no FXOS8700 detected ... Check your wiring!");
    while (1);
  }
}

void readLidar() {
  if (vl53Front.dataReady()) {
    lidarDistanceFront = vl53Front.distance();
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
  packData();

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
  }
}

void updateSensors() {
  // Ultrasonic Update
  distanceSonarFront = frontUltrasonic.ping_cm();

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

void packData() {
  updateSensors();
  dataSend[0] = servo.read();
  dataSend[1] = distanceSonarFront;
  dataSend[2] = lidarDistanceFront;
  dataSend[3] = lidarDistanceBack;
  dataSend[4] = servo.read();
  dataSend[5] = x;
  dataSend[6] = y;
  dataSend[7] = elapsedTime;
  dataSend[8] = aevent.acceleration.y;
  dataSend[9] = aevent.acceleration.z;
  dataSend[10] = mevent.magnetic.x;
  dataSend[11] = mevent.magnetic.y;
}

void rotateServo() {
  servoAngle = (servoAngle + 1) % 180;
  servo.write(servoAngle);
}

void action(float actionNumber) {
  switch ((int)actionNumber) {
    case -1:
      mapping();
      return;
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
  stepperLeft.runSpeed();
  stepperRight.runSpeed();

  if (goToOrientation == 0) {
    if (actionNumber == 1) {
      y += DIST_PER_STEP;  // move north
    } else if (actionNumber == 2) {
      y -= DIST_PER_STEP;  // move north
    }

  } else if (goToOrientation == 90) {
    if (actionNumber == 1) {
      x += DIST_PER_STEP;  // move west
    } else if (actionNumber == 2) {
      x -= DIST_PER_STEP;  // move west
    }

  } else if (goToOrientation == 180) {
    if (actionNumber == 1) {
      y -= DIST_PER_STEP;  // move south
    } else if (actionNumber == 2) {
      y += DIST_PER_STEP;  // move south
    }

  } else if (goToOrientation == 270) {
    if (actionNumber == 1) {
      x -= DIST_PER_STEP;  // move east
    } else if (actionNumber == 2) {
      x += DIST_PER_STEP;  // move east
    }
  }
}

void mapping(){

}

void stopMotors() {
  stepperLeft.setSpeed(0);
  stepperRight.setSpeed(0);
}

void moveForward() {
  stepperLeft.setSpeed(-CONST_SPEED_STEPPER);
  stepperRight.setSpeed(CONST_SPEED_STEPPER);
}

void moveBackward() {
  stepperLeft.setSpeed(CONST_SPEED_STEPPER);
  stepperRight.setSpeed(-CONST_SPEED_STEPPER);
}

void moveRight() {
  goToOrientation = (int)(orientation + 90) % 360;
  Serial.println("goToOrientation : ");
  Serial.println(goToOrientation);
  while (goToOrientation != (int)orientation) {
    updateSensors();
    Serial.println("Orientation : ");
    Serial.println(orientation);
    stepperLeft.setSpeed(-CONST_SPEED_STEPPER);
    stepperRight.setSpeed(-CONST_SPEED_STEPPER);
    stepperLeft.runSpeed();
    stepperRight.runSpeed();
  }
}

void moveLeft() {
  goToOrientation = (int)(orientation - 90) % 360;
  while (goToOrientation != (int)orientation) {
    updateSensors();
    stepperLeft.setSpeed(CONST_SPEED_STEPPER);
    stepperRight.setSpeed(CONST_SPEED_STEPPER);
    stepperLeft.runSpeed();
    stepperRight.runSpeed();
  }
}

void Task1code(void* pvParameters) {
  for (;;) {
    action(actionNumber);
  }
}

void loop() {
  sendData();
  readData();
  delay(10);
}
