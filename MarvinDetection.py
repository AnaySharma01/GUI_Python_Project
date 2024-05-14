#imports packages
import time
import cv2
import numpy as np

def alien_detected():
    detected = False
    # Read the alien template
    template = cv2.imread('img.png', 0)

    # Perform match operations.
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    # Specify a threshold
    threshold = 0.25

    # https://www.geeksforgeeks.org/template-matching-using-opencv-in-python/
    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)

    # Draw a rectangle around the matched region
    for point in zip(*loc[::-1]):
        actual_point = point

    if actual_point in zip(*loc[::-1]):
        detected = True
        print("the mission is complete")

