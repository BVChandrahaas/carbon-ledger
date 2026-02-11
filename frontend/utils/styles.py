import streamlit as st

def apply_custom_style():
    """
    Applies custom CSS to make Streamlit look like a professional dashboard.
    """
    st.markdown("""
    <style>
        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Global styles */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Background color */
        .main {
            background-color: #F8FAFC;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Card styling */
        .stMarkdown div[data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #1E293B !important;
        }
        
        .card {
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            margin-bottom: 20px;
        }

        .card-title {
            color: #64748B;
            font-size: 0.875rem;
            font-weight: 500;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .card-value {
            color: #0F172A;
            font-size: 1.5rem;
            font-weight: 700;
        }

        .card-delta {
            font-size: 0.875rem;
            margin-top: 4px;
        }

        .delta-positive {
            color: #EF4444;
        }

        .delta-negative {
            color: #10B981;
        }

        /* Header styling */
        .dashboard-header {
            margin-bottom: 32px;
        }

        .dashboard-title {
            font-size: 1.875rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 4px;
        }

        .dashboard-subtitle {
            font-size: 1rem;
            color: #64748B;
        }

        /* Buttons */
        .stButton>button {
            border-radius: 8px;
            font-weight: 500;
            padding: 0.5rem 1rem;
            background-color: #2563EB;
            color: white;
            border: none;
            transition: all 0.2s;
        }

        .stButton>button:hover {
            background-color: #1D4ED8;
            border: none;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-bottom: 2px solid transparent;
            color: #64748B;
            font-weight: 500;
        }

        .stTabs [aria-selected="true"] {
            border-bottom: 2px solid #2563EB !important;
            color: #2563EB !important;
        }

        /* Badges */
        .badge {
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
            display: inline-block;
        }

        .badge-scope1 { background-color: #EFF6FF; color: #1E40AF; border: 1px solid #BFDBFE; }
        .badge-scope2 { background-color: #F0FDF4; color: #166534; border: 1px solid #BBF7D0; }
        .badge-scope3 { background-color: #FDF2F8; color: #9D174D; border: 1px solid #FBCFE8; }

    </style>
    """, unsafe_allow_html=True)

def header(title, subtitle):
    st.markdown(f"""
    <div class="dashboard-header">
        <div class="dashboard-title">{title}</div>
        <div class="dashboard-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def kpi_card(title, value, delta=None, delta_type="neutral"):
    delta_html = ""
    if delta:
        delta_class = "delta-positive" if delta_type == "increase" else "delta-negative" if delta_type == "decrease" else ""
        delta_html = f'<div class="card-delta {delta_class}">{delta}</div>'
    
    st.markdown(f"""
    <div class="card">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def card_begin():
    st.markdown('<div class="card">', unsafe_allow_html=True)

def card_end():
    st.markdown('</div>', unsafe_allow_html=True)

def sidebar_header():
    """
    Adds the professional logo and title to the sidebar.
    """
    st.sidebar.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 32px; padding: 0 16px;">
            <div style="background-color: #2563EB; color: white; padding: 8px; border-radius: 8px; font-weight: bold; font-size: 20px; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">
                CL
            </div>
            <div style="font-size: 20px; font-weight: 700; color: #0F172A;">
                Carbon Ledger
            </div>
        </div>
    """, unsafe_allow_html=True)
