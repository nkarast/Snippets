# Get the iris dataset
library(datasets)
dataset1 <- datasets::iris

## remove the species column
cols <- c("Species","Sepal.Length")

dataset1 <- dataset1[, !(names(dataset1)) %in% cols]

## Create a pairs plot.
#pairs(dataset1)
pairs(~., data=dataset1)   # the ~. statement creates the scatterplot for all columns in data