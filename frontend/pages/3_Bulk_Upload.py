import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bulk Upload | Carbon Ledger", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #ffffff;
        padding: 40px 60px;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    h1 {
        font-size: 32px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 12px;
    }
    
    .subtitle {
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 48px;
        line-height: 1.6;
    }
    
    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 16px;
        margin-top: 0;
        padding-top: 0;
    }
    
    .section-text {
        color: #6b7280;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    .stDownloadButton > button {
        background: #4F46E5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.2s;
    }
    
    .stDownloadButton > button:hover {
        background: #4338CA;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    .upload-area {
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 80px 48px;
        text-align: center;
        background: #fafbfc;
        transition: all 0.2s;
        margin-bottom: 24px;
    }
    
    .upload-area:hover {
        border-color: #4F46E5;
        background: #f8f9ff;
    }
    
    .upload-icon {
        font-size: 64px;
        margin-bottom: 20px;
        color: #6b7280;
    }
    
    .upload-text {
        color: #111827;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    .upload-subtext {
        color: #6b7280;
        font-size: 14px;
    }
    
    .stButton > button {
        background: #4F46E5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: #4338CA;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    .stButton > button:disabled {
        background: #d1d5db !important;
        color: #9ca3af !important;
        cursor: not-allowed;
        box-shadow: none !important;
    }

    .stButton > button:not(:disabled) {
        background: #4F46E5 !important;
        color: white !important;
    }
    
    [data-testid="stFileUploader"] {
        display: none;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 14px;
        padding: 32px 0;
        margin-top: 80px;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Success message styling */
    .element-container:has(.stSuccess) {
        margin-top: 16px;
        margin-bottom: 16px;
    }
    
    /* Info message styling */
    .element-container:has(.stInfo) {
        margin-top: 12px;
        margin-bottom: 16px;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        margin-top: 16px;
        margin-bottom: 16px;
    }
    
    /* Preview title */
    h3 {
        font-size: 18px;
        font-weight: 600;
        color: #111827;
        margin-top: 24px;
        margin-bottom: 12px;
    }
    
    /* Warning box */
    .stWarning {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 16px;
        border-radius: 8px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("Bulk Upload Emissions")
st.markdown('<p class="subtitle">Efficiently import your carbon emission data using CSV files. Follow the steps below to ensure a smooth upload process.</p>', unsafe_allow_html=True)

if 'org_id' not in st.session_state:
    st.warning("Please select an organization from the Home page first.")
else:
    api = st.session_state.api
    org_id = st.session_state.org_id
    
    # Download CSV Template Section - no extra spacing div
    st.markdown('<h2 class="section-title">Download CSV Template</h2>', unsafe_allow_html=True)
    st.markdown('''
    <div class="section-text">
        To ensure data consistency and accuracy, please download our pre-formatted CSV template. 
        It includes all the necessary columns for your emission records, simplifying the upload process.
    </div>
    ''', unsafe_allow_html=True)
    
    # Template data
    template_data = {
        'facility_id': ['(facility_uuid)', '(facility_uuid)'],
        'scope': ['scope1', 'scope2'],
        'category': ['Company Fleet Fuel', 'Electricity Consumption'],
        'subcategory': ['Diesel', 'Grid'],
        'quantity': [500, 12000],
        'unit': ['liters', 'kWh'],
        'emission_factor_used': [2.687, 0.712],
        'activity_date': ['2024-10-26', '2024-10-25'],
        'notes': ['Monthly fuel purchase', 'Office electricity bill']
    }
    df_template = pd.DataFrame(template_data)
    csv = df_template.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        "Download Template",
        csv,
        "emissions_template.csv",
        "text/csv",
        key='download-csv',
        use_container_width=False
    )
    
    # Add spacing before next section
    st.markdown("<div style='margin-top: 56px;'></div>", unsafe_allow_html=True)
    
    # Upload Emission Data Section
    st.markdown('<h2 class="section-title">Upload Emission Data</h2>', unsafe_allow_html=True)
    
    # File uploader (hidden, but functional)
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        label_visibility="collapsed",
        key="csv_uploader"
    )
    
    # Custom upload area with click functionality
    if uploaded_file is None:
        st.markdown('''
        <div class="upload-area">
            <div class="upload-text">Drag & drop your CSV file here or click to browse</div>
            <div class="upload-subtext">Accepted formats: CSV only. Max file size: 10MB.</div>
        </div>
        ''', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        
        # Preview the uploaded file
        try:
            df_preview = pd.read_csv(uploaded_file)
            st.markdown("### File Preview")
            st.dataframe(df_preview.head(5), use_container_width=True)
            
            st.info(f"Found {len(df_preview)} records in the file")
            
            # Reset file pointer for upload
            uploaded_file.seek(0)
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    # Upload button aligned to the right
    col1, col2 = st.columns([4, 1])
    
    with col2:
        if uploaded_file is not None:
            if st.button("Upload Files", use_container_width=True):
                with st.spinner("Processing file..."):
                    try:
                        # Reset file pointer
                        uploaded_file.seek(0)
                        
                        result = api.upload_bulk_csv(org_id, uploaded_file)
                        
                        st.success(f"Upload completed! Status: {result.get('processing_status', 'completed')}")
                        
                        if result.get('records_created', 0) > 0:
                            st.info(f"Records created: {result['records_created']}")
                        
                        if result.get('error_message'):
                            st.warning(f"Note: {result['error_message']}")
                        
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"Upload failed: {str(e)}")
        else:
            st.button("Upload Files", disabled=False, use_container_width=True)
    
    # Footer
    st.markdown('<div class="footer">© 2026 Carbon Ledger. All rights reserved.</div>', unsafe_allow_html=True)