#Import the stuff we need   #influx -precision rfc3339  : to open influx with readable date and time
#pip install influxdb 
from influxdb import InfluxDBClient
from datetime import datetime


#Setup database
client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'electric_meter')
# client.create_database('electric_meter')  #This line not used as only one database needed
print(client.get_list_database())
# client.switch_database('electric_2nd_meter')    #This line not used as only one database needed


#Setup Payload
json_payload = []
data = {
    "measurement": "electric_consumption",
    "tags": {
        "unit": "kWh" 
        },
    "time": datetime.now(),
    "fields": {
        'value': 3.0,
    }
}
json_payload.append(data)
print(json_payload)


#Send our payload
client.write_points(json_payload)