import pandas as pd
import matplotlib.pyplot as plt

# Load the new data from the CSV file
file_path = r"C:\Users\annmon.james\Downloads\City_LXS_G_2.0_Latest_final_4.csv"
data = pd.read_csv(file_path)

# Define the bins and labels for categorization
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, float('inf')]
labels = ['0 to 10', '10 to 20', '20 to 30', '30 to 40', '40 to 50', '50 to 60', '60 to 70',
          '70 to 80', '80 to 90', '90 to 100', '> 100']

# Cut the data into categories using the bins
categories = pd.cut(data['Current_value'], bins=bins, labels=labels, right=False)

# Add the category column to the data
data['Category'] = categories

# Calculate the sum of 'Current_value' values in each category
category_sums = data.groupby('Category')['Current_value'].sum()

# Calculate the absolute sum for percentage calculation
total_sum = category_sums.abs().sum()

# Calculate the percentage each category contributes
percentages = (category_sums.abs() / total_sum * 100).reset_index(name='Percentage')

# Plotting the results
plt.figure(figsize=(12, 7))
bars = plt.bar(percentages['Category'], percentages['Percentage'], color='skyblue')

# Adding the percentage labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f"{round(yval, 2)}%", ha='center', va='bottom')

plt.xlabel('Current Value Ranges (A)')
plt.ylabel('Percentage of Total Current (%)')
plt.title('Percentage Distribution of Current Values')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
