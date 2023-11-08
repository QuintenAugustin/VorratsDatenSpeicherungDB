import pandas as pd
import lxml.etree
import pandas_read_xml as pdx
import os
import xml.etree.ElementTree as ET
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 1)


#df_out = pd.read_xml(xml, parser="lxml")

#print(df_out)

#df_parsed = pd.read_xml(
#    xml,
#    xpath="//timetable/s/* ",
#    parser="lxml",
#)
#df_address_stack = pd.read_xml(xml,xpath='//employee_name/email/id[contains(@name,"stack")]//address')
#columns = ["id", "eva", "m", "ar", "test", "cp", "l"]
#df_out = pd.DataFrame(
#    data=df_parsed.values.reshape(-1, len(columns)),
#    columns=columns,
    
#)
#df_out = df_out.drop(columns=["m", "ar", "test"])

##Fetches date and time for proper file naming.
#    current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
#
#    #converts datetime object to string and defines Filepath
#    str_current_datetime = str(current_datetime)
#    file_name = str_current_datetime+".xml"
#    timetableChangesFilePath = "rawdata/timetableChanges/"+ file_name

#This is bad but its the easiest way to deal with the various xml files. 
data1 = ET.tostring(ET.parse('rawdata/timetableChanges/8000028.xml').getroot()).decode("utf-8")
data2 = ET.tostring(ET.parse('rawdata/timetableChanges/8000105.xml').getroot()).decode("utf-8")
f = open("preprocessedData/timetableChanges/Output.xml", "a+")
#This is here so that element tree parser doesnt complain about junk, gotta have proper xml structure sadly
f.write("<new_root>")
f.write(data1)
f.write(data2)
f.write("</new_root>")
f.close()
print('XMLs unioned, starting dataframe construction')

#The unioned XML is completely flattened by this godsend of a package. Arriving at these two lines took 20hours.
#There is a reason why this bloody file used to be called textformatter9.py in past commits......
df = pdx.read_xml("preprocessedData/timetableChanges/Output.xml", [ 'new_root','timetable'], root_is_rows=False)
df = pdx.fully_flatten(df)
print('Base dataframe constructed')   
#Renaming the automatically generated columns that represent file path to make them nice to read and sanity check.
df.rename(columns={'@station' : 'station',
                   's|@eva':'EvaNumberTrainTrip', 
                   's|@id':'uniqueTrainTripId',
                   's|ar|@clt':'ArrivalCancellationTime',
                   's|ar|@cp':'ArrivalChangePlatform', 
                   's|ar|@cs':'ArrivalCancellationStatus',
                   's|ar|@cpth':'ArrivalChangePath', 
                   's|ar|@ct':'ArrivalChangeTime',
                   's|ar|@dc':'ArrivalDistantChange', #Tf does this mean?
                   's|ar|@l':'ArrivalLine',
                   's|ar|@pp':'ArrivalPlannedPlatform',
                   's|ar|@ppth':'ArrivalPlannedPlatform',
                   's|ar|@ps':'ArrivalPlannedStatus', #This is also used if a cancellation has been revoked!
                   's|ar|@pt':'ArrivalPlannedTime', #Probably won't use this one to avoid data doubling
                   's|ar|@tra':'ArrivalTransition', #Train changes ID from one to another due to operating a different trip now. Annoying but makes sense.
                   's|dp|@clt':'DepartureCancellationTime',
                   's|dp|@cp':'DepartureChangePlatform',
                   's|dp|@cpth':'DepartureChangePath',
                   's|dp|@cs':'DepartureCancellationStatus',
                   's|dp|@ct':'DepartureChangeTime',
                   's|dp|@l':'DepartureLine',
                   's|dp|@pp':'DeparturePlannedPlatform',
                   's|dp|@ppth':'DeparturePlannedPath',
                   's|dp|@ps':'DeparturePlannedStatus', #Same as with the last planned status.
                   's|dp|@pt':'DeparturePlannedTime',
                   's|dp|@tra':'DepartureTransition',          
                   },inplace=True)
print('Base dataframe formatted')

#Splitting the base dataframe up into several parts for being inserted into a relational database later on.
#Might as well do it here and not tax the database with continuous junk later on. Also saves massively on local storage doing it this way.
#To put things into perspective, the base dataframe saved into excel for just Frankfurt and Bayreuth was 12k rows. This is 3k.


DFChangedArrivals=df[['EvaNumberTrainTrip','uniqueTrainTripId','ArrivalCancellationStatus','ArrivalCancellationTime','ArrivalDistantChange','ArrivalChangePlatform','ArrivalChangePath','ArrivalChangeTime','ArrivalLine']]
DFChangedArrivals=DFChangedArrivals.drop_duplicates()
print('Arrival dataframe extracted')

DFChangedDepartures=df[['EvaNumberTrainTrip','uniqueTrainTripId','DepartureCancellationStatus','DepartureCancellationTime','DeparturePlannedStatus','DepartureChangePlatform','DepartureChangePath','DepartureChangeTime','DepartureLine']]
DFChangedDepartures=DFChangedDepartures.drop_duplicates()
print('Departures dataframe extracted')

#These are only here if you want to observe what output data might look like. Mostly for sanity checking.
#df.to_excel('output4.xlsx', index=False)
DFChangedArrivals.to_excel('arrivalData.xlsx', index=False)
DFChangedDepartures.to_excel('departureData.xlsx', index=False)

