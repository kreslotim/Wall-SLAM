#include <Adafruit_FXAS21002C.h>
#include <Adafruit_FXOS8700.h>
#include <Adafruit_Sensor.h>


/* Assign a unique ID to this sensor at the same time */
Adafruit_FXAS21002C gyro = Adafruit_FXAS21002C(0x0021002C);
Adafruit_FXOS8700 accelmag = Adafruit_FXOS8700(0x8700A, 0x8700B);

// Define sensor event objects
sensors_event_t gyroEvent;
sensors_event_t accelmagEvent;

// Define sensor data arrays
float accelX, accelY, accelZ;
float gyroX, gyroY, gyroZ;
float magX, magY, magZ;

// Define orientation variables
float yaw, pitch, roll;

// Define complementary filter variables
float prevYaw = 0;

float alpha = 1;

void setup() {
  Serial.begin(115200);

  Wire.begin();
  
  // Initialize sensors
  if(!gyro.begin())
  {
    Serial.println("Failed to initialize gyroscope!");
    while(1);
  }
  if(!accelmag.begin())
  {
    Serial.println("Failed to initialize accelerometer/magnetometer!");
    while(1);
  }
  
  // Set accelerometer range to 4G
  //accelmag.setAccelerometerRange(LIS3DH_RANGE_4_G);
  
  // Set gyroscope range to 250 DPS
  //gyro.setRange(FXAS21002_RANGE_250DPS);
}

void loop() {

  sensors_event_t event;
  sensors_event_t aevent, mevent;

    // Read sensor data
    gyro.getEvent(&event);
    accelmag.getEvent(&aevent, &mevent);
  
  // Extract sensor data
  accelX = aevent.acceleration.x;
  accelY = aevent.acceleration.y;
  accelZ = aevent.acceleration.z;
  
  gyroX = event.gyro.x;
  gyroY = event.gyro.y;
  gyroZ = event.gyro.z;

  //if (0 <= gyroZ && gyroZ <= 0.02) gyroZ = 0;
  
  magX = mevent.magnetic.x;
  magY = mevent.magnetic.y;
  magZ = mevent.magnetic.z;
  
  // Calculate orientation using accelerometer and magnetometer data
  pitch = atan2(-accelX, sqrt(accelY * accelY + accelZ * accelZ)) * 180 / PI;
  roll = atan2(accelY, accelZ) * 180 / PI;

  yaw = prevYaw + gyroZ * (1/100.);
  prevYaw = yaw;

  float heading = (180*atan2(magY,magX)/PI) * alpha;
  Serial.println("Heading: " + String(heading));

  //Serial.println("X: " + (String)magX);
  //Serial.println("Y: "+ (String)magY);
  //Serial.println("Yaw: " + String(yaw));
  Serial.println("GyroHeading: "+String(yaw));
  //Serial.println(gyroZ);
  //Serial.print("Pitch: ");
  //Serial.println(pitch);
  //Serial.print("Roll: ");
  //Serial.println(roll);
  
  delay(10);
}