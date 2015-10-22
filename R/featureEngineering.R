library(datasets)
dataset1 <- datasets::iris

library(dplyr)


# add two columns  of the area to the dataset
dataset1 <- mutate(dataset1,
                   SepalArea=Sepal.Length*Sepal.Width,
                   PetalArea=Petal.Length*Petal.Width)


# scatterplot matrix
pairs(~ ., data = dataset1)



