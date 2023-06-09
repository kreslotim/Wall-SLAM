#include <WiFi.h>
#include <WebServer.h>
#include <NewPing.h>
#include <ESP32Servo.h>
#include "Adafruit_VL53L1X.h"
#include <Adafruit_FXAS21002C.h>
#include <Adafruit_FXOS8700.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_Sensor_Calibration.h>
#include <Adafruit_AHRS.h>
#include <Wire.h>
#include <AccelStepper.h>
#include <WiFiUdp.h>
#include <math.h>
// Create instance of IMU Sensor and declare pointers to Adafruit sensor objects
Adafruit_Sensor *accelerometer, *gyroscope, *magnetometer;
#include "NXP_FXOS_FXAS.h"  // NXP 9-DoF breakout

// Task handle for managing the task 
TaskHandle_t Task1;

// Sensor event and control variables
sensors_event_t event;
sensors_event_t aevent, mevent;
float heading;
float prevHeading;
const int THRESHOLD_VALUE = 1;
const int SPEED_INCREMENT = 100;
float yaw;
float initialMagHeading = 0;

float gyroZ;
float orientationMag = 0;
// Define complementary filter variables
unsigned long prevTimestamp = 0;

int distanceSonarFront = 0;
int16_t lidarDistanceFront;
int16_t lidarDistanceBack;
float dataSend[12];
int servoAngle=1;
int numberOfConnectionOld = 0;
float actionNumber = 0;
int goToOrientation = 0;
float curr_x = 0;
float curr_y = 0;
unsigned long startTime; // Variable to store the start time
unsigned long elapsedTime;
uint32_t timestamp;
int direction = 1;

// Stepper motor and distance settings
const float ACCELERATION_STEPPER = 250.0;
const float MAX_SPEED_STEPPER = 2000;
const float CONST_SPEED_STEPPER = 500;
const int STEPS_PER_REV = 2038;
const int STEPS_90_DEG = 1680;
const int16_t MIN_LIDAR_DISTANCE = 150;  // in mm
const int16_t MIN_SONAR_DISTANCE = 40;  // in mm (in cm but we x10 the distance)
const int SERVO_INIT_POS = 84;
const int MAX_DISTANCE_SONAR = 400;
const float DIST_PER_STEP = 0.06;  // in mm per step

// Stepper motor stepping modes
#define FULLSTEP 4
#define HALFSTEP 8

// Ultrasonic sensor pins
#define TRIG_PIN 12
#define ECHO_PIN 14

// VL53L1X lidar sensor pins
#define IRQ_PIN 2
#define XSHUT_PIN 3

// Servo motor pin
#define servoPin 15

// I2C communication pins for Fronr lidar (the back one is set on standart I2C pins)
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

// IMU Settings
#if defined(ADAFRUIT_SENSOR_CALIBRATION_USE_EEPROM)
  Adafruit_Sensor_Calibration_EEPROM cal;
#else
  Adafruit_Sensor_Calibration_SDFat cal;
#endif

#define FILTER_UPDATE_RATE_HZ 100
#define PRINT_EVERY_N_UPDATES 10
//#define AHRS_DEBUG_OUTPUT

// Create instance of Servo
Servo servo;

// pick your filter! slower == better quality output
Adafruit_NXPSensorFusion filter; // slowest
//Adafruit_Madgwick filter;  // faster than NXP
//Adafruit_Mahony filter;  // fastest/smalleset

// Create instance of Lidar
Adafruit_VL53L1X vl53Front = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);
Adafruit_VL53L1X vl53Back = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);

// Create intance of Gyro, Accel and Mag
Adafruit_FXAS21002C gyro = Adafruit_FXAS21002C(0x0021002C);
Adafruit_FXOS8700 accelmag = Adafruit_FXOS8700(0x8700A, 0x8700B);

// Create instance of Ultrasonic sensor
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

bool isTurning = false;

//Open Wifi Port
WiFiServer sendServer(SEND_DATA_PORT);
WiFiServer recieveServer(RECIEVE_DATA_PORT);

// Initialize WiFi and WebServer objects
WiFiClient sendClient;
WiFiClient recieveClient;

// Configure IP addresses of the local access point
IPAddress local_IP(192, 168, 1, 22);
IPAddress user_IP(192, 168, 1, 23);

IPAddress gateway(192, 168, 1, 5);
IPAddress subnet(255, 255, 255, 0);

