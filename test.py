import os
import pandas as pd

# Define the path to the folder
main_folder_path = r"C:\Users\annmo\Downloads\EMI_EMC - Copy"

# List all files in the directory
for filename in os.listdir(main_folder_path):
    if filename.endswith('.xlsx'):
        # Construct full file path for the Excel file
        file_path = os.path.join(main_folder_path, filename)
        # Read the Excel file
        df = pd.read_excel(file_path)
        # Construct the .csv file path
        csv_path = os.path.join(main_folder_path, filename[:-5] + '.csv')
        # Write to a .csv file, overwriting any existing file with the same name
        df.to_csv(csv_path, index=False)
        print(f"Converted and replaced {filename} with {os.path.basename(csv_path)}")
        # Remove the original Excel file
        os.remove(file_path)
        print(f"Deleted original Excel file: {filename}")
