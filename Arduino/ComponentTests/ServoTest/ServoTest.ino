#include <ESP32Servo.h>

#define servoPin 15
Servo servo;
int val = 0;
int angle = 86;

int direction = 1;

void setup() {
  // put your setup code here, to run once:
  servo.attach(servoPin);
  Serial.begin(115200);

}

void loop() {
  //rotateServo();
  controlServo();
}

void rotateServo() {
  angle += direction;
  if (angle > 180 || angle < 0) {
    direction *= -1;
  }
  servo.write(angle);
  Serial.println(angle);
  delay(10);
}

void controlServo() {
  while (Serial.available() == 0) {}
  val = Serial.parseInt();
  servo.write(val);
  angle = servo.read();
  Serial.println(angle);
}
