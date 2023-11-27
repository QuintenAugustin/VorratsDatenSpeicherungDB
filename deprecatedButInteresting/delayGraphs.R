#install.packages("RODBC")
#install.packages("tidyverse")
#install.packages("lubridate")
#install.packages("data.table)
library(lubridate)
library(RODBC)
library(tidyverse)
library(data.table)



#Average arrival delay of every Train category (right now for Hamburg)
ggplot(newrDataFrame2 |>
         filter(stationName == "Hamburg Hbf") |>
         group_by(TrainCategory) |>
         summarise(hmm = mean(arrivalDifftime,na.rm=TRUE)/60),
       aes(x = reorder(TrainCategory, -hmm),y = hmm)
)+
  geom_bar(stat = 'identity')+
  geom_text(aes(label = after_stat(y)))
