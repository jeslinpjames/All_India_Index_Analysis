import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path
from datetime import datetime

# File paths
data_path = Path("../output/csv/all_india_index_with_growth_rates.csv")
template_path = Path("templates/report_template.html")
output_html_path = Path("output/report.html")
output_pdf_path = Path("output/report.pdf")
chart_path = Path("output/general_index_chart.png")

# Load data
df = pd.read_csv(data_path, parse_dates=['Date'])

# Example Data Processing for Inflation Summary
sectors = df['Sector'].unique()
inflation_summary = {}

for sector in sectors:
    sector_data = df[df['Sector'] == sector]
    monthly_inflation = sector_data['General index'].pct_change().mean() * 100
    annual_inflation = sector_data['General index'].pct_change(12).mean() * 100
    inflation_summary[sector] = {"monthly": round(monthly_inflation, 2), "annual": round(annual_inflation, 2)}

# Plot General Index Trend
plt.figure(figsize=(10, 6))
for sector in sectors:
    sector_data = df[df['Sector'] == sector]
    plt.plot(sector_data['Date'], sector_data['General index'], label=sector)
plt.xlabel('Date')
plt.ylabel('General Index')
plt.title('General Index Trends')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(chart_path)
plt.close()

# Load Jinja2 template and render HTML
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(str(template_path))
html_out = template.render(
    generated_date=datetime.now().strftime('%Y-%m-%d'),
    inflation_summary=inflation_summary,
    general_index_chart=str(chart_path)
)

# Save HTML Report
with open(output_html_path, 'w') as f:
    f.write(html_out)

# Convert HTML to PDF
HTML(string=html_out).write_pdf(output_pdf_path)
print(f"Report generated at {output_pdf_path}")
