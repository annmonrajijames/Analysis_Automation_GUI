import pandas as pd

def analyze_data(file_path):
    # Read the input file
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")

    # Convert DateTime to numeric and handle NaN values
    # data['DateTime'] = pd.to_numeric(data['DateTime'], errors='coerce')
    data['DateTime'] = pd.to_datetime(data['DateTime'])
    data = data.dropna(subset=['DateTime'])
    data['DateTime'] = pd.to_datetime(data['DateTime'], unit='s')
    data['DateTime'] = data['DateTime'] + pd.to_timedelta('5h30m')

    # Calculate the localtime difference between consecutive rows
    data['localtime_Diff'] = data['DateTime'].diff().dt.total_seconds().fillna(0)

    # Calculate Speed in m/s
    data['Speed_kmh'] = data['MotorSpeed'] * 0.0836
    data['Speed_ms'] = data['Speed_kmh'] / 3.6

    # Calculate the total distance based on RPM
    total_distance_with_RPM = 0
    for index, row in data.iterrows():
        if 0 < row['MotorSpeed'] < 1000:
            distance_interval = row['Speed_ms'] * row['localtime_Diff']
            total_distance_with_RPM += distance_interval

    total_distance_with_RPM = total_distance_with_RPM / 1000  # Convert to kilometers

    # Print the total distance
    print(f"Total distance based on RPM: {total_distance_with_RPM:.2f} km")

    # Filter data for regeneration current analysis
    filtered_data_withoutDischarge = data[(data['PackCurr'] > 0) & (data['PackCurr'] < 50)]
    regen_ah = abs((filtered_data_withoutDischarge['PackCurr'] * filtered_data_withoutDischarge['localtime_Diff']).sum()) / 3600  # Convert seconds to hours
    avg_regen_current = filtered_data_withoutDischarge['PackCurr'].mean()
    Total_ah = abs((data['PackCurr'] * data['localtime_Diff']).sum()) / 3600  # Convert seconds to hours

    # Calculate the actual Watt-hours (Wh) using the trapezoidal rule for numerical integration
    watt_h = abs((data['PackCurr'] * 51.2 * data['localtime_Diff']).sum()) / 3600  # Convert seconds to hours
    print("Actual Watt-hours (Wh):------------------------------------> {:.2f}" .format(watt_h))

    # Print the regeneration analysis results
    print(f"Total regeneration (Ah): {regen_ah:.2f} Ah")
    print(f"Average regeneration current (A): {avg_regen_current:.2f}")
    print(f"Total Ah: {Total_ah:.2f} Ah")

# Example usage
file_path = r'C:\Users\kamalesh.kb\SANJITH_DRIVE_CYCLE\NDURO_18_ECO_MODE_SANJITH_ORD_DRIVE_1CYCLE_24012025.csv'  # Replace with your file path
analyze_data(file_path)