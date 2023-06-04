#include <AccelStepper.h>
#include <NewPing.h>
#include <ESP32Servo.h>
#include "Adafruit_VL53L1X.h"
#include <Adafruit_FXAS21002C.h>
#include <Adafruit_FXOS8700.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

// Gyro Accel Mag (GAM)
#define SDA_2 26                                            // New I2C Data Pin
#define SCL_2 27                                            // New I2C Clock Pin
Adafruit_FXAS21002C gyro = Adafruit_FXAS21002C(0x0021002C); /* Assign a unique ID to the sensors at the same time */
Adafruit_FXOS8700 accelmag = Adafruit_FXOS8700(0x8700A, 0x8700B);

// VL53L1X Lidar
#define IRQ_PIN 2
#define XSHUT_PIN 3
Adafruit_VL53L1X vl53 = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);
const int16_t minLidarDistance = 150;  // in mm

// Sonar
#define trigPin 12
#define echoPin 14
const int maxSonarDistance = 400;  // in cm
const int minSonarDistance = 8;    // in cm
NewPing sonar(trigPin, echoPin, maxSonarDistance);

// Servo
#define servoPin 15
Servo servo;
const int servoInitPos = 84;  // 86 degrees
int servoAngle = servoInitPos;
int direction = 1;

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

// Define step constants
#define FULLSTEP 4
#define HALFSTEP 8

// Define acceleration and maximum speed values
const float acceleration = 250.0;
const float maxSpeed = 2000;
const float constSpeed = 1000;
const int STEPS_PER_REV = 2038;
const int STEPS_90_DEG = 1740;

// Creates two instances
// Pins entered in sequence IN1-IN3-IN2-IN4 for proper step sequence
AccelStepper stepperLeft(FULLSTEP, lIN1, lIN3, lIN2, lIN4);
AccelStepper stepperRight(FULLSTEP, rIN1, rIN3, rIN2, rIN4);

int sonarDistance;
int16_t lidarDistance;

const unsigned long interval = 10;
unsigned long previousMillis = 0;

void setup() {

  // Serial Monitor
  Serial.begin(115200);

  // Gyro Accel Mag (GAM)
  setupGAM();

  // Lidar
  setupLidar();

  // Servo
  servo.attach(servoPin);
  servo.write(servoInitPos);  // Put servo to initial position (looking forward)

  // Set initial speed and acceleration
  stepperLeft.setMaxSpeed(maxSpeed);
  stepperLeft.setAcceleration(acceleration);
  stepperRight.setMaxSpeed(maxSpeed);
  stepperRight.setAcceleration(acceleration);
}

void loop() {
  unsigned long currentMillis = millis();  // millis() = number of milliseconds that have elapsed since the board started running

  // Read lidar sensor
  readAndPrintLidar();
  // Print Gyro Accel Mag data
  //getEventGAM();

  // Read sonar sensor
  //sonarDistance = sonar.ping_cm();

  // If sonarDistance / lidarDistance is less than minDistance, turn right
  if (lidarDistance < minLidarDistance && lidarDistance != 0 && lidarDistance != -1) {
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

  moveForward();

  // This code executes every 10 milliseconds (rotating servo)
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    rotateServo();
  }
}

void moveForward() {
  // Move forward at constant speed if distance is greater than or equal to minDistance
  stepperLeft.setSpeed(-constSpeed);  // negative speed for left motor
  stepperRight.setSpeed(constSpeed);  // positive speed for right motor
  stepperLeft.runSpeed();
  stepperRight.runSpeed();
}

void rotateServo() {
  servoAngle += direction;
  if (servoAngle > 135 || servoAngle < 45) {
    direction *= -1;
  }
  servo.write(servoAngle);
  //Serial.println(servoAngle);
  //delay(10);
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
      Serial.print(F("Couldn't get lidar distance: "));
      Serial.println(vl53.vl_status);
      return;
    }
    Serial.print(F("Lidar distance: "));
    Serial.print(lidarDistance);
    Serial.println(" mm");

    // data is read out, time for another reading!
    //vl53.clearInterrupt(); // provokes an unnecessary delay
  }
}

