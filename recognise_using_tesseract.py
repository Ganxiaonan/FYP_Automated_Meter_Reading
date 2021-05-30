import pytesseract
from pytesseract import Output
import cv2
import numpy as np
from pyzbar import pyzbar
from PIL import Image

img=cv2.imread("./images/1.jpeg")
image=img.copy()
barcodes=pyzbar.decode(image)
#print(pytesseract.image_to_string("data//test2.png"))
#print('========================')
#print(pytesseract.image_to_data("data//test2.png"))

d=pytesseract.image_to_data("./images/1.jpeg",output_type=Output.DICT,lang='ssd_alphanum_plus')
bboxes=len(d['level'])
image[:] = (255,255,255) 
for i in range(bboxes):
    (x,y,w,h)=(d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    config=int(d['conf'][i])
    text=d['text'][i]
    text=text.replace(" ","")
    text=text.replace("?","")
    text=text.replace("[","")
    #print(config)

    if config >= 30 and text !="":
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,0,0),1)
        print(text)
'''
for barcode in barcodes:
    (x,y,w,h)=barcode.rect
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

    barcodeData=barcode.data.decode("utf-8")
    barcodeType=barcode.type

    word="{} ({})".format(barcodeData,barcodeType)
    cv2.putText(img,word,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)

    print("[INFO] Found {} barcode: {}".format(barcodeType,barcodeData))
    
#cv2.imshow('white',image)
#cv2.imshow('img',img)
combine = np.hstack((image, img))
'''
cv2.imshow('original',img)
cv2.imshow('detect',image)
cv2.waitKey(0)


