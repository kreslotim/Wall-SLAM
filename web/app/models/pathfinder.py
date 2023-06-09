import heapq
import math
import numpy as np

class PathFinder:
    def __init__(self, obs = [], cell_dim = 100, grid_length = 4000, passed_weight = 1):
        """
        Initializes the PathFinder object. Handles all data related to finding an optimized path (Grid, path, obstacles...). 

        Arguments:
            obs (list): Raw list of obstacles in car coordinates.
            cell_dim (int): The dimension of each grid cell.
            grid_rad (int): The radius of the grid.

        """
        self.togo_position = None

        # "Radius" of the square grid cm
        self.cell_dim = cell_dim
        self.grid_length = grid_length
        self.obs = obs

        self.grid = []
        self.path = []

        self.grid_weights = []
        self.PASSED_WEIGHT = passed_weight

        self.generateGrid(obs)

    def generateGrid(self, obs):
        """
        Generate grid from collected obstacle scans 
        (fill_grid has the same purpose but is more specific to K-means) 

        Arguments: 
            obs (list): Raw list of obstacles in car coordinates.
        Returns:
            grid (Array) : The grid with obstacles, if an obstacle is present the cell index will be 1 otherwise 0.
        """
        # Initialize the 2D array representing the grid map
        self.grid = np.zeros((int(self.grid_length / self.cell_dim), int(self.grid_length / self.cell_dim)))
        self.grid_weights = np.zeros(self.grid.shape)

        obstacle_coordinates = obs.copy()
        
        # Sensitivity (obstacle points per block, think of it as a threshold)
        sensitivity = 10

        # Iterate through the list of obstacle coordinates
        for obstacle in obstacle_coordinates:
            # Convert obstacle coordinates to grid coordinates
            grid_x, grid_y = self.car_to_grid(obstacle)

            # Increment the value of the corresponding grid cell, ensure that its valid too
            if 0 <= grid_x < len(self.grid) and 0 <= grid_y < len(self.grid):
                self.grid[grid_y][grid_x] += 1

        self.grid = np.where(self.grid < sensitivity, 0, 1)
        return self.grid.copy()
   
    def dijkstra_shortest_path(self, current_position):
        """
        Dijkstra algorithm that searches for the optimal path while avoiding turns at any cost.

        Arguments:
            current_position (tuple): The current cell the robot occupies.
        Returns:
            paths (array): a list of cell indices representing the optimal path
        """
        # Check if grid exits or if the starting position is not an obstacle
        if len(self.grid) == 0 or self.grid[current_position[1]][current_position[0]] == 1:
            return []

        self.grid_weights[current_position[1]][current_position[0]] = self.PASSED_WEIGHT
        rows = len(self.grid)
        cols = len(self.grid[0])

        # Create a priority queue for Dijkstra's algorithm
        queue = [(0, current_position)]
        heapq.heapify(queue)

        # Create a dictionary to track distances from the starting position
        distances = {current_position: 0}

        # Create a dictionary to track the previous positions in the shortest path
        previous = {}

        # Define possible directions: up, down, left, right
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

        while queue:
            current_dist, current_pos = heapq.heappop(queue)

            # Check if the current position is the destination
            if current_pos == self.togo_position:
                self.path = [self.grid_to_car(current_pos)]
                while current_pos in previous:
                    self.path.append(self.grid_to_car(previous[current_pos]))
                    current_pos = previous[current_pos]

                self.path.reverse()
                return self.path.copy()

            x, y = current_pos

            # Get the previous position
            prev_pos = previous.get(current_pos)

            # Explore all possible directions
            for i in range(4):
                dx, dy = directions[i]
                new_x = x + dx
                new_y = y + dy

                # Check if the new position is within the grid boundaries
                if 0 <= new_x < rows and 0 <= new_y < cols:
                    new_pos = (new_x, new_y)
                    
                    if self.grid[new_y][new_x] == 0:
                        # Calculate the cost for changing directions
                        if prev_pos is None :
                            # Current Orrientation, todo get it.
                            prev_dx = 0
                            prev_dy = 1
                        else : 
                           
                            prev_dx = x-prev_pos[0]
                            prev_dy = y-prev_pos[1]
                        if (dx == prev_dx or dy == prev_dy):
                            direction_cost = 0 
                        else:
                            direction_cost = 4

                        # Update the distance if it's shorter than the previously recorded distance
                        new_dist = current_dist + 1 + direction_cost + self.grid_weights[y][x]
                        if new_pos not in distances or new_dist < distances[new_pos]:
                            distances[new_pos] = new_dist
                            previous[new_pos] = current_pos
                            heapq.heappush(queue, (new_dist, new_pos))

        # If there is no path to the destination
        return [-1]

    def path_to_actionNumber(self, current_orr = 0):
        """
        Converts the path to a sequence of action numbers that the car needs to follow.

        Arguments: 
            current_orr (int): The current orientation of the car.

        Returns:
            actions (list): A list of action numbers (1 for movement, 4 for left turn, 3 for right turn).

        """
        # 1 : move, 4 : turn left, 3 : turn right
        path = self.path.copy()
        if len(path) == 0:
            return [float(0)]
        
        action = []

        while len(path) > 1:
            #   Find in which axe we are moving 0 if X and 1 if Y
            axe = 1 if path[0][0] - path[1][0] == 0 else 0
            moved = 0

            # Set the new targeted orientation
            if path[0][axe] - path[1][axe] < 0:
                togo_orr = 90 - axe * 90 # relative orr
            if path[0][axe] - path[1][axe] > 0:
                togo_orr =  270 - axe * 90 
            
                
            while moved == 0:
                # Move forward if we are already in the good direction
                if current_orr == togo_orr :
                    action.append(1)
                    moved = 1
                    path.pop(0)
    
                # Move Right if 90 degree turn is necessary
                if togo_orr == (current_orr + 90) % 360 :
                    action.append(3)
                    current_orr = (current_orr + 90) % 360

                # Move Right if 189 degree turn is necessary
                if togo_orr == (current_orr + 180) % 360:
                    action.append(3)
                    current_orr = (current_orr + 90) % 360
                
                # Move Right if -90 degree turn is necessary
                if togo_orr == (current_orr + 270) % 360:
                    action.append(4)
                    current_orr = (current_orr + 270) % 360
        return action  
    
    ############ K-Means Helper ############

    def fill_grid(self, obs):
        """
        Fill the grid from not accessible cell

        Arguments: 
            obs :  list of obstacles in grid coordinates  
        Returns:
            grid (Array) : The grid with obstacle if present, if an obstacle is present the cell index will be 1.

        """
        self.grid = np.zeros((len(self.grid),len(self.grid)))
        
        obstacle_coordinates = obs.copy()
        
        # Iterate through the list of obstacle coordinates
        for obstacle in obstacle_coordinates:
            # Convert obstacle coordinates to grid coordinates
            grid_x, grid_y = obstacle
            # Increment the value of the corresponding grid cell, ensure that its valid too
            if 0 <= grid_x < len(self.grid) and 0 <= grid_y < len(self.grid):
                self.grid[grid_y][grid_x] = 1

        print(self.grid)
        return self.grid.copy()
    
    ######## TRANSFORMATION #############

    def car_to_grid(self, point_car):
        """
        Compute the car coordinates with in the referentiel of the array-grid

        Arguments: 
            point_car (tuple) : cooridnates of the car such as (x,y) 
        Returns:
            x (int): coordinate x in the grid
            y (int):  coordinate y in the grid
        """
        x = point_car[0] + (len(self.grid[0])*self.cell_dim)/2
        y = point_car[1] + (len(self.grid[1])*self.cell_dim)/2

        x = math.floor(x/self.cell_dim)
        y = math.floor(y/self.cell_dim)
        
        return x,y
    
    def grid_to_car(self, point_grid):
        """
        Compute the car coordinates in the car's reference frame given the grid coordinates.

        Arguments: 
            point_grid (tuple) : coordinates of a point in the grid such as (x, y) 
        Returns:
            x (float): x-coordinate in the car's reference frame
            y (float): y-coordinate in the car's reference frame
        """

        x_grid, y_grid = point_grid

        x = (x_grid + 0.5 ) * self.cell_dim - (len(self.grid[0]) * self.cell_dim) / 2
        y = (y_grid + 0.5 ) * self.cell_dim - (len(self.grid[1]) * self.cell_dim) / 2

        return x,y
    
 



 
