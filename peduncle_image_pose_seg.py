# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 14:29:21 2021

@author: ozangokkan
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt

def nothing(x):
    pass

# Load image
# image = cv2.imread('C:/Users/ozangokkan/Desktop/project studies/biber/omron/koyu4.jpg')
image = cv2.imread('C:/Users/ozangokkan/Desktop/project studies/biber/proje/biberli/b3-frames/test/frame183.jpg')
original = image

r,g,b = cv2.split(original)

kernel = np.ones((5,5), np.uint8)
img_erosionr = cv2.erode(r, kernel, iterations=1)
img_erosiong = cv2.erode(g, kernel, iterations=1)
img_erosionb = cv2.erode(b, kernel, iterations=1)
# image = cv2.merge((img_erosionr,img_erosiong,img_erosionb))
# image = cv2.addWeighted(image, 1.5, image, -.5, 0)
# back = cv2.imread('C:/Users/ozangokkan/Desktop/project studies/biber/biberli/b3-frames/test/frame0.jpg',0)
img = cv2.copyMakeBorder(image, 100, 100, 100, 100, cv2.BORDER_CONSTANT)
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
h, s, v = cv2.split(hsv)
# r,g,b = cv2.split(rgb)
# image = cv2.merge((v,g,b))
# diff = image - back
# plt.imshow(diff)


def brightness(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v,value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

# image = brightness(image, value=100)
#cv2.imshow("image", img)
#-------------for hsv color filtering----------
# Create a window
cv2.namedWindow('image')

# Create trackbars for color change
# Hue is from 0-179 for Opencv
cv2.createTrackbar('HMin', 'image', 0, 255, nothing)
cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

# Set default value for Max HSV trackbars
cv2.setTrackbarPos('HMax', 'image', 179)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('VMax', 'image', 255)

# Initialize HSV min/max values
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

while(1):
    image = cv2.resize(image, (1000, 500))
    # Get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'image')
    sMin = cv2.getTrackbarPos('SMin', 'image')
    vMin = cv2.getTrackbarPos('VMin', 'image')
    hMax = cv2.getTrackbarPos('HMax', 'image')
    sMax = cv2.getTrackbarPos('SMax', 'image')
    vMax = cv2.getTrackbarPos('VMax', 'image')

    # Set minimum and maximum HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Convert to HSV format and color threshold
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)

    # Print if there is a change in HSV value
    if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    # Display result image
    cv2.imshow('image', result)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
#kernel = np.ones((2,2),np.uint8)
#result = cv2.dilate(result, kernel, iterations=3)

cv2.imwrite("C:/Users/ozangokkan/Desktop/biber/omron/basler_result_hsv.jpg",result)





#-------------for rgb color filtering-----------------------------------------




image = cv2.imread('C:/Users/ozangokkan/Desktop/biber/omron/basler_result_hsv.jpg')


#-------------for rgb color filtering----------
# Create a window
cv2.namedWindow('image')

cv2.createTrackbar('RMin', 'image', 0, 255, nothing)
cv2.createTrackbar('GMin', 'image', 0, 255, nothing)
cv2.createTrackbar('BMin', 'image', 0, 255, nothing)
cv2.createTrackbar('RMax', 'image', 0, 255, nothing)
cv2.createTrackbar('GMax', 'image', 0, 255, nothing)
cv2.createTrackbar('BMax', 'image', 0, 255, nothing)

cv2.setTrackbarPos('RMax', 'image', 255)
cv2.setTrackbarPos('GMax', 'image', 255)
cv2.setTrackbarPos('BMax', 'image', 255)

# Initialize RGB min/max values
rMin = gMin = bMin = rMax = gMax = bMax = 0
prMin = pgMin = pbMin = prMax = pgMax = pbMax = 0

