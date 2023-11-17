#LETS FUCKING GO THANKS STACK OVERFLOW YOU GUYS ARE THE BEST WOOO


import pyodbc
import textformatterTimeTablePlanned as planned
import pandas as pd


df = planned.DFPlannedTrainsMapping
records = df.values.tolist()


# Connect to SQL Server
server = '(localdb)\\localBahnminingDB' 
database = 'test' 
username = 'User' 
password = '' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
cursor = cnxn.cursor()

#Insert Data
#sql_insert = '''
#    declare @station varchar(50) = ?
#    declare @uniqueTrainTripId varchar(150) = ?
#    declare @uniqueId varchar(200) = ?
#    UPDATE [PLannedTrainsMapping] 
#    SET station = @station, uniqueTrainTripId = @uniqueTrainTripId
#    WHERE uniqueId = @uniqueId

#    IF @@ROWCOUNT = 0
#        INSERT INTO [PlannedTrainsMapping] 
#            (uniqueId, station, uniqueTrainTripId)
#        VALUES (@uniqueId, @station, @uniqueTrainTripId)    
#'''
#cursor.executemany(sql_insert, records)

df = planned.DFPlannedArrivals
#Where the dataframe isnt null there is the dataframe, else there is a lack of data. This way this method doesn't complain about that.
df = df.where(pd.notnull(df), None)
records = df.values.tolist()
sql_insert = '''
    declare @station varchar(50) = ?
    declare @uniqueTrainTripId varchar(150) = ?
    declare @arrivalPlannedLine varchar(50) = ?    
    declare @arrivalPlannedPlatform varchar(50) = ? 
    declare @arrivalPlannedTime bigint = ?
    declare @arrivalPlannedTransition varchar(150) = ?
    declare @uniqueId varchar(200) = ?
    UPDATE [PlannedArrivals]
    SET station = @station, uniqueTrainTripId = @uniqueTrainTripId, arrivalPlannedLine = @arrivalPlannedLine, arrivalPlannedPlatform = @arrivalPlannedPlatform, arrivalPlannedTime = @arrivalPlannedTime, arrivalPlannedTransition = @arrivalPlannedTransition
    WHERE uniqueId = @uniqueId

    IF @@ROWCOUNT = 0
        INSERT INTO [PlannedArrivals]
            (uniqueId, station, uniqueTrainTripid, arrivalPlannedLine, arrivalPlannedPlatform, arrivalPlannedTime, arrivalPlannedTransition)
        VALUES (@uniqueId, @station, @uniqueTrainTripId, @arrivalPlannedLine, @arrivalPlannedPlatform, @arrivalPlannedTime, @arrivalPlannedTransition)

'''
cursor.executemany(sql_insert, records)
print("Planned arrivals insertion executed")

df = planned.DFPlannedDepartures
df = df.where(pd.notnull(df), None)
records = df.values.tolist()
sql_insert = '''
    declare @station varchar(50) = ?
    declare @uniqueTrainTripId varchar(150) = ?
    declare @departurePlannedLine varchar(50) = ?    
    declare @departurePlannedPlatform varchar(50) = ? 
    declare @departurePlannedTime bigint = ?
    declare @departurePlannedTransition varchar(150) = ?
    declare @uniqueId varchar(200) = ?
    UPDATE [PlannedDepartures]
    SET station = @station, uniqueTrainTripId = @uniqueTrainTripId, departurePlannedLine = @departurePlannedLine, departurePlannedPlatform = @departurePlannedPlatform, departurePlannedTime = @departurePlannedTime, departurePlannedTransition = @departurePlannedTransition
    WHERE uniqueId = @uniqueId

    IF @@ROWCOUNT = 0
        INSERT INTO [PlannedDepartures]
            (uniqueId, station, uniqueTrainTripid, departurePlannedLine, departurePlannedPlatform, departurePlannedTime, departurePlannedTransition)
        VALUES (@uniqueId, @station, @uniqueTrainTripId, @departurePlannedLine, @departurePlannedPlatform, @departurePlannedTime, @departurePlannedTransition)
'''
cursor.executemany(sql_insert, records)
print("Planned departure insertion executed")



df = planned.DFTrainInformation
df = df.where(pd.notnull(df), None)
records = df.values.tolist()
sql_insert = '''
    declare @station varchar(50) = ?
    declare @uniqueTrainTripId varchar(150) = ?
    declare @TrainCategory varchar(50) = ?
    declare @TrainNumber int = ?
    declare @uniqueId varchar(200) = ?
    UPDATE [PlannedTrainInformation]
    SET station = @station, uniqueTrainTripId = @uniqueTrainTripId, TrainCategory = @TrainCategory, TrainNumber = @TrainNumber
    WHERE uniqueId = @uniqueId

    IF @@ROWCOUNT = 0
        INSERT INTO [PlannedTrainInformation]
            (uniqueId, station, uniqueTrainTripid, TrainCategory, TrainNumber)
        VALUES (@uniqueId, @station, @uniqueTrainTripId, @TrainCategory, @TrainNumber)
'''
cursor.executemany(sql_insert, records)
print("Planned train information insertion executed")


cnxn.commit()