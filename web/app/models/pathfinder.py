from collections import deque
import heapq
import math
import numpy as np

class PathFinder:
    def __init__(self, obs, cell_dim = 1, grid_rad = 100):
        # "Radius" of the square grid cm
        self.cell_dim = cell_dim
        self.obs = obs
        self.grid = self.generateGrid(obs,grid_rad)

    def _generateGrid(self, obs, grid_rad):
        """
        Generate grid from collected obstacle scans

        Arguments: 
            obs :  raw list of obstacles in car coordinates  
            grid_rad : The wanted radius of the grid
        Returns:
            grid (Array) : The grid with obstacle if present, if an obstacle is present the cell index will be 1.

        :param obst: raw list of obstacles in car coordinates  
        :return: sampled grid with cells set to 1 or 0
        """
        # Initialize the 2D array representing the grid map
        self.grid = np.zeros((int(2*grid_rad / self.cell_dim), int(2*grid_rad / self.cell_dim)))
        obstacle_coordinates = obs.copy()
        
        # Sensitivity (obstacle points per block, think of it as a threshold)
        sensitivity = 3

        # Iterate through the list of obstacle coordinates
        for obstacle in obstacle_coordinates:
            # Convert obstacle coordinates to grid coordinates
            grid_x = self.car_to_grid_coor(obstacle)
            grid_y = self.car_to_grid(obstacle)

            # Increment the value of the corresponding grid cell, ensure that its valid too
            if 0 <= grid_x < 2*grid_rad / self.cell_dim and 0 <= grid_y < 2*grid_rad / self.cell_dim:
                self.grid[grid_y, grid_x] += 1

        self.grid = np.where(self.grid < sensitivity, 0, 1)

        return self.grid
   

    def dijkstra_shortest_path(self, current_position, togo_position):
        """
        Dijkstra algorithm that search for the optimal path
        
        Arguments: 
            current_position : the current cell the robot occupy
            togo_position : the cell that we wish to travel to
        Returns:
            paths (array): a list of index of cell to travel to that is optimal
        """

        rows = len(self.grid)
        cols = len(self.grid[0])

        # Create a priority queue for Dijkstra's algorithm
        queue = [(0, (current_position))]
        heapq.heapify(queue)

        # Create a dictionary to track distances from the starting position
        distances = {current_position: 0}

        # Create a dictionary to track the previous positions in the shortest path
        previous = {}

        # Define possible directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            current_dist, current_pos = heapq.heappop(queue)

            # Check if the current position is the destination
            if current_pos == togo_position:
                path = []
                while current_pos in previous:
                    path.append( previous[current_pos])
                    current_pos = previous[current_pos]
                return path

            x, y = current_pos

            # Explore all possible directions
            for i in range(4):
                dx, dy = directions[i]
                new_x = x + dx
                new_y = y + dy

                # Check if the new position is within the grid boundaries
                if 0 <= new_x < rows and 0 <= new_y < cols:
                    new_pos = (new_x, new_y)
                    cost = 1  # Assuming each step has a cost of 1

                    # Calculate the new distance from the starting position
                    new_dist = current_dist + cost

                    # Update the distance if it's shorter than the previously recorded distance
                    if new_pos not in distances or new_dist < distances[new_pos]:
                        distances[new_pos] = new_dist
                        previous[new_pos] = current_pos
                        heapq.heappush(queue, (new_dist, new_pos))

        # If there is no path to the destination
        return [-1]

######## TRANSFORMATION #############

    def car_to_grid(self, point_car):
        """
        Compute the car coordinates with in the referentiel of the grid

        Arguments: 
            point_car: cooridnates of the car such as (x,y) 
        Returns:
            x: coordinate x in the grid
            y: coordinate y in the grid
        """
        x = math.floor(point_car[0] + (len(self.grid[0])*self.cell_dim)/2)
        y = math.floor(point_car[1] + (len(self.grid[0])*self.cell_dim)/2)
        return x,y
    
    def fetch_in_grid(self, point_grid):
        x = point_grid[0]-1
        y = point_grid[1]
        return self.grid(x,y)
    

    def path_to_actionNumber(self, path, current_orr=0):
        """
        Produce a sequence of instruction that the car need to follow.

        Arguments: 
            path: a sequence of coordinate that represent a path
        Returns:
            actionNumber: a sequence of action to send to the robot that need to perform them
            y: coordinate y in the grid
        """
        # 1 : move, 2 : turn left, 3 : turn right
        action = []
        while len(path) > 1:
            axe = 0
            if path[0][0] - path[1][0] == 0:
                axe = 1
            
            if path[0][axe] - path[1][axe] > 0:
                if current_orr == 0 :
                    action.append(0)
                if current_orr == 90:
                    action.append(0)
                if current_orr == 180:
                    action.append(0)
                if current_orr == 270:
                    action.append(0)
   
        return 