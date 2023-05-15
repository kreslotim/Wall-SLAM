#include "Adafruit_VL53L1X.h"

#define IRQ_PIN 2
#define XSHUT_PIN 3

#define SDA_2 26
#define SCL_2 27

Adafruit_VL53L1X vl53l = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);
Adafruit_VL53L1X vl53r = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  Serial.println(F("Adafruit VL53L1X sensor demo"));

  Wire.begin();

  Wire1.begin(SDA_2,SCL_2);

  if (! vl53l.begin(0x29, &Wire)) {
    Serial.print(F("Error on init of Left VL sensor: "));
    Serial.println(vl53l.vl_status);
    while (1)       delay(10);
  }
  if (! vl53r.begin(0x29, &Wire1)) {
    Serial.print(F("Error on init of Right VL sensor: "));
    Serial.println(vl53r.vl_status);
    while (1)       delay(10);
  }
  Serial.println(F("VL53L1X sensor OK!"));

  Serial.print(F("Left Sensor ID: 0x"));
  Serial.println(vl53l.sensorID(), HEX);
  Serial.print(F("Right Sensor ID: 0x"));
  Serial.println(vl53r.sensorID(), HEX);

  if (! vl53l.startRanging()) {
    Serial.print(F("Left Couldn't start ranging: "));
    Serial.println(vl53l.vl_status);
    while (1)       delay(10);
  }
  if (! vl53r.startRanging()) {
    Serial.print(F("Right Couldn't start ranging: "));
    Serial.println(vl53r.vl_status);
    while (1)       delay(10);
  }
  Serial.println(F("Ranging started"));

  // Valid timing budgets: 15, 20, 33, 50, 100, 200 and 500ms!
  vl53l.setTimingBudget(50);
  vl53r.setTimingBudget(50);
  Serial.print(F("Timing budget (ms): "));
  Serial.println(vl53l.getTimingBudget());

  /*
  vl.VL53L1X_SetDistanceThreshold(100, 300, 3, 1);
  vl.VL53L1X_SetInterruptPolarity(0);
  */
}

void loop() {
  int16_t distanceLeft;
  int16_t distanceRight;

  if (vl53l.dataReady()) {
    // new measurement for the taking!
    distanceLeft = vl53l.distance();
    if (distanceLeft == -1) {
      // something went wrong!
      Serial.print(F("Couldn't get Left distance: "));
      Serial.println(vl53l.vl_status);
      return;
    }
    Serial.print(F("Distance Left: "));
    Serial.print(distanceLeft);
    Serial.println(" mm");

    // data is read out, time for another reading!
    vl53l.clearInterrupt();
  }

  if (vl53r.dataReady()) {
    // new measurement for the taking!
    distanceRight = vl53r.distance();
    if (distanceRight == -1) {
      // something went wrong!
      Serial.print(F("Couldn't get Right distance: "));
      Serial.println(vl53r.vl_status);
      return;
    }
    Serial.print(F("Distance Right: "));
    Serial.print(distanceRight);
    Serial.println(" mm");

    Serial.println(" ");

    // data is read out, time for another reading!
    vl53r.clearInterrupt();
  }
}
