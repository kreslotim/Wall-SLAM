# Wall-SLAM - Simultaneous Localization And Mapping
Timofey Kreslo, Sylvain Pichot, Finn Mac Namara, Alonso Coaguila, Florian Dejean.

June 2023

<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/e592ad42-2deb-4919-802d-11c624c35482" width = 600 />

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

## Description
Wall-SLAM is a project that we have elaborated within the course CS-358 Making Intelligent Things, under the direction of Prof. Koch and under the supervision of Federico Stella and Anirudhh Ramesh.
This report outlines the key features, methodology, challenges faced, and a detailed "How To Build" guide.

Our [project proposal](https://github.com/kreslotim/Wall-SLAM/blob/main/proposal/proposal.md), can be useful to witness some deviations in our project from our expectations.

The primary objective of the project was to build a cost-effective and compact SLAM robot capable of mapping unknown and dynamic environments. 

## Overview
[small video and demo of all functionaltites]

We utilized the data from the distance sensors (Ultrasonic and LIDAR), IMU (Inertial Measurement Unit) sensor, and Stepper motors to estimate the robot's pose (position and orientation) and simultaneously construct a map of the environment. This involved integrating data from different sensors using techniques such as sensor calibration, fusion and Kalman filtering algorithms.

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
As zealous devotees of the enchanting Disney's figure Wall-E, we couldn't resist the temptation to transform our prototype into his spitting image. But, alas, our professor promptly intervened, bursting our bubble of whimsy with a witty remark. With a mischievous twinkle in his eye, he playfully reminded us that while Wall-E excelled in garbage collection and exuded undeniable cuteness, our project's aspirations extended beyond those realms. Thus, we bid farewell to our beloved Wall-E robot, sparing it from a destiny of cuteness overload and instead refocusing our efforts on more practical endeavors.

<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/6667b767-95a2-45b7-8b5e-17c26d23500b" width = 400/>

Given that our intentions did not encompass teaching our robot to engage in garbage collection or vacuuming activities, we decided to shift our focus towards functionality that would enable mapping of the surrounding environment, akin to modern autonomous vacuum cleaners. Furthermore, we chose to retain the concept of tracks with wheels, as it offered enhanced precision in movement and rotation, while opting for rubber tracks to minimize slippage during maneuvering.

### Sketches
Initially, we engaged in the process of conceptualizing our ideas through sketches to determine the optimal arrangement of electronic components. Our primary objective was to achieve a compact design that would streamline the assembly process and expedite 3D printing requirements. This approach was aimed at optimizing the overall efficiency of the construction phase.

We initiated the development process by focusing on the chassis design. Subsequently, we proceeded to devise an arrangement strategy. The robot incorporated two stepper motors along with their corresponding drivers, a servo, a battery, and a micro-controller. For the initial prototype, we positioned both stepper motors at the rear section of the chassis. In order to counterbalance the weight distribution, the batteries and the micro-controller were placed at the front section. Lastly, the servo, responsible for holding the sensors, was centrally positioned within the chassis.

<img src = "https://user-images.githubusercontent.com/56829239/232310112-f7f68b36-d2c5-4ecf-8979-ef074a0ed3eb.png" width = 700/>
This approach was promptly dismissed as it became apparent that in order to facilitate turning, both motors needed to rotate in opposite directions, necessitating the rotation of the entire car around its vertical axis. 

The rotation of the machine necessitates the alignment of the servo and the primary axis of rotation. This alignment is crucial during turning maneuvers as the distance sensors are required to scan in close proximity to the adjacent wall. By maintaining the sensors in close proximity to the central axis of rotation, the objective is to minimize noise and optimize the accuracy of the scanning process.

Consequently, we proposed an alternative design to address this limitation.
<img src = "https://user-images.githubusercontent.com/56829239/232310079-931594a3-6049-4ff0-9cc0-58b74d3c37e4.png" width = 700/>

This design greatly appealed to us, and we made the decision to proceed in this particular direction. During our exploration on the web, we chanced upon a toy named [SMARS](https://www.smarsfan.com/) (Screwed/Screwless Modular Assembleable Robotic System), which seemed to align closely with our envisioned requirements. We found inspiration in its design and opted to incorporate a chassis that closely resembled to SMARS. To assess the feasibility of the track concept, we even went as far as designing the entire SMARS idea to evaluate its effectiveness.

<img src = "https://github.com/kreslotim/Wall-SLAM/blob/main/Pictures/ezgif-4-9122e21e39.gif">

Having appreciated the remarkable ingenuity behind the notion of using the printing filament as a means to securely bind the tracks together, as well as the exceptional functionality of this approach in practical implementation, we wholeheartedly adopted this design for our project. Consequently, this decision entailed the utilization of the same wheels, as the tracks had been meticulously tailored to ensure precise compatibility with these specific wheel components. This deliberate alignment not only guaranteed optimal performance but also facilitated seamless integration between the tracks and wheels, thereby fortifying the overall effectiveness of our system.

The subsequent focus of our attention revolved around the development of the chassis, and the incorporation of the battery, the motors and the sensors.  

As soon as we agreed on the placement of all the components, we started designing in 3D.
In order to leverage the collaborative design features, we opted to use Fusion 360, enabling effective teamwork during the design process. Minor design changes have been made in Freecad, in order to save time.

Here's what we've come up with.
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/182bb3ea-2b7f-49c3-83fd-62bc438a0f22" width = 700/>

<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/4402e84b-2550-423e-8a4e-7c284bb5df46" width = 700/>

Now we will explain the choice we've made for positioning the electronic pieces.
The parts that are highlighted in green are those that we designed ourselves. The Ultrasonic sensor's frame as well as the wheels and the tracks were borrowed from SMARS project, because they fit our requirements well.
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/9eac749d-10e7-4cae-a3eb-60efbaca4600" width = 700/>
While we adopted the wheel design from SMARS, we had to adapt it's axle mount to fit the rectangular axle of the motor we are using. Furthermore, it is essential to align the axle of the slave wheel with the motor's axle to ensure that both wheels are at the same level.
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/3dcc6850-5950-4f5f-9a45-e38546c61ef8" width = 700/>

In order to optimize the efficiency of the printing and assembly process, we strategically positioned all the components in close proximity to one another, ensuring minimal wasted space on the chassis.

As the heaviest electronic component of the entire construction, the battery serves as a central anchor within the overall design. By positioning it at the center, we establish a stable foundation upon which the remaining components, i.e. the servo and the lidars sensors are securely mounted and connected.
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/f2b20805-2bfe-478f-b751-ee17c3dc3ad8" width = 700/>

The cover slides over the battery and encases the servo on top.
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/6061ea20-960f-4265-97e7-7a94cdba535c" width = 700/>

The servo, in return, holds both lidars (distance sensors) that are sneaked on the servo's arm.
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/a595e70b-5473-4abe-b3f3-71a7b0facc83" width = 700/>
## Assembly

Once
<img src = "https://github.com/kreslotim/Wall-SLAM/assets/56829239/243612a9-e803-44b0-9ae7-f1f7f143721a" width = 700/>


## 0.2 How are we going to build it ?
### Obstacle detection
Lidar and ultrasound are both commonly used sensors for Simultaneous Localization and Map-
ping applications. However, Lidar has the following advantages:

   - 1. **Accuracy**: Lidar sensors provide much higher accuracy measurements than ultrasound.
    Lidar can measure distances with a precision of a few millimeters, whereas ultrasound can
    only measure distances to within a few centimeters. Also the resolution is much higher.
   - 2. **Noise immunity**: Lidar sensors are less susceptible to noise and interference than ultra-sound sensors. Lidar uses light to measure distances, whereas ultrasound uses sound waves.
    This makes Lidar less sensitive to acoustic noise and interference.
   - 3. **Mechanical aspect**: Lidar has a bigger range or aperture angle (in degrees) so i would
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

<img align = "left" src = "https://user-images.githubusercontent.com/56829239/232311292-8a2b68fb-5e41-4616-a399-67ffa0f45f40.png" width = 200 />
<img src = "https://user-images.githubusercontent.com/56829239/232311342-40701424-a3a3-41a2-a878-7908d8a43223.png" width = 200 /> 
<img src = "https://user-images.githubusercontent.com/56829239/232311379-c23d53fa-cd01-4fae-97e1-4c63016e2084.png" width = 200 />


### Robot localization
To determine where the robot is on the map we will use two stepper motors, the inputs given to the motors allow us to calculate the position of the robot based on its starting point.
(https://www.youtube.com/watch?v=5CmjB4WF5XA). 
Regarding the software, we need to create an algorithm that creates a link between the current position and the new targeted position without going through obstacle. To limit inaccuracy, we will use an IMU to determine the orientation of the robot (ex: https://www.youtube.com/watch?v=KMhbV1p3MWk).

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

Solution: We added an IMU sensor to check the rotational information.
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

## 0.5 Buy list
SMARS robot (total 120.- frs):
### Electronics 1x SMARS
    1. ESP-32                                                     1x (14.-)
    2. Stepper Motor / (replaced by smaller motor 5V)             2x (22.-)
    3. A4988 Motor Driver                                         2x (3,9)
    4. Ultrasonic Module Distance Sensor HC-SR04                  2x (4,5)
    5. Battery Block Coupler 6 Battery 9V [Same as the lego car]  1x (5.-)
    6. 9 axis ICM-20948 9DoF IMU                                  1x (24.-)
    7. 180 Servo Motor                                            1x (2 for 15.30.-)

We wish to build a second SMARS for optional goal and to have some redundancy in case one
part fails. 
SMARS robot illustration:

<img src = "https://user-images.githubusercontent.com/56829239/232310908-d8e2eb6b-0b33-4ed4-a58d-663cec184cc3.png" width = 500/>


## 0.6 Milestones
### • Milestone 1 : Build a 3D PRINTED prototype of the chassis with working step-per motors, check track driving behaviour and get communication between the computer and the vehicle+sensors to work (Deadline : 1st May).
(From Week 6 - 7)
* Task 1: Design and print the chassis prototype for our vehicle.
* Task 2: Assemble and collect all the necessary hardware and sensors. So we can rapidly combine it with the 3D parts
* Task 3: (Start coding the software) Find a way to collect the data from the sensors/Arduino and send them to the CC via Wi-fi.

FIRST SMARS PROTOTYPE should be built on the 7th of April

(From Week 8 - 9)
* Task 4: Check that the sensors work well and that the output are correct. So we can change the sensors if we aren’t satisfied with the current ones
* Task 5: Transfer the output of the robot on a map, so we can start utilizing the data.
* Task 6: Create an algorithm that moves the car from an initial position to another given position. Starting to send instruction to the SMARS from the CC to see if are able to correctly control the robot.

### • Milestone 2: Implement an algorithm that allows the robot to create a map of its environment and return to its initial position using the map.(Deadline : 26th May)
(From Week 10-11)
* Task 1: Code the mapping and localization algorithm, needs to be autonomous. So we can start plotting the obstacles.
* Task 2: Test the limit of our robot and debug the mapping and localization algorithm, if any problem are detected.

OVERALL WORKING SLAM ROBOT should be able to map on the 20th of May

(From Week 11-13)
* Task 3: Have a working SLAM robot.
* Task 4: Have a working UI.

### • Optional Goal: Scale up the number of SMARS
The integration of another robot. The goal would be to reduce the time needed to map out
an area. One of the possible solution would be by scaling up the number of robots working
together. This is might be quite complicated, and we haven’t really thought of it yet but
we are leaving the door open.
### • Optional Goal: Sound integration
It would be amazing if the robot could produce noises/music on command, or produce noises in real time through Wi-Fi. This would allow the robot to communicate in real time to a person blocking its way or allowing it to call for help if it is stuck.


## 0.7 Weekly Tasks
This section is to split up the jobs, that have to be done, evenly with the team members. We
plan weekly team meetings between us (without the Phd student) to keep us up to date on
what is going on and where we are exactly in the project. We find it important to have good
communication especially when it comes to asking for help. We will be focusing a lot on talking
and understanding the other team members. With that said the tasks here will not always be
done by the person mentioned because on the moment problems might arise or even the initial
plan wasn’t a good solution to the problem. On the other hand, we can guarantee that all team
members will have a saying in the more general tasks in the Week n°# column

    Week n°#                Tim                 Florian             Finn                Alonso              Sylvain
    6. Discussion on        Building a pro-     Modelling on        Modelling on        Modelling on        Modelling and
      how we are go-        totype version      Fusion 360,         Fusion 360 and      Fusion360,          brainstorming
      ing to design the     of the SMARS        first model         brainstorming.      second model        on the software
      robot.                (with smaller       with diagonal                           with side by        a connectivity
                            components that     stepped motors.                         side stepped        through Wi-Fi.
                            Tim has).                                                   motors.
    
    7. Analysing            Analyse 3D          Compare and         Learn how           Compare and         Draw an electric
    SMARS prototype and     printed models,     analyse 3D          to control a        analyse 3D          circuit to see if
    3D printed prototype    and draw an         printed models.     stepper motor.      printed models.     all connections 
    chassis as well as      electric circuit.                                                               are good.
    clarifying the
    electric wiring.
    
    Holidays                Do research         Do research on      Advance on          Advance on          Do research on
    Start the software      on ultrasonic       stepper motor       the circuit         the circuit         IMU and how to
    research, to learn      sensor and how      and how to          and review          and review          use it, and see
    how to correctly        to use it and       use it and see      prototype with      prototype with      how we can use
    use our equipment       see how we can      how we can          the constraints     the constraints     python to utilize
    and starting to         use python to       use python to       of the wiring,      of the wiring,      it’s data.
    understand how          utilize it’s data.  utilize it’s data.  if done check       if done check
    we are going to                                                 how to create       how to create
    design and code                                                 a 2D map with       a 2D map with
    the software.                                                   Python.             Python.
                                    
    8. Assemble the         Debugging           Playing around      Debugging           Soldering and       Soldering and
    hardware, and           the ultrasonic      with the stepper    the ultrasonic      assembling the      assembling the
    the software.           sensors code        motors and see      sensors code        hardware.           hardware.
                            and real life       how precious        and see how
                            testing.            they are            it would work
                                                code to             with the 360
                                                real life ratio).   servo.
                                                
    9. This should          Debugging.          Debugging           Debugging           Debugging           Debugging
    just be a                                   cable management    hardware if         remodelling         remodelling
    debugging week                              if necessary.       cables fall off.    if necessary.       if necessary.
    and time to reflect
    a bit on how we
    are working as a
    team.


For now, we only planned individual tasks till week 9 (for Milestone) to see the dynamic of
our group. When the first milestone is achieved, we will plan new weekly tasks for the next
milestone.

## 0.8 Progress documentation
In development from Week 7 onwards...

We started to develop the chassis for the robot. First we need consider what it needs to hold,
followed by how to arrange it. The robot will hold the 2 stepper motors, a servo, a battery and
a micro-controller. For a first prototype, the stepper motors both go in the back, to compensate
for the back weight, we would put the batteries and micro-controller in the front, finally in the
center the servo holding the sensors.

<img src = "https://user-images.githubusercontent.com/56829239/232310112-f7f68b36-d2c5-4ecf-8979-ef074a0ed3eb.png" width = 700/>


Our second prototype has the stepper motors diagonally split from each other. This version
is more campact (smaller in terms of width). 
We want to test different configurations in turns
of weight dispersion:

<img src = "https://user-images.githubusercontent.com/56829239/232310079-931594a3-6049-4ff0-9cc0-58b74d3c37e4.png" width = 700/>

Here is first SMARS prototype with our own equipment. This will allow us to quickly test if
tracks are a good use in our project, so we can change our design if this isn’t the case.

<img align = "left" src = "https://user-images.githubusercontent.com/56829239/232310221-48497394-6d34-42c5-9630-422581552723.png" width = 300/>
<img src = "https://user-images.githubusercontent.com/56829239/232310280-4229fd2a-700a-45fc-84d2-e9abf6f51453.png" width = 300/>


## 0.9 References
* [1] Figure 1 : Alain Godot. Algorithmes SLAM (Simultaneous Localization and Mapping). May 2019. URL: https://www.innowtech.com/2019/05/16/les-algorithmes-slam-simultaneous-localization-and-mapping/
* [2] Figure 2 : @CodersCafeTech. DIY Radar With Ultrasonic Sensor And Chat-GPT Generated Arduino Code — Coders Cafe. Youtube. 2023. URL: https://youtube.com/shorts
/o7DMHJKhpws?feature=share
* [3] Figure 3 : Channel Everything. Two ultrasonic sensors on a servo for angle and distance data. Youtube. 2016. URL: https://www.youtube.com/watch?v=dHZB0WhLl8g&t=12s
* [4] Figure 4 : Hani’s Experiments. How to make an ultrasonic Radar. Youtube. 2021. URL: https://www.youtube.com/watch?v=xngpwyQKnRw
* [5] Figure 5 : Kevin McAleer. SMARS Fan. 2018. URL: https://www.smarsfan.com
