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


CURRENT_SPEED_LIMIT = "None"
CURRENT_TRAFFIC_LIGHT = "None"


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
    image = cv2.imread("Test/GreenClose.jpg")
    image = image_processing.image_resize(image,500)

    
    #Add Noise - Uncomment to add noise
    #image = image_processing.saltAndPepper(image,0.05)
    #image = image_processing.alter_brightness(image,5)
    #image = image_processing.changeOrientation(image,0)

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
    #checking for previous files and deleting
    if os.path.exists("imageResults.csv"):
      os.remove("imageResults.csv")
    else:
      print("The file does not exist")

    
    image7 = cv2.imread("test/50far.jpg")
    outputImage = image7.copy()
    outputImage2 = image7.copy()
            
    with open('imageResults.csv', 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(Headings)
        for image in images:
            images[image] = image_processing.image_resize(images[image],500)
            print("Starting image:" + image)
            for i in np.arange(0,0.25,0.05):
                Temp = image_processing.saltAndPepper(images[image],i)
                currentLights = trafficLightRecog.detect_traffic_light(Temp,outputImage)
                currentSpeedSign = speedSignRecog.detect_speed_sign(Temp,outputImage2)

                if currentLights is None: #No bounding box detected
                    green = yellow = red = 0
                else:
                    if sum(currentLights) == 0: #No light colour detected
                        green = yellow = red = 0
                    else:
                        if currentLights[0] == 1:
                            green = 1
                        else:
                            green = 0
                        if currentLights[1] == 1:
                            yellow = 1
                        else:
                            yellow = 0
                        if currentLights[2] == 1:
                            red = 1
                        else:
                            red = 0
                            
                if currentSpeedSign != None:
                    speed = currentSpeedSign
                else:
                    speed = "None"
                row = [image , i,"0","0",green,yellow,red,speed]
                writer.writerow(row)
                
            for j in np.arange(5,30,5):
                Temp = image_processing.alter_brightness(images[image],j)
                currentLights = trafficLightRecog.detect_traffic_light(Temp,outputImage)
                currentSpeedSign = speedSignRecog.detect_speed_sign(Temp,outputImage2)

                if currentLights is None: #No bounding box detected
                    green = yellow = red = 0
                else:
                    if sum(currentLights) == 0: #No light colour detected
                        green = yellow = red = 0
                    else:
                        if currentLights[0] == 1:
                            green = 1
                        else:
                            green = 0
                        if currentLights[1] == 1:
                            yellow = 1
                        else:
                            yellow = 0
                        if currentLights[2] == 1:
                            red = 1
                        else:
                            red = 0
                            
                if currentSpeedSign != None:
                    speed = currentSpeedSign
                else:
                    speed = "None"
                row = [image , "0","0",j,green,yellow,red,speed]
                writer.writerow(row)

            for k in np.arange(2,12,2):
                Temp = image_processing.changeOrientation(images[image],k)
                currentLights = trafficLightRecog.detect_traffic_light(Temp,outputImage)
                currentSpeedSign = speedSignRecog.detect_speed_sign(Temp,outputImage2)

                if currentLights is None: #No bounding box detected
                    green = yellow = red = 0
                else:
                    if sum(currentLights) == 0: #No light colour detected
                        green = yellow = red = 0
                    else:
                        if currentLights[0] == 1:
                            green = 1
                        else:
                            green = 0
                        if currentLights[1] == 1:
                            yellow = 1
                        else:
                            yellow = 0
                        if currentLights[2] == 1:
                            red = 1
                        else:
                            red = 0
                            
                if currentSpeedSign != None:
                    speed = currentSpeedSign
                else:
                    speed = "None"
                row = [image , "0",k,"0",green,yellow,red,speed]
                writer.writerow(row)

    csvFile.close()

     

main()
#create_csv(cached_test_images) #Uncomment to recreate csv file
