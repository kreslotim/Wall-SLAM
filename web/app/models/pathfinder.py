from collections import deque
import heapq
import math
import numpy as np

class PathFinder:
    def __init__(self, obs, cell_dim = 10, grid_rad = 100):

        self.togo_position = (10,10)

        # "Radius" of the square grid cm
        self.cell_dim = cell_dim
        self.obs = obs
        self.grid = self._generateGrid(obs,grid_rad)

        self.list_of_obstacles_in_grid = self.generate_list_of_obstacles_for_website()
        self.path = []
        
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
        sensitivity = 1

        # Iterate through the list of obstacle coordinates
        for obstacle in obstacle_coordinates:
            # Convert obstacle coordinates to grid coordinates
            grid_x, grid_y = self.car_to_grid(obstacle)

            # Increment the value of the corresponding grid cell, ensure that its valid too
            if 0 <= grid_x < len(self.grid) and 0 <= grid_y < len(self.grid):
                self.grid[grid_x, grid_y] += 1

        self.grid = np.where(self.grid < sensitivity, 0, 1)

        return self.grid
   

    def dijkstra_shortest_path(self, current_position):
        """
        Dijkstra algorithm that searches for the optimal path while avoiding turns at any cost.

        Arguments:
            current_position: the current cell the robot occupies
            togo_position: the cell that we wish to travel to
        Returns:
            paths (array): a list of cell indices representing the optimal path
        """
        print(f"Car Position : {current_position}")
        print(f"Togo Position : {self.togo_position}")


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
                self.path = [self.get_in_array_coords(current_pos)]
                while current_pos in previous:
                    self.path.append(self.get_in_array_coords(previous[current_pos]))
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
                    
                    if self.grid[new_x][new_y] == 0:
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

    def path_to_actionNumber(self, current_orr=180):
        """
        Produce a sequence of instruction that the car need to follow.

        Arguments: 
            path: a sequence of coordinate that represent a path
        Returns:
            actionNumber: a sequence of action to send to the robot that need to perform them
            y: coordinate y in the grid
        """
        # 1 : move, 4 : turn left, 3 : turn right
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
                    action.append(4)
                    current_orr = current_orr + 90

                if current_orr > togo_orr :
                    action.append(3)
                    current_orr = current_orr - 90
        return action
    
######## TRANSFORMATION #############



    def car_to_grid(self, point_car):
        """
        Compute the car coordinates with in the referentiel of the grid such as [0,0] of the grid is in the bottom left.

        Arguments: 
            point_car: cooridnates of the car such as (x,y) 
        Returns:
            x: coordinate x in the grid
            y: coordinate y in the grid
        """
        x = point_car[0] + (len(self.grid[0])*self.cell_dim)/2
        y = point_car[1] + (len(self.grid[1])*self.cell_dim)/2

        x = math.floor(x/self.cell_dim)
        y = math.floor(y/self.cell_dim)
        
        return x,y
    
    def get_in_grid_coords(self, point_grid):
        """
        Gets the content of the grid at (x,y). Since grid is constructed with [0,0] bottom left but in a array with [0,0] top left. This method allows you to make a transition.

        Arguments: 
            point_grid: cooridnates of the grid as (x,y) 
        Returns:
            grid_value: the content at the position of the grid 
        """
        y = len(self.grid) -point_grid[0] - 1
        x = point_grid[1] 
        return x,y
    
    
    def get_in_array_coords(self, point_array):
        """
        Gets the content of the grid at (x, y) based on array coordinates, where [0, 0] is the top left.

        Arguments:
            point_array: coordinates of the grid in array format as (x, y)
        Returns:
            grid_value: the content at the position of the grid
        """
        y = point_array[0]
        x = len(self.grid) - point_array[1] - 1
        return x, y

    
    def generate_list_of_obstacles_for_website(self): 
        if len(self.grid) != 0: 
            obstacle_cell = self.find_positive_coordinates(self.grid)  
            return obstacle_cell
        return []
    
    def find_positive_coordinates(self, grid):
        grid = np.array(grid)
        coordinates = np.argwhere(grid == 1)
        return [self.get_in_array_coords((int(x), int(y))) for x, y in coordinates]
    
    def generateGrid(self, obs):
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
        self.grid = np.zeros((len(self.grid),len(self.grid)))
        
        obstacle_coordinates = obs.copy()
        
        # Sensitivity (obstacle points per block, think of it as a threshold)
        sensitivity = 1


        # Iterate through the list of obstacle coordinates
        for obstacle in obstacle_coordinates:
            # Convert obstacle coordinates to grid coordinates
            grid_x, grid_y = self.car_to_grid(obstacle)

            # Increment the value of the corresponding grid cell, ensure that its valid too
            if 0 <= grid_x < len(self.grid) and 0 <= grid_y < len(self.grid):
                self.grid[grid_y, grid_x] += 1

        self.grid = np.where(self.grid < sensitivity, 0, 1)

        return self.grid
    
    def setTarget_xy_in_website(self, coordinates):
        self.togo_position = self.get_in_grid_coords((coordinates[0],coordinates[1]))
        print(f"Website coord : {coordinates} ")
 