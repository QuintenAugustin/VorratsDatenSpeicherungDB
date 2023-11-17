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
data1 = ET.tostring(ET.parse('rawdata/timetablePlanned/8000028.xml').getroot()).decode("utf-8")
data2 = ET.tostring(ET.parse('rawdata/timetablePlanned/8000105.xml').getroot()).decode("utf-8")
f = open("preprocessedData/timetablePlanned/Output.xml", "a+")
#This is here so that element tree parser doesnt complain about junk, gotta have proper xml structure sadly
f.write("<new_root>")
f.write(data1)
f.write(data2)
f.write("</new_root>")
f.close()
print('XMLs unioned, starting dataframe construction')

#The unioned XML is completely flattened by this godsend of a package.
df = pdx.read_xml("preprocessedData/timetablePlanned/Output.xml", [ 'new_root','timetable'], root_is_rows=False)
df = pdx.fully_flatten(df)
print('Base dataframe for planned timetables constructed')


#Renaming the automatically generated columns that represent file path to make them nice to read and sanity check.
df.rename(columns={'@station' : 'station',
                   's|@id':'uniqueTrainTripId',
                   's|ar|@l':'arrivalPlannedLine',
                   's|ar|@pp':'arrivalPlannedPlatform',
                   's|ar|@ppth':'arrivalPlannedPath',
                   's|ar|@ps':'arrivalPlannedStatus', #Not sure why this is here. Going to have to do some snooping.
                   's|ar|@pt':'arrivalPlannedTime', #Probably won't use this one to avoid data doubling
                   's|ar|@tra':'arrivalPlannedTransition', #Train changes ID from one to another due to operating a different trip now. Annoying but makes sense.
                   's|dp|@l':'departurePlannedLine',
                   's|dp|@pp':'departurePlannedPlatform',
                   's|dp|@ppth':'DeparturePlannedPath',
                   's|dp|@ps':'DeparturePlannedStatus', #Same as with the last planned status.
                   's|dp|@pt':'departurePlannedTime',
                   's|dp|@tra':'departurePlannedTransition',
                   's|tl|@c':'TrainCategory',       
                   's|tl|@n':'TrainNumber',
                   },inplace=True)
print('Base dataframe formatted, commencing extraction') 
#df.to_excel('plannedTimeTables2.xlsx', index=False)
#print(df)
#Not sure if splitting it up makes sense. We will have to find out.
#Splitting the base dataframe up into several parts for being inserted into a relational database later on.
#DFStations=df[['EvaNumber', 'station']]
#dropping duplicates in second step because otherwise it puts other columns in too.
#DFStations=DFStations.drop_duplicates()
#print('Station dataframe extracted')

DFPlannedArrivals=df[['station','uniqueTrainTripId','arrivalPlannedLine','arrivalPlannedPlatform','arrivalPlannedTime','arrivalPlannedTransition']]

#dropping duplicates in second step because otherwise it puts other columns in too.
DFPlannedArrivals=DFPlannedArrivals.drop_duplicates()

#These unique IDs serve as an identifier of THIS specific train trip at THIS specific station. API only provides unique identifiers for station
#and train trip. By combining these two i can actually properly map stuff and properly call stuff. A unique trip ID shouldn't appear at the same station
#twice unless DB suddenly started playing with the reverse (which would be surprising since their drivers are too busy striking to even consider the reverse.)
#It will however appear at all stations for that train trip. Thus while unlikely to occur with my sample size, for the sake of clean data anything but this is unacceptable.
#Doing it after dropping duplicates because performance. I may delete station and train trip id fields later on as this information now is repeated a lot. Not sure yet as I am not sure how the rest of this will go.
DFPlannedArrivals['uniqueId'] = DFPlannedArrivals['station'].astype(str) + DFPlannedArrivals['uniqueTrainTripId'].astype(str)
print('Arrivals dataframe extracted')

DFPlannedDepartures=df[['station','uniqueTrainTripId','departurePlannedLine', 'departurePlannedPlatform', 'departurePlannedTime', 'departurePlannedTransition']]
DFPlannedDepartures=DFPlannedDepartures.drop_duplicates()
DFPlannedDepartures['uniqueId'] = DFPlannedDepartures['station'].astype(str) + DFPlannedDepartures['uniqueTrainTripId'].astype(str)
print('Departures dataframe extracted')

DFTrainInformation=df[['station','uniqueTrainTripId','TrainCategory','TrainNumber']]
DFTrainInformation=DFTrainInformation.drop_duplicates()
DFTrainInformation['uniqueId'] = DFTrainInformation['station'].astype(str) + DFTrainInformation['uniqueTrainTripId'].astype(str)
print('Train information dataframe extracted')

DFPlannedTrainsMapping=df[['station','uniqueTrainTripId']]
DFPlannedTrainsMapping=DFPlannedTrainsMapping.drop_duplicates()
DFPlannedTrainsMapping['uniqueId'] = DFPlannedTrainsMapping['station'].astype(str) + DFPlannedTrainsMapping['uniqueTrainTripId'].astype(str)
print('Train-Station mapping extracted')
print('Great deeds have been done on this fine day. The data is ready for further assimilation. Even this horrible data quality bows before you. All hail pandas read xml.')


#df.to_excel('plannedBaseFrame.xlsx',index=False)
DFPlannedArrivals.to_excel('plannedArrivals.xlsx',index=False)
DFPlannedDepartures.to_excel('plannedDepartures.xlsx', index=False)
#DFTrainInformation.to_excel('plannedTrainInformation.xlsx',index=False)
#DFPlannedTrainsMapping.to_excel('plannedTrainMapping.xlsx',index=False)
