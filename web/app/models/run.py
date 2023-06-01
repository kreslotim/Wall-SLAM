import plotly.graph_objects as go
import matplotlib.pyplot as plt
from pathfinder import PathFinder

obs = [[10,0],[0,10],[-10,0], [-30, -30], [-40, -40] ,[-40, 0], [40, 0], [ 60, 0], [70,-10] ] # Example obstacle coordinates
grid_rad = 100  # Example grid radius

path_finder = PathFinder(obs, cell_dim=10, grid_rad=grid_rad)

current_position = (0,0)  # Example current position

path_finder.setTarget_xy_in_website((0,0))  # Example target position

path = path_finder.dijkstra_shortest_path(path_finder.car_to_grid(current_position)).copy()


action_numbers = path_finder.path_to_actionNumber(current_orr=0)
#print("Action Numbers:", action_numbers)

obstacles_for_website = path_finder.generate_list_of_obstacles_for_website()
print(f"########")


print(f"Togo in grid : {path_finder.togo_position}")
print("Shortest Path:", path)
print("Obstacles for Website:", obstacles_for_website)
print(f"Sequence will then be {path_finder.path_to_actionNumber()}")

for this in path :
    if this != -1:
        print(path_finder.__grid_to_website(this))
# Plotting the grid with obstacles

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
if path and path[0] != -1 :
    path_x = [coord[1] for coord in path]  # Reversed indexing
    path_y = [coord[0] for coord in path]  # Reversed indexing
    plt.plot(path_y, path_x, color='red', linewidth=2)

# Display the plot
plt.show()