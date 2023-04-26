#include <AccelStepper.h>
#include <NewPing.h>
#include <ESP32Servo.h>
#include "Adafruit_VL53L1X.h"
#include <Adafruit_Sensor.h>
#include <Wire.h>

#define IRQ_PIN 2
#define XSHUT_PIN 3
#define trigPin 12
#define echoPin 14
#define servoPin 15
#define lIN1 2
#define lIN2 0
#define lIN3 4
#define lIN4 16
#define rIN1 17
#define rIN2 5
#define rIN3 18
#define rIN4 19
#define FULLSTEP 4
#define HALFSTEP 8

const int16_t minLidarDistance = 150;  // in mm

const int maxSonarDistance = 400;  // in cm
const int minSonarDistance = 8;    // in cm

const float acceleration = 250.0;
const float maxSpeed = 2000;
const float constSpeed = 1000;
const int STEPS_PER_REV = 2038;
const int STEPS_90_DEG = 1740;
const float DIST_PER_STEP = 0.6; // in mm per step

const unsigned long interval = 10; // delay for servo

const int SERVO_INIT_POS = 84;  // 86 degrees

int servoAngle = SERVO_INIT_POS;
int direction = 1;

int sonarDistance;
int16_t lidarDistance;
int nbSteps;

unsigned long previousMillis = 0;

// VL53L1X Lidar
Adafruit_VL53L1X vl53 = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);

// Sonar
NewPing sonar(trigPin, echoPin, maxSonarDistance);

// Servo
Servo servo;

// Motors
AccelStepper stepperLeft(FULLSTEP, lIN1, lIN3, lIN2, lIN4);
AccelStepper stepperRight(FULLSTEP, rIN1, rIN3, rIN2, rIN4);


void setup() {

  // Serial Monitor
  Serial.begin(115200);

  // Lidar
  setupLidar();

  // Servo
  servo.attach(servoPin);
  servo.write(SERVO_INIT_POS);  // Put servo to initial position (looking forward)

  // Set initial speed and acceleration
  stepperLeft.setMaxSpeed(maxSpeed);
  stepperLeft.setAcceleration(acceleration);
  stepperRight.setMaxSpeed(maxSpeed);
  stepperRight.setAcceleration(acceleration);
}

void loop() {
  unsigned long currentMillis = millis();  // millis() = number of milliseconds that have elapsed since the board started running

  // Read sonar sensor
  //sonarDistance = sonar.ping_cm();

  readLidar();

  // If sonarDistance / lidarDistance is less than minDistance, turn right
  if (lidarDistance < minLidarDistance && lidarDistance != 0 && lidarDistance != -1) {

    nbSteps = stepperRight.currentPosition();
    scan180();
    turnLeft();
  }

  moveForward();
}

void scan180() {

  servo.write(0);
  for (int angle = 0; angle <= 180; angle++) {
    servo.write(angle);
    delay(10);
    readLidar();
    String output = String((int)angle) + "," + String((int)lidarDistance) + "," + String((int)(nbSteps*DIST_PER_STEP)) +","+ String((int)0);
    Serial.println(output);
  }
  servo.write(SERVO_INIT_POS);
}

void moveForward() {
  // Move forward at constant speed if distance is greater than or equal to minDistance
  stepperLeft.setSpeed(-constSpeed);  // negative speed for left motor
  stepperRight.setSpeed(constSpeed);  // positive speed for right motor
  stepperLeft.runSpeed();
  stepperRight.runSpeed();
}

void turnRight() {
    stepperLeft.setCurrentPosition(0);
    stepperRight.setCurrentPosition(0);
    //delay(500);  // stop for 0.5 seconds
    stepperLeft.move(-STEPS_90_DEG);  // turn right 90 degrees
    stepperRight.move(-STEPS_90_DEG);
    while (stepperLeft.distanceToGo() != 0 || stepperRight.distanceToGo() != 0) {
      stepperLeft.run();
      stepperRight.run();
    }
}

void turnLeft() {
  stepperLeft.setCurrentPosition(0);
    stepperRight.setCurrentPosition(0);
    //delay(500);  // stop for 0.5 seconds
    stepperLeft.move(STEPS_90_DEG);  // turn right 90 degrees
    stepperRight.move(STEPS_90_DEG);
    while (stepperLeft.distanceToGo() != 0 || stepperRight.distanceToGo() != 0) {
      stepperLeft.run();
      stepperRight.run();
    }
}


void printSonar() {
  Serial.print("Sonar distance: ");
  Serial.println(sonarDistance);
}

void readAndPrintLidar() {

  if (vl53.dataReady()) {
    // new measurement for the taking!
    lidarDistance = vl53.distance();
    if (lidarDistance == -1) {
      // something went wrong!
      //Serial.print(F("Couldn't get lidar distance: "));
      //Serial.println(vl53.vl_status);
      return;
    }


    //Serial.print(F("Lidar distance: "));
    //Serial.print(lidarDistance);
    //Serial.println(" mm");

    // data is read out, time for another reading!
    //vl53.clearInterrupt(); // provokes an unnecessary delay
  }
}

void readLidar() {
  if (vl53.dataReady()) {
    // new measurement for the taking!
    lidarDistance = vl53.distance();
  }
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

