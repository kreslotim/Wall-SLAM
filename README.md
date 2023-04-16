# CS-358 Making Intelligent Things
## Project : Simultaneous Localization And Mapping
Timofey Kreslo, Sylvain Pichot, Finn Mac Namara, Alonso Coaguila, Florian Dejean

March 2023

## Contents
    • 0.1 Description and motivation of the project  . . . . . . . . . . . . . . . . . . . . . . 1
    • 0.2 How are we going to build it ? . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2
    • 0.3 Resources  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
    • 0.4 Risks  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
    • 0.5 Buy list . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
    • 0.6 Milestones . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
    • 0.7 Weekly Tasks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
    • 0.8 Progress documentation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
    • 0.9 References . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10

## 0.1 Description and motivation of the project
Our project involves building a robot that will perform Simultaneous Localization and Mapping
(SLAM). SLAM is a crucial technology for robotic systems that need to move in dynamic and
unknown environments. Robots equipped with SLAM can map and navigate their surroundings
without human intervention, making them valuable for various applications such as warehouse
automation, search and rescue operations, etc... In general, the sensors used on SLAM robot are
quite expensive and big so our objective would also be to reduce the size and price.

We will utilize an ultrasonic sensors system (see following section for the sensor discussion)
to implement the SLAM algorithm, and we will develop a software program that will render the
robot autonomous via Wi-Fi. This will require integrating various components of the robot, such
as the motor control system, the ultrasonic sensor system, and the Wi-Fi communication module.

Overall, the project consists of deploying an autonomous robot that will map its surrounding
area using SLAM algorithm with an end goal of displaying a cohesive 2D-map of the area.

## 0.2 How are we going to build it ?
### Obstacle detection
Lidar and ultrasound are both commonly used sensors for Simultaneous Localization and Map-
ping applications. However, Lidar has the following advantages:

   - 1. Accuracy: Lidar sensors provide much higher accuracy measurements than ultrasound.
    Lidar can measure distances with a precision of a few millimeters, whereas ultrasound can
    only measure distances to within a few centimeters. Also the resolution is much higher.
   - 2. Noise immunity: Lidar sensors are less susceptible to noise and interference than ultra-sound sensors. Lidar uses light to measure distances, whereas ultrasound uses sound waves.
    This makes Lidar less sensitive to acoustic noise and interference.
   - 3. Mechanical aspect: Lidar has a bigger range or aperture angle (in degrees) so i would
    need to be spun around, unlike the ultra sound solution.
    
Overall, Lidar sensors provide much more accurate and detailed information about the envi-
ronment, which is essential for accurate SLAM. The problem with Lidar is that it is expensive
and has the potential to blow the budget.

Consequently, we will opt for an ultrasonic sensor which is a cheaper alternative of a Lidar
sensor. The sensor gives us the distance D with the detected obstacle. Two ultrasonic sensors
will be rotating on top of the robot (back-to-back on a 180 degrees servo, so we can plot any
obstacle around the robot) (ex: https://howtomechatronics.com/projects/arduino-rad
ar-project/). Software wise : Knowing the direction of the ultrasonic sensor we can create a
block (representing an obstacle) of a distance D from the sensor).

