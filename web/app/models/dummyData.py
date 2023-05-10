import math
import random
import time

class DummyData:
    def __init__(self, nbData):
        self.obstacles = {}
        self.startTime = time.time()
        self.nbData = nbData
       
        self.x_sent =[]
        self.x_received = []
        self.y_sent = []
        self.y_received =[]

        for u in range(nbData):
            self._randomlyFill()

        self.startTime = time.time()
        

    def _dataToObstacle(self,x_car,y_car, distance,orientation):    
        # Calculate the x and y coordinates of the obstacle
        orientation = math.radians(orientation)
        point_x = x_car + distance * math.cos(orientation)
        point_y = y_car + distance * math.sin(orientation)
        obstacle_position = (point_x, point_y)
        
        # Check if the obstacle position is already in the dictionary
        if obstacle_position in self.obstacles:
            self.obstacles[obstacle_position].add((x_car, y_car))
        else:
            self.obstacles[obstacle_position] = {(x_car, y_car)}

        return((x_car,y_car), obstacle_position)
    
    def _randomlyFill(self):
        # Generate random car position within range (-100, 100)
        x_car = random.uniform(-100, 100)
        y_car = random.uniform(-100, 100)
    
        # Generate random obstacles and add them to the obstacle map
        for i in range(2):
            # Calculate distance and orientation between car position and obstacle position
            distance =  random.uniform(4, 6)
            orientation = random.uniform(0,180)
            self.obstacles[(x_car,y_car)] = self._dataToObstacle(x_car,y_car,distance,orientation)


    # Add obstacle to the obstacle map
    def random_com(self):
        self.x_sent.append(time.time()-self.startTime)
        self.x_received.append(time.time()-self.startTime)
        self.y_sent.append(2)
        self.y_received.append( 2)
        return self.x_sent,self.x_received,self.y_sent,self.y_received