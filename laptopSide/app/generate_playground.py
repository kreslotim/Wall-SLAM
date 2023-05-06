import numpy as np
import matplotlib as plt

class Landmark:
    ##
    #1......2
    #........
    #4......3
    ##
    def __init__(self, corners) -> None:
        self.corners = corners

    
    def has_intersection(self, point, angle):
        
        ## Line
        a = np.tan(angle)
        b = point[1] - a * point[0]
        
        line = lambda x: a*x + b
        
        ##check
        right = (angle >= 1.5 * np.pi()) and (angle <= 0.5 * np.pi())

        on_top = False
        under = False
        touch = False

        for corner in self.corners:
            if((right and corner[0] < point[0]) or (not(right) and corner[0] > point[0])):
                continue

            on_top = on_top or ((line(corner[0]) < corner[1]))
            under = under or (line(corner[0]) > corner[1])
            touch = touch or (line(corner[0]) == corner[1])
        
        return touch or (on_top and under)
    
    def intersection(self, point, angle):

        if not(self.has_intersection(point, angle)):
            return None
        
        ## Line
        a = np.tan(angle)
        b = point[1] - a * point[0]

        ##
        intersections = []
        for i in range(len(self.corners)):
            
            ## If stacked
            if(self.corners[i][0] == self.corners[(i+1)%len(self.corners)][0]):
                top, bot = max(self.corners[i][0], self.corners[(i+1)%len(self.corners)][0]), min(self.corners[i][0], self.corners[(i+1)%len(self.corners)][0])

                res = (a*self.corners[i][0] + b)
                if (res >=  bot and res <= top):
                    intersections.append(np.array([self.corners[i][0], res]))
                
                continue

            ## Not stacked
            left, right = None

            if(self.corners[i][0] > self.corners[(i+1)%len(self.corners)][0]):
                left, right = self.corners[(i+1)%len(self.corners)], self.corners[i]
            else:
                left, right = self.corners[i], self.corners[(i+1)%len(self.corners)]

            t_a = (right[1] - left[1])/(right[0] - left[0])
            t_b = right[1] - t_a * right[0]

            #Edge case where ray is aligned
            if (t_a == a):
                if (a* left[0] + b == left[1]):
                    sd_left = (left[0] - point[0])**2 + (left[1] - point[1])**2
                    sd_right = (right[0] - point[0])**2 + (right[1] - point[1])**2

                    if(sd_left > sd_right):
                        intersections.append(right)
                    else:
                        intersections.append(left)
                continue
            
            t_x = (t_b - b)/(a - t_a)

            intersections.append(np.array([t_x, a*t_x + b]))
        
        closest = intersections[0]
        sd_closest = (point[0] - closest[0])**2 + (point[1] - closest[1])**2

        for i in range(1, len(intersections)):
            sd_curr = (point[0] - intersections[i][0])**2 + (point[1] - intersections[i][1])**2
            if(sd_closest > sd_curr):
                closest = intersections[i]
                sd_closest = sd_curr
        
        return closest

        

class Playground:
    def __init__(self, lx = 100, ly = 100) -> None:
        self.dim = (lx, ly)
        self.landmarks = []
    

    def add_landmark(self, landmark):
        self.landmarks.append(landmark.boundary)

    def intersection(self, point, angle):
        possible_intersection = []

        for landmark in self.landmarks:
            l_intersection = landmark.intersection(point, angle)

            if(l_intersection != None):
                possible_intersection.append(l_intersection)
        
        
        if possible_intersection:
            closest = possible_intersection[0]
            sd_closest = (point[0] - closest[0])**2 + (point[1] - closest[1])**2

            for i in range(1, len(possible_intersection)):
                curr = possible_intersection[i]
                sd_curr = (point[0] - curr[0])**2 + (point[1] - curr[1])**2

                if(sd_curr < sd_closest):
                    closest = curr
                    sd_closest = sd_closest
            
            return closest


        return None
