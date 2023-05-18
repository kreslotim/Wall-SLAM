float x;    // Position X
float y;    // Position Y

bool onX;

static float B = 0.01;  // ticksToMeters
static float A = 1;  
static float C = 1;     // x -> y

static float Q = 1;     // Procees Noise Variance
static float R = 1;     // Mesurement Noise

float prevVarX;
float prevVarY;


void setup() {
  x = 0;
  y = 0;
  
  onX = True;

  prevVarX = 1;
  prevVarY = 1; 
}

void loop() {
  
  float mesuredDistance = 5;  // add IMU distance
  float ticksDone = 5;        // ticks done since last time

  if(onX){
    float kalman[] = kalmanFilterStep(ticksDone, x, prevVarX, mesuredDistance);

    x = kalmam[0]
    prevVarX = kalman[1]
  }else{
    float kalman[] = kalmanFilterStep(ticksDone, y, prevVarY, mesuredDistance);

    y = kalmam[0]
    prevVarY = kalman[1]
  }

}


float predDistance(float ticks, float prevEstimate){
  return ticksToMeters*ticks + A*prevEstimate;
}


float kalmanFilterStep(float ticks, float prevEst, float prevVar, float mesureD){

  //Prediction Step
  float pDis = predDistance(ticks, prevEst);
  float pVar = A * prevVar * A + Q;

  //Update Step
  float K = pVar * C / (C * pVar * C + R);
  float kEst = pDis + K * (mesX - C * pDis)
  float kVar = (1 - K * C) * pVar

  //Returning values
  float kalmanValues[2] = {kEst, kVar}
  return kalmanValues
}