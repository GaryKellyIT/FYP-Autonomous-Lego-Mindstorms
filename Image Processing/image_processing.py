'''
Author: Gary Kelly - C16380531
Description: Collection of useful opencv related functions to be used
             for stop sign detection and traffic light detection.
'''
import numpy as np
import cv2
import random
import imutils

BOUNDING_X = 0
BOUNDING_Y = 0

'''
Function to resize image to given dimensions, used for template matching
'''
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
            dim = None
            (h, w) = image.shape[:2]

            # if both the width and height are None, then return the
            # original image
            if width is None and height is None:
                return image

            # check to see if the width is None
            if width is None:
                # calculate the ratio of the height and construct the
                # dimensions
                r = height / float(h)
                dim = (int(w * r), height)

            # otherwise, the height is None
            else:
                # calculate the ratio of the width and construct the
                # dimensions
                r = width / float(w)
                dim = (width, int(h * r))

            resized = cv2.resize(image, dim, interpolation = inter)

            return resized
        

'''
Function to find most similar image from templates
'''
def template_matching(image, templates, threshold):
    template_likelihood = {}
    for template in templates:
        res = cv2.matchTemplate(image, templates[template], cv2.TM_CCOEFF_NORMED)
        template_likelihood[template] = max(res)
        #print(template)
        #print(max(res))

    #print(float(max(template_likelihood.values())))
    if template_likelihood:
        if float(max(template_likelihood.values())) > threshold:
            return max(template_likelihood, key=template_likelihood.get)

    return None

'''
Function to get largest contour from a mask
'''
def largest_contour(mask):
    contours,_ = cv2.findContours(mask, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if contours:
        return contours
    else:
        return None

'''
Function to process image and get smallest bounding box of largest contour
'''
def process_image(image, mask, outputImage):
    #call largest contour
    contours = largest_contour(mask)
    if contours:
        x,y,w,h=cv2.boundingRect(contours[0])
        cv2.rectangle(outputImage,(x,y),(x+w,y+h),(0,255,0),2)
    else:
        return None

    global BOUNDING_X
    global BOUNDING_Y
    BOUNDING_X = x
    BOUNDING_Y = y
    #cv2.imshow("original image",image)
    slicedImage = image[y:y+h,x:x+w]
    #slicedImage = cv2.cvtColor(slicedImage, cv2.COLOR_HSV2BGR)
    #cv2.imshow("sliced image",slicedImage)

    return slicedImage

'''
Function to detect traffic light colour being shown
'''
def detect_light_colour(processed_image, mask, outputImage):
    resulting_image = cv2.bitwise_and(processed_image, processed_image, mask=mask)

    grayscale_image = cv2.cvtColor(resulting_image, cv2.COLOR_HSV2BGR)
    grayscale_image = cv2.cvtColor(grayscale_image, cv2.COLOR_BGR2GRAY)

    grayscale_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)
    
    circles = cv2.HoughCircles(grayscale_image, cv2.HOUGH_GRADIENT, 1, 80, param1 = 50, param2 = 18, minRadius = 15, maxRadius = 70)

    if circles is None:
        return 0
    else:
        draw_detected_circles(outputImage, circles)
        return 1

'''
Function to draw detected traffic light colour being shown, called from detect_light_colour()
'''
def draw_detected_circles(outputImage, circles):     
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(outputImage, (BOUNDING_X + x, BOUNDING_Y + y), r, (0, 255, 0), 4)
            cv2.rectangle(outputImage, (BOUNDING_X + x - 5,BOUNDING_Y + y - 5), (BOUNDING_X + x + 5,BOUNDING_Y + y + 5), (0, 128, 255), -1)
    
    return outputImage


'''
Funtion to add salt and pepper noise to image.
Inputs: image, probability of change (number between 0 and 1)
Outputs: New image
'''
def saltAndPepper(image,prob):
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:#pepper
                output[i][j] = 0
            elif rdn > thres:#salt
                output[i][j] = 255
            else:#same
                output[i][j] = image[i][j]
    return output

'''
Function to alter brightness of image
Inputs: Image, value to change brightness by
Outputs: New image
'''
def alter_brightness(image, value):
    hsvImage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsvImage)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    hsvImage = cv2.merge((h, s, v))
    output = cv2.cvtColor(hsvImage,cv2.COLOR_HSV2BGR)
    return output

'''
Function to change orientation of image
Inputs: Image, angle to change image by
Outputs: New image
'''
def changeOrientation(image,angle):
    rotated = imutils.rotate_bound(image,angle)
    #convert black bg to white bg
    rotated[np.where((rotated==[0,0,0]).all(axis=2))] = [255,255,255]
    return rotated

'''
Function to fix orientation of image
Inputs: Image, angle to change image by
Outputs: New image
'''
def fixOrientation(image,angle):
    rotated = imutils.rotate_bound(image,360-angle)
    #convert black bg to white bg
    rotated[np.where((rotated==[0,0,0]).all(axis=2))] = [255,255,255]
    return rotated

'''
Function to crop rectangle found by minAreaRect function
'''
def crop_minAreaRect(img, rect):

    # rotate img
    angle = rect[2]
    rows,cols = img.shape[0], img.shape[1]

    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    img_rot = cv2.warpAffine(img,M,(cols,rows))

    cv2.imshow("img_rot",img_rot)
    key = cv2.waitKey(0)
    print(rect)
    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0) 
    box = cv2.boxPoints(rect0)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]    
    #pts[pts < 0] = 0
    print(pts)
    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1], 
                       pts[1][0]:pts[2][0]]

    return img_crop
