#include <CheapStepper.h>

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


CheapStepper Rstepper (rIN1,rIN2,rIN3,rIN4);
CheapStepper Lstepper (lIN1,lIN2,lIN3,lIN4);

void setup()
{
  
  Rstepper.setRpm(20);
  Lstepper.setRpm(20); 
  
}

void loop() {

Rstepper.moveDegreesCW (180);
Lstepper.moveDegreesCW (180);
delay(1000); 
Rstepper.moveDegreesCCW (180);
Lstepper.moveDegreesCCW (180);
delay(1000);  
}