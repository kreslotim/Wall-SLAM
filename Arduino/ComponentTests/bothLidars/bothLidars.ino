#include "Adafruit_VL53L1X.h"
#include <Adafruit_FXAS21002C.h>
#include <Adafruit_FXOS8700.h>
#include <Adafruit_Sensor.h>


#define IRQ_PIN 2
#define XSHUT_PIN 3

#define SDA_1 26
#define SCL_1 27

#define SDA_2 33
#define SCL_2 25

Adafruit_VL53L1X vl53b = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);
Adafruit_VL53L1X vl53f = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);

TwoWire I2Ctwo = TwoWire(1);

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  Serial.println(F("Adafruit VL53L1X sensor demo"));

  Wire.begin();
  //Wire1.begin(SDA_2,SCL_2);

  
  if (! vl53f.begin(0x29, &Wire)) {
    Serial.print(F("Error on init of Right VL sensor: "));
    Serial.println(vl53f.vl_status);
    while (1)       delay(10);
  }

  Serial.println(F("VL53L1X sensor OK!"));

  Serial.print(F("Left Sensor ID: 0x"));
  Serial.println(vl53b.sensorID(), HEX);
  Serial.print(F("Right Sensor ID: 0x"));
  Serial.println(vl53f.sensorID(), HEX);

  if (! vl53b.startRanging()) {
    Serial.print(F("Left Couldn't start ranging: "));
    Serial.println(vl53b.vl_status);
    while (1)       delay(10);
  }
  if (! vl53f.startRanging()) {
    Serial.print(F("Right Couldn't start ranging: "));
    Serial.println(vl53f.vl_status);
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
  int16_t distanceBack;
  int16_t distanceFront;

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

    // data is read out, time for another reading!
    vl53b.clearInterrupt();
  }

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

    Serial.println(" ");

    // data is read out, time for another reading!
    vl53f.clearInterrupt();
  }

    delay(10);

}
