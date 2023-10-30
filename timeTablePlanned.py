import http.client
import constants
from datetime import datetime

conn = http.client.HTTPSConnection("apis.deutschebahn.com")

headers = {
    'DB-Client-Id':  constants.API_CLIENT_ID,
    'DB-Api-Key': constants.API_KEY,
    'accept': "application/xml"
    }

conn.request("GET", "/db-api-marketplace/apis/timetables/v1/plan/8000028/231030/20", headers=headers)

res = conn.getresponse()
data = res.read()

#Fetches date and time for proper file naming.
current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")

#converts datetime object to string and defines Filepath
str_current_datetime = str(current_datetime)
file_name = str_current_datetime+".xml"
timetableChangesFilePath = "rawdata/timetablePlanned/"+ file_name

#Writes timetable changes to file
with open(timetableChangesFilePath, 'w') as f:
    f.write(data.decode("utf-8"))
    f.close()
