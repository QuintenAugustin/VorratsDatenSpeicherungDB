import http.client
import constants
import time
from datetime import datetime, timedelta
import stationList as l
from time import sleep

#Does all the main API work. Easier this way because DB documents how to handle Python.
#The reason this is all so overbuilt is because the timetable planned and timetable changes information aren't persistently stored by
#DeutscheBahn. Thus I can't just go ahead and download all the data for 2022 (then Id have been done with this project after a week.)
#Instead they only keep the data for a few hours. Thus every 30inutes I request planned timetable information from DB and store them..... way down the track.
#You will get there eventually.


for i in l.relevantStations:
    station = i
    #Delay to ensure all api calls are accepted
    sleep(0.9)
    #The actual connector is provided by DB, everything else is mine.
    conn = http.client.HTTPSConnection("apis.deutschebahn.com")
    headers = {
        'DB-Client-Id':  constants.API_CLIENT_ID,
        'DB-Api-Key': constants.API_KEY,
        'accept': "application/xml"
        }

    
    #Jank af but works. Gets current time in seconds, then, adding another hour on top and then converting to proper hours.
    currentHour = time.time()
    futureHour = currentHour + 60*60
    futureHour = time.strftime("%H", time.localtime(futureHour))
    #Fetches date and time for proper file naming.
    current_datetime = datetime.now().strftime("%y%m%d")
    #Not having this originally cost me a couple of hours. DB is very agressive when it comes to deleting.
    if futureHour == "00": 
        today = datetime.now()
        delta = timedelta(days=1)
        tomorrow = today + delta
        current_datetime = tomorrow.strftime("%y%m%d")



    conn.request(f"GET", f"/db-api-marketplace/apis/timetables/v1/plan/{station}/{current_datetime}/{futureHour}", headers=headers)

    res = conn.getresponse()
    data = res.read()
    #converts datetime object to string and defines Filepath
    timetableChangesFilePath = f"rawdata/timetablePlanned/{station}.xml"

    #Writes timetable changes to file
    with open(timetableChangesFilePath, 'w', encoding="utf-8") as f:
        f.write(data.decode("utf-8"))
        f.close()
