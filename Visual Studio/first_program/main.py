#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Write your program here
#brick.sound.beep()

#initialize two motors and drive base
left = Motor(Port.B)
right = Motor(Port.C)
robot = DriveBase(left, right, 56, 114)

#initialize sensors
ultrasonic_sensor = UltrasonicSensor(Port.S4)
colour_sensor = ColorSensor(Port.S1)

# Drive forward until an object is detected
robot.drive(100, 0)
while ultrasonic_sensor.distance() > 300:
    #print("still in loop")
    print(ultrasonic_sensor.distance())
    
print("Less than now")
wait(5)

print(ultrasonic_sensor.distance())
robot.stop()


#brick.sound.beep(1000, 500)
