library(datasets)
dataset1 <- datasets::iris

plotCols <- c("Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width")


plotBox <- function(x) {
    title <- paste("Box plot of", x, "by Species") 
    ggplot(dataset1, aes_string('Species', x)) +
        geom_boxplot() +ggtitle(title)
}
lapply(plotCols, plotBox)