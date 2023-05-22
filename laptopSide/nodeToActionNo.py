import math


def move_to_target(nodes):
    sequence = []
    current_x = 0
    current_y = 0
    current_angle = 90 # Corresponds to our standart def

    for node in nodes:
        target_x, target_y = node

        # Calculate the distance and angle to the target node
        distance = math.sqrt((target_x - current_x) ** 2 + (target_y - current_y) ** 2)
        angle = math.degrees(math.atan2(target_y - current_y, target_x - current_x))

        # Update the robot's orientation
        if angle != current_angle:
            angle_diff = angle - current_angle
            if angle_diff > 0:
                sequence.append(3)  # Encode orientateRight() / turnRight() ?
            else:
                sequence.append(2)  # Encode orientateLeft() / turnLeft() ?

        # Add the forward() function call to the sequence
        sequence.append(1)  # Encode forward()

        # Update the robot's current position and angle
        current_x = target_x
        current_y = target_y
        current_angle = angle

    return sequence


# Test
nodes = [(0, 10), (0, 20), (0, 30), (10, 30), (20, 30), (30, 30), (30, 20), (30, 10), (30, 0), (30, -10)]
encoded_sequence = move_to_target(nodes)

print(encoded_sequence) 

# forward() -> 1
# orientateLeft() -> 2
# orientateRight() -> 3
