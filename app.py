# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote

# Configure page
st.set_page_config(
    page_title="Stirling Q&R Lead Generation",
    page_icon="📈",
    layout="centered"
)

# GitHub configuration - REPLACE WITH YOUR DETAILS
GITHUB_USER = "stirlington"  # Your GitHub username
REPO_NAME = "Lead-Gen"       # Your repository name
BRANCH = "main"              # Your branch name
PDF_FILENAME = "Top 5 Considerations Before Signing an Exclusive Agency Agreement.pdf"

# Encoded PDF URL
ENCODED_FILENAME = quote(PDF_FILENAME)
PDF_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ENCODED_FILENAME}"

# Session state management
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def display_logo():
    """Display logo with error handling"""
    try:
        st.image("Stirling_QR_Logo.png", use_container_width=True)
    except Exception as e:
        st.error(f"Missing logo file: {str(e)}")
        st.stop()

# Login management
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

if not st.session_state.submitted:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("Download Our Exclusive Agency Agreement Guide")
    
    with st.form("lead_form"):
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone Number*")
        company = st.text_input("Company Name (optional)")
        
        st.markdown("""*By entering your information...*""")  # Your privacy text
        
        if st.form_submit_button("Download Now →"):
            if all([name, email, phone]):
                new_lead = pd.DataFrame({
                    "Name": [name],
                    "Email": [email],
                    "Phone": [phone],
                    "Company": [company],
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                try:
                    existing = pd.read_csv("leads.csv")
                    updated = pd.concat([existing, new_lead])
                except FileNotFoundError:
                    updated = new_lead
                
                updated.to_csv("leads.csv", index=False)
                st.session_state.submitted = True
                st.rerun()

else:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("🎉 Your Guide is Ready!")
    st.balloons()
    
    st.markdown(f"""
    <iframe src="https://docs.google.com/viewer?url={PDF_URL}&embedded=true" 
            width="100%" 
            height="800px" 
            style="border: none; margin-top: 20px;">
    </iframe>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    [Download PDF Guide]({PDF_URL})
    """)
