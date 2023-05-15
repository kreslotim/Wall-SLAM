import numpy as np
import matplotlib as plt

import geometry as geo
        

class Playground:
    def __init__(self) -> None:
        self.landmarks = []
    

    def add_landmark(self, landmark):
        self.landmarks.append(landmark)

    def intersection(self, point, angle):

        possible_intersections = []

        for mark in self.landmarks:
            for i in range(len(mark)):
                a, b = mark[i], mark[i - 1]
                intersection = geo.geometry.ray_intersection(point, angle, a, b)

                if not(intersection is None):
                    possible_intersections.append(np.copy(intersection))     
        return geo.geometry.closest_point(point, np.array(possible_intersections)) if(possible_intersections) else None
