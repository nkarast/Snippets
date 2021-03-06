## Set a flag to define the environment Azure = FALSE
if(Azure){
    ## If in Azure, read the input data table into a data frame 
    frame1 <- maml.mapInputPort(1)
} else {
    ## If in RStudio read the local .csv file
    dirName <- "/Users/nkarast/Downloads/DAT203xLabfiles"
    fileName <- "cadairydata.csv"
    infile <- file.path(dirName, fileName)
    frame1 <- read.csv( infile, header = TRUE, stringsAsFactors = FALSE)
}
## Select a subset of columns
library(dplyr)

frame1 <- select(frame1, Year, Month, Cottagecheese.Prod, Icecream.Prod, Milk.Prod)
# chain verbs to show totals for August frame1 <- frame1 %>%
filter(Month == 'Aug') %>%
    mutate(Total.Prod = Cottagecheese.Prod + Icecream.Prod + Milk.Prod)
## If in Azure output the data frame. if(Azure) maml.mapOutputPort('frame1')