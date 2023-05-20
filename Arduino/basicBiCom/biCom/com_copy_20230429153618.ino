#include <math.h>

// State variables
double x_hat1 = 0.0;  // Estimated position of object 1
double x_hat2 = 0.0;  // Estimated position of object 2
double P1 = 1.0;     // State covariance of object 1
double P2 = 1.0;     // State covariance of object 2

// Process noise and measurement noise
double Q = 0.1;      // Process noise covariance
double R = 1.0;      // Measurement noise covariance

// Kalman gain
double K1, K2;

// Measurement variables
double z1 = 0.0;     // Measured position of object 1
double z2 = 0.0;     // Measured position of object 2

void setup() {
  // Initialize any required hardware or variables
  Serial.begin(9600);
}

void loop() {
  // Simulate measurements (replace these with your own measurements)
  z1 = sin(millis() / 1000.0);
  z2 = cos(millis() / 1000.0);

  // Perform the EKF steps
  predictState();
  updateState();

  // Print the estimated positions
  Serial.print("Object 1: ");
  Serial.print(x_hat1);
  Serial.print(" | Object 2: ");
  Serial.println(x_hat2);

  // Wait for a brief moment before the next iteration
  delay(100);
}

// Update the state estimate based on the measurements
void updateState() {
  // Step 1: Calculate the innovations
  double y1 = z1 - x_hat1;
  double y2 = z2 - x_hat2;

  // Step 2: Calculate the Kalman gains
  K1 = P1 / (P1 + R);
  K2 = P2 / (P2 + R);

  // Step 3: Update the state estimates
  x_hat1 += K1 * y1;
  x_hat2 += K2 * y2;

  // Step 4: Update the state covariances
  P1 = (1 - K1) * P1;
  P2 = (1 - K2) * P2;
}

// Predict the next state estimate based on system dynamics
void predictState() {
  // Step 1: Predict the state estimates
  double x_pred1 = x_hat1;
  double x_pred2 = x_hat2;

  // Step 2: Predict the state covariances
  double P_pred1 = P1 + Q;
  double P_pred2 = P2 + Q;

  // Step 3: Update the state estimates and covariances
  x_hat1 = x_pred1;
  x_hat2 = x_pred2;
  P1 = P_pred1;
  P2 = P_pred2;
}


