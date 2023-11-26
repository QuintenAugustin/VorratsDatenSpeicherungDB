#install.packages("RODBC")
#install.packages("tidyverse")
#install.packages("lubridate")
#install.packages("data.table)
library(lubridate)
library(RODBC)
library(tidyverse)
library(data.table)
library(plyr)
library(kableExtra)


#Hell yeah, not is.na gives me this here basic functionality.
#bar chart that displays the amount of planned trains for a station
ggplot(rDataFrame |>
         group_by(TrainCategory)|>
         summarise(non_na_count = sum(!is.na(arrivalCancellationStatus))/nrow(rDataFrame[!is.na(rDataFrame$arrivalPlannedTime),])),
       aes(TrainCategory, non_na_count)
) +
  geom_bar(stat ='identity')+
  geom_text(aes(label = after_stat(y)))

nrow(rDataFrame[!is.na(rDataFrame$arrivalPlannedTime),]) |>
  group_by(TrainCategory)


rDataFrame |>
  count(TrainCategory)

result <- rDataFrame |>
  group_by(TrainCategory) |>
  summarise(bleh = {nrow(result$arrivalPlannedTime)})


blob <- rDataFrame
blob$cancellation <- ifelse(is.na(blob$arrivalCancellationStatus), 0, 1)

bla <- data.frame(aggregate(blob[26], list(blob$TrainCategory), mean))

bla <- data.frame(rDataFrame |>
                    filter(!is.na(arrivalPlannedTime)))
#You know this is really bad but its fine. 100 to get Percentage values lol
bla$cancellation <- ifelse(is.na(bla$arrivalCancellationStatus), 0, 100)

helloR <-data.frame(aggregate(bla[26], list(bla$TrainCategory), mean))


helloR |>
  kbl() |>
  kable_classic(full_width = F, html_font = "Cambria", position = "left")

