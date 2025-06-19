# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 20:06:38 2021

@author: ozangokkan
"""


from pypylon import pylon
import cv2
import numpy as np
import datetime
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
#Relay Trigger
#Set numbers on board
GPIO.setmode(GPIO.BCM)
def relay_on(pin):
    GPIO.output(pin, GPIO.HIGH)

def relay_off(pin):
    GPIO.output(pin, GPIO.LOW)


def pepper_peduncle_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rgb = image.copy()
    w_,h_,d_ = rgb.shape
    direction = -1
    kernel = np.ones((12,12),np.uint8)
    dilated = cv2.dilate(gray, kernel, iterations=3)
    #cv2.imshow("dilate", dilated)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    areas = []
    yellow_line_length = 0
    white_line_length = 0
    for ind, contour_ in enumerate(contours):
            areas.append(cv2.contourArea(contour_)) 
    for ind, contour_ in enumerate(contours):
        
        max_area = max(areas)
        if cv2.contourArea(contour_) >= max_area and cv2.contourArea(contour_) > 1000:
            first_topleft_x,first_topleft_y, w, h = cv2.boundingRect(contour_)
            # if first_topleft_y < 100:
            center_coordinates = (first_topleft_x+w//2, first_topleft_y+h//2)
            radius = 10
            color = (0, 0, 255)
            # Line thickness of 5 px
            thickness = 5
            image = cv2.circle(rgb, center_coordinates, radius, color, thickness)

            #image = cv2.rectangle(image, (first_topleft_x,first_topleft_y), (first_topleft_x+w, first_topleft_y+h), (0,255,0), 1)
            
            detect = cv2.rectangle(image, (first_topleft_x,first_topleft_y), 
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
                
                image = cv2.putText(detect, text, (30,50), cv2.FONT_HERSHEY_SIMPLEX, 
                           1, (0,255,255), 2, cv2.LINE_AA)
                cv2.putText(detect,"{}".format(string), (30,90), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255))
            elif yellow_line_length > white_line_length:
                text = "Pepper left sided. Please rotate to the right"
                direction = 0
                string = ("Direction:{}(left)".format(direction))
                print(text)
                
                image = cv2.putText(detect, text, (30,50), cv2.FONT_HERSHEY_SIMPLEX, 
                           1, (0,255,255), 2, cv2.LINE_AA)
                cv2.putText(detect,"{}".format(string), (30,90), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255))
            else:
                #direction = -1
                pass
        else:
            image = rgb
            pass
            
    return image, direction



def dark_peduncle_detection(image):
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
    
            if w/h < 4.0 and w/h > 1.0 and first_topleft_y < 100:
    
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
                    
                    image = cv2.putText(detect, text, (first_topleft_x,first_topleft_y), cv2.FONT_HERSHEY_SIMPLEX, 
                               1, (255,255,255), 2, cv2.LINE_AA)
                    cv2.putText(detect,"{}".format(string), (30,90), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255))
                elif yellow_line_length > white_line_length:
                    text = "Pepper left sided. Please rotate to the right"
                    direction = 0
                    string = ("Direction:{}(left)".format(direction))
                    print(text)
                    
                    image = cv2.putText(detect, text, (50,first_topleft_y), cv2.FONT_HERSHEY_SIMPLEX, 
                               1, (255,255,255), 2, cv2.LINE_AA)
                    cv2.putText(detect,"{}".format(string), (30,90), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255))
    return image, direction




log_count = 1
# Make Configurations
path     = "/home/pi/Desktop/biber/config.txt"
log_path = "/home/pi/Desktop/biber/log.txt"


with open(path, "r") as config:
    result = config.readlines()
hMin, sMin, vMin = result[0][5:-1], result[1][5:-1], result[2][5:-1]
hMax, sMax, vMax = result[3][5:-1], result[4][5:-1], result[5][5:]

# pin number assingment on raspberry board
pin_no = int(result[6][9:]) # pin assing for left trigger
GPIO.setup(pin_no, GPIO.OUT) # GPIO Assign mode

right_pin_no = int(result[7][10:]) # pin assing for right trigger
GPIO.setup(right_pin_no, GPIO.OUT)

#trigger timer 
timer_left = float(result[8][16:])
timer_right = float(result[9][17:])
# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()
# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned


while True:
    try:
        while camera.IsGrabbing():
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                # Access the image data
                image = converter.Convert(grabResult)
                img = image.GetArray()
                img = cv2.resize(img, (1000, 1000))
                img2 = img.copy()
                # Set minimum and maximum HSV values to display
                lower = np.array([int(hMin), int(sMin), int(vMin)])
                upper = np.array([int(hMax), int(sMax), int(vMax)])
                #lower = np.array([30, 100, 90])
                #upper = np.array([50, 255, 255])
                
                # Convert to HSV format and color threshold
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, lower, upper)
                img = cv2.bitwise_and(img, img, mask=mask)
                result, direction = pepper_peduncle_detection(img)
                # if direction == -1:
                    # result, direction = dark_peduncle_detection(img2)
                    
                if result.any():
                    if direction == 0:
                        try:
                            GPIO.output(pin_no, 0)
                            print("relay on")
                            time.sleep(timer_left)
                            GPIO.output(pin_no, 1)
                            print("relay off")
                            time.sleep(timer_left)
                        finally:
                            pass
#                             GPIO.cleanup()
                    elif direction == 1:
                        try:
                            GPIO.output(right_pin_no, 0)
                            print("relay on")
                            time.sleep(timer_right)
                            GPIO.output(right_pin_no, 1)
                            print("relay off")
                            time.sleep(timer_right)
                        finally:
                            pass
                    else:
                        GPIO.output(right_pin_no, 0)
                        GPIO.output(right_pin_no, 1)
                        pass
                else:
                    pass
                cv2.namedWindow('pepper', cv2.WINDOW_NORMAL)
                cv2.imshow('pepper', result)
                k = cv2.waitKey(1)
                if k == ord('q'):
                    break
                
            grabResult.Release()
        
        # Releasing the resource    
        camera.StopGrabbing()
        camera.Close()
        cv2.destroyAllWindows()

    except Exception as e:
                with open("/home/pi/Desktop/biber/log.txt", "a") as log:
                    log.write("%s\nError Info : %s\nError capturing Time : %s\n" % (log_count, e, datetime.datetime.now()))
                    log.write("----------------------****************************-------------------\n")
                    log_count += 1
                pass
