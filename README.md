# Wall-SLAM - Simultaneous Localization And Mapping

Timofey Kreslo, Sylvain Pichot, Finn MacNamara, Alonso Coaguila, Florian Dejean.

<img src = "https://github.com/kreslotim/Wall-SLAM/assets/73421792/da1ffdf1-7803-49f7-8f3c-9e4dbe255364" width = 500/>

June 2023

## Description

Wall-SLAM is a project that we have developed within the course CS-358 Making Intelligent Things, under the direction of Prof. Koch and under the supervision of Federico Stella and Anirudhh Ramesh. This report outlines the key features, methodology, challenges faced, and a detailed “How To Build” guide.

Our [project proposal](https://github.com/kreslotim/Wall-SLAM/blob/main/proposal/proposal.md), can be useful to understand some deviations in our project from our expectations.

The primary objective of the project was to build a cost-effective and compact SLAM robot capable of mapping unknown and dynamic environments.

## Overview

https://github.com/kreslotim/Wall-SLAM/assets/56829239/a7d6daf9-7e9c-4008-a5e7-d5f0c00a2a69

Main idea:

We utilize the data from the distance sensors (Ultrasonic and LIDAR), IMU (Inertial Measurement Unit) sensor, and Stepper motors to estimate the robot's pose (position and orientation) and simultaneously construct a map of the environment. All this data will be processed and then displayed on on a website that  This involved integrating data from different sensors using techniques such as sensor calibration, fusion and Kalman filtering algorithms.

## Components and supplies

- ESP32
- NXP Precision 9DoF IMU
- VL53L1X Time of Flight Distance Sensor (2x)
- HC-SR04 Ultrasonic Sensor
- 180-Degree Servo
- Stepper motor 28byj-48 (2x)
- ULN2003 motor driver (2x)
- XL6009E1 DC-DC Voltage Converter - 5V
- 9V Battery supply
- Power Switch
- 3D Prints (STLs)

## 3D Design

<img align="left" src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/6667b767-95a2-45b7-8b5e-17c26d23500b" width = 500>

As zealous devotees of the enchanting Disney’s figure Wall-E, we couldn’t resist the temptation to transform our prototype into his spitting image. But, alas, our professor promptly intervened, bursting our bubble of whimsy with a comic remark. He reminded us that while Wall-E excelled in garbage collection and exuded undeniable cuteness, our project’s aspirations extended beyond those realms. Thus, we bid farewell to our beloved Wall-E robot, sparing it from a destiny of cuteness overload and instead refocusing our efforts on more practical endeavors.

We decided to shift our focus to functionalities that would enable mapping of the surrounding environment, which is covered by SLAM. Additionally, we chose to retain the concept of tracks with wheels, as it offers enhanced precision in movement and rotation (especially the ability to turn on the spot), while opting for rubber tracks to minimize slippage during maneuvering. The adventure of building a SLAM robot starts here. Our first step is to build our robot, that we later named... Chewbacca, we will give a reason for that name at the end of the report. Meanwhile lets see how we built it. 

 <br/><br/>

### 1. Sketches

<img align = "left" src = "https://user-images.githubusercontent.com/56829239/232310112-f7f68b36-d2c5-4ecf-8979-ef074a0ed3eb.png" width = 500>

We started by sketching our ideas and figuring out how to arrange electronic components in the best way possible. Our main goal was to create a compact design that would make the assembly process easier and speed up 3D printing. This approach aimed to make the construction phase more efficient overall.

We initiated the development process by focusing on the chassis design. Subsequently, we proceeded to devise an arrangement strategy. The robot incorporated two stepper motors along with their corresponding drivers, a servo, a battery, and a micro-controller. For the initial prototype, we positioned both stepper motors at the rear section of the chassis. In order to counterbalance the weight distribution, the batteries and the micro-controller were placed at the front section. Lastly, the servo, responsible for holding the sensors, was centrally positioned within the chassis.

<img align = "left" src = "https://user-images.githubusercontent.com/56829239/232310079-931594a3-6049-4ff0-9cc0-58b74d3c37e4.png" width = 500>

This approach was promptly dismissed as it became apparent that in order to facilitate turning, both motors needed to rotate in opposite directions, necessitating the rotation of the entire car around its vertical axis.

The rotation of the machine necessitates the alignment of the servo and the primary axis of rotation. This alignment is crucial during turning maneuvers as the distance sensors are required to scan in close proximity to the adjacent wall. By maintaining the sensors in close proximity to the central axis of rotation, the objective is to minimize noise and optimize the accuracy of the scanning process.

Consequently, we proposed an alternative design to address this limitation.


This design greatly appealed to us, and we made the decision to proceed in this particular direction. During our exploration on the web, we chanced upon a robot named [SMARS](https://www.smarsfan.com/) (Screwed/Screwless Modular assemblable Robotic System), which seemed to align closely with our envisioned requirements. We found inspiration in its design and opted to incorporate a chassis that closely resembled to SMARS. To assess the feasibility of the track concept, we even went as far as designing the entire SMARS idea to evaluate its effectiveness.

Having appreciated the remarkable ingenuity behind the notion of using the printing filament as a means to securely bind the tracks together, as well as the exceptional functionality of this approach in practical implementation, we wholeheartedly adopted this design for our project. Consequently, this decision entailed the utilization of the same wheels, as the tracks had been meticulously tailored to ensure precise compatibility with these specific wheel components. This deliberate alignment not only guaranteed optimal performance but also facilitated seamless integration between the tracks and wheels, thereby fortifying the overall effectiveness of our system.

The subsequent focus of our attention revolved around the development of the chassis, and the incorporation of the battery, the motors and the sensors.

As soon as we agreed on the placement of all the components, we started designing in 3D. In order to leverage the collaborative design features, we opted to use Fusion 360, allowing for effective teamwork during the design process. Minor design changes have been made in FreeCad, in order to save time.

Here’s what we’ve come up with.
<p align = "center">
 <img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/182bb3ea-2b7f-49c3-83fd-62bc438a0f22" width = 800>
 <img align = "center" src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/4402e84b-2550-423e-8a4e-7c284bb5df46" width = 800>
</p>

Now we will explain the choice we’ve made for positioning the electronic pieces. The parts that are highlighted in green are those that we designed ourselves. The Ultrasonic sensor’s frame as well as the wheels and the tracks were borrowed from SMARS project, because they fit our requirements well.

<p align = "center">
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/9eac749d-10e7-4cae-a3eb-60efbaca4600" width = 500>
</p>

While we adopted the wheel design from SMARS ([link for STLs](https://www.thingiverse.com/thing:2662828)), we had to adapt it’s axle mount to fit the rectangular axle of the motor we are using. Furthermore, it is essential to align the axle of the slave wheel with the motor’s axle to ensure that both wheels are at the same level.

<p align = "center">
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/3dcc6850-5950-4f5f-9a45-e38546c61ef8" width = 700>
</p>
 
In order to optimize the efficiency of the printing and assembly process, we strategically positioned all the components in close proximity to one another, ensuring minimal wasted space on the chassis.

As the heaviest electronic component of the entire construction, the battery serves as a central anchor within the overall design. By positioning it at the center, we establish a stable foundation upon which the remaining components, i.e. the servo and the sensors are securely mounted and connected.

<p align = "center">
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/f2b20805-2bfe-478f-b751-ee17c3dc3ad8" width = 700>
</p>
 
The cover slides over the battery and encases the servo on top.

The servo, in return, holds both lidars (distance sensors) that are sneaked on the servo’s arm.
<p float = "left">
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/6061ea20-960f-4265-97e7-7a94cdba535c" width = 450>
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/a595e70b-5473-4abe-b3f3-71a7b0facc83" width = 450>
</p>
 
### 2. Assembly

Once the design was ready, it was printed at EPFL in DLL, and partly at home. Mostly PETG material was used, except for the tracks which were printed using FLEX rubber filament, under the consent of Sébastien Martinerie - 3D printing Coach at the SPOT. Caterpillars are connected by means of an ordinary filament in its initial form, as mentioned above.
<p align = "center">
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/243612a9-e803-44b0-9ae7-f1f7f143721a" width = 700>
</p>

To make power control easier, a switch has been added on top of the cover that holds the servo.
Given that multiple components, including the Arduino, operate at the same power level and share a common ground, the wires are soldered together in a centralized manner resembling the arrangement of an octopus

<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/0c49d524-4f6e-45af-a541-f1add8a3db69" width = 500>
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/9da87210-9a63-49e8-aca9-97f923d56dd9" width = 500>

The opposite side of the switch features the motion sensor (IMU) securely attached to the cover that holds the servo, using screws:
<p align = "center">
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/6b4e3ff5-6718-4936-b830-be0c61812fe6" width = 500>
</p>

<br/><br/>

<img align = "left" src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/550c9bed-20b3-41ab-b2bd-64b25c6ab565" width = 500>
Here the difficulty turned out to be to establish connections between numerous devices that rely on the I2C (Inter-Integrated Circuit) serial communication protocol. In particular, there was an issue with two lidars having the same address, preventing them from being connected on the same I2C bus. One possible solution would have been to use a multiplexer, but since one was not available, an alternative approach was devised through code.

<br/><br/>

To overcome this challenge, some of the ESP32 GPIOs needed to be reconfigured to function as I2C pins, to which we connected the front lidar. Subsequently, the motion sensor was connected to the standard I2C pins, and the back lidar was also connected to these same pins as well. This was possible because the motion sensor and the lidar had different addresses assigned to them, ensuring that there was no conflict in their communication over the shared I2C bus. Finally, to ensure proper insulation and protection, we applied heat shrink tubing at the junction point where the three wires met.

<br/><br/>
<br/><br/>

A detailed circuit diagram of all connections is shown below:

<p align = "center">
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/c93e14a5-a572-4767-83b8-24d0dcf6c076">
</p>

In conclusion, the assembly of our car involved strategically placing two lidars on top of a servo that rotated around the same vertical axle as the car itself. This configuration enabled us to detect obstacles within a proximity of 4 meters by performing a single 180-degree servo rotation. 

Additionally, we positioned an ultrasonic sensor at the front of the car, ensuring continuous forward movement while avoiding potential collisions. If an obstacle was detected directly in the car's trajectory, the sensor would halt the motors, allowing the program to recalibrate and determine an alternate path for the car to follow. These careful arrangements and sensor placements greatly enhanced the car's obstacle detection and navigation capabilities, ensuring a safer and more efficient operation.

### 3. Problems and Risks

There were several risks and issues we encountered during the project, primarily related to the management of batteries. One significant problem arose from the frequent changing of batteries, which required manipulating multiple components and wires. In hindsight, it would have been more advisable to use a LIPO battery that offers greater stability and ease of use. 

Additionally, a critical mistake was made when we placed the voltage regulator on a very thin layer of double-sided tape directly attached to the battery case, which had metal circles on its surface. This design flaw led to a potential short circuit between the six batteries and the voltage regulator when components were pushed against each other. This short circuit had the potential to cause severe damage to the entire system and possibly lead to its complete failure or even a fire hazard.

Therefore, we implemented a solution by adding a small cardboard spacer to provide insulation and maintain a safe distance between the electronic components.

Another significant issue we faced was related to the control of the steppers, which proved to be too slow for our project's requirements. While the car moved at a slow pace, the map updates occurred rapidly, causing a bottleneck in our system. Initially, we chose these specific steppers to ensure precise positioning. 

However, this decision posed challenges as the tracks on which the car operated became increasingly loose over time. Prolonged use resulted in the tracks losing their elasticity, leading to deviations from a straight line. Specifically, one side of the car moved faster than the other, exacerbating the issue of maintaining a consistent trajectory. By securing the tracks with the elastic bands, we effectively restored the required tension and stability, mitigating the issue of one side of the car moving faster than the other.

In retrospect, alternative steppers with higher speed capabilities could have been a more suitable choice to address this problem.

## Data & Algorithm Software

Unfortunately, the SLAM algorithm is too memory-bound and computationally slow for a microcontroller. To address this issue, we have the microcontroller connect via Wi-Fi to a capable external computer called the Command Computer (CC). This is why the microcontroller used has Wi-Fi capability. The Wi-Fi connection also allows the robot to move freely. Therefore, the microcontroller only receives commands movement and returns sensor data to the CC. 

**The different tools** we developed for this are:

### 1. **Web Interface**

To see in real time the advancement of the mapping and for debugging purpose, we made a complete interface that display every step of the data flow. To do so, we are using Flask, Plotly and bootstrap.

<img src = "Pictures/Mozilla Firefox 2023-06-04 16-34-36 - Trim.gif">
 
*Sample setup*

- *Communication frequency* : shows the number of data packages sent and received, as well as the number of obstacles detected.
- Orientation Line Chart: shows the sensor fusion of the accelerometer and magnetometer and its variation.
- *Noisy Obstacle Detection*: This is a map without any filter, displaying every data point no matter how weird it is. This allows us to clearly see how much data we filter out.
- *Redundancy Check*: This is a map that has undergone a first cleanup.
- *K-Mean Graph*: This map is a visual representation of obstacles. With some basic machine learning that we have optimized, we can map and understand the environment with greater ease. The path calculated using Dijkstra is display with the current position and the togo position.

### 2. **The Different Algorithms**

To navigate and treat the data we receive from the robot we have elaborated different algorithms to efficiently put them to use. 

- **Pathfinding Algorithm:**
    
    We used Dijkstra's algorithm which is a popular pathfinding algorithm used to find the shortest path between two nodes in a graph with non-negative edge weights. We applied more weights to nodes if there was a change in direction (due to the fact that our robot loses a lot of time during turns, and also imprecision adding up with the turns) and less to the nodes that the robot hasn’t visited yet. 
    
    To create the graph with the nodes, we run K-means on the list of filtered obstacles. We then render the node inaccessible if the cell containt an obstacle/cluster calculated by Kmean. Kmean also determines the best targeted position (more detail on that below).
    
    One challenge was to translate global instructions into instructions that the car can understand, which are limited to goForward(), turnLeft(), and turnRight(). Hence, we ran Djikstra every 0.5 seconds to find the new best move to apply to the robot depending on its current position and orientation. This solution is costly, but is robust since imagine if all of a sudden we remove an obstacles the robot sees that there is immediately a new optimal path. This hence enabled the robot to react to it’s environment.
    
    *Photo of the Pathfinding Algorithm in action right below…*
    
- **Map - kmean.py and mapK.py**
<p float = "left">
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/73421792/78efdc26-d8c6-4f3f-8294-cb8b9af3a81c" width = 500>
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/73421792/00b7bc57-6bfb-498e-97f6-08204f556cb7" width = 500>
</p>

   In order to determine if there is a real obstacle, we are using kmean algorithm to determine their position and center. Finding those center are useful to move to the less dense zone, the zone that is unexplored or empty. Due to our Djikstra algorithm, we added high weight to already explore area, hence resulting in a path that will always try to explore. If a path cannot explore anymore, this mean we have map the whole area.
    
   - Kmean try to assign K cluster to a data set and optimize the distance between the point from a center.
       - To determine the best K, so our number of obstacle, we run multiple time the algorithm and look for the minimal distance of the cluster related to their center. ***(Elbow method)***
        - To initiate our center, we already approximate where the center should be ***(kmean ++).*** Then we move again the center to approach the center of mass better till we converge.
    
   - In order to reduce noise, which can be seen as the outlier and stand alone point in our dataset, we slice our data randomly before training kmean. If a cluster is assign less than a fixed number of point, we will modify the label to be considered as a noisy cluster, represented with the red dots on the above graphic.
    
   - To represent an obstacle, we decided to turn them into rectangle taking the minimum and maximum. This lead to more strict threshold since our obstacle are hollow shape and to create multiple rectangle for one obstacle depending on its size.
    
   **kmean.py** handle all the necessary function to run the kmean++ algorithm and the Elbow method using numpy.
    
   **mapk.py** handle how to interpret this data in your main app.
    
- **Noise Correction - Kalman**
    
    In order to combine our sensor, we utilize known variance of them to correct sudden noise.
    
    - Using the acceleration from the IMU, the actual speed of the robot can be determined for a short period. A better estimate can be determined with a Kalman filter by combing the IMU measurements and the speed inputted in the steppers. What the Kalman filter does is an estimate by combining our prediction of speed and the correlated measurement of acceleration through the covariance of our prediction and our measurements. The covariance was gathered from the documentation from the physical components, being the IMU and the stepper motors. Unfortunately, we could not accurately implement a Kalman filter due to multiple reasons. First of all, the stepper motors lacked proper and clear documentation regarding their covariance regarding their position and speed so this led to estimating a covariance. Second of all, we lacked experience with developing Kalman filters. Third of all, the stepper motors are too precise and the IMU is too imprecise, rendering fine tuning very difficult. Each reason exacerbated the next one. The final straw was when it was found that multiplying a scalar to the steps done by the stepper motor was more precise and requires less computation. Nevertheless, we believe that a Kalman filter is possible to implement for the simultaneous localization but given that a simpler and more efficent solution provided with better results than the prototype. If a Kalman filter were to be implemented, we would recommend replacing the stepper motors with an alternative.
    
    - We successfully utilized fusion algorithms combining the magnetometer and gyroscope of the IMU to compute a highly accurate heading orientation. Among the available filters, the Mahony filter provided the fastest results but lacked precision, while the Madgwick and NXP Sensor Fusion filters offered greater accuracy at the cost of slower computation.
        
        In our implementation, we employed the [NXP Sensor Fusion](https://github.com/adafruit/Adafruit_AHRS/blob/master/examples/calibration/NXP_FXOS_FXAS.h) algorithm, which was developed by the creators of the [Adafruit IMU](https://cdn-learn.adafruit.com/downloads/pdf/nxp-precision-9dof-breakout.pdf) we utilized. By leveraging this precise heading calculation, we implemented an autocorrection mechanism using a Kalman filter for the car's orientation. Every period of time, we checked if the orientation difference exceeded a predefined threshold, prompting us to adjust the stepper motor with a constant number of steps. 
        
        This autocorrection was necessary due to the loose tracks on which our car operated. Initially, the freshly printed rubber filament tracks performed flawlessly until they were stretched too much, reducing their elasticity and causing them to scroll in empty space. As a result, one side of the car moved slower than the other, leading to slight deviations from a straight line. 
        
        To demonstrate the effectiveness of the Kalman filter on the orientation, a graph displaying three different orientations is presented on the web interface. It is evident that the gyroscope-based orientation exhibits significant deviation, while the magnetometer-based orientation closely matches the precision achieved by the heading computed using the Kalman Filter. 
        
- **Data Validation - Redundancy**
    
    In order to check if a data point was even ready to be considered an obstacle in the real life, we perform a redundancy check. A simple check if the obstacle is still present or a check to see if there is enought detection points for it to be considered as an actual obstacles before giving the the list of points to as an input for K-means 
    
    *Here is a the graph without the filter:*  
    ![noisy_example](https://github.com/kreslotim/Wall-SLAM/assets/73421792/e273c981-825e-441b-81e7-4f7f59a3de8a)

    *Here it is with the filter (the lump present in [0,200] is the charging cable attached to the car with is accidental and not present in the photo with the observed obstacles):*
    ![filter_example](https://github.com/kreslotim/Wall-SLAM/assets/73421792/951d0479-695e-4062-83f1-0511c76d06bd)


### 3. **TCP Connection ESP32 ↔ CC (Python)**

In order to process our data, we utilize a python code that run intensive computation and take avoid the heavy computation from the ESP32. To do that we need to have great connectivity between the two : esp32.py and espComm.ino are the two files responsible of communication.

- *EspComm.ino*  : Sets up a WIFI access point to allow the CC to connect. It opens two ports, a sending port and a receiving port. This prevents us from mixing the data up. The code sets up an Access Point using the ESP32's built-in WiFi capabilities. It creates a server to receive data on one port and send data on another port.
    
    ```arduino
    //Open Wifi Port
    WiFiServer sendServer(SEND_DATA_PORT);
    WiFiServer recieveServer(RECIEVE_DATA_PORT);
    
    //Open WifiClients
    WiFiClient sendClient;
    WiFiClient recieveClient;
    
    // Configure IP addresses of the local access point
    IPAddress local_IP(192, 168, 1, 22);
    IPAddress user_IP(192, 168, 1, 23);
    
    IPAddress gateway(192, 168, 1, 5);
    IPAddress subnet(255, 255, 255, 0);
    
    void setup() {
      // Access Point SetUp
      WiFi.softAPConfig(local_IP, gateway, subnet);
      WiFi.softAP(ssid, password);
    
      // WifiServer Setup
      sendServer.begin();
      recieveServer.begin();
    	...
    ```
    
    The interesting part about the Arduino connection is the problem we had with running the motors simultaneously with the data connection. The Arduino data transfer needed some time to run, on the other hand the stepper motors needed instructions as fast as possible due to the fact that we were stepping them step by step (check the AccelStepper.h library for more: [https://www.airspayce.com/mikem/arduino/AccelStepper/classAccelStepper.html](https://www.airspayce.com/mikem/arduino/AccelStepper/classAccelStepper.html)). The two pieces of code couldn’t run on the same core so we utilize the Arduino’s second code 
    
    ```arduino
    void setup(){
    	...
    	// Setup core to Move
      xTaskCreatePinnedToCore(
        Task1code, /* Task function. */
        "Task1",   /* name of task. */
        10000,     /* Stack size of task */
        NULL,      /* parameter of the task */
        1,         /* priority of the task */
        &Task1,    /* Task handle to keep track of created task */
        1);        /* pin task to core 0 */
      ...
    }
    
    void Task1code(void* pvParameters) {
      for (;;) {
        action(actionNumber);
      }
    }
    
    void loop() {
      if(WiFi.softAPgetStationNum() == 1){
        sendData();
        readData();
        delay(10);
      } 
    }
    ```
    
    Fun fact ‘loop()’ is running by default on core 0. Here with this setup Task1Code is running on core 1. Here is a link for more information about how to set up an ESP32 with two cores : [https://randomnerdtutorials.com/esp32-dual-core-arduino-ide/](https://randomnerdtutorials.com/esp32-dual-core-arduino-ide/)
    
    We quickly dove in other methods of connection :
    
    - We tried having our the ESP32 connect throug our access point created by our laptop, but our amazing firewall prevented us from using the ports directly. To prevent any security issue we decided not to play around with it. 
    
    - We tried Bluetooth connection as well. Unfortunately even if we were able to successfully create the link with the computer the fact that we only had one port we got a lot of data confused. So we decided to stick with the ESP32 just creating an access point.
    
- *Esp32.py* : This automatically connect to the WIFI generated by the EspComm.ino.
    
    ```python
    import pywifi
    def connect_to_wifi(self):
            iface = wifi.interfaces()[0]  # Get the first available network interface
    
            iface.disconnect()  # Disconnect from any existing Wi-Fi connection
            time.sleep(1)
    
            profile = pywifi.Profile()  # Create a new Wi-Fi profile
            profile.ssid = self.ssid   # Set the SSID (Wi-Fi network name)
            profile.auth = pywifi.const.AUTH_ALG_OPEN  # Set the authentication algorithm
    
            # Set the encryption type and password
            profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
            profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
            profile.key = self.password
    
            iface.remove_all_network_profiles()  # Remove all existing profiles
            temp_profile = iface.add_network_profile(profile)  # Add the new profile
    
            iface.connect(temp_profile)  # Connect to the network
            time.sleep(5)
    
            return iface.status() == pywifi.const.IFACE_CONNECTED # if the connection is sucessfull or not
    ```
    
    Once connected we will listen for any socket communication and if the Esp sent a message we will be able to get it’s IP. 
    
    ```python
    while self.espIP is None:
                try:
                    self.get_info= socket.socket()
                    self.get_info.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.get_info.bind(('0.0.0.0', self.recv_port))  # bind to a local address and port
                    self.get_info.settimeout(3.0)  # set a timeout of 3 seconds
                    self.get_info.listen(0)  # start listening for incoming connections
                    self.recv_socket, client_address = self.get_info.accept() # Wait to receive a transmission
                    self.get_info.close() # Close the socket 
                    self.espIP = client_address[0] # From the answer, get the IP assign to this device
                except Exception as e:
                    print(f"No information was sent by ESP, retrying... {e}")
    ```
    
    Next we will create another socket to be able to send command to the Esp too
    
    ```python
    self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.send_socket.settimeout(5)  # set a timeout of 2 seconds
    self.send_socket.connect((self.espIP, self.send_port))
    ```
    Then to read or sent data, we can simple run those command. We will pin a thread to constantly run __listen().
    
    
    ```python
    def __listen(self):
            while self.running:
                if self.connected:
                    try:
                        # Receive data from the client socket
                        data = self.recv_socket.recv(48)
                        if data:         
                            data_decoded = struct.unpack('ffffffffffff', data)
                            # Use the data 
    	                        ....
    
                    except Exception as e:
                             print("Connection error :", e)
    												 self.connected = False
    ```
    
    Here, this code is responsible for sending an action number over a socket and waiting for a response from an ESP32 device. It handles connection errors and provides success/failure status codes.
    
    ```python
    def __send_actionNumber(self, actionNumber):
            if self.connected:
                try:
                    # Send the packed angles over the socket
                    data = struct.pack('f', actionNumber)
                    self.send_socket.sendall(data)      
                    response = 0
    
                    while (not response == "200") :            
                        response = self.send_socket.recv(1024).decode()   
                        print("Received response from ESP32:", response)
    
                except Exception as e:
                    print("Connection error :", e)
                    self.connected =False
                    return 400   # Connection failed   
                return response # Sucess, will output code 200
            return 400 # Connection failed
    ```
    
    In case of failure, a thread will be tasked to restart the connection procedure and turn the boolean self.connected to true again.
    
    Below you can find the UML diagram that we designed and used as a reference to coding our classes:
    

### Problems and Risks

One of the main issues we ran into, is the instability of the connection. In early stage of the project, we had to manually connected to Wifi, due to frequent reboot of the esp, our OS refused to directly reconnect leading to wait a few minute for between every try. The solution we found was to force the reconnection by using a python library.

### 4. Simulation

At an earlier stage of the project, we tried to create a simulation to test different algorithms but unfortunately we had to divert our attention to other aspects. Nevertheless a prototype was developed, in which the robot is represented as a point mass and the landmarks are a string of 2d points.

To simulate the LIDAR that the robot used, we created a python class with static methods to handle the light collisions with Numpy with the shapes called Geometry which was called by the Playground class which would contain all the landmarks which was called by the Rover class which represents the robot. To get a better picture of the area, the rover could move from point to point. To add some realism, every time rover scanned it would add a noise random varialbe that is ajustable with a modifiable scalar.

![simulation](https://github.com/kreslotim/Wall-SLAM/assets/100040759/df899282-23aa-4720-8ff3-f07543068743)

As mentioned before, we ended up not using the simulation much, with hindsight, we admit that it was not useful within the time frame we had. Maybe if the time frame was bigger, we could have used it to develop the the navigation algorithmns, it could have helped with not having to depend on the robot for more realistic tests and allow parrallel workflows.

### 5. Software Overview

![software_overview](https://github.com/kreslotim/Wall-SLAM/assets/73421792/5a94ce7e-97e6-4e1b-a4b2-8adc71c75500)

### 6. Problems and Risks

Due to how little testing we were able to do in real scenarios, our kmean hyperparameters may not fit for a complete mapping or may need to be adjusted depending of the size explored.

## Why Chewbacca ?
We decided to named our robot Chewbacca, with all his wiring they just look similar. Chewbacca has problem navigating around his surrounding with all of hair covering his eye just like our robot. Chewbacca has his powerful blaster, our robot has powerful Lidar guns. Chewbacca has two legs, our robots has two motors. Chewbacca has good balaance, our robot has an IMU that can easily find his orientation. I hope you enjoyed the little adventure with our Chewbacca, sadly this is the end of his story... or is it ?   
