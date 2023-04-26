// Define pin numbers for the sensors
int orientation = 0;
int distance = 0;

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
}

void loop() {

  int x_car = random(200)-100;
  int y_car = random(200)-100;
  
  
  for (int angle = 100; angle < 170; angle += 5) {
      // Convert sensor values to the desired format
      String output = String(angle) + ", " + String(random(101)) + "," + String(x_car) +","+ String(y_car);

      // Print the formatted sensor values to the serial plotter
      Serial.println(output);

      // Delay for a short period to prevent flooding the serial plotter
      delay(10);
  }

  delay(3000);

}
