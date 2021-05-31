import cv2
import numpy as np

def preprocessing(roi):
    # convert to gray scale
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # emlarge roi
    roi = cv2.resize(roi, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    
    roi = cv2.GaussianBlur(roi, (15,15), 0)
    
    #binarise roi
    roi = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    
    kernel = np.ones((5,5),np.uint8)
    roi = cv2.erode(roi,kernel,iterations = 1)
    
    roi = cv2.medianBlur(roi, 15)
    roi = cv2.medianBlur(roi, 15)

    kernel = np.ones((3,3),np.uint8)
    roi = cv2.erode(roi,kernel,iterations = 1)
    
    roi = cv2.medianBlur(roi, 13)
    
    return roi
    