while(1):
    image = cv2.resize(image, (1000, 500))
    # Get current positions of all trackbars
    rMin = cv2.getTrackbarPos('RMin', 'image')
    gMin = cv2.getTrackbarPos('GMin', 'image')
    bMin = cv2.getTrackbarPos('BMin', 'image')
    rMax = cv2.getTrackbarPos('RMax', 'image')
    gMax = cv2.getTrackbarPos('GMax', 'image')
    bMax = cv2.getTrackbarPos('BMax', 'image')

    # Set minimum and maximum RGB values to display
    lower = np.array([rMin, gMin, bMin])
    upper = np.array([rMax, gMax, bMax])

    # Convert to RGB format and color threshold
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mask = cv2.inRange(rgb, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)

    # Print if there is a change in RGB value
    if((prMin != rMin) | (pgMin != gMin) | (pbMin != bMin) | (prMax != rMax) | (pgMax != gMax) | (pbMax != bMax) ):
        print("(rMin = %d , gMin = %d, bMin = %d), (rMax = %d , gMax = %d, bMax = %d)" % (rMin , gMin , bMin, rMax, gMax , bMax))
        prMin = rMin
        pgMin = gMin
        pbMin = bMin
        prMax = rMax
        pgMax = gMax
        pbMax = bMax

    # Display result image
    cv2.imshow('image', result)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

cv2.imwrite("C:/Users/ozangokkan/Desktop/biber/omron/basler_result_rgb.jpg",result)


#--------------------------processing direction--------------------------------


image = cv2.imread('C:/Users/ozangokkan/Desktop/biber/omron/basler_result_rgb.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
h_,w_,d_ = rgb.shape
direction = 0
kernel = np.ones((2,2),np.uint8)
dilated = cv2.dilate(gray, kernel, iterations=3)
#cv2.imshow("dilate", dilated)
contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
areas = []
for ind, contour_ in enumerate(contours):
        areas.append(cv2.contourArea(contour_)) 
for ind, contour_ in enumerate(contours):
    
    max_area = max(areas)
    if cv2.contourArea(contour_) == max_area:
        first_topleft_x,first_topleft_y, w, h = cv2.boundingRect(contour_)
        
        center_coordinates = (first_topleft_x+w//2, first_topleft_y+h//2)
        radius = 10
        color = (255, 0, 0)
        # Line thickness of 5 px
        thickness = 5
        image = cv2.circle(rgb, center_coordinates, radius, color, thickness)

        #image = cv2.rectangle(image, (first_topleft_x,first_topleft_y), (first_topleft_x+w, first_topleft_y+h), (0,255,0), 1)
        
        detect = cv2.rectangle(rgb, (first_topleft_x,first_topleft_y), 
                               (first_topleft_x+w, first_topleft_y+h), 
                               (0,255,0), 1)
        
        #draw lines through central point
        image = cv2.arrowedLine(detect, (first_topleft_x+w//2, first_topleft_y+h//2), 
                                (w_, first_topleft_y+h//2),
                                (255,255,0), 3)
        
        image = cv2.arrowedLine(detect, (first_topleft_x+w//2, first_topleft_y+h//2), 
                                (0, first_topleft_y+h//2),(255,255,255), 3)
        yellow_line_length = w_-first_topleft_x+w//2
        white_line_length = first_topleft_x+w//2 - 0
        if yellow_line_length < white_line_length:
            direction = 1
            text = "Pepper right sided. Please rotate to the left"
            string = ("Direction:{}(right)".format(direction))
            print(text)
        else:
            text = "Pepper left sided. Please rotate to the right"
            direction = 0
            string = ("Direction:{}(left)".format(direction))
            print(text)
        image = cv2.putText(detect, text, (20,50), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,255,255), 2, cv2.LINE_AA)
        

        cv2.putText(detect,"{}".format(string), (20,90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255))

            
cv2.imwrite("C:/Users/ozangokkan/Desktop/biber/omron/basler_sap3.jpg",cv2.cvtColor(detect, cv2.COLOR_BGR2RGB))
cv2.imshow("image",cv2.cvtColor(detect, cv2.COLOR_BGR2RGB))

