import numpy as np
import playground as play
import geometry as geo

class Rover:

    def __init__(self, start, max_size):
        self.play = play.Playground()
        self.pos = start
        self.past_pos = [start]
        self.max_size = max_size
        self.points = []

    def set_landmark(self, landmarks):
        for land in landmarks:
            self.play.add_landmark(land)
    
    def scan_zone(self, scans):
        d_alpha = 2 * np.pi / scans
        
        angles = d_alpha * np.arange(scans)
        for alpha in angles:
            inter = self.play.intersection(self.pos, alpha)
            if not(inter is None):
                self.points.append(self.play.intersection(self.pos, alpha))
    
    def move(self, alpha):
        p_pos = self.pos + geo.geometry.angle_unit(alpha)

        if(abs(p_pos[0]) < self.max_size or abs(p_pos[1]) < self.max_size):
            self.pos = p_pos
            self.past_pos.append(p_pos)
    
    
    def path_move(self, path, scan_rate):

        for post in path:
            if (abs(post[0]) <= self.max_size and abs(post[1]) <= self.max_size):
                self.pos = post
                self.past_pos.append(post)
                
        return None