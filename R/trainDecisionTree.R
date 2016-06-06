##
##  Build a decision tree to indentify the species
##

library(datasets)
library(caret)
library(rattle)

# Step 1: Get the data
indata <- datasets::iris
    
# Step 2: Explore..
#pairs(~. , data=indata)
        # there is some interesting behaviour (linear rel. petal L/W, 
        # clusters of Sepal L.W)
        # let's throw everything into a DT

## or using carets feature plot
# 1. pairs
plot_feat_pairs <-featurePlot(x=indata[, 1:4], 
                        y= indata$Species, 
                        plot="pairs", #plot="ellipse",
                        ## Add a key at the top
                        auto.key = list(columns=3))
plot_feat_pairs

# 2. pairs+ellipse
plot_feat_ellipse <-featurePlot(x=indata[, 1:4], 
                              y= indata$Species, 
                              plot="ellipse",
                              ## Add a key at the top
                              auto.key = list(columns=3))
plot_feat_ellipse

# 3. density
plot_feat_density <-featurePlot(x=indata[, 1:4], 
                                y= indata$Species, 
                                plot="density",
                                ## Pass in options to xyplot() to 
                                ## make it prettier
                                scales = list(x = list(relation="free"),
                                              y = list(relation="free")),
                                adjust = 1.5,
                                pch = "|",
                                layout = c(4, 1),
                                auto.key = list(columns = 3))
plot_feat_density

# 4. Box Plots
plot_feat_box <- featurePlot(x = iris[, 1:4],
                             y = iris$Species,
                             plot = "box",
                             ## Pass in options to bwplot() 
                             scales = list(y = list(relation="free"),
                                           x = list(rot = 90)),
                             layout = c(4,1 ),
                             auto.key = list(columns = 2))
plot_feat_box



# Step 3 : Set the seed
set.seed(1987)

# Step 4: Sample the dataset -> Generate a vector by sampling the linear
#         space from index 1 to nrow(indata) and sample it floor(nrow(indata))*0.6
#         times
#                       150      ,       90
train_indx <- sample(nrow(indata), floor(nrow(indata)*0.6))

train_sample <- indata[train_indx, ]    # all columns from the indices above
test_sample  <- indata[-train_indx, ]   # all the columns from the rest


# Step 5: Train the model using the caret train() function
#         the algorithm is in the "method" arg
#         the Y and X vectors are defined as formula : y ~ x1 + x2 + ...
formula <- as.formula(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width)

# method is the method string ( use names(getModelInfo()) to find out)
# minsplit = min # of obs in a node to split
# minbucket = min # of obs in a leaf node
# cp = complexity parameter : Any split that does not decrease the overall 
#                               lack of fit by a factor of cp is not attempted. 
# maxdepth = maximum size of tree (Root = 0)
tr <- train(formula, train_sample, method="rpart", minsplit=2, 
            minbucket=1, cp=0.001, maxdepth=8)



# visualise the tree with rattle fancyRpartPlot
fancyRpartPlot(tr$finalModel)
