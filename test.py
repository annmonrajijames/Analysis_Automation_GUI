import os
import pandas as pd

def process_file(file_path):
    try:
        # Determine the file type based on the extension
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension not in ['.xlsx', '.xls', '.csv']:
            print(f"Skipped: {file_path} (Unsupported file type)")
            return

        # Read the first row to get the date and time from the header
        if file_extension in ['.xlsx', '.xls']:
            first_row = pd.read_excel(file_path, nrows=1, header=None)
        elif file_extension == '.csv':
            first_row = pd.read_csv(file_path, nrows=1, header=None)

        if first_row.empty:
            print(f"Skipped: {file_path} (File is empty)")
            return

        date_time = first_row.iloc[0, 0]
        if ':' in str(date_time):
            date_time = str(date_time).split(':', 1)[1].strip()

        # Read the rest of the data, skipping the first row
        if file_extension in ['.xlsx', '.xls']:
            data = pd.read_excel(file_path, skiprows=1)
        elif file_extension == '.csv':
            data = pd.read_csv(file_path, skiprows=1)

        # Check if "Time" column exists
        if "Time" not in data.columns:
            print(f"Skipped: {file_path} (No 'Time' column found)")
            return

        # Insert the date and time as a new column
        data.insert(0, 'Creation Time', date_time)

        # Drop the first three rows that were originally the 2nd, 3rd, and 4th rows in the file
        if len(data) > 3:
            data = data.drop(data.index[:3])

        # Save the processed data back to the same file
        if file_extension in ['.xlsx', '.xls']:
            data.to_excel(file_path, index=False, engine='openpyxl')
        elif file_extension == '.csv':
            data.to_csv(file_path, index=False)

        print(f"Processed and saved: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    # File path to the input file
    file_path = r"C:\Users\srijanani.LTPL\Downloads\LX 70 _ SEG MOTOR_04-01-2025_ battery no 64_time_01.17 pm to_03.48 pm_Eco mode.xlsx"  # Update this path as needed
    print(f"Processing file: {file_path}")
    process_file(file_path)

if __name__ == "__main__":
    main()
