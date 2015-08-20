

complete <- function(directory, id = 1:332) {
    ## 'directory' is a character vector of length 1 indicating
    ## the location of the CSV files
    
    ## 'id' is an integer vector indicating the monitor ID numbers
    ## to be used
    
    ## Return a data frame of the form:
    ## id nobs
    ## 1  117
    ## 2  1041
    ## ...
    ## where 'id' is the monitor ID number and 'nobs' is the
    ## number of complete cases
    
    debug <- 0
    
    ############################################## 
    # initialise the vector of the complete cases 
    nobs <- numeric(0)
    
    for(curr_id in id){
        
        # pasting together the name of the file, using formatC to fix the int width
        temp_filename <- paste(directory,"/",
                               formatC(curr_id, width=3, format="d", flag="0"),
                               ".csv", sep="")
        
        if(debug) print(temp_filename)
        
        # opening the file and reading the df
        temp_file <- read.csv(temp_filename)
        
        # appending to nobs vector the number of complete cases
        nobs <- c(nobs, sum(complete.cases(temp_file)))
        
    }# for
    #print(n_obs)
    
    # creating & return the dataframe
    df <- data.frame(id,nobs,stringsAsFactors=FALSE)
    df
}# end of script