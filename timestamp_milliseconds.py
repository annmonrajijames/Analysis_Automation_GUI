import pandas as pd
import os

# Load the CSV file
df = pd.read_csv(r'C:\Users\kamalesh.kb\Nduro_3_kw\Nduro_3kWh _05-11-2024__time_11-21amto_11.54am.csv')

# Assuming the DATETIME column is named 'DATETIME'
df['DATETIME'] = pd.to_datetime(df['DATETIME'], unit='s')  # Convert to datetime from seconds

# Add 5 hours and 30 minutes to each timestamp
df['DATETIME'] = df['DATETIME'] + pd.to_timedelta('5h30m')

# Format the DATETIME to include milliseconds and display as hh:mm:ss:SSS format
df['formatted_timestamp'] = df['DATETIME'].dt.strftime('%H:%M:%S') + ':' + (df['DATETIME'].dt.microsecond // 1000).astype(str)

# Remove any unnecessary zeros and ensure the milliseconds display correctly
df['formatted_timestamp'] = df['formatted_timestamp'].str.replace(r"(\d{2})(\d{1})$", r"\1:\2")

# Get the directory of the input file
input_file_dir = os.path.dirname(r'C:\Users\kamalesh.kb\Nduro_3_kw\Nduro_3kWh _05-11-2024__time_11-21amto_11.54am.csv')

# Save the modified DataFrame to a new CSV file in the same directory
output_file = os.path.join(input_file_dir, 'output.csv')
df.to_csv(output_file, index=False)

