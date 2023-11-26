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
  plotOutput("plot"),
  plotOutput("plot2")
 # tabsetPanel(tabPanel("Data", tableOutput("tbTable")))
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
    resTest <- sqlQuery(db_conn, sql, stringsAsFactor = FALSE)
    #Closing database connection
    odbcClose(db_conn)
    resTest
  })
  output$tbTable <-
    renderTable(myData())
  
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
  
  

    #output$Plot <- renderPlot({ })
}

# Run the application 
shinyApp(ui = ui, server = server)
