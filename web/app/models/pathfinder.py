import heapq
import math
import numpy as np

class PathFinder:
    def __init__(self, obs = [], cell_dim = 10, grid_rad = 100):
        """
        Initializes the PathFinder object. Handles all data related to finding an optimized path (Grid, path, obstacles...). 

        Arguments:
            obs (list): Raw list of obstacles in car coordinates.
            cell_dim (int): The dimension of each grid cell.
            grid_rad (int): The radius of the grid.

        """
        self.togo_position = (10,10)

        # "Radius" of the square grid cm
        self.cell_dim = cell_dim
        self.grid_rad = grid_rad
        self.obs = obs

        self.grid = []
        self.path = []

        self.generateGrid(obs)

    def generateGrid(self, obs):
        """
        Generate grid from collected obstacle scans

        Arguments: 
            obs (list): Raw list of obstacles in car coordinates.
        Returns:
            grid (Array) : The grid with obstacles, if an obstacle is present the cell index will be 1 otherwise 0.
        """
        # Initialize the 2D array representing the grid map
        self.grid = np.zeros((int(2*self.grid_rad / self.cell_dim), int(2*self.grid_rad / self.cell_dim)))

        obstacle_coordinates = obs.copy()
        
        # Sensitivity (obstacle points per block, think of it as a threshold)
        sensitivity = 1

        # Iterate through the list of obstacle coordinates
        for obstacle in obstacle_coordinates:
            # Convert obstacle coordinates to grid coordinates
            grid_x, grid_y = self.car_to_grid(obstacle)

            # Increment the value of the corresponding grid cell, ensure that its valid too
            if 0 <= grid_x < len(self.grid) and 0 <= grid_y < len(self.grid):
                self.grid[grid_x, grid_y] += 1

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
        if self.grid[current_position[1]][current_position[0]] == 1:
            return []


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
                self.path = [self.__grid_to_website(current_pos)]
                while current_pos in previous:
                    self.path.append(self.__grid_to_website(previous[current_pos]))
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
                            direction_cost = 0
                           

                     

                        # Update the distance if it's shorter than the previously recorded distance
                        new_dist = current_dist + 1 + direction_cost
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
        current_orr = current_orr + 90 #offset
        path = self.path.copy()
        if len(path) == 0:
            return float(0)
        
        if path[0] == -1:
            return -2
        action = []
        while len(path) > 1:
            axe = 1 if path[0][0] - path[1][0] == 0 else 0
            moved = 0

            if path[0][axe] - path[1][axe] > 0:
                togo_orr = 90 + axe*90# relative orr
            if path[0][axe] - path[1][axe] < 0:
                togo_orr =  270 -axe*270 
            if path[0][axe] - path[1][axe] == 0:
                togo_orr = 0
                
            while moved == 0:
                if current_orr == togo_orr :
                    action.append(1)
                    moved = 1
                    path.pop(0)
                    
                if current_orr < togo_orr :
                    action.append(3)
                    current_orr = current_orr + 90

                if current_orr > togo_orr :
                    action.append(4)
                    current_orr = current_orr - 90
        return action
    
    def generate_list_of_obstacles_for_website(self): 
        """
        Generates a list of obstacle coordinates in web format for website visualization.

        Returns:
            obstacles (list): List of obstacle coordinates in grid format.
        """
        if len(self.grid) != 0: 
            grid = np.array(self.grid)
            coordinates = np.argwhere(grid == 1)
            obstacle_cell = [self.__website_to_grid((int(x), int(y))) for x, y in coordinates]
            return obstacle_cell
        return []
    
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
                self.grid[grid_y, grid_x] = 1

        return self.grid
    
    ######## TRANSFORMATION #############
    '''
    We are using three different coordinates system : Car, Grid, Website.
    Grid and Website transformation shouldn't be used outside of the class.

    Car : is a cartesian coordinates system

    Grid :
            0 -------> y
            |
            |
            |
            v
            x
    Website :

            y
            ^
            |
            |
            |
            0-------> x
    '''

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
        
        return self.__website_to_grid((x,y))
    
    def __website_to_grid(self, point_grid):
        """
        Gets the content of the grid at (x,y). Since grid is constructed with [0,0] bottom left but in a array with [0,0] top left. This method allows you to make a transition.

        Arguments: 
            point_grid (tuple): cooridnates of the grid as (x,y) 
        Returns:
            x (int): coordinate x in the grid
            y (int): coordinate y in the grid
        """
        y = len(self.grid) - point_grid[0] - 1
        x = point_grid[1] 
        return x,y
    
    def __grid_to_website(self, point_array):
        """
        Gets the content of the grid at (x, y) based on array coordinates, where [0, 0] is the top left.

        Arguments:
            point_array (tuple): coordinates of the grid in array format as (x, y)
        Returns:
            x (int): coordinate x in the array
            y (int): coordinate y in the array
        """
        y = point_array[0]
        x = len(self.grid) - point_array[1] - 1
        return x, y
    
    ############ SETTER ############

    def setTarget_xy_in_website(self, coordinates):
        self.togo_position = self.__website_to_grid((coordinates[0],coordinates[1]))
 



 