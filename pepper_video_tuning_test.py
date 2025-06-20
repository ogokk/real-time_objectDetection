# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 13:06:20 2021

@author: ozangokkan
"""





import cv2
import numpy as np

def callback(x):
    pass

#cap = cv2.VideoCapture('C:/Users/ozangokkan/Desktop/biber/omron/biber renk algılama operasyonu.mp4')
# cap = cv2.VideoCapture("C:/Users/ozangokkan/Desktop/project studies/biber/bibersiz/new-b2.avi")
cap = cv2.VideoCapture("C:/Users/ozangokkan/Desktop/project studies/biber/biberli/new-b3.avi")
#cap = cv2.VideoCapture(0)

cv2.namedWindow('image')

ilowH = 0
ihighH = 179

ilowS = 0
ihighS = 255
ilowV = 0
ihighV = 255

# create trackbars for color change
cv2.createTrackbar('lowH','image',ilowH,179,callback)
cv2.createTrackbar('highH','image',ihighH,179,callback)

cv2.createTrackbar('lowS','image',ilowS,255,callback)
cv2.createTrackbar('highS','image',ihighS,255,callback)

cv2.createTrackbar('lowV','image',ilowV,255,callback)
cv2.createTrackbar('highV','image',ihighV,255,callback)



while True:
    # grab the frame
    ret, frame = cap.read()

    # get trackbar positions
    ilowH = cv2.getTrackbarPos('lowH', 'image')
    ihighH = cv2.getTrackbarPos('highH', 'image')
    ilowS = cv2.getTrackbarPos('lowS', 'image')
    ihighS = cv2.getTrackbarPos('highS', 'image')
    ilowV = cv2.getTrackbarPos('lowV', 'image')
    ihighV = cv2.getTrackbarPos('highV', 'image')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([ilowH, ilowS, ilowV])
    higher_hsv = np.array([ihighH, ihighS, ihighV])
    mask = cv2.inRange(hsv, lower_hsv, higher_hsv)

    frame = cv2.bitwise_and(frame, frame, mask=mask)

    # show thresholded image
    cv2.imshow('image', frame)
    k = cv2.waitKey(200) & 0xFF # large wait time to remove freezing
    if k == 113 or k == 27:
        break


cv2.destroyAllWindows()
cap.release()