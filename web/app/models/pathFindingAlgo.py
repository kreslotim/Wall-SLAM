from collections import deque
import numpy as np

class PathFinder:
 
    def __init__(self):
        self.target_x = 0
        self.target_y = 0            
            
    def generateGrid(self, obst):
        """
        Generate grid from collected obstacle scans

        :param obst: raw list of obstacles in car coordinates
        :return: sampled grid with cells set to 1 or 0
        """
        # Initialize the 2D array representing the grid map
        grid = np.zeros((20, 20))
        obstacle_coordinates = obst
        cell_dimension = 10
        # Sensitivity (obstacle points per block, think of it as a threshold)
        sensitivity = 3

        # Iterate through the list of obstacle coordinates
        for obstacle in obstacle_coordinates:
            # Convert obstacle coordinates to grid coordinates
            grid_x = int((obstacle[0] + 100) / cell_dimension)
            grid_y = int((100 - obstacle[1]) / cell_dimension)

            # Increment the value of the corresponding grid cell, ensure that its valid too
            if 0 <= grid_x < 20 and 0 <= grid_y < 20:
                grid[grid_y, grid_x] += 1

        # Denoise
        grid[grid < sensitivity] = 0
        # Set occupied cells at least 3 obstacles
        grid[grid >= sensitivity] = 1

        return grid


    def shortest_path(self, grid_pos, grid_dest, grid):
        """
        Finds the shortest path between two cells of the grid
        :param grid_pos: departure cell
        :param grid_dest: destination cell
        :param grid: sampled obstacles as a discrete grid
        :return: array with global path instructions e.g. go [N,N,N,E,E,S,S,...]
        """
        rows = len(grid)
        cols = len(grid[0])

        # Check for trivial case: the current position is the destination
        if grid_pos == grid_dest or grid[grid_dest[0]][grid_dest[1]] == 1:
            return []

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

                    # Check if the new position is not an obstacle and not visited
                    if grid[new_x][new_y] == 0 and new_pos not in visited:
                        queue.append((new_pos, path + [direction_names[i]]))
                        visited.add(new_pos)

        # If there is no path to the destination
        return []


    def encode_directions(self, path):
        """
        :param path: global path instructions e.g. go [N,N,N,E,E,S,S,...]
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
        :return: array of instructions to the car to execute, e.g. ['L', 'L', 'F', 'F'] can be changed to action numbers in
                def path_to_seq(orient, path)
        """
        current_orientation = orient
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
                car_instructions.append("L")
                current_orientation = (current_orientation + 90) % 360

            while i < len(global_instructions) and current_orientation == global_instructions[i]:
                car_instructions.append("F")
                i += 1

        return car_instructions


    def instructions_to_go_x_y(self, pos_car, orientation, obst):
        """
            Calculates the shortest route
                :param obst: list of obstacles
                :param orientation: initial orientation of robot (N=0, W=90, ...)
                :param dest_car: car destination (x,y) tuple (cm)
                :param pos_car: initial car position (x,y) tuple (cm)

            Returns:
                array of instructions to the car e.g. ['L', 'L', 'F', 'F'] can be changed to action numbers in
                def path_to_seq(orient, path)

                IMPORTANT: returns an empty array in all error cases
                (same start & destination, destination is an obstacle, ...)

            """
        start = (int((100 - pos_car[1]) / 10), int((pos_car[0] + 100) / 10))
        end = (int((100 - self.target_y) / 10), int((self.target_x + 100) / 10))

        grid = self.generateGrid(obst)
        path = self.shortest_path(start, end, grid)
        instr = self.path_to_seq(orientation, path)

        grid[start] = 2  # mark start with 2 in the grid
        grid[end] = 3  # mark end with 3 in the grid
        print(grid)
        print(path)
        print(instr)

        #TODO not optimal 
        return instr[0]