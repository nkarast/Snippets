library(DBI) # library(RMySQL) # not required if DBI is there

## Step 1) Create a connection with the Server

con <- dbConnect(RMySQL::MySQL(),
                 dbname   = "company", 
                 host     = "courses.csrrinzqubik.us-east-1.rds.amazonaws.com",
                 port     = 3306,
                 user     = "student",
                 password = "datacamp")

## Step 2) List the tables the DB holds
dbListTables(con)

## Step 3) Read table from DB into a R df
employees_df <- dbReadTable(con, "employees")

## Step 4) Disconnect from DB
dbDisconnect(con)

