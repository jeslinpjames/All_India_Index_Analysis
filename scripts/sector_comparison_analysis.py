# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# File paths
data_path = Path("../output/all_india_index_with_growth_rates.csv")
output_path = Path("../output/")
output_path.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

# Load the data with growth rates
df = pd.read_csv(data_path, parse_dates=['Date'])

# Calculate average General Index by sector
sector_avg = df.groupby('Sector')['General index'].mean().reset_index()
sector_avg.columns = ['Sector', 'Average General Index']

# Plot average General Index across sectors
plt.figure(figsize=(10, 6))
plt.bar(sector_avg['Sector'], sector_avg['Average General Index'], color=['#4CAF50', '#FF5733', '#FFC300'])
plt.title("Average General Index by Sector")
plt.xlabel("Sector")
plt.ylabel("Average General Index")
plt.grid(True)
plt.savefig(output_path / "average_general_index_by_sector.png")
plt.show()

# Plot Monthly and Annual Growth Rates by Sector for trend comparison
plt.figure(figsize=(12, 6))
for sector in df['Sector'].unique():
    sector_data = df[df['Sector'] == sector]
    plt.plot(sector_data['Date'], sector_data['Monthly Growth Rate (%)'], label=f'{sector} - Monthly Growth', linestyle='-')
    plt.plot(sector_data['Date'], sector_data['Annual Growth Rate (%)'], label=f'{sector} - Annual Growth', linestyle='--')

plt.title("Monthly and Annual Growth Rates Comparison by Sector")
plt.xlabel("Date")
plt.ylabel("Growth Rate (%)")
plt.legend(title="Growth Rate Type")
plt.grid(True)
plt.savefig(output_path / "growth_rate_comparison_by_sector.png")
plt.show()

# Save the sector average data for documentation
sector_avg.to_csv(output_path / "sector_average_general_index.csv", index=False)
