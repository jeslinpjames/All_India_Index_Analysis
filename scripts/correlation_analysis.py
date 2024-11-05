# Import required libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# File paths
data_path = Path("../output/all_india_index_with_growth_rates.csv")
output_path = Path("../output/")
output_path.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

# Load the data with growth rates
df = pd.read_csv(data_path, parse_dates=['Date'])

# Select numerical columns for correlation (all categories except 'Date', 'Sector', 'Year', 'Month')
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
numeric_columns.remove("General index")  # Remove 'General index' as we focus on component relationships

# Calculate and plot correlation matrix for each sector
for sector in df['Sector'].unique():
    sector_data = df[df['Sector'] == sector]
    
    # Calculate correlation matrix
    correlation_matrix = sector_data[numeric_columns].corr()
    
    # Plot correlation heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title(f"Correlation Matrix of Index Components - {sector} Sector")
    plt.savefig(output_path / f"{sector.lower()}_sector_correlation_matrix.png")
    plt.show()

    # Save correlation matrix to CSV
    correlation_matrix.to_csv(output_path / f"{sector.lower()}_sector_correlation_matrix.csv")

# Optional: Calculate lagged correlations if needed (e.g., 1-month lag for specific components)
