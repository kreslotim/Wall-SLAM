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


$\documentclass{report}

\usepackage[colorlinks = true,
            linkcolor = black,
            urlcolor  = blue,
            citecolor = darkblue,
            anchorcolor = red]{hyperref}
\usepackage[a4paper]{geometry}
\usepackage[table]{xcolor}
\usepackage{makecell, cellspace, caption}
\usepackage[absolute,overlay]{textpos}
\usepackage{tabularx}
\usepackage{stackengine}
\usepackage{cite}   
\usepackage{nicematrix}
\usepackage{enumitem}% http://ctan.org/pkg/enumitem
\usepackage{xurl}


\title{\textbf{CS-358 Making Intelligent Things}\\Project : Simultaneous Localization And Mapping }
\author{Timofey Kreslo, Sylvain Pichot, Finn Mac Namara, Alonso Coaguila, Florian Dejean}
\date{March 2023}

\graphicspath{{pictures/}}

\begin{document}

\maketitle

\tableofcontents

\section{Description and motivation of the project}

Our project involves building a robot that will perform Simultaneous Localization and Mapping (SLAM). SLAM is a crucial technology for robotic systems that need to move in dynamic and unknown environments. Robots equipped with SLAM can map and navigate their surroundings without human intervention, making them valuable for various applications such as warehouse automation, search and rescue operations, etc... In general, the sensors used on SLAM robot are quite expensive and big so our objective would also be to reduce the size and price.  \newline

We will utilize an ultrasonic sensors system (see following section for the sensor discussion) to implement the SLAM algorithm, and we will develop a software program that will render the robot autonomous via Wi-Fi. This will require integrating various components of the robot, such as the motor control system, the ultrasonic sensor system, and the Wi-Fi communication module. \newline

Overall, the project consists of deploying an autonomous robot that will map its surrounding area using SLAM algorithm with an end goal of displaying a cohesive 2D-map of the area.

