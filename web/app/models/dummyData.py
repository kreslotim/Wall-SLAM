import math
import random

class dummyData:

    def __init__(self):
        self.obstacles = {}
        
        

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
            return self._dataToObstacle(x_car,y_car,distance,orientation)

            # Add obstacle to the obstacle map
        
