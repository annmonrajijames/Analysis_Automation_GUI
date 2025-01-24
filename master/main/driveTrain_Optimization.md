import pandas as pd
 
# Assuming 'df' is your DataFrame with a datetime index and a 'motor_speed' column
 
# Resample to 1-second intervals and apply different aggregations
resampled_sum = df['motor_speed'].resample('1S').mean()


like this
input file - .csv or .xlsx
Make the input data as a dataframe called - "input_data"

what i want is, i have a column called 'MotorSpeed [SA: 02]' in my excel or csv data.

i have my time column called "DATETIME" - which is of format - 22-01-2025  13:54:57, 22-01-2025  13:54:58

i will be having 'n' data for example 5 data in 22-01-2025  13:54:57 and 10 data in 22-01-2025  13:54:58, so i want to resample it using mean() method.

and save the updated df as sampled_df and create a new output file and save in the smae folder of the input file (but you must not replace the input raw file)

Output file - In the same location of input file (same as input file format - if input .csv then output also .csv and vice versa)


**Bottleneck:**
If resampling done on Motorspeed, then what will we do with other parameters



# Resample to 1-second intervals and apply different aggregations
resampled_sum = df['motor_speed'].resample('1S').sum()
resampled_median = df['motor_speed'].resample('1S').median()
resampled_max = df['motor_speed'].resample('1S').max()
resampled_min = df['motor_speed'].resample('1S').min()
resampled_count = df['motor_speed'].resample('1S').count()
resampled_first = df['motor_speed'].resample('1S').first()
resampled_last = df['motor_speed'].resample('1S').last()
resampled_std = df['motor_speed'].resample('1S').std()
resampled_var = df['motor_speed'].resample('1S').var()