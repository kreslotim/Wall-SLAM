// Full orientation sensing using NXP/Madgwick/Mahony and a range of 9-DoF
// sensor sets.
// You *must* perform a magnetic calibration before this code will work.
//
// To view this data, use the Arduino Serial Monitor to watch the
// scrolling angles, or run the OrientationVisualiser example in Processing.
// Based on  https://github.com/PaulStoffregen/NXPMotionSense with adjustments
// to Adafruit Unified Sensor interface

#include <Adafruit_Sensor_Calibration.h>
#include <Adafruit_AHRS.h>
#include <AccelStepper.h>

Adafruit_Sensor *accelerometer, *gyroscope, *magnetometer;

#include "NXP_FXOS_FXAS.h"  // NXP 9-DoF breakout

// pick your filter! slower == better quality output
//Adafruit_NXPSensorFusion filter; // slowest
Adafruit_Madgwick filter;  // faster than NXP
//Adafruit_Mahony filter;  // fastest/smalleset

#if defined(ADAFRUIT_SENSOR_CALIBRATION_USE_EEPROM)
  Adafruit_Sensor_Calibration_EEPROM cal;
#else
  Adafruit_Sensor_Calibration_SDFat cal;
#endif

#define FILTER_UPDATE_RATE_HZ 100
#define PRINT_EVERY_N_UPDATES 10
//#define AHRS_DEBUG_OUTPUT

// Left Motor
#define lIN1 2
#define lIN2 23
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
const float acceleration = 200.0;
const float maxSpeed = 1000;
const float constSpeed = 500;
const int STEPS_PER_REV = 2038;

float heading;
float prevHeading = 0.0;
const int THRESHOLD_VALUE = 5;
const int SPEED_INCREMENT = 10;

uint32_t timestamp;

// Creates two instances
// Pins entered in sequence IN1-IN3-IN2-IN4 for proper step sequence
AccelStepper stepperRight(FULLSTEP, rIN1, rIN3, rIN2, rIN4);
AccelStepper stepperLeft(FULLSTEP, lIN1, lIN3, lIN2, lIN4);

void setup() {

  stepperRight.setMaxSpeed(maxSpeed);
  stepperRight.setAcceleration(acceleration);
  stepperRight.setSpeed(constSpeed);

  stepperLeft.setMaxSpeed(maxSpeed);
  stepperLeft.setAcceleration(acceleration);
  stepperLeft.setSpeed(-constSpeed);

  Serial.begin(115200);
  while (!Serial) yield();

  if (!cal.begin()) {
    Serial.println("Failed to initialize calibration helper");
  } else if (! cal.loadCalibration()) {
    Serial.println("No calibration loaded/found");
  }

  if (!init_sensors()) {
    Serial.println("Failed to find sensors");
    while (1) delay(10);
  }
  

  setup_sensors();
  filter.begin(FILTER_UPDATE_RATE_HZ);
  timestamp = millis();

  Wire.setClock(400000); // 400KHz
}


void loop() {
  getHeading();

  stepperRight.runSpeed();
  stepperLeft.runSpeed();

}

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


void correctHeading() {
  // Calculate the heading difference between the current and previous heading
float headingDiff = heading - prevHeading;

// Check if the heading difference exceeds a threshold value
if (abs(headingDiff) > THRESHOLD_VALUE) {
  // Adjust the speed of the motors
  if (headingDiff > 0) {
    // Increase the speed of the motors in the defeating direction
    stepperRight.setSpeed(constSpeed + SPEED_INCREMENT);
    stepperLeft.setSpeed(-constSpeed - SPEED_INCREMENT);
  } else {
    // Decrease the speed of the motors in the defeating direction
    stepperRight.setSpeed(constSpeed - SPEED_INCREMENT);
    stepperLeft.setSpeed(-constSpeed + SPEED_INCREMENT);
  }
} else {
  // Reset the speeds to the constant values
  stepperRight.setSpeed(constSpeed);
  stepperLeft.setSpeed(-constSpeed);
}

// Store the current heading as the previous heading for the next iteration
prevHeading = heading;
}