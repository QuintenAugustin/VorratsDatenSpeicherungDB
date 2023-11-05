import http.client
import constants
from datetime import datetime
import stationList as l
from time import sleep

#Does all the main API work. Easier this way because DB documents how to handle Python.S

for i in l.relevantStations:
    station = i
    #Delay to ensure all api calls are accepted
    sleep(0.2)

conn = http.client.HTTPSConnection("apis.deutschebahn.com")

headers = {
    'DB-Client-Id':  constants.API_CLIENT_ID,
    'DB-Api-Key': constants.API_KEY,
    'accept': "application/xml"
    }

conn.request(f"GET", f"/db-api-marketplace/apis/timetables/v1/plan/{station}/231030/20", headers=headers)

res = conn.getresponse()
data = res.read()

#Fetches date and time for proper file naming.
current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")

#converts datetime object to string and defines Filepath
str_current_datetime = str(current_datetime)
file_name = str_current_datetime+".xml"
timetableChangesFilePath = "rawdata/timetablePlanned/"+ file_name

#Writes timetable changes to file
with open(timetableChangesFilePath, 'w', encoding="utf-8") as f:
    f.write(data.decode("utf-8"))
    f.close()