\begin{center}
\stackunder[5pt]{\includegraphics[scale=0.5]{MIT Project/pictures/2d_map.png}}{\scriptsize \href{{https://www.innowtech.com/2019/05/16/les-algorithmes-slam-simultaneous-localization-and-mapping/}}{Source : Figure 1}}
\end{center}
\newpage

\section{How are we going to build it ?}

\textbf{Obstacle detection}\newline
Lidar and ultrasound are both commonly used sensors for Simultaneous Localization and Mapping applications. However, Lidar has the following advantages:
\begin{enumerate}
     \item \textbf{Accuracy:}
      Lidar sensors provide much higher accuracy measurements than ultrasound. Lidar can measure distances with a precision of a few millimeters, whereas ultrasound can only measure distances to within a few centimeters. Also the resolution is much higher.

      \item \textbf{Noise immunity:} Lidar sensors are less susceptible to noise and interference than ultrasound sensors. Lidar uses light to measure distances, whereas ultrasound uses sound waves. This makes Lidar less sensitive to acoustic noise and interference. 

      \item \textbf{Mechanical aspect:} Lidar has a bigger range or aperture angle (in degrees) so i would need to be spun around, unlike the ultra sound solution.
\end{enumerate}

Overall, Lidar sensors provide much more accurate and detailed information about the environment, which is essential for accurate SLAM. The problem with Lidar is that it is expensive and has the potential to blow the budget.

Consequently, we will opt for an ultrasonic sensor which is a cheaper alternative of a Lidar sensor. The sensor gives us the distance D with the detected obstacle. Two ultrasonic sensors will be rotating on top of the robot (back-to-back on a 180 degrees servo, so we can plot any obstacle around the robot) (ex: \url{https://howtomechatronics.com/projects/arduino-radar-project/}). Software wise : Knowing the direction of the ultrasonic sensor we can create a block (representing an obstacle) of a distance D from the sensor).\newline \newline
\begin{figure}[h]
    \centering
    \stackunder[5pt]{\includegraphics[scale=0.4]{pictures/serv.png}}{\scriptsize \href{{https://youtube.com/shorts/o7DMHJKhpws?feature=share}}{Source : Figure 2}}
    \stackunder[5pt]{\includegraphics[scale=0.2]{pictures/doubleServ.png}}{\scriptsize \href{https://www.youtube.com/watch?v=dHZB0WhLl8g&t=12s}{Source : Figure 3}}
    \stackunder[5pt]{\includegraphics[scale=0.15]{pictures/sensorServo.png}}{\scriptsize \href{https://www.youtube.com/watch?v=xngpwyQKnRw}{Source : Figure 4}}
\end{figure}





\textbf{Robot localization}\newline
To determine where the robot is on the map we will use two stepper motors, the inputs given to the motors allow us to calculate the position of the robot based on its starting point. (\url{https://www.youtube.com/watch?v=5CmjB4WF5XA}) . Regarding  the software, we need to create an algorithm that creates a link between the current position and the new targeted position without going through obstacle. To limit inaccuracy, we will use an IMU to determine the orientation of the robot (ex: \url{https://www.youtube.com/watch?v=KMhbV1p3MWk}). \newline 

\textbf{Computational Work}\newline
Unfortunately, the SLAM algorithm is too memory bound and computationally slow for a micro-controller. To deal with this problem, we plan having the micro-controller connect through Wi-Fi to a capable external computer, the Command Computer (CC), hence why the micro-controller used has Wi-Fi capability. The Wi-Fi connection also allows the robot to move freely. Therefore, the micro-controller only receives commands for movement and returns the sensors data to the CC.\newline 

\textbf{Algorithm \& Data}\newline
To create the map and control the robot with the CC, the micro-controller will collect and send to the CC the following elements: the position of the robot, the orientation of the robot (IMU), the distance detected from the ultrasonic sensor and the orientation of the sensor (180 Servo). Then using the data it receives, the CC generates the map and sends new commands to the robot from a distance. We want to use Python and the Robot Operation System (ROS) as a framework since its industry standard and can provide a myriad of useful tools/resources. Regarding ROS and Arduino compatibility, we have found \href{http://wiki.ros.org/rosserial_arduino/Tutorials/Arduino%20IDE%20Setup}{the following solution}. If we have time, we might use some basic machine learning algorithms to detect noise.

\section{Resources}

Firstly, we have discovered open-source projects and tutorials available at : \newline - \url{https://wired.chillibasket.com/3d-printed-wall-e/} \newline -  
 \url{https://3delworld.com/how-to-make-smars-robot-3d-printed-2023/}\newline -
  \url{https://youtu.be/htoBvSq8jLA} (position tracking) \newline 
 
 That gives us access to numerous STL files for SMARS parts. These files include components that we can use to construct our SMARS robots for SLAM. This will save us a significant amount of time and effort, as we do not need to design and model these parts from scratch.\newline

Additionally, we have also developed a program, last year, for efficient route finding using Dijkstra algorithms. This program will be instrumental in enabling our robot to navigate through the environment autonomously while avoiding obstacles. The Dijkstra algorithm is a graph-based algorithm that finds the shortest path between two points in a graph. We will modify this algorithm to suit the needs of our project, such as incorporating the sensor data from the camera vision system to avoid obstacles in real-time.

\section{Risks}

\begin{enumerate}
 \item \textbf{Mechanical issues:} \newline 
We are using precise steppers motors, to navigate through the map but we still need to take into account error accumulation. This can be an issue since we are planning continuously updating the robots position via the stepping information of the motors. \newline Also using tracks could turn out to be a bad idea, because tracks slip when touring on the spot, resulting in screwed up data for odometry (="use of data from motion sensors to estimate change in position over time"). 
  
  Solution: We added an IMU sensor to check the rotational information. In case this does not work, we need to consider a simplified design of the chassis, a bit like an automatic hoover. (That is, only two wheels and one stabilizing thing in front/back).  \newline 
  After all, there is a reason why those vacuum cleaners are built the way they are. \newline    
  Now, if it still has problems on the localizing part, we need modifying the area. to map and setting up some kind of orientation system (reflective tape around cylinders is common way in industrial environments, an easier way would be to simply add a grid like pattern for the robot to follow on the ground).
  
  \item \textbf{Sensor accuracy}: \newline 
  Our SLAM robot rely heavily on ultrasonic sensors to navigate and build maps of their environment. These sensors must be accurate and reliable, otherwise the robot will struggle to locate itself or map its surroundings. The sensors should be as good as possible.

  Solution: If the ultrasonic sensors are inaccurate, means that we would have to change the placement of the sensors, worst case scenario the sensor has to be right in front of the wall, we would put the sensor in front of the car and make it work similar to a Roomba.
  \item \textbf{Environmental Interference:} \newline
  The surface on which the robot is must be flat and stable, if those condition aren't respected we will easily lost the position of the robot, making it challenging for the robot to navigate and detect its surroundings accurately, resulting in a poor map. 

  Solution: We will restrain the robot environment to avoid that, and in case of such environment we will able to detect them due the gyro (IMU) and stop the algorithm if the environment is unavoidable. An example of such will be a small jump that if the robot is not aware of it, it will get flipped.
  
  \item \textbf{Computational power:} \newline
  Building a SLAM robot requires significant computational power to process sensor data, run algorithms, and control the robot's movements. The ESP8266 lacks this power.
  
  Solution: Computation will be done on a laptop with wireless communication. 
  \item \textbf{Communication problems}:\newline 
  Our SLAM robot will rely on wireless communication to receive commands or send data, and any communication problems can lead to delays or malfunctions in its real time mapping ability.

  Solution: We could try Bluetooth instead but the problem might still arise. We can use a cable but that strongly reduces the mobility of the robot. Another approach will be to await till good communication is made, every time there seem to be a perturbation. 
  
\end{enumerate}
\newpage
\section{Buy list}
\texttt{SMARS} robot (total 120.- frs):

\begin{table}[h]
\hspace{-4mm}

\centering\captionsetup{justification = centering, labelformat = empty}
\renewcommand{\arraystretch}{1.4}
\caption{\large\textbf{Electronics 1x SMARS}}
\begin{NiceTabular}{ccc}[vlines]
\CodeBefore
    \rowcolor{gray!25}{}
\Body
    \hline
    \Block{1-1}{\textbf{\#}} & \textbf{Name} & \textbf{Quantity (Price/item)}\\
    \hline
         1 & \href{www.bastelgarage.ch/nodemcu-32-esp32-wifi-bluetooth-entwicklungsboard-cp2102?search=esp-32}{ESP-32} & 1 (14.-)\\
         2 & \href{https://www.bastelgarage.ch/stepper-motor-schrittmotor-5v-1-64-28byj-48}{Stepper Motor / (replaced by smaller motor 5V) } & 2 (22.-)\\
         3 & \href{https://www.bastelgarage.ch/a4988-schrittmotor-treiber-stepper-driver-modul?search=a4988}{A4988 Motor Driver} & 2 (3,9)\\
         4 & \href{https://www.distrelec.ch/fr/capteur-de-distance-ultrasons-hc-sr04-sparkfun-electronics-sen-15569/p/30160395?trackQuery=+Sensor+HC-SR05&pos=1&origPos=1&origPageSize=50&track=true}{Ultrasonic Module Distance Sensor HC-SR04} & 2 (4,5)\\
         5 & \href{https://www.bastelgarage.ch/batteriefach-batteriehalter-6-x-aa-mit-9v-stecker-anschluss?search=batteriehalter}{Battery Block Coupler 6 Battery 9V [Same as the lego car]}& 1 (5.-)\\
         6 & \href{https://www.distrelec.ch/fr/capteur-de-mouvement-breakout-icm-20948-9dof-imu-sparkfun-electronics-sen-15335/p/30157561?trackQuery=imu&pos=3&origPos=3&origPageSize=50&track=true}{9 axis ICM-20948 9DoF IMU} & 1 (24.-)\\
         7 & \href{ https://www.distrelec.ch/fr/kit-de-servomoteur-180-m5stack-a076/p/30285940?trackQuery=servomoteur&pos=5&origPos=16&origPageSize=50&track=true} { 180 Servo Motor} & 1 (2 for 15.30.-)\\
    \hline
\end{NiceTabular}
\end{table}
\texttt We wish to build a second {SMARS} for optional goal and to have some redundancy in case one part fails.
 \texttt{SMARS} robot Illustration:

\begin{center}
\stackunder[5pt]{\includegraphics[scale=0.45]{pictures/smars.png}}{\scriptsize \href{{https://www.smarsfan.com/}}{Source : Figure 5}}
\end{center}

\newpage
\section{Milestones}

\begin{itemize}
\item \textbf{Milestone 1 : Build a 3D PRINTED prototype of the chassis with working stepper motors, check track driving behaviour and get communication between the computer and the vehicle+sensors to work (Deadline : 1st May).}\newline\newline
(From Week 6 - 7)\newline
Task 1: Design and print the chassis prototype for our vehicle.\newline
Task 2: Assemble and collect all the necessary hardware and sensors. So we can rapidly combine it with the 3D parts \newline
Task 3: (Start coding the software) Find a way to collect the data from the sensors/Arduino and send them to the CC via Wi-fi.\newline\newline
FIRST SMARS PROTOTYPE should be built on the 7th of April \newline

(From Week 8 - 9)\newline
 Task 4: Check that the sensors work well and that the output are correct. So we can change the sensors if we aren't satisfied with the current ones\newline
 Task 5: Transfer the output of the robot on a map, so we can start utilizing the data. \newline
 Task 6: Create an algorithm that moves the car from an initial position to another given position. Starting to send instruction to the SMARS from the CC to see if are able to correctly control the robot. \newline

\item \textbf{Milestone 2: Implement an algorithm that allows the robot to create a map of its environment and return to its initial position using the map.(Deadline : 26th May)}\newline\newline
 (From Week 10-11) \newline
 Task 1: Code the mapping and localization algorithm, needs to be autonomous. So we can start plotting the obstacles.\newline
 Task 2: Test the limit of our robot and debug the mapping and localization algorithm, if any problem are detected.\newline
 
 OVERALL WORKING SLAM ROBOT should be able to map on the 20th of May \newline\newline
(From Week 11-13)\newline
 Task 3: Have a working SLAM robot.\newline
 Task 4: Have a working UI.\newline
    
\item \textbf{Optional Goal: Scale up the number of SMARS} \newline
The integration of another robot. The goal would be to reduce the time needed to map out an area. One of the possible solution would be by scaling up the number of robots working together. This is might be quite complicated, and we haven't really thought of it yet but we are leaving the door open.

\item \textbf{Optional Goal: Sound integration} \newline It would be amazing if the robot could produce noises/music on command, or produce noises in real time through Wi-Fi. This would allow the robot to communicate in real time to a person blocking its way or allowing it to call for help if it is stuck. 
\end{itemize}

\section{Weekly Tasks}

This section is to split up the jobs, that have to be done, evenly with the team members. We plan weekly team meetings between us (without the Phd student) to keep us up to date on what is going on and where we are exactly in the project. We find it important to have good communication especially when it comes to asking for help. We will be focusing a lot on talking and understanding the other team members. With that said the tasks here will not always be done by the person mentioned because on the moment problems might arise or even the initial plan wasn't a good solution to the problem. On the other hand, we can guarantee that all team members will have a saying in the more general tasks in the Week n°\# column  

\begin{table}[htbp]
  \centering
  \label{tab:example}
  \begin{tabularx}{\textwidth}{|X|X|X|X|X|X|}
    \hline
    Week n°\# 
    & Tim 
    & Florian 
    & Finn 
    & Alonso 
    & Sylvain\\
    \hline
    6 \scriptsize {(Discussion on how we are going to design the robot) }
    & \scriptsize {Building a prototype version of the SMARS (with smaller competents that Tim has)}
    & \scriptsize {Modelling on Fusion 360, first model with diagonal stepped motors }
    & \scriptsize {Modelling on Fusion 360 and brainstorming }
    & \scriptsize {Modelling on Fusion360, second model with side by side stepped motors }
    & \scriptsize {Modelling and brainstorming on the software a connectivity through Wi-Fi} \\
     \hline
    7 \scriptsize {(Analysing SMARS prototype and 3D printed prototype chassis as well as clarifying the electric wiring) }
    & \scriptsize {Analyse 3D printed models, and draw an electric circuit}
    & \scriptsize {Compare and analyse 3D printed models}
    & \scriptsize {Learn how to control a stepped motor }
    & \scriptsize {Compare and analyse 3D printed models}
    & \scriptsize {Draw an electric circuit to see if all connections are good} \\
    \hline
    Holidays \scriptsize {(Start the software research, to learn how to correctly use our equipment and starting to understand how we are going to design and code the software)}
    & \scriptsize {Do research on ultrasonic sensor and how to use it and see how we can use python to utilize it's data}                         
    & \scriptsize {Do research on stepper motor and how to use it and see how we can use python to utilize it's data}
    & \scriptsize {Advance on the circuit and review prototype with the constraints of the wiring, if done check how to create a 2D map with Python}
    & \scriptsize {Advance on the circuit and review prototype with the constraints of the wiring, if done check how to create a 2D map with Python}
    & \scriptsize {Do research on IMU and how to use it, and see how we can use python to utilize it's data}\\
    \hline
    8 \scriptsize {(Assemble the hardware, and the software)}
    & \scriptsize {Debugging the ultrasonic sensors code and real life testing}
    & \scriptsize {Playing around with the stepper motors and see how precious they are (code to real life ratio)}
    & \scriptsize {Debugging the ultrasonic sensors code and see how it would work with the 360 servo }
    & \scriptsize {Soldering and assembling the hardware}
    & \scriptsize {Soldering and assembling the hardware}\\
    \hline
    9 \scriptsize {(This should just be a debugging week and time to reflect a bit on how we are working as a team)}
    & \scriptsize {Debugging }
    & \scriptsize {Debugging (cable management if necessary)}
    & \scriptsize {Debugging (hardware if cables fall off)}
    & \scriptsize {Debugging (remodelling if necessary)}
    & \scriptsize {Debugging (remodelling if necessary)}\\
    \hline
  \end{tabularx}
\end{table}

For now, we only planned individual tasks till week 9 (for Milestone) to see the dynamic of our group. When the first milestone is achieved, we will plan new weekly tasks for the next milestone.
\newpage

\section{Progress documentation}
In development from Week 7 onwards...\newline

We started to develop the chassis for the robot. First we need consider what it needs to hold, followed by how to arrange it. The robot will hold the 2 stepper motors, a servo, a battery and a micro-controller. For a first prototype, the stepper motors both go in the back, to compensate for the back weight, we would put the batteries and micro-controller in the front, finally in the center the servo holding the sensors.\newline

\includegraphics[scale=0.32]{descript.jpg} \newline

Our second prototype has the stepper motors diagonally spilt from each other. This version is more campact (smaller in terms of width). We want to test different configurations in turns of weight dispersion: \newline
\includegraphics[scale=0.72]{MIT Project/pictures/descript_bis.png}

Here is first SMARS prototype with our own equipment. This will allow us to quickly test if tracks are a good use in our project, so we can change our design if this isn't the case. \newline
\begin{center}
\includegraphics[scale=0.1]{MIT Project/pictures/smars_1.jpeg}
\includegraphics[scale=0.1]{MIT Project/pictures/smars_2.jpeg}
\end{center}
\newpage
\section{References}

\begin{enumerate}[label={[\arabic*]}]

  \item Figure 1 : Alain Godot. \textit{Algorithmes SLAM (Simultaneous Localization and Mapping)}. May 2019. URL: \url{https://www.innowtech.com/2019/05/16/les-algorithmes-slam-simultaneous-localization-and-mapping/}
  \item Figure 2 : @CodersCafeTech. \textit{DIY Radar With Ultrasonic Sensor And Chat-GPT Generated Arduino Code | Coders Cafe}. Youtube. 2023. URL: \url{https://youtube.com/shorts/o7DMHJKhpws?feature=share}
  \item Figure 3 : Channel Everything. \textit{Two ultrasonic sensors on a servo for angle and distance data}. Youtube. 2016. URL: \url{https://www.youtube.com/watch?v=dHZB0WhLl8g&t=12s}
  \item Figure 4 : Hani's Experiments. \textit{How to make an ultrasonic Radar}. Youtube. 2021. URL: \url{https://www.youtube.com/watch?v=xngpwyQKnRw}
  \item Figure 5 : Kevin McAleer. \textit{SMARS Fan}. 2018. URL: \url{https://www.smarsfan.com}
  
\end{enumerate}

\end{document}

$
