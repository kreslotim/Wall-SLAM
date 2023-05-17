import math
import heapq

def dijkstra(grid, start, end):
    rows = len(grid)
    cols = len(grid[0])
    distances = [[float('inf')] * cols for _ in range(rows)]
    distances[start[0]][start[1]] = 0
    pq = [(0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_node == end:
            return distances[end[0]][end[1]]

        if current_dist > distances[current_node[0]][current_node[1]]:
            continue

        neighbors = get_neighbors(grid, current_node)
        for neighbor in neighbors:
            neighbor_dist = current_dist + 1  # Assuming each step has a cost of 1
            if neighbor_dist < distances[neighbor[0]][neighbor[1]]:
                distances[neighbor[0]][neighbor[1]] = neighbor_dist
                heapq.heappush(pq, (neighbor_dist, neighbor))

    # No path found
    return -1

def get_neighbors(grid, node):
    rows = len(grid)
    cols = len(grid[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []

    for dx, dy in directions:
        nx, ny = node[0] + dx, node[1] + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 1:
            neighbors.append((nx, ny))

    return neighbors

def create_grid(size, obstacles):
    grid = [[0] * size[1] for _ in range(size[0])]
    for obstacle in obstacles:
        x, y = int(math.floor(obstacle[0])), int(math.floor(obstacle[1]))
        grid[x][y] = 1
    return grid

# Example usage:
obstacle_table = [(0.5, 0.5), (1.2, 1.7), (2.8, 3.3)]
grid_size = (4, 4)
start = (0, 0)
end = (3, 3)

grid = create_grid(grid_size, obstacle_table)

shortest_distance = dijkstra(grid, start, end)
if shortest_distance == -1:
    print("No path found.")
else:
    print("Shortest distance:", shortest_distance)