void setup() {
  Serial.begin(115200);



  // Servo Setup
  servo.attach(servoPin);
  servo.write(SERVO_INIT_POS);  // Put servo to initial position (looking forward)

  // Setup Front/Back lidars and IMU
  setupLidarsAndIMU();

  // Setup IMU Fusion algorithm
  setupIMUFusion();

  // Motors Setup
  stepperLeft.setMaxSpeed(MAX_SPEED_STEPPER);
  stepperLeft.setAcceleration(ACCELERATION_STEPPER);
  stepperRight.setMaxSpeed(MAX_SPEED_STEPPER);
  stepperRight.setAcceleration(ACCELERATION_STEPPER);
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

// Initializes lidar sensors and IMU.
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

// Initializes the IMU using Sensor Fusion Algorithm
void setupIMUFusion() {
  while (!Serial) yield();

  //if (!cal.begin()) {
  //  Serial.println("Failed to initialize calibration helper");
  //} else if (! cal.loadCalibration()) {
  //  Serial.println("No calibration loaded/found");
  //}

  if (!init_sensors()) {
    Serial.println("Failed to find sensors");
    while (1) delay(10);
  }

  setup_sensors();
  filter.begin(FILTER_UPDATE_RATE_HZ);
  timestamp = millis();

  Wire.setClock(400000); // 400KHz

  sensors_event_t mag;
  magnetometer->getEvent(&mag);
  // Calculate the initial magnetometer heading
  initialMagHeading = (180 * atan2(-mag.magnetic.y, mag.magnetic.x) / PI);
}

// Computes precise orientation using Fusion Sensor Algorithm, combining magnetometer and gyroscope data.
void getHeading() {
  
  float gx, gy, gz;
  static uint8_t counter = 0;

  if ((millis() - timestamp) < (1000 / FILTER_UPDATE_RATE_HZ)) {
    return;
  }
  timestamp = millis();
  // Read the motion sensors
  sensors_event_t accel, gyro, mag;
  accelerometer->getEvent(&accel);
  gyroscope->getEvent(&gyro);
  magnetometer->getEvent(&mag);
#if defined(AHRS_DEBUG_OUTPUT)
  Serial.print("I2C took "); Serial.print(millis()-timestamp); Serial.println(" ms");
#endif

  cal.calibrate(mag);
  cal.calibrate(accel);
  cal.calibrate(gyro);
  // Gyroscope needs to be converted from Rad/s to Degree/s
  // the rest are not unit-important
  gx = gyro.gyro.x * SENSORS_RADS_TO_DPS;
  gy = gyro.gyro.y * SENSORS_RADS_TO_DPS;
  gz = gyro.gyro.z * SENSORS_RADS_TO_DPS;

  gyroZ = gz;

  // Update the SensorFusion filter
  filter.update(gx, gy, gz, 
                accel.acceleration.x, accel.acceleration.y, accel.acceleration.z, 
                mag.magnetic.x, mag.magnetic.y, mag.magnetic.z);
#if defined(AHRS_DEBUG_OUTPUT)
  Serial.print("Update took "); Serial.print(millis()-timestamp); Serial.println(" ms");
#endif

  // only print the calculated output once in a while
  if (counter++ <= PRINT_EVERY_N_UPDATES) {
    return;
  }
  // reset the counter
  counter = 0;

#if defined(AHRS_DEBUG_OUTPUT)
  Serial.print("Raw: ");
  Serial.print(accel.acceleration.x, 4); Serial.print(", ");
  Serial.print(accel.acceleration.y, 4); Serial.print(", ");
  Serial.print(accel.acceleration.z, 4); Serial.print(", ");
  Serial.print(gx, 4); Serial.print(", ");
  Serial.print(gy, 4); Serial.print(", ");
  Serial.print(gz, 4); Serial.print(", ");
  Serial.print(mag.magnetic.x, 4); Serial.print(", ");
  Serial.print(mag.magnetic.y, 4); Serial.print(", ");
  Serial.print(mag.magnetic.z, 4); Serial.println("");
#endif

  // print the heading
  heading = filter.getYaw();
  //Serial.print("Orientation: ");
  //Serial.println(heading);
  
#if defined(AHRS_DEBUG_OUTPUT)
  Serial.print("Took "); Serial.print(millis()-timestamp); Serial.println(" ms");
#endif
}

// Reads distance from both lidars (front and back)
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

// Reads the data comming from the laptop side
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

// Sends data to the laptop
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

//  Updates the distance and motion sensors (IMU, and both lidars on servo)
void updateSensors() {

  //Update Timer
  elapsedTime = (float)(millis() - startTime);

  // Ultrasonic Update
  distanceSonarFront = frontUltrasonic.ping_cm() * 10; 

  // Lidar Update
  rotateServo();
  readLidar();

  getHeading();

  // IMU Update
  gyro.getEvent(&event);
  accelmag.getEvent(&aevent, &mevent);

  // Orientation Update
  orientationMag = atan2(-mevent.magnetic.y, mevent.magnetic.x) * 180 / PI - initialMagHeading;

  if (orientationMag < 0) {
      orientationMag += 360;
    } else if (orientationMag >= 360) {
      orientationMag -= 360;
    }
  
  unsigned long currentTimestamp = millis();
  float deltaTime = (currentTimestamp - prevTimestamp) / 1000.0; // Convert milliseconds to seconds
  prevTimestamp = currentTimestamp;

  // Update the yaw
  yaw -= (gyroZ * 180/PI) * deltaTime;

   //Keep yaw within the range of 0 to 360 degrees
  if (yaw < 0) {
    yaw += 360;
  } else if (yaw >= 360) {
    yaw -= 360;
  }

  yaw = fmod(yaw, 360.0);
  
}

// Packs the data into packets for sending to laptop
void packData() {
  updateSensors();
  dataSend[0] = servo.read();
  dataSend[1] = distanceSonarFront;
  dataSend[2] = lidarDistanceFront;
  dataSend[3] = lidarDistanceBack;
  dataSend[4] = servo.read() + goToOrientation;
  dataSend[5] = curr_x;
  dataSend[6] = curr_y;
  dataSend[7] = elapsedTime;
  dataSend[8] = orientationMag; // Mag or
  dataSend[9] = yaw;  // Gyro Or
  dataSend[10] = heading;
  dataSend[11] = goToOrientation;
  //Serial.print("Orientation :");
  //Serial.print(goToOrientation);

  //Serial.println("magOrientation: "+ String(orientationMag));
  //Serial.println("gyroOrientation: "+ String(yaw));
  //Serial.println("Kalman heading: "+ String(heading));

}

// Sweeps the servo from 0 to 180 and backwards
void rotateServo() {
  if (servoAngle >= 180 || servoAngle <= 0) direction = -direction;
  servoAngle += direction;
  servo.write(servoAngle);

}

// Determines the behaviour of the car (moving, turning, stop)
void action(float actionNumber) {
  
  //Serial.println(distanceSonarFront);

  switch ((int)actionNumber) {
    case 0:
      stopMotors();
      break;
    case 1:
      if (distanceSonarFront <= MIN_SONAR_DISTANCE) {
        stopMotors();
      }
      else {
        moveForward();
      }
      
      break;

    case 2:
      moveBackward();
      break;

    case 3:
      moveRight();
      actionNumber = 0;
      break;

    case 4:
      moveLeft();
      actionNumber = 0;

      break;

    default:
      stepperLeft.run();
      stepperRight.run();
  }

  actionNumber = 0;
}


// Stops all motors
void stopMotors() {
  stepperLeft.setSpeed(0);
  stepperRight.setSpeed(0);
  stepperLeft.runSpeed();
  stepperRight.runSpeed();
}

// Moves the car forward
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
  
  correctHeading();
}

