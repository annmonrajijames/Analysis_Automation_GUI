import pandas as pd
import matplotlib.pyplot as plt
 
# Load the data from the Excel file
file_path = r'Enter_file_path'  # Update with your actual file path
data = pd.read_excel(file_path)
 
# Filter out rows where PackCurr_6 is greater than 0
filtered_data = data[data['PackCurr_6'] <= 0]
 
# Define the bins and labels for categorization
bins = [-float('inf'), -100, -90, -80, -70, -60, -50, -40, -30, -20, -10, 0]
labels = ['< -100', '-100 to -90', '-90 to -80', '-80 to -70', '-70 to -60', '-60 to -50',
          '-50 to -40', '-40 to -30', '-30 to -20', '-20 to -10', '-10 to 0']
 
# Cut the data into categories using the bins
categories = pd.cut(filtered_data['PackCurr_6'], bins=bins, labels=labels, right=False)
 
# Add the category column to the filtered data
filtered_data['Category'] = categories
 
# Calculate the sum of 'PackCurr_6' values in each category
category_sums = filtered_data.groupby('Category')['PackCurr_6'].sum()
 
# Calculate the absolute sum for percentage calculation (ignoring signs since all values are negative)
total_sum = category_sums.abs().sum()
 
# Calculate the percentage each category contributes
percentages = (category_sums.abs() / total_sum * 100).reset_index(name='Percentage')
 
# Plotting the results
plt.figure(figsize=(10, 6))
bars = plt.bar(percentages['Category'], percentages['Percentage'], color='skyblue')
 
# Adding the percentage labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom')
 
plt.xlabel('Current Ranges (A)')
plt.ylabel('Percentage of Total Current (%)')
plt.title('Percentage Distribution of Pack Currents')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()