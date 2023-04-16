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
