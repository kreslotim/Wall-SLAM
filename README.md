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
