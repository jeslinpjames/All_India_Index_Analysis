# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pathlib import Path

# File paths
data_path = Path("../output/all_india_index_with_growth_rates.csv")
output_path = Path("../output/")
output_path.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

# Load the processed data with Date column
df = pd.read_csv(data_path, parse_dates=['Date'])

# Forecasting for each sector
forecast_steps = 12  # Forecast for the next 12 months
for sector in df['Sector'].unique():
    # Filter data for each sector and set Date as index
    sector_data = df[df['Sector'] == sector].set_index('Date')['General index']
    
    # Ensure data is in a continuous monthly frequency
    sector_data = sector_data.asfreq('MS').fillna(method='ffill')
    
    # Fit ARIMA model
    model = ARIMA(sector_data, order=(1, 1, 1))
    model_fit = model.fit()
    
    # Forecast
    forecast = model_fit.forecast(steps=forecast_steps)
    forecast_dates = pd.date_range(start=sector_data.index[-1] + pd.DateOffset(months=1), periods=forecast_steps, freq='MS')
    forecast_series = pd.Series(forecast, index=forecast_dates)
    
    # Plot actual data and forecast
    plt.figure(figsize=(12, 6))
    plt.plot(sector_data, label="Historical Data")
    plt.plot(forecast_series, label="Forecast", linestyle="--")
    plt.title(f"Forecast of General Index for {sector} Sector (Next 12 Months)")
    plt.xlabel("Date")
    plt.ylabel("General Index")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path / f"{sector.lower()}_forecast.png")
    plt.show()
    
    # Save forecast data to CSV
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecasted General Index': forecast})
    forecast_df.to_csv(output_path / f"{sector.lower()}_forecast.csv", index=False)
