#LETS FUCKING GO THANKS STACK OVERFLOW YOU GUYS ARE THE BEST WOOO


import pyodbc
import textformatterTimeTablePlanned as planned


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
sql_insert = '''
    declare @station varchar(50) = ?
    declare @uniqueTrainTripId varchar(150) = ?
    declare @uniqueId varchar(200) = ?
    UPDATE [PLannedTrainsMapping] 
    SET station = @station, uniqueTrainTripId = @uniqueTrainTripId
    WHERE uniqueId = @uniqueId

    IF @@ROWCOUNT = 0
        INSERT INTO [PlannedTrainsMapping] 
            (uniqueId, station, uniqueTrainTripId)
        VALUES (@uniqueId, @station, @uniqueTrainTripId)    
'''
cursor.executemany(sql_insert, records)

df = planned.DFTrainInformation
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

cnxn.commit()