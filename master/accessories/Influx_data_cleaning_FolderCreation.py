import pandas as pd
def process_data(file_path):
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
        return file_path  # If no "Time" column, return without processing
    
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
    
    return file_path

path=r"C:\Users\annmo\Downloads\Root_folder\oct_8\r1\log.csv"
process_data(path)