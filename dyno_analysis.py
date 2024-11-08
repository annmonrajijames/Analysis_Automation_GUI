import pandas as pd

# Load the CSV file
df = pd.read_csv(r"C:\Users\kamalesh.kb\NOV_7_IDC_DATA\Cleaned_data\Modified_FL-07_11_2024-NDURO_190KG_ORD_TRIAL-19_MORNING_TRIAL_DATA.csv")

# 1. Calculate the mean and maximum of 'PackCurr' column
pack_curr_mean = df['PackCurr'].mean()
pack_curr_max = df['PackCurr'].max()
pack_curr_min = df['PackCurr'].min()

print(f"Average of 'PackCurr': ",abs(pack_curr_mean))
print(f"Max of 'PackCurr': ",pack_curr_max)

# 2. Calculate the mean and maximum of 'RLS_Force' column
force_mean = df['RLS_Force'].mean()
force_max = df['RLS_Force'].max()
force_min = df['RLS_Force'].min()

print(f"Average of 'RLS_Force': ",force_mean)
print(f"Max of 'RLS_Force': ",force_max)
print(f"Min of 'RLS_Force': ",force_min)

# 3. Calculate the watt-hours using the formula for 'PackVol'
# Compute delta t based on time differences

# Parse the 'Date Time' column into datetime format with millisecond precision
df['Date Time'] = pd.to_datetime(df['Date Time'], format='%d:%m:%Y %H:%M:%S:%f')

# Calculate time difference in seconds
df['localtime_Diff'] = df['Date Time'].diff().dt.total_seconds().fillna(0)

# Calculate the instantaneous watt-hours for each time interval and store it in a new column
df['power'] = df['PackCurr'] * df['PackVol']


print("Average watt-hours (Wh): ",abs(df['power'].mean()))
print("Peak watt-hours (Wh):",abs(df['power'].mean()))

watt_h = abs((df['PackCurr'] * df['PackVol'] * df['localtime_Diff']).sum()) / 3600  # Convert seconds to hours
print("Actual Watt-hours (Wh): {:.2f}" .format(watt_h))

# print(df[['Date Time', 'localtime_Diff']].head())



