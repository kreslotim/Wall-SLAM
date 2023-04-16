#include <ESP32Servo.h>

Servo servo;

#define servoPin 15

void setup() {
  // put your setup code here, to run once:
  servo.attach(servoPin);
  Serial.begin(115200);
  servo.write(0);
}

int val = 0;
int angle = 0;

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() == 0) {}
  val = Serial.parseInt();
  servo.write(val);
  angle = servo.read();
  Serial.println(angle);

}
