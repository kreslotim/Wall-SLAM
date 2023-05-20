# Used numpy because it is a bit simpler with the arrays
import numpy as np

# Initialize the 2D array representing the grid map
grid = np.zeros((20, 20))

# Generate random obstacles for testing
num_obstacles = 500
obstacle_coordinates = np.random.randint(-100, 101, size=(num_obstacles, 2))

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

# Denoise?
grid[grid < sensitivity] = 0
# Set occupied cells at least 3 obstacles
grid[grid >= sensitivity] = 1

# Print the resulting grid
print(grid)
