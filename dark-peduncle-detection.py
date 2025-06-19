# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 14:34:49 2022

@author: ozangokkan
"""



import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

start = time.time()
# Load image
# image = cv2.imread('C:/Users/ozangokkan/Desktop/project studies/biber/omron/koyu4.jpg')
image = cv2.imread('C:/Users/ozangokkan/Desktop/project studies/biber/proje/biberli/b3-frames/test/frame208.jpg')
image = cv2.resize(image, (1000, 1000))

# tuning parameters in case of dark pepper peduncula detection 
hMin, sMin, vMin = 30,60,100
hMax, sMax, vMax = 65, 255, 145

lower = np.array([hMin, sMin, vMin])
upper = np.array([hMax, sMax, vMax])

# Convert to HSV format and color threshold
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower, upper)
result = cv2.bitwise_and(image, image, mask=mask)
result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

kernel = np.ones((4,4),np.uint8)
dilated = cv2.dilate(result, kernel, iterations=3)
contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# contours, hierarchy = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

areas = []
wh = []
w_,h_,d_ = hsv.shape
for ind, contour_ in enumerate(contours):
    areas.append(cv2.contourArea(contour_)) 


    if cv2.contourArea(contour_) >= 1500 and cv2.contourArea(contour_) < 6000:
        first_topleft_x,first_topleft_y, w, h = cv2.boundingRect(contour_)
        # print("coord.=",first_topleft_x)
        
        if w/h > 1.0 and w/h < 4.0 and first_topleft_y < 100:
            wh.append([w,h,w/h])

            dilated = cv2.rectangle(dilated, (first_topleft_x,first_topleft_y), 
                               (first_topleft_x+w, first_topleft_y+h), 
                               (255,255,0), 2)
            detect = dilated
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
                print(direction)
                print(first_topleft_x,first_topleft_y)

                image = cv2.putText(detect, text, (first_topleft_x,first_topleft_y), cv2.FONT_HERSHEY_SIMPLEX, 
                           1, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(detect,"{}".format(string), (30,90), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))
            elif yellow_line_length > white_line_length:
                text = "Pepper left sided. Please rotate to the right"
                direction = 0
                string = ("Direction:{}(left)".format(direction))
                print(text)
                print(direction)
                print(first_topleft_x,first_topleft_y)

                image = cv2.putText(detect, text, (50,first_topleft_y), cv2.FONT_HERSHEY_SIMPLEX, 
                           1, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(detect,"{}".format(string), (30,90), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255))

print("execution time:",(time.time()-start))
cv2.imshow("ert", image)

