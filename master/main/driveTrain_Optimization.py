import pandas as pd
import os

# Load input file
input_file = r"C:\Users\kamalesh.kb\Drive_cycle\Drive_cycle_1\drive_cycle.csv"  # Update with your file path
file_extension = os.path.splitext(input_file)[-1].lower()

# Read the file
if file_extension == ".csv":
    input_data = pd.read_csv(input_file)
elif file_extension in [".xls", ".xlsx"]:
    input_data = pd.read_excel(input_file)
else:
    raise ValueError("Unsupported file format")

# Convert 'DATETIME' column to datetime format
# input_data['DATETIME'] = pd.to_datetime(input_data['DATETIME'], format="%d-%m-%Y %H:%M:%S")
# Convert 'DATETIME' column to datetime format (auto-detect format)
input_data['DATETIME'] = pd.to_datetime(input_data['DATETIME'], format="%Y-%m-%d %H:%M:%S", errors='coerce')


# Set 'DATETIME' as index
input_data.set_index('DATETIME', inplace=True)

# Resample 'MotorSpeed [SA: 02]' to 1-second intervals using mean
sampled_df = input_data['MotorSpeed [SA: 02]'].resample('1S').mean().reset_index()

# Define output file path
output_file = os.path.join(os.path.dirname(input_file), f"resampled{file_extension}")

# Save the output file in the same format as input
if file_extension == ".csv":
    sampled_df.to_csv(output_file, index=False)
else:
    sampled_df.to_excel(output_file, index=False)

print(f"Resampled data saved at: {output_file}")
