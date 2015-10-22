library(datasets)
library(ggplot2)

# Load the iris dataset
dataset1 <-  datasets::iris

# Plot few columns
plotCols <- c("Sepal.Length", "Sepal.Width")


plotIris <- function(x){
    title <- paste("Petal width vs",x,"\n conditioned on species")
    ggplot(dataset1, aes_string(x, "Petal.Width"))+geom_point() + 
        facet_grid(. ~ Species) + ggtitle(title) + stat_smooth(method="lm")
    
    
}#end of plotIris

lapply(plotCols, plotIris)


####

#plotCols4 <- c("RelativeCompactness",
#               "SurfaceArea",
#               "WallArea",
#               "RoofArea",
#               "GlazingArea",
#               "GlazingAreaDistribution",
#               "HeatingLoad")
#library(gridExtra)
#eeHist <- function(x) {
#    title <- paste("Histogram of", x, "conditioned on OverallHeight")
#    ggplot(dataset1, aes_string(x)) + geom_histogram(aes(y = ..density..)) + facet_grid(. ~ OverallHeight) + ggtitle(title) +
#        geom_density()
#}
#lapply(plotCols4, eeHist)