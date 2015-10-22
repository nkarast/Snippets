library(dplyr)
library(datasets)

dataset1 <- datasets::airquality
pairs(dataset1)
#remove outliers
dataset1 <- dataset1 %>% # backpipe
                    filter(Solar.R<120.) %>%
                    filter(Temp<18.) 

