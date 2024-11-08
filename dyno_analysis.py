import pandas as pd
import openpyxl

# Load the CSV file
df = pd.read_csv(r"C:\Users\kamalesh.kb\NOV_7_IDC_DATA\Cleaned_data\Modified_FL-07_11_2024-NDURO_190KG_ORD_TRIAL-19_MORNING_TRIAL_DATA.csv")

# Calculate the mean, max, and min of 'PackCurr' column
pack_curr_mean = abs(df['PackCurr'].mean())
pack_curr_max = df['PackCurr'].max()
pack_curr_min = df['PackCurr'].min()

# Calculate the mean, max, and min of 'ForceAtWheel' column
force_mean = df['ForceAtWheel'].mean()
force_max = df['ForceAtWheel'].max()
force_min = df['ForceAtWheel'].min()

# Parse the 'Date Time' column into datetime format with millisecond precision
df['Date Time'] = pd.to_datetime(df['Date Time'], format='%d:%m:%Y %H:%M:%S:%f')

# Calculate time difference in seconds
df['localtime_Diff'] = df['Date Time'].diff().dt.total_seconds().fillna(0)

# Calculate the instantaneous power and watt-hours
df['power'] = df['PackCurr'] * df['PackVol']
average_power = abs(df['power'].mean())
peak_power = abs(df['power'].max())

# Calculate total watt-hours
watt_h = abs((df['PackCurr'] * df['PackVol'] * df['localtime_Diff']).sum()) / 3600

# Prepare analysis data for Excel output
ppt_data = {
    "Average of 'PackCurr' (A)": pack_curr_mean,
    "Max of 'PackCurr' (A)": pack_curr_max,
    "Min of 'PackCurr' (A)": pack_curr_min,
    "Average of 'ForceAtWheel' (N)": force_mean,
    "Max of 'ForceAtWheel' (N)": force_max,
    "Min of 'ForceAtWheel' (N)": force_min,
    "Average Power (W)": average_power,
    "Peak Power (W)": peak_power,
    "Total Watt-hours (Wh)": watt_h,
}

# Create a new Excel workbook and write data to it
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Analysis Results"

# Populate Excel sheet with analysis data
for i, (key, value) in enumerate(ppt_data.items(), start=1):
    ws.cell(row=i, column=1, value=key)
    ws.cell(row=i, column=2, value=value)

# Define the output file path
folder_path = r"C:\Users\kamalesh.kb\NOV_7_IDC_DATA\Cleaned_data"
folder_name = "Modified_FL-07_11_2024-NDURO_190KG_ORD_TRIAL-19_MORNING_TRIAL_DATA"
excel_output_file = f"{folder_path}/analysis_{folder_name}.xlsx"

# Save the Excel workbook
wb.save(excel_output_file)
print("Excel output file generated at:", excel_output_file)
