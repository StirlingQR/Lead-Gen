# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote
import smtplib
from email.message import EmailMessage

# Configure page
st.set_page_config(
    page_title="Stirling Q&R Lead Generation",
    page_icon="📈",
    layout="centered"
)

# GitHub configuration
GITHUB_USER = "stirlington"
REPO_NAME = "Lead-Gen"
BRANCH = "main"
PDF_FILENAME = "Top 5 Considerations Before Signing an Exclusive Agency Agreement.pdf"
ENCODED_FILENAME = quote(PDF_FILENAME)
PDF_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ENCODED_FILENAME}"

# Session state setup
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def display_logo():
    try:
        st.image("Stirling_QR_Logo.png", use_container_width=True)
    except Exception as e:
        st.error(f"Missing logo file: {str(e)}")
        st.stop()

def send_alert(name, email):
    # Configure your SMTP settings here
    pass  # Add your email sending logic

# Login management
if not st.session_state.logged_in:
    if st.button("Admin Login", key="admin_login"):
        st.session_state.show_login = True
else:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.show_login = False
        st.rerun()

if 'show_login' in st.session_state and st.session_state.show_login:
    with st.form("Login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Authenticate"):
            if username == "chris@stirlingqr.com" and password == "Measure897!":
                st.session_state.logged_in = True
                st.session_state.show_login = False
                st.rerun()
            else:
                st.error("Invalid credentials")

if st.session_state.logged_in:
    st.title("🔐 Leads Dashboard")
    try:
        leads_df = pd.read_csv("leads.csv")
        st.dataframe(
            leads_df.style.format({"Phone": lambda x: f"{x}"),
            use_container_width=True
        )
        
        if st.download_button(
            label="Export Leads",
            data=leads_df.to_csv(index=False),
            file_name="stirling_leads.csv",
            mime="text/csv"
        ):
            st.success("Exported successfully")
            
    except FileNotFoundError:
        st.warning("No leads collected yet")
    st.stop()

# Main Form
if not st.session_state.submitted:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("Download Our Agency Agreement Guide")
    
    with st.form("lead_form", clear_on_submit=True):
        name = st.text_input("Full Name*")
        email = st.text_input("Work Email*")
        phone = st.text_input("Direct Phone*")
        company = st.text_input("Company Name")
        
        submitted = st.form_submit_button("Get Your Copy Now")
        
        if submitted:
            if all([name, email, phone]):
                new_entry = {
                    "Name": name,
                    "Email": email,
                    "Phone": phone.replace(" ", ""),
                    "Company": company,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                try:
                    existing = pd.read_csv("leads.csv")
                    updated = pd.concat([existing, pd.DataFrame([new_entry])])
                except FileNotFoundError:
                    updated = pd.DataFrame([new_entry])
                
                updated.to_csv("leads.csv", index=False)
                send_alert(name, email)
                st.session_state.submitted = True
                st.rerun()
            else:
                st.error("Please complete required fields")

# Success Page
else:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        display_logo()
    
    st.title("🎉 Your Guide is Ready!")
    st.success("✅ Guide successfully downloaded! Check your email")
    
    # Auto-download and preview
    st.markdown(f"""
    <a id="auto-dl" href="{PDF_URL}" download hidden></a>
    <script>
        document.getElementById('auto-dl').click();
    </script>
    <iframe src="https://docs.google.com/viewer?url={PDF_URL}&embedded=true" 
            width="100%" 
            height="600" 
            style="border:none;margin-top:2rem">
    </iframe>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    """, unsafe_allow_html=True)
