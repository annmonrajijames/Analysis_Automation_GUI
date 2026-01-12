import pandas as pd
from datetime import datetime, timedelta

# Function to add 5 hours and 30 minutes to the time
def add_time_offset(time_str):
    start_time_str, end_time_str = time_str.split(' to ')
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
    
    # Add 5 hours and 30 minutes
    offset = timedelta(hours=5, minutes=30)
    updated_start_time = start_time + offset
    updated_end_time = end_time + offset
    
    return f"{updated_start_time} to {updated_end_time}"

# Function to process the file and add a new column with updated times
def update_times_in_file(file_path, output_path):
    # Read the file (supports both CSV and Excel)
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
    
    # Add the updated times to a new column
    print(df.head())
    df['Updated Date'] = df['Date_localtime'].apply(add_time_offset)
    
    # Save the file back
    if file_path.endswith('.csv'):
        df.to_csv(output_path, index=False)
    elif file_path.endswith('.xlsx'):
        df.to_excel(output_path, index=False)
    
    print(f"Updated times saved to {output_path}")

# Example usage
file_path = r'C:\Users\kamalesh.kb\Kislay_req_range\dat.xlsx'  # Replace with your file path
output_path = r'C:\Users\kamalesh.kb\Kislay_req_range\dat.xlsx'  # Replace with the desired output file path

update_times_in_file(file_path, output_path)
