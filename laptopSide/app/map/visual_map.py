import numpy as np
import cv2

input_dict = {
    (30, 30): (60, 70),
    (30, 31): (60, 71),
    (30, 32): (60, 72),
    (30, 33): (60, 73),
    (30, 34): (60, 74),
    (31, 30): (61, 70),
    (31, 34): (61, 74),
    (32, 30): (62, 70),
    (32, 34): (62, 74),
    (33, 30): (63, 70),
    (33, 34): (63, 74),
    (34, 30): (64, 70),
    (34, 31): (64, 71),
    (34, 32): (64, 72),
    (34, 33): (64, 73),
    (34, 34): (64, 74),
}

# Define the size of the map
map_size = (200, 200)

# Create an empty map
map_image = np.zeros(map_size, dtype=np.uint8)

# Define the colors for the obstacles and cars
obstacle_color = 255
car_color = 128

# Iterate over the obstacle positions and draw them on the map
for obstacle_pos, car_pos in input_dict.items():
    # Convert the obstacle and car positions to integers
    obstacle_pos = (int(obstacle_pos[0]), int(obstacle_pos[1]))
    car_pos = (int(car_pos[0]), int(car_pos[1]))
    
    # Draw the obstacle as a filled circle
    cv2.circle(map_image, obstacle_pos, radius=5, color=obstacle_color, thickness=-1)
    
    # Draw the car as a filled square
    cv2.rectangle(map_image, car_pos, (car_pos[0]+5, car_pos[1]+5), color=car_color, thickness=-1)

cv2.imshow("Map Rough", map_image)
# Perform image processing to extract the geometrical shapes of the obstacles
# Convert the map image to binary using a threshold
threshold_value = 128
ret, binary_map = cv2.threshold(map_image, threshold_value, 255, cv2.THRESH_BINARY)

# Perform morphological opening to remove small noise
kernel_size = (3, 3)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
opening = cv2.morphologyEx(binary_map, cv2.MORPH_OPEN, kernel)

# Perform connected component labeling to extract the obstacles
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opening)

# Iterate over the connected components and draw their bounding boxes on the map
for i in range(1, num_labels):
    # Get the bounding box of the component
    x, y, w, h, area = stats[i]
    
    # Draw the bounding box on the map
    cv2.rectangle(map_image, (x, y), (x+w, y+h), color=obstacle_color, thickness=2)

# Show the resulting map image
cv2.imshow("Map Image", map_image)
cv2.waitKey(0)
