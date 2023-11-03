import http.client
import json
from datetime import datetime
import os.path
import constants

#Does all the main API work. Easier this way because DB documents how to handle Python.S

conn = http.client.HTTPSConnection("apis.deutschebahn.com")

#No looking at my keys. That'd be an amateur mistake
headers = {
    'DB-Client-Id': constants.API_CLIENT_ID ,
    'DB-Api-Key': constants.API_KEY,
    'accept': "application/json"
    }

#fetches info for specific train station
#turn this into a loop going forward iterating through an array of eva numbers Quinten. That'd be smart would it not?
conn.request("GET", "/db-api-marketplace/apis/timetables/v1/rchg/8000105", headers=headers)


res = conn.getresponse()
data = res.read()

#Fetches date and time for proper file naming.
current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")

#converts datetime object to string and defines Filepath
str_current_datetime = str(current_datetime)
file_name = str_current_datetime+".xml"
timetableChangesFilePath = "rawdata/timetableChanges/"+ file_name

#Writes timetable changes to file
with open(timetableChangesFilePath, 'w') as f:
    f.write(data.decode("utf-8"))
    f.close()


