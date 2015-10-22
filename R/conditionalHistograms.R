library(datasets)
dataset1 <- datasets::iris

# use ggplot2 to create conditioned scatter plots
plotCols <- c("Sepal.Length", 
              "Sepal.Width", "Petal.Length")

plotData <-function(x){
    title<- paste("Petal.Width vs",x, "\n conditioned on species")
    ggplot(dataset1, aes_string(x)) + geom_histogram(aes(y=..density..)) +
        facet_grid(. ~ Species) + 
        ggtitle(title) + 
        geom_density()
    
}#end of function
lapply(plotCols, plotData)