import cv2
import numpy as np
import utils
import pytesseract
from pytesseract import Output
from pyzbar import pyzbar
from PIL import Image

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

def recognise_text(roi,tessdata):
    final_text = ""
    roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
    img=roi
    image=roi.copy()
    barcodes=pyzbar.decode(image)

    d=pytesseract.image_to_data(image,output_type=Output.DICT,lang=tessdata)
    bboxes=len(d['level'])
    image[:] = (255,255,255) 
    for i in range(bboxes):
        (x,y,w,h)=(d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        config=int(d['conf'][i])
        text=d['text'][i]
        text=text.replace(" ","")
        text=text.replace("?","")
        text=text.replace("[","")
        text=text.replace(":","")
        text=text.replace("/","")
        text=text.replace(".","")
        text=text.replace("-","")
        text=text.replace("b","h")
        text=text.replace("D","0")
        final_text = final_text + text
        #print(config)

        if config >= 30 and text !="":
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,0,0),1)
#             print(text)
    
    return final_text, img, image

def preprocessing_unit(roi):
    # convert to gray scale
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # emlarge roi
    roi = cv2.resize(roi, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)
    
    roi = cv2.GaussianBlur(roi, (15,15), 0)
    
    #binarise roi
    roi = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    
    kernel = np.ones((5,5),np.uint8)
    roi = cv2.erode(roi,kernel,iterations = 1)
    
    roi = cv2.medianBlur(roi, 13)
    roi = cv2.medianBlur(roi, 13)

    kernel = np.ones((3,3),np.uint8)
    roi = cv2.erode(roi,kernel,iterations = 1)
    
    roi = cv2.medianBlur(roi, 13)
    
    kernel = np.ones((3,3),np.uint8)
    
    return roi
