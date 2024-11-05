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
    
    # Ensure all category columns are numeric; convert non-numeric values to NaN and then fill them
    sector_data[categories] = sector_data[categories].apply(pd.to_numeric, errors='coerce').fillna(method='ffill')
    sector_data['General index'] = pd.to_numeric(sector_data['General index'], errors='coerce').fillna(method='ffill')
    
    # Calculate percentage contribution for each category relative to the General Index
    for category in categories:
        sector_data[f'{category} Contribution (%)'] = (sector_data[category] / sector_data['General index']) * 100
    
    # Plot percentage contributions over time
    plt.figure(figsize=(14, 8))
    for category in categories:
        plt.plot(sector_data.index, sector_data[f'{category} Contribution (%)'], label=category, linestyle='-')
    
    plt.title(f"Percentage Contribution of Categories to General Index - {sector} Sector")
    plt.xlabel("Date")
    plt.ylabel("Contribution (%)")
    plt.legend(title="Categories", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path / f"{sector.lower()}_contribution_to_general_index.png")
    plt.show()
    
    # Calculate variance for each category to measure volatility
    variance_df = sector_data[categories].var()
    
    # Plot variance for each category
    plt.figure(figsize=(10, 6))
    variance_df.plot(kind='bar')
    plt.title(f"Variance of Categories within {sector} Sector")
    plt.xlabel("Category")
    plt.ylabel("Variance")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path / f"{sector.lower()}_category_variance.png")
    plt.show()
    
    # Save sector-specific data with contributions and variance analysis
    sector_data.to_csv(output_path / f"{sector.lower()}_composition_analysis.csv")
    variance_df.to_csv(output_path / f"{sector.lower()}_category_variance.csv", header=["Variance"])
