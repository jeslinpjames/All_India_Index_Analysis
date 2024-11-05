# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# File paths
data_path = Path("../output/processed_all_india_index.csv")
output_path = Path("../output/")
output_path.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

# Load the processed data with date column
df = pd.read_csv(data_path, parse_dates=['Date'])

# Sort data by date within each sector for calculating growth rates
df.sort_values(by=['Sector', 'Date'], inplace=True)

# Calculate Monthly Growth Rate for 'General index' within each sector
df['Monthly Growth Rate (%)'] = df.groupby('Sector')['General index'].pct_change() * 100

# Calculate Annual Growth Rate for 'General index' by comparing the same month in the previous year
df['Annual Growth Rate (%)'] = df.groupby(['Sector', df['Date'].dt.month])['General index'].pct_change(12) * 100

# Preview the data with growth rates
print("Data with Growth Rates:\n", df.head())

# Plot the growth rates for each sector
plt.figure(figsize=(12, 6))
for sector in df['Sector'].unique():
    sector_data = df[df['Sector'] == sector]
    plt.plot(sector_data['Date'], sector_data['Monthly Growth Rate (%)'], label=f'{sector} - Monthly Growth', marker='o', linestyle='-')
    plt.plot(sector_data['Date'], sector_data['Annual Growth Rate (%)'], label=f'{sector} - Annual Growth', marker='x', linestyle='--')

plt.title("All India Index - Monthly and Annual Growth Rates Over Time")
plt.xlabel("Date")
plt.ylabel("Growth Rate (%)")
plt.legend(title="Growth Rate Type")
plt.grid(True)
plt.savefig(output_path / "growth_rates_trend.png")  # Save plot to output folder
plt.show()

# Save the data with growth rates for further analysis
df.to_csv(output_path / "all_india_index_with_growth_rates.csv", index=False)
