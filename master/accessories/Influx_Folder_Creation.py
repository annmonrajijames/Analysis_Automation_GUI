import os
import pandas as pd
from datetime import datetime

def try_parse_date(date_str):
    for fmt in ('%d-%m-%y', '%d/%m/%Y'):  # Add more formats as needed
        try:
            return datetime.strptime(date_str.split()[0], fmt)
        except ValueError:
            continue
    raise ValueError(f"date format not recognized for {date_str}")

def organize_files(root_folder):
    ride_count = {}
    
    for filename in os.listdir(root_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(root_folder, filename)
            
            try:
                data = pd.read_csv(file_path, header=None, low_memory=False)
                date_str = data.iloc[1, 0]
                date_obj = try_parse_date(date_str)
                date_formatted = date_obj.strftime('%d_%B_%Y')
                
                if date_formatted not in ride_count:
                    ride_count[date_formatted] = 0
                ride_count[date_formatted] += 1
                ride_folder = f"Ride_{ride_count[date_formatted]}"
                
                date_folder_path = os.path.join(root_folder, date_formatted)
                if not os.path.exists(date_folder_path):
                    os.makedirs(date_folder_path)
                
                ride_folder_path = os.path.join(date_folder_path, ride_folder)
                os.makedirs(ride_folder_path)
                
                new_file_path = os.path.join(ride_folder_path, 'log.csv')
                os.rename(file_path, new_file_path)
                
                print(f"File {filename} processed and moved to {new_file_path}")
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")

root_folder = r"C:\Users\annmo\Downloads\Root_folder"
organize_files(root_folder)
