#include <NewPing.h>

#define trigPin 12
#define echoPin 14

const int maxDistance = 400; // in cm

NewPing sonar (trigPin, echoPin, maxDistance);
void setup() {
  Serial.begin(9600);
  delay(50);
}

int distance = 0;

void loop() {
  distance = sonar.ping_cm();
  Serial.print("Ultrasonic distance: ");
  Serial.println(distance);
}