// Moves the car backward
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

// Turns the car 90 degrees right
void moveRight() {
  goToOrientation = (int)(goToOrientation + 90) % 360;
  stepperLeft.setCurrentPosition(0);
  stepperRight.setCurrentPosition(0);
  stepperLeft.move(-STEPS_90_DEG);  // turn right 90 degrees
  stepperRight.move(-STEPS_90_DEG);
  while (stepperLeft.distanceToGo() != 0 || stepperRight.distanceToGo() != 0) {
    lidarDistanceFront = -1;
    lidarDistanceBack = -1;
    stepperLeft.run();
    stepperRight.run();
  }
  
}

// Turns the car 90 degrees left
void moveLeft() {
  goToOrientation = (int)(goToOrientation + 270) % 360;
  stepperLeft.setCurrentPosition(0);
  stepperRight.setCurrentPosition(0);
  stepperLeft.move(STEPS_90_DEG);  // turn right 90 degrees
  stepperRight.move(STEPS_90_DEG);
  while (stepperLeft.distanceToGo() != 0 || stepperRight.distanceToGo() != 0) {
    lidarDistanceFront = -1;
    lidarDistanceBack = -1;
    stepperLeft.run();
    stepperRight.run();
  }
}

// Corrects the orientation of the car while moving, using motion sensor and Kalman filter, to keep it moving in a straight line
void correctHeading() {
// Calculate the heading difference between the current and previous heading
float headingDiff = heading - prevHeading;

// Check if the heading difference exceeds a threshold value
if (abs(headingDiff) > THRESHOLD_VALUE) {
  // Adjust the speed of the motors
  if (headingDiff < 0) {
    // Increase the speed of the motors in the defeating direction
    stepperRight.setSpeed(CONST_SPEED_STEPPER - SPEED_INCREMENT);
    stepperLeft.setSpeed(-CONST_SPEED_STEPPER - SPEED_INCREMENT);
    stepperRight.runSpeed();
    stepperLeft.runSpeed();
    //Serial.println("INCREMENT LEFT");
  } else {
    // Decrease the speed of the motors in the defeating direction
    stepperRight.setSpeed(CONST_SPEED_STEPPER + SPEED_INCREMENT);
    stepperLeft.setSpeed(-CONST_SPEED_STEPPER + SPEED_INCREMENT);
    stepperRight.runSpeed();
    stepperLeft.runSpeed();
    //Serial.println("INCREMENT RIGHT");
  }
} else {
  // Reset the speeds to the constant values
  stepperRight.setSpeed(CONST_SPEED_STEPPER);
  stepperLeft.setSpeed(-CONST_SPEED_STEPPER);
  stepperRight.runSpeed();
  stepperLeft.runSpeed();
  }
  // Store the current heading as the previous heading for the next iteration
  prevHeading = heading;
}

// 
void Task1code(void* pvParameters) {
  for (;;) {
    action(actionNumber);
  }
}

// main loop code sending and receiving data fro
void loop() {
  if(WiFi.softAPgetStationNum() == 1){
    sendData();
    readData();
    delay(10);
  } 
}