#include <WiFi.h>
#include "Adafruit_VL53L0X.h"
#include <Adafruit_FXAS21002C.h>
#include <Adafruit_FXOS8700.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <AccelStepper.h>


TaskHandle_t Task1;

sensors_event_t event;
sensors_event_t aevent, mevent;
float actionNumber = 0;
float orientation = 0;
int goToOrientation = 0;
float x = 0;
float y = 0;
unsigned long startTime; // Variable to store the start time
unsigned long endTime;
int direction = 1;

const float ACCELERATION_STEPPER = 250.0;
const float MAX_SPEED_STEPPER = 1000;
const float CONST_SPEED_STEPPER = 500;
const int STEPS_PER_REV = 2038;
const int STEPS_90_DEG = 1740;
const int SERVO_INIT_POS = 84;
const int MAX_DISTANCE_SONAR = 400;
const float DIST_PER_STEP = 0.06;  // in mm per step

static float B = DIST_PER_STEP * 0.001;  // ticksToMeters
static float A = 1;  
static float C = 1;     // x -> y


//Kalman const and var
const float ROT_PER_METER = 2.5 * M_1_PI;
const float STEPS_PER_METERS = 2048 * ROT_PER_METER;

const float Q_SPEED_RATIO = 0.015625;
const float R_ACCEL_RATIO = 9.80665 * 0.000126;

float speed_prev = 0;

float varX = 0;
float varY = 0;

float timeDelta;

float accX = 0;
float accY = 0;
float accZ = 0;


#define FULLSTEP 4
#define HALFSTEP 8

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


// Create intance of Gyro, Accel and Mag
Adafruit_FXAS21002C gyro = Adafruit_FXAS21002C(0x0021002C);
Adafruit_FXOS8700 accelmag = Adafruit_FXOS8700(0x8700A, 0x8700B);

// Create instances of stepper motors
AccelStepper stepperLeft(FULLSTEP, L_IN1, L_IN3, L_IN2, L_IN4);
AccelStepper stepperRight(FULLSTEP, R_IN1, R_IN3, R_IN2, R_IN4);



void setup() {
  Serial.begin(115200);
  Serial.println("hello");

  // Gyro Accel Mag (GAM) Setup
  setupLidarsAndIMU();

  // Motors Setup
  stepperLeft.setMaxSpeed(MAX_SPEED_STEPPER);
  stepperRight.setMaxSpeed(MAX_SPEED_STEPPER);

  stepperLeft.setSpeed(-CONST_SPEED_STEPPER);
  stepperRight.setSpeed(CONST_SPEED_STEPPER);

  
  
  // Setup core to Move
  xTaskCreatePinnedToCore(
    Task1code,  /* Task function. */
    "Task1",    /* name of task. */
    2048,       /* Stack size of task */
    NULL,       /* parameter of the task */
    0,          /* priority of the task */
    &Task1,     /* Task handle to keep track of created task */
    1);         /* pin task to core 1 */

  delay(500);

  // Setup Timer
  startTime = millis(); // Record the start time
}


void setupLidarsAndIMU() {
  Wire.begin();

  /* Initialise the sensor */
  if (!gyro.begin(0x21, &Wire)) {
    Serial.println("Ooops, no FXAS21002C detected ... Check your wiring!");
    while (1);
  }

  if (!accelmag.begin(0x1F, &Wire)) {
    Serial.println("Ooops, no FXOS8700 detected ... Check your wiring!");
    while (1);
  }
}


void updateSensors() {
  // IMU Update
  gyro.getEvent(&event);
  accelmag.getEvent(&aevent, &mevent);

  // Orientation Update
  orientation = atan2(mevent.magnetic.y, mevent.magnetic.x) * 180 / PI;
}

float Q_rsqrt( float number ){
  long i;
  float x2, y;
  const float threehalfs = 1.5F;

  x2 = number * 0.5F;
  y  = number;
  i  = * ( long * ) &y;    // evil floating point bit level hacking
  i  = 0x5f3759df - ( i >> 1 );               // what the fuck? 
  y  = * ( float * ) &i;
  y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration
  y  = y * ( threehalfs - ( x2 * y * y ) );   // 2nd iteration,

  return y;
}

float currAcceleration(){
  accelmag.getEvent(&aevent, &mevent);
  float ax = aevent.acceleration.x * aevent.acceleration.x + aevent.acceleration.y * aevent.acceleration.y + aevent.acceleration.z * aevent.acceleration.z;
  return Q_rsqrt(ax) * ax;
}

float currODR(){
  fxos8700ODR_t rate = accelmag.getOutputDataRate();

  if (rate == ODR_800HZ)    return 800;
  if (rate == ODR_400HZ)    return 400;
  if (rate == ODR_200HZ)    return 200;
  if (rate == ODR_100HZ)    return 100;
  if (rate == ODR_50HZ)     return 50;
  if (rate == ODR_25HZ)     return 25;
  if (rate == ODR_12_5HZ)   return 12.5;
  if (rate == ODR_6_25HZ)   return 6.25;
  if (rate == ODR_3_125HZ)  return 3.125;
  if (rate == ODR_1_5625HZ) return 1.5625;
  if (rate == ODR_0_7813HZ) return 0.7813;

  Serial.println("DEAD");
  return 1;
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
}

float * stepEKF(float est, float var){
  float dtSq = (timeDelta * timeDelta) * (0.001 * 0.001);
  Serial.println("ekf");

  //Prediction Step
  float speedStep = STEPS_PER_METERS * stepperRight.speed();

  float predX = est + timeDelta * speedStep;
  float predP = var + dtSq * Q_SPEED_RATIO * STEPS_PER_METERS * stepperRight.speed();

  //Mesurement Step
  float currAccel = currAcceleration();
  float H_k = 2/dtSq;
  float R_k = R_ACCEL_RATIO * Q_rsqrt(currODR());

  //Update Step
  float innov = currAccel - H_k * est + speed_prev * timeDelta;
  speed_prev += currAccel * timeDelta;
  float S_k = dtSq * dtSq * predP + R_k;
  float K_k = (H_k * H_k * predP) / S_k;

  float estDist = (predX + K_k * innov);
  float estVar = (1 - K_k * H_k) * predP;
  static float estimates[2] = {estDist, estVar};
  return estimates;
}



void Task1code(void* pvParameters) {
  for(;;){
    stepperLeft.runSpeed();
    stepperRight.runSpeed();
  }
}


void loop() {
  endTime = millis();
  timeDelta = ((float)(endTime - startTime));
  updateSensors();
  Serial.print("");
  if(timeDelta > 500){
    Serial.print(currODR());
    Serial.print(aevent.acceleration.y);
    Serial.print(" ");
    Serial.println(aevent.acceleration.y - accY);


    accX = aevent.acceleration.x;
    accY = aevent.acceleration.y;
    accZ = aevent.acceleration.z;
    //if(x >= 100){
      //if(stepperLeft.speed() == 0)  return;
      //stepperLeft.setSpeed(0);
      //stepperRight.setSpeed(0);
    //}else{
      //Serial.println(stepperLeft.speed());
      //float *values = stepEKF(x, varX);
      //x = values[0];
      //Serial.println(x);
      //varX = values[1];
    //}
    startTime = endTime;
  }
}