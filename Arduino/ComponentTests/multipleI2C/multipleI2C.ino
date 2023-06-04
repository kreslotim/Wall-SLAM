#include "Adafruit_VL53L1X.h"
#include <Adafruit_FXAS21002C.h>
#include <Adafruit_FXOS8700.h>
#include <Adafruit_Sensor.h>


#define IRQ_PIN 2
#define XSHUT_PIN 3

#define SDA 21
#define SCL 22

#define SDA_1 26
#define SCL_1 27

// two lidars (Front and Back)
Adafruit_VL53L1X vl53b = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);
Adafruit_VL53L1X vl53f = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);

/* Assign a unique ID to this sensor at the same time */
Adafruit_FXAS21002C gyro = Adafruit_FXAS21002C(0x0021002C);
Adafruit_FXOS8700 accelmag = Adafruit_FXOS8700(0x8700A, 0x8700B);

void setup() {
  Serial.begin(115200);
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



  if (! vl53f.begin(0x29, &Wire1)) {
    Serial.print(F("Error on init of Right VL sensor: "));
    Serial.println(vl53f.vl_status);
    while (1)       delay(10);
  }
  if (! vl53b.begin(0x29, &Wire)) {
    Serial.print(F("Error on init of Left VL sensor: "));
    Serial.println(vl53b.vl_status);
    while (1)       delay(10);
  }

  Serial.println(F("VL53L1X sensor OK!"));

  Serial.print(F("Front Sensor ID: 0x"));
  Serial.println(vl53f.sensorID(), HEX);
  Serial.print(F("Back Sensor ID: 0x"));
  Serial.println(vl53b.sensorID(), HEX);
  

  if (! vl53f.startRanging()) {
    Serial.print(F("Front Couldn't start ranging: "));
    Serial.println(vl53f.vl_status);
    while (1)       delay(10);
  }
  if (! vl53b.startRanging()) {
    Serial.print(F("Back Couldn't start ranging: "));
    Serial.println(vl53b.vl_status);
    while (1)       delay(10);
  }
  Serial.println(F("Ranging started"));

  // Valid timing budgets: 15, 20, 33, 50, 100, 200 and 500ms!
  vl53b.setTimingBudget(50);
  vl53f.setTimingBudget(50);
  Serial.print(F("Timing budget (ms): "));
  Serial.println(vl53b.getTimingBudget());

  /*
  vl.VL53L1X_SetDistanceThreshold(100, 300, 3, 1);
  vl.VL53L1X_SetInterruptPolarity(0);
  */
}

void loop() {
  int16_t distanceFront;
  int16_t distanceBack;
  
  getEventGAM();

  if (vl53f.dataReady()) {
    // new measurement for the taking!
    distanceFront = vl53f.distance();
    if (distanceFront == -1) {
      // something went wrong!
      Serial.print(F("Couldn't get Front distance: "));
      Serial.println(vl53f.vl_status);
      return;
    }
    Serial.print(F("Distance Front: "));
    Serial.print(distanceFront);
    Serial.println(" mm");

    // data is read out, time for another reading!
    vl53f.clearInterrupt();
  }

  if (vl53b.dataReady()) {
    // new measurement for the taking!
    distanceBack = vl53b.distance();
    if (distanceBack == -1) {
      // something went wrong!
      Serial.print(F("Couldn't get Back distance: "));
      Serial.println(vl53b.vl_status);
      return;
    }
    Serial.print(F("Distance Back: "));
    Serial.print(distanceBack);
    Serial.println(" mm");

    Serial.println(" ");

    // data is read out, time for another reading!
    vl53b.clearInterrupt();
  }

    delay(10);

}

void getEventGAM() {
  /* Get a new sensor event */
  sensors_event_t event;
  sensors_event_t aevent, mevent;

  /* Get a new sensor event */
  gyro.getEvent(&event);
  accelmag.getEvent(&aevent, &mevent);

  /* Display the results (speed is measured in rad/s) */
  Serial.print("G ");
  Serial.print("X: ");
  Serial.print(event.gyro.x);
  Serial.print("  ");
  Serial.print("Y: ");
  Serial.print(event.gyro.y);
  Serial.print("  ");
  Serial.print("Z: ");
  Serial.print(event.gyro.z);
  Serial.print("  ");
  Serial.println("rad/s ");
  //delay(500);

  /* Display the accel results (acceleration is measured in m/s^2) */
  Serial.print("A ");
  Serial.print("X: ");
  Serial.print(aevent.acceleration.x, 4);
  Serial.print("  ");
  Serial.print("Y: ");
  Serial.print(aevent.acceleration.y, 4);
  Serial.print("  ");
  Serial.print("Z: ");
  Serial.print(aevent.acceleration.z, 4);
  Serial.print("  ");
  Serial.println("m/s^2");

  /* Display the mag results (mag data is in uTesla) */
  Serial.print("M ");
  Serial.print("X: ");
  Serial.print(mevent.magnetic.x, 1);
  Serial.print("  ");
  Serial.print("Y: ");
  Serial.print(mevent.magnetic.y, 1);
  Serial.print("  ");
  Serial.print("Z: ");
  Serial.print(mevent.magnetic.z, 1);
  Serial.print("  ");
  Serial.println("uT");

  Serial.println("");

  delay(500);
}
