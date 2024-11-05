# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# File paths
data_path = Path("../data/All_India_Index_Upto_Nov23.csv")
output_path = Path("../output/")
output_path.mkdir(parents=True, exist_ok=True)  # Create output directory if it doesn't exist

# Load the data
df = pd.read_csv(data_path)

# Preview the data structure
print("Data Preview:\n", df.head())

# Combine 'Year' and 'Month' columns to create a 'Date' column
df['Date'] = pd.to_datetime(df['Year'].astype(str) + ' ' + df['Month'], format='%Y %B', errors='coerce')

# Check for any rows with invalid dates (if any)
invalid_dates = df[df['Date'].isna()]
if not invalid_dates.empty:
    print("Rows with invalid dates found and will be handled:", invalid_dates)

# Drop rows with invalid dates, if any
df.dropna(subset=['Date'], inplace=True)

# Sort data by date
df.sort_values(by='Date', inplace=True)

# Plot the time series trend for 'General index' (or any other column of interest)
plt.figure(figsize=(12, 6))
for sector in df['Sector'].unique():
    sector_data = df[df['Sector'] == sector]
    plt.plot(sector_data['Date'], sector_data['General index'], label=sector, marker='o', linestyle='-')

plt.title("All India Index - Trend Over Time")
plt.xlabel("Date")
plt.ylabel("General Index Value")
plt.legend(title="Sector")
plt.grid(True)
plt.savefig(output_path / "all_india_index_trend.png")  # Save plot to output folder
plt.show()

# Save processed data for further analysis
df.to_csv(output_path / "processed_all_india_index.csv", index=False)
