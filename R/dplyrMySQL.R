# set up a src that connects to the mysql database (src_mysql is provided by dplyr)
my_db <- src_mysql(dbname = "dplyr", 
                   host = "dplyr.csrrinzqubik.us-east-1.rds.amazonaws.com", 
                   port = 3306, 
                   user = "dplyr",
                   password = "dplyr")

# and reference a table within that src: nycflights is now available as an 
#R object that references to the remote nycflights table
nycflights <- tbl(my_db, "dplyr")

# glimpse at nycflights
glimpse(nycflights)

# Calculate the grouped summaries detailed in the instructions
nycflights %>% group_by(carrier) %>% summarise(n_flights = n(), avg_delay = mean(arr_delay)) %>% arrange(avg_delay)

