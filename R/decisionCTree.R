# Let'us use ctree on iris

library(datasets)
library(party) # ctree

indata <- datasets::iris

# set seed
set.seed(1987)

# split the dataset
train_indx <- ssample(nrow(indata), floor(nrow(indata)*0.7))
train_set <- indata[train_indx, ]
test_set <- indata[-train_indx, ]

# train a ctree mode
model <- ctree(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width, data=train_set)