### Robot localization
To determine where the robot is on the map we will use two stepper motors, the inputs given
to the motors allow us to calculate the position of the robot based on its starting point.
(https://www.youtube.com/watch?v=5CmjB4WF5XA) . Regarding the software, we need to
create an algorithm that creates a link between the current position and the new targeted posi-
tion without going through obstacle. To limit inaccuracy, we will use an IMU to determine the orientation of the robot (ex: https://www.youtube.com/watch?v=KMhbV1p3MWk).

### Computational Work
Unfortunately, the SLAM algorithm is too memory bound and computationally slow for a micro-
controller. To deal with this problem, we plan having the micro-controller connect through Wi-Fi
to a capable external computer, the Command Computer (CC), hence why the micro-controller
used has Wi-Fi capability. The Wi-Fi connection also allows the robot to move freely. Therefore,
the micro-controller only receives commands for movement and returns the sensors data to the
CC.

### Algorithm & Data
To create the map and control the robot with the CC, the micro-controller will collect and send
to the CC the following elements: the position of the robot, the orientation of the robot (IMU),
the distance detected from the ultrasonic sensor and the orientation of the sensor (180 Servo).
Then using the data it receives, the CC generates the map and sends new commands to the robot
from a distance. We want to use Python and the Robot Operation System (ROS) as a framework
since its industry standard and can provide a myriad of useful tools/resources. Regarding ROS
and Arduino compatibility, we have found the following solution. If we have time, we might use
some basic machine learning algorithms to detect noise.

## 0.3 Resources
Firstly, we have discovered open-source projects and tutorials available at :
- https://wired.chillibasket.com/3d-printed-wall-e/
- https://3delworld.com/how-to-make-smars-robot-3d-printed-2023/
- https://youtu.be/htoBvSq8jLA (position tracking)

That gives us access to numerous STL files for SMARS parts. These files include components
that we can use to construct our SMARS robots for SLAM. This will save us a significant amount
of time and effort, as we do not need to design and model these parts from scratch.

Additionally, we have also developed a program, last year, for efficient route finding using
Dijkstra algorithms. This program will be instrumental in enabling our robot to navigate through
the environment autonomously while avoiding obstacles. The Dijkstra algorithm is a graph-
based algorithm that finds the shortest path between two points in a graph. We will modify this
algorithm to suit the needs of our project, such as incorporating the sensor data from the camera
vision system to avoid obstacles in real-time.

## 0.4 Risks
1. **Mechanical issues**:
We are using precise steppers motors, to navigate through the map but we still need to take
into account error accumulation. This can be an issue since we are planning continuously
updating the robots position via the stepping information of the motors.
Also using tracks could turn out to be a bad idea, because tracks slip when touring on the
spot, resulting in screwed up data for odometry (=”use of data from motion sensors to
estimate change in position over time”).

Solution: We added an IMU sensor to check the rotational information. In case this does
not work, we need to consider a simplified design of the chassis, a bit like an automatic
hoover. (That is, only two wheels and one stabilizing thing in front/back).
After all, there is a reason why those vacuum cleaners are built the way they are.
Now, if it still has problems on the localizing part, we need modifying the area. to map
and setting up some kind of orientation system (reflective tape around cylinders is common
way in industrial environments, an easier way would be to simply add a grid like pattern
for the robot to follow on the ground).

2. **Sensor accuracy**:
Our SLAM robot rely heavily on ultrasonic sensors to navigate and build maps of their
environment. These sensors must be accurate and reliable, otherwise the robot will struggle
to locate itself or map its surroundings. The sensors should be as good as possible.

Solution: If the ultrasonic sensors are inaccurate, means that we would have to change the
placement of the sensors, worst case scenario the sensor has to be right in front of the wall,
we would put the sensor in front of the car and make it work similar to a Roomba.

3. **Environmental Interference**:
The surface on which the robot is must be flat and stable, if those condition aren’t respected
we will easily lost the position of the robot, making it challenging for the robot to navigate
and detect its surroundings accurately, resulting in a poor map.

Solution: We will restrain the robot environment to avoid that, and in case of such en-
vironment we will able to detect them due the gyro (IMU) and stop the algorithm if the
environment is unavoidable. An example of such will be a small jump that if the robot is
not aware of it, it will get flipped.

4. **Computational power**:
Building a SLAM robot requires significant computational power to process sensor data,
run algorithms, and control the robot’s movements. The ESP8266 lacks this power.

Solution: Computation will be done on a laptop with wireless communication.

5. **Communication problems**:
Our SLAM robot will rely on wireless communication to receive commands or send data,
and any communication problems can lead to delays or malfunctions in its real time map-
ping ability.

Solution: We could try Bluetooth instead but the problem might still arise. We can use
a cable but that strongly reduces the mobility of the robot. Another approach will be to
await till good communication is made, every time there seem to be a perturbation.
