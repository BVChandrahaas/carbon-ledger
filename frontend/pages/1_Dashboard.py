import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from utils.api_client import APIClient

st.set_page_config(page_title="Dashboard | Carbon Ledger", layout="wide")

# Apply same styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    h1 {
        font-size: 32px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 8px;
    }
    
    .subtitle {
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 32px;
    }
    
    [data-testid="stMetric"] {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #6b7280;
        font-weight: 500;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
    }
    
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
    }
    
    .chart-title {
        font-size: 18px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 8px;
    }
    
    .chart-subtitle {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 16px;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
    }
    
    thead tr {
        border-bottom: 1px solid #e5e7eb;
    }
    
    th {
        text-align: left;
        padding: 12px 16px;
        font-size: 12px;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    td {
        padding: 16px;
        font-size: 14px;
        color: #111827;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .scope-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .scope-1 {
        background: #dbeafe;
        color: #1e40af;
    }
    
    .scope-2 {
        background: #d1fae5;
        color: #065f46;
    }
    
    .scope-3 {
        background: #fef3c7;
        color: #92400e;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
    }
    
    .stDownloadButton > button {
        background: white;
        color: #6b7280;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Carbon Emissions Dashboard")
st.markdown('<p class="subtitle">A comprehensive overview of your organization\'s carbon footprint.</p>', unsafe_allow_html=True)

if 'org_id' not in st.session_state:
    st.warning("Please select an organization from the Home page first.")
else:
    # Initialize API if not present
    if 'api' not in st.session_state:
        st.session_state.api = APIClient()
        
    api = st.session_state.api
    org_id = st.session_state.org_id

    try:
        # Fetch data
        stats = api.get_dashboard_stats(org_id, period=None)
        records = api.get_emission_records(org_id)
        
        # Top metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_emissions = float(stats['total_emissions'])
            st.metric(
                label="Total Emissions",
                value=f"{total_emissions:,.0f}tCO2e",
                delta="+12% last month"
            )
        
        with col2:
            emissions_per_employee = total_emissions / 1000 if total_emissions > 0 else 0
            st.metric(
                label="Emissions per Employee",
                value=f"{emissions_per_employee:.1f}tCO2e/FTE",
                delta="Steady since Q3"
            )
        
        with col3:
            intensity = total_emissions / 3000 if total_emissions > 0 else 0
            st.metric(
                label="Emissions Intensity",
                value=f"{intensity:.1f}tCO2e/M$",
                delta="-5% from target"
            )
        
        with col4:
            record_count = int(stats.get('record_count', 0))
            st.metric(
                label="Total Records",
                value=f"{record_count:,}",
                delta=f"+{record_count - 100} this month" if record_count > 100 else "New"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container"><div class="chart-title">Emissions by Scope</div><div class="chart-subtitle">Breakdown of your carbon footprint by operational scope.</div></div>', unsafe_allow_html=True)
            
            scope_data = pd.DataFrame({
                'Scope': ['Scope 1', 'Scope 2', 'Scope 3'],
                'Emissions': [float(stats['scope1']), float(stats['scope2']), float(stats['scope3'])]
            })
            
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=scope_data['Scope'],
                    y=scope_data['Emissions'],
                    marker=dict(
                        color=['#4F46E5', '#10b981', '#f59e0b'],
                        cornerradius=8
                    ),
                    text=scope_data['Emissions'].apply(lambda x: f'{x:,.0f}'),
                    textposition='outside',
                )
            ])
            
            fig_bar.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showline=False, title=""),
                yaxis=dict(showgrid=True, gridcolor='#f3f4f6', showline=False, title="Emissions (tCO2e)"),
                font=dict(family="Inter", size=12, color="#6b7280"),
                showlegend=False
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            st.markdown('<div class="chart-container"><div class="chart-title">Monthly Emissions Trend</div><div class="chart-subtitle">Total carbon emissions over the past 12 months.</div></div>', unsafe_allow_html=True)
            
            # Generate sample monthly data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            emissions_trend = [180, 195, 200, 230, 235, 210, 245, 240, 260, 280, 285, 290]
            
            fig_line = go.Figure(data=go.Scatter(
                x=months,
                y=emissions_trend,
                mode='lines+markers',
                line=dict(color='#4F46E5', width=3),
                marker=dict(size=8, color='#4F46E5'),
                fill='tozeroy',
                fillcolor='rgba(79, 70, 229, 0.1)'
            ))
            
            fig_line.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showline=False, title=""),
                yaxis=dict(showgrid=True, gridcolor='#f3f4f6', showline=False, title="Total Emissions (tCO2e)"),
                font=dict(family="Inter", size=12, color="#6b7280"),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_line, use_container_width=True)
        
        # Recent emissions records
        st.markdown('<div class="chart-container"><div class="chart-title">Recent Emissions Records</div><div class="chart-subtitle">Latest entries for your carbon emissions.</div></div>', unsafe_allow_html=True)
        
        col_actions1, col_actions2 = st.columns([6, 1])
        with col_actions2:
            if st.button("Add New Record", use_container_width=True):
                st.switch_page("pages/2_Add_Emissions.py")
        
        with col_actions1:
            st.download_button(
                label="Download Report",
                data="Sample CSV data",
                file_name="emissions_report.csv",
                mime="text/csv",
                use_container_width=False
            )
        
        if records['results']:
            df_records = pd.DataFrame(records['results'])
            
            # Create custom HTML table
            table_html = "<table><thead><tr>"
            table_html += "<th>ACTIVITY</th><th>SCOPE</th><th>AMOUNT</th><th>UNIT</th><th>DATE</th>"
            table_html += "</tr></thead><tbody>"
            
            for _, row in df_records.head(7).iterrows():
                scope_class = f"scope-{row['scope'][-1]}" if 'scope' in row else "scope-1"
                scope_label = row.get('scope', 'N/A').replace('scope', 'Scope ')
                val = float(row.get('quantity', 0))
                
                table_html += "<tr>"
                table_html += f"<td>{row.get('category', 'N/A')}</td>"
                table_html += f'<td><span class="scope-badge {scope_class}">{scope_label}</span></td>'
                table_html += f"<td>{val:,.0f}</td>"
                table_html += f"<td>{row.get('unit', 'N/A')}</td>"
                table_html += f"<td>{row.get('activity_date', 'N/A')}</td>"
                table_html += "</tr>"
            
            table_html += "</tbody></table>"
            
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.info("No emission records found. Start by adding your first record!")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Please check your backend connection and try again.")
