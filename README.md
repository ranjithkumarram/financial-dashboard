7# Financial Controlling Dashboard

A comprehensive financial performance monitoring dashboard built with Streamlit, featuring auto-generated financial data and interactive visualizations.

## 🚀 Enhanced Features

### 📊 Advanced Analytics
- **Multi-tab Interface**: Organized analytics with Trend Analysis, Department Performance, Financial Ratios, Advanced Analytics, and Cash Flow Dashboard tabs
- **Enhanced Visualizations**: Improved charts with better styling, hover effects, and professional design
- **Heatmap Analysis**: Monthly performance heatmap for quick insights
- **Correlation Matrix**: Understand relationships between financial metrics
- **Cash Flow Analysis**: Dedicated cash flow dashboard with operating, investing, and financing activities

### 🎛️ Improved Controls
- **Advanced Filtering**: Enhanced sidebar with additional options like forecast display and anomaly detection
- **Scenario Analysis**: Interactive sliders for revenue and expense what-if analysis
- **Trend Indicators**: Metrics now show percentage changes compared to previous period
- **Department Analysis**: Detailed department-wise performance tracking

### 📈 Professional Design
- **Custom CSS Styling**: Professional gradient cards and improved typography
- **Responsive Layout**: Optimized for different screen sizes
- **Color-coded Metrics**: Visual indicators for positive/negative changes
- **Scenario Indicators**: Visual feedback when scenario analysis is active

### 📥 Enhanced Data Management
- **Multiple Export Options**: Download both main and department data separately
- **Detailed Data Views**: Expandable raw data sections with formatted numbers
- **Data Summary**: Quick overview of selected data period and scope
- **Budget Variance Analysis**: Compare actual performance against budget targets

### 💰 Advanced Financial Metrics
- **EBITDA Margin**: Operating performance metric excluding financing and depreciation effects
- **Cash Conversion Cycle**: Working capital efficiency metrics
- **Operating Cash Flow Ratio**: Short-term solvency measurement
- **Quick Ratio**: More conservative liquidity measurement
- **Variance Analysis**: Actual vs Budget performance tracking
- **Industry Benchmarking**: Compare against industry averages

## Key Features

- 📊 **Real-time Financial Metrics**: Track revenue, expenses, profit, and profit margin with trend indicators
- 📈 **Interactive Charts**: Enhanced line charts, bar charts, pie charts with professional styling
- 🎯 **Financial Ratios**: Expanded KPIs with industry averages and target comparisons
- 🔍 **Advanced Filtering**: Multiple filter options including forecast and anomaly detection
- 📥 **Dual Data Export**: Download both main financial data and department data
- 💰 **Auto-generated Data**: Realistic financial data generation for demonstration

## Installation

1. Clone or download this project
2. Navigate to the project directory:
   ```bash
   cd financial-dashboard
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard

### Method 1: Manual commands
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the application:
   ```bash
   streamlit run app.py
   ```

### Method 2: Using run script (Windows)
- Double-click `run.bat` or run it from command prompt

The dashboard will open in your default web browser at `http://localhost:8501`

## Dashboard Components

### Key Metrics
- Total Revenue
- Total Expenses  
- Total Profit
- Average Profit Margin

### Visualizations
- Revenue vs Expenses Trend Chart
- Profit Margin Trend Chart
- Department Performance Analysis
- Revenue Distribution by Department

### Financial Ratios
- Gross Profit Margin
- Operating Margin  
- Expense Ratio
- Revenue Growth (Month-over-Month)

## Data Source

This dashboard uses auto-generated financial data that includes:
- Monthly financial data for the past 12 months
- Department-wise breakdown (Sales, Marketing, R&D, Operations, Administration)
- Realistic seasonal patterns and trends
- Random variations to simulate real-world data

## Customization

To use real data instead of auto-generated data:
1. Replace the `generate_financial_data()` function in `app.py`
2. Connect to your database or CSV files
3. Format the data to match the expected structure

## Deployment

This dashboard can be deployed on:
- Streamlit Cloud
- Heroku
- AWS/Azure/GCP
- Any platform that supports Python applications

## Dependencies

- streamlit==1.28.0
- pandas==2.0.3
- numpy==1.24.3
- plotly==5.15.0
- streamlit-extras==0.3.0

## License

MIT License - Feel free to use and modify for your financial controlling needs.