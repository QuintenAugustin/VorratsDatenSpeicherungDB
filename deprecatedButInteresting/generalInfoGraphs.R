#install.packages("RODBC")
#install.packages("tidyverse")
#install.packages("lubridate")
#install.packages("data.table)
library(lubridate)
library(RODBC)
library(tidyverse)
library(data.table)



#Amount of trips recorded in database by station
ggplot(rDataFrame, aes(x = fct_infreq( stationName))) +
  geom_bar()


#Amount of trips by train category
ggplot(rDataFrame, aes(x = fct_infreq(TrainCategory)))+
  geom_bar()
