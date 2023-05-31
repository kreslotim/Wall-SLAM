import math
import random

class SlamData:
    def __init__(self):
        # INPUT
        self.numberOfObsInOneGo = 50
        self.delete_distance_if_no_distance = 2000
        self.delete_distance_linear_equation = 10
        self.max_distance_detection = 2000
        self.number_min_of_obstacle = 1
        self.in_radius = 10

        # Obstacles variables
        self.list_of_obs = []
        self.list_of_100_x_obs = []
        self.list_of_100_y_obs = []
        self.list_of_100_orr = []

        # Current Car coordinates
        self.curr_x_car = 0
        self.curr_y_car = 0
        self.perfect_orientation = 0


    def add_orr( self, magOrr, gryOrr, kalmanOrr, time):
        self.list_of_100_orr.append((magOrr,gryOrr,kalmanOrr,time))
        if len(self.list_of_100_orr) > self.numberOfObsInOneGo:
            self._clear_temp_list()

    def _add_and_delete_obstacle(self, x_car, y_car, obs_distance, orientation):

        if obs_distance != 0 and -self.max_distance_detection < obs_distance < self.max_distance_detection:
            x_new, y_new = self._dataToObstacle(x_car, y_car, obs_distance,orientation)   
            self.list_of_obs.append([x_new,y_new])
            self.list_of_100_x_obs.append(x_new)
            self.list_of_100_y_obs.append(y_new)
        else :
            obs_distance = self.delete_distance_if_no_distance
            x_new, y_new = self._dataToObstacle(x_car,y_car, obs_distance,orientation)   

        # Calculate the linear equation between the car and new obstacle
        if x_new - x_car != 0:
            m = (y_new - y_car) / (x_new - x_car)
            b = -m * x_car + y_car
        else:
            m = float('inf')
            b = y_car

        # Find the obstacles that lie on the linear equation between the new obstacle and the origin
        obstacles_to_delete = []

        for obstacle in self.list_of_obs:
            x_obs, y_obs = obstacle

            # Check if the obstacle lies on the linear equation
            if m != float('inf'):
                distance = abs(y_obs - m * x_obs - b) / math.sqrt(1 + m**2)
            else:
                distance = abs(y_car - y_new)

            # Check if the obstacle lies between the new obstacle and the origin
            if (x_car < x_obs < x_new  or x_car > x_obs > x_new ) and (y_car  < y_obs < y_new  or y_car > y_obs > y_new )and self.delete_distance_linear_equation > distance :
                    obstacles_to_delete.append(obstacle)

        # Remove the obstacles that lie on the linear equation between the new obstacle and the origin
        self.list_of_obs = [obstacle for obstacle in self.list_of_obs if obstacle not in obstacles_to_delete]

        return self.list_of_obs

    def _filter_obstacles(self, number_min_of_obstacle, radius ):
        filtered_obs = []

        for obstacle in self.list_of_obs:
            count = 0

            # Check the distance between each point and the obstacle
            for point in self.list_of_obs:
                if obstacle != point:
                    distance = math.sqrt((obstacle[0] - point[0])**2 + (obstacle[1] - point[1])**2)
                    if distance <= radius:
                        count += 1

            # If the count is greater than or equal to n, keep the obstacle
            if count >= number_min_of_obstacle:
                filtered_obs.append(obstacle)

        self.list_of_obs = filtered_obs.copy()

        return self.list_of_obs

    def _is_ready_to_go(self):
        return len(self.list_of_100_x_obs) > self.numberOfObsInOneGo 

    def _is_ready_to_go_orr(self):
        return len(self.list_of_100_orr) > self.numberOfObsInOneGo 

    def _clear_temp_list(self):
        self.list_of_100_x_obs.clear()
        self.list_of_100_y_obs.clear()
        self.list_of_100_orr.clear()


############ HELPER METHOD ############

    def _dataToObstacle(self, x_car, y_car, distance, orientation):  
    # Calculate the x and y coordinates of the obstacle
        orientation = math.radians(orientation)
        point_x = x_car + distance * math.cos(orientation)
        point_y = y_car + distance * math.sin(orientation)

        return(point_x,point_y)  
