import cv2
import utils

#Import the stuff we need
#pip install influxdb 
from influxdb import InfluxDBClient
from datetime import datetime
import pytz

#Setup database
client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'electric_meter6')
client.create_database('electric_meter6')  #This line not used as only one database needed
print(client.get_list_database())
# client.switch_database('electric_2nd_meter')    #This line not used as only one database needed

#Setup Payload
json_payload = []

# define region of interest (exclude unit)
(x_min,y_min) = (120,210)
(x_max,y_max) = (440,280)

# define region of interest of unit
(unit_x_min,unit_y_min) = (434,220)
(unit_x_max,unit_y_max) = (540,270)

i = 0

cap= cv2.VideoCapture("output2.mp4")

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")


while (cap.isOpened()):
    ret,frame= cap.read()
    
    i = i+1
    
    if (i % 100 == 0):
        
        # crop image, only process roi
        roi = frame[y_min:y_max,x_min:x_max]
        unit_roi = frame[unit_y_min:unit_y_max,unit_x_min:unit_x_max]

        unit_roi=  utils.preprocessing_unit(unit_roi)
        unit_text,unit_roi,unit_detection = utils.recognise_text(unit_roi,'eng1')
        
        try:
        
            if unit_text == 'kvarh' or unit_text == 'kVarh':
                
                roi = utils.preprocessing(roi)
                text,roi,detection = utils.recognise_text(roi,'ssd_alphanum_plus')
                text = int(text)
                
                if text > 88888888:  #ignore if reading more than possible maximum reading(88888888)
                    i = i-1
                    continue
                
                if text > 10000:
                    text = text[4:7]
                    
                print("meter reading = ",text,unit_text)
                
                data = {
                    "measurement": "electric_consumption",
                    "tags": {
                        "unit": 'kVarh'
                    },
                    "time": datetime.now(pytz.timezone('Asia/Singapore')),
                    "fields": {
                        'value': float(text),
                    }
                }
                json_payload.append(data)
             
                #Send our payload
                client.write_points(json_payload)
                
            if unit_text == 'kWh' or unit_text == 'kwh':
                
                roi = utils.preprocessing(roi)
                text,roi,detection = utils.recognise_text(roi,'ssd_alphanum_plus')
                text = int(text)
                
                if text > 88888888:  #ignore if reading more than possible maximum reading(88888888)
                    i = i-1
                    continue
                
                if text > 100000:    
                    text = text[3:7]
                    
                print("meter reading = ",text,unit_text)
                
                data = {
                    "measurement": "electric_consumption",
                    "tags": {
                        "unit": 'kWh'
                    },
                    "time": datetime.now(pytz.timezone('Asia/Singapore')),
                    "fields": {
                        'value': float(text),
                    }
                }
                json_payload.append(data)
             
                #Send our payload
                client.write_points(json_payload)
                
        except:
            i = i-1
            continue
    
        if ret == True:
            cv2.imshow('frame', frame)
            cv2.imshow('roi', roi)
            cv2.imshow('unit_roi', unit_roi)
   
    
    if i > 10000:
        i = 0

    if cv2.waitKey(1) & 0xFF == 27:  #Press Esc to quit program
        break
    

cap.release()
cv2.destroyAllWindows()