import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import calendar
from streamlit_extras.metric_cards import style_metric_cards

# Set page configuration
st.set_page_config(
    page_title="Financial Controlling Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Format numbers with K and M abbreviations
def format_currency(value):
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.1f}K"
    else:
        return f"${value:,.0f}"

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #1f77b4 !important;
        margin-bottom: 0.5rem !important;
    }
    .sub-header {
        font-size: 1.2rem !important;
        color: #666 !important;
        margin-bottom: 2rem !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        text-align: center;
    }
    .positive-change {
        color: #2E8B57 !important;
        font-weight: bold;
    }
    .negative-change {
        color: #DC143C !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Generate enhanced financial data with budget and cash flow components
def generate_financial_data():
    np.random.seed(42)
    
    # Generate dates for the last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start_date, end_date, freq='M')
    
    # Generate revenue data with seasonal pattern
    base_revenue = 1000000
    revenue_trend = np.linspace(0.9, 1.2, len(dates))
    seasonal_factor = np.sin(np.linspace(0, 4*np.pi, len(dates))) * 0.1 + 1
    revenue = base_revenue * revenue_trend * seasonal_factor * np.random.normal(1, 0.05, len(dates))
    
    # Generate budget data (5-10% higher than actual for variance analysis)
    budget_revenue = revenue * np.random.uniform(1.05, 1.1, len(dates))
    
    # Generate expense data (60-70% of revenue)
    expense_ratio = np.random.uniform(0.6, 0.7, len(dates))
    expenses = revenue * expense_ratio * np.random.normal(1, 0.03, len(dates))
    budget_expenses = expenses * np.random.uniform(0.95, 1.0, len(dates))
    
    # Calculate profit
    profit = revenue - expenses
    budget_profit = budget_revenue - budget_expenses
    
    # Generate cash flow data
    operating_cash_flow = profit * np.random.uniform(0.8, 1.2, len(dates))
    investing_cash_flow = -expenses * np.random.uniform(0.1, 0.3, len(dates))
    financing_cash_flow = profit * np.random.uniform(-0.2, 0.2, len(dates))
    net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
    
    # Generate working capital metrics
    current_assets = revenue * np.random.uniform(0.3, 0.5, len(dates))
    current_liabilities = expenses * np.random.uniform(0.2, 0.4, len(dates))
    
    # Generate department-wise data
    departments = ['Sales', 'Marketing', 'R&D', 'Operations', 'Administration']
    dept_data = []
    for i, date in enumerate(dates):
        for dept in departments:
            dept_revenue = revenue[i] * np.random.uniform(0.1, 0.3)
            dept_expenses = expenses[i] * np.random.uniform(0.15, 0.25)
            dept_budget_revenue = dept_revenue * np.random.uniform(1.05, 1.1)
            dept_budget_expenses = dept_expenses * np.random.uniform(0.95, 1.0)
            dept_data.append({
                'Date': date,
                'Department': dept,
                'Revenue': dept_revenue,
                'Expenses': dept_expenses,
                'Profit': dept_revenue - dept_expenses,
                'Budget_Revenue': dept_budget_revenue,
                'Budget_Expenses': dept_budget_expenses,
                'Budget_Profit': dept_budget_revenue - dept_budget_expenses
            })
    
    # Create main dataframe
    main_df = pd.DataFrame({
        'Date': dates,
        'Revenue': revenue,
        'Expenses': expenses,
        'Profit': profit,
        'Profit Margin': profit / revenue,
        'Budget_Revenue': budget_revenue,
        'Budget_Expenses': budget_expenses,
        'Budget_Profit': budget_profit,
        'Budget_Profit_Margin': budget_profit / budget_revenue,
        'Operating_Cash_Flow': operating_cash_flow,
        'Investing_Cash_Flow': investing_cash_flow,
        'Financing_Cash_Flow': financing_cash_flow,
        'Net_Cash_Flow': net_cash_flow,
        'Current_Assets': current_assets,
        'Current_Liabilities': current_liabilities,
        'Month': dates.strftime('%B %Y')
    })
    
    # Create department dataframe
    dept_df = pd.DataFrame(dept_data)
    dept_df['Month'] = dept_df['Date'].dt.strftime('%B %Y')
    
    return main_df, dept_df

# Load data
main_df, dept_df = generate_financial_data()

# Sidebar with enhanced filters
st.sidebar.header("🎛️ Dashboard Controls")
st.sidebar.markdown("---")

# Time period filter
time_period = st.sidebar.selectbox(
    "📅 Time Period",
    ["Last 3 Months", "Last 6 Months", "Last 12 Months", "All Time"],
    index=2
)

# Department filter
department_filter = st.sidebar.multiselect(
    "🏢 Departments",
    options=dept_df['Department'].unique(),
    default=dept_df['Department'].unique()
)

# Additional filters
show_forecast = st.sidebar.checkbox("📈 Show 3-month Forecast", value=True)
show_anomalies = st.sidebar.checkbox("🔍 Highlight Anomalies", value=True)

# Scenario analysis controls
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Scenario Analysis")
revenue_scenario = st.sidebar.slider(
    "Revenue Change (%)",
    min_value=-20,
    max_value=20,
    value=0,
    help="Simulate revenue changes"
)
expense_scenario = st.sidebar.slider(
    "Expense Change (%)",
    min_value=-20,
    max_value=20,
    value=0,
    help="Simulate expense optimization"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 Use filters to customize your financial analysis")

# Filter data based on selections
if time_period == "Last 3 Months":
    filtered_main = main_df[main_df['Date'] >= main_df['Date'].max() - timedelta(days=90)]
    filtered_dept = dept_df[dept_df['Date'] >= dept_df['Date'].max() - timedelta(days=90)]
elif time_period == "Last 6 Months":
    filtered_main = main_df[main_df['Date'] >= main_df['Date'].max() - timedelta(days=180)]
    filtered_dept = dept_df[dept_df['Date'] >= dept_df['Date'].max() - timedelta(days=180)]
elif time_period == "Last 12 Months":
    filtered_main = main_df
    filtered_dept = dept_df
else:
    filtered_main = main_df
    filtered_dept = dept_df

filtered_dept = filtered_dept[filtered_dept['Department'].isin(department_filter)]

# Apply scenario analysis
if revenue_scenario != 0:
    filtered_main = filtered_main.copy()
    filtered_main['Revenue'] = filtered_main['Revenue'] * (1 + revenue_scenario / 100)
    filtered_main['Profit'] = filtered_main['Revenue'] - filtered_main['Expenses']
    filtered_main['Profit Margin'] = filtered_main['Profit'] / filtered_main['Revenue']

if expense_scenario != 0:
    filtered_main = filtered_main.copy()
    filtered_main['Expenses'] = filtered_main['Expenses'] * (1 + expense_scenario / 100)
    filtered_main['Profit'] = filtered_main['Revenue'] - filtered_main['Expenses']
    filtered_main['Profit Margin'] = filtered_main['Profit'] / filtered_main['Revenue']

# Main dashboard
st.markdown('<h1 class="main-header">💰 Financial Controlling Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Financial Performance Monitoring & Analytics</p>', unsafe_allow_html=True)

# Show scenario info if active
if revenue_scenario != 0 or expense_scenario != 0:
    st.info(f"📊 **Scenario Active:** Revenue {revenue_scenario:+.0f}%, Expenses {expense_scenario:+.0f}%")

# Enhanced key metrics with trends
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = filtered_main['Revenue'].sum()
    prev_revenue = main_df[main_df['Date'] < filtered_main['Date'].min()]['Revenue'].sum() if len(filtered_main) > 0 else total_revenue
    revenue_change = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
    st.metric("Total Revenue", format_currency(total_revenue), f"{revenue_change:+.1f}%")

with col2:
    total_expenses = filtered_main['Expenses'].sum()
    prev_expenses = main_df[main_df['Date'] < filtered_main['Date'].min()]['Expenses'].sum() if len(filtered_main) > 0 else total_expenses
    expenses_change = ((total_expenses - prev_expenses) / prev_expenses * 100) if prev_expenses > 0 else 0
    st.metric("Total Expenses", format_currency(total_expenses), f"{expenses_change:+.1f}%")

with col3:
    total_profit = filtered_main['Profit'].sum()
    prev_profit = main_df[main_df['Date'] < filtered_main['Date'].min()]['Profit'].sum() if len(filtered_main) > 0 else total_profit
    profit_change = ((total_profit - prev_profit) / prev_profit * 100) if prev_profit > 0 else 0
    st.metric("Total Profit", format_currency(total_profit), f"{profit_change:+.1f}%")

with col4:
    avg_margin = filtered_main['Profit Margin'].mean() * 100
    prev_margin = main_df[main_df['Date'] < filtered_main['Date'].min()]['Profit Margin'].mean() * 100 if len(filtered_main) > 0 else avg_margin
    margin_change = avg_margin - prev_margin
    st.metric("Avg Profit Margin", f"{avg_margin:.1f}%", f"{margin_change:+.1f}%")

# Style metric cards
style_metric_cards()

# Performance overview section
st.markdown("---")
st.subheader("📊 Performance Overview")

# Enhanced charts with multiple visualizations including Cash Flow
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Trend Analysis", "Department Performance", "Financial Ratios", "Advanced Analytics", "Cash Flow Dashboard"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue vs Expenses Trend")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=filtered_main['Date'], y=filtered_main['Revenue'], 
                                name='Revenue', line=dict(color='#2E8B57', width=3)))
        fig1.add_trace(go.Scatter(x=filtered_main['Date'], y=filtered_main['Expenses'], 
                                name='Expenses', line=dict(color='#DC143C', width=3)))
        fig1.update_layout(
            height=400,
            hovermode='x unified',
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Profit Margin Trend")
        fig2 = px.line(filtered_main, x='Date', y='Profit Margin',
                      title='', labels={'Profit Margin': 'Profit Margin (%)'})
        fig2.update_traces(line=dict(color='#4169E1', width=3))
        fig2.update_layout(
            height=400, 
            yaxis_tickformat=".1%",
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        dept_summary = filtered_dept.groupby('Department').agg({
            'Revenue': 'sum',
            'Expenses': 'sum',
            'Profit': 'sum'
        }).reset_index()
        
        st.subheader("Profit by Department")
        fig3 = px.bar(dept_summary, x='Department', y='Profit',
                     title='', color='Profit',
                     color_continuous_scale='Viridis')
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.subheader("Revenue Distribution")
        fig4 = px.pie(dept_summary, values='Revenue', names='Department',
                     title='', hole=0.3)
        fig4.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    # Enhanced financial ratios with advanced metrics
    latest_data = filtered_main.iloc[-1] if len(filtered_main) > 0 else main_df.iloc[-1]
    
    # Calculate additional advanced ratios
    ebitda_margin = latest_data['Profit'] / latest_data['Revenue']  # Simplified EBITDA
    current_ratio = latest_data['Current_Assets'] / latest_data['Current_Liabilities'] if latest_data['Current_Liabilities'] > 0 else 0
    quick_ratio = (latest_data['Current_Assets'] * 0.7) / latest_data['Current_Liabilities'] if latest_data['Current_Liabilities'] > 0 else 0
    operating_cash_flow_ratio = latest_data['Operating_Cash_Flow'] / latest_data['Current_Liabilities'] if latest_data['Current_Liabilities'] > 0 else 0
    
    # Calculate variance metrics
    revenue_variance = (latest_data['Revenue'] - latest_data['Budget_Revenue']) / latest_data['Budget_Revenue'] if latest_data['Budget_Revenue'] > 0 else 0
    expense_variance = (latest_data['Expenses'] - latest_data['Budget_Expenses']) / latest_data['Budget_Expenses'] if latest_data['Budget_Expenses'] > 0 else 0
    
    ratios_data = {
        'Ratio': [
            'Gross Profit Margin',
            'Operating Margin',
            'EBITDA Margin',
            'Expense Ratio',
            'Revenue Growth (MoM)',
            'Return on Investment',
            'Current Ratio',
            'Quick Ratio',
            'Operating Cash Flow Ratio',
            'Revenue Variance',
            'Expense Variance'
        ],
        'Value': [
            latest_data['Profit Margin'],
            latest_data['Profit'] / latest_data['Revenue'],
            ebitda_margin,
            latest_data['Expenses'] / latest_data['Revenue'],
            (filtered_main['Revenue'].iloc[-1] / filtered_main['Revenue'].iloc[-2] - 1) if len(filtered_main) > 1 else 0,
            latest_data['Profit'] / latest_data['Expenses'] if latest_data['Expenses'] > 0 else 0,
            current_ratio,
            quick_ratio,
            operating_cash_flow_ratio,
            revenue_variance,
            expense_variance
        ],
        'Target': [0.25, 0.20, 0.22, 0.65, 0.05, 0.3, 2.0, 1.5, 1.2, 0.0, 0.0],
        'Industry Avg': [0.22, 0.18, 0.20, 0.68, 0.04, 0.25, 1.8, 1.3, 1.0, -0.05, 0.03]
    }
    
    ratios_df = pd.DataFrame(ratios_data)
    ratios_df['Status'] = ratios_df.apply(
        lambda x: '✅ Good' if (x['Ratio'] in ['Revenue Variance', 'Expense Variance'] and abs(x['Value']) <= 0.05)
                  or (x['Ratio'] not in ['Revenue Variance', 'Expense Variance'] and x['Value'] >= x['Target'])
                  else '⚠️ Needs Attention', axis=1
    )
    
    st.subheader("Advanced Financial Ratios Analysis")
    st.dataframe(ratios_df.style.format({
        'Value': lambda x: '{:.1%}'.format(x) if isinstance(x, float) and abs(x) < 1 else '{:.2f}'.format(x),
        'Target': lambda x: '{:.1%}'.format(x) if isinstance(x, float) and abs(x) < 1 else '{:.2f}'.format(x),
        'Industry Avg': lambda x: '{:.1%}'.format(x) if isinstance(x, float) and abs(x) < 1 else '{:.2f}'.format(x)
    }), use_container_width=True, height=500)
    
    # Ratio performance chart
    fig_ratios = px.bar(ratios_df, x='Ratio', y='Value',
                       title='Financial Ratios vs Targets',
                       color='Status', color_discrete_map={'✅ Good': '#2E8B57', '⚠️ Needs Attention': '#DC143C'})
    fig_ratios.add_hline(y=0.25, line_dash="dash", line_color="red", annotation_text="Target Line")
    fig_ratios.update_layout(height=500, xaxis_tickangle=45)
    st.plotly_chart(fig_ratios, use_container_width=True)

with tab4:
    st.subheader("Advanced Analytics")
    
    # Monthly performance heatmap
    monthly_data = filtered_main.copy()
    monthly_data['Year'] = monthly_data['Date'].dt.year
    monthly_data['Month'] = monthly_data['Date'].dt.month
    
    heatmap_data = monthly_data.pivot_table(
        values='Profit Margin',
        index='Year',
        columns='Month',
        aggfunc='mean'
    ).fillna(0)
    
    # Ensure we have all 12 months for proper display
    all_months = list(range(1, 13))
    for month in all_months:
        if month not in heatmap_data.columns:
            heatmap_data[month] = 0
    
    # Reorder columns to ensure proper month order
    heatmap_data = heatmap_data[all_months]
    
    fig_heatmap = px.imshow(heatmap_data,
                          labels=dict(x="Month", y="Year", color="Profit Margin"),
                          x=[calendar.month_abbr[i] for i in all_months],
                          title="Monthly Profit Margin Heatmap",
                          color_continuous_scale="Viridis")
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Correlation analysis
    st.subheader("Financial Metrics Correlation")
    corr_matrix = filtered_main[['Revenue', 'Expenses', 'Profit', 'Profit Margin']].corr()
    fig_corr = px.imshow(corr_matrix, 
                        text_auto=True, 
                        aspect="auto",
                        title="Correlation Matrix",
                        color_continuous_scale="RdBu_r")
    st.plotly_chart(fig_corr, use_container_width=True)

with tab5:
    st.subheader("💰 Cash Flow Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cash flow components
        latest_cash_flow = filtered_main.iloc[-1] if len(filtered_main) > 0 else main_df.iloc[-1]
        cash_flow_data = {
            'Category': ['Operating', 'Investing', 'Financing'],
            'Amount': [
                latest_cash_flow['Operating_Cash_Flow'],
                latest_cash_flow['Investing_Cash_Flow'],
                latest_cash_flow['Financing_Cash_Flow']
            ]
        }
        
        fig_cash_flow = px.bar(cash_flow_data, x='Category', y='Amount',
                              title='Cash Flow Components',
                              color='Category',
                              color_discrete_map={
                                  'Operating': '#2E8B57',
                                  'Investing': '#4169E1',
                                  'Financing': '#FFA500'
                              })
        fig_cash_flow.update_layout(height=400)
        st.plotly_chart(fig_cash_flow, use_container_width=True)
    
    with col2:
        # Net cash flow trend
        fig_net_cash = px.line(filtered_main, x='Date', y='Net_Cash_Flow',
                              title='Net Cash Flow Trend',
                              labels={'Net_Cash_Flow': 'Net Cash Flow ($)'})
        fig_net_cash.update_traces(line=dict(color='#DC143C', width=3))
        fig_net_cash.update_layout(height=400)
        st.plotly_chart(fig_net_cash, use_container_width=True)
    
    # Cash flow metrics
    st.subheader("📊 Cash Flow Metrics")
    cash_col1, cash_col2, cash_col3, cash_col4 = st.columns(4)
    
    with cash_col1:
        avg_operating_cf = filtered_main['Operating_Cash_Flow'].mean()
        st.metric("Avg Operating CF", format_currency(avg_operating_cf))
    
    with cash_col2:
        avg_net_cf = filtered_main['Net_Cash_Flow'].mean()
        st.metric("Avg Net CF", format_currency(avg_net_cf))
    
    with cash_col3:
        cash_conversion = (filtered_main['Operating_Cash_Flow'] / filtered_main['Revenue']).mean() * 100
        st.metric("Cash Conversion (%)", f"{cash_conversion:.1f}%")
    
    with cash_col4:
        current_ratio_avg = filtered_main['Current_Assets'].mean() / filtered_main['Current_Liabilities'].mean()
        st.metric("Avg Current Ratio", f"{current_ratio_avg:.2f}")

# Data export and additional features
st.markdown("---")
st.subheader("📥 Data Management")

col1, col2 = st.columns(2)

with col1:
    # Enhanced download options
    csv_main = filtered_main.to_csv(index=False)
    csv_dept = filtered_dept.to_csv(index=False)
    
    st.download_button(
        label="📊 Download Main Data (CSV)",
        data=csv_main,
        file_name="financial_main_data.csv",
        mime="text/csv",
        key="main_csv"
    )
    
    st.download_button(
        label="🏢 Download Department Data (CSV)",
        data=csv_dept,
        file_name="financial_department_data.csv",
        mime="text/csv",
        key="dept_csv"
    )

with col2:
    # Data summary
    st.info("""
    **Data Summary:**
    - Period: {} to {}
    - Total Records: {}
    - Departments: {}
    """.format(
        filtered_main['Date'].min().strftime('%Y-%m-%d'),
        filtered_main['Date'].max().strftime('%Y-%m-%d'),
        len(filtered_main),
        len(department_filter)
    ))

# Raw data view with enhanced options
if st.checkbox("🔍 Show Detailed Data View"):
    st.subheader("Detailed Financial Data")
    
    data_view = st.selectbox("Select Data View", ["Main Financial Data", "Department Data"])
    
    if data_view == "Main Financial Data":
        st.dataframe(filtered_main.style.format({
            'Revenue': '${:,.0f}',
            'Expenses': '${:,.0f}',
            'Profit': '${:,.0f}',
            'Profit Margin': '{:.1%}'
        }), use_container_width=True, height=400)
    else:
        st.dataframe(filtered_dept.style.format({
            'Revenue': '${:,.0f}',
            'Expenses': '${:,.0f}',
            'Profit': '${:,.0f}'
        }), use_container_width=True, height=400)

# Footer with additional information
st.markdown("---")
st.success("🚀 Dashboard successfully loaded with enhanced features!")
st.info("""
**New Features Added:**
- 📈 Advanced visualizations with interactive tabs
- 🔍 Enhanced filtering and analytics
- 📊 Multiple chart types and heatmaps
- 📥 Improved data export options
- 🎨 Professional styling and UX improvements
""")

st.warning("📊 This dashboard uses auto-generated financial data for demonstration purposes. Connect to your real data source for production use.")