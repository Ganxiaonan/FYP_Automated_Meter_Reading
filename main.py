import cv2
import utils

#Import the stuff we need
#pip install influxdb 
from influxdb import InfluxDBClient
from datetime import datetime

#Setup database
client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'electric_meter6')
client.create_database('electric_meter6')  #This line not used as only one database needed
print(client.get_list_database())
# client.switch_database('electric_2nd_meter')    #This line not used as only one database needed

#Setup Payload
json_payload = []

# define region of interest (exclude unit)
(x_min,y_min) = (120,200)
(x_max,y_max) = (440,290)

# define region of interest of unit
(unit_x_min,unit_y_min) = (434,238)
(unit_x_max,unit_y_max) = (539,286)

cap= cv2.VideoCapture("output2.mp4")

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")


while (cap.isOpened()):
    ret,frame= cap.read()
    
    # crop image, only process roi
    roi = frame[y_min:y_max,x_min:x_max]
    
    roi = utils.preprocessing(roi)
    
    text,roi,detection = utils.recognise_text(roi)
    
    try:
        text = int(text)
    except:
        continue
    
    print("meter reading = ",int(text))
    
    if int(text)>88888888:  #ignore if reading more than possible maximum reading(88888888)
        continue

    if ret == True:
        cv2.imshow('frame', frame)
        cv2.imshow('roi', roi)
        cv2.imshow('detection', detection)
    try:
        data = {
            "measurement": "electric_consumption",
            "tags": {
                "unit": 'kWh'
                },
            "time": datetime.now(),
            "fields": {
                'value': float(text),
            }
        }
        json_payload.append(data)
        
        #Send our payload
        client.write_points(json_payload)
            
    except:
        pass

    if cv2.waitKey(1) & 0xFF == 27:  #Press Esc to quit program
        break

cap.release()
cv2.destroyAllWindows()