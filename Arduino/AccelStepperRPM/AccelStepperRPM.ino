// Include the AccelStepper Library
#include <AccelStepper.h>

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


// Creates two instances
// Pins entered in sequence IN1-IN3-IN2-IN4 for proper step sequence
AccelStepper stepperRight(FULLSTEP, rIN1, rIN3, rIN2, rIN4);
AccelStepper stepperLeft(FULLSTEP, lIN1, lIN3, lIN2, lIN4);

void setup() {
  //Serial.begin(115200); // to start serial monitor

  // set the maximum speed, acceleration factor,
  // initial speed and the target position for motor Right and Left motors
  stepperRight.setMaxSpeed(maxSpeed);
  stepperRight.setAcceleration(acceleration);
  stepperRight.setSpeed(constSpeed);

  stepperLeft.setMaxSpeed(maxSpeed);
  stepperLeft.setAcceleration(acceleration);
  stepperLeft.setSpeed(-constSpeed-40);

  //stepperRight.moveTo(STEPS_PER_REV); // + on Right motor to go forward
  //stepperLeft.moveTo(-STEPS_PER_REV); // - on Left motor  to go forward

}

void loop() {

  // Change direction once the motor reaches target position
  //if (stepperRight.distanceToGo() == 0)
  //  stepperRight.moveTo(-stepperRight.currentPosition());
  //if (stepperLeft.distanceToGo() == 0)
  //  stepperLeft.moveTo(-stepperLeft.currentPosition());


  // Move the motor one step
  stepperRight.runSpeed();
  stepperLeft.runSpeed();

  //Serial.println(stepper1.currentPosition()); // to print result in serial monitor
}