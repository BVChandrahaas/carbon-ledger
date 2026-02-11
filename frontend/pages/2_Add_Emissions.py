import streamlit as st
import datetime
from utils.api_client import APIClient

st.set_page_config(page_title="Add Emissions | Carbon Ledger", layout="centered")

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
    
    .form-section {
        background: white;
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
    }
    
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 20px;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 15px;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stDateInput > div > div > input:focus {
        border-color: #4F46E5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    label {
        font-size: 14px;
        font-weight: 600;
        color: #374151;
        margin-bottom: 8px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 15px;
        width: 100%;
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    .helper-text {
        font-size: 13px;
        color: #6b7280;
        margin-top: 4px;
    }
    
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #4F46E5;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
        color: #1e40af;
        font-size: 14px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("Add New Emission Record")

if 'org_id' not in st.session_state:
    st.warning("Please select an organization from the Home page first.")
else:
    # Initialize API if not present
    if 'api' not in st.session_state:
        from utils.api_client import APIClient
        st.session_state.api = APIClient()
        
    api = st.session_state.api
    org_id = st.session_state.org_id
    
    # Activity Details Section
    st.markdown('<div class="form-section"><div class="section-title">Activity Details</div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Activity Type
        try:
            efs = api.get_emission_factors()
            def get_label(f):
                sub = f" - {f['subcategory']}" if f['subcategory'] else ""
                return f"{f['category']}{sub} ({f['unit']}) [{f['region']}]"
            
            ef_options = {get_label(f): f for f in efs['results']}
            sorted_labels = sorted(ef_options.keys())
            
            selected_ef_label = st.selectbox(
                "Activity Type",
                sorted_labels,
                help="Select the type of emission activity"
            )
            selected_ef = ef_options[selected_ef_label]
        except Exception as e:
            st.error(f"Error loading emission factors: {e}")
            selected_ef = None
    
    if selected_ef:
        with col2:
            # Scope (display only, derived from activity type)
            scope_display = selected_ef['scope'].replace('scope', 'Scope ')
            st.selectbox(
                "Scope",
                [scope_display],
                disabled=True,
                help="Scope is automatically determined by activity type"
            )
        
        # Emission Quantity Section
        st.markdown('<div class="form-section"><div class="section-title">Emission Quantity</div></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            quantity = st.number_input(
                "Quantity",
                min_value=0.0,
                value=1500.0,
                format="%.2f",
                help=f"Enter the quantity in {selected_ef['unit']}"
            )
            st.markdown(f'<div class="helper-text">e.g., 1500</div>', unsafe_allow_html=True)
        
        with col2:
            st.selectbox(
                "Unit",
                [selected_ef['unit']],
                disabled=True,
                help="Unit is determined by activity type"
            )
        
        # Emission Date Section
        st.markdown('<div class="form-section"><div class="section-title">Emission Date</div></div>', unsafe_allow_html=True)
        
        activity_date = st.date_input(
            "Date",
            value=datetime.date.today(),
            help="Select the date when this emission activity occurred"
        )
        st.markdown(f'<div class="helper-text">Pick a date</div>', unsafe_allow_html=True)
        
        # Additional Notes Section
        st.markdown('<div class="form-section"><div class="section-title">Additional Notes</div></div>', unsafe_allow_html=True)
        
        notes = st.text_area(
            "Notes",
            placeholder="Any additional details or context for this emission (optional)",
            help="Optional field for additional information",
            label_visibility="collapsed"
        )
        st.markdown(f'<div class="helper-text">Any additional details or context for this emission (optional)</div>', unsafe_allow_html=True)
        
        # Submit button
        if st.button("Save Emission", use_container_width=True):
            try:
                # Get facility (use first available for demo)
                facilities = api.get_facilities(org_id)
                if not facilities['results']:
                    st.error("No facilities found. Please create a facility in Settings first.")
                else:
                    fac_id = facilities['results'][0]['id']
                    
                    data = {
                        'organization': org_id,
                        'facility': fac_id,
                        'scope': selected_ef['scope'],
                        'category': selected_ef['category'],
                        'subcategory': selected_ef['subcategory'],
                        'quantity': quantity,
                        'unit': selected_ef['unit'],
                        'emission_factor_used': selected_ef['emission_factor_co2e'],
                        'emission_factor': selected_ef['id'],
                        'activity_date': activity_date.isoformat(),
                        'notes': notes,
                        'data_source': 'manual_entry'
                    }
                    
                    result = api.create_emission_record(data)
                    st.success(f"Successfully recorded! Calculated: **{result['co2e_calculated']} kg CO2e**")
                    
                    st.markdown("""
                    <div class="info-box">
                        <strong>What's next?</strong><br>
                        • View this record on the Dashboard<br>
                        • Add more emission records<br>
                        • Download your emissions report
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Error saving record: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_detail = e.response.json()
                        st.error(f"Backend error: {error_detail}")
                    except:
                        pass
