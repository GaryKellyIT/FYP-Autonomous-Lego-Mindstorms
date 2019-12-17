#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase


#initialize two motors and drive base
left = Motor(Port.B)
right = Motor(Port.C)
wheel_diameter = 56
axle_track = 114
robot = DriveBase(left, right, wheel_diameter, axle_track)

#initialize sensors
ultrasonic_sensor = UltrasonicSensor(Port.S4)

#start driving
robot.drive(100, 0)

# Drive forward until an object is detected within 30cm
while ultrasonic_sensor.distance() > 300:
    print(ultrasonic_sensor.distance())
    

wait(5)

print(ultrasonic_sensor.distance())

#stop
robot.stop()