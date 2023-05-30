from collections import deque
import numpy as np

class PathFinder:
 
    def __init__(self):

        # Target position
        self.target_x = 0
        self.target_y = 0 

        # Target route
        self.x_route = []
        self.y_route = []

        # "Radius" of the sqaure grid cm
        self.grid_rad = 100
        self.cell_dim = 10

        self.grid = []
        self.generateGrid([])

    def instructions_to_go_x_y(self, point_car, orientation, obst):
        """
            Calculates the shortest route
                :param obst: list of obstacles
                :param orientation: initial orientation of robot (N=0, W=90, ...)
                :param dest_car: car destination (x,y) tuple (cm)
                :param pos_car: initial car position (x,y) tuple (cm)

            Returns:
                array of instructions to the car e.g. [1,4,..]  can be modified in
                def path_to_seq(orient, path)

                IMPORTANT: returns an empty array in all error cases
                (same start & destination, destination is an obstacle, ...)

            """
        start = self.car_to_grid(point_car)
        end = [self.target_x, self.target_y]

        # Finding the optimal path 
        grid = self.generateGrid(obst)
        path = self.shortest_path(start, end, grid)
        instr = self.path_to_seq(orientation, path)

        # Mapping path and obstacles
        self.generate_coordinate_path_in_website(path, start)
        self.generate_list_of_obstacles_for_website()
        
        return float(instr[0])

######## HELPER METHODS TO FIND AND SEND PATH #############

    def generateGrid(self, obst):
        """
        Generate grid from collected obstacle scans

        :param obst: raw list of obstacles in car coordinates  
        :return: sampled grid with cells set to 1 or 0
        """
        # Initialize the 2D array representing the grid map
        self.grid = np.zeros((int(2*self.grid_rad / self.cell_dim), int(2*self.grid_rad / self.cell_dim)))
        obstacle_coordinates = obst.copy()
        
        # Sensitivity (obstacle points per block, think of it as a threshold)
        sensitivity = 3

        # Iterate through the list of obstacle coordinates
        for obstacle in obstacle_coordinates:
            # Convert obstacle coordinates to grid coordinates
            grid_x, grid_y = self.car_to_grid(obstacle)

            # Increment the value of the corresponding grid cell, ensure that its valid too
            if 0 <= grid_x < 2*self.grid_rad / self.cell_dim and 0 <= grid_y < 2*self.grid_rad / self.cell_dim:
                self.grid[grid_y, grid_x] += 1

        self.grid = np.where(self.grid < sensitivity, 0, 1)

        return self.grid

    def shortest_path(self, grid_pos, grid_dest, grid):
        """
        Finds the shortest path between two cells of the grid with minimal turns
        :param grid_pos: departure cell
        :param grid_dest: destination cell
        :param grid: sampled obstacles as a discrete grid
        :return: array with global path instructions with minimal turns, e.g., go [N,N,N,E,E,S,S,...]
        """
        rows = len(grid)
        cols = len(grid[0])

        # Check for trivial case: the current position is the destination
        if grid_pos == grid_dest or grid[grid_dest[0]][grid_dest[1]] == 1:
            return [404]

        # Create a queue for BFS algo
        queue = deque([(grid_pos, [])])

        # Create a set to track visited positions
        visited = set([grid_pos])

        # Define possible directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        direction_names = ['N', 'S', 'W', 'E']

        while queue:
            current_pos, path = queue.popleft()

            # Check if the current position is the destination
            if current_pos == grid_dest:
                return path if len(path) != 0 else [-1]

            x, y = current_pos

            # Explore all possible directions
            for i in range(4):
                dx, dy = directions[i]
                new_x = x + dx
                new_y = y + dy

                # Check if the new position is within the grid boundaries
                if 0 <= new_x < rows and 0 <= new_y < cols:
                    new_pos = (new_x, new_y)

                    # Check if the new position is not an obstacle and not visited
                    if grid[new_x][new_y] == 0 and new_pos not in visited:
                        new_path = path + [direction_names[i]]

                        # Check if there will be a turn in direction
                        if len(new_path) >= 2 and new_path[-1] != new_path[-2]:
                            queue.append((new_pos, new_path))
                        else:
                            queue.appendleft((new_pos, new_path))
                        visited.add(new_pos)

        # If there is no path to the destination
        return [404]

    def encode_directions(self, path):
        """
        :param path: global path instructions e.g. go [W,W.]
        :return: encoded global path instructions e.g. go [0,90,90,180,...]
        """
        encoding_map = {'N': 0, 'W': 90, 'S': 180, 'E': 270}
        encoded_list = []

        for direction in path:
            encoded_direction = encoding_map.get(direction)
            if encoded_direction is not None:
                encoded_list.append(encoded_direction)

        return encoded_list
    
    def path_to_seq(self, orient, path):
        """
        :param orient: orientation: initial orientation of robot (N=0, W=90, ...)
        :param path: encoded global path instructions e.g. go [0,90,90,180,...]
        :return: array of instructions to the car to execute, e.g. [1,4,..] can be changed  in
                def path_to_seq(orient, path)
        """
        current_orientation = int(orient)
        global_instructions = self.encode_directions(path)
        car_instructions = []

        # 0 = N
        # 90 = W
        # 180 = S
        # 270 = E
        # moveForward() = F
        # turnRight() = R
        # turnLeft = L

        # algorithm runs in linear time (nearly)
        i = 0
        while i < len(global_instructions):
            while current_orientation != global_instructions[i]:
                if (current_orientation + 180) % 360 == global_instructions[i]:
                    car_instructions.append(4)
                    car_instructions.append(4)
                    current_orientation = (current_orientation + 180) % 360
                elif (current_orientation + 90) % 360 == global_instructions[i]:
                    car_instructions.append(3)
                    current_orientation = (current_orientation + 90) % 360
                else:
                    car_instructions.append(4)
                    current_orientation =  (current_orientation + 270) % 360

            while i < len(global_instructions) and current_orientation == global_instructions[i]:
                    car_instructions.append(1)
                    i += 1
        return car_instructions

