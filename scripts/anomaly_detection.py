# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# File paths
data_path = Path("../output/all_india_index_with_growth_rates.csv")
output_path = Path("../output/")
output_path.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

# Load the data with growth rates
df = pd.read_csv(data_path, parse_dates=['Date'])

# Identify Outliers using Z-score for 'General index' within each sector
df['Z-score'] = df.groupby('Sector')['General index'].transform(lambda x: (x - x.mean()) / x.std())
df['Outlier'] = df['Z-score'].apply(lambda z: 'Yes' if abs(z) > 3 else 'No')  # Mark as outlier if |Z-score| > 3

# Save outlier data
outliers = df[df['Outlier'] == 'Yes']
outliers.to_csv(output_path / "outliers_general_index.csv", index=False)

# Plot outliers for each sector
plt.figure(figsize=(12, 6))
for sector in df['Sector'].unique():
    sector_data = df[df['Sector'] == sector]
    plt.plot(sector_data['Date'], sector_data['General index'], label=sector, linestyle='-', marker='o')
    outlier_dates = sector_data[sector_data['Outlier'] == 'Yes']['Date']
    outlier_values = sector_data[sector_data['Outlier'] == 'Yes']['General index']
    plt.scatter(outlier_dates, outlier_values, color='red', label=f'{sector} Outliers')

plt.title("All India Index - Outliers in General Index by Sector")
plt.xlabel("Date")
plt.ylabel("General Index")
plt.legend(title="Sector")
plt.grid(True)
plt.savefig(output_path / "general_index_outliers.png")
plt.show()

# Volatility Analysis: Calculate rolling standard deviation (e.g., 3-month window) for volatility measure
df['Volatility'] = df.groupby('Sector')['General index'].transform(lambda x: x.rolling(window=3).std())

# Plot Volatility over time
plt.figure(figsize=(12, 6))
for sector in df['Sector'].unique():
    sector_data = df[df['Sector'] == sector]
    plt.plot(sector_data['Date'], sector_data['Volatility'], label=f"{sector} - 3-Month Volatility", linestyle='-')

plt.title("All India Index - Volatility (Rolling Standard Deviation)")
plt.xlabel("Date")
plt.ylabel("Volatility (3-Month Rolling Std Dev)")
plt.legend(title="Sector")
plt.grid(True)
plt.savefig(output_path / "general_index_volatility.png")
plt.show()

# Save data with outliers and volatility for documentation
df.to_csv(output_path / "all_india_index_with_outliers_and_volatility.csv", index=False)
