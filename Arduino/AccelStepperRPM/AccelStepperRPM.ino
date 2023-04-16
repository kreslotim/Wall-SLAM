// Include the AccelStepper Library
#include <AccelStepper.h>

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

// Creates two instances
// Pins entered in sequence IN1-IN3-IN2-IN4 for proper step sequence
AccelStepper stepper1(FULLSTEP, lIN1, lIN3, lIN2, lIN4);
AccelStepper stepper2(FULLSTEP, rIN1, rIN3, rIN2, rIN4);

void setup() {
  //Serial.begin(115200); // to start serial monitor

  // set the maximum speed, acceleration factor,
  // initial speed and the target position for motor 1
  stepper1.setMaxSpeed(1000.0);
  stepper1.setAcceleration(50.0);
  stepper1.setSpeed(100);
  stepper1.moveTo(2038); // + on motor 1 to go backward

  // set the same for motor 2
  stepper2.setMaxSpeed(1000.0);
  stepper2.setAcceleration(50.0);
  stepper2.setSpeed(100);
  stepper2.moveTo(-2038); // - on motor 2 to go backward
}

void loop() {
  // Change direction once the motor reaches target position
  if (stepper1.distanceToGo() == 0)
    stepper1.moveTo(-stepper1.currentPosition());
  if (stepper2.distanceToGo() == 0)
    stepper2.moveTo(-stepper2.currentPosition());


  // Move the motor one step
  stepper1.run();
  stepper2.run();

  //Serial.println(stepper1.currentPosition()); // to print result in serial monitor
}