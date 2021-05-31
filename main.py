import cv2
import numpy as np
import utils

# define region of ROI (exclude unit)
(x_min,y_min) = (120,200)
(x_max,y_max) = (440,290)

cap= cv2.VideoCapture("output2.mp4")

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")


while (cap.isOpened()):
    ret,frame= cap.read()
    
    # crop image, only process roi
    roi = frame[y_min:y_max,x_min:x_max]
    
    roi = utils.preprocessing(roi)

    if ret == True:
#         cv2.imshow('frame', frame)
        cv2.imshow('roi', roi)

    if cv2.waitKey(15) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()