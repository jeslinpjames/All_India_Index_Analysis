# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# File paths
data_path = Path("../output/all_india_index_with_growth_rates.csv")
output_path = Path("../output/")
output_path.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

# Load the processed data
df = pd.read_csv(data_path, parse_dates=['Date'])

# List of categories excluding 'General index' and other non-numeric columns
categories = df.columns[3:-4]

# Sector-specific analysis for each category
for sector in df['Sector'].unique():
    sector_data = df[df['Sector'] == sector].set_index('Date')
    
    # Ensure all categories are numeric and fill any NaN values with forward fill method
    sector_data[categories] = sector_data[categories].apply(pd.to_numeric, errors='coerce').fillna(method='ffill')
    
    # Plot each category within the sector
    plt.figure(figsize=(14, 8))
    for category in categories:
        plt.plot(sector_data.index, sector_data[category], label=category, linestyle='-')
    
    plt.title(f"Category Trends within {sector} Sector")
    plt.xlabel("Date")
    plt.ylabel("Index Value")
    plt.legend(title="Categories", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path / f"{sector.lower()}_category_trends.png")
    plt.show()
    
    # Save sector-specific category data for further analysis
    sector_data.to_csv(output_path / f"{sector.lower()}_category_data.csv")
