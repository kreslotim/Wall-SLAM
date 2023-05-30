from collections import deque
import heapq
import numpy as np

class PathFinder:
    def __init__(self, obs):
        # Target position
        self.target_x = 0
        self.target_y = 0 

        # Target route
        self.x_route = []
        self.y_route = []

        # "Radius" of the square grid cm
        self.grid_rad = 100
        self.cell_dim = 1
        self.obs = obs
        self.grid = generateGrid()


  
    def generateGrid(self, obs):
        """
        Generate grid from collected obstacle scans

        :param obst: raw list of obstacles in car coordinates  
        :return: sampled grid with cells set to 1 or 0
        """
        # Initialize the 2D array representing the grid map
        self.grid = np.zeros((int(2*self.grid_rad / self.cell_dim), int(2*self.grid_rad / self.cell_dim)))
        obstacle_coordinates = obs.copy()
        
        # Sensitivity (obstacle points per block, think of it as a threshold)
        sensitivity = 3

        # Iterate through the list of obstacle coordinates
        for obstacle in obstacle_coordinates:
            # Convert obstacle coordinates to grid coordinates
            grid_x = self.car_to_grid_coor(obstacle, 100, 10)[0]
            grid_y = self.car_to_grid_coor(obstacle, 100, 10)[1]

            # Increment the value of the corresponding grid cell, ensure that its valid too
            if 0 <= grid_x < 2*self.grid_rad / self.cell_dim and 0 <= grid_y < 2*self.grid_rad / self.cell_dim:
                self.grid[grid_y, grid_x] += 1

        self.grid = np.where(self.grid < sensitivity, 0, 1)

        return self.grid
   

    def dijkstra_shortest_path(self, grid_pos, grid_dest, grid):
        rows = len(grid)
        cols = len(grid[0])

        # Check for trivial case: the current position is the destination
        if grid_pos == grid_dest or grid[grid_dest[0]][grid_dest[1]] == 1:
            return [-1]

        # Create a priority queue for Dijkstra's algorithm
        queue = [(0, grid_pos)]
        heapq.heapify(queue)

        # Create a dictionary to track distances from the starting position
        distances = {grid_pos: 0}

        # Create a dictionary to track the previous positions in the shortest path
        previous = {}

        # Define possible directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        direction_names = ['N', 'S', 'W', 'E']

        while queue:
            current_dist, current_pos = heapq.heappop(queue)

            # Check if the current position is the destination
            if current_pos == grid_dest:
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

