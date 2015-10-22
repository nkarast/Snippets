## Load the data
library(datasets)
dataset1 <- datasets::airquality


## Replace the "." with "_" in dataset headers
names(dataset1) <- gsub("\\.", "_", names(dataset1))


## Remove columns we are not going to use. 
dataset1$Day <- NULL


## Convert some columns to factors/categorical. 
catList <- c("Temp", "Month")
dataset1[, catList] <- lapply(dataset1[, catList], 
                             function(x) as.factor(as.character(x)))


## Scale the numeric features. 
scaleList <- c("Solar_R", "Wind","Ozone")
dataset1[, scaleList] <- lapply(dataset1[, scaleList], function(x) as.numeric(scale(x)))
