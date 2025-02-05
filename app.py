# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Stirling Q&R Lead Generation",
    page_icon="📈",
    layout="centered"
)

# Initialize paths
LOGO_PATH = Path(__file__).parent / "Stirling_QR_Logo.png"
PDF_PATH = Path(__file__).parent / "document.pdf"

# Initialize session states
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# File handling function
def get_pdf_bytes():
    try:
        with open(PDF_PATH, "rb") as f:
            return f.read()
    except FileNotFoundError:
        st.error("⚠️ PDF document missing - please ensure 'document.pdf' exists in the root directory")
        st.stop()

# Logo display with error handling
def display_logo():
    try:
        st.image(str(LOGO_PATH), use_container_width=True)
    except FileNotFoundError:
        st.error("⚠️ Logo file missing - please ensure 'Stirling_QR_Logo.png' exists in the root directory")
        st.stop()

# Login sidebar
with st.sidebar:
    if not st.session_state.logged_in:
        st.title("Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username == "chris@stirlingqr.com" and password == "Measure897!":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

# Admin panel
if st.session_state.logged_in:
    st.title("🔐 Leads Dashboard")
    
    try:
        leads_df = pd.read_csv("leads.csv")
        st.dataframe(leads_df, use_container_width=True)
        
        csv = leads_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="leads.csv",
            mime="text/csv"
        )
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
            
    except FileNotFoundError:
        st.warning("No leads collected yet")
    
    st.stop()

# Main form logic
if not st.session_state.submitted:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("Download Our Quality Assurance Recruitment Guide")
    
    with st.form("lead_form"):
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone Number*")
        
        st.markdown("""
        *By entering your information, you consent to Stirling Q&R collecting and storing your details. 
        You are opting in to be contacted by our team via email or phone to discuss your recruitment needs. 
        Your data will be handled securely and will not be shared with third parties without your consent.*
        """)
        
        if st.form_submit_button("Download Now →"):
            if all([name, email, phone]):
                # Save lead to CSV
                new_lead = {
                    "Name": [name],
                    "Email": [email],
                    "Phone": [phone],
                    "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                }
                
                try:
                    existing = pd.read_csv("leads.csv")
                    updated = pd.concat([existing, pd.DataFrame(new_lead)])
                except FileNotFoundError:
                    updated = pd.DataFrame(new_lead)
                
                updated.to_csv("leads.csv", index=False)
                st.session_state.submitted = True
                st.rerun()
            else:
                st.error("Please complete all required fields")

# Thank you page
else:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("🎉 Download Complete!")
    st.balloons()
    
    # Trigger PDF download
    pdf_bytes = get_pdf_bytes()
    st.download_button(
        label="Download Guide (PDF)",
        data=pdf_bytes,
        file_name="QA_Recruitment_Guide.pdf",
        mime="application/octet-stream"
    )
    
    st.markdown("""
    **Your document should begin downloading automatically.**  
    If it doesn't start within a few seconds, click the download button above.
    
    ### Next Steps:
    1. Check your email for confirmation
    2. Expect our follow-up within 24 hours
    3. Save our contact: +44 1234 567890
    
    *Looking forward to helping with your QA recruitment needs!*
    """)
