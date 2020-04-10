'''
Author: Gary Kelly - C16380531
Description: Program to detect traffic light from an image
Method: 1)Take in image
        2)Threshold for black
        3)Find largest contour
        4)Find min area rectangle for this contour
        4)Use this min area rectangle as region of interest
        5)Create 3 masks using this ROI - one for each of the colours of the traffic light
        6)Perform Hough circles transfor on each of these masks and display resulting circles
        7)Return array containing colours of lights found
Inputs: Original image, copy of original image for displaying output
Outputs: Array - [Green / Yellow / Red] OR None
'''
import numpy as np
import cv2
import image_processing

def detect_traffic_light(image,outputImage):
    
    lowerBlack = np.array([0,0,0])
    upperBlack = np.array([90,120,90])
    mask = cv2.inRange(image, lowerBlack, upperBlack)
    #cv2.imshow("Black Mask",mask)
    processed_image = image_processing.process_image(image,mask,outputImage)

    if processed_image is None:
        return None
    

    hsvImage = cv2.cvtColor(processed_image, cv2.COLOR_BGR2HSV)

    #color range
    #lowerRed1 = np.array([0,170,100])
    #upperRed1 = np.array([10,255,255])
    lowerRed2 = np.array([160,170,100])
    upperRed2 = np.array([180,255,255])
    lowerGreen = np.array([40,140,90])
    upperGreen = np.array([90,255,255])
    lowerYellow = np.array([15,150,150])
    upperYellow = np.array([35,255,255])

    #create masks
    #lowerRedMask = cv2.inRange(hsvImage, lowerRed1, upperRed1)
    redMask = cv2.inRange(hsvImage, lowerRed2, upperRed2)#upperRedMask
    greenMask = cv2.inRange(hsvImage, lowerGreen, upperGreen)
    yellowMask = cv2.inRange(hsvImage, lowerYellow, upperYellow)
    #redMask = cv2.add(lowerRedMask, upperRedMask)

    shape = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    greenMask= cv2.morphologyEx(greenMask,cv2.MORPH_CLOSE,shape)
    yellowMask = cv2.morphologyEx(yellowMask,cv2.MORPH_CLOSE,shape)
    redMask= cv2.morphologyEx(redMask,cv2.MORPH_CLOSE,shape)
    #cv2.imshow("redMask",redMask)
    
    redVal = image_processing.detect_light_colour(hsvImage, redMask, outputImage)
    yellowVal = image_processing.detect_light_colour(hsvImage, yellowMask, outputImage)
    greenVal = image_processing.detect_light_colour(hsvImage, greenMask, outputImage)
  
    #print("greenVal is :"+ str(greenVal))
    #print("yellowVal is :"+ str(yellowVal))
    #print("redVal is :"+ str(redVal))

    lightsDetected = [greenVal,yellowVal,redVal]
    return lightsDetected

