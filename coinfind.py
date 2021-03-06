#!/usr/bin/python

import cv2
import numpy as np
import sys
from time import sleep
from matplotlib import pyplot

# device /dev/video1
device = 0

def getCapture(device):
    video_capture = cv2.VideoCapture(device)
    return video_capture

def processImage(img):
    # blur to reduce noise
    img = cv2.GaussianBlur(img,(1,1),0)

    # canny edge detection on img
    canny_img = cv2.Canny(img,100,170)

    return canny_img

def boundingCircle(canny_img):
    # morph
    kernel = np.ones((3, 3), np.uint8)
    close_circle = cv2.morphologyEx(canny_img,cv2.MORPH_CLOSE,kernel, iterations=5)

    # fill bounds
    bounding_img = close_circle.copy()

    image, bounding_circles, hierarchy = cv2.findContours(bounding_img, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE)

    return bounding_circles, image


def detectCoins(bounding_circles, display_img):
    
    count = 0
    for circle in bounding_circles:
        area = cv2.contourArea(circle)

        if 10000 < area and area < 40000:
            count += 1
 
        ellipse = cv2.fitEllipse(circle)
        cv2.ellipse(display_img, ellipse, (0,0,255),3)

    print("# of coins: " + str(count))

def display(frame):
    cv2.imshow('camera', frame)

def main():    
    camera_feed = getCapture(device)

    while 1:
        ret, frame = camera_feed.read()
        canny_img = processImage(frame)
        bounding_circles, colored_img = boundingCircle(canny_img)
        detectCoins(bounding_circles, frame)
        if ret == True:
            display(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    video_capture.release()
    cv2.destroyAllWindows()

main() 
