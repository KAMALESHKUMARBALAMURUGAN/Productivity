## MESSAGE FROM AMEY
Need support from @Kamalesh K Balamurugan for setting up script for analysing all ORD Batteries IoT data. This is to check the data uptime with the latest battery & IoT firmware so that we can give a good ahead for 500 build. 

## In person explanation from Amey
1. If 1 or more data came within 30 seconds interval, Increment the Variable "data_count" by '1'. 
2. Condition 1: Sleep status has to be '0' (Because In sleep, Data won't be transmitted for much time).
3. If Sleep status is '0', No data came in a 30 second interval then increment a flag called "No_data". 

**This will be done on each day's data**

1. Time -Time and CAN time
2. Ignore '7' which is sleep and '0' which is for Holiday mode (Bms Status)


## **Moving forward:**
1. The input file will be a excel or csv file.
2. Output will be shown as a print statements
3. In dataframe, the column called "time" , in that column need to find the difference between previous rows "time" column value, for example 00:00:18 in row 2 and 00:00:48 in row 3 of 'time' then new column called 'time_diff' will be created in the dataframe, so in time_diff column in row 3 i want 30. (that is 3-2 and place it in 3)
   