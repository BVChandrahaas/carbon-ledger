import streamlit as st

st.set_page_config(page_title="Settings | Carbon Ledger", layout="wide")

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
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        border-bottom: 2px solid #e5e7eb;
        border-radius: 12px 12px 0 0;
        padding: 16px 16px 0 16px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 500;
        color: #6b7280;
        background-color: transparent;
        font-size: 15px;
    }
    
    .stTabs [aria-selected="true"] {
        color: #2563eb;
        border-bottom: 2px solid #2563eb;
        background-color: transparent;
    }
    
    .settings-section {
        background: white;
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
    }
    
    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 8px;
    }
    
    .section-description {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 24px;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 15px;
        background: #ffffff;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    label {
        font-size: 14px;
        font-weight: 600;
        color: #374151;
        margin-bottom: 8px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 15px;
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
</style>
""", unsafe_allow_html=True)

st.title("Settings")
st.markdown('<p class="subtitle">Manage your application-wide and organization-specific configurations.</p>', unsafe_allow_html=True)

if 'org_id' not in st.session_state:
    st.warning("Please select an organization from the Home page first.")
else:
    # Create tabs
    tabs = st.tabs(["Organization", "Accounts", "Facilities", "Integrations"])
    
    # Organization Tab
    with tabs[0]:
        # Organization Profile Section
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Organization Profile</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-description">View and update your organization\'s general information.</div>', unsafe_allow_html=True)
        
        org_name = st.text_input(
            "Organization Name",
            value="Carbon Ledger Inc.",
            help="The legal name of your organization"
        )
        
        contact_email = st.text_input(
            "Contact Email",
            value="contact@carbonledger.com",
            help="Primary contact email for your organization"
        )
        
        industry_type = st.selectbox(
            "Industry Type",
            ["Manufacturing", "Technology", "Retail", "Healthcare", "Finance", "Energy", "Transportation", "Other"],
            index=0,
            help="Select the primary industry sector"
        )
        
        if st.button("Save Changes", key="save_org"):
            st.success("Organization profile updated successfully!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Regional & Time Settings Section
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Regional & Time Settings</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-description">Configure time zone and regional preferences for reporting.</div>', unsafe_allow_html=True)
        
        time_zone = st.selectbox(
            "Time Zone",
            [
                "UTC+00:00 London",
                "UTC-05:00 New York",
                "UTC-08:00 Los Angeles",
                "UTC+01:00 Paris",
                "UTC+08:00 Singapore",
                "UTC+09:00 Tokyo"
            ],
            index=0,
            help="Select your organization's primary time zone"
        )
        
        currency = st.selectbox(
            "Currency",
            [
                "USD - United States Dollar",
                "EUR - Euro",
                "GBP - British Pound",
                "JPY - Japanese Yen",
                "CNY - Chinese Yuan"
            ],
            index=0,
            help="Select your preferred currency for financial reporting"
        )
        
        if st.button("Update Regional Settings", key="save_regional"):
            st.success("Regional settings updated successfully!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Accounts Tab
    with tabs[1]:
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">User Accounts</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-description">Manage user accounts and permissions for your organization.</div>', unsafe_allow_html=True)
        
        st.info("User management features coming soon. Contact your administrator to add or modify user accounts.")
        
        # Sample user table
        st.markdown("### Current Users")
        users_data = {
            "Name": ["Admin User", "John Doe", "Jane Smith"],
            "Email": ["admin@company.com", "john@company.com", "jane@company.com"],
            "Role": ["Administrator", "Editor", "Viewer"],
            "Status": ["Active", "Active", "Active"]
        }
        st.table(users_data)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Facilities Tab
    with tabs[2]:
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Facilities Management</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-description">Add and manage facilities for your organization.</div>', unsafe_allow_html=True)
        
        try:
            api = st.session_state.api
            org_id = st.session_state.org_id
            
            facilities = api.get_facilities(org_id)
            
            if facilities['results']:
                st.markdown("### Your Facilities")
                for fac in facilities['results']:
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.markdown(f"**{fac['name']}**")
                    with col2:
                        st.markdown(f"_{fac.get('location', 'No location')}_")
                    with col3:
                        st.button("Edit", key=f"edit_{fac['id']}", use_container_width=True)
            else:
                st.info("No facilities found. Add your first facility below.")
            
            st.markdown("---")
            
            st.markdown("### Add New Facility")
            
            new_fac_name = st.text_input("Facility Name", placeholder="e.g., Main Office")
            new_fac_location = st.text_input("Location", placeholder="e.g., New York, USA")
            
            if st.button("Add Facility", key="add_facility"):
                st.success("Facility added successfully!")
            
        except Exception as e:
            st.error(f"Error loading facilities: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Integrations Tab
    with tabs[3]:
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Integrations</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-description">Connect Carbon Ledger with third-party services and data sources.</div>', unsafe_allow_html=True)
        
        st.info("Integration features coming soon. Future integrations will include energy providers, accounting software, and IoT sensors.")
        
        # Sample integrations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin-bottom: 16px;">
                <h4 style="margin-top: 0;">Analytics Platform</h4>
                <p style="color: #6b7280; font-size: 14px;">Connect to advanced analytics and reporting tools.</p>
                <button style="background: #f3f4f6; border: 1px solid #d1d5db; border-radius: 6px; padding: 8px 16px; cursor: pointer;">
                    Coming Soon
                </button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin-bottom: 16px;">
                <h4 style="margin-top: 0;">Energy Provider</h4>
                <p style="color: #6b7280; font-size: 14px;">Automatically import energy consumption data.</p>
                <button style="background: #f3f4f6; border: 1px solid #d1d5db; border-radius: 6px; padding: 8px 16px; cursor: pointer;">
                    Coming Soon
                </button>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 13px; padding: 24px 0; margin-top: 48px; border-top: 1px solid #e5e7eb;">
    © 2026 Carbon Ledger. All rights reserved.
</div>
""", unsafe_allow_html=True)