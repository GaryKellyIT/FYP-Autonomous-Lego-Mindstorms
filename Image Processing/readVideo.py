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
    cached_test_images[test_image_name] = test_image



'''
function to read in video from Pi, process video frame by frame checking for detected
speed signs/ traffic lights and sending the appropriate max speed to lego mindstorms program

traffic light function returns - Array - [Green / Yellow / Red] OR None
Speed Sign function returns - int - 30 OR 50 OR 60 OR 80 OR 100 OR 120 OR None
'''
def main():
    global CURRENT_SPEED_LIMIT
    global CURRENT_TRAFFIC_LIGHT
    image = cv2.imread("test/GreenLight.jpg")
    #image = cv2.imread("Templates/30.png")
    #image = cv2.imread("test.jpg")
    
        
    #image = image_processing.saltAndPepper(image,0.05)
    #image = image_processing.alter_brightness(image,5)
    image = image_processing.changeOrientation(image,10)
    image = image_processing.fixOrientation(image,10)
    DetectedLightBorder = image.copy()
    DetectedSpeedSign = image.copy()

    
    currentLights = trafficLightRecog.detect_traffic_light(image,DetectedLightBorder)
    currentSpeedSign = speedSignRecog.detect_speed_sign(image,DetectedSpeedSign)

    
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
    
    cv2.imshow('detected light border', DetectedLightBorder)
    cv2.imshow('detected speed sign', DetectedSpeedSign)
    key = cv2.waitKey(0)




'''
Function to loop through directory of images adding noise(salt+pepper, altering
orientation, altering saturation) and output results to csv file for visualization.
'''
def create_csv(images):
    Headings = ['Filename', 'Salt+Pepper', 'Orientation', 'Saturation', 'Green detected', 'Yellow detected', 'Red detected', 'Speed detected']

    image7 = cv2.imread("Input/GreenLight.jpg")
    outputImage = image7.copy()
    outputImage2 = image7.copy()
            
    with open('imageResults.csv', 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(Headings)
        for image in images:
            for i in np.arange(0,0.25,0.05):
                
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
