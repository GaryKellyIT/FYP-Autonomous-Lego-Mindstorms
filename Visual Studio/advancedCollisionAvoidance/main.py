#!/usr/bin/env micropython

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, ColorSensor

#left = LargeMotor(OUTPUT_B)
#right = LargeMotor(OUTPUT_C)

# Instantiate the MoveTank object
tank = MoveTank(OUTPUT_B, OUTPUT_C)

tank.color = ColorSensor(INPUT_1)
tank.gyro = GyroSensor(INPUT_2)
tank.side_us = UltrasonicSensor(INPUT_3)
tank.front_us = UltrasonicSensor(INPUT_4)


while tank.color.reflected_light_intensity > 12: 
    if tank.front_us.distance_centimeters < 20:
        #collision avoidance
        tank.gyro.mode = 'GYRO-RATE'
        tank.gyro.mode = 'GYRO-ANG'
        print(tank.gyro.angle)
        #tank.gyro.reset()
        while tank.gyro.angle > -88:
            tank.on(0,20)
        while tank.side_us.distance_centimeters < 50:
            tank.on(20,20)
        while tank.gyro.angle < -2:
            tank.on(20,0)
        while tank.side_us.distance_centimeters < 50:
            tank.on(20,20)
        while tank.gyro.angle < 88:
            tank.on(20,0)
        while tank.color.reflected_light_intensity < 40:
            tank.on(20,20)
        
        tank.stop()
    else:
        #line follow
        b_power = (50 - tank.color.reflected_light_intensity) * 1
        c_power = (tank.color.reflected_light_intensity - 21) * 1
        tank.on(b_power,c_power)
