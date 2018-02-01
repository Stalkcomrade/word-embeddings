#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#

library(shiny)
library(rbokeh)
library(readr)
library(magrittr)

# Define UI 
ui <- fluidPage(
  
  # Application title
  titlePanel("Semantic Space for IMDB comments"),
  
  # Sidebar
  sidebarLayout(
    sidebarPanel(
      numericInput("clust",
                   "Number of Clusters", 
                   value = 10),
      numericInput("words",
                   "Number of Words", 
                   value = 500),
      actionButton("run", "Run")),
    
    mainPanel(
      rbokeh::rbokehOutput("distPlot")
    )
  )
)
# Define server logic
server <- function(input, output) {
  
  interm <- eventReactive(input$run, {
    
    ## using bash to call .py script
    print(str_c('python3.5 /home/ruser/imdb/app/Untitled.py --words=', input$words,' --clusters=', input$clust))
    system(str_c('python3.5 /home/ruser/imdb/app/Untitled.py --words=', input$words,' --clusters=', input$clust))
    
    
    tsne_df = read_csv("/home/ruser/imdb/data/tsne_df.csv")
    tsne_df$cluster %<>% as.character()
    return(tsne_df)
  }) 
  
  output$distPlot <- renderRbokeh(
    
    figure(width = 1000, height = 800, legend_location = NULL) %>% 
      ly_points(data = interm(), x = x, y = y, color = color,
                glyph = cluster, hover = words) 
  )
}

shinyApp(ui = ui, server = server)

