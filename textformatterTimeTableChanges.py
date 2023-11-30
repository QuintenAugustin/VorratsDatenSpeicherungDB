import pandas as pd
import pandas_read_xml as pdx
import xml.etree.ElementTree as ET
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 12)




#This is bad but its the easiest way to deal with the various xml files. I should replace this with a loop like I did for the API connectors
#But honestly this works and id rather not touch this now as its not that bad for few trains. Only gets relevant when you massively increase scope.
#Full disclaimer: This does not handle unexpected API returns well. That thus far only happened a single time due to API downtime.
#This API downtime happened on the night of the 26th of November. Before then I had no way to handle it because I did not know what 
#API downtime would look like. Answer: XML Document with downtime warnings. Had I known what the warnings look like i'd have handled this,
#However it is way too close to deadline to hastily try implementing a catch for that and potentially destroying everything.
#Another note: The reason I wanted to consolidate everything before pushing to the Server is that I assume that this would be less Server activity. Whether ultimately consolidating and then pushing once or pushing once for every station is better I dont know. I suspect that since this consolidation and fully  flattening grows exponentially this may be worse but I do not know.
data1 = ET.tostring(ET.parse('rawdata/timetableChanges/8000028.xml').getroot()).decode("utf-8")
data2 = ET.tostring(ET.parse('rawdata/timetableChanges/8000105.xml').getroot()).decode("utf-8")
data3 = ET.tostring(ET.parse('rawdata/timetableChanges/8002549.xml').getroot()).decode("utf-8")
data4 = ET.tostring(ET.parse('rawdata/timetableChanges/8011160.xml').getroot()).decode("utf-8")
f = open("preprocessedData/timetableChanges/Output.xml", "a+")
#This is here so that element tree parser doesnt complain about junk, gotta have proper xml structure sadly
f.write("<new_root>")
f.write(data1)
f.write(data2)
f.write(data3)
f.write(data4)
f.write("</new_root>")
f.close()
print('XMLs unioned, starting dataframe construction')


#The unioned XML is completely flattened by this godsend of a package. Arriving at these two lines took 20hours.
#There is a reason why this bloody file used to be called textformatter9.py in past commits......
df = pdx.read_xml("preprocessedData/timetableChanges/Output.xml", [ 'new_root','timetable'], root_is_rows=False)
df = pdx.fully_flatten(df)
print('Base dataframe constructed') 
#df.to_excel('output3.xlsx', index=False)
#Dealing with non existant columns to ensure that they exist.
cols_to_check = ['s|@eva', 's|@id', 's|ar|@clt', 's|ar|@cp', 's|ar|@cs', 's|ar|@cpth', 's|ar|@ct', 's|ar|@dc', 's|ar|@l', 's|ar|@pp', 's|ar|@ppth', 's|ar|@ps', 's|ar|@pt', 's|ar|@tra', 's|dp|@clt', 's|dp|@cp', 's|dp|@cpth', 's|dp|@cs', 's|dp|@ct', 's|dp|@l', 's|dp|@pp', 's|dp|@ppth', 's|dp|@ps', 's|dp|@pt', 's|dp|@tra']
unionList=list(set(df.columns).union(cols_to_check))
df = df.reindex(columns=sorted(unionList)).fillna('').replace([''], [None])
#Non existant value are None, important later on for sql too. 
#Renaming the automatically generated columns that represent file path to make them nice to read and sanity check.
df.rename(columns={'@station' : 'station',
                   's|@eva':'EVANumberTrainTrip', 
                   's|@id':'uniqueTrainTripId',
                   's|ar|@clt':'arrivalCancellationTime',
                   's|ar|@cp':'arrivalChangePlatform', 
                   's|ar|@cs':'arrivalCancellationStatus',
                   's|ar|@cpth':'arrivalChangePath', 
                   's|ar|@ct':'arrivalChangeTime',
                   's|ar|@dc':'arrivalDistantChange', #Tf does this mean? Seems to be very rare. Taking it out for now.
                   's|ar|@l':'arrivalChangesLine',
                   's|ar|@pp':'arrivalChangesPlannedPlatform',
                   's|ar|@ppth':'arrivalChangesPlannedPath',
                   's|ar|@ps':'arrivalChangesPlannedStatus', #This is also used if a cancellation has been revoked!
                   's|ar|@pt':'arrivalChangesPlannedTime', #Probably won't use this one to avoid data doubling. Edit: I am using this to see whether I can make even more fun of DB
                   's|ar|@tra':'arrivalChangesTransition', #Train changes ID from one to another due to operating a different trip now. Annoying but makes sense.
                   's|dp|@clt':'departureCancellationTime',
                   's|dp|@cp':'departureChangePlatform',
                   's|dp|@cpth':'departureChangePath',
                   's|dp|@cs':'departureCancellationStatus',
                   's|dp|@ct':'departureChangeTime',
                   's|dp|@l':'departureChangesLine',
                   's|dp|@pp':'departureChangesPlannedPlatform',
                   's|dp|@ppth':'departureChangesPlannedPath',
                   's|dp|@ps':'departureChangesPlannedStatus', #Same as with the last planned status.
                   's|dp|@pt':'departureChangesPlannedTime',
                   's|dp|@tra':'departureChangesTransition',          
                   },inplace=True)
print('Base dataframe formatted')
#df.to_excel('output4.xlsx', index=False)
#print(df)
#df.to_csv('moin.csv', index=False)

#Splitting the base dataframe up into several parts for being inserted into a relational database later on.
#Might as well do it here and not tax the database with continuous junk later on. Also saves massively on local storage doing it this way.
#To put things into perspective, the base dataframe saved into excel for just Frankfurt and Bayreuth was 12k rows. This is 3k.
DFChangedArrivals=df[['EVANumberTrainTrip','uniqueTrainTripId','arrivalCancellationStatus','arrivalCancellationTime','arrivalChangesPlannedStatus','arrivalChangePlatform','arrivalChangeTime','arrivalChangesLine','arrivalChangesPlannedPlatform','arrivalChangesPlannedTime','arrivalChangesTransition']]
DFChangedArrivals=DFChangedArrivals.drop_duplicates()
DFChangedArrivals['uniqueId']=DFChangedArrivals['EVANumberTrainTrip'].astype(str) + DFChangedArrivals['uniqueTrainTripId'].astype(str) 
print('Arrival changes dataframe extracted')

DFChangedDepartures=df[['EVANumberTrainTrip','uniqueTrainTripId','departureCancellationStatus','departureCancellationTime','departureChangesPlannedStatus','departureChangePlatform','departureChangeTime','departureChangesLine','departureChangesPlannedPlatform','departureChangesPlannedTime','departureChangesTransition']]
DFChangedDepartures=DFChangedDepartures.drop_duplicates()
DFChangedDepartures['uniqueId']=DFChangedDepartures['EVANumberTrainTrip'].astype(str) + DFChangedDepartures['uniqueTrainTripId'].astype(str)
print('Departure changes dataframe extracted')

DFChangedDataMapping=df[['EVANumberTrainTrip','uniqueTrainTripId']]
DFChangedDataMapping=DFChangedDataMapping.drop_duplicates()
print('Change data Station-TripId mapping extracted')

#These are only here if you want to observe what output data might look like. Mostly for sanity checking.
#print(df)
#DFChangedArrivals.to_excel('arrivalData.xlsx', index=False)
#DFChangedDepartures.to_excel('departureData.xlsx', index=False)
#DFChangedDataMapping.to_excel('changedDataMapping.xlsx', index=False)

