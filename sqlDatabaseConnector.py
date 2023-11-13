import pandas as pd
import sqlalchemy as sa
#import textformatter as changedData
import textformatterTimeTablePlanned as plannedData

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

with engine.begin() as conn:
    conn.exec_driver_sql("DROP TABLE IF EXISTS planned_trains_mapping")
    conn.exec_driver_sql(
        "CREATE TABLE planned_trains_mapping(station varchar(50), uniqueTrainTripId varchar(100), uniqueId varchar(100) primary key)"
    )
    df = plannedData.DFPlannedTrainsMapping
    print(df)

    df.to_sql("#temp_table",conn, index=False, if_exists="replace")
    print("Temp dataframe created")
    conn.exec_driver_sql(
        """\
        MERGE planned_trains_mapping WITH (HOLDLOCK) AS main
        USING (SELECT station, uniqueTrainTripId, uniqueId FROM #temp_table) AS temp
        ON (main.uniqueId = temp.uniqueId)
        WHEN NOT MATCHED THEN
            INSERT(station, uniqueTrainTripId, uniqueId) VALUES (temp.station, temp.uniqueTrainTripId, temp.uniqueId);    
    """
    )