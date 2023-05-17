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

        self.startTime = time.time()
        

    def _randomlyFill(self):
        # Generate random car position within range (-100, 100)
        x_car = random.uniform(-100, 100)
        y_car = random.uniform(-100, 100)
    
        # Generate random obstacles and add them to the obstacle map
    
        distance =  random.uniform(4, 6)
        orientation = random.uniform(0,180)
        return [time.time()-self.startTime, x_car,y_car,distance,orientation]
    # Add obstacle to the obstacle map
    def random_com(self):
        self.x_sent.append(time.time()-self.startTime)
        self.x_received.append(time.time()-self.startTime)
        self.y_sent.append(2)
        self.y_received.append( 2)
        return self.x_sent,self.x_received,self.y_sent,self.y_received