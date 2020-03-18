'''
Author: Gary Kelly - C16380531
Description: Program to detect traffic light from an image
Method: 
Inputs: Original image, copy of original image for displaying output
Outputs: Array - [Green / Yellow / Red] OR None
'''
import numpy as np
import cv2
import image_processing

def detect_traffic_light(image,outputImage):
    
    lowerBlack = np.array([0,0,0])
    upperBlack = np.array([90,90,90])
    mask = cv2.inRange(image, lowerBlack, upperBlack)
    processed_image = image_processing.process_image(image,mask,outputImage)
    detectedLights = processed_image.copy()

    if processed_image is None:
        return None
    


    hsvImage = cv2.cvtColor(processed_image, cv2.COLOR_BGR2HSV)

    #color range
    lowerRed1 = np.array([0,170,100])
    upperRed1 = np.array([10,255,255])
    lowerRed2 = np.array([160,170,100])
    upperRed2 = np.array([180,255,255])
    lowerGreen = np.array([40,140,90])
    upperGreen = np.array([90,255,255])
    lowerYellow = np.array([15,150,150])
    upperYellow = np.array([35,255,255])

    #create masks
    lowerRedMask = cv2.inRange(hsvImage, lowerRed1, upperRed1)
    upperRedMask = cv2.inRange(hsvImage, lowerRed2, upperRed2)
    greenMask = cv2.inRange(hsvImage, lowerGreen, upperGreen)
    yellowMask = cv2.inRange(hsvImage, lowerYellow, upperYellow)
    redMask = cv2.add(lowerRedMask, upperRedMask)
    
    redVal = image_processing.detect_light_colour(hsvImage, redMask, detectedLights)
    yellowVal = image_processing.detect_light_colour(hsvImage, yellowMask, detectedLights)
    greenVal = image_processing.detect_light_colour(hsvImage, greenMask, detectedLights)

    cv2.imshow("Detected Lights",detectedLights)

    
    
    print("greenVal is :"+ str(greenVal))
    print("yellowVal is :"+ str(yellowVal))
    print("redVal is :"+ str(redVal))

    lightsDetected = [greenVal,yellowVal,redVal]

    return lightsDetected

