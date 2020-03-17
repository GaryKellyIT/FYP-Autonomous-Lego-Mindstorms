'''
Author: Gary Kelly - C16380531
Description: Program to detect traffic light from an image
'''
def detect_traffic_light(image,outputImage):
    processed_image = image_processing.process_image(image,lowerBlack,upperBlack,outputImage)
    image_processing.detect_light_colour(processed_image, lowerRed, upperRed, outputImage)
    image_processing.detect_light_colour(processed_image, lowerRed, upperRed, outputImage)
    image_processing.detect_light_colour(processed_image, lowerRed, upperRed, outputImage)
    

def detect_light_colour(processed_image, lowerRange, upperRange, outputImage):
    mask = cv2.inRange(image, lowerRange, upperRange)

    resulting_image = cv2.bitwise_and(processed_image, processed_image, mask=mask)

    grayscale_image = cv2.cvtColor(resulting_image, cv2.COLOR_HSV2RGB)
    grayscale_image = cv2.cvtColor(grayscale_image, cv2.COLOR_RGB2GRAY)

    grayscale_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)

    circles = cv2.HoughCircles(grayscale_image, cv2.HOUGH_GRADIENT, 1, 80, param1 = 50, param2 = 18, minRadius = 25, maxRadius = 70)

    draw_detected_circles(outputImage, circles)
    
    return value
    
    
def draw_detected_box(copy_image,(x1,y1),(x2,y2)):
    '''
    draw rectangle
    return copy_image
    '''

def draw_detected_circles(outputImage, circles):
    if circles:
        circles = np.round(r_circles[0, :]).astype("int")
     
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(outputImage, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(outputImage, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    return outputImage

def output_result():
    '''
    
    '''