######## COORDINATES FOR WEBSITE #############
    
    def generate_coordinate_path_in_website(self,path, initial_position):
        x, y = initial_position
        t_x,t_y = self.grid_to_website((x,y))
        self.x_route = [t_x]
        self.y_route = [t_y]
                            
        if path[0] == 404 :
            self.x_route = []
            self.y_route = [] 
        else :
            for instruction in path:
                if instruction == "N":
                    y -= 1
                elif instruction == "S":
                    y += 1
                elif instruction == "W":
                    x -= 1
                elif instruction == "E":
                    x += 1

                website_x, website_y = self.grid_to_website((x,y))
                self.x_route.append(website_x)
                self.y_route.append(website_y)

        return self.x_route, self.y_route
    
    def generate_list_of_obstacles_for_website(self): 
        if len(self.grid) != 0: 
            obstacle_cell = self.find_positive_coordinates(self.grid) 
            transformed_coordinates = [] 
            for coord in obstacle_cell: 
                transformed_x, transformed_y = self.grid_to_website(coord)
                transformed_coordinates.append((transformed_x, transformed_y)) 
            return transformed_coordinates
        return None
    
    def find_positive_coordinates(self, grid):
        grid = np.array(grid)
        coordinates = np.argwhere(grid == 1)
        return [(x, y) for x, y in coordinates]
 
######## TRANSFORMATION #############

    def website_to_grid(self, point_website): 
        x = len(self.grid)-1 - point_website[1]
        y = point_website[0]
        return x, y
    
    def grid_to_website(self, point_grid): 
        x, =  point_grid[1] 
        y =len(self.grid)- 1 - point_grid[0]
        return x, y
    
    def car_to_grid(self, point_car):
        x = int((self.grid_rad - point_car[1]) / self.cell_dim)
        y = int((point_car[0] + self.grid_rad) / self.cell_dim)
        return x,y

######## SETTER #############

    def setTarget_xy_in_website(self, coordinates):
        self.website_to_grid(coordinates)
        self.target_x = coordinates[0]
        self.target_y = coordinates[1]
        print(f"New Target in grid coord {[self.target_x, self.target_y]} ")

