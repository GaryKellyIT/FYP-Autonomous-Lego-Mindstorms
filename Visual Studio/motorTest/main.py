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

#initialize timer
timer = StopWatch()
timer.reset()

#start driving
robot.drive(100, 0)

#drive until timer reaches 5s
while timer.time() < 5000:
    print("still driving")

#stop
robot.stop()