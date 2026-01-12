import os
import pandas as pd

def find_excel_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.startswith('analysis') and file.endswith('.xlsx'):
                yield os.path.join(root, file)

def merge_columns(files):
    df_list = []
    for file in files:
        df = pd.read_excel(file, usecols=[1])  # Read only the second column
        df_list.append(df)
    
    # Concatenate all dataframes horizontally
    merged_df = pd.concat(df_list, axis=1)
    return merged_df

# Specify the path to your root folder
root_directory = r"C:\Users\annmo\OneDrive\Desktop\Influx_LX70"
excel_files = find_excel_files(root_directory)
result_df = merge_columns(excel_files)

# Save the result to a new CSV file on your desktop
result_df.to_csv(r'C:\Users\annmo\OneDrive\Desktop\merged_output.csv', index=False)
