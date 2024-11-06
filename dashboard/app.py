import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path  # Add this import statement

# Load the processed data
data_path = Path("output/csv/all_india_index_with_growth_rates.csv")
df = pd.read_csv(data_path, parse_dates=['Date'])

# Streamlit page configuration
st.set_page_config(page_title="All India Index Dashboard", layout="wide")

# Sidebar filters
st.sidebar.header("Filter Options")
sector = st.sidebar.selectbox("Select Sector", options=df['Sector'].unique())
category = st.sidebar.selectbox("Select Category", options=df.columns[3:-4])
time_frame = st.sidebar.slider("Select Time Range", min_value=int(df['Date'].dt.year.min()), 
                               max_value=int(df['Date'].dt.year.max()), value=(2015, 2023))

# Filter data based on selected options
filtered_data = df[(df['Sector'] == sector) & (df['Date'].dt.year.between(time_frame[0], time_frame[1]))]

# Display sector data overview
st.title(f"All India Index Dashboard - {sector} Sector")
st.write(f"Data range: {time_frame[0]} to {time_frame[1]}")

# General Index Trend
st.subheader("General Index Trend")
fig = px.line(filtered_data, x='Date', y='General index', title="General Index Over Time")
st.plotly_chart(fig, use_container_width=True)

# Category-specific Inflation Analysis
st.subheader(f"{category} Inflation Analysis")
filtered_data[f'{category} Monthly Inflation (%)'] = filtered_data[category].pct_change() * 100
filtered_data[f'{category} Annual Inflation (%)'] = filtered_data[category].pct_change(12) * 100

fig_monthly = px.line(filtered_data, x='Date', y=f'{category} Monthly Inflation (%)', title="Monthly Inflation")
fig_annual = px.line(filtered_data, x='Date', y=f'{category} Annual Inflation (%)', title="Annual Inflation")

st.plotly_chart(fig_monthly, use_container_width=True)
st.plotly_chart(fig_annual, use_container_width=True)

# Category Contribution to General Index
st.subheader(f"Category Contribution to General Index - {sector} Sector")
filtered_data[f'{category} Contribution (%)'] = (filtered_data[category] / filtered_data['General index']) * 100
fig_contrib = px.line(filtered_data, x='Date', y=f'{category} Contribution (%)', title="Category Contribution to General Index")
st.plotly_chart(fig_contrib, use_container_width=True)
