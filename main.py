import http.client
import json
from datetime import datetime
import os.path
import constants

conn = http.client.HTTPSConnection("apis.deutschebahn.com")

headers = {
    'DB-Client-Id': constants.API_CLIENT_ID ,
    'DB-Api-Key': constants.API_KEY,
    'accept': "application/xml"
    }

conn.request("GET", "/db-api-marketplace/apis/timetables/v1/fchg/8000105", headers=headers)


res = conn.getresponse()
data = res.read()


current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")

#converts datetime object to string
str_current_datetime = str(current_datetime)
file_name = str_current_datetime+".xml"



textFilePath = "rawdata/"+ file_name

with open(textFilePath, 'w') as f:
    f.write(data.decode("utf-8"))
    f.close()



#file = open(completeName,'w')
#print(completeName)
#file.write(data.decode("utf-8"))
#print("File created: ", file.name)
#file.close()