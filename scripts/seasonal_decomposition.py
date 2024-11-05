# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pathlib import Path

# File paths
data_path = Path("../output/all_india_index_with_growth_rates.csv")
output_path = Path("../output/")
output_path.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

# Load the processed data with Date column
df = pd.read_csv(data_path, parse_dates=['Date'])

# Drop rows where 'General index' is missing for initial data cleanup
df = df.dropna(subset=['General index'])

# Identify any remaining missing values by date
missing_summary = df.isna().sum()
print("Remaining missing values by column:\n", missing_summary)

# Perform seasonal decomposition for each sector
for sector in df['Sector'].unique():
    sector_data = df[df['Sector'] == sector].set_index('Date')
    
    # Ensure data is indexed by date and frequency is monthly
    sector_data = sector_data.asfreq('ME')
    
    # Linear interpolation for minor missing data
    sector_data['General index'] = sector_data['General index'].interpolate(method='linear')
    
    # Fill any remaining missing values with the mean as a last resort
    if sector_data['General index'].isna().any():
        sector_data['General index'].fillna(sector_data['General index'].mean(), inplace=True)
    
    # Confirm no missing values remain
    if sector_data['General index'].isna().any():
        raise ValueError(f"Missing values still remain in {sector} sector after filling methods.")
    
    # Perform seasonal decomposition on 'General index'
    decomposition = seasonal_decompose(sector_data['General index'], model='additive', period=12)
    
    # Plot decomposition
    plt.figure(figsize=(10, 8))
    decomposition.plot()
    plt.suptitle(f"Seasonal Decomposition of General Index - {sector} Sector", y=1.05)
    plt.savefig(output_path / f"{sector.lower()}_seasonal_decomposition.png")
    plt.show()
    
    # Save each component (trend, seasonal, resid) for further analysis if needed
    sector_data['Trend'] = decomposition.trend
    sector_data['Seasonal'] = decomposition.seasonal
    sector_data['Residual'] = decomposition.resid
    sector_data.to_csv(output_path / f"{sector.lower()}_decomposed_data.csv")
