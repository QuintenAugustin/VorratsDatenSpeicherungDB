import http.client
import constants
import time
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
    #Fetches date and time for proper file naming.
    current_datetime = datetime.now().strftime("%y%m%d")
    
    #Jank af but works. Gets current time in seconds, then, adding another hour on top and then converting to proper hours.
    currentHour = time.time()
    futureHour = currentHour + 60*60
    futureHour = time.strftime("%H", time.localtime(futureHour))


    conn.request(f"GET", f"/db-api-marketplace/apis/timetables/v1/plan/{station}/{current_datetime}/{futureHour}", headers=headers)

    res = conn.getresponse()
    data = res.read()
    #converts datetime object to string and defines Filepath
    timetableChangesFilePath = f"rawdata/timetablePlanned/{station}.xml"

    #Writes timetable changes to file
    with open(timetableChangesFilePath, 'w', encoding="utf-8") as f:
        f.write(data.decode("utf-8"))
        f.close()
