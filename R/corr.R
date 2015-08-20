#
# @ Author: Nikolaos Karastathis < nkarast .at. gmail .dot. com >
#
# R Programming : Assignment #1 - Part 3
#


corr <- function(directory, threshold = 0) {
    ## 'directory' is a character vector of length 1 indicating
    ## the location of the CSV files
    
    ## 'threshold' is a numeric vector of length 1 indicating the
    ## number of completely observed observations (on all
    ## variables) required to compute the correlation between
    ## nitrate and sulfate; the default is 0
    
    ## Return a numeric vector of correlations
    ## NOTE: Do not round the result!
    
    
    #############################################################
    debug <- 0
    
    # get the df for complete cases
    comp_df <- complete(directory)
    comp_df <- comp_df[which(comp_df["nobs"]>threshold),]
    id <- comp_df[,"id"]
    
    # initializing null numeric vector
    correlations <- numeric(0)
    
    for(curr_id in id){
        
        # pasting together the name of the file, using formatC to fix the int width
        temp_filename <- paste(directory,"/",
                               formatC(curr_id, width=3, format="d", flag="0"),
                               ".csv", sep="")
        
        if(debug) print(temp_filename)
        
        # opening the file and reading the df
        temp_file <- read.csv(temp_filename)
        
        # appending to the correlations vector
        correlations <- c(correlations, cor(temp_file[,"sulfate"],temp_file[,"nitrate"],use="complete"))
        
    }
    
    correlations
    
}