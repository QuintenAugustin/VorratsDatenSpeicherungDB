#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#
library(RODBC)
library(shiny)
library(ggplot2)
library(tidyverse)
library(kableExtra)
library(data.table)

# Define UI for application that draws a histogram
ui <- basicPage(

    # Application title
    h1("Train Data"),

     #      plotOutput("Plot")
mainPanel(
  #If you uncomment these they should work. This was all still testing phase, however 
  #plotOutput("plot"),
  #plotOutput("plot2"),
 # plotOutput("plot3")
  #tabsetPanel(tabPanel("Data", tableOutput("tbTable")))
  tableOutput("tbTable2")
)
)

# Define server logic required to draw a histogram
server <- function(input, output, session) {
  myData <- reactive({
    #Connecting to sql server via the odbc connector I have
    db_conn <- odbcConnect("RDatabaseConnector", rows_at_time = 1)
    
    if (db_conn == -1) {
      quit("no", 1)
    }
    sql <- "SELECT * FROM [test].[dbo].[ViewForR]"
    resTest <- data.frame(sqlQuery(db_conn, sql, stringsAsFactor = FALSE))
    #Closing database connection
    odbcClose(db_conn)
    print(resTest)
  })
#  myData2 <- reactive ({
  #This is where i decided to drop R. I could not get these after another to work in any way :( It was taking too much time to get it to work ultimately.
 #   myData2 <- myData()
   # myData2 <- transform(myData(), arrivalPlannedTime=as.POSIXct(as.character(arrivalPlannedTime), format = '%y%m%d%H%M'))
#    myData2 <- transform(myData(), arrivalChangeTime=as.POSIXct(as.character(arrivalChangeTime), format = '%y%m%d%H%M'))
 #   myData2 <- transform(myData(), departureChangeTime=as.POSIXct(as.character(departureChangeTime), format = '%y%m%d%H%M'))
  #  myData2 <- transform(myData(), departurePlannedTime=as.POSIXct(as.character(departurePlannedTime), format = '%y%m%d%H%M'))
   # myData2$arrivalDifftime <- as.numeric(difftime(myData2$arrivalChangeTime, myData2$arrivalPlannedTime))
 # })
  #Time for the ultimate badness but i have no time to figure out a nice solution.
  modifiedData1 <- reactive ({
      transform(myData(), arrivalPlannedTime=as.POSIXct(as.character(arrivalPlannedTime), format = '%y%m%d%H%M'))
    print(modifiedData1)
      })

  
  
  
  output$tbTable <-
    renderTable(myData())
  
  
  output$tbTable2 <-
    renderTable(modifiedData1())
  
  output$plot <- 
    renderPlot({
      df <- myData()
      ggplot(df, aes(x = fct_infreq(stationName)))+ 
        geom_bar()
    })
  output$plot2 <- 
    renderPlot({
    ggplot(myData()|>
             group_by(stationName)|>
             summarise(not_na_count = sum(!is.na(departurePlannedLine))),
           aes(stationName, not_na_count)
           )+
    geom_bar(stat = 'identity')
    })
  #output$plot3 <-
   # renderPlot({
   #   myData2 <- transform(myData(), arrivalPlannedTime=as.POSIXct(as.character(arrivalPlannedTime), format = '%y%m%d%H%M'))
  #    myData2 <- transform(myData(), arrivalChangeTime=as.POSIXct(as.character(arrivalChangeTime), format = '%y%m%d%H%M'))
  #    myData2 <- transform(myData(), departureChangeTime=as.POSIXct(as.character(departureChangeTime), format = '%y%m%d%H%M'))
  #    myData2 <- transform(myData(), departurePlannedTime=as.POSIXct(as.character(departurePlannedTime), format = '%y%m%d%H%M'))
   #   myData2$arrivalDifftime <- as.numeric(difftime(myData2$arrivalChangeTime, myData2$arrivalPlannedTime))
    #  ggplot(myData2 |>
    #           group_by(TrainCategory) |>
    #           summarise(hmm = mean(arrivalDifftime,na.rm=TRUE)/60),
     #        aes(x = reorder(TrainCategory, -hmm),y = hmm)
    #  )+
     #   geom_bar(stat = 'identity')+
      #  geom_text(aes(label = after_stat(y)))
      
      
    #})
  
  

    #output$Plot <- renderPlot({ })
}

# Run the application 
shinyApp(ui = ui, server = server)
