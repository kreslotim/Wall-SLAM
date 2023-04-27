import math
import serial
import matplotlib.pyplot as plt

# Connect to ESP32 serial port
ser = serial.Serial('COM5', 115200)
ser.flushInput()

# Initialize lists to store data
x_data = []
y_data = []
car_positions = []

# Define the size of the plot
plt.xlim([-200, 200])
plt.ylim([-200, 200])

# Read data from serial port and plot it
plt.ion()  # Turn on interactive mode
plt.show()

while True:
    try:
        # Read one line of data from serial port
        data = ser.readline().decode('utf-8').strip()

        # Split the data into orientation, distance, x_car and y_car
        orientation, distance, x_car, y_car = data.split(',')
        orientation = int(orientation)
        distance = int(distance)
        x_car = int(x_car)
        y_car = int(y_car)

        # Calculate the x and y coordinates of the point
        # Convert orientation from degrees to radians
        orientation = math.radians(orientation)

        # Calculate X and Y coordinates
        point_x = x_car + distance * math.cos(orientation)
        point_y = y_car + distance * math.sin(orientation)

        # Add the coordinates to the data lists
        x_data.append(point_x)
        y_data.append(point_y)

        # Plot the point with blue dots
        plt.plot(x_data, y_data, 'bo')

        # Plot the car position with red dots and store it in car_positions
        car_position = (x_car, y_car)
        car_positions.append(car_position)
        plt.plot(x_car, y_car, 'ro')

        # Connect the red dots with a line
        if len(car_positions) > 1:
            car_x, car_y = zip(*car_positions)
            plt.plot(car_x, car_y, 'r-')

        # Update the plot
        plt.draw()
        plt.pause(0.1)

    except KeyboardInterrupt:
        break

# Close serial port
ser.close()
