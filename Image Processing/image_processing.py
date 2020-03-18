'''
Author: Gary Kelly - C16380531
Description: Collection of useful opencv related functions to be used
             for stop sign detection and traffic light detection.
'''
import numpy as np
import cv2
import random
import imutils

#global variables to store position of sliced image for output purposes
BOUNDING_X = 0
BOUNDING_Y = 0

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
            # initialize the dimensions of the image to be resized and
            # grab the image size
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

            # resize the image
            resized = cv2.resize(image, dim, interpolation = inter)

            # return the resized image
            return resized


def largest_contour(image):
    contours,_ = cv2.findContours(image, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours[0]

def template_matching(image, templates, size):
    template_likelihood = {}
    for template in cached_speed_sign_templates:
        res = cv2.matchTemplate(image, templates[template], cv2.TM_CCOEFF_NORMED)
        print(res)
        print(template)

    if template_likelihood:
        return max(template_likelihood, key=template_likelihood.get)

    return 0


def process_image(image, mask, outputImage):
    contours,_ = cv2.findContours(mask, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    if contours:
        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(outputImage,[box],0,(0,0,255),2)
        #cv2.rectangle(outputImage,(x,y),(x+w,y+h),(0,255,0),2)
    else:
        return None

    slicedImage = crop_minAreaRect(image,rect)
    '''
    x = min(TL[0],BL[0])
    y = min(TL[1],TR[1])
    w = max(TR[0],BR[0]) - x
    h = max(BL[0],BR[0]) - y
    '''
    x=y=0
    w=h=50
    #print(box)
    global BOUNDING_X
    global BOUNDING_y
    BOUNDING_X = x
    BOUNDING_Y = y
    
    #slicedImage = image[y:y+h,x:x+w]

    return slicedImage


def detect_light_colour(processed_image, mask, outputImage):
    resulting_image = cv2.bitwise_and(processed_image, processed_image, mask=mask)

    grayscale_image = cv2.cvtColor(resulting_image, cv2.COLOR_HSV2RGB)
    grayscale_image = cv2.cvtColor(grayscale_image, cv2.COLOR_RGB2GRAY)

    grayscale_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)

    circles = cv2.HoughCircles(grayscale_image, cv2.HOUGH_GRADIENT, 1, 80, param1 = 50, param2 = 18, minRadius = 25, maxRadius = 70)

    if circles is None:
        return 0
    else:
        draw_detected_circles(outputImage, circles)
        return 1

def draw_detected_circles(outputImage, circles):     
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(outputImage, (BOUNDING_X + x, BOUNDING_Y + y), r, (0, 255, 0), 4)
            cv2.rectangle(outputImage, (BOUNDING_X + x - 5, BOUNDING_Y + y - 5), (BOUNDING_X + x + 5, BOUNDING_Y + y + 5), (0, 128, 255), -1)
    
    return outputImage



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

def alter_brightness(image, value):
    hsvImage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsvImage)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    hsvImage = cv2.merge((h, s, v))
    output = cv2.cvtColor(hsvImage,cv2.COLOR_HSV2BGR)
    return output

def changeOrientation(image,angle):
    rotated = imutils.rotate_bound(image,angle)
    #convert black bg to white bg
    rotated[np.where((rotated==[0,0,0]).all(axis=2))] = [255,255,255]
    return rotated

def fixOrientation(image,angle):
    rotated = imutils.rotate_bound(image,360-angle)
    #convert black bg to white bg
    rotated[np.where((rotated==[0,0,0]).all(axis=2))] = [255,255,255]
    return rotated

def crop_minAreaRect(img, rect):

    # rotate img
    angle = rect[2]
    rows,cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    img_rot = cv2.warpAffine(img,M,(cols,rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0) 
    box = cv2.boxPoints(rect0)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]    
    pts[pts < 0] = 0

    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1], 
                       pts[1][0]:pts[2][0]]

    return img_crop
