import http.client
from datetime import datetime
import constants
import stationList as l
from time import sleep

#Does all the main API work. Easier this way because DB documents how to handle Python.
#The reason this is all so overbuilt is because the timetable planned and timetable changes information aren't persistently stored by
#DeutscheBahn. Thus I can't just go ahead and download all the data for 2022 (then Id have been done with this project after a week.)
#Instead they only keep the data for a few hours. Thus every 10minutes I request change information from DB and store them..... way down the track.
#You will get there eventually.

for i in l.relevantStations:
    station = i
    #Delay to ensure all api calls are accepted
    sleep(0.4)

    conn = http.client.HTTPSConnection("apis.deutschebahn.com")
    #No looking at my keys. That'd be an amateur mistake
    headers = {
        'DB-Client-Id': constants.API_CLIENT_ID ,
        'DB-Api-Key': constants.API_KEY,
        'accept': "application/json"
        }

    #fetches info for specific train station
    #turn this into a loop going forward iterating through an array of eva numbers Quinten. That'd be smart would it not? Done
    conn.request(f"GET", f"/db-api-marketplace/apis/timetables/v1/fchg/{station}", headers=headers)


    res = conn.getresponse()
    data = res.read()
    
    #Defines the filepath to store data based on the current station in the loop.
    timetableChangesFilePath = f"rawdata/timetableChanges/{station}.xml"

    #Writes timetable changes to file
    with open(timetableChangesFilePath, 'w', encoding="utf-8") as f:
        f.write(data.decode("utf-8"))
        f.close()
    print(f'Successfully obtained data for {station}') 
print('You have assumed control over all information')    


