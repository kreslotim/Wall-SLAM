#include <NewPing.h>

const int trigPin = 22;
const int echoPin = 23;

const int IN1 = 13;
const int IN2 = 12;
const int IN3 = 14;
const int IN4 = 27;

float range = 100; //cm
int distance = 0;
NewPing sonar (trigPin, echoPin, range);

void setup() {
Serial.begin(9600);
delay(50);
pinMode(IN1, OUTPUT);
pinMode(IN2, OUTPUT);
pinMode(IN3, OUTPUT);
pinMode(IN4, OUTPUT);

}

void loop() {

distance = sonar.ping_cm();
Serial.print("The Distance is: ");
Serial.println(distance);

digitalWrite(IN1, HIGH);
digitalWrite(IN2, LOW);
digitalWrite(IN3, HIGH);
digitalWrite(IN4, LOW);
delay(2000);
digitalWrite(IN1, LOW);
digitalWrite(IN2, HIGH);
digitalWrite(IN3, LOW);
digitalWrite(IN4, HIGH);
delay(2000);

}
