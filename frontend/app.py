import streamlit as st
from utils.api_client import APIClient

# Page configuration
st.set_page_config(
    page_title="Carbon Ledger",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the new modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #ffffff;
        padding: 20px 60px;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e5e7eb;
    }
    
    /* Sidebar logo */
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 20px 16px;
        margin-bottom: 32px;
    }
    
    .sidebar-logo-icon {
        width: 36px;
        height: 36px;
        background: #4F46E5;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
        font-weight: 600;
    }
    
    .sidebar-logo-text {
        font-size: 18px;
        font-weight: 600;
        color: #4F46E5;
    }
    
    /* Sidebar menu items */
    .sidebar-menu-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        margin: 4px 8px;
        border-radius: 8px;
        color: #374151;
        font-size: 15px;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .sidebar-menu-item:hover {
        background-color: #e5e7eb;
    }
    
    .sidebar-menu-icon {
        font-size: 18px;
    }
    
    /* Sidebar configuration */
    .sidebar-config {
        margin-top: 32px;
        padding: 16px;
    }
    
    .sidebar-config-title {
        font-size: 13px;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }
    
    /* Sidebar user profile */
    .sidebar-user {
        margin-top: 100px;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px;
        background: #ffffff;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    
    .sidebar-user-avatar {
        width: 40px;
        height: 40px;
        background: #d1d5db;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    
    .sidebar-user-info {
        flex: 1;
    }
    
    .sidebar-user-name {
        font-weight: 600;
        font-size: 14px;
        color: #111827;
    }
    
    .sidebar-user-email {
        font-size: 12px;
        color: #6b7280;
    }
    
    /* Main content */
    h1 {
        font-size: 44px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 20px;
        text-align: center;
        line-height: 1.2;
    }
    
    h2 {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
        margin-top: 80px;
        margin-bottom: 40px;
    }
    
    .subtitle {
        color: #6b7280;
        font-size: 17px;
        text-align: center;
        margin-bottom: 36px;
        line-height: 1.6;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 40px 0 60px 0;
    }
    
    /* Buttons */
    .btn-primary {
        background: #4F46E5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 14px 32px;
        font-weight: 600;
        font-size: 15px;
        cursor: pointer;
        transition: all 0.2s;
        display: inline-block;
        text-decoration: none;
        margin: 0 8px;
    }
    
    .btn-primary:hover {
        background: #4338CA;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    .btn-secondary {
        background: white;
        color: #374151;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 14px 32px;
        font-weight: 600;
        font-size: 15px;
        cursor: pointer;
        transition: all 0.2s;
        display: inline-block;
        text-decoration: none;
        margin: 0 8px;
    }
    
    .btn-secondary:hover {
        background: #f9fafb;
        border-color: #9ca3af;
    }
    
    /* Feature cards */
    .feature-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 32px 24px;
        text-align: center;
        height: 320px;
        transition: all 0.2s;
        margin-bottom: 15px;
    }
    
    .feature-card:hover {
        border-color: #4F46E5;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .feature-title {
        font-size: 20px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 12px;
    }
    
    .feature-description {
        color: #6b7280;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    .feature-button {
        background: #f9fafb;
        color: #374151;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 8px 20px;
        font-weight: 500;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s;
        display: inline-block;
    }
    
    .feature-button:hover {
        background: #f3f4f6;
        border-color: #d1d5db;
    }
    
    /* Feature highlights */
    .feature-highlights {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        gap: 40px;
        margin-top: 80px;
        padding: 40px 0;
        border-top: 1px solid #e5e7eb;
    }
    
    .feature-highlight {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #374151;
        font-size: 15px;
        font-weight: 500;
    }
    
    .feature-highlight-icon {
        color: #10b981;
        font-size: 18px;
        font-weight: bold;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 14px;
        padding: 32px 0;
        margin-top: 64px;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Deploy button in top right */
    .deploy-button {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        color: #374151;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
        font-size: 14px;
        cursor: pointer;
        z-index: 1000;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom button styling */
    .stButton > button {
        background: #4F46E5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 14px 32px;
        font-weight: 600;
        font-size: 15px;
        width: 100%;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: #4338CA;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    /* Sidebar buttons */
    button[key="add_emissions_sidebar"],
    button[key="bulk_upload_sidebar"],
    button[key="settings_sidebar"] {
        background: #4F46E5 !important;
        color: white !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        margin-bottom: 8px !important;
    }
    
    button[key="add_emissions_sidebar"]:hover,
    button[key="bulk_upload_sidebar"]:hover,
    button[key="settings_sidebar"]:hover {
        background: #4338CA !important;
    }
    
    /* Secondary button for Learn More */
    button[key="learn_more"] {
        background: white !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
    }
    
    button[key="learn_more"]:hover {
        background: #f9fafb !important;
        border-color: #9ca3af !important;
    }
    
    /* Select box styling */
    .stSelectbox > div > div > select {
        border: 1px solid #d1d5db;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
        background: white;
    }
    
    .stSelectbox label {
        font-size: 13px;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize API Client
if 'api' not in st.session_state:
    st.session_state.api = APIClient()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">◆</div>
        <div class="sidebar-logo-text">Carbon Ledger</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu items with better styling
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    if st.button("➕  Add Emissions", key="add_emissions_sidebar", use_container_width=True):
        st.switch_page("pages/2_Add_Emissions.py")
    
    if st.button("⬆  Bulk Upload", key="bulk_upload_sidebar", use_container_width=True):
        st.switch_page("pages/3_Bulk_Upload.py")
    
    if st.button("⚙  Settings", key="settings_sidebar", use_container_width=True):
        st.switch_page("pages/4_Settings.py")
    
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-config-title">CONFIGURATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-config-title" style="margin-top: 8px; margin-bottom: 8px;">ORGANIZATION</div>', unsafe_allow_html=True)
    
    try:
        orgs = st.session_state.api.get_organizations()
        org_names = {o['name']: o['id'] for o in orgs['results']}
        
        if org_names:
            selected_org_name = st.selectbox(
                "Organization",
                list(org_names.keys()),
                key="org_select",
                label_visibility="collapsed"
            )
            st.session_state.org_id = org_names[selected_org_name]
            st.session_state.org_name = selected_org_name
            
            # Show selected organization with checkmark
            st.markdown(f"""
            <div style="padding: 10px 12px; background: #f0fdf4; border: 1px solid #86efac; border-radius: 6px; margin-top: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #16a34a;">✓</span>
                    <span style="color: #166534; font-size: 14px; font-weight: 500;">{selected_org_name}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No organizations found")
    except Exception as e:
        st.error(f"Connection error: {e}")
    
    # User profile at bottom
    st.markdown("""
    <div class="sidebar-user">
        <div class="sidebar-user-avatar">👤</div>
        <div class="sidebar-user-info">
            <div class="sidebar-user-name">Admin User</div>
            <div class="sidebar-user-email">admin@company.com</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Deploy button (top right)
    st.markdown("""
    <div class="deploy-button">Deploy</div>
    """, unsafe_allow_html=True)
    
    # Hero section
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    
    st.title("Welcome to Carbon Ledger")
    st.markdown(
        '<p class="subtitle">Track, calculate, and report your organization\'s carbon footprint with precision.</p>',
        unsafe_allow_html=True
    )
    
    # Hero buttons - centered
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        btn_col1, btn_col2 = st.columns([1, 1], gap="small")
        with btn_col1:
            if st.button("Get Started", key="get_started", use_container_width=True):
                st.switch_page("pages/1_Dashboard.py")
        with btn_col2:
            if st.button("Learn More", key="learn_more", use_container_width=True):
                pass  # Add learn more action
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key Features section
    st.markdown("<h2 style='margin-left: 0;'>Key Features</h2>", unsafe_allow_html=True)
    
    # Add spacing
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div style="width: 64px; height: 64px; background: #f0f4ff; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 17H7V10H9V17ZM13 17H11V7H13V17ZM17 17H15V13H17V17ZM19 19H5V5H19V19ZM19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3Z" fill="#4F46E5"/>
                </svg>
            </div>
            <div class="feature-title">Analytics Dashboard</div>
            <div class="feature-description">
                Gain insights into your emissions with interactive dashboards and real-time metrics.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore", key="btn_dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div style="width: 64px; height: 64px; background: #f0f4ff; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M14 2H6C4.9 2 4.01 2.9 4.01 4L4 20C4 21.1 4.89 22 5.99 22H18C19.1 22 20 21.1 20 20V8L14 2ZM16 18H8V16H16V18ZM16 14H8V12H16V14ZM13 9V3.5L18.5 9H13Z" fill="#4F46E5"/>
                </svg>
            </div>
            <div class="feature-title">Easy Data Entry</div>
            <div class="feature-description">
                Simplify data input for individual activities or bulk CSV uploads.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore", key="btn_add", use_container_width=True):
            st.switch_page("pages/2_Add_Emissions.py")
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div style="width: 64px; height: 64px; background: #f0f4ff; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 16H16V18H8V16ZM8 12H16V14H8V12ZM14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.89 22 5.99 22H18C19.1 22 20 21.1 20 20V8L14 2ZM18 20H6V4H13V9H18V20Z" fill="#4F46E5"/>
                </svg>
            </div>
            <div class="feature-title">Comprehensive Reporting</div>
            <div class="feature-description">
                Generate customizable and detailed reports for stakeholders and compliance.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore", key="btn_report", use_container_width=True):
            st.info("Reporting module coming soon!")
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div style="width: 64px; height: 64px; background: #f0f4ff; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM11 19.93C7.05 19.44 4 16.08 4 12C4 11.38 4.08 10.79 4.21 10.21L9 15V16C9 17.1 9.9 18 11 18V19.93ZM17.9 17.39C17.64 16.58 16.9 16 16 16H15V13C15 12.45 14.55 12 14 12H8V10H10C10.55 10 11 9.55 11 9V7H13C14.1 7 15 6.1 15 5V4.59C17.93 5.78 20 8.65 20 12C20 14.08 19.2 15.97 17.9 17.39Z" fill="#4F46E5"/>
                </svg>
            </div>
            <div class="feature-title">Seamless Integrations</div>
            <div class="feature-description">
                Connect with existing systems for automated data flow and enhanced functionality.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore", key="btn_settings", use_container_width=True):
            st.switch_page("pages/4_Settings.py")
    
    # Feature highlights
    st.markdown("""
    <div class="feature-highlights">
        <div class="feature-highlight">
            <span class="feature-highlight-icon">✓</span>
            <span>Real-time emission tracking</span>
        </div>
        <div class="feature-highlight">
            <span class="feature-highlight-icon">✓</span>
            <span>Multi-scope categorization</span>
        </div>
        <div class="feature-highlight">
            <span class="feature-highlight-icon">✓</span>
            <span>Automated calculations</span>
        </div>
        <div class="feature-highlight">
            <span class="feature-highlight-icon">✓</span>
            <span>Export & reporting capabilities</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="footer">© 2026 Carbon Ledger. All rights reserved.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()