#This file exists because I am stupid and too lazy to go figure out CSV imports into sql server lol
#Also yes I could probably do my other sql stuffs with df.to_sql but the way I found works and is tested. 
#Don't want to touch it unless I have excess time and suffer from severe boredom.


import pandas as pd 
import pyodbc
import sqlalchemy as sa

# Connect to SQL Server
connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=(localdb)\\localBahnminingDB;"
    "Database=test;"
    "Trusted_Connection=yes;"
)

connection_url = sa.engine.URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": connection_string}
)

engine = sa.create_engine(connection_url, fast_executemany=True)

df = pd.read_csv('importantResources/AllStationEvaNumbers2020.CSV', sep=';', decimal=',')
print(df)
df = df.where(pd.notnull(df), None)
df.to_sql("StationData", engine, index=False, if_exists="replace")
