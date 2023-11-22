import http.client
import json
from datetime import datetime
import os.path
import constants
import stationList as l
from time import sleep

#Does all the main API work. Easier this way because DB documents how to handle Python.S

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

    #This does not work. I will have to revert to old format and merge xml files manually. Maybe with something like with every iteration through i z increases by 1 thus changing name?
    timetableChangesFilePath = f"rawdata/timetableChanges/{station}.xml"

    #Writes timetable changes to file
    with open(timetableChangesFilePath, 'w', encoding="utf-8") as f:
        f.write(data.decode("utf-8"))
        f.close()
    print(f'Successfully obtained data for {station}') 
print('You have assumed control over all information')    


