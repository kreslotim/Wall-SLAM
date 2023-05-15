import rover as rov
import generate_shapes as shapes

import matplotlib.pyplot as plt
import numpy as np

landmarks = np.array([[[-5, 6], [-6, 5], [-7, 6], [-6, 7]], [[-3, 4], [-1, 4], [-1, 2], [-3, 2]], [[1, 0], [0, -2], [2, -2]], [[-2, -6], [1, -7], [2, -10], [-5, -7]], [[-3, 0], [-2, 0], [-1, -1], [-2, -2], [-3, -2], [-4, -1]]])
scan_rate = 16

chewy = rov.Rover(np.array([-5, 5]), 20)
chewy.set_landmark(landmarks)

for i in range(10):
    chewy.scan_zone(scan_rate)
    chewy.move(0)
for i in range(10):
    chewy.scan_zone(scan_rate)
    chewy.move(1.5 * np.pi)
for i in range(10):
    chewy.scan_zone(scan_rate)
    chewy.move(np.pi)
for i in range(10):
    chewy.scan_zone(scan_rate)
    chewy.move(0.5 * np.pi)

points = np.array(chewy.points)
points = points.T

position = np.array(chewy.past_pos)
position = position.T

print(points.shape)

plt.plot(points[0], points[1], "*b")
plt.plot(position[0], position[1], "xr")
plt.xlim(-chewy.max_size, chewy.max_size)
plt.ylim(-chewy.max_size, chewy.max_size)
plt.show()
plt.close()
