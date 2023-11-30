#install.packages("RODBC")
#install.packages("tidyverse")
#install.packages("lubridate")
library(lubridate)
library(RODBC)
library(tidyverse)
#All of this is deprecated and was always only meant as loose tests for figuring out functionality. It was never meant to be very well organised.
#However most of this works and I would have used this in other R files had I decided to go with R
#Connecting to sql server via the odbc connector I have
#This connection method I took from someone else.
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


#testDate <- as.Date(rDataFrame$arrivalPlannedTime, "%y%m%d%H%M")
#?strptime()
#Sanity checking tests
as.Date("2311190847", "%y%m%d%H%M")

#testDateFrame <- as.data.frame(rDataFrame[,5])
#testDataFrame2 <- na.omit(testDateFrame)

newrDataFrame <-rDataFrame
#You know, it took me 2.5 fucking hours to figure this blasted thing out. THE FACT THAT IT WORKED WITH MY TEST LISTS WAS DRIVING ME INSANE!
newrDataFrame2 <- transform(newrDataFrame, arrivalPlannedTime=as.POSIXct(as.character(arrivalPlannedTime), format = '%y%m%d%H%M'))
newrDataFrame2 <- transform(newrDataFrame2, arrivalChangeTime=as.POSIXct(as.character(arrivalChangeTime), format = '%y%m%d%H%M'))
newrDataFrame2 <- transform(newrDataFrame2, departureChangeTime=as.POSIXct(as.character(departureChangeTime), format = '%y%m%d%H%M'))
newrDataFrame2 <- transform(newrDataFrame2, departurePlannedTime=as.POSIXct(as.character(departurePlannedTime), format = '%y%m%d%H%M'))


#This works, however if you want to appear a little more professional and fancy then do the next one bruh
calcTest <- data.frame( newrDataFrame2$arrivalChangeTime - newrDataFrame2$arrivalPlannedTime)


properCalcTest <- data.frame(difftime(newrDataFrame2$arrivalChangeTime, newrDataFrame2$arrivalPlannedTime, units="mins"))
newrDataFrame2$arrivalDifftime <- as.numeric(difftime(newrDataFrame2$arrivalChangeTime, newrDataFrame2$arrivalPlannedTime))
#This does not work because of course it doesn't. Will figure that out later. I love staying up long. <- It works now :) I had to turn difftime into numeric
#That allows for cool math.
ggplot(newrDataFrame2 |>
         group_by(stationName) |>
         summarise(moin = mean(arrivalDifftime)),
       aes(stationName, moin)
       )


newrDataFrame2 |>
  group_by(stationName) |>
  summarise(moin = mean(arrivalDifftime)) -> result
result



#Average arrival delay of every Train category
ggplot(newrDataFrame2 |>
    group_by(TrainCategory) |>
    summarise(hmm = mean(arrivalDifftime,na.rm=TRUE)/60),
    aes(x = reorder(TrainCategory, -hmm),y = hmm)
    )+
geom_bar(stat = 'identity')+
geom_text(aes(label = after_stat(y)))


blob <- rDataFrame
blob$cancellation <- ifelse(is.na(blob$arrivalCancellationStatus), 0, 1)
View(blob)
aggregate(blob[26], list(blob$TrainCategory), mean)
bla <- rDataFrame
bla$cancellation <- ifelse(is.na(bla$arrivalCancellationStatus), 0, 100)
HelloR <-data.frame(aggregate(bla[26], list(bla$TrainCategory), mean))

