import pandas as pd
import os

def process_csv_file(file_path):
    try:
        # Read the first line to get the date and time from the header
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
        date_time = first_line.split(':', 1)[1].strip() if ':' in first_line else first_line
    
        # Load the data using a chunk size
        chunk_size = 50000  # Adjust chunk size based on your system's memory
        chunks = pd.read_csv(file_path, skiprows=1, chunksize=chunk_size)
        
        # Check if the "Time" column exists in the first chunk
        first_chunk = next(chunks, None)
        if first_chunk is None or "Time" not in first_chunk.columns:
            print(f"Skipped: {file_path} (No 'Time' column found)")
            return
        
        # If "Time" column exists, reinitialize chunks iterator and proceed with processing
        chunks = pd.read_csv(file_path, skiprows=1, chunksize=chunk_size)
        data_frames = []
        
        for chunk in chunks:
            # Insert the date and time as a new column
            chunk.insert(0, 'Creation Time', date_time)
            data_frames.append(chunk)
    
        # Concatenate all chunks into one DataFrame
        data = pd.concat(data_frames, ignore_index=True)
    
        # Drop the first three rows which were initially 2nd, 3rd, and 4th in the original file
        data = data.drop([0, 1, 2])
    
        # Save the processed data to the same file, overwriting the original
        data.to_csv(file_path, index=False)
        print(f"Processed and saved: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_all_csv_files(root_folder):
    # Find all CSV files in the root_folder and its subdirectories
    for dirpath, _, filenames in os.walk(root_folder):
        for file in filenames:
            if file.endswith('.csv'):
                full_path = os.path.join(dirpath, file)
                process_csv_file(full_path)

root_folder = r"C:\Users\annmo\Downloads\Root_folder"
process_all_csv_files(root_folder)
