import pandas as pd

# Read the input file (assuming CSV format)
df = pd.read_excel(r'C:\Users\kamalesh.kb\BATTERY_IOT_DATA_ANALYSIS\CanData_ML2AJBKNDA00151.xlsx')

# Convert the 'time' column to datetime format
df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')

# Calculate the time difference in seconds and create a new column 'time_diff'
df['time_diff'] = df['time'].diff().dt.total_seconds()

# Print the dataframe to show the output
print(df)import pandas as pd

# Read the input file (assuming CSV format)
df = pd.read_excel(r'C:\Users\kamalesh.kb\BATTERY_IOT_DATA_ANALYSIS\CanData_ML2AJBKNDA00151.xlsx')

# Convert the 'time' column to datetime format
df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')

# Calculate the time difference in seconds and create a new column 'time_diff'
df['time_diff'] = df['time'].diff().dt.total_seconds()

# Print the dataframe to show the output
print(df)