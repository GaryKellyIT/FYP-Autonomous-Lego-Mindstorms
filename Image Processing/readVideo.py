'''
Author: Gary Kelly - C16380531
Description: Program to take in a live video feed from raspberry pi camera module
             and check for traffic lights / stop signs and act accordingly.
'''
import numpy as np
import cv2
import glob
import csv
import os

import trafficLightRecog
import speedSignRecog
import image_processing


CURRENT_SPEED_LIMIT = 30
CURRENT_TRAFFIC_LIGHT = "None"

#checking for previous files and deleting
if os.path.exists("imageResults.csv"):
  os.remove("imageResults.csv")
else:
  print("The file does not exist")

cached_test_images = {}
test_dir = 'Test/*'
test_images = glob.glob(test_dir)

for test_image_path in test_images:
    test_image = cv2.imread(test_image_path)
    test_image_name = test_image_path[len(test_dir) - 1:-4]
    print(test_image_name)
    cached_test_images[test_image_name] = test_image

'''
read in video frame by frame
for every 5th frame / 10th / whatever value - call functions to detect for
traffic light and stop sign.

traffic light function returns - string - Green / Yellow / Red / None
Speed Sign function returns - int - 30 / 50 /60 /80 /100 / 120 / -1(No sign detected)

depending on return values send commands to mindstorms
'''
def main():
    global CURRENT_SPEED_LIMIT
    global CURRENT_TRAFFIC_LIGHT
    print(CURRENT_SPEED_LIMIT)
    image = cv2.imread("Input/GreenLight.jpg")
    #image = cv2.imread("Templates/30.png")
    
        
    #image = image_processing.saltAndPepper(image,0.05)
    #image = image_processing.alter_brightness(image,5)
    image = image_processing.changeOrientation(image,10)
    image = image_processing.fixOrientation(image,10)
    #image = cv2.imread("test.jpg")
    outputImage = image.copy()
    outputImage2 = image.copy()

    
    currentLights = trafficLightRecog.detect_traffic_light(image,outputImage)
    currentSpeedSign = speedSignRecog.detect_speed_sign(image,outputImage2)

    
    #Evaluating which light has been detected
    if currentLights is None:
        print("No lights detected")
    else:
        if sum(currentLights) > 1:
            print("Multiple lights detected. Slowing down!")
        elif sum(currentLights) == 0:
            print("No lights detected")
        else:
            if currentLights[0] == 1:
                CURRENT_TRAFFIC_LIGHT = "Green"
            elif currentLights[1] == 1:
                CURRENT_TRAFFIC_LIGHT = "Yellow"
            else:
                CURRENT_TRAFFIC_LIGHT = "Red"
    
    #Evaluating current speed limit
    if currentSpeedSign != None:
        CURRENT_SPEED_LIMIT = currentSpeedSign
  
    print(CURRENT_SPEED_LIMIT)
    print(CURRENT_TRAFFIC_LIGHT)
    
    cv2.imshow('detected results', outputImage)
    cv2.imshow('detected results2', outputImage2)
    key = cv2.waitKey(0)

def create_csv(images):
    Headings = ['Filename', 'Salt+Pepper', 'Orientation', 'Saturation', 'Green detected', 'Yellow detected', 'Red detected', 'Speed detected']

    image7 = cv2.imread("Traffic Light Recognition/Input/GreenLight.jpg")
    outputImage = image7.copy()
    outputImage2 = image7.copy()
            
    with open('imageResults.csv', 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(Headings)
        for image in images:
            for i in np.arange(0,0.5,0.05):
                
                Temp = image_processing.saltAndPepper(images[image],i)
                cv2.imshow('input', Temp)
                key = cv2.waitKey(0)
                currentLights = trafficLightRecog.detect_traffic_light(Temp,outputImage)
                currentSpeedSign = speedSignRecog.detect_speed_sign(Temp,outputImage2)
                if currentLights is None:
                    green = yellow = red = 0
                else:
                    if sum(currentLights) == 0:
                        green = yellow = red = 0
                    else:
                        if currentLights[0] == 1:
                            green = 1
                        if currentLights[1] == 1:
                            yellow = 1
                        if currentLights[1] == 1:
                            red = 1
                if currentSpeedSign != None:
                    speed = currentSpeedSign
                row = [image , i,"0","0",green,yellow,red,speed]
                writer.writerow(row)
        

    csvFile.close()

     

main()
#create_csv(cached_test_images)
