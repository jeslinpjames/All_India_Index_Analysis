# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# File paths
data_path = Path("../output/csv/all_india_index_with_growth_rates.csv")
csv_output_path = Path("../output/csv/")
graphs_output_path = Path("../output/graphs/")
csv_output_path.mkdir(parents=True, exist_ok=True)      # Ensure csv output directory exists
graphs_output_path.mkdir(parents=True, exist_ok=True)   # Ensure graphs output directory exists

# Load the processed data
df = pd.read_csv(data_path, parse_dates=['Date'])

# List of categories excluding 'General index' and other non-numeric columns
categories = df.columns[3:-4]

# Calculate Monthly and Annual Inflation Rates
for sector in df['Sector'].unique():
    sector_data = df[df['Sector'] == sector].set_index('Date')
    
    # Convert all category columns and General Index to numeric, coercing errors to NaN, then forward fill to handle any gaps
    sector_data[categories] = sector_data[categories].apply(pd.to_numeric, errors='coerce').fillna(method='ffill')
    sector_data['General index'] = pd.to_numeric(sector_data['General index'], errors='coerce').fillna(method='ffill')
    
    # Monthly inflation rate for General Index and each category
    for category in ['General index'] + categories.tolist():
        sector_data[f'{category} Monthly Inflation (%)'] = sector_data[category].pct_change() * 100
    
    # Annual inflation rate (year-over-year change)
    for category in ['General index'] + categories.tolist():
        sector_data[f'{category} Annual Inflation (%)'] = sector_data[category].pct_change(12) * 100
    
    # Plot General Index Inflation (Monthly and Annual)
    plt.figure(figsize=(12, 6))
    plt.plot(sector_data.index, sector_data['General index Monthly Inflation (%)'], label='Monthly Inflation', linestyle='-')
    plt.plot(sector_data.index, sector_data['General index Annual Inflation (%)'], label='Annual Inflation', linestyle='--')
    plt.title(f"Inflation Rate of General Index - {sector} Sector")
    plt.xlabel("Date")
    plt.ylabel("Inflation Rate (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(graphs_output_path / f"{sector.lower()}_general_index_inflation.png")
    plt.show()
    
    # Identify highest inflationary categories on average (based on Annual Inflation)
    average_annual_inflation = sector_data[[f'{category} Annual Inflation (%)' for category in categories]].mean().sort_values(ascending=False)
    
    # Plot average annual inflation by category
    plt.figure(figsize=(10, 6))
    average_annual_inflation.plot(kind='bar', color='orange')
    plt.title(f"Average Annual Inflation by Category - {sector} Sector")
    plt.xlabel("Category")
    plt.ylabel("Average Annual Inflation (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(graphs_output_path / f"{sector.lower()}_category_inflation.png")
    plt.show()
    
    # Save inflation data for further analysis
    sector_data.to_csv(csv_output_path / f"{sector.lower()}_inflation_data.csv")
    average_annual_inflation.to_csv(csv_output_path / f"{sector.lower()}_average_annual_inflation.csv", header=["Average Annual Inflation (%)"])
