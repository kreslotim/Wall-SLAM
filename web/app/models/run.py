import plotly.graph_objects as go
import matplotlib.pyplot as plt
from pathfinder import PathFinder

obs = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (2, 0), (1, 0), (2,3), (0,0)]  # Example obstacle coordinates
grid_rad = 100  # Example grid radius

path_finder = PathFinder(obs, cell_dim=10, grid_rad=grid_rad)

current_position = (0, 0)  # Example current position
togo_position = (15, 10)  # Example target position

path = path_finder.dijkstra_shortest_path(current_position, togo_position)
print("Shortest Path:", path)

action_numbers = path_finder.path_to_actionNumber(current_orr=0)
print("Action Numbers:", action_numbers)

obstacles_for_website = path_finder.generate_list_of_obstacles_for_website()
print("Obstacles for Website:", obstacles_for_website)

# Plotting the grid with obstacles
plt.imshow(path_finder.grid, cmap='binary', origin='lower')

# Plotting the obstacles
if obstacles_for_website:
    obstacles_x = [coord[0] for coord in obstacles_for_website]
    obstacles_y = [coord[1] for coord in obstacles_for_website]
    plt.scatter(obstacles_y, obstacles_x, color='blue', marker='s', s=50)

# Setting the grid and axes labels
plt.grid(True)
plt.xlabel('Grid Y')
plt.ylabel('Grid X')

# Display the path
if path:
    path_x = [coord[1] for coord in path]  # Reversed indexing
    path_y = [coord[0] for coord in path]  # Reversed indexing
    plt.plot(path_y, path_x, color='red', linewidth=2)

# Display the plot
plt.show()