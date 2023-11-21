#install.packages("RODBC")
#install.packages("tidyverse")
#install.packages("lubridate")
library(lubridate)
library(RODBC)
library(tidyverse)

#Connecting to sql server via the odbc connector I have
db_conn <- odbcConnect("RDatabaseConnector", rows_at_time = 1)

if (db_conn == -1) {
  quit("no", 1)
}

sql <- "
SELECT *
  FROM [test].[dbo].[ViewForR]
"
#Dataframe created here. This actually worked first try. A first in this project. I am shocked.
rDataFrame <- sqlQuery(db_conn, sql, stringsAsFactor = FALSE)
#Closing database connection
odbcClose(db_conn)

View(rDataFrame)


#Amount of planned train trip entries for each station in database
ggplot(rDataFrame, aes(x = fct_infreq( stationName))) +
  geom_bar()

ggplot(rDataFrame, aes(x = stationName, y = arrivalPlannedLine)) +
  geom_bar()
#Hell yeah, not is.na gives me this here basic functionality.
rDataFrame |>
  group_by(stationName) |> summarise(non_na_count = sum(!is.na(arrivalPlannedLine)))

test <- rDataFrame |>
  group_by(stationName) |> summarise(non_na_count = sum(!is.na(departurePlannedLine)))

ggplot(test, aes( x = stationName, y = non_na_count))+
  geom_bar(stat='identity')

#bar chart that displays the amount of planned trains for a station
ggplot(rDataFrame |>
         group_by(stationName)|>
         summarise(non_na_count = sum(!is.na(departurePlannedLine))),
       aes(stationName, non_na_count)
       ) +
  geom_bar(stat ='identity')+
  geom_text(aes(label = after_stat(y)))

#This gets me today. Very useful.
Sys.Date()


testDate <- as.Date(DateTime,rDataFrame$arrivalPlannedTime, "%yy-%mm-%dd %HH-%MM")
