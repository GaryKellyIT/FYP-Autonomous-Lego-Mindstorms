'''
Author: Gary Kelly - C16380531
Description: Program to detect speed sign from an image
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
#print(templates)

for template_path in templates:
    template = cv2.imread(template_path, 0)
    template_name = template_path[len(speed_sign_template_dir) - 1:-4]
    #print(template_name)
    cached_speed_sign_templates[template_name] = template

    

def detect_speed_sign(image,outputImage):
    hsvImage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    LowerRedRangeLower=(0,100,100)
    LowerRedRangeUpper=(160,100,100)
    UpperRedRangeLower=(160,100,100)
    UpperRedRangeUpper=(180,255,255)

    lowerMask = cv2.inRange(hsvImage, LowerRedRangeLower, UpperRedRangeLower)
    upperMask = cv2.inRange(hsvImage, LowerRedRangeUpper, UpperRedRangeUpper)
    mask = lowerMask + upperMask


    processed_image = image_processing.process_image(hsvImage,mask,outputImage)

    if processed_image is None:
        return None
    
    processed_image = image_processing.image_resize(processed_image,138,138)

    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_HSV2BGR)
    processed_image_gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("sliced",processed_image_gray)
    template_likelihood = {}
    for template in cached_speed_sign_templates:
        res = cv2.matchTemplate(processed_image_gray, cached_speed_sign_templates[template], cv2.TM_CCOEFF_NORMED)
        template_likelihood[template] = max(res)
        print(max(res))
        

    if template_likelihood:
        return max(template_likelihood, key=template_likelihood.get)
    
    return 0
    




def validate_circle(image):
    '''
    similar to process_image but uses Hough Circle to validate contour is circular
    return 1 for circle, 0 for no circle
    '''

