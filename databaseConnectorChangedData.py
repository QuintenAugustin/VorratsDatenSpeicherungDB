#LETS FUCKING GO THANKS STACK OVERFLOW YOU GUYS ARE THE BEST WOOO
import pyodbc
import textformatterTimeTableChanges as changes
import pandas as pd



# Connect to SQL Server
server = '(localdb)\\localBahnminingDB' 
database = 'test' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
cursor = cnxn.cursor()


df = changes.DFChangedArrivals
#Where the dataframe isnt null there is the dataframe, else there is a lack of data. This way this method doesn't complain about that.
df = df.where(pd.notnull(df), None)
records = df.values.tolist()
sql_insert = '''
    declare @EVANumberTrainTrip int = ?
    declare @uniqueTrainTripId varchar(150) = ?
    declare @arrivalCancellationStatus varchar(10) = ?    
    declare @arrivalCancellationTime bigint = ? 
    declare @arrivalChangesPlannedStatus varchar(10) = ?
    declare @arrivalChangePlatform varchar(50) = ?
    declare @arrivalChangeTime bigint = ?
    declare @arrivalChangesLine varchar(50) = ?
    declare @arrivalChangesPlannedPlatform varchar(50) = ?
    declare @arrivalChangesPlannedTime bigint = ?
    declare @arrivalChangesTransition varchar(150) = ?
    declare @uniqueId varchar(200) = ?
    UPDATE [ChangedArrivals]
    SET EVANumberTrainTrip = @EVANumberTrainTrip, 
        uniqueTrainTripId = @uniqueTrainTripId, 
        arrivalCancellationStatus = @arrivalCancellationStatus,
        arrivalCancellationTime = @arrivalCancellationTime,
        arrivalChangesPlannedStatus = @arrivalChangesPlannedStatus,
        arrivalChangePlatform = @arrivalChangePlatform,
        arrivalChangeTime = @arrivalChangeTime,
        arrivalChangesLine = @arrivalChangesLine,
        arrivalChangesPlannedPlatform = @arrivalChangesPlannedPlatform,
        arrivalChangesPlannedTime = @arrivalChangesPlannedTime,
        arrivalChangesTransition = @arrivalChangesTransition
    WHERE uniqueId = @uniqueId

    IF @@ROWCOUNT = 0
        INSERT INTO [ChangedArrivals]
            (uniqueId, EVANumberTrainTrip, uniqueTrainTripid, arrivalCancellationStatus, arrivalCancellationTime, arrivalChangesPlannedStatus, arrivalChangePlatform, arrivalChangeTime, arrivalChangesLine, arrivalChangesPlannedPlatform, arrivalChangesPlannedTime, arrivalChangesTransition)
        VALUES (@uniqueId, @EVANumberTrainTrip, @uniqueTrainTripId, @arrivalCancellationStatus, @arrivalCancellationTime, @arrivalChangesPlannedStatus, @arrivalChangePlatform, @arrivalChangeTime, @arrivalChangesLine, @arrivalChangesPlannedPlatform, @arrivalChangesPlannedTime, @arrivalChangesTransition)

'''
cursor.executemany(sql_insert, records)
print("Changed arrivals insertion executed")

df = changes.DFChangedDepartures
#Where the dataframe isnt null there is the dataframe, else there is a lack of data. This way this method doesn't complain about that.
df = df.where(pd.notnull(df), None)
records = df.values.tolist()
sql_insert = '''
    declare @EVANumberTrainTrip int = ?
    declare @uniqueTrainTripId varchar(150) = ?
    declare @departureCancellationStatus varchar(10) = ?    
    declare @departureCancellationTime bigint = ? 
    declare @departureChangesPlannedStatus varchar(10) = ?
    declare @departureChangePlatform varchar(50) = ?
    declare @departureChangeTime bigint = ?
    declare @departureChangesLine varchar(50) = ?
    declare @departureChangesPlannedPlatform varchar(50) = ?
    declare @departureChangesPlannedTime bigint = ?
    declare @departureChangesTransition varchar(150) = ?
    declare @uniqueId varchar(200) = ?
    UPDATE [ChangedDepartures]
    SET EVANumberTrainTrip = @EVANumberTrainTrip, 
        uniqueTrainTripId = @uniqueTrainTripId, 
        departureCancellationStatus = @departureCancellationStatus,
        departureCancellationTime = @departureCancellationTime,
        departureChangesPlannedStatus = @departureChangesPlannedStatus,
        departureChangePlatform = @departureChangePlatform,
        departureChangeTime = @departureChangeTime,
        departureChangesLine = @departureChangesLine,
        departureChangesPlannedPlatform = @departureChangesPlannedPlatform,
        departureChangesPlannedTime = @departureChangesPlannedTime,
        departureChangesTransition = @departureChangesTransition
    WHERE uniqueId = @uniqueId

    IF @@ROWCOUNT = 0
        INSERT INTO [Changeddepartures]
            (uniqueId, EVANumberTrainTrip, uniqueTrainTripid, departureCancellationStatus, departureCancellationTime, departureChangesPlannedStatus, departureChangePlatform, departureChangeTime, departureChangesLine, departureChangesPlannedPlatform, departureChangesPlannedTime, departureChangesTransition)
        VALUES (@uniqueId, @EVANumberTrainTrip, @uniqueTrainTripId, @departureCancellationStatus, @departureCancellationTime, @departureChangesPlannedStatus, @departureChangePlatform, @departureChangeTime, @departureChangesLine, @departureChangesPlannedPlatform, @departureChangesPlannedTime, @departureChangesTransition)

'''
cursor.executemany(sql_insert, records)
print("Changed departures insertion executed")

cnxn.commit()
#deleting Output file contents to prepare it for next run
open('preprocessedData/timetableChanges/Output.xml', 'w').close()