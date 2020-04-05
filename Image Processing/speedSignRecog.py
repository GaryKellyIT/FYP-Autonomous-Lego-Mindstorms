'''
Author: Gary Kelly - C16380531
Description: Program to detect speed sign from an image
Method: 
Inputs: Original image, copy of original image for displaying output
Outputs: returns int - 30 OR 50 OR 60 OR 80 OR 100 OR 120 OR None
'''
import numpy as np
import cv2
import os
import glob
import image_processing

'''
Read in templates
'''
cached_speed_sign_templates = {}
speed_sign_template_dir = 'Templates/*'
templates = glob.glob(speed_sign_template_dir)

for template_path in templates:
    template = cv2.imread(template_path, 0)
    template_name = template_path[len(speed_sign_template_dir) - 1:-4]
    cached_speed_sign_templates[template_name] = template

    
def detect_speed_sign(image,outputImage):
    hsvImage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    LowerRedRangeLower=(0,100,100)
    LowerRedRangeUpper=(10,255,255)
    UpperRedRangeLower=(160,100,100)
    UpperRedRangeUpper=(180,255,255)

    lowerMask = cv2.inRange(hsvImage, LowerRedRangeLower, LowerRedRangeUpper)
    upperMask = cv2.inRange(hsvImage, UpperRedRangeLower, UpperRedRangeUpper)
    mask = lowerMask + upperMask

    #cv2.imshow("mask",mask)
    processed_image = image_processing.process_image(image,mask,outputImage)

    if processed_image is None:
        return None
    
    processed_image = image_processing.image_resize(processed_image,138,138)

    #processed_image = cv2.cvtColor(processed_image, cv2.COLOR_HSV2BGR)
    processed_image_gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("sliced",processed_image_gray)

    threshold = 0.1
    closestTemplate = image_processing.template_matching(processed_image_gray, cached_speed_sign_templates, threshold)
    
    if closestTemplate:
        return closestTemplate
    else:
        return None