void getEventGAM() {
  /* Get a new sensor event */
  sensors_event_t event;
  sensors_event_t aevent, mevent;

  /* Get a new sensor event */
  gyro.getEvent(&event);
  accelmag.getEvent(&aevent, &mevent);

  /* Display the results (speed is measured in rad/s) */
  Serial.print("G ");
  Serial.print("X: ");
  Serial.print(event.gyro.x);
  Serial.print("  ");
  Serial.print("Y: ");
  Serial.print(event.gyro.y);
  Serial.print("  ");
  Serial.print("Z: ");
  Serial.print(event.gyro.z);
  Serial.print("  ");
  Serial.println("rad/s ");
  //delay(500);

  /* Display the accel results (acceleration is measured in m/s^2) */
  Serial.print("A ");
  Serial.print("X: ");
  Serial.print(aevent.acceleration.x, 4);
  Serial.print("  ");
  Serial.print("Y: ");
  Serial.print(aevent.acceleration.y, 4);
  Serial.print("  ");
  Serial.print("Z: ");
  Serial.print(aevent.acceleration.z, 4);
  Serial.print("  ");
  Serial.println("m/s^2");

  /* Display the mag results (mag data is in uTesla) */
  Serial.print("M ");
  Serial.print("X: ");
  Serial.print(mevent.magnetic.x, 1);
  Serial.print("  ");
  Serial.print("Y: ");
  Serial.print(mevent.magnetic.y, 1);
  Serial.print("  ");
  Serial.print("Z: ");
  Serial.print(mevent.magnetic.z, 1);
  Serial.print("  ");
  Serial.println("uT");

  //delay(500);
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
  //Serial.begin(115200);

  /* Wait for the Serial Monitor */
  while (!Serial) {
    delay(1);
  }

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

  /* Set gyro range. (optional, default is 250 dps) */
  // gyro.setRange(GYRO_RANGE_2000DPS);

  /* Display some basic information on this sensor */
  displaySensorDetails();
}

void displaySensorDetails(void) {
  sensor_t sensor;
  sensor_t accel, mag;
  gyro.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print("Sensor:       ");
  Serial.println(sensor.name);
  Serial.print("Driver Ver:   ");
  Serial.println(sensor.version);
  Serial.print("Unique ID:    0x");
  Serial.println(sensor.sensor_id, HEX);
  Serial.print("Max Value:    ");
  Serial.print(sensor.max_value);
  Serial.println(" rad/s");
  Serial.print("Min Value:    ");
  Serial.print(sensor.min_value);
  Serial.println(" rad/s");
  Serial.print("Resolution:   ");
  Serial.print(sensor.resolution);
  Serial.println(" rad/s");
  Serial.println("------------------------------------");
  Serial.println("");
  //delay(500);

  accelmag.getSensor(&accel, &mag);
  Serial.println("------------------------------------");
  Serial.println("ACCELEROMETER");
  Serial.println("------------------------------------");
  Serial.print("Sensor:       ");
  Serial.println(accel.name);
  Serial.print("Driver Ver:   ");
  Serial.println(accel.version);
  Serial.print("Unique ID:    0x");
  Serial.println(accel.sensor_id, HEX);
  Serial.print("Min Delay:    ");
  Serial.print(accel.min_delay);
  Serial.println(" s");
  Serial.print("Max Value:    ");
  Serial.print(accel.max_value, 4);
  Serial.println(" m/s^2");
  Serial.print("Min Value:    ");
  Serial.print(accel.min_value, 4);
  Serial.println(" m/s^2");
  Serial.print("Resolution:   ");
  Serial.print(accel.resolution, 8);
  Serial.println(" m/s^2");
  Serial.println("------------------------------------");
  Serial.println("");
  Serial.println("------------------------------------");
  Serial.println("MAGNETOMETER");
  Serial.println("------------------------------------");
  Serial.print("Sensor:       ");
  Serial.println(mag.name);
  Serial.print("Driver Ver:   ");
  Serial.println(mag.version);
  Serial.print("Unique ID:    0x");
  Serial.println(mag.sensor_id, HEX);
  Serial.print("Min Delay:    ");
  Serial.print(accel.min_delay);
  Serial.println(" s");
  Serial.print("Max Value:    ");
  Serial.print(mag.max_value);
  Serial.println(" uT");
  Serial.print("Min Value:    ");
  Serial.print(mag.min_value);
  Serial.println(" uT");
  Serial.print("Resolution:   ");
  Serial.print(mag.resolution);
  Serial.println(" uT");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}