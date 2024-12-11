# The class CarSimulator is a simple 2D vehicle simulator.
# The vehicle states are:
# - x: is the position on the x axis on a xy plane
# - y: is the position on the y axis on a xy plane
# - v is the vehicle speed in the direction of travel of the vehicle
# - theta: is the angle wrt the x axis (0 rad means the vehicle
#   is parallel to the x axis, in the positive direction;
#   pi/2 rad means the vehicle is parallel
#   to the y axis, in the positive direction)
# - NOTE: all units are SI: meters (m) for distances, seconds (s) for
#   time, radians (rad) for angles...
#
# (1)
# Write the method "simulatorStep", which should update
# the vehicle states, given 3 inputs:
#  - a: commanded vehicle acceleration
#  - wheel_angle: steering angle, measured at the wheels;
#    0 rad means that the wheels are "straight" wrt the vehicle.
#    A positive value means that the vehicle is turning counterclockwise
#  - dt: duration of time after which we want to provide
#    a state update (time step)
#
# (2)
# Complete the function "main". This function should run the following simulation:
# - The vehicle starts at 0 m/s
# - The vehicle drives on a straight line and accelerates from 0 m/s to 10 m/s
#   at a constant rate of 0.4 m/s^2, then it proceeds at constant speed.
# - Once reached the speed of 10 m/s, the vehicle drives in a clockwise circle of
#   roughly 100 m radius
# - the simulation ends at 100 s
#
# (3)
# - plot the vehicle's trajectory on the xy plane
# - plot the longitudinal and lateral accelerations over time

import numpy as np
import matplotlib.pyplot as plt

class CarSimulator():
    def __init__(self, wheelbase, v0, theta0):
        # INPUTS:
        # the wheel base is the distance between the front and the rear wheels
        self.wheelbase = wheelbase
        self.x = 0
        self.y = 0
        self.v = v0
        self.theta = theta0

    def simulatorStep(self, a, wheel_angle, dt):
        # update the vehicle speed. a = dv/dt so dv = a*dt and v_new = v_old + dv
        self.v = self.v + a * dt

        # update the vehicle orientation
        if (wheel_angle == 0):
            # car is going straight so no change in theta, angular velocity is 0
            omega = 0
        else:
            # turning radius computed using wheelbase and wheel angle
            turning_radius = self.wheelbase / np.tan(wheel_angle)
            omega = self.v / turning_radius # angular velocity
        
        # new angle = old angle + angular velocity * dt
        self.theta = self.theta + omega * dt

        # update the vehicle position:
        # x_new = x_old + dx where dx = v_x*dt and v_x = v*cos(theta)
        # is the x-component of velocity.
        self.x = self.x + self.v * np.cos(self.theta) * dt
        # y_new = y_old + dy where dy = v_y*dt and v_y = v*sin(theta)
        # is the y-component of velocity.
        self.y = self.y + self.v * np.sin(self.theta) * dt


def main():
    wheelbase = 4  # arbitrary 4m wheelbase
    v0 = 0         # initial velocity
    theta0 = 0     # initial angle relative to x-axis
    simulator = CarSimulator(wheelbase, v0, theta0)
    dt = 0.01       # arbitrarily set the time step to 0.1 s

    # simulation variables
    time = 100     # total simulation time (seconds)
    steps = int(time / dt)
    t = np.linspace(0, time, steps)

    # arrays to store data for plotting
    x_positions = []
    y_positions = []
    longitudinal_accelerations = []
    lateral_accelerations = []

    # Simulation loop
    for step in range(steps):
        # Phase 1: accelerate to 10 m/s in a straight line
        if simulator.v < 10:
            a = 0.4  # constant longitudinal acceleration
            wheel_angle = 0  # no steering
        # Phase 2: maintain speed and turn in a clockwise circle
        else:
            a = 0  # constant speed, longitudinal acceleration of 0
            # turning radius of ~100m, negative value means the vehicle is
            # turning clockwise
            wheel_angle = -np.arctan(simulator.wheelbase / 100)
        
        # Compute lateral acceleration
        if wheel_angle != 0:
            # compute turning radius based on wheelbase, wheel angle
            turning_radius = simulator.wheelbase / np.tan(wheel_angle)
            # acceleration of theta = v^2 / r
            lateral_acceleration = simulator.v ** 2 / turning_radius
        else:
            lateral_acceleration = 0 # vehicle traveling straight, no lateral acceleration

        # Step simulation
        simulator.simulatorStep(a, wheel_angle, dt)

        # Store data
        x_positions.append(simulator.x)
        y_positions.append(simulator.y)
        longitudinal_accelerations.append(a)
        lateral_accelerations.append(lateral_acceleration)

    # Plot trajectory on xy plane
    plt.figure()
    plt.plot(x_positions, y_positions, label="Trajectory")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Vehicle Trajectory")
    plt.legend()
    plt.grid()
    plt.axis('equal') # make axis scales equal so we should see a circle.

    # Plot longitudinal and lateral accelerations over time
    plt.figure()
    plt.plot(t, longitudinal_accelerations, label="Longitudinal Acceleration (m/s²)")
    plt.plot(t, lateral_accelerations, label="Lateral Acceleration (m/s²)")
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s²)")
    plt.title("Accelerations Over Time")
    plt.legend()
    plt.grid()

    # Show plots
    plt.show()

main